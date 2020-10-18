# OANDA UTILS

## Setup

### Install

```console
cd oanda_utils
pipenv install
```

### Set credentials in .env

```console
touch .env
```

Write your access token in .env file.

```
OANDA_ACCESS_TOKEN=''
```

## Usage

### Get historical data

Ex: USD/JPY chart 5 sec candle

```py
instrument = 'USD_JPY'
since = datetime.strptime('2005-01-06 00:00:00', '%Y-%m-%d %H:%M:%S')
until = datetime.strptime('2005-01-06 00:10:00', '%Y-%m-%d %H:%M:%S')
interval = 'S5'

df = get_candles(
    since=since,
    until=until,
    instrument=instrument,
    interval=interval,
)
```

## References

[Introduction](http://developer.oanda.com/rest-live-v20/introduction/)

-`interval`: http://developer.oanda.com/rest-live-v20/instrument-df/#collapse_definition_1

## Test

```console
pipenv run python tests/test_get_candles.py
```

Note: Append the module paths in advance.

Ex: tests/test_get_candles.py

```py
import sys
sys.path.append('~/code/oanda_utils')
from candles import get_candles, count_rows
```
