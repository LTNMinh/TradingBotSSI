
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