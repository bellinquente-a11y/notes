---
quiz: core
---

# Iterators and Generators

Iteration is fundamental in data processing, especially to fetch data **lazily** (one at a time as needed; the opposite is **eagerly**). See [lazy-evaluation.md](lazy-evaluation.md) for the full tradeoff analysis.

## Iterables and Iterators

- **Iterable**: object that implements `__iter__`, which returns an **iterator**; if not available it falls back to `__getitem__`.
- **Iterator**: object that defines `__next__` (returning a value or `raise StopIteration`) and `__iter__` (returning self).
- Iterable objects used in:
  - `for` loops
  - list, dict and set [comprehensions](comprehensions.md) (`[2*s for s in x]`)
  - unpacking assignments (`*x`) — see [unpacking.md](unpacking.md) for the full `*`/`**` operator reference

## Generators

!!! note "A generator is an iterator you write with yield instead of __next__"
    A generator function suspends at each `yield`, preserving local state between calls. This lets you express complex iteration logic as sequential code without building a full collection in memory. The compiler converts the function body into a state machine automatically.

- A **generator function** is a function with the `yield` keyword (`return` not needed).
- It returns a **generator** object, which is an iterator built by the compiler.
- Alternatively, use a **generator expression**: `(2*s for s in x)`.
- Generators can be used to implement iterators.
- Generators are a secret weapon for large datasets.

```python
def evens(n):
    for i in range(n):
        if i % 2 == 0:
            yield i

list(evens(10))  # [0, 2, 4, 6, 8]
```

## `yield from`

A generator object supports four operations, not just "produce a value": `next()`/`send(value)`, `throw(exc)`, `close()`, and termination (`StopIteration`, optionally carrying a `return value`). `yield from sub()` **delegates** to a subgenerator across all four; a plain `for x in sub(): yield x` only covers the first.

```python
def sub():
    total = 0
    while True:
        x = yield total
        if x is None:
            return "done"
        total += x

def outer():
    result = yield from sub()   # forwards send()/throw()/close(), captures return value
    print(result)

g = outer()
next(g)           # prime
g.send(5)         # reaches sub() directly -> 5
```

!!! note "`yield from` vs. a `for` loop"
    A `for` loop re-yields values but silently drops anything sent via `.send()`, doesn't propagate `.throw()`, and doesn't run the subgenerator's `finally` block deterministically on `.close()`. Use `yield from` whenever the subgenerator is a real generator you want to treat as inlined — not just an iterable to drain.

- Common uses: flattening nested structures (`yield from flatten(item)` recursively) and splitting one large generator into composable helper generators.
- `itertools.chain` looks similar for pure iteration but is a plain iterator — no send/throw/close forwarding.
- Historically, pre-3.5 asyncio coroutines (`@asyncio.coroutine` + `yield from`) used this exact delegation protocol to suspend/resume against the event loop; [`async`/`await`](../concurrency/asyncio.md) is the typed successor to the same mechanism.
- Since Python 3.7 ([PEP 479](https://peps.python.org/pep-0479/)), a `StopIteration` raised inside a generator body is converted to `RuntimeError`, closing a footgun where it used to silently truncate an enclosing `yield from` chain.

## Generators in the Standard Library

Avoid reinventing the wheel — use `itertools`.

- **Filtering**: `compress`, `dropwhile`, `filter`, `islice`, `takewhile`
- **Mapping**: `accumulate`, `enumerate`, `map`
- **Merging**: `chain`, `chain.from_iterable`, `product`, `zip`, `zip_longest`
- **Multiple outputs**: `combinations`, `count`, `pairwise`, `cycle`, `permutations`, `repeat`
- **Rearranging**: `[groupby](itertools/groupby.md)`, `reversed`, `tee`
- **Reducing**: `all`, `any`, `max`, `min`, `reduce`, `sum`

