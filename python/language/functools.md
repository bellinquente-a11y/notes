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

## Caching and Partial Application

- `@functools.lru_cache(maxsize=256)` — cache results of a function. LRU = least recently used.
- `@functools.cache` (Python 3.9+) — equivalent to `lru_cache(maxsize=None)`. Watch out for memory growth.
- `functools.partial(f, x=1)` — partially apply arguments to create a new callable.

```python
from functools import lru_cache, partial

@lru_cache(maxsize=128)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

double = partial(pow, exp=2)
double(3)  # 9
```
