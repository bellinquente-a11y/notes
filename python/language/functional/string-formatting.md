# Number Formatting in Python

`f"{value:spec}"` and `format(value, "spec")` both invoke `value.__format__(spec)`. `str(x)` is equivalent to `format(x, "")`.

## Format spec mini-language

```
{value:[fill][align][sign][#][0][width][grouping][.precision][type]}
```

### Type codes

| Code | Output | Example |
|------|--------|---------|
| `f`  | Fixed-point | `f"{3.14:.2f}"` → `'3.14'` |
| `e`/`E` | Scientific | `f"{12345:.2e}"` → `'1.23e+04'` |
| `g`  | Fixed or scientific, whichever is shorter | `f"{0.00012:.3g}"` → `'0.00012'` |
| `%`  | Percent (×100, appends %) | `f"{0.173:.1%}"` → `'17.3%'` |
| `d`  | Integer decimal | `f"{42:d}"` → `'42'` |
| `b`/`x`/`X`/`o` | Binary / hex / HEX / octal | `f"{255:x}"` → `'ff'` |

### Precision

`.precision` means **decimal places** for `f`/`e`/`E`/`%`, but **significant figures** for `g` and bare floats.

```python
f"{3.14159:.2f}"   # '3.14'     — 2 decimal places
f"{3.14159:.4g}"   # '3.142'    — 4 significant figures
```

### Width and alignment

```python
f"{3.14:10.2f}"    # '      3.14'  — right-aligned in 10 chars (default for numbers)
f"{3.14:<10.2f}"   # '3.14      '  — left-aligned
f"{3.14:^10.2f}"   # '   3.14   '  — centred
f"{3.14:010.2f}"   # '0000003.14'  — zero-padded to width 10
```

### Sign

```python
f"{3.14:+.2f}"     # '+3.14'   — always show sign
f"{3.14: .2f}"     # ' 3.14'   — space for positive
```

### Thousands separator

```python
f"{1234567:,.2f}"   # '1,234,567.00'
f"{1234567:_.2f}"   # '1_234_567.00'
```

### Alternate form (`#`)

```python
f"{255:#x}"    # '0xff'
f"{10:#b}"     # '0b1010'
```

## Common patterns

```python
# Price table column, right-aligned 12 chars, comma thousands, 2 dp:
f"{price:>12,.2f}"

# Scientific with sign, 3 sig figs:
f"{-0.000123:+.3e}"     # '-1.230e-04'

# Hex with zero-padding to 8 digits:
f"{255:#010x}"          # '0x000000ff'

# Dynamic spec:
spec = ",.2f"
f"{price:{spec}}"       # nest an expression inside the spec field
```

## Custom __format__

```python
class Money:
    def __format__(self, spec):
        if spec == "short":
            return f"${self.amount:,.0f}"
        return f"${self.amount:{spec}}"

f"{Money(1234.5):.2f}"    # '$1234.50'
f"{Money(1234.5):short}"  # '$1,235'
```
