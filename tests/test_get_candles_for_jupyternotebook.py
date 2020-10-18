def test_core(
    since: str,
    until: str,
    instrument: str = 'USD_JPY',
    interval: str = 'S5',
):
    THRESH = 0.5
    if type(since) == str:
        since = datetime.strptime(since, '%Y-%m-%d %H:%M:%S')
    if type(until) == str:
        until = datetime.strptime(until, '%Y-%m-%d %H:%M:%S')
    df = get_candles(
        since=since,
        until=until,
        instrument=instrument,
        interval=interval,
    )
    period = until - since
    n_rows = count_rows(
        period=period,
        interval=interval,
    )

    n_df = len(df)
    cond = (THRESH * n_rows < n_df) and (n_df <= n_rows)
    if not cond:
        print(f'n_df: {n_df}, n_rows: {n_rows}')
        print(f'df.head():\n', df.head())
        print(f'df.tail():\n', df.tail())
    return cond


def test_get_candles_for_second_interval():
    instrument = 'USD_JPY'
    since = datetime.strptime('2005-01-06 00:00:00', '%Y-%m-%d %H:%M:%S')
    until = datetime.strptime('2005-01-06 01:00:00', '%Y-%m-%d %H:%M:%S')
    interval = 'S5'

    cond = test_core(
        since=since,
        until=until,
        instrument=instrument,
        interval=interval,
    )
    assert cond


def test_get_candles_for_minute_interval():
    instrument = 'USD_JPY'
    since = datetime.strptime('2005-01-06 00:00:00', '%Y-%m-%d %H:%M:%S')
    until = datetime.strptime('2005-01-06 05:00:00', '%Y-%m-%d %H:%M:%S')
    interval = 'M1'

    cond = test_core(
        since=since,
        until=until,
        instrument=instrument,
        interval=interval,
    )
    assert cond


def test_get_candles_for_hour_interval():
    instrument = 'USD_JPY'
    since = datetime.strptime('2005-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    until = datetime.strptime('2005-01-31 00:00:00', '%Y-%m-%d %H:%M:%S')
    interval = 'H1'

    cond = test_core(
        since=since,
        until=until,
        instrument=instrument,
        interval=interval,
    )
    assert cond


def test_get_candles_for_day_interval():
    instrument = 'USD_JPY'
    since = datetime.strptime('2005-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    until = datetime.strptime('2020-12-31 00:00:00', '%Y-%m-%d %H:%M:%S')
    interval = 'D'

    cond = test_core(
        since=since,
        until=until,
        instrument=instrument,
        interval=interval,
    )
    assert cond


def test_get_candles_for_week_interval():
    instrument = 'USD_JPY'
    since = datetime.strptime('2005-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    until = datetime.strptime('2020-12-31 00:00:00', '%Y-%m-%d %H:%M:%S')
    interval = 'W'

    cond = test_core(
        since=since,
        until=until,
        instrument=instrument,
        interval=interval,
    )
    assert cond


test_get_candles_for_second_interval()
test_get_candles_for_minute_interval()
test_get_candles_for_hour_interval()
test_get_candles_for_day_interval()
test_get_candles_for_week_interval()
