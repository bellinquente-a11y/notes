# Poetry

## What is Poetry?

Poetry is a modern Python tool for:

- dependency management
- virtual environment management
- packaging Python projects

It replaces the traditional combination of:

- `pip`
- `requirements.txt`
- `virtualenv`
- `setup.py`

with a single workflow centered around:

- `pyproject.toml` (requirements)
- `poetry.lock` (what's installed)

It provides a unified workflow for managing Python projects.

---

## Why use Poetry?

Main advantages:

- reproducible environments
- deterministic dependency versions
- automatic virtual environments
- cleaner project structure
- easier collaboration

Poetry helps avoid:
> "works on my machine" problems.

---

## Installation (macOS)

Install Poetry:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

---

## Project scaffold

```bash
poetry new finlib
cd finlib
poetry add pydantic
poetry add --group dev mypy ruff black pytest
```

```text 
finlib/
|-- pyproject.toml
|-- src/finlib/__init__.py
|-- tests/
```

## Usage

Add to `pyproject.toml` the following

``` text
[tool.mypy]
python_version = '3.12'
strict = true
warn_return_any = true
```

```bash
poetry run mypy src/ --strict
```