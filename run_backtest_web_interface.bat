#docker-compose -f docker-compose.yml run --rm freqtrade download-data -c ./user_data/config.json -t 15m  --days 1000
docker-compose -f docker-compose-ws.yml up
PAUSE