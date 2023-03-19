import os

import pytest
from trading_bot_utils.clients.tapi import TAPIClient


@pytest.fixture
def tapi_client() -> TAPIClient:
    ConsumerID = os.getenv("ConsumerID")
    ConsumerSecret = os.getenv("ConsumerSecret")
    PrivateKey = os.getenv("PrivateKey")
    PIN = os.getenv("PIN")
    account_id = os.getenv("accountID")

    return TAPIClient(
        ConsumerID=ConsumerID,
        ConsumerSecret=ConsumerSecret,
        PrivateKey=PrivateKey,
        PIN=PIN,
        account_id=account_id,
    )


def test_init(tapi_client: TAPIClient):
    assert tapi_client


def test_check_balance(tapi_client: TAPIClient):
    balance = tapi_client.get_balance()
    assert balance != -1


def test_check_position(tapi_client: TAPIClient):
    position = tapi_client.get_position()
    assert position != -1


def test_check_max_buy_quantity(tapi_client: TAPIClient):
    print(tapi_client.get_max_buy_quantity("VNF302303", 0))


def test_check_max_sell_quantity(tapi_client: TAPIClient):
    print(tapi_client.get_max_sell_quantity("VNF302303", 0))
