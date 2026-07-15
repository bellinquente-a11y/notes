# Notes

Learning notes and references across software engineering, ML, and AI topics.

| Directory | Description |
|-----------|-------------|
| [data/](docs/data/) | NumPy and Pandas — arrays, vectorised operations, DataFrames |
| [dsa/](docs/dsa/) | Data structures and algorithms: complexity, queues, trees, graphs |
| [finance/](docs/finance/) | Trading, exchanges, and market data APIs |
| [git/](docs/git/) | Git workflows, commands, and CI/CD |
| [python/](docs/python/) | Python language, tooling, and type system |
| [tools/](docs/tools/) | Language-agnostic tools and notation |

## Structure

notes/\
├── dsa/\
│   ├── [complexity.md](docs/dsa/complexity.md)\
│   ├── [graphs.md](docs/dsa/graphs.md)\
│   ├── [queues.md](docs/dsa/queues.md)\
│   └── [trees.md](docs/dsa/trees.md)\
├── data/\
│   ├── numpy/\
│   │   ├── [broadcasting.md](docs/data/numpy/broadcasting.md)\
│   │   └── [dtypes.md](docs/data/numpy/dtypes.md)\
│   └── pandas/\
│       ├── [chaining.md](docs/data/pandas/chaining.md)\
│       ├── [datetimes.md](docs/data/pandas/datetimes.md)\
│       ├── [display.md](docs/data/pandas/display.md)\
│       ├── [dtypes.md](docs/data/pandas/dtypes.md)\
│       ├── [indexing.md](docs/data/pandas/indexing.md)\
│       └── [iteration.md](docs/data/pandas/iteration.md)\
├── finance/\
│   ├── [binance.md](docs/finance/binance.md)\
│   └── [market-data-apis.md](docs/finance/market-data-apis.md)\
├── git/\
│   ├── [git.md](docs/git/git.md)\
│   ├── [github-actions.md](docs/git/github-actions.md)\
│   └── [tags-releases.md](docs/git/tags-releases.md)\
├── python/\
│   ├── language/\
│   │   ├── concurrency/\
│   │   │   ├── [asyncio.md](docs/python/language/concurrency/asyncio.md)\
│   │   │   ├── [concurrency.md](docs/python/language/concurrency/concurrency.md)\
│   │   │   └── [threading.md](docs/python/language/concurrency/threading.md)\
│   │   ├── functional/\
│   │   │   ├── itertools/\
│   │   │   │   ├── [accumulate.md](docs/python/language/functional/itertools/accumulate.md)\
│   │   │   │   ├── [core.md](docs/python/language/functional/itertools/core.md)\
│   │   │   │   ├── [filtering.md](docs/python/language/functional/itertools/filtering.md)\
│   │   │   │   └── [groupby.md](docs/python/language/functional/itertools/groupby.md)\
│   │   │   ├── [comprehensions.md](docs/python/language/functional/comprehensions.md)\
│   │   │   ├── [functools.md](docs/python/language/functional/functools.md)\
│   │   │   ├── [iterators-generators.md](docs/python/language/functional/iterators-generators.md)\
│   │   │   ├── [lazy-evaluation.md](docs/python/language/functional/lazy-evaluation.md)\
│   │   │   ├── [operator.md](docs/python/language/functional/operator.md)\
│   │   │   ├── [string-formatting.md](docs/python/language/functional/string-formatting.md)\
│   │   │   └── [unpacking.md](docs/python/language/functional/unpacking.md)\
│   │   ├── objects/\
│   │   │   ├── [data-model.md](docs/python/language/objects/data-model.md)\
│   │   │   ├── [exceptions.md](docs/python/language/objects/exceptions.md)\
│   │   │   ├── [hash.md](docs/python/language/objects/hash.md)\
│   │   │   ├── [mutation.md](docs/python/language/objects/mutation.md)\
│   │   │   ├── [numbers.md](docs/python/language/objects/numbers.md)\
│   │   │   ├── [oop.md](docs/python/language/objects/oop.md)\
│   │   │   ├── [repository-di.md](docs/python/language/objects/repository-di.md)\
│   │   │   ├── [sets.md](docs/python/language/objects/sets.md)\
│   │   │   ├── [structural-typing.md](docs/python/language/objects/structural-typing.md)\
│   │   │   ├── [subscriptable.md](docs/python/language/objects/subscriptable.md)\
│   │   │   ├── [typing.md](docs/python/language/objects/typing.md)\
│   │   │   └── [warnings.md](docs/python/language/objects/warnings.md)\
│   │   └── runtime/\
│   │       ├── [cli.md](docs/python/language/runtime/cli.md)\
│   │       ├── [context-managers.md](docs/python/language/runtime/context-managers.md)\
│   │       ├── [datetime.md](docs/python/language/runtime/datetime.md)\
│   │       ├── [entrypoint.md](docs/python/language/runtime/entrypoint.md)\
│   │       ├── [import-system.md](docs/python/language/runtime/import-system.md)\
│   │       ├── [logging.md](docs/python/language/runtime/logging.md)\
│   │       ├── [match.md](docs/python/language/runtime/match.md)\
│   │       ├── [pathlib.md](docs/python/language/runtime/pathlib.md)\
│   │       ├── [scopes.md](docs/python/language/runtime/scopes.md)\
│   │       └── [subprocess.md](docs/python/language/runtime/subprocess.md)\
│   └── tooling/\
│       ├── pydantic/\
│       │   ├── [pydantic.md](docs/python/tooling/pydantic/pydantic.md)\
│       │   ├── [pydantic-settings.md](docs/python/tooling/pydantic/pydantic-settings.md)\
│       │   └── [pydantic-validators.md](docs/python/tooling/pydantic/pydantic-validators.md)\
│       ├── testing/\
│       │   ├── [hypothesis.md](docs/python/tooling/testing/hypothesis.md)\
│       │   ├── [mocking.md](docs/python/tooling/testing/mocking.md)\
│       │   ├── [pytest.md](docs/python/tooling/testing/pytest.md)\
│       │   ├── [testing-patterns.md](docs/python/tooling/testing/testing-patterns.md)\
│       │   └── [testing-strategy.md](docs/python/tooling/testing/testing-strategy.md)\
│       ├── [aiohttp.md](docs/python/tooling/aiohttp.md)\
│       ├── [fastapi.md](docs/python/tooling/fastapi.md)\
│       ├── [jsonl.md](docs/python/tooling/jsonl.md)\
│       ├── [mypy.md](docs/python/tooling/mypy.md)\
│       ├── [poetry.md](docs/python/tooling/poetry.md)\
│       ├── [pyenv.md](docs/python/tooling/pyenv.md)\
│       ├── [ruff.md](docs/python/tooling/ruff.md)\
│       ├── [structlog.md](docs/python/tooling/structlog.md)\
│       └── [terminal-tables.md](docs/python/tooling/terminal-tables.md)\
└── tools/\
    ├── [env-vars.md](docs/tools/env-vars.md)\
    ├── [markdown.md](docs/tools/markdown.md)\
    ├── [mermaid.md](docs/tools/mermaid.md)\
    └── [zsh.md](docs/tools/zsh.md)
