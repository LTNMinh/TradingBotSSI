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

