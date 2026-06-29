# The Import System

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

## Packages and `__init__.py`

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

!!! warning "Imports in __init__.py run on every import of the package"
    `from finlib.models import Trade` triggers `finlib/models/__init__.py` to execute. Any slow import (numpy, pandas, a DB driver) placed there adds latency to every module that imports from your package. Keep `__init__.py` thin — only re-export symbols; let submodules do heavy lifting lazily.

> Python 3.3+ also supports **namespace packages** (directories without `__init__.py`) for splitting a package across multiple directories. This is a niche feature; for normal projects always use `__init__.py`.
