# Testing

Tests are executable claims about behaviour. They exist to enable *change* safely — refactors, upgrades, onboarding — not to reach a coverage number.

## The test pyramid

```
         ▲  E2E / smoke tests     (few, slow, high confidence)
        ▲▲▲ Integration tests     (moderate — real deps wired together)
       ▲▲▲▲▲ Unit tests           (many, fast, pinpoint failures)
```

Most tests should be units. Integration tests catch what units can't (schema mismatches, transaction semantics). E2E tests cover only the critical path.

## What to test

Test **behaviour, not implementation**. The rule of thumb: risk × value.

- **Test heavily**: pure functions, validation/parsing, error paths, business rules
- **Skip**: trivial getters, third-party library internals, UI layout

> "Test the things that scare you." — Kent Beck

## AAA pattern

Every test has three acts:

```python
def test_trade_rejects_negative_quantity():
    # Arrange
    data = {"symbol": "BHP", "quantity": -10, "price": 45.5, "side": "BUY"}

    # Act + Assert
    with pytest.raises(ValidationError):
        Trade(**data)
```

One test, one behaviour. If a test has 10 assertions, split it into 10 tests.

## Fakes, stubs, mocks

| Term | What it does | When to use |
|------|-------------|-------------|
| **Stub** | Returns a canned value | Drive a code path |
| **Mock** | Stub that records calls | Assert a side effect was triggered |
| **Fake** | Lightweight real implementation (e.g. in-memory dict) | When a stub is too thin |

Don't mock what you don't own — mocking third-party library internals lets the mock drift from reality. Mock at your own boundary.

```python
from unittest.mock import MagicMock, patch

def test_sends_alert_on_breach():
    with patch("myapp.notifier.send_email") as mock_send:
        check_risk_limit(position=1_000_000)
        mock_send.assert_called_once()
```

## How much is enough?

80–90% line coverage is a reasonable floor; beyond that, returns diminish fast. Better questions:

- Do the scary parts (validation, error handling, business rules) have tests?
- Would a new reader understand expected behaviour from the test suite?
- Does a real bug cause a test to fail? (Use `mutmut` for mutation testing.)

## TDD: Red → Green → Refactor

Write the failing test first, then write the minimal code to pass it, then clean up.

```
Red (failing test) → Green (passes) → Refactor (clean without breaking)
```

Most useful when fixing bugs (write a test that reproduces the bug, then fix it) and when designing new APIs.

## Useful pytest ecosystem

| Package | Role |
|---------|------|
| [`pytest`](pytest.md) | Runner, discovery, assertions |
| `pytest-cov` | Coverage (`--cov=myapp --cov-report=term-missing`) |
| `pytest-mock` | Cleaner `mocker` fixture |
| `hypothesis` | Property-based testing — auto-generates edge cases |
| `factory_boy` | Generates fixture data for models |
| `mutmut` | Mutation testing to verify test quality |

### hypothesis example

```python
from hypothesis import given, strategies as st

@given(st.integers(max_value=-1))
def test_rejects_any_negative_quantity(qty):
    with pytest.raises(ValidationError):
        Trade(symbol="BHP", quantity=qty, price=1.0, side="BUY")
```

## Testing functions with external dependencies

The problem: a function that opens a CSV or queries a database makes tests slow, fragile, and non-deterministic. The solution is always the same — **create a seam** where the test can swap in a substitute.

### Root cause: hidden coupling

```python
# BAD — dependency is invisible from the outside
def load_prices(symbol: str) -> list[float]:
    with open("/data/prices.csv") as f:   # impossible to swap in tests
        ...

# GOOD — caller decides what file to use (dependency injection)
def load_prices(symbol: str, filepath: str | Path) -> list[float]:
    with open(filepath) as f:
        ...
```

Receive dependencies as arguments rather than creating them internally.

### Strategy 1 — real file via `tmp_path` (best for file I/O)

pytest's built-in `tmp_path` fixture provides a fresh temp directory per test. Deleted automatically after the test.

```python
def test_load_prices(tmp_path):
    csv_file = tmp_path / "prices.csv"
    csv_file.write_text("symbol,price\nBHP,45.5\nBHP,46.0\n")

    result = load_prices("BHP", filepath=csv_file)

    assert result == [45.5, 46.0]
```

### Strategy 2 — in-memory file object (`io.StringIO`)

Accept `TextIO` (any file-like) instead of a path string. Fastest option; no filesystem touched.

```python
import io, csv

def load_prices(symbol: str, file) -> list[float]:
    return [float(r["price"]) for r in csv.DictReader(file) if r["symbol"] == symbol]

def test_load_prices():
    assert load_prices("BHP", io.StringIO("symbol,price\nBHP,45.5\n")) == [45.5]
```

### Strategy 3 — in-memory database (SQLite `:memory:`)

A real SQL engine, zero infrastructure. Best for unit-testing SQL logic.

```python
import sqlite3

def get_open_trades(conn) -> list[dict]:
    conn.row_factory = sqlite3.Row
    return [dict(r) for r in conn.execute("SELECT * FROM trades WHERE status='OPEN'")]

def test_returns_only_open_trades():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE trades (id INT, status TEXT)")
    conn.execute("INSERT INTO trades VALUES (1, 'OPEN'), (2, 'CLOSED')")

    assert len(get_open_trades(conn)) == 1
```

Limitation: SQLite dialect differs from Postgres/MySQL. Use Testcontainers for full dialect fidelity.

### Strategy 4 — transaction rollback (integration tests against a real DB)

Wrap each test in a transaction rolled back on teardown. State never leaks between tests.

```python
@pytest.fixture
def db_conn():
    conn = psycopg2.connect(dsn="postgresql://localhost/testdb")
    conn.autocommit = False
    yield conn
    conn.rollback()
    conn.close()
```

### Strategy 5 — `patch()` (last resort)

When you can't inject the dependency. Ties the test to implementation details — fragile under refactors.

```python
from unittest.mock import mock_open, patch

def test_load_prices_mocked():
    with patch("builtins.open", mock_open(read_data="symbol,price\nBHP,45.5\n")):
        assert load_prices("BHP", "/any/path") == [45.5]
```

### Decision guide

| Situation | Strategy |
|-----------|----------|
| File I/O, testing parsing logic | `tmp_path` (real file) |
| File I/O, parsing logic is trivial | `io.StringIO` |
| SQL, SQLite dialect is fine | `sqlite3.connect(":memory:")` |
| SQL, need exact dialect | Testcontainers or rollback fixture |
| Can't inject the dep | `patch()` |

## Related notes

- [`pytest.md`](pytest.md) — command quick-reference
- [`pydantic.md`](pydantic.md) — validation logic concentrates at model boundaries, ideal test target
- [`mypy.md`](mypy.md) — static types + dynamic tests are complementary, not redundant