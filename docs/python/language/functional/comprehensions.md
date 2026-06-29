# Comprehensions

Comprehensions build a new collection by mapping and/or filtering an iterable in a single expression. Use them when the intent is *transformation or filtering*; use a loop when the body has side effects, accumulates multiple things, or is too complex to read in one line.

## List comprehensions

```python
squares = [x**2 for x in range(10)]
```

**Filter (if at the end)** — excludes items:
```python
positives = [x for x in data if x > 0]
```

**Ternary (if/else in the expression)** — transforms all items:
```python
clamped = [x if x > 0 else 0 for x in data]
```

Mixing both is at the readability limit:
```python
result = [x if x > 0 else 0 for x in data if x is not None]
```

## Nested comprehensions

Two `for` clauses, read left-to-right (outer loop first):

```python
# Flatten a 2D list
flat = [x for row in matrix for x in row]

# Cartesian product
pairs = [(x, y) for x in [1, 2] for y in ['a', 'b']]
```

One level of nesting is usually fine; two or more levels — use a loop.

A nested *comprehension of comprehensions* produces a 2D list (different from flattening):
```python
transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
# but prefer: list(zip(*matrix))
```

## Dict comprehensions

```python
word_lengths = {w: len(w) for w in words}          # from iterable
uppercased   = {k: v.upper() for k, v in d.items()} # transform dict
active       = {k: v for k, v in d.items() if v['active']}  # filter dict
inverted     = {v: k for k, v in d.items()}          # invert (unique values only)
```

Use a loop when the value needs multiple steps or key collisions need explicit handling.

## Set comprehensions

```python
unique_lengths = {len(w) for w in words}
initials       = {name[0].upper() for name in names if name}
```

Identical to list comprehensions but deduplicate automatically. Prefer over `set(... for ...)` for consistency with dict syntax.

## When to use a loop instead

| Situation | Reason |
|---|---|
| Side effects (print, write, mutate) | Comprehensions imply no side effects |
| Multiple accumulations | One comprehension = one output |
| Multi-step value computation | Can't use intermediate variables |
| Per-item error handling | `try/except` can't go inside |
| > 2 `for` clauses | Loop order becomes confusing |
| `break` / `continue` flow control | Not expressible in a comprehension |

## Performance note

List comprehensions are faster than `for` + `.append()` (the append method is resolved once, not per iteration), but readability is the primary reason to prefer them.

!!! tip "Use a generator expression when you only need one pass"
    `[x**2 for x in range(1_000_000)]` allocates ~8 MB immediately. `sum(x**2 for x in range(1_000_000))` uses O(1) memory — the generator feeds values one at a time into `sum`, which never builds the list. Use `[...]` only when you need the list itself (indexing, multiple passes, `len`).

For single-pass consumption, use a **generator expression** instead to avoid materialising the full list:
```python
total = sum(x**2 for x in range(1_000_000))
```

See [iterators-generators.md](iterators-generators.md) for more on generators.