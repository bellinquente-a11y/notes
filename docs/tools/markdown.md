# Markdown

Lightweight markup that renders as HTML. CommonMark is the baseline spec; GitHub (GFM) and MkDocs add extensions.

!!! tip "Mental model"
    Two layers: **block elements** (headings, lists, code fences, tables, blockquotes) define structure and are separated by blank lines; **inline elements** (bold, links, code) decorate content within a block. Rendering problems are almost always a missing blank line or wrong indentation.

---

## Block elements

### Headings

```markdown
# H1
## H2
### H3
```

Prefer ATX-style (`#`) over Setext (`===` / `---`).

### Lists

```markdown
- unordered  (use -, *, or + consistently)
  - nested (2-space indent)

1. ordered
2. items

- [x] task done
- [ ] task pending
```

### Code blocks

````markdown
```python
def foo(): return 42
```
````

Language tag enables syntax highlighting. Four-space indent also works but fenced blocks are preferred.

### Blockquotes

```markdown
> quote text
>> nested quote
```

### Tables (GFM)

```markdown
| A    |  B   |    C |
|------|:----:|-----:|
| left | ctr  | right|
```

Colons in the separator row set alignment (left / centre / right).

### Horizontal rule

```markdown
---
```

---

## Inline elements

| Syntax | Result |
|--------|--------|
| `*text*` or `_text_` | *italic* |
| `**text**` | **bold** |
| `***text***` | ***bold italic*** |
| `~~text~~` | ~~strikethrough~~ (GFM) |
| `` `code` `` | inline code |

### Links

```markdown
[label](https://url)               # inline
[label](url "title")               # with hover title
[label][ref]  …  [ref]: url        # reference-style
```

Relative links work: `[other note](../python/typing.md)`.

### Images

```markdown
![alt text](image.png)
```

### Escaping

Prefix special characters with `\` to render them literally: `\*`, `\#`, `\_`.

---

## MkDocs / Material extensions

### Admonition boxes

```markdown
!!! note "Title"
    Body (4-space indent).

!!! warning
!!! tip
!!! info / success / failure / danger / bug / example / quote
```

Collapsible: `???` (collapsed) or `???+` (open).

### Code with line numbers and highlights

````markdown
```python linenums="1" hl_lines="2 3"
def foo():
    x = 1
    return x
```
````

### Footnotes

```markdown
Text.[^1]

[^1]: Footnote content.
```
