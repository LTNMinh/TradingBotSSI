FROM tradingbot/tradingbot:latest

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir ./log

COPY ./ ./

CMD [ "python3", "./main.py" ]