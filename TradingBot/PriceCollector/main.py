import json
import os
import time
import traceback

import ssi_fc_data
import zmq
from loguru import logger
from trading_bot_utils.clients.database import TimescaleDBClient
from trading_bot_utils.generators import OHCLGenerator
from trading_bot_utils.parser import parsing_data

import config


def get_trading_future_symbol_data():
    import datetime

    FORMAT = "%d/%m/%Y"

    def _filter_vn30(x):
        return x["Symbol"].startswith("VN30")

    data = ssi_fc_data.securities(config, "DER", 1, 100)["data"]
    mylist = list(filter(_filter_vn30, data))
    mylist.sort(key=lambda x: x["Symbol"])
    current_symbol = mylist[0]["Symbol"]

    resp = ssi_fc_data.securities_details(config, "DER", current_symbol, 1, 10)
    if resp["status"] == "DataNotReady":
        print(resp)
        return None

    derivatives_detail = ssi_fc_data.securities_details(
        config, "DER", current_symbol, 1, 10
    )["data"]
    maturities_date = derivatives_detail[0]["RepeatedInfo"][0]["MaturityDate"]
    maturities_date = datetime.datetime.strptime(maturities_date, FORMAT)
    today = datetime.datetime.utcnow() + datetime.timedelta(hours=7)

    if maturities_date.date() == today.date():
        return mylist[1]["Symbol"]

    return current_symbol


def get_market_data(message):
    try:
        message = json.loads(message["Content"])
        logger.info(message)

        global my_generator
        global socket
        global myClient

        myClient.insert_data(parsing_data(message))
        bar = my_generator.process_event(message)

        if bar:
            logger.info("True")
            event = json.dumps(vars(bar), default=str).encode("utf-8")
            logger.info(event)
            socket.send(event)
    except:
        logger.error(traceback.print_exc())


def getError(error):
    logger.info(error)


ZMQ_STRATEGIST_ADDRESS = os.environ.get("ZMQ_STRATEGIST_ADDRESS", "tcp://*:5556")
DEBUG = True if os.environ.get("DEBUG", "False").lower() == "true" else False
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")


if not DEBUG:
    logger.add("log/MARKET_{time:YYYY-MM-DD}.log", mode="a", rotation="1 day")


if __name__ == "__main__":
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)

    myClient = TimescaleDBClient(
        user="postgres",
        password="postgres",
        database="postgres",
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
    )

    while True:
        try:
            socket.bind(ZMQ_STRATEGIST_ADDRESS)
        except:
            logger.info(f"Wait For {ZMQ_STRATEGIST_ADDRESS} live")
            time.sleep(0.2)
        finally:
            logger.info(f"Start to publish {ZMQ_STRATEGIST_ADDRESS}")
            break

    my_generator = OHCLGenerator(min=1)

    if not DEBUG:
        config.access_jwt = ssi_fc_data.access_token(config)["data"]["accessToken"]
        symbol = get_trading_future_symbol_data()
        selected_channel = f"X-TRADE:{symbol}"
        logger.info(f"Start to Stream Channel {selected_channel}")

        ssi_fc_data.Market_Data_Stream(
            config, get_market_data, getError, selected_channel
        )
    else:
        with open("TRADELOG.log", "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                message = {"Content": line.split(" - ")[-1]}
                get_market_data(message)
