# The Import System

- `sys.path` lists the directories Python searches when importing a module.
- `__init__.py` makes a directory a **package** (importable namespace).
- When imported, a module generates a `__pycache__` directory with bytecode.

```python
import sys
print(sys.path)         # where Python looks
import finlib
print(finlib.__file__)  # where the package lives
```

## Package structure

```
mylib/
├── __init__.py         ← makes mylib importable
├── models/
│   ├── __init__.py     ← makes mylib.models a subpackage
│   ├── trade.py        ← mylib.models.trade
│   └── portfolio.py
└── utils/
    ├── __init__.py
    └── math.py
```

---

## Absolute vs relative imports

**Absolute** (recommended everywhere, required in scripts):

```python
from mylib.models.trade import Trade
from mylib.models import Trade        # only if __init__.py re-exports it
```

**Relative** (inside the package only — fail when run as `__main__`):

```python
# inside mylib/models/portfolio.py
from .trade import Trade          # sibling module
from . import trade               # sibling module object
from .. import utils              # parent's subpackage
from ..utils.math import sharpe   # grandparent-relative
```

Dots = levels up: `.` current package, `..` parent, `...` grandparent.

---

## Controlling the public API via `__init__.py`

Re-export symbols so callers use a stable, flat API without knowing internal file structure:

```python
# mylib/models/__init__.py
from .trade import Trade
from .portfolio import Portfolio

# caller can now write:
from mylib.models import Trade    # instead of mylib.models.trade.Trade
```

**`__all__`** controls what `from package import *` exposes and serves as the canonical public-API declaration:

```python
__all__ = ["Trade", "Portfolio"]
```

**Explicit re-export for mypy** — by default mypy treats `from .trade import Trade` in `__init__.py` as a private import. Signal intent with `as`:

```python
from .trade import Trade as Trade           # "as X" = intentional re-export
from .portfolio import Portfolio as Portfolio
```

!!! warning "Keep `__init__.py` thin"
    Everything in `__init__.py` runs on every `import mylib`. Heavy imports (numpy, a DB driver) placed there add startup latency to all callers. Re-export names; let submodules do the heavy lifting.

---

## Circular imports

Happen when two modules import each other. Symptoms: `ImportError: cannot import name 'X' from partially initialized module`.

**Fix 1 — restructure (best)**: extract shared types to a third module that neither imports:

```
models/base.py      ← shared types, no sibling imports
models/trade.py     ← imports from base only
models/portfolio.py ← imports from base only
```

**Fix 2 — deferred import**: move the import inside the function that needs it:

```python
def get_trades(self):
    from .trade import Trade    # runs at call time, not module load time
    return [Trade(...) for ...]
```

**Fix 3 — `TYPE_CHECKING` guard** (type annotations only):

```python
from __future__ import annotations   # annotations become lazy strings
from typing import TYPE_CHECKING

if TYPE_CHECKING:                    # False at runtime, True for mypy/pyright
    from .trade import Trade

class Portfolio:
    def add(self, trade: Trade) -> None: ...
```

---

## Lazy submodule loading (advanced)

For large libraries where users need only a subset, load submodules on attribute access:

```python
# mylib/__init__.py
def __getattr__(name: str):
    if name == "analysis":
        import mylib.analysis as m
        return m
    raise AttributeError(f"module 'mylib' has no attribute {name!r}")
```

`mylib.analysis` is only imported when first accessed. Pattern used by `scipy`, `pandas`, `sklearn`.

---

## Rules of thumb

| Situation | Do this |
|---|---|
| Inside package, importing a sibling | relative import (`from .module import X`) |
| Scripts, entry points, tests | absolute import |
| Exposing a clean public API | re-export in `__init__.py` |
| Preventing `import *` pollution | define `__all__` |
| mypy complains about re-exports | `from .x import X as X` |
| Circular import | restructure → deferred import → `TYPE_CHECKING` guard |
| Heavy dep in `__init__.py` | move to submodule |

> Python 3.3+ supports **namespace packages** (no `__init__.py`) for splitting a package across directories. Niche feature — always use `__init__.py` for normal projects.
