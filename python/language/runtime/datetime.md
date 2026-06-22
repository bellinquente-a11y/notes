# Datetime Parsing

Converting a datetime string to a `datetime.datetime` object.

## Three approaches

### `strptime` — known format

```python
from datetime import datetime

dt = datetime.strptime("2024-06-21 14:30:00", "%Y-%m-%d %H:%M:%S")
```

Supply a format string using `strftime`/`strptime` codes. Raises `ValueError` on mismatch.

Common codes:

| Code | Meaning | Example |
|------|---------|---------|
| `%Y` | 4-digit year | `2024` |
| `%m` | zero-padded month | `06` |
| `%d` | zero-padded day | `21` |
| `%H` | 24h hour | `14` |
| `%M` | minutes | `30` |
| `%S` | seconds | `00` |
| `%f` | microseconds | `000000` |
| `%z` | UTC offset | `+0000` |
| `%I` | 12h hour | `02` |
| `%p` | AM/PM | `PM` |

### `fromisoformat` — ISO 8601 strings (Python ≥ 3.7)

```python
dt = datetime.fromisoformat("2024-06-21T14:30:00")
dt = datetime.fromisoformat("2024-06-21T14:30:00+05:30")
```

- Python 3.11+ handles trailing `Z` natively.
- On 3.10 and below: `s.replace("Z", "+00:00")` before parsing.

### `dateutil.parser.parse` — fuzzy / unknown format

```python
from dateutil import parser  # pip install python-dateutil

dt = parser.parse("June 21 2024 2:30pm")
```

Tries many formats automatically. Convenient for user input or heterogeneous sources; can silently misparse ambiguous strings like `01/02/03`.

## Which to use?

| Situation | Use |
|-----------|-----|
| Known, fixed format | `strptime` |
| ISO 8601 from an API / database | `fromisoformat` |
| Unknown / user-supplied format | `dateutil.parser.parse` |

## Timezone awareness

A `datetime` is either *naive* (no `tzinfo`) or *aware* (has `tzinfo`). Mixing them raises `TypeError`.

```python
from datetime import datetime, timezone

# naive
dt = datetime.strptime("2024-06-21 14:30", "%Y-%m-%d %H:%M")
dt.tzinfo  # None

# aware via format string
dt = datetime.strptime("2024-06-21 14:30 +0000", "%Y-%m-%d %H:%M %z")

# attach tz to a naive datetime (only safe if you know the tz)
dt = dt.replace(tzinfo=timezone.utc)
```

## Going the other way

```python
dt.strftime("%Y-%m-%d")   # → "2024-06-21"
dt.isoformat()             # → "2024-06-21T14:30:00"
```