docker-compose -f docker-compose.yml run --rm freqtrade download-data -c ./user_data/config.json -t 15m  --days 1000
docker-compose -f docker-compose.yml run --rm freqtrade backtesting --strategy deadzone --timerange=20220810-20220925 -c user_data/config.json
PAUSE