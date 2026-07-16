---
tags:
  - testing
quiz: detail
---

# Python — Float Comparison

## Why `==` fails

Floats are IEEE 754 binary — many decimals can't be represented exactly:

```python
0.1 + 0.2 == 0.3   # False
```

## `math.isclose` — standard library

```python
import math
math.isclose(a, b, rel_tol=1e-9, abs_tol=0.0)
# True if |a-b| <= max(rel_tol * max(|a|, |b|), abs_tol)
```

- `rel_tol` scales with magnitude — good for non-zero values
- `abs_tol` is a fixed floor — **required near zero** (relative tolerance of ~0 is ~0)

```python
math.isclose(1000.0, 1000.001, rel_tol=1e-3)  # True
math.isclose(0.0, 1e-10, abs_tol=1e-9)        # True
math.isclose(0.0, 1e-10)                       # False — rel_tol alone fails near zero
```

!!! warning "Near-zero comparisons need abs_tol"
    `rel_tol * max(|a|, |b|)` collapses to nearly zero when both values are tiny, so `isclose(0.0, 1e-15)` returns `False` with only the default `rel_tol`. Always pass `abs_tol` when either value can be near zero.

## pytest

```python
assert 0.1 + 0.2 == pytest.approx(0.3)              # scalar
assert [0.1, 0.2] == pytest.approx([0.1, 0.2])      # sequence
assert {'v': 0.1} == pytest.approx({'v': 0.1})      # dict
# defaults: rel=1e-6, abs=1e-12; override with pytest.approx(x, rel=1e-3)
```

## NumPy arrays

```python
np.isclose(a, b, rtol=1e-5, atol=1e-8)   # element-wise → bool array
np.allclose(a, b, rtol=1e-5, atol=1e-8)  # True if all close
# formula: |a-b| <= atol + rtol*|b|
```

## Quick reference

| Context | Tool |
|---------|------|
| General code | `math.isclose(a, b, rel_tol=…, abs_tol=…)` |
| Simple fixed scale | `abs(a - b) < tol` |
| Tests | `pytest.approx` |
| Arrays | `np.isclose` / `np.allclose` |
