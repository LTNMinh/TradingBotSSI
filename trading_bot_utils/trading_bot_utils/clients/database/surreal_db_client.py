import json
import threading

import requests


class SurrealClient:
    def __init__(
        self,
        user_name,
        password,
        namespace,
        database,
        connection="localhost",
        port=8000,
    ) -> None:
        self.headers = {
            "Accept": "application/json",
            "NS": namespace,
            "DB": database,
            "Content-Type": "text/plain",
        }

        self.auth = (user_name, password)
        self.connection = f"{connection}:{port}"
        self.init_db()

    def init_db(self):
        SCHEMA = """
            DEFINE TABLE tick SCHEMAFULL; 
            DEFINE FIELD RType on tick type string;
            DEFINE FIELD TradingDate on tick type datetime;
            DEFINE FIELD Time on tick type datetime;
            DEFINE FIELD Symbol on tick type string;
            DEFINE FIELD Celing on tick type float;
            DEFINE FIELD Floor on tick type float;
            DEFINE FIELD RefPrice on tick type float;
            DEFINE FIELD AvgPrice on tick type float;
            DEFINE FIELD PriorVal on tick type float;
            DEFINE FIELD LastPrice on tick type float;
            DEFINE FIELD LastVol on tick type float;
            DEFINE FIELD TotalVal on tick type float;
            DEFINE FIELD TotalVol on tick type float;
            DEFINE FIELD MarketId on tick type string; 
            DEFINE FIELD Exchange on tick type string; 
            DEFINE FIELD TradingSession on tick type string; 
            DEFINE FIELD TradingStatus on tick type string; 
            DEFINE FIELD Change on tick type float; 
            DEFINE FIELD RatioChange on tick type float; 
            DEFINE FIELD EstMatchedPrice on tick type float; 
            DEFINE FIELD Highest on tick type float; 
            DEFINE FIELD Lowest on tick type float; 
        """
        requests.post(
            f"http://{self.connection}/sql",
            headers=self.headers,
            auth=self.auth,
            data=SCHEMA,
        ).json()

    def query(self, query):
        return requests.post(
            f"http://{self.connection}/sql",
            headers=self.headers,
            auth=self.auth,
            data=query,
        ).json()

    def _create(self, data, table):
        response = requests.post(
            f"http://{self.connection}/key/{table}",
            headers=self.headers,
            auth=self.auth,
            data=json.dumps(data),
        ).json()

        if response[0]["status"] == "OK":
            return
        else:
            raise Exception(f"Create New data {data} on table {table} failed")

    def create(self, data, table):
        while True:
            try:
                threading.Thread(target=self._create, args=(data, table)).start()
            except RuntimeError:
                pass
            else:
                break
