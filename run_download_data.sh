#! /bin/bash
shopt -s expand_aliases
source ../util/sourceme.sh
freqtrade download-data -c ./user_data/config.json -t 15m  --days 365
#freqtrade download-data -c ./user_data/config_allcoins.json -t 1h  --days 100
#freqtrade download-data -c ./user_data/config_allcoins.json -t 3m --days 100
