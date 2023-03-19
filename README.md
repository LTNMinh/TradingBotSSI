# Trading Bot SSI 
This is the trading bot using SSI api 


## Run Bot
### Create ENV file

```bash
# .env

ConsumerID=<Your Consumer ID here>
ConsumerSecret=<Your Consumer Secret here>
PrivateKey=<Your Private Key Here>
PIN=<Your Pin here>
accountID=<Your Account ID here>

# Internal ZMQ config 
ZMQ_STRATEGIST_ADDRESS=tcp://*:3000
ZMQ_PUB_ADDRESS=tcp://price_pub:3000
ZMQ_EXECUTOR_ADDRESS=tcp://executor:3001

POSTGRES_HOST=timescaledb
POSTGRES_PORT=5432

#STRATEGY PARAM
STRATEGY_NAME=<Your Strategy Name here> 
STRATEGY_PARAM=24#30

DEBUG=True
```

### Build Docker with package
```bash
./build_docker.sh 
```

### Run Docker Stack 
```bash
cd TradingBot
./build.sh

```

