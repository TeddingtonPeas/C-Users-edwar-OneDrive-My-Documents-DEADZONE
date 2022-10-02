#! /bin/bash
shopt -s expand_aliases
source ../util/sourceme.sh

freqtrade backtesting --strategy deadzone --timerange=20220810-20220925 -c user_data/config.json
