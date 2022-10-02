#! /bin/bash
shopt -s expand_aliases
source ../util/sourceme.sh
#freqtrade hyperopt -s strategy_spaghetti_01 --spaces buy --hyperopt-loss SharpeHyperOptLoss -c user_data/config_levtokens_ETH.json -e 5000 --timerange=20210101-20220226


################
## RUN ALL BUILT IN LOSS FUNCTIONS  for longs only
###############
freqtrade hyperopt -s deadzone --spaces  buy --hyperopt-loss SharpeHyperOptLoss -c user_data/config.json -e 4000 --timerange=20220601-20220825 >! optlogs/Sharpe.log
freqtrade hyperopt -s deadzone --spaces  buy --hyperopt-loss SortinoHyperOptLoss -c user_data/config.json -e 4000 --timerange=20220601-20220926 >! optlogs/sortino.log
freqtrade hyperopt -s deadzone --spaces  buy --hyperopt-loss OnlyProfitHyperOptLoss -c user_data/config.json -e 4000 --timerange=20220601-20220726 >! optlogs/Only.log
freqtrade hyperopt -s deadzone --spaces  buy --hyperopt-loss CalmarHyperOptLoss -c user_data/config.json -e 4000 --timerange=20220601-20220726 >! optlogs/Calmar.log
freqtrade hyperopt -s deadzone --spaces  buy --hyperopt-loss ProfitDrawDownHyperOptLoss -c user_data/config.json -e 4000 --timerange=20220601-20220726 >! optlogs/Profit.log


################
## RUN ALL BUILT IN LOSS FUNCTIONS  for shorts only
###############
#freqtrade hyperopt -s strategy_spaghetti_01 --spaces buy sell stoploss --hyperopt-loss SharpeHyperOptLoss -c user_data/backtest_config_levtokens_BTC_shorts.json -e 2000 --timerange=20210101-20220226 > optlogs/Sharpe.log
#freqtrade hyperopt -s strategy_spaghetti_01 --spaces buy sell stoploss --hyperopt-loss SortinoHyperOptLoss -c user_data/backtest_config_levtokens_BTC_shorts.json -e 2000 --timerange=20210101-20220226 > optlogs/Sortino.log
#freqtrade hyperopt -s strategy_spaghetti_01 --spaces buy sell stoploss --hyperopt-loss OnlyProfitHyperOptLoss -c user_data/backtest_config_levtokens_BTC_shorts.json -e 2000 --timerange=20210101-20220226 > optlogs/OnlyProfit.log
#freqtrade hyperopt -s strategy_spaghetti_01 --spaces buy sell stoploss --hyperopt-loss ShortTradeDurationHyperOptLoss -c user_data/backtest_config_levtokens_BTC_shorts.json -e 2000 --timerange=20210101-20220226 > optlogs/ShortTrades.log
#freqtrade hyperopt -s strategy_spaghetti_01 --spaces buy sell stoploss --hyperopt-loss CalmarHyperOptLoss -c user_data/backtest_config_levtokens_BTC_shorts.json -e 2000 --timerange=20210101-20220226 > optlogs/Calmar.log
#freqtrade hyperopt -s strategy_spaghetti_01 --spaces buy sell stoploss --hyperopt-loss ProfitDrawDownHyperOptLoss -c user_data/backtest_config_levtokens_BTC_shorts.json -e 2000 --timerange=20210101-20220226 > optlogs/ProfitDrawDown.log



#freqtrade hyperopt -s strategy_spaghetti_01 --spaces buy --hyperopt-loss MaxDrawDownHyperOptLoss -c user_data/config_levtokens_ETH.json -e 5000 --timerange=20210101-20220226 
#freqtrade hyperopt -s strategy_spaghetti_01 --spaces buy stoploss trailing --hyperopt-loss twotradesperday -c user_data/config_levtokens_ETH.json -e 5000 --timerange=20210101-20220226
