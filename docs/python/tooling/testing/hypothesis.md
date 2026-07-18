---
tags:
  - testing
quiz: detail
---

# Hypothesis

Property-based testing: instead of hand-picking inputs, you declare *invariants* that must hold for all valid inputs, and Hypothesis generates hundreds of random cases to falsify them. When a failure is found, it **shrinks** the input to the smallest counterexample.

Install: `pip install hypothesis` (integrates with [pytest](pytest.md) natively, no plugin needed).

## Core pattern

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers(), min_size=1))
def test_reverse_is_involution(xs):
    assert list(reversed(list(reversed(xs)))) == xs
```

`@given` injects generated values; the test runs ~100 times (default).

## Strategies

Strategies (`st.*`) are recipes for generating data:

```python
st.integers(min_value=0, max_value=100)
st.floats(min_value=-0.5, max_value=0.5, allow_nan=False, allow_infinity=False)
st.text()
st.lists(st.integers(), min_size=1, max_size=50)
st.one_of(st.integers(), st.none())
```

Compose freely: `st.lists(st.floats(...), min_size=1)`.

## Multiple parameters

`@given` accepts one strategy per test argument — positional or keyword — and draws each independently every example:

```python
@given(st.integers(), st.integers())
def test_add_commutative(a, b):
    assert a + b == b + a

@given(a=st.integers(min_value=0), b=st.floats(allow_nan=False))
def test_mixed_kwargs(a, b):
    ...
```

When parameters must be *related* (e.g. `low <= high`), don't generate them independently and filter — Hypothesis may discard most examples before finding a valid one. Use `st.composite` to draw dependently instead:

```python
from hypothesis import strategies as st

@st.composite
def low_high(draw):
    low = draw(st.integers(min_value=0, max_value=100))
    high = draw(st.integers(min_value=low, max_value=100))
    return low, high

@given(low_high())
def test_range(pair):
    low, high = pair
    assert low <= high
```

!!! tip "Filtering vs composite"
    `st.tuples(a, b).filter(lambda p: p[0] <= p[1])` works but wastes examples on rejected draws; `st.composite` builds only valid combinations and shrinks them together.

## Constrain, don't filter

`assume(condition)` and `.filter(predicate)` both generate a candidate and discard it if false — same cost, different timing. Every discarded example still counts against the example budget; too high a discard rate raises `FailedHealthCheck` (`HealthCheck.filter_too_much`) instead of silently retrying forever.

```python
# Wastes ~50% of draws
@given(st.integers(), st.integers())
def test_range(low, high):
    assume(low <= high)
    ...

# Can't generate an invalid pair
@st.composite
def ordered_pair(draw):
    low = draw(st.integers())
    high = draw(st.integers(min_value=low))
    return low, high
```

Filtering is fine for cheap, rarely-triggered exclusions (`.filter(lambda x: x != 0)`); it becomes a problem when two draws are tightly coupled, which is exactly when `st.composite` pays off.

## Bounding `st.floats`

`st.floats()` with no arguments generates the full IEEE 754 space — NaN, ±infinity, subnormals included — because a float-typed parameter accepts them just as validly as `3.14`. `allow_nan=False`, `allow_infinity=False`, and a bounded `min_value`/`max_value` are **domain statements**, not workarounds: each says "this quantity cannot be NaN / infinite / out of range" in this specific system. Make that claim consciously — checking it actually holds — rather than adding it just to silence a failing assertion like `x == x`. If NaN handling is part of the contract, test it separately instead of folding it into the same strategy as everything else.

## Generating valid Pydantic models with `st.builds`

`st.builds(cls, **kwargs)` calls `cls(**kwargs)` with each keyword drawn from its strategy — works for any callable, including a [Pydantic](../../libraries/pydantic/pydantic.md) `BaseModel`:

```python
trades = st.builds(
    Trade,
    symbol=st.text(min_size=1, max_size=10),
    price=st.decimals(min_value="0.01", max_value="100000", places=2),
    qty=st.integers(min_value=1, max_value=10_000),
    side=st.sampled_from(['BUY', 'SELL']),
)
```

Modern Hypothesis registers hooks for installed Pydantic models, so `st.builds(Trade)` alone can infer strategies from field types — handy for smoke-testing, less useful when you need to steer specific fields toward boundary values.

!!! note "Hypothesis and Pydantic disagree about 'valid'"
    `st.text()` describes what the *type system* allows; `Field(..., min_length=1)` describes what the *domain* allows. `st.text()` happily generates `""`, which then raises `ValidationError` — a strategy that doesn't mirror the `Field` constraints wastes most of its draws on rejected instances. Similarly, `st.decimals()` can generate `Decimal("NaN")` by default (same philosophy as `st.floats()` above), which fails a `Field(..., gt=0)` check every time. The fix is the same as above: tighten the strategy to mirror the constraint, not filter after the fact.

## Composite strategies with shared, dependent structure

`@st.composite` draws values sequentially, using earlier draws to parameterize later ones — the tool for structure that independent strategies can't express, like a portfolio where every trade shares a small symbol pool and timestamps stay ordered:

```python
@st.composite
def portfolios(draw, min_trades=1, max_trades=20):
    symbols = draw(st.lists(
        st.text(alphabet=st.characters(whitelist_categories=["Lu"]), min_size=1, max_size=4),
        min_size=1, max_size=5, unique=True,
    ))
    n = draw(st.integers(min_value=min_trades, max_value=max_trades))

    timestamps = [draw(st.datetimes())]
    for _ in range(n - 1):
        offset = draw(st.integers(min_value=1, max_value=3600))
        timestamps.append(timestamps[-1] + timedelta(seconds=offset))

    trades = draw(st.lists(
        st.builds(Trade, symbol=st.sampled_from(symbols), ...),  # shared pool, not per-trade
        min_size=n, max_size=n,
    ))
    return list(zip(timestamps, trades))
```

Ordering timestamps by appending `previous + offset` guarantees the invariant by construction — no post-hoc sort that would mask a real ordering bug in the code under test. Composite strategies also shrink coherently: because later draws depend on earlier ones, shrinking preserves the relationships (fewer trades, smaller offsets) instead of producing an incoherent partial state.

## Property patterns

| Pattern | Example assertion |
|---|---|
| Invariant | `result <= 0` always |
| Round-trip | `decode(encode(x)) == x` |
| Commutativity | `f(a, b) == f(b, a)` |
| Idempotence | `f(f(x)) == f(x)` |
| Boundary | `f([x]) == base_case` |

## `max_drawdown` example

Maximum Drawdown (MDD) = largest peak-to-trough decline in a cumulative return series.

```python
def max_drawdown(returns: list[float]) -> float:
    cumulative = peak = 1.0
    max_dd = 0.0
    for r in returns:
        cumulative *= (1 + r)
        peak = max(peak, cumulative)
        max_dd = min(max_dd, (cumulative - peak) / peak)
    return max_dd
```

Three properties that always hold:

```python
from hypothesis import given, strategies as st

_returns = st.lists(
    st.floats(min_value=-0.5, max_value=0.5, allow_nan=False, allow_infinity=False),
    min_size=1,
)

@given(_returns)
def test_nonpositive(returns):        # Property 1: sign contract
    assert max_drawdown(returns) <= 0

@given(st.lists(
    st.floats(min_value=0, max_value=0.5, allow_nan=False, allow_infinity=False),
    min_size=1,
))
def test_nonneg_returns(returns):     # Property 2: no decline → no drawdown
    assert max_drawdown(returns) == 0.0

@given(st.floats(min_value=-0.5, max_value=0.5, allow_nan=False, allow_infinity=False))
def test_single_element(r):           # Property 3: base case
    assert max_drawdown([r]) == 0.0
```

!!! note "Why bound the floats?"
    `min_value=-0.5, max_value=0.5` keeps cumulative return away from 0 and ∞, preventing `nan` from IEEE 754 edge cases masking actual bugs. Test NaN behaviour separately if needed.

!!! tip "Shrinking"
    If Property 1 fails on `[0.1, -0.2, 0.3]`, Hypothesis shrinks it to `[-0.1]` — the minimal list that still triggers the bug. Fix the implementation to handle that case and the shrunk example becomes the regression anchor.

## Settings

```python
from hypothesis import settings, HealthCheck

@settings(max_examples=500, suppress_health_check=[HealthCheck.too_slow])
@given(_returns)
def test_nonpositive(returns):
    assert max_drawdown(returns) <= 0
```

- `max_examples` (default 100): number of passing cases to generate.
- `deadline`: fail with `DeadlineExceeded` if one example exceeds N ms (default 200ms) — catches accidental quadratic blowups or I/O sneaking into what should be a pure-function test. Set `deadline=None` for tests that are legitimately slow (large composite structures, real fixtures) rather than disguising the slowness.
- `.hypothesis/` directory: Hypothesis stores failures across runs and replays them first on the next run.

## Pin explicit cases alongside properties

```python
from hypothesis import example

@given(_returns)
@example([-0.5])   # always runs, acts as a regression test
def test_nonpositive(returns):
    assert max_drawdown(returns) <= 0
```

## Reproducing a failure with the example blob

`@settings(print_blob=True)` prints an encoded reproduction blob alongside a falsifying example:

```
Falsifying example: test_range(pair=(3, 1))
You can add @reproduce_failure('6.100.0', b'AXicY2BAAAAAOgAB') as a decorator
on this test to reproduce this failure.
```

Pasting `@reproduce_failure(...)` onto the test replays that exact generated value deterministically, bypassing the random search — useful when a failure came from a complex composite value (a whole generated portfolio) that's tedious to reconstruct from the printed repr, or when a fresh `@given` run wouldn't hit the same case again. It's version-pinned to the Hypothesis release that produced it, so treat it as a short-term local reproduction aid — once you've isolated the concrete failing value, promote it to a permanent `@example(...)` and delete the decorator.

## Hypothesis vs parametrize

| Scenario | Use |
|---|---|
| Known edge cases | `@pytest.mark.parametrize` |
| Mathematical invariants | `@given` |
| Round-trip / commutativity | `@given` |
| Side-effect-heavy integration | plain pytest fixtures |
