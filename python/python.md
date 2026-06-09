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
- Protocols are mainly useful for static type checkers like `mypy`.
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