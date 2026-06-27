# Decorators and `functools`

## Decorators

A function that takes a function as input and returns a new function.

### No arguments — 2 levels of nesting

```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ...
        return func(*args, **kwargs)
    return wrapper
```

`@functools.wraps` preserves the metadata of the original function (name, docstring) instead of exposing the wrapper.

### With arguments — 3 levels of nesting

```python
def my_decorator(x_dec):                # 1. receives decorator arguments
    def decorator(func):                # 2. receives the function being decorated
        def wrapper(*args, **kwargs):   # 3. receives the function call arguments
            ...
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

## Memoization with `@lru_cache`

Memoisation caches the result of a function call keyed on its arguments. On a cache hit, the function body is never executed — the stored result is returned immediately.

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

LRU = Least Recently Used: when `maxsize` entries are stored, the least recently accessed entry is evicted to make room.

### The hashability constraint

The cache key is built from arguments exactly like a `dict` key — every argument must be **hashable**. Passing a `list`, `dict`, or `set` raises `TypeError` at call time.

```python
@lru_cache(maxsize=128)
def process(data: tuple[float, ...]) -> float: ...  # tuple ✓
# process([1.0, 2.0])  → TypeError: unhashable type: 'list'
process((1.0, 2.0))    # ✓
```

Use `tuple` instead of `list`, `frozenset` instead of `set`, `frozen=True` dataclasses instead of mutable ones.

### The determinism constraint

The cache never re-calls the function for a previously seen input. If the output can change for the same input — reads from a DB, file, clock, or RNG — the cached result silently goes stale.

```python
@lru_cache(maxsize=None)
def get_price(symbol: str) -> float:
    return db.query(...)   # BAD: price moves, cache doesn't
```

Memoisation is only correct for **pure functions**: same inputs → same output, always, with no side effects.

### `@cache` — unbounded variant

`@functools.cache` (Python 3.9+) is `lru_cache(maxsize=None)` with no eviction and slightly less overhead. Safe for small, well-bounded input spaces; risky in long-running processes with unbounded inputs.

```python
from functools import cache

@cache
def fib(n: int) -> int:
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

### Introspection and invalidation

```python
fib.cache_info()   # CacheInfo(hits=34, misses=10, maxsize=128, currsize=10)
fib.cache_clear()  # wipe entire cache (no per-key invalidation in stdlib)
```

### Pitfall: caching instance methods

`self` is part of the cache key, so the module-level cache dict holds a **strong reference to `self`**, preventing garbage collection of instances.

For a computed attribute with no arguments, use `@functools.cached_property` — it stores the result on the instance itself:

```python
from functools import cached_property

class Pricer:
    @cached_property
    def fair_value(self) -> float:
        return heavy_computation(self.data)   # computed once, stored on self
```

### Decision guide


| Situation                             | Choice                     |
| ------------------------------------- | -------------------------- |
| Pure function, unbounded inputs       | `@lru_cache(maxsize=N)`    |
| Pure function, small/fixed inputs     | `@cache`                   |
| Computed instance attribute (no args) | `@cached_property`         |
| DB / file / network read              | Do not cache at this layer |
| Per-key expiry or invalidation needed | `cachetools` library       |


## Partial Application

`functools.partial` fixes some arguments of a callable, returning a new callable for the rest:

```python
from functools import partial

square = partial(pow, exp=2)
square(3)  # 9
```

