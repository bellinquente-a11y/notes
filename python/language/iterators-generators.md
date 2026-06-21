# Iterators and Generators

Iteration is fundamental in data processing, especially to fetch data **lazily** (one at a time as needed; the opposite is **eagerly**).

## Iterables and Iterators

- **Iterable**: object that implements `__iter__`, which returns an **iterator**; if not available it falls back to `__getitem__`.
- **Iterator**: object that defines `__next__` (returning a value or `raise StopIteration`) and `__iter__` (returning self).
- Iterable objects used in:
  - `for` loops
  - list, dict and set [comprehensions](comprehensions.md) (`[2*s for s in x]`)
  - unpacking assignments (`*x`)

## Generators

- A **generator function** is a function with the `yield` keyword (`return` not needed).
- It returns a **generator** object, which is an iterator built by the compiler.
- Alternatively, use a **generator expression**: `(2*s for s in x)`.
- Generators can be used to implement iterators.
- `yield from` delegates to a subgenerator.
- Generators are a secret weapon for large datasets.

```python
def evens(n):
    for i in range(n):
        if i % 2 == 0:
            yield i

list(evens(10))  # [0, 2, 4, 6, 8]
```

## Generators in the Standard Library

Avoid reinventing the wheel — use `itertools`.

- **Filtering**: `compress`, `dropwhile`, `filter`, `islice`, `takewhile`
- **Mapping**: `accumulate`, `enumerate`, `map`
- **Merging**: `chain`, `chain.from_iterable`, `product`, `zip`, `zip_longest`
- **Multiple outputs**: `combinations`, `count`, `pairwise`, `cycle`, `permutations`, `repeat`
- **Rearranging**: `[groupby](itertools-groupby.md)`, `reversed`, `tee`
- **Reducing**: `all`, `any`, `max`, `min`, `reduce`, `sum`

