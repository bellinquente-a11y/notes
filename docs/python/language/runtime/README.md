# Python — Language / Runtime

| File | Type | Description |
|------|------|-------------|
| [asyncio.md](asyncio.md) | note | async def, await, asyncio.run(), gather(), create_task() — core mechanics |
| [cli.md](cli.md) | ref | Running Python from the terminal: `-c`, `-m`, scripts |
| [concurrency.md](concurrency.md) | note | GIL, threading, multiprocessing, asyncio — overview and decision guide |
| [context-managers.md](context-managers.md) | note | `with` statement, class-based and `@contextmanager` |
| [datetime.md](datetime.md) | note | datetime from strings and integer timestamps; timezone awareness; strptime, fromisoformat, fromtimestamp |
| [entrypoint.md](entrypoint.md) | note | `__name__`, `if __name__ == "__main__"` guard, `__main__.py`, async `main` with `asyncio.run()` |
| [import-system.md](import-system.md) | note | Modules, packages, `__init__.py`, `sys.path`, public API |
| [logging.md](logging.md) | note | stdlib logging: pipeline, levels, dictConfig, best practices, structured logging |
| [pathlib.md](pathlib.md) | ref | pathlib.Path: object-oriented filesystem paths, replacing os.path |
| [scopes.md](scopes.md) | note | LEGB rule, local/global/nonlocal, closures, late-binding gotcha, class scope |
| [threading.md](threading.md) | note | `ThreadPoolExecutor`, `Future` mechanics, `as_completed`, exception handling, shared state |