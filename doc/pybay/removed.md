

---
class: mitigation
---

# `ThreadPoolExecutor` As Completed

```python
def add(a, b):
    return a + b

pairs = [(1, 10), (2, 20), (3, 30)]
results = [None] * len(pairs)

with ThreadPoolExecutor() as ex:
    futures = {
        ex.submit(add, *args): i for i, args in enumerate(pairs)
    }
    for future in as_completed(futures):
        results[futures[future]] = future.result()
```
