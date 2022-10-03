# freqtrade environment for deadzone strategy

## Introduction

Freqtrade is an open source python based trading bot for linux.  I have built this repo to make it as user friendly as possible to develope and optimize strategies in windows. This repo contains the strategy file and some windows .bat scripts to run freqtrade on this strategy.
In order to run freqtrade you will need to download and install docker desktop.  Docker is a virtual machine and this is the easiest way to run freqtrade.

This is a quick and dirty information dump to get you up and running.  You will undoubtably need more detail than this to be effective. However this should get you started.

I reccomend reading throught the freqtrade documentation. https://www.freqtrade.io/en/stable/  There is a lot of it but it is fairly complete. 

## Steps to setup environment:

1) Install docker desktop from https://www.docker.com/
2) install github desktop from https://desktop.github.com/
3) using github desktop clone the following github repo to a location on your pc that you want to work.  Documents/deadzone for example
4) github repo: https://github.com/donjonson/deadzone
5) reboot pc
6) build freqtrade docker image
  1) double-click the util/setup_environment.bat

That should be all you need to start using the freqtrade python trading bot environment.  

## Important Information

- All of the strategy specific information is in the user_data direcotry
  - user_data/config.json is the config file for the strategy. This is where you set the list of coins to trade and timeframe.
  - user_data/strategies/deadzone.py is the python strategy file for deadzone strategy.
### Freqtrade batch scripts
To run any of the batch scripts just double click them in windows. 
- run_backtest.bat
  - The name is self explanatory.  This will run a terminal based backtest and print the results to the terminal.  
  - you can modify the timerange in this file to control how far back the test goes.
  
  
- run_download_price_data.bat
  - before you can backtest or optimize a strategy you need to be have the price data.
  - This will downlaod the specified timeframe candlestick data for all coins in the whitelist defined in config.json file.
  - all of thei batch scripts actually do this before running their expected operation.  but this file only downloads data.
  - it may be desireable to comment out the download data from the other scripts.
  
  
- run_optimization.bat
  - This will start the optimizatoin
  - the --hyperopt-loss arguement tells hyperopt what to optize for.
  - the -j option specifies the number of parallel cores to use. (it will use all cores if no -j option is given)
  - the -e option tells it how many iterations or 'epochs' to use.
  - This is a Machine Learning based optimization so it starts with a set of random points an then runs gradient algorithms to find the optimal result. 
  
- docker-compose files
  - do not touch thse.  they do not need editing and you will break the flow if you change them.
