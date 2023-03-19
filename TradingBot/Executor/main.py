import os
import time

import zmq
from loguru import logger

ZMQ_STRATEGIST_ADDRESS = os.environ.get(
    "ZMQ_STRATEGIST_ADDRESS", "tcp://localhost:5556"
)

logger.add("log/TRADE_{time:YYYY-MM-DD}.log", mode="a", rotation="1 day")

if __name__ == "__main__":
    context = zmq.Context()
    receiver = context.socket(zmq.PULL)

    while True:
        try:
            receiver.bind(ZMQ_STRATEGIST_ADDRESS)
        except:
            logger.info(f"Wait For {ZMQ_STRATEGIST_ADDRESS} live")
            time.sleep(0.2)
        finally:
            logger.info(f"Start to Connect Strategist: {ZMQ_STRATEGIST_ADDRESS}")
            break

    while True:
        logger.info(receiver.recv_string())
