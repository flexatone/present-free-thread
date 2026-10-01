

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






---
class: history
---

# Data Races: In-Place Convolution

```python{1-4|6-8|10-11|13-}
rng = np.random.default_rng(0)
signal, kernel = rng.random(1_000_000), rng.random(10)
chunk = 100
out = np.zeros(len(signal) + len(kernel) - 1)

def process(start):
    result = np.convolve(signal[start:start + chunk], kernel)
    out[start:start + len(result)] += result

with ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(process, range(0, len(signal), chunk))

print(f"Mismatched elements:
{(~np.isclose(out, np.convolve(signal, kernel))).sum():,} of
{len(out):,}")
```



---
class: history
---

# Data Races: In-Place Convolution

```bash{1-2|4-5|7-8}
$ ~/.env314/bin/python ex.py
Mismatched elements: 0 of 1,000,009

$ ~/.env314t/bin/python ex.py
Mismatched elements: 1,970 of 1,000,009

$ ~/.env314t/bin/python ex.py
Mismatched elements: 1,989 of 1,000,009
```





---
class: mitigation
---

# Embarrassingly Parallel Operations

<v-clicks depth=2>

- Concurrency is not always easy: locks, shared data
- Easy concurrency is embarrassing: no dependencies
- Processing isolated data partitions
    - Applying the same function to numerous files or images
    - Processing records from a DB query
    - Processing rows or columns from an array

</v-clicks>






---
class: mitigation
---

# Multi-Threading NumPy Operations

<v-clicks depth=2>

- Many NumPy routines are already no-GIL
- Few NumPy routines use threads
- A high performance bar
- NumPy arrays can be made immutable: `flags.writeable`
- Immutability prevents accidental in-place mutation

</v-clicks>




---
class: mitigation
---

# Per-row even square sum 1e6

<img class="plot" src="/images/ft-np-perf-ess-1e6.png" />





- Defend with immutable data structures
    - `tuple`
    - `np.ndarray.flags.writeable`
    - `frozendict` (3.15!)
