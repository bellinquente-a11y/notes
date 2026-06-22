# Classes: Inheritance and Interfaces

## Inheritance

- Composition (x has y) is preferred over inheritance (x is y).
- Multiple inheritance available (`class U(A, B)`). The MRO (method resolution order) determines which method is called. Check `cls.__mro__`.
- The MRO follows the C3 linearisation algorithm.
- Use `super()` to call the next class in the MRO.
- Subclassing built-in types has pitfalls — consider before doing.
- Some say only ABCs (abstract base classes) should be subclassed.

## Abstract Base Classes (ABCs)

```python
from abc import ABC, abstractmethod

class Instrument(ABC):

    @property
    @abstractmethod
    def symbol(self) -> str: ...

    @abstractmethod
    def price(self) -> Decimal: ...
```

- ABCs use **nominal typing**: a class must explicitly inherit from the base class.
- Subclasses that don't implement all abstract methods cannot be instantiated.
- Better for frameworks, plugins, and strict class designs.
- ABCs are better when the base class provides shared implementation.

## Protocols

- `Protocol` defines an interface based on object structure, from `typing`: `from typing import Protocol`.
- A class satisfies a protocol if it has the required methods/attributes — no explicit inheritance needed.
- This is called **structural typing**, matching Python's duck typing idea.
- Protocols are mainly useful for static type checkers like `[mypy](../../tooling/mypy.md)`.
- By default, protocols do not enforce behaviour at runtime.
- `@runtime_checkable` allows limited `isinstance()` checks.

## Protocols vs ABCs


|                      | ABC                               | Protocol                        |
| -------------------- | --------------------------------- | ------------------------------- |
| Typing               | Nominal                           | Structural                      |
| Requires inheritance | Yes                               | No                              |
| Runtime enforcement  | Yes                               | Optional (`@runtime_checkable`) |
| Best for             | Frameworks, shared implementation | Flexible duck typing            |


- ABC: "you belong to this family."
- Protocol: "you behave in the required way."
- In modern Python, protocols are often preferred for lightweight interfaces.

See also: [data-model.md](data-model.md) for dunder methods and `@dataclass`.