# `itertools.accumulate` — running totals

`accumulate(iterable, func=operator.add, *, initial=None)` yields cumulative results of a binary function applied left-to-right. Lazy equivalent of `numpy.cumsum` / `numpy.cumprod`.

## Default: running sum

```python
from itertools import accumulate

list(accumulate([1, 2, 3, 4, 5]))
# [1, 3, 6, 10, 15]
```

## With `operator.mul`: compound returns

```python
import operator

daily_gross = [1.01, 0.99, 1.02]
list(accumulate(daily_gross, operator.mul))
# [1.01, 0.9999, 1.01990...]
```

## `initial` (3.8+): prepend a starting value

Output length becomes `len(input) + 1`:

```python
list(accumulate([1, 2, 3], operator.add, initial=10))
# [10, 11, 13, 16]
```

## Gross return / NAV series pattern

```python
from itertools import accumulate
import operator

daily_net = [0.01, -0.01, 0.02, 0.005]
nav = list(accumulate(
    (1 + r for r in daily_net),
    operator.mul,
    initial=1.0,
))
# [1.0, 1.01, 0.9999, 1.01990..., 1.02500...]
```

Equivalent to `numpy.cumprod(1 + returns)` prepended with 1.0, but lazy and composable.

## Running max / drawdown tracking

```python
prices = [100, 102, 101, 105, 98, 107]

peaks = list(accumulate(prices, max))
# [100, 102, 102, 105, 105, 107]

drawdowns = [(p - pk) / pk for p, pk in zip(prices, peaks)]
```

## `accumulate` vs `reduce`

| | `accumulate` | `functools.reduce` |
|---|---|---|
| Returns | iterator of all intermediate values | single final value |
| Use for | time series, NAV paths, running stats | scalar fold / aggregate |
| Lazy | yes | no |

## Related

- [core.md](core.md) — chain, islice, product, combinations
- [groupby.md](groupby.md) — consecutive grouping
- [../iterators-generators.md](../iterators-generators.md) — iterator protocol
