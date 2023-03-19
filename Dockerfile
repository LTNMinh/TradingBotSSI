FROM python:3.8.16-alpine3.16
RUN apk --no-cache add gcc &&\
    apk --no-cache add libc-dev &&\ 
    apk --no-cache add libffi-dev &&\
    apk --no-cache add build-base && \
    apk --no-cache add postgresql-dev && \
    apk --no-cache add postgresql-libs

RUN pip install --no-cache-dir numpy==1.24.2 && \
    pip install --no-cache-dir psycopg2==2.9.5 && \
    pip install --no-cache-dir gevent==22.10.2

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

COPY WheelPackage/ssi_fc_data-2.0.0-py3-none-any.whl /ssi_fc_data-2.0.0-py3-none-any.whl
COPY WheelPackage/ssi_fctrading-2.1.0-py3-none-any.whl ssi_fctrading-2.1.0-py3-none-any.whl

RUN pip install --no-cache-dir ssi_fc_data-2.0.0-py3-none-any.whl && \ 
    pip install --no-cache-dir ssi_fctrading-2.1.0-py3-none-any.whl

COPY trading_bot_utils/dist/trading_bot_utils-0.0.4-py3-none-any.whl trading_bot_utils-0.0.4-py3-none-any.whl
RUN pip install --no-cache-dir trading_bot_utils-0.0.4-py3-none-any.whl