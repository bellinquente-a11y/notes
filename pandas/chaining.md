# Method Chaining and SettingWithCopyWarning

## Method chaining

Instead of reassigning `df` repeatedly, chain operations that each return a new DataFrame:

```python
result = (
    raw
    .query('price > 0')
    .assign(
        log_price=lambda d: np.log(d['price']),
        returns=lambda d: d['price'].pct_change(),
    )
    .dropna()
    .reset_index(drop=True)
)
```

`raw` is never mutated. Each step is independently readable and commentable.

### `.query(expr)` — filter rows

```python
df.query('age > 18 and city == "London"')
df.query('price > @threshold')   # @ references a Python variable
```

### `.assign(**kwargs)` — add or overwrite columns

```python
df.assign(
    income_k=lambda d: d['income'] / 1_000,
    is_high_earner=lambda d: d['income_k'] > 50,   # can reference columns assigned above
)
```

Lambdas receive the DataFrame *as it is at that step*. Columns added earlier in the same call are visible to later ones (dict ordering, Python 3.7+). Assign `None` to drop a column.

### `.pipe(func, *args, **kwargs)` — apply a named function mid-chain

```python
def trim_outliers(df, col, n_std=3):
    lo, hi = df[col].mean() - n_std*df[col].std(), df[col].mean() + n_std*df[col].std()
    return df[df[col].between(lo, hi)]

result = (
    raw
    .assign(returns=lambda d: d['close'].pct_change())
    .pipe(trim_outliers, col='returns', n_std=2.5)
    .dropna()
)
```

`df.pipe(f, ...)` calls `f(df, ...)` — a fluency adapter for functions that don't natively chain. Debug mid-chain: `.pipe(lambda d: (print(d.shape), d)[1])`.

---

## Common chain operations — catalog

| # | Method | What it does |
|---|--------|-------------|
| 1 | `.query(expr)` | Filter rows |
| 2 | `.assign(**kwargs)` | Add or transform columns |
| 3 | `.astype(dict)` | Cast dtypes |
| 4 | `.rename(columns=...)` | Rename columns |
| 5 | `.drop(columns=[...])` / `.filter(...)` | Remove or select columns |
| 6 | `.sort_values(by=...)` | Sort rows |
| 7 | `.dropna()` / `.fillna(...)` | Handle missing values |
| 8 | `.assign(c=lambda d: d['c'].str...)` | String operations on a column |
| 9 | `.set_index()` / `.reset_index(drop=True)` | Index management |
| 10 | `.groupby().agg(...)` | Aggregate by group |

### 1. Filter rows — `.query()`

```python
df.query('price > 0 and volume > 1_000')
df.query('status == "active"')
df.query('date > @cutoff')      # @ = Python variable
```

### 2. Add / transform columns — `.assign()`

See the section above. Key: lambdas see columns added earlier in the same call.

### 3. Cast dtype — `.astype()`

```python
df.astype({'price': 'float32', 'volume': 'float32', 'trades': 'int32'})
# or inline via assign:
df.assign(price=lambda d: d['price'].astype('float32'))
```

Use `.astype(dict)` for bulk casts; `.assign()` when interleaved with other column ops.

### 4. Rename columns — `.rename()`

```python
df.rename(columns={'open_time': 'date', 'quote_vol': 'quote_volume'})
df.rename(columns=str.lower)                        # apply function to all names
df.rename(columns=lambda c: c.replace(' ', '_'))
```

### 5. Select or drop columns

```python
df.drop(columns=['ignore', 'close_time'])
df.filter(items=['open', 'high', 'low', 'close'])   # select by name
df.filter(like='taker')                             # names containing 'taker'
df.filter(regex=r'^vol')                            # names matching regex
```

Prefer `.filter()` over `df[['a','b']]` in a chain — keeps the fluent style.

### 6. Sort — `.sort_values()`

```python
df.sort_values('date')
df.sort_values('volume', ascending=False)
df.sort_values(['date', 'symbol'])
```

### 7. Handle missing — `.dropna()` / `.fillna()`

```python
df.dropna(subset=['open', 'close'])     # drop rows where these cols are null
df.fillna({'volume': 0})
df.ffill()                              # forward-fill (time-series gaps)
```

`.dropna()` usually follows `.assign()` calls that produce NaN (e.g. `.pct_change()`).

### 8. String operations — `.assign()` + `.str`

```python
df.assign(
    symbol=lambda d: d['symbol'].str.upper(),
    name=lambda d: d['name'].str.strip().str.lower(),
    base=lambda d: d['symbol'].str[:-4],    # 'BTCUSDT' → 'BTC'
)
```

Chain `.str` methods: `.str.strip().str.lower().str.replace('-', '_')`. Always vectorised — no `.apply()` loop needed.

### 9. Index management — `.set_index()` / `.reset_index()`

```python
df.set_index('date')            # promote column to index (enables resample)
df.reset_index(drop=True)       # clean 0…n-1 index after filtering/sorting
df.reset_index()                # move index back to a column
```

### 10. Groupby aggregation — `.groupby().agg()`

```python
(df
 .groupby('symbol')
 .agg(
     avg_close=('close', 'mean'),
     total_volume=('volume', 'sum'),
     n=('close', 'count'),
 )
 .sort_values('total_volume', ascending=False)
 .reset_index()
)
```

Named aggregations (`output=('source', 'func')`) name columns directly. The result of `.agg()` re-enters the chain as a normal DataFrame.

### Full pipeline example

```python
result = (
    raw
    .query('volume > 0 and close > 0')
    .astype({'open': 'float32', 'high': 'float32',
             'low': 'float32', 'close': 'float32'})
    .assign(
        returns=lambda d: d['close'].pct_change(),
        buy_ratio=lambda d: d['taker_buy_vol'] / d['volume'],
        symbol=lambda d: d['symbol'].str.upper(),
    )
    .rename(columns={'quote_vol': 'quote_volume'})
    .drop(columns=['ignore'])
    .dropna(subset=['returns'])
    .sort_values('date')
    .reset_index(drop=True)
)
```

---

## SettingWithCopyWarning

Triggered by **chained indexing used for assignment**: two `[]` operations where the first may return a copy.

```python
df[df['age'] > 18]['name'] = 'adult'   # WARNING — assignment likely lost
```

Step 1 (`df[df['age'] > 18]`) returns a new object (view or copy — not guaranteed). Step 2 writes to that object. If it's a copy, `df` is unchanged.

**Why view vs copy is unpredictable:** NumPy returns a view for contiguous slices, a copy for boolean masks and fancy integer indexing. Pandas can't tell you which you got.

### The fix: `.loc` for any write

`.loc[row_mask, col]` is a single operation directly on the original — no intermediate object.

```python
df.loc[df['age'] > 18, 'name'] = 'adult'   # correct
```

**Rule: reading can chain; writing must use `.loc` on the original.**

### Explicit `.copy()` for an independent subset

```python
subset = df[df['age'] > 18].copy()   # explicit intent: separate object
subset['name'] = 'adult'             # safe, no warning
```

### Decision table

| Intent | Pattern | Correct? |
|--------|---------|----------|
| Read from subset | `df[mask]['col'].mean()` | Yes |
| Modify original | `df.loc[mask, 'col'] = v` | Yes |
| Work with a separate copy | `sub = df[mask].copy(); sub['col'] = v` | Yes |
| Modify original (wrong way) | `df[mask]['col'] = v` | No — warning |

### Pandas 2.0+ Copy-on-Write (CoW)

CoW (default in pandas 3.0) makes every indexing result a copy — view-mutation is gone, the warning disappears. Code that wrote to a slice expecting to modify the original silently breaks. Fix: `.loc` on the original, which is correct under both old and CoW semantics.
