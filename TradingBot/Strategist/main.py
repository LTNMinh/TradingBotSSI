import importlib
import json
import os
import time

import zmq
from loguru import logger

from trading_bot_utils.clients.database import TimescaleDBClient
from trading_bot_utils.clients.tapi import TAPIClient

ZMQ_PUB_ADDRESS = os.environ.get("ZMQ_PUB_ADDRESS", "tcp://localhost:5556")
ZMQ_EXECUTOR_ADDRESS = os.environ.get("ZMQ_EXECUTOR_ADDRESS", "tcp://localhost:5556")

STRATEGY_NAME = str(os.environ.get("STRATEGY_NAME"))
STRATEGY_PARAM = str(os.environ.get("STRATEGY_PARAM", "24")).split("#")


POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
DEBUG = True if os.environ.get("DEBUG", "False").lower() == "true" else False

if not DEBUG:
    logger.add("log/SIGNAL_{time:YYYY-MM-DD}.log", mode="a", rotation="1 day")

if __name__ == "__main__":
    context = zmq.Context()
    receiver = context.socket(zmq.PULL)
    publisher = context.socket(zmq.PUSH)
    myClient = TimescaleDBClient(
        user="postgres",
        password="postgres",
        database="postgres",
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
    )

    while True:
        try:
            receiver.connect(ZMQ_PUB_ADDRESS)
        except:
            logger.info(f"Wait For {ZMQ_PUB_ADDRESS} live")
            time.sleep(0.2)
        finally:
            logger.info(f"Start to Connect: {ZMQ_PUB_ADDRESS}")
            break

    while True:
        try:
            publisher.connect(ZMQ_EXECUTOR_ADDRESS)
        except:
            logger.info(f"Wait For {ZMQ_EXECUTOR_ADDRESS} live")
            time.sleep(0.2)
        finally:
            logger.info(f"Start to Connect: {ZMQ_EXECUTOR_ADDRESS}")
            break

    module_name = "trading_bot_utils.strategies"
    module = importlib.import_module(module_name)
    Strategy = getattr(module, STRATEGY_NAME)

    ConsumerID = os.getenv("ConsumerID")
    ConsumerSecret = os.getenv("ConsumerSecret")
    PrivateKey = os.getenv("PrivateKey")
    PIN = os.getenv("PIN")
    account_id = os.getenv("accountID")

    client = TAPIClient(
        ConsumerID=ConsumerID,
        ConsumerSecret=ConsumerSecret,
        PrivateKey=PrivateKey,
        PIN=PIN,
        account_id=account_id,
    )
    myStrategy = Strategy(client, *STRATEGY_PARAM)
    logger.info(f"Init Strategy {Strategy.__name__} successful ")

    while True:
        event = json.loads(receiver.recv())
        logger.info(event)
        signal = myStrategy.process_event(event)
        if signal:
            logger.info(signal)
            # publisher.send_string(str(signal))
