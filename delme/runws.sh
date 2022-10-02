#! /bin/bash
#! /bin/bash
shopt -s expand_aliases
source ../util/sourceme.sh
#freqtrade webserver --config user_data/btconfig_10.json
#freqtrade webserver --config user_data/btconfig.json
#freqtrade webserver --config user_data/bt_ETH_config.json
#freqtrade webserver --config user_data/config_ADA.json
#freqtrade webserver --config user_data/config_levtokens_VET_bt.json
freqtrade_up webserver --config user_data/config.json
#freqtrade webserver --config user_data/config_levtokens_mult_bt.json
#freqtrade webserver --config user_data/config_levtokens_ETH_bt.json
#freqtrade webserver --config user_data/config_btc3LS.json
