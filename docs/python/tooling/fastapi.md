# FastAPI — Dependency Injection

FastAPI's DI system does in two phases what you do manually in `Service.__init__(repo=...)` — but it handles request-scoped resources that can't exist at startup.

## Two phases

| Phase | When | What happens |
|-------|------|--------------|
| Decoration | `@app.get(...)` executes | `inspect.signature()` → `get_dependant()` → tree of `Dependant` nodes stored on the route |
| Request | HTTP arrives | `solve_dependencies()` walks tree, calls factories, caches results, injects values |

The expensive reflection (`inspect`) runs once at startup. Per-request work is just function calls.

## `get_dependant()` — inspection at decoration time

```python
# routing.py — called inside APIRoute.__init__()
self.dependant = get_dependant(path=self.path_format, call=self.endpoint)
```

For each parameter in the endpoint signature, `analyze_param()` classifies it:

- default is `Depends(f)` → recurse into `get_dependant(call=f)` and append as sub-dependency
- default is `Query(...)` / annotation is `int` → path/query/body field

`Depends` itself is a frozen dataclass — it stores the callable, not the result:

```python
@dataclass(frozen=True)
class Depends:
    dependency: Callable[..., Any] | None = None
    use_cache: bool = True
```

The result is a tree of `Dependant` objects, built once, reused on every request.

## `solve_dependencies()` — execution at request time

```python
async def solve_dependencies(*, request, dependant, dependency_cache, ...):
    for sub_dependant in dependant.dependencies:
        call = sub_dependant.call
        if use_cache and (call, ...) in dependency_cache:
            solved = dependency_cache[(call, ...)]
        else:
            inner = await solve_dependencies(request, sub_dependant, ...)
            solved = await call(**inner.values)   # ← factory called here
            dependency_cache[(call, ...)] = solved
        values[sub_dependant.name] = solved
```

Leaves resolved first (topological order). Generator dependencies (`yield`) tie into an `AsyncExitStack` for post-response cleanup.

## What `Depends()` adds over manual injection

### 1 — Request-scoped resources

Manual injection wires at startup. `Depends` wires at request time, so factories can consume live request data:

```python
def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session          # session closed after response

def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> User:
    token = request.headers["Authorization"]   # only exists at request time
    return db.query(User).filter(...).first()
```

This isn't automating what you'd do manually — it's enabling something you *can't* do at startup.

### 2 — Automatic deduplication

With `use_cache=True` (default), each factory is called at most once per request, regardless of how many route parameters or sub-dependencies declare it. If both `get_trading_service` and `get_current_user` depend on `get_db`, it's called once and the session is shared. Manual factories require threading the shared instance by hand.

!!! tip "Depends() is a deferred call token"
    `Depends(f)` means "call `f` at request time and inject its return value here." The *how* (signature analysis, sub-dependency graph) is resolved once at decoration time; the *call* happens per request.

!!! note "Manual DI vs framework DI"
    Manual DI (`__init__` injection) is startup injection — right for stateless, long-lived objects like service classes. `Depends` is request injection — right for anything that needs live request state or must be scoped to a single request lifecycle.

## Related

- [repository-di.md](../language/objects/repository-di.md) — manual DI with Protocol + `__init__` injection
- [pydantic/pydantic.md](pydantic/pydantic.md) — Pydantic validates the resolved values from path/query params
