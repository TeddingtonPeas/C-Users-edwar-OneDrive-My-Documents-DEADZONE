:: downloads price data for the coins listed in the config.json file from the exchange listed in the same file.
:: you can choose how many days back from now the data starts.
:: The below will download 15m candlestick data for the last 1000 days
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

docker-compose -f docker-compose.yml run --rm freqtrade download-data -c ./user_data/config.json -t 15m  --days 1000
PAUSE