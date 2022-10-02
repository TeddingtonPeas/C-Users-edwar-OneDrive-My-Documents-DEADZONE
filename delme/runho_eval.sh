#!/bin/bash
#freqtrade hyperopt -s strategy_spaghetti_01 --spaces buy --hyperopt-loss SharpeHyperOptLoss -c user_data/config_levtokens_ETH.json -e 5000 --timerange=20210101-20220226


################
## RUN ALL BUILT IN LOSS FUNCTIONS  for longs only
###############
#freqtrade hyperopt -s strategy_spaghetti_01 --spaces buy sell stoploss --hyperopt-loss SharpeHyperOptLoss -c user_data/backtest_config_levtokens_BTC_longs.json -e 2000 --timerange=20210101-20220226 > optlogs/longs/Sharpe.log
#freqtrade hyperopt -s strategy_spaghetti_01 --spaces buy sell stoploss --hyperopt-loss SortinoHyperOptLoss -c user_data/backtest_config_levtokens_BTC_longs.json -e 2000 --timerange=20210101-20220226 > optlogs/longs/Sortino.log
#freqtrade hyperopt -s strategy_spaghetti_01 --spaces buy sell stoploss --hyperopt-loss OnlyProfitHyperOptLoss -c user_data/backtest_config_levtokens_BTC_longs.json -e 2000 --timerange=20210101-20220226 > optlogs/longs/OnlyProfit.log
#freqtrade hyperopt -s strategy_spaghetti_01 --spaces buy sell stoploss --hyperopt-loss ShortTradeDurationHyperOptLoss -c user_data/backtest_config_levtokens_BTC_longs.json -e 2000 --timerange=20210101-20220226 > optlogs/longs/ShortTrades.log
#freqtrade hyperopt -s strategy_spaghetti_01 --spaces buy sell stoploss --hyperopt-loss CalmarHyperOptLoss -c user_data/backtest_config_levtokens_BTC_longs.json -e 2000 --timerange=20210101-20220226 > optlogs/longs/Calmar.log
#freqtrade hyperopt -s strategy_spaghetti_01 --spaces buy sell stoploss --hyperopt-loss ProfitDrawDownHyperOptLoss -c user_data/backtest_config_levtokens_BTC_longs.json -e 2000 --timerange=20210101-20220226 > optlogs/longs/ProfitDrawDown.log

################
## RUN ALL BUILT IN LOSS FUNCTIONS  for shorts only
###############
freqtrade hyperopt -s strategy_spaghetti_01 --spaces buy sell stoploss --hyperopt-loss SharpeHyperOptLoss -c user_data/backtest_config_levtokens_BTC_shorts.json -e 2000 --timerange=20210101-20220226 > optlogs/shorts/Sharpe.log
freqtrade hyperopt -s strategy_spaghetti_01 --spaces buy sell stoploss --hyperopt-loss SortinoHyperOptLoss -c user_data/backtest_config_levtokens_BTC_shorts.json -e 2000 --timerange=20210101-20220226 > optlogs/Sshorts/ortino.log
freqtrade hyperopt -s strategy_spaghetti_01 --spaces buy sell stoploss --hyperopt-loss OnlyProfitHyperOptLoss -c user_data/backtest_config_levtokens_BTC_shorts.json -e 2000 --timerange=20210101-20220226 > optlogs/shorts/OnlyProfit.log
freqtrade hyperopt -s strategy_spaghetti_01 --spaces buy sell stoploss --hyperopt-loss ShortTradeDurationHyperOptLoss -c user_data/backtest_config_levtokens_BTC_shorts.json -e 2000 --timerange=20210101-20220226 > optlogs/shorts/ShortTrades.log
freqtrade hyperopt -s strategy_spaghetti_01 --spaces buy sell stoploss --hyperopt-loss CalmarHyperOptLoss -c user_data/backtest_config_levtokens_BTC_shorts.json -e 2000 --timerange=20210101-20220226 > optlogs/shorts/Calmar.log
freqtrade hyperopt -s strategy_spaghetti_01 --spaces buy sell stoploss --hyperopt-loss ProfitDrawDownHyperOptLoss -c user_data/backtest_config_levtokens_BTC_shorts.json -e 2000 --timerange=20210101-20220226 > optlogs/shorts/ProfitDrawDown.log

################
## Evaluate the results of all the hyper opts.
## save the best results as json files and delete the results databases to save space
###############

search_dir=./user_data/hyperopt_results/
for entry in "$search_dir"/*
do
	if [[entry == "temp.csv"]]; then
		rm -rf temp.csv
	fi

	if [[entry == "*fthypt"]]; then
		#print to csv so we can pull the best iterations out
		freqtrade hyperopt-list --best -export-csv temp.csv
		#run python script to read the csv and generate a reduced version of of the fthypt file
	fi
                




#freqtrade hyperopt -s strategy_spaghetti_01 --spaces buy --hyperopt-loss MaxDrawDownHyperOptLoss -c user_data/config_levtokens_ETH.json -e 5000 --timerange=20210101-20220226 
#freqtrade hyperopt -s strategy_spaghetti_01 --spaces buy stoploss trailing --hyperopt-loss twotradesperday -c user_data/config_levtokens_ETH.json -e 5000 --timerange=20210101-20220226

################
## command to get the best results from a data file
###############
freqtrade hyperopt-list --min-trades 100 --min-avg-profit 1.5 --best -d
