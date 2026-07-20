---
tags:
  - typing
quiz: core
---

# typing module — selected constructs

Key types from `typing` (and `typing_extensions`) that go beyond basic annotations. Enforced by [mypy](../../tooling/mypy.md) and [Pydantic](../../libraries/pydantic/pydantic.md) at parse time; ignored by the Python runtime.

---

## `Literal` — restrict to specific values

Narrows a type to a fixed set of constants rather than the broad base type.

```python
from typing import Literal

Side = Literal['BUY', 'SELL']

def place_order(side: Side) -> None: ...

place_order('BUY')    # ok
place_order('hold')   # mypy error
```

Allowed value types: `str`, `int`, `bool`, `bytes`, `None`, Enum members. Not variables or mutable types.

### Subtype direction

!!! warning "A plain str variable fails assignment to a Literal type"
    `Literal['BUY']` is a subtype of `str`, but `str` is *not* a subtype of `Literal['BUY', 'SELL']`. This means passing a `str` variable (even one that happens to hold `'BUY'`) to a `Literal`-typed parameter is a mypy error. You must either narrow the variable first (e.g. via a branch or `assert`) or use a `Literal` annotation at the assignment site.

`Literal['BUY']` is a **subtype** of `str` — narrowing is always safe.  
`str` is **not** a subtype of `Literal['BUY']` — a bare `str` variable could be anything.

```python
x: str = 'BUY'
place_order(x)   # mypy error: str is not assignable to Literal['BUY', 'SELL']
```

### Type narrowing in branches

```python
def process(side: Literal['BUY', 'SELL']) -> None:
    if side == 'BUY':
        ...  # checker knows: side is Literal['BUY']
    else:
        ...  # checker knows: side is Literal['SELL']
```

### Overloads — different return types per literal argument

```python
from typing import overload

@overload
def parse(raw: str, mode: Literal['int']) -> int: ...
@overload
def parse(raw: str, mode: Literal['float']) -> float: ...
def parse(raw: str, mode: str) -> int | float:
    return int(raw) if mode == 'int' else float(raw)

x = parse("42", "int")     # x: int
y = parse("3.14", "float") # y: float
```

### Runtime introspection

```python
from typing import get_args

get_args(Side)  # ('BUY', 'SELL')

# Manual validation without Pydantic:
if value not in get_args(Side):
    raise ValueError(f"invalid side: {value!r}")
```

### `Literal` vs `Enum`

| | `Literal` | `Enum` |
|--|-----------|--------|
| Runtime type | plain `str`/`int` | `Enum` instance |
| Methods | none | can add |
| Pydantic JSON | natural | needs `.value` |
| Use when | static valid-value set, no logic | need behaviour or identity |

### `TypeAlias`

```python
from typing import TypeAlias
Side: TypeAlias = Literal['BUY', 'SELL']  # explicit alias (Python 3.10+)
```

Python 3.12 adds `type Side = Literal['BUY', 'SELL']` as a cleaner alternative.

### Version

Introduced in Python 3.8 (PEP 586).

---

## `cast` — override the checker, not the runtime

`cast(Type, value)` tells the type checker "treat this as `Type`" with zero runtime effect — no `isinstance` check, no conversion. It's `return value` under the hood.

```python
from typing import cast

raw: dict[str, object] = get_config()
port = cast(int, raw["port"])  # checker now treats port as int
```

Use it when a checker can't infer a type you know to be true (e.g. after `json.loads()`, or a loose library stub) — not to silence errors you don't understand.

!!! warning "No runtime safety"
    If the value isn't actually `Type`, `cast` won't catch it — the bug surfaces later, elsewhere. Prefer `assert isinstance(x, T)` when you want the check enforced at runtime; reach for `cast` when the type is unrepresentable at runtime (generics like `list[int]`, Protocols) or verification is genuinely too costly.
