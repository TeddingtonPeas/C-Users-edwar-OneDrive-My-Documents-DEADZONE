::docker-compose -f docker-compose.yml run --rm freqtrade download-data -c ./user_data/config.json -t 15m  --days 1000
::docker-compose -f docker-compose.yml run --rm freqtrade hyperopt -s deadzone --spaces  buy --hyperopt-loss SharpeHyperOptLoss -c user_data/config.json -e 4000 --timerange=20220601-20220825 -j 4
::docker-compose -f docker-compose.yml run --rm freqtrade hyperopt -s deadzone --spaces  buy --hyperopt-loss SorinoHyperOptLoss -c user_data/config.json -e 2000 --timerange=20220601-20220825 -j 8
docker-compose -f docker-compose.yml run --rm freqtrade hyperopt -s deadzone --spaces  buy --hyperopt-loss OnlyProfitHyperOptLoss -c user_data/config.json -e 100 --timerange=20220601-20220825
::docker-compose -f docker-compose.yml run --rm freqtrade hyperopt -s deadzone --spaces  buy --hyperopt-loss CalmarHyperOptLoss -c user_data/config.json -e 4000 --timerange=20220601-20220825
::docker-compose -f docker-compose.yml run --rm freqtrade hyperopt -s deadzone --spaces  buy --hyperopt-loss ProfitDrawDownHyperOptLoss -c user_data/config.json -e 4000 --timerange=20220601-20220825
PAUSE