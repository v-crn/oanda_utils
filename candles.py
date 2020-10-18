import pandas as pd
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
from oandapyV20.types import DateTime
from datetime import datetime, timedelta


OANDA_ACCESS_TOKEN = ''
OANDA_ENVIRONMENT = "practice"
LIMIT_ROWS = 5000


def get_equity(
    since: str,
    until: str,
    instrument: str = 'USD_JPY',
    price: str = 'mid',
    interval: str = 'S5',
) -> pd.DataFrame:
    assert price in ['M', 'A', 'B'],\
        "'price' must be 'M' or 'A' or 'B'."
    cnt = 'mid' if price == 'M' \
        else 'ask' if price == 'A' \
        else 'bid' if price == 'B' \
        else 'mid'
    # interval: http://developer.oanda.com/rest-live-v20/instrument-df/#collapse_definition_1

    params = {
        "from": DateTime(since).value,
        "to": DateTime(until).value,
        "price": price,
        "granularity": interval
    }
    r = instruments.InstrumentsCandles(instrument=instrument, params=params)

    api = API(access_token=OANDA_ACCESS_TOKEN, environment=OANDA_ENVIRONMENT)
    api.request(r)
    raw_list = []
    for raw in r.response['candles']:
        raw_list.append(
            [
                raw['time'],
                raw[cnt]['o'],
                raw[cnt]
                ['h'],
                raw[cnt]['l'],
                raw[cnt]['c'],
                raw['volume']
            ]
        )
    raw_df = pd.DataFrame(
        raw_list,
        columns=[
            'Time',
            f'Open_{cnt}',
            f'High_{cnt}',
            f'Low_{cnt}',
            f'Close_{cnt}',
            'Volume'
        ])
    return raw_df


def add_equities(
    df: pd.DataFrame,
    since: str,
    until: str,
    instrument: str = 'USD_JPY',
    interval: str = 'S5',
) -> pd.DataFrame:
    print(f'since: {since}, until: {until}')
    raw_a = get_equity(
        since=since,
        until=until,
        instrument=instrument,
        price='A',
        interval=interval
    )
    raw_b = get_equity(
        since=since,
        until=until,
        instrument=instrument,
        price='B',
        interval=interval
    )
    raw_m = get_equity(
        since=since,
        until=until,
        instrument=instrument,
        price='M',
        interval=interval
    )

    raw = pd.merge(raw_a, raw_b)
    raw = pd.merge(raw, raw_m)
    raw = raw.set_index('Time')
    raw.index = pd.to_datetime(raw.index)

    df = pd.concat([df, raw])
    return df


def count_rows(
    period: timedelta,
    interval: str,
) -> int:
    unit_time = float(interval[1:]) if len(interval) > 1 else 1.0

    if period.days > 0:
        if 'S' in interval:
            rows_per_day = 24 * 3600 / unit_time
        if 'M' in interval:
            rows_per_day = 24 * 60 / unit_time
        if 'H' in interval:
            rows_per_day = 24 / unit_time
        if 'D' in interval:
            rows_per_day = unit_time
        if 'W' in interval:
            rows_per_day = unit_time / 7.0

        return period.days * rows_per_day

    # period が1日の範囲の場合
    if 'S' in interval:
        rows_per_sec = 1 / unit_time
    if 'M' in interval:
        rows_per_sec = 1 / (60 * unit_time)
    if 'H' in interval:
        rows_per_sec = 1 / (3600 * unit_time)

    return int(period.total_seconds() * rows_per_sec)


def get_candles(
    since: str,
    until: str,
    instrument: str = 'USD_JPY',
    interval: str = 'S5',
) -> pd.DataFrame:
    if type(since) == str:
        since = datetime.strptime(since, '%Y-%m-%d %H:%M:%S')
    if type(until) == str:
        until = datetime.strptime(until, '%Y-%m-%d %H:%M:%S')

    df = pd.DataFrame()

    if until > datetime.now():
        until = datetime.now()

    period = until - since
    n_rows = count_rows(
        period=period,
        interval=interval,
    )
    remain = n_rows
    unit_time = float(interval[1:]) if len(interval) > 1 else 1.0

    while True:
        delta = LIMIT_ROWS * unit_time if remain > LIMIT_ROWS \
            else remain * unit_time
        if 'S' in interval:
            until = since + timedelta(seconds=delta)
        if 'M' in interval:
            until = since + timedelta(minutes=delta)
        if 'H' in interval:
            until = since + timedelta(hours=delta)
        if 'D' in interval:
            until = since + timedelta(days=delta)
        if 'W' in interval:
            until = since + timedelta(weeks=delta)

        df = add_equities(
            df=df,
            since=since,
            until=until,
            instrument=instrument,
            interval=interval,
        )
        since = until
        remain -= LIMIT_ROWS
        if remain <= 0:
            break

    return df
