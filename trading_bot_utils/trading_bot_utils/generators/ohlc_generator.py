import datetime as dt
from copy import deepcopy

from loguru import logger

STR_TIME = "%d/%m/%Y %H:%M:%S"


class OHLCBar(object):
    def __init__(self, price, volume, time, trading_session, symbol):
        self.symbol = symbol
        self.time = time.replace(second=0, microsecond=0)

        self.open = price
        self.high = price
        self.low = price
        self.close = price

        self.volume = volume

        self.trading_session = trading_session

    def add_tick(self, price, volume):
        last_price = price

        self.close = last_price
        if last_price > self.high:
            self.high = last_price
        elif last_price < self.low:
            self.low = last_price

        self.volume += volume

    def __repr__(self):
        rep = f"OHLC({str(self.time)},{self.open},{self.high},{self.low},{self.close} , {self.volume})"
        return rep


class OHCLGenerator:
    def __init__(self, min=1):
        self.min = min
        self.current_bar = None
        self.release_bar = None

    def process_event(self, message):
        time = dt.datetime.strptime(
            message["TradingDate"] + " " + message["Time"], STR_TIME
        )
        price = message["LastPrice"]
        volume = message["LastVol"]
        trading_session = message["TradingSession"]
        symbol = message["Symbol"]

        if trading_session == "LO":
            # logger.info(message)

            if self.current_bar is None:
                self.current_bar = OHLCBar(
                    price=price,
                    volume=volume,
                    time=time,
                    trading_session=trading_session,
                    symbol=symbol,
                )
                return None

            # logger.info(time - self.current_bar.time)
            if (time - self.current_bar.time) < dt.timedelta(minutes=self.min):
                self.current_bar.add_tick(price, volume)
                return None

            self.release_bar = deepcopy(self.current_bar)
            self.current_bar = OHLCBar(
                price=price,
                volume=volume,
                time=time,
                trading_session=trading_session,
                symbol=symbol,
            )

            # logger.info(self.current_bar)
            return self.release_bar

        elif (trading_session == "ATO") and (price > 0):
            return OHLCBar(
                price=price,
                volume=volume,
                time=time,
                trading_session=trading_session,
                symbol=symbol,
            )

        elif trading_session == "ATC":
            return self.release_bar

        elif trading_session == "C":
            return OHLCBar(
                price=price,
                volume=volume,
                time=time,
                trading_session="ATC",
                symbol=symbol,
            )
