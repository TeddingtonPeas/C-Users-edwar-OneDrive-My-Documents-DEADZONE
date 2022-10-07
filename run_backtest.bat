docker-compose -f docker-compose.yml run --rm freqtrade download-data -c ./user_data/config.json -t 15m  --days 1000
docker-compose -f docker-compose.yml run --rm freqtrade backtesting --strategy deadzone --timerange=20200101-20220907 -c user_data/config.json
PAUSE