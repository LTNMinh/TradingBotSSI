MYPWD=$(pwd)
cd trading_bot_utils/
python3 setup.py bdist_wheel sdist
cd $MYPWD
docker build -t tradingbot/tradingbot:latest .
