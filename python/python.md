# Python

## Usage from CPI

```bash
    python -c 'import sys'
```

```python
    import sys
```

## The import system

- sys.path includes the folders looked by python when importing a module
- The file `__init__.py` makes a directory a package.
- When imported, a module generates a `__pycache__` directory with bytecode compilation cache

```bash
import sys
print(sys.path)   # where Python looks for modules

import finlib
print(finlib.__file__)   # where the package lives
print(finlib.__spec__)   # full module spec
```

## The Data Model

- The key API (?) of the Python language is the Data Model
- The Data Model is a class framework in which classes have special methods (dunder methods)
- The advantage of dunder methods is uniformity and the ability to apply to them the built-in libraries
- Typical examples are: `__init__`, `__len__`, `__get_item__`, `__repr__`, `__hash__` and all the operations.
- Emulating sequences is one of the most common use.
  

## Pythonic objects

- Important string/bytes representaion methdos of an object: `__repr__`, `__str__`, `__format__`, `__bytes__`
- Use `__eq__` and `__hash__` to support testing
- Decorators `@classmethod` (e.g. alternative constructor) and `@staticmethos` (not very useful)
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