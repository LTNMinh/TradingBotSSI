import io
import threading
import time
from typing import Iterator, Optional

import psycopg2
from loguru import logger
from psycopg2 import pool


class StringIteratorIO(io.TextIOBase):
    def __init__(self, iter: Iterator[str]):
        self._iter = iter
        self._buff = ""

    def readable(self) -> bool:
        return True

    def _read1(self, n: Optional[int] = None) -> str:
        while not self._buff:
            try:
                self._buff = next(self._iter)
            except StopIteration:
                break
        ret = self._buff[:n]
        self._buff = self._buff[len(ret) :]
        return ret

    def read(self, n: Optional[int] = None) -> str:
        line = []
        if n is None or n < 0:
            while True:
                m = self._read1()
                if not m:
                    break
                line.append(m)
        else:
            while n > 0:
                m = self._read1(n)
                if not m:
                    break
                n -= len(m)
                line.append(m)
        return "".join(line)


class TimescaleDBClient:
    def __init__(self, user, password, host, port, database) -> None:
        retry = 10
        for i in range(retry):
            try:
                self.connection_pool = psycopg2.pool.ThreadedConnectionPool(
                    10,
                    30,
                    user=user,
                    password=password,
                    host=host,
                    port=port,
                    database=database,
                )
            except psycopg2.OperationalError:
                logger.info(f"Database is not start. Retry {i} times")
                time.sleep(20)

    def batch_import(self, list_data):
        connection = self.connection_pool.getconn()
        with connection.cursor() as cursor:
            my_string_iterator = StringIteratorIO(
                ("|".join(map(str, data)) + "\n" for data in list_data)
            )
            cursor.copy_from(my_string_iterator, "stocks_real_time", sep="|", size=1024)
            connection.commit()
        self.connection_pool.putconn(connection)

    def insert_data(self, data):
        while True:
            try:
                threading.Thread(
                    target=self._insert_data,
                    args=(data,),
                ).start()
            except RuntimeError:
                pass
            except Exception:
                break
            else:
                break

    def _insert_data(self, data):
        while True:
            try:
                conn = self.connection_pool.getconn()
                insert_query = """ INSERT INTO stocks_real_time 
                                    (time,rtype,symbol,celling,floor,ref_price,last_price,last_vol,total_val,total_vol,exchange,trading_session,trading_status,change,ratio_change) 
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                cursor = conn.cursor()
                cursor.execute(insert_query, data)
                cursor.close()
                conn.commit()

                self.connection_pool.putconn(conn)
            except psycopg2.pool.PoolError:
                pass
            except Exception:
                logger.error("Cannot Import To Database")
                break
            else:
                break
