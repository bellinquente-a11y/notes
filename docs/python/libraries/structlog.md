---
tags:
  - logging
quiz: detail
---

# structlog

Third-party logging library that makes structured (key=value) logging the natural default. Every log call produces a dictionary; renderers output it as JSON, coloured console text, or anything else. Sits on top of (or beside) stdlib [`logging`](../language/stdlib/logging.md).

## Why over stdlib

- Context binding via `log.bind(key=val)` instead of `LoggerAdapter` / `extra={}`
- Fully composable processor pipeline instead of fixed Filter → Formatter chain
- Built-in `JSONRenderer` and `ConsoleRenderer`
- `capture_logs()` for zero-config test assertions

## Basic usage

```python
import structlog

log = structlog.get_logger(__name__)

log.info("order_placed", order_id=123, user="alice")
# → {"event": "order_placed", "order_id": 123, "user": "alice", ...}
```

## stdlib vs structlog: when to use which

!!! warning "Libraries must always use stdlib"
    A library that imports structlog forces consumers to install and configure it. Libraries call `logging.getLogger(__name__)` only — configuration belongs to the application.

| Situation | Use |
|---|---|
| Script / CLI tool | stdlib — `basicConfig` is one line |
| Library / reusable package | stdlib — always |
| Service / API / async app | structlog |
| Per-request context (`request_id`, `trace_id`) without `extra={}` boilerplate | structlog (`bind_contextvars`) |
| JSON output for log aggregator | structlog or stdlib + `python-json-logger` |
| Simple test assertions on log output | structlog (`capture_logs()`) |
| Need `RotatingFileHandler`, `SMTPHandler`, external `dictConfig` file | stdlib |

They also compose: structlog can sit on top of stdlib (stdlib mode), so third-party libs using `logging.getLogger` route through the same handler as your structlog calls.

## Log methods

| Method | Level | Notes |
|---|---|---|
| `log.debug(event, **kw)` | DEBUG | |
| `log.info(event, **kw)` | INFO | |
| `log.warning(event, **kw)` | WARNING | |
| `log.error(event, **kw)` | ERROR | |
| `log.critical(event, **kw)` | CRITICAL | |
| `log.exception(event, **kw)` | ERROR | captures current exception automatically — use inside `except` blocks |

`log.exception` is shorthand for `log.error(..., exc_info=True)` — no manual `sys.exc_info()` needed.

!!! tip "Level filtering is zero-cost"
    `make_filtering_bound_logger(logging.INFO)` bakes the minimum level into the class at config time. Calls below the threshold become no-ops — no dict construction, no processor chain traversal.

### Changing the level

- **Native mode** (`wrapper_class=structlog.stdlib.BoundLogger` not set) — level lives in `wrapper_class`; there's no `setLevel()`, re-run `configure()` with a new threshold to change it:

  ```python
  structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(logging.WARNING), ...)
  ```

- **stdlib mode** (`wrapper_class=structlog.stdlib.BoundLogger`) — `make_filtering_bound_logger` doesn't apply; set the level on the stdlib logger as usual: `logging.getLogger().setLevel(logging.DEBUG)`.

To suppress one specific event rather than a whole level tier, raise `structlog.DropEvent` from a processor:

```python
def drop_health_checks(logger, method, event_dict):
    if event_dict.get("event") == "health_check":
        raise structlog.DropEvent()
    return event_dict
```

## Bound logger

`log.bind(**kw)` returns a new logger with those keys permanently attached:

```python
bound = log.bind(service="pricing", symbol="BTC")
bound.info("price_fetched", price=42.0)
# every future call carries service= and symbol=
```

`log.unbind("symbol")` removes a key. `log.new(**kw)` resets all context.

## Processor pipeline

Each processor is a callable `(logger, method, event_dict) -> event_dict`. They chain in order; the last one renders to a string.

| Processor | Adds |
|-----------|------|
| `add_log_level` | `"level": "info"` |
| `TimeStamper(fmt="iso")` | `"timestamp": "2026-..."` |
| `dict_tracebacks` | exception → nested dict (JSON-safe) |
| `ExceptionRenderer()` | pretty exception in console |
| `merge_contextvars` | pull in async context (see below) |
| `ConsoleRenderer()` | coloured dev output |
| `JSONRenderer()` | JSON string for production |

## Configuration

`structlog.configure()` is called **once at the entry point** (never in library code). It sets four things:

```python
structlog.configure(
    processors=[...],       # pipeline: list of (logger, method, event_dict) → event_dict
    wrapper_class=...,      # what get_logger() returns
    logger_factory=...,     # what performs final I/O
    context_class=dict,     # storage for bound context
)
```

### Native mode (structlog owns I/O)

structlog writes to stdout directly. Use when you don't need to share a pipeline with stdlib libraries.

```python
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,   # must be first
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer(),            # dev; swap for JSONRenderer() in prod
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    logger_factory=structlog.PrintLoggerFactory(),
)
```

### stdlib mode (shared pipeline with third-party libraries)

structlog preprocesses; stdlib handlers do the routing (file, SMTP, etc.). Third-party `logging.getLogger()` calls and structlog calls share one renderer.

```python
# 1. structlog hands off to stdlib
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,  # must be last
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

# 2. stdlib renders what structlog sends
formatter = structlog.stdlib.ProcessorFormatter(
    processor=structlog.dev.ConsoleRenderer(),
    foreign_pre_chain=[                       # handles logs from stdlib loggers (httpx, etc.)
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
    ],
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)
```

!!! note "foreign_pre_chain is required in stdlib mode"
    Records arriving from stdlib loggers (e.g. httpx, sqlalchemy) have no `event` key. `foreign_pre_chain` preprocesses them before the formatter runs. Without it, those records error.

### Switching renderer via Settings

The renderer is just the last item in the `processors` list — pick it with a plain conditional on a [pydantic Settings](pydantic/pydantic-settings.md) field:

```python
shared_processors = [
    structlog.contextvars.merge_contextvars,
    structlog.processors.add_log_level,
    structlog.processors.TimeStamper(fmt="iso"),
]
renderer = (
    structlog.processors.JSONRenderer()
    if settings.environment == "production"
    else structlog.dev.ConsoleRenderer()
)
structlog.configure(processors=[*shared_processors, renderer], ...)
```

Keeping `shared_processors` common to both branches means only the *encoding* changes between environments, not the log content.

### Dev vs prod processor chain

| Processor | Dev | Prod |
|---|---|---|
| `merge_contextvars` | yes | yes |
| `add_log_level` | yes | yes |
| `TimeStamper(fmt="iso")` | yes | yes |
| `ExceptionRenderer()` | yes — pretty console | — |
| `dict_tracebacks` | — | yes — exceptions as JSON-safe dict |
| `ConsoleRenderer()` | yes | — |
| `JSONRenderer()` | — | yes |

### `wrapper_class` and `logger_factory`

| Parameter | Native mode | stdlib mode |
|---|---|---|
| `wrapper_class` | `make_filtering_bound_logger(logging.INFO)` — level baked in, zero-cost filtering | `structlog.stdlib.BoundLogger` |
| `logger_factory` | `PrintLoggerFactory()` | `stdlib.LoggerFactory()` |

## Async: `contextvars` integration

Attach context to the current async task without threading a bound logger everywhere:

```python
from structlog.contextvars import bind_contextvars, clear_contextvars

async def handle_request(request):
    clear_contextvars()
    bind_contextvars(request_id=request.headers["X-Request-ID"])
    # all log calls in this task (and subtasks) now carry request_id
    log.info("request_received")
```

Requires `merge_contextvars` as the first processor in the chain.

## Testing

See [structlog-testing.md](../tooling/testing/structlog-testing.md) — `capture_logs()`, assertion patterns, pytest fixture, comparison with `caplog`.

## Install

```bash
pip install structlog
```
