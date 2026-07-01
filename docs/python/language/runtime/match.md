# match / case (Python 3.10+)

Python's switch-case equivalent — but more powerful: **structural pattern matching** that dispatches on type, shape, and value simultaneously.

## Basic value matching

```python
match command:
    case "quit":   print("quitting")
    case "start":  print("starting")
    case _:        print("unknown")   # wildcard default, never binds a variable
```

First matching case wins; no fallthrough. If nothing matches and there's no `_`, nothing happens.

## Matching on class type — the main use case

```python
from dataclasses import dataclass

@dataclass
class BuyOrder:  symbol: str; qty: float
@dataclass
class SellOrder: symbol: str; qty: float

match order:
    case BuyOrder(symbol=s, qty=q):   print(f"buy {q} {s}")
    case SellOrder(symbol=s, qty=q):  print(f"sell {q} {s}")
    case _:                           raise ValueError(order)
```

Pattern simultaneously checks the type **and** extracts fields into local variables.

## Dict and sequence patterns

```python
# Dict — matches any dict containing these keys
match event:
    case {"type": "trade", "symbol": sym, "qty": qty}:
        record(sym, qty)

# Sequence
match tokens:
    case []:             ...   # empty
    case [x]:            ...   # exactly one
    case [first, *rest]: ...   # head + tail
```

## OR patterns and guards

```python
match status:
    case "pending" | "processing":   print("in progress")

match order:
    case BuyOrder(qty=q) if q > 1000:   print("large — needs approval")
    case BuyOrder(qty=q):               print(f"buy {q}")
```

## Gotcha: bare names are capture variables, not constants

```python
BUY = "BUY"
match side:
    case BUY:      # WRONG — captures into a new variable named BUY
    case "BUY":    # RIGHT — literal match
    case Side.BUY: # RIGHT — dotted name looks up the constant
```

!!! warning "No constants in patterns"
    A bare name like `BUY` in a pattern is always a capture variable. Use string/int literals or dotted names (`Enum.MEMBER`, `Class.ATTR`) to match against a known value.

## Pre-3.10 alternative: dict dispatch

```python
actions = {"quit": do_quit, "start": do_start}
actions.get(command, do_default)()
```

Fine for simple value → callable dispatch; `match` is better when you need type checks or destructuring.

!!! tip "match vs if/elif"
    Use `match` when dispatching on **type or structure** (replaces `isinstance` chains). Use `if/elif` for arbitrary boolean conditions — `match` guards are limited to one expression per case.
