# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401

# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame  # noqa
from datetime import datetime  # noqa
from typing import Optional, Union  # noqa
import pandas_ta as pdta

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,
                                IStrategy, IntParameter)
from freqtrade.exchange import timeframe_to_prev_date
# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import pandas_ta as pta
import freqtrade.vendor.qtpylib.indicators as qtpylib

######  Bollinger band function

def calc_BBLower(source, length, mult):
    basis = ta.SMA(source, int(length))
    dev = mult * ta.STDDEV(source, int(length))
    return basis - dev
    
def calc_BBUpper(source, length, mult):
    basis = ta.SMA(source, int(length))
    dev = mult * ta.STDDEV(source, int(length))
    return basis + dev

class deadzone(IStrategy):
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 3

    # Optimal timeframe for the strategy.
    timeframe = '15m'

    # Can this strategy go short?
    can_short: bool = False

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {
        "60": 0.1,
        "30": 1,
        "0": 1,
    }

    # Optimal stoploss designed for the strategy.
    # This attribute will be overridden if the config file contains "stoploss".
    stoploss = -1

    # Trailing stoploss
    #trailing_stop = True
    # trailing_only_offset_is_reached = False
    # trailing_stop_positive = 0.01
    # trailing_stop_positive_offset = 0.0  # Disabled / not configured

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True

    # These values can be overridden in the config.
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False
    use_custom_stoploss = True

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 30

    #______________________________________________________________________________
    #                            START STRATEGY PARAMS
    #_____________________________________________________________________________

    takeLong = True
    takeExtra = True
    takeShort = False

    active_days_of_week = [0,1,2,3,4]

    cooldownPeriod = IntParameter(0, 100, default=0, space="buy", optimize=False)

     #TP : RR
    riskLongMultip = DecimalParameter(0.1, 10, default=1.0, space="buy", decimals=1, optimize = True)  
    riskShortMultip = DecimalParameter(0.1, 10, default=1.0, space="buy", optimize = False, decimals=1)



    ## ATR BAND PARAMS
    ##----------
    sourceUpper = 'close'
    sourceLower = 'close'
    atrMultUpper = DecimalParameter(0.1, 3.5, default=2.0, space="buy", decimals=1) #ATR Long Stoploss
    atrMultLower = DecimalParameter(0.1, 3.5, default=2.0, space="buy", optimize= False, decimals=1) #ATR Shor tStoploss
    atrPeriod = IntParameter(10,20, default=14, optimize = False) # ATR length
    atrPeriods = [14]



    ## WAE Period
    bollinger_band_lengths = np.arange(17,24,1)
    bb_mults = np.arange(1,21,1)
    deadzonemultipliers = np.around(np.arange(4.0,9.0,0.1), 1)

### uncomment for fixed values during single backtest.  (dont use in optimmization)
###----------------------------
#    bollinger_band_lengths = [20]
#    bb_mults = [2]
#    deadzonemultipliers = [7.2]
###----------------------------

    #Sensitivity = IntParameter(50, 250, default = 50, space = "buy", optimize = True)
    Sensitivity = CategoricalParameter([50, 250], default = 50, space = "buy", optimize = True)
    fastLength = IntParameter(1, 250, default = 25, space = "buy", optimize = False) #FastEMALength 
    slowLength = IntParameter(1, 250, default = 150, space = "buy", optimize = False) #SlowEMALength 
    bb_mult= IntParameter(bb_mults[0], bb_mults[-1], default=bb_mults[0], space="buy", optimize= False) # DeadZone Multiplier
    channelLength = IntParameter( bollinger_band_lengths[0], bollinger_band_lengths[-1], default = bollinger_band_lengths[0], space = "buy", optimize = True) # BB Length
    
    deadzonemultiplier = DecimalParameter(deadzonemultipliers[0], deadzonemultipliers[-1], default=deadzonemultipliers[0], space="buy", optimize= True, decimals=1) # DeadZone Multiplier

    #______________________________________________________________________________
    #                           END STRATEGY PARAMS
    #______________________________________________________________________________
    


    # Optional order type mapping.
    order_types = {
        'entry': 'limit',
        'exit': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # Optional order time in force.
    order_time_in_force = {
        'entry': 'gtc',
        'exit': 'gtc'
    }
    
    @property
    def plot_config(self):
        return {
            # Main plot indicators (Moving averages, ...)
            'main_plot': {
                'tema': {},
                'sar': {'color': 'white'},
            },
            'subplots': {
                # Subplots - each dict defines one additional plot
                "MACD": {
                    'macd': {'color': 'blue'},
                    'macdsignal': {'color': 'orange'},
                },
                "RSI": {
                    'rsi': {'color': 'red'},
                }
            }
        }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:


        #####
        ## DEADZONE
        #####
        for guy in self.deadzonemultipliers:
           dataframe['deadzone' + str(guy)] = pdta.rma(ta.TRANGE(dataframe), 100) * guy

        #####
        # MACD
        #####
        macd = ta.MACD(dataframe, fastperiod=self.fastLength.value, slowperiod=self.slowLength.value)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']


        #####
        ## ATR
        #####
        for guy in self.atrPeriods:
            dataframe['atr_' + str(guy)] = ta.ATR(dataframe, guy)
        

        #####
        # Bollinger Bands
        #####
        for bblen in self.bollinger_band_lengths:
            for mult in self.bb_mults:            
                mod = str(bblen)
                mod2 = str(mult)
                #bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=bblen, stds=2)
                dataframe['bb_lowerband_' + mod + '_' + mod2] = calc_BBLower(dataframe['close'], bblen, mult)
                dataframe['bb_upperband_' + mod + '_' + mod2] = calc_BBUpper(dataframe['close'], bblen, mult)

        
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        
        """
        Based on TA indicators, populates the entry signal for the given dataframe
        :param dataframe: DataFrame
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with entry columns populated
        """
        #dataframe['t1'] = (dataframe['macd'] - dataframe['macd'].shift(1)) * self.Sensitivity.value
        dataframe['e1'] = (dataframe['bb_upperband_' + str(self.channelLength.value) + '_' + str(self.bb_mult.value)] - dataframe['bb_lowerband_' + str(self.channelLength.value) + '_' + str(self.bb_mult.value)]) 
        #dataframe['trendUown'] = dataframe['t1'] if dataframe['t1'] < 0 else 0

        ## comment out before optimizing
        dataframe['bc1'] = (qtpylib.crossed_above(dataframe['e1'], dataframe['deadzone' + str(self.deadzonemultiplier.value)]) | (dataframe['e1'] > dataframe['deadzone' + str(self.deadzonemultiplier.value)]))
        dataframe['bc2'] = (((dataframe['macd'] - dataframe['macd'].shift(1)) * self.Sensitivity.value) > 0 )
        dataframe['bc3'] = (dataframe['deadzone' + str(self.deadzonemultiplier.value)])

        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['e1'], dataframe['deadzone' + str(self.deadzonemultiplier.value)]) | (dataframe['e1'] > dataframe['deadzone' + str(self.deadzonemultiplier.value)])) &  # longZoneCond
                (((dataframe['macd'] - dataframe['macd'].shift(1)) * self.Sensitivity.value) > 0 ) &       #trendUp > 0
                #(dataframe['date'].dt.dayofweek in self.active_days_of_week) &
                (
                    (dataframe['date'].dt.dayofweek == 0 if 0 in self.active_days_of_week else False) |
                    (dataframe['date'].dt.dayofweek == 1 if 1 in self.active_days_of_week else False) |
                    (dataframe['date'].dt.dayofweek == 2 if 2 in self.active_days_of_week else False) |
                    (dataframe['date'].dt.dayofweek == 3 if 3 in self.active_days_of_week else False) |
                    (dataframe['date'].dt.dayofweek == 4 if 4 in self.active_days_of_week else False) |
                    (dataframe['date'].dt.dayofweek == 5 if 5 in self.active_days_of_week else False) |
                    (dataframe['date'].dt.dayofweek == 6 if 6 in self.active_days_of_week else False)
                ) &
                (dataframe['deadzone' + str(self.deadzonemultiplier.value)] != 0)  # DEADZONE != 0
                #(dataframe['volume'] > 0)  # Make sure Volume is not 0
            ),
            'enter_long'] = 1
        # Uncomment to use shorts (Only used in futures/margin mode. Check the documentation for more info)
        """
        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['rsi'], self.sell_rsi.value)) &  # Signal: RSI crosses above sell_rsi
                (dataframe['tema'] > dataframe['bb_middleband']) &  # Guard: tema above BB middle
                (dataframe['tema'] < dataframe['tema'].shift(1)) &  # Guard: tema is falling
                (dataframe['volume'] > 0)  # Make sure Volume is not 0
            ),
            'enter_short'] = 1
        """

        
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the exit signal for the given dataframe
        :param dataframe: DataFrame
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with exit columns populated
        """
        
        ## put these in here so they can be hyperopted.  will slow down optimization runs...
        dataframe['exit_long'] = 0
        # Uncomment to use shorts (Only used in futures/margin mode. Check the documentation for more info)
        """
        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe['rsi'], self.buy_rsi.value)) &  # Signal: RSI crosses above buy_rsi
                (dataframe['tema'] <= dataframe['bb_middleband']) &  # Guard: tema below BB middle
                (dataframe['tema'] > dataframe['tema'].shift(1)) &  # Guard: tema is raising
                (dataframe['volume'] > 0)  # Make sure Volume is not 0
            ),v      
            'exit_short'] = 1
        """
        
        return dataframe



    def custom_exit(self, pair: str, trade: 'Trade', current_time: 'datetime', current_rate: float,
                    current_profit: float, **kwargs):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()
        # Look up trade Open candle.
        trade_date = timeframe_to_prev_date(self.timeframe, trade.open_date_utc)
        trade_candle = dataframe.loc[dataframe['date'] == trade_date]
        
        trade_entry_price = trade.open_rate
        atrLongStop =trade.open_rate - (trade_candle['atr_' + str(self.atrPeriod.value)] * self.atrMultLower.value)
        
        longRisk = trade_candle['close'] - atrLongStop
        longTp = trade_entry_price + (self.riskLongMultip.value * longRisk)

        # Sell if price is >= TP point
        #TODO check if longTP.item() is valid 
        if ((len(longTp) > 0) and (current_rate >= longTp.item())):
            return 'long_TP_hit_' + str(longTp.item())




    def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime,
                    current_rate: float, current_profit: float, **kwargs) -> float:
        

        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()

        # Look up trade Open candle.
        trade_date = timeframe_to_prev_date(self.timeframe, trade.open_date_utc)
        trade_candle = dataframe.loc[dataframe['date'] == trade_date]
        
        trade_entry_price = trade.open_rate
        atrLongStop =trade.open_rate - (trade_candle['atr_' + str(self.atrPeriod.value)] * self.atrMultLower.value)
        
        # Sell if price is < TP point
        

        # Use parabolic sar as absolute stoploss price
        #stoploss_price = dataframe['close'] - (dataframe['atr'] * self.atrMultiUpper.value)

        # Convert absolute price to percentage relative to current_rate
        if ((len(atrLongStop) > 0) and (atrLongStop.item() < current_rate)):
            
            return (atrLongStop.item() / current_rate) - 1

        # return maximum stoploss value, keeping current stoploss price unchanged
        
        return 1
