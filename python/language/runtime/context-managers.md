# Context Managers

Used to do something temporarily, then reliably undo it. Big advantage: hard to leave the environment in a bad state.

```python
with manager() as x:
    do_work(x)
```

Equivalent to:

```python
x = setup()
try:
    do_work(x)
finally:
    cleanup()
```

Common uses: file reading, database connections, threading, timing, changing settings temporarily.

## Class-based Context Manager

Requires `__enter__` and `__exit__` methods.

```python
class Manager:
    def __enter__(self):
        setup()
        return value

    def __exit__(self, exc_type, exc_val, exc_tb):
        cleanup()
        return False  # don't suppress exceptions
```

## Generator-based (`@contextmanager`)

```python
from contextlib import contextmanager

@contextmanager
def manager():
    setup_code()
    try:
        yield value   # becomes the result of __enter__()
    finally:
        cleanup_code()  # behaves like __exit__()
```
