import os
import random

from ssi_fctrading import FCTradingClient
from ssi_fctrading.models import fcmodel_requests

Url = "https://fc-tradeapi.ssi.com.vn/"
StreamURL = "https://fc-tradehub.ssi.com.vn/"
TwoFAType = 0


class TAPIClient:
    def __init__(
        self, ConsumerID, ConsumerSecret, PrivateKey, PIN, account_id="1"
    ) -> None:
        self.client = FCTradingClient(
            Url,
            ConsumerID,
            ConsumerSecret,
            PrivateKey,
            0,
        )
        self.client.verifyCode(PIN)
        self.account_id = account_id

    def get_balance(self):
        fc_rq = fcmodel_requests.DerivativeAccountBalance(str(self.account_id))
        res = self.client.get_derivative_account_balance(fc_rq)
        if res["status"] != 200:
            return -1

        return res["data"]

    def get_position(self, type="derivatives"):
        fc_rq = fcmodel_requests.DerivativePosition(str(self.account_id))
        res = self.client.get_derivative_position(fc_rq)
        if res["status"] != 200:
            return -1

        return res["data"]

    def get_max_buy_quantity(self, instrument_id, price):
        fc_rq = fcmodel_requests.MaxBuyQty(
            str(self.account_id), str(instrument_id), float(price)
        )
        res = self.client.get_max_buy_qty(fc_rq)
        if res["status"] != 200:
            return -1

        return res["data"]

    def get_max_sell_quantity(self, instrument_id, price):
        fc_rq = fcmodel_requests.MaxSellQty(
            str(self.account_id), str(instrument_id), float(price)
        )
        res = self.client.get_max_sell_qty(fc_rq)
        if res["status"] != 200:
            return -1

        return res["data"]

    def market_long(
        self,
        quantity,
        instrument_id,
        market_id="VNFE",
        stop_order=False,
        stop_price=0,
        stop_type="",
        stop_step=0,
        loss_step=0,
        profit_step=0,
    ):
        res = self._new_order(
            price=0,
            quantity=quantity,
            instrument_id=instrument_id,
            order_type="MP",
            market_id=market_id,
            side="B",
            stop_order=stop_order,
            stop_price=stop_price,
            stop_type=stop_type,
            stop_step=stop_step,
            loss_step=loss_step,
            profit_step=profit_step,
        )
        return res

    def market_short(
        self,
        quantity,
        instrument_id,
        market_id="VNFE",
        stop_order=False,
        stop_price=0,
        stop_type="",
        stop_step=0,
        loss_step=0,
        profit_step=0,
    ):
        res = self._new_order(
            price=0,
            quantity=quantity,
            instrument_id=instrument_id,
            order_type="MP",
            market_id=market_id,
            side="S",
            stop_order=stop_order,
            stop_price=stop_price,
            stop_type=stop_type,
            stop_step=stop_step,
            loss_step=loss_step,
            profit_step=profit_step,
        )
        return res

    def _new_order(
        self,
        price,
        quantity,
        instrument_id,
        order_type,
        market_id="VNFE",
        side="B",
        stop_order=False,
        stop_price=0,
        stop_type="",
        stop_step=0,
        loss_step=0,
        profit_step=0,
    ):
        fc_req = fcmodel_requests.NewOrder(
            str(self.account_id).upper(),
            str(random.randint(0, 99999999)),
            str(instrument_id).upper(),
            str(market_id).upper(),
            str(side).upper(),
            str(order_type).upper(),
            float(price),
            int(quantity),
            bool(stop_order),
            float(stop_price),
            str(stop_type),
            float(stop_step),
            float(loss_step),
            float(profit_step),
        )
        res = self.client.new_order(fc_req)
        return res
