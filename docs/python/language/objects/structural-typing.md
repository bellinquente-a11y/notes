# Structural Typing

Two ways a type system decides "is X acceptable where T is expected?":

- **Nominal** — X must be *declared* as T (via inheritance or registration).
- **Structural** — X must have T's *shape*: the right methods and attributes, no declaration needed.

Python's runtime has always been structural (duck typing). `Protocol` (PEP 544, Python 3.8+) extends that to static analysis via [mypy](../../tooling/mypy.md).

## `Protocol`

```python
from typing import Protocol

class Serialisable(Protocol):
    def to_dict(self) -> dict[str, object]: ...

def save(obj: Serialisable) -> None:
    data = obj.to_dict()   # mypy checks structurally
```

Any class with a compatible `to_dict` method satisfies `Serialisable` — **without inheriting from it**. Third-party classes work out of the box.

Protocols can also require attributes:

```python
class HasName(Protocol):
    name: str
```

## Protocol vs ABC

| | `Protocol` | `abc.ABC` |
|--|-----------|-----------|
| Declaration required | No | Yes — must subclass |
| Third-party classes | Works | Won't unless they inherit |
| Enforcement | mypy (static) | `abstractmethod` (runtime) |
| `isinstance` | Only with `@runtime_checkable` | Yes |

!!! tip "When to reach for each"
    Use `Protocol` when accepting any object with the right shape (especially from libraries you don't control). Use `ABC` when you own the hierarchy and need to enforce implementation at construction time.

## `@runtime_checkable`

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Quackable(Protocol):
    def quack(self) -> str: ...

isinstance(obj, Quackable)   # True if obj has .quack — checks name only, not signature
```

Use sparingly — it only verifies method *existence*, not signatures.

## Protocol inheritance

```python
class Readable(Protocol):
    def read(self) -> bytes: ...

class Writable(Protocol):
    def write(self, data: bytes) -> int: ...

class ReadWritable(Readable, Writable, Protocol): ...   # include Protocol in MRO
```

!!! warning "Always include `Protocol` when inheriting protocols"
    Omitting it makes mypy treat the subclass as a regular nominal class, breaking structural checking.

## `Callable` is structural too

`Callable[[int], str]` — accepts any callable with that signature (function, lambda, `__call__` object). Structural typing working implicitly in everyday annotations.

## Mental model

> Nominal: "Is it *declared* to be the right type?"  
> Structural: "Does it *have the right shape*?"

Related: [typing.md](typing.md) for `Literal` and other constructs; [mypy.md](../../tooling/mypy.md) for static checking configuration.
