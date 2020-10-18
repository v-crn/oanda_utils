import unittest
from datetime import datetime, timedelta
from candles import get_candles, count_rows
import sys
sys.path.append('/mnt/e/Code/v-crn/ML/Investments/oanda_utils')


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
    return (THRESH * n_rows < n_df) and (n_df <= n_rows)


class TestGetCandles(unittest.TestCase):
    """
    test class of get_candles.py
    """

    def test_get_candles_for_second_interval(self):
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
        self.assertTrue(cond)

    def test_get_candles_for_minute_interval(self):
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
        self.assertTrue(cond)

    def test_get_candles_for_hour_interval(self):
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
        self.assertTrue(cond)

    def test_get_candles_for_day_interval(self):
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
        self.assertTrue(cond)

    def test_get_candles_for_week_interval(self):
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
        self.assertTrue(cond)


if __name__ == "__main__":
    unittest.main()
