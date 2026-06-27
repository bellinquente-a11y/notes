# The Data Model and Pythonic Objects

## The Data Model

- The key API of the Python language is the Data Model.
- It is a class framework in which classes have special methods (dunder methods).
- The advantage of dunder methods is uniformity and the ability to apply built-in functions to them.
- Typical examples: `__init__`, `__len__`, [`__getitem__`](subscriptable.md), `__repr__`, `__hash__` and arithmetic operators.
- Emulating sequences is one of the most common uses.

## Pythonic Objects

- String/bytes representation: `__repr__`, `__str__`, `__format__`, `__bytes__`
- Use `__eq__` and `__hash__` to support equality testing and use in sets/dicts.
- `__call__` makes an object callable (i.e., `obj(x)`).
- Decorators `@classmethod` (e.g. alternative constructor) and `@staticmethod` (not very useful).
- Implement `__format__` that parses `format_spec` to use:
  - `format(obj, format_spec)`
  - `'1 BRL = {rate:0.2f} USD'.format(rate=brl)`
  - `f'1 USD = {1 / brl:0.2f} BRL'`
- Make objects immutable by making attributes private with `self.__x`, then define a getter with `@property`.
- Declare the class attribute `__slots__` to save memory.
- Define the class attribute `typecode`, which an instance can override.

## `@dataclass`

- `@dataclass` is a decorator from the `dataclasses` module.
- It automatically generates boilerplate methods like `__init__` and `__repr__`.
- Mainly used for classes that store data.
- Fields are defined using type hints.
- `@dataclass(frozen=True)` makes instances immutable and adds `__hash__`.
- `__post_init__`: validation runs after `__init__`.

```python
from dataclasses import dataclass

@dataclass
class Trade:
    symbol: str
    price: float
```

See also: [oop.md](oop.md) for inheritance, ABCs, and Protocols.