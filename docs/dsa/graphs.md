# Graphs

A graph G = (V, E) is a set of vertices V connected by edges E. Unlike trees, graphs can have cycles and disconnected components.

## Representations

### Adjacency list — `dict[int, list[int]]`

```python
graph = {
    0: [1, 2],
    1: [0, 3],
    2: [0],
    3: [1],
}
```

- Storage: O(V + E) — only existing edges stored.
- Edge lookup: O(degree(v)).
- **Use for sparse graphs** (default choice).

### Adjacency matrix — `list[list[int]]`

```python
matrix = [
    [0, 1, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [0, 1, 0, 0],
]
```

- Storage: O(V²) — all pairs, regardless of edge count.
- Edge lookup: O(1) — `matrix[u][v]`.
- **Use for dense graphs** or when O(1) edge checks are needed (e.g. Floyd-Warshall).

---

## BFS — Breadth-First Search

Explores level by level. Uses a `deque` as a FIFO (First In, First Out) queue. Natural for **shortest path** in unweighted graphs.

```python
from collections import deque

def bfs(graph: dict[int, list[int]], start: int) -> list[int]:
    visited = {start}       # mark before enqueuing to prevent duplicates
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nbr in graph[node]:
            if nbr not in visited:
                visited.add(nbr)
                queue.append(nbr)
    return order
```

Shortest path variant — carry distance in the queue:

```python
def bfs_shortest(graph, start, end):
    visited = {start}
    queue = deque([(start, 0)])
    while queue:
        node, dist = queue.popleft()
        if node == end:
            return dist
        for nbr in graph[node]:
            if nbr not in visited:
                visited.add(nbr)
                queue.append((nbr, dist + 1))
    return -1
```

---

## DFS — Depth-First Search

Explores one path fully before backtracking. Natural for **connected components, cycle detection, topological sort**.

### Iterative (explicit stack)

```python
def dfs(graph: dict[int, list[int]], start: int) -> list[int]:
    visited = set()
    stack = [start]
    order = []
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        for nbr in graph[node]:
            if nbr not in visited:
                stack.append(nbr)
    return order
```

!!! warning "Mark visited after popping, not before pushing"
    A node can appear in the stack multiple times before being processed. The `if node in visited: continue` guard handles this. BFS marks before enqueuing (safe because each node appears at most once per level); iterative DFS marks after popping.

### Topological sort (DFS post-order)

A node is appended *after* all its descendants are processed; reversing gives dependency order.

```python
def topo_sort(graph: dict[int, list[int]]) -> list[int]:
    visited, order = set(), []
    def dfs(node):
        visited.add(node)
        for nbr in graph[node]:
            if nbr not in visited:
                dfs(nbr)
        order.append(node)          # post-order: after all descendants
    for node in graph:
        if node not in visited:
            dfs(node)
    return order[::-1]              # reverse post-order = topological order
```

---

## Connected components

```python
def connected_components(graph: dict[int, list[int]]) -> list[list[int]]:
    visited, components = set(), []
    for node in graph:
        if node not in visited:
            component = bfs(graph, node)
            visited.update(component)
            components.append(component)
    return components
```

---

## BFS vs DFS

| | BFS | DFS |
|--|-----|-----|
| Data structure | `deque` (FIFO) | stack / recursion (LIFO) |
| Explores | level by level | one full path first |
| Shortest path (unweighted) | ✓ | ✗ |
| Topological sort | Kahn's algo | post-order (above) |
| Space worst case | O(V) wide level | O(V) deep path |

## Complexity

| | Adjacency list | Adjacency matrix |
|--|---------------|-----------------|
| Storage | O(V + E) | O(V²) |
| BFS / DFS | O(V + E) | O(V²) |
| Edge exists? | O(degree) | O(1) |

## See also

- [queues.md](queues.md) — `deque` mechanics underlying BFS
- [trees.md](trees.md) — trees are acyclic connected graphs; DFS traversal patterns carry over
- [complexity.md](complexity.md) — storage and traversal costs
