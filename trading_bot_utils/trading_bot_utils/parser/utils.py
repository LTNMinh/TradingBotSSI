import datetime

STR_TIME = "%d/%m/%Y %H:%M:%S"
STR_F_TIME = "%Y-%m-%dT%H:%M:%S+7:00"


def parsing_data(data):
    return (
        datetime.datetime.strptime(
            data["TradingDate"] + " " + data["Time"], STR_TIME
        ).strftime(STR_F_TIME),
        data["RType"],
        data["Symbol"],
        data["Ceiling"],
        data["Floor"],
        data["RefPrice"],
        data["LastPrice"],
        data["LastVol"],
        data["TotalVal"],
        data["TotalVol"],
        data["Exchange"],
        data["TradingSession"],
        data["TradingStatus"],
        data["Change"],
        data["RatioChange"],
    )
