
CREATE TABLE stocks_real_time (
    time TIMESTAMPTZ NOT NULL,
    rtype TEXT NOT NULL,
    symbol TEXT NOT NULL,
    celling DOUBLE PRECISION NULL,
    floor DOUBLE PRECISION NULL,
    ref_price DOUBLE PRECISION NULL,
    last_price DOUBLE PRECISION NULL,
    last_vol INT NULL,
    total_val DOUBLE PRECISION NULL,
    total_vol DOUBLE PRECISION NULL,
    exchange TEXT NULL,
    trading_session TEXT NULL,
    trading_status TEXT NULL,
    change DOUBLE PRECISION NULL,
    ratio_change DOUBLE PRECISION NULL
);

SELECT create_hypertable('stocks_real_time','time');

CREATE MATERIALIZED VIEW stock_candlestick_one_min
WITH (timescaledb.continuous) AS
SELECT time_bucket('1 minutes', time) AS one_min,
	symbol,
    first(last_price,time) as open,
    max(last_price) as high,
    min(last_price) as low,
    last(last_price,time) as close,
    sum(last_vol) as total_vol 
from public.stocks_real_time
where trading_session = 'LO'
GROUP BY one_min, symbol ;