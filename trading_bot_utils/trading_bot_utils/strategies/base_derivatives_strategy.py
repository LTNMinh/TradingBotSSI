from trading_bot_utils.clients.tapi import TAPIClient


class BaseDerivativesStrategy:
    def __init__(self, client: TAPIClient) -> None:
        self.client = client

        self.position = self.get_open_position()
        self.balance = self.get_current_balance()

    def process_event(self, event):
        pass

    def market_long(self, quantity, instrument_id) -> None:
        self.client.market_long(quantity=quantity, instrument_id=instrument_id)

    def market_short(self, quantity, instrument_id) -> None:
        self.client.market_short(quantity=quantity, instrument_id=instrument_id)

    def get_open_position(self):
        """
        openPosition: [{
            marketID: "VNFE",
            instrumentID: "VN30F2106",
            longQty: 8,
            shortQty: 0,
            net: 8,
            bidAvgPrice: 0,
            askAvgPrice: 0,
            tradePrice: 1452.7,
            marketPrice: 1452.7,
            floatingPL: 0,
            tradingPL: 0
        }],
        closePosition: []
        }
        """
        pos = self.client.get_position()
        return pos["openPosition"]

    def get_current_balance(self):
        balance = self.client.get_balance()
        return balance["accountBalance"]

    def get_max_buy_quantity(self, instrument_id, price):
        return self.client.get_max_buy_quantity(instrument_id, price)

    def get_max_self_quantity(self, instrument_id, price):
        return self.client.get_max_sell_quantity(instrument_id, price)
