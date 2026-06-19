# Python

## Usage from CPI

### Run an individual command

```bash
    python -c 'import sys'
```

```bash
    python -c script.py
```

### Run a module

Notice without .py

```bash
    python -m module
```

## The import system

- `sys.path` lists the directories Python searches when importing a module.
- The file `__init__.py` makes a directory a **package** (importable namespace).
- When imported, a module generates a `__pycache__` directory with bytecode compilation cache.

```python
import sys
print(sys.path)         # where Python looks for modules

import finlib
print(finlib.__file__)  # where the package lives
print(finlib.__spec__)  # full module spec
```

### Packages and `__init__.py`

A **package** is a directory with an `__init__.py` file. Without it, `import finlib` fails even if the directory exists on `sys.path`.

```
finlib/
├── __init__.py        ← makes finlib importable
├── models/
│   ├── __init__.py    ← makes finlib.models a subpackage
│   └── trade.py       ← importable as finlib.models.trade
└── utils/
    ├── __init__.py
    └── math.py
```

`__init__.py` can be empty — presence alone is enough. Common uses:

**Flattening the public API** (most common) — re-export symbols so callers don't need to know your internal file structure:

```python
# finlib/models/__init__.py
from .trade import Trade          # "." = current package (relative import)
from .portfolio import Portfolio

# users can now write:
from finlib.models import Trade   # instead of finlib.models.trade.Trade
```

**`__all__`** — controls what `from package import *` exports:

```python
__all__ = ['Trade', 'Portfolio']
```

**Practical rules:**
- Empty `__init__.py` for internal subpackages — just to make them importable.
- Use re-exports in the top-level `__init__.py` to define your public API.
- Don't import heavy dependencies at the top of `__init__.py` — it runs on every `import finlib`.

> Python 3.3+ also supports **namespace packages** (directories without `__init__.py`) for splitting a package across multiple directories. This is a niche feature; for normal projects always use `__init__.py`.

## The Data Model

- The key API (?) of the Python language is the Data Model
- The Data Model is a class framework in which classes have special methods (dunder methods)
- The advantage of dunder methods is uniformity and the ability to apply to them the built-in libraries
- Typical examples are: `__init__`, `__len__`, `__get_item__`, `__repr__`, `__hash__` and all the operations.
- Emulating sequences is one of the most common use.
  

## Pythonic objects

- Important string/bytes representaion methdos of an object: `__repr__`, `__str__`, `__format__`, `__bytes__`
- Use `__eq__` and `__hash__` to support testing
- `__call__` makes an object callable (i.e., you can use it as a function `obj(x)`)
- Decorators `@classmethod` (e.g. alternative constructor) and `@staticmethod` (not very useful)
- Implement `__format__` that parses `format_spec` to use:
    - `format(obj, format_spec)`
    - `'1 BRL = {rate:0.2f} USD'.format(rate=brl)'`
    - `f'1 USD = {1 / brl:0.2f} BRL'` 
- Make objects immutable by making attributes private with `self.__x`, then define the getter with `@property`
- Declare the class attribute `__slots__` to save memory
- Define the class attribute `typecode`, which an instance can overrride


## `@dataclass`

- `@dataclass` is a decorator from the `dataclasses` module.
- It automatically generates boilerplate methods like `__init__` and `__repr__`.
- Mainly used for classes that store data.
- Fields are defined using type hints.
- `@dataclass(frozen=True)` makes instances immutable and adds `__hash__`
- `__post_init__`: validation runs after `__init__`
- Example:

```python
from dataclasses import dataclass

@dataclass
class Trade:
    symbol: str
    price: float
```

## Inheritance

- Composition (x has y) is preferred over inheritance (x is y)
- Multiple inhertiance available (`class U(A,B)`). The MRO (method resolution order) determines the order of the methods called. Check the `self.__mro__` attribute.
- The MRO follows the C3 algorithm.
- Use the `super()` function to refer to the superclass
- Issues with subclassing built-in types: consider before doing
- Some people say only `ABC` (abstract base classes) should be subclassed

### abstract base classes

```python 
from abc import ABC, abstractmethod

class Instrument(ABC):

    @property
    @abstractmethod
    def symbol(self) -> str: ...

    @abstractmethod
    def price(self) -> Decimal: ...
```

## Protocols

### Protocols in Python

- `Protocol` defines an interface based on object structure.
- It comes from `typing`: `from typing import Protocol`.
- A class satisfies a protocol if it has the required methods/attributes.
- It does **not** need to inherit from the protocol explicitly.
- This is called **structural typing**.
- It matches Python’s duck typing idea: “if it behaves correctly, it is acceptable”.
- Protocols are mainly useful for static type checkers like [`mypy`](mypy.md).
- They help document expected behaviour without forcing class hierarchies.
- Example: a `Runnable` protocol may require a `run()` method.
- Any class with a compatible `run()` method can be used as `Runnable`.
- By default, protocols do not enforce behaviour at runtime.
- `@runtime_checkable` allows limited `isinstance()` checks.
- Protocols are useful when flexibility and loose coupling matter.

### Protocols vs ABCs

- `ABC` means **Abstract Base Class**.
- ABCs use **nominal typing**: a class must explicitly inherit from the base class.
- Protocols use **structural typing**: a class only needs the right shape.
- ABCs can prevent incomplete subclasses from being instantiated.
- Protocols usually rely on static type checkers rather than runtime checks.
- Use an ABC when you want explicit inheritance and runtime enforcement.
- Use a Protocol when you want flexible duck typing with type hints.
- ABCs are better when the base class provides shared implementation.
- Protocols are better when unrelated classes should satisfy the same interface.
- ABC: “you belong to this family.”
- Protocol: “you behave in the required way.”
- In modern Python, protocols are often preferred for lightweight interfaces.
- ABCs remain useful for frameworks, plugins, and strict class designs.

## Iterators & generators

Iteration is fundamental in data processing, esp to fetch data **lazily** (one at a time as needed; the oppsite is **eagerly**).

### Iterables and iterators

- **Iterable** object that implements `__iter__`, which returns an **iterator**; if not available it uses `__getitem__` 
- **Iterator** object that defines `__next__` (returning a value or `raise StopIteration`) and `__iter__` (returning self).
- Iterable objects used in: 
    - `for` loops
    - list, dict and set comprehensions (i.e., `[2*s for s in x]`)
    - unpacking assignments (i.e., `*x`)

### Generators

- A **generator function** is a function that has the `yield` keyword (`return` not needed).
- It returns a **generator** object, which is an iterator built by the compiler.
- Instead of the `yield` keyword, generator can be build by a **generator expression**, e.g. `(2*s for s in x)`
- Generators can be used to implement iterators.
- `yield from` is used to allow a generator to delegate to a subgenerator.
- Generators are a secret weapon for large datasets.

### Generators in the standard library (built-in or `itertools`)

Avoid reinventing the wheel.

- Filtering: `compress`, `dropwhile`, `filter`, `isslice`, `takewhile`
- Mapping: `accumulate`, `enumerate`, `map`
- Merging: `chain`, `chain.from_iterable`, `product`, `zip`, `zip_longest`
- Multiple outputs: `combinations`, `count`, `pairwise`, `cycle`, `permutations`, `repeat`
- Rearraging: `groupby`, `reversed`, `tee`
- Reducing functions: `all`, `any`, `max`, `min`, `reduce`, `sum`


## Context managers

Used to do something temporarily, then relaibly undo it.
Big advantage: it is hard to leave the environment in a bad state. 

```python
with manager() as x:
    do_work(x)
```

means:
1. enter/setup the source
2. give me something to use as x
3. run the block
4. exit/cleean up, even if exceptions arise

and is equivalent to

```python
x = setup()
try:
    do_work(x)
finally:
    cleanup()
```

Used for:
- file reading
- database connections
- threading
- timing
- changing settings temporarily

### Context manager defined as a class

It's a class that requires a `__enter__` and a `__exit__` method.

### Context manager from generator (`@contextlib`)

```python
@contextmanager
def manager():
    setup_code()
    try:
        yield value   # this becomes the result of __enter__()
    finally:
        cleanup_code()  # this behaves like __exit__()
```

## Decorators

A function that takes a function as an input and returns a new function.

### No argument

With no argument, it requires 2 levels of nesting.

```python
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper():
        ...
    return wrapper
```

The `functools.wrap` decorator is used to preserve the metadata of the original function (as opposed to the uninteresting wrapper).

### With arguments

Three levels of nesting needed.

```python
def my_decorator(x_dec):                # 1. receives decorator arguments
    def decorator(func):                # 2. receives the function being decorated
        def wrapper(*args, **kwargs):   # 3. receives the function call arguments
            ...
        return wrapper
    return decorator
```

## Caching & partial (`functools` module)

- Cache the results of a function using the decorator `@functools.lru_cache(maxsize-256)`. LRU = last recently used.
- From Python 3.9 `cache = lru_cache(maxsize=None)`. Watch out for memory explosion.
- `functools.partial` is used to partially apply arguments, e.g. `new_f = partial(f, x=1)`

