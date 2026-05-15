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
  