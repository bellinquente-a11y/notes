# Notes

Learning notes and references across software engineering, ML, and AI topics.

| Directory | Description |
|-----------|-------------|
| [data/](docs/data/) | NumPy and Pandas — arrays, vectorised operations, DataFrames |
| [dsa/](docs/dsa/) | Data structures and algorithms: complexity, queues, trees, graphs |
| [finance/](docs/finance/) | Trading, exchanges, and market data APIs |
| [git/](docs/git/) | Git workflows, commands, and CI/CD |
| [python/](docs/python/) | Python language, libraries, and tooling |
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
│       ├── [chaining-catalog.md](docs/data/pandas/chaining-catalog.md)\
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
│   │   │   └── [warnings.md](docs/python/language/objects/warnings.md)\
│   │   ├── runtime/\
│   │   │   ├── [context-managers.md](docs/python/language/runtime/context-managers.md)\
│   │   │   ├── [entrypoint.md](docs/python/language/runtime/entrypoint.md)\
│   │   │   ├── [import-system.md](docs/python/language/runtime/import-system.md)\
│   │   │   ├── [match.md](docs/python/language/runtime/match.md)\
│   │   │   └── [scopes.md](docs/python/language/runtime/scopes.md)\
│   │   ├── stdlib/\
│   │   │   ├── [cli.md](docs/python/language/stdlib/cli.md)\
│   │   │   ├── [datetime.md](docs/python/language/stdlib/datetime.md)\
│   │   │   ├── [file-io.md](docs/python/language/stdlib/file-io.md)\
│   │   │   ├── [logging.md](docs/python/language/stdlib/logging.md)\
│   │   │   ├── [pathlib.md](docs/python/language/stdlib/pathlib.md)\
│   │   │   ├── [string-formatting.md](docs/python/language/stdlib/string-formatting.md)\
│   │   │   └── [subprocess.md](docs/python/language/stdlib/subprocess.md)\
│   │   └── typing/\
│   │       ├── [structural-typing.md](docs/python/language/typing/structural-typing.md)\
│   │       ├── [subscriptable.md](docs/python/language/typing/subscriptable.md)\
│   │       └── [typing.md](docs/python/language/typing/typing.md)\
│   ├── libraries/\
│   │   ├── pydantic/\
│   │   │   ├── [pydantic.md](docs/python/libraries/pydantic/pydantic.md)\
│   │   │   ├── [pydantic-settings.md](docs/python/libraries/pydantic/pydantic-settings.md)\
│   │   │   └── [pydantic-validators.md](docs/python/libraries/pydantic/pydantic-validators.md)\
│   │   ├── [aiohttp.md](docs/python/libraries/aiohttp.md)\
│   │   ├── [fastapi.md](docs/python/libraries/fastapi.md)\
│   │   ├── [jsonl.md](docs/python/libraries/jsonl.md)\
│   │   ├── [structlog.md](docs/python/libraries/structlog.md)\
│   │   └── [terminal-tables.md](docs/python/libraries/terminal-tables.md)\
│   └── tooling/\
│       ├── testing/\
│       │   ├── [contract-tests.md](docs/python/tooling/testing/contract-tests.md)\
│       │   ├── [fixtures.md](docs/python/tooling/testing/fixtures.md)\
│       │   ├── [hypothesis.md](docs/python/tooling/testing/hypothesis.md)\
│       │   ├── [mocking-network.md](docs/python/tooling/testing/mocking-network.md)\
│       │   ├── [mocking.md](docs/python/tooling/testing/mocking.md)\
│       │   ├── [pytest.md](docs/python/tooling/testing/pytest.md)\
│       │   ├── [structlog-testing.md](docs/python/tooling/testing/structlog-testing.md)\
│       │   ├── [testing-patterns.md](docs/python/tooling/testing/testing-patterns.md)\
│       │   └── [testing-strategy.md](docs/python/tooling/testing/testing-strategy.md)\
│       ├── [mypy.md](docs/python/tooling/mypy.md)\
│       ├── [poetry.md](docs/python/tooling/poetry.md)\
│       ├── [pyenv.md](docs/python/tooling/pyenv.md)\
│       └── [ruff.md](docs/python/tooling/ruff.md)\
└── tools/\
    ├── [env-vars.md](docs/tools/env-vars.md)\
    ├── [markdown.md](docs/tools/markdown.md)\
    ├── [mermaid.md](docs/tools/mermaid.md)\
    └── [zsh.md](docs/tools/zsh.md)
