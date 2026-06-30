# pathlib.Path

Object-oriented filesystem paths. Replaces `os.path` — use it in all new code.

```python
from pathlib import Path

p = Path("data") / "prices" / "aapl.csv"
p.parent    # Path("data/prices")
p.name      # "aapl.csv"
p.stem      # "aapl"
p.suffix    # ".csv"
```

## Construction

```python
Path("relative/path")
Path("/absolute/path")
Path.home()              # ~
Path.cwd()               # current working directory
Path(__file__).parent    # directory of the current script — use this, not os.path.dirname
```

## Reading and writing

```python
p.read_text(encoding="utf-8")            # whole file as str
p.write_text("content\n", encoding="utf-8")
p.read_bytes() / p.write_bytes(b"...")

with p.open("a", encoding="utf-8") as f:  # for append or line-by-line
    f.write("line\n")
```

## Existence and creation

```python
p.exists()    # True/False
p.is_file()
p.is_dir()

p.mkdir(parents=True, exist_ok=True)   # mkdir -p
p.unlink(missing_ok=True)              # delete file
```

## Globbing

```python
list(Path("docs").iterdir())          # all entries, one level
list(Path("docs").rglob("*.md"))      # recursive
```

## os.path equivalents

| os.path | pathlib |
|---|---|
| `os.path.join(a, b)` | `Path(a) / b` |
| `os.path.exists(p)` | `p.exists()` |
| `os.path.dirname(p)` | `p.parent` |
| `os.path.basename(p)` | `p.name` |

!!! tip "Script-relative paths"
    `Path(__file__).parent / "data"` always resolves relative to the script, regardless of the working directory when you invoke it.