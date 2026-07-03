# Python CLI

## Running Python from the shell

```bash
python script.py          # run a file
python -c 'import sys'   # run a string
python -m module          # run a module (no .py extension)
```

---

## sys.argv — raw argument list

`sys.argv` is a plain list of strings: `argv[0]` is the script name, the rest are tokens passed by the shell.

```python
# python script.py foo --bar 42
import sys
print(sys.argv)  # ['script.py', 'foo', '--bar', '42']
```

Everything is a string; no type conversion, no `--help`, no error messages. Fine for zero/one positional args; use `argparse` for anything more.

---

## argparse — structured argument parsing

```python
import argparse

parser = argparse.ArgumentParser(description="What this script does")

# positional — required, no -- prefix
parser.add_argument("filename", help="input file")

# optional flags
parser.add_argument("--count", type=int, default=10, help="number of items")
parser.add_argument("--verbose", action="store_true")

args = parser.parse_args()  # reads sys.argv[1:] by default
# args.filename → str, args.count → int, args.verbose → bool
```

`--help` is generated automatically. Bad input prints an error and exits.

### Positional vs optional

| | Positional | Optional flag |
|---|---|---|
| `add_argument` syntax | `"name"` | `"--name"` / `"-n"` |
| Required? | yes | no (use `required=True` to force) |
| Access | `args.name` | `args.name` |

### Key `add_argument` parameters

| Parameter | Effect |
|-----------|--------|
| `type` | convert string: `int`, `float`, `Path`, any callable |
| `default` | value when flag is absent (`None` if omitted) |
| `action="store_true"` | boolean switch: present → `True` |
| `action="append"` | `--tag a --tag b` → `["a", "b"]` |
| `nargs` | `"?"` 0–1, `"*"` any, `"+"` one+, `N` exactly N |
| `choices` | restrict values: `choices=["json", "csv"]` |

Dashes in long flags become underscores in the namespace: `--output-file` → `args.output_file`.

### Short and long flags

```python
parser.add_argument("-v", "--verbose", action="store_true")
# -v and --verbose both set args.verbose
```

### Subcommands

```python
sub = parser.add_subparsers(dest="command")

push = sub.add_parser("push")
push.add_argument("--force", action="store_true")

args = parser.parse_args()
if args.command == "push":
    ...
```

### Mutually exclusive flags

```python
group = parser.add_mutually_exclusive_group()
group.add_argument("--quiet", action="store_true")
group.add_argument("--verbose", action="store_true")
```

### Testing

Pass a list directly so tests don't touch real `sys.argv`:

```python
args = parser.parse_args(["file.txt", "--count", "5"])
```

!!! tip "Extract logic from parsing"
    Keep `parse_args()` in `main()`; pass the namespace into functions. Then unit-test those functions without invoking the parser at all.

!!! warning "Error handling"
    `parse_args()` calls `sys.exit(2)` on bad input. Use `ArgumentParser(exit_on_error=False)` (Python 3.9+) to catch `ArgumentError` instead.
