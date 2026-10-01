---
theme: seriph
# background: https://cover.sli.dev
title: Getting Started with Free-Threaded Python Using NumPy
class: text-center
transition: slide-left
comark: true
---

# Getting Started with Free-Threaded Python Using NumPy

Christopher Ariza <br/>




---
layout: center
class: text-center quote
---

<style scoped>
.slidev-layout {
  background-color: #0f0f1e;
  background-image: radial-gradient(ellipse 60% 50% at 50% 50%, rgba(60, 60, 110, 0.5) 0%, transparent 100%);
}
</style>

# “Python is slow.”

<!--
We have all heard this said many times
For many of us who have used Python for decades, you cannot help but bristle a little bit
Yes, some operations are slow, but we get have such readability and flexability
Yes, numerical ops are also slow but we have access to excellent C-libraries like NumPy and Arrow
But one aspect of Python performance remained hard to justify: concurrency
-->


---
class: history
---

# Python Concurrency: Two Suboptimal Options

<v-clicks depth=2>

- Multithreading and Multiprocessing
- Multithreading
    - Excellent for I/O-bound processing
    - Terrible for CPU-bound processing
    - The Global Interpreter Lock (GIL)
- Multiprocessing
    - Excellent for true CPU concurrency
    - Significant startup and memory overhead
    - Practical only when units of work are large

</v-clicks>


---
class: history
---

# Python Free Threading

<v-clicks depth=2>

- Python threads are no longer bound by the GIL
- Python 3.13 (experimental), Python 3.14 (supported)


</v-clicks>



---
class: history
---

# GIL-Bound Threading: Python 3.14

```python {1-6|8-10|12-}
>>> from concurrent.futures import ThreadPoolExecutor
>>> import numpy as np

>>> array = np.arange(100_000_000).reshape(10_000, 10_000)
>>> def f(row): (row[row % 2 == 0]**2).sum()
...

>>> %timeit np.fromiter((f(row) for row in array), dtype=float,
count=array.shape[0])
313 ms ± 4.92 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

>>> %timeit with ThreadPoolExecutor() as ex:
np.fromiter(ex.map(f, array), dtype=float, count=array.shape[0])
383 ms ± 12.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

---
class: history
---

# Free-Threading: Python 3.14t

```python {1-6|8-10|12-}
>>> from concurrent.futures import ThreadPoolExecutor
>>> import numpy as np

>>> array = np.arange(100_000_000).reshape(10_000, 10_000)
>>> def f(row): (row[row % 2 == 0]**2).sum()
...

>>> %timeit np.fromiter((f(row) for row in array), dtype=float,
count=array.shape[0])
306 ms ± 2.25 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

>>> %timeit with ThreadPoolExecutor() as ex:
np.fromiter(ex.map(f, array), dtype=float, count=array.shape[0])
71 ms ± 682 μs per loop (mean ± std. dev. of 7 runs, 10 loops each)
```

---
class: history
---

# The Global Interpreter Lock

<v-clicks depth=2>

- A lock on bytecode execution: `pthread_mutex_lock()` (POSIX)
- Only one thread can execute bytecode at a time
- Ensures no data races
- Over a decade of work to remove the GIL
- “No GIL” is “free-threaded”

</v-clicks>



---
class: history
---

# The Journey to No-GIL

<v-clicks depth=2>

- Thread-safe reference counting
    - Biased: `ob_ref_local`, `ob_ref_shared`
    - Per-thread thread-based storage
    - Deferred
    - Immortal objects
    - Stop-the-world GC
- Built-in locking in containers
- A new memory allocator (mimalloc)

</v-clicks>



---
layout: center
class: text-center quote
---

<style scoped>
.slidev-layout {
  background-color: #0f0f1e;
  background-image: radial-gradient(ellipse 60% 50% at 50% 50%, rgba(60, 60, 110, 0.5) 0%, transparent 100%);
}
</style>

# Free-threading may be the greatest enhancement to Python performance


<!-- More impactful than JIT and many other recent enhancements  -->


---
class: history
---

# Why I Care

<v-clicks depth=2>

- Lots of CPU-bound processing
- Lots of embarrassingly parallel row-wise calculations
- Multiprocessing overhead overwhelmed concurrency benefits

</v-clicks>

---
class: history
---

# Why You Should Care

<v-clicks depth=2>

- Free-threading offers the quickest path to better performance
- Easy to use with standard-library tools

</v-clicks>


---
class: history
---

# Why NumPy

<v-clicks depth=2>

- Processing NumPy 2D arrays generalizes to other domains
- NumPy early to offer free-threaded wheels
- NumPy is already fast and (sometimes) GIL-free
- Faster NumPy processing is extraordinary

</v-clicks>



<!-- II -->


---
layout: center
class: text-center
---

<style scoped>
.slidev-layout {
  background-color: #1a1a2e;
  background-image: radial-gradient(rgba(255,255,255,0.05) 2px, transparent 2px);
  background-size: 48px 48px;
}
</style>

# Running Free-Threaded Python

<div style="position:absolute;right:0%;bottom:-5%;font-size:450px !important;line-height:1 !important;opacity:0.04;pointer-events:none;filter:brightness(0) invert(1);">🐍</div>



---
class: history
---

# Installing & Building

<v-clicks depth=2>

- Two different binaries: `python3.14` and `python3.14t`
- Distributors
    - Python.org
    - MacOS: homebrew: `brew install python-freethreading`
    - Debian / Ubuntu: `apt`:
        ```bash
        sudo add-apt-repository ppa:deadsnakes/ppa
        sudo apt update
        sudo apt install python3.14-nogil
        ```
- Compiling from source: `--disable-gil`

</v-clicks>


---
class: history
---

# Running

<v-clicks depth=2>

- A free-threading build has `python3.14` and `python3.14t` binaries
- Virtual environments have only `python3.14` and `python`

</v-clicks>


---
class: history
---

# Discovery

<v-clicks depth=2>

- Neither binary name nor version tells you it is free-threaded
```bash
$ python --version
Python 3.14.0
```
- Two approaches to discovery:
```bash
$ python -VV
Python 3.14.0 free-threading build (main, Oct  8 2025, 09:33:34) [GCC 13.3.0]

$ strings ~/.env314t/bin/python | grep -i 'free-threading build'
%.80s free-threading build (%.80s) %.80s
```

</v-clicks>


---
class: history
---

# The GIL Is a Zombie

<v-clicks depth=2>

- The GIL is disabled, not removed
- The GIL can be reenabled at startup
    - `PYTHON_GIL=1` environment variable
    - `-X gil=1` flag at launch
- The GIL can be reeanbled during runtime
- Discovering the GIL status: `sys._is_gil_enalbled()`

</v-clicks>


---
class: history
---

# Raising the Dead


```bash{1-2|3-4}
$ python3 -c "import sys;print(sys._is_gil_enabled())"
False
$ python3 -X gil=1 -c "import sys;print(sys._is_gil_enabled())"
True
```



---
class: history
---

# The Requirement of Compatible Packages

<v-clicks depth=2>

- Binary wheels must be specially built
- Importing non-compatible wheels re-enables the GIL
- Native Python packages are always compatible

</v-clicks>



---
class: history
---

# Building Free-Threading Compatible C-Extensions

<v-clicks depth=2>

- `Py_GIL_DISABLED`: constant for discovery of runtime type
- `PyUnstable_Module_SetGIL()`: register no-GIL support
```c {1-5,9|6-8}
PyMODINIT_FUNC
PyInit_mymodule(void)
{
    PyObject *m = PyModule_Create(&moduledef);
    if (m == NULL) { return NULL; }
#ifdef Py_GIL_DISABLED
    PyUnstable_Module_SetGIL(m, Py_MOD_GIL_NOT_USED);
#endif
    return m;
}
```

</v-clicks>


<!-- #ifdef is a preprocessor directive -->


---
class: history
---

# Compatible Does Not Mean Thread-Safe

<v-clicks depth=2>

- Declaring `Py_MOD_GIL_NOT_USED` does not render thread safety
- Easy to accidentally rely on the GIL
- Shared mutable module state

</v-clicks>




<!-- III -->

---
layout: center
class: text-center
---

<style scoped>
.slidev-layout {
  background-color: #1a2e2a;
  background-image: radial-gradient(rgba(255,255,255,0.05) 2px, transparent 2px);
  background-size: 48px 48px;
}
</style>

# Using `ThreadPoolExecutor`

<div style="position:absolute;right:-0%;bottom:-5%;font-size:450px !important;line-height:1 !important;opacity:0.04;pointer-events:none;filter:brightness(0) invert(1);">🐝</div>



---
class: mitigation
---

# Runing Threads in Python

<v-clicks depth=2>

- `Thread` objects
- Concurrent futures `ThreadPoolExecutor`

</v-clicks>


---
class: mitigation
---

# Using `ThreadPoolExecutor`

<v-clicks depth=2>

- Context manager for multi-threaded processing
- Configurable worker counts
- Executor `map()` processes one function with many args
- Executor `submit()` creates futures

</v-clicks>


---
class: mitigation
---

# `ThreadPoolExecutor.map()`

```python{1|3-4|6-7|9-}
from concurrent.futures import ThreadPoolExecutor

def add(a, b):
    return a + b

left = [1, 2, 3, 4]
right = [10, 20, 30, 40]

with ThreadPoolExecutor() as executor:
    results = list(executor.map(add, left, right))
```

<!-- Units of work driven by arg count -->


---
class: mitigation
---

# `ThreadPoolExecutor.submit()`

```python{1-2|4|6-}
def add(a, b):
    return a + b

pairs = [(1, 10), (2, 20), (3, 30)]

with ThreadPoolExecutor() as executor:
    futures = [executor.submit(add, *args) for args in pairs]
    results = [future.result() for future in futures]
```



---
class: mitigation
---

# Multi-Threading NumPy Processes

<v-clicks depth=2>

- Many NumPy processes are already no-GIL
- Few NumPy processes use threads
- A high performance bar
- NumPy arrays can be made immutable: `flags.writeable`
- Immutability makes data races impossible

</v-clicks>

<!-- only linear algeabra libraries use threads -->


---
class: mitigation
---

# Using `ThreadPoolExecutor` with 2D arrays

<v-clicks depth=2>

- Iterating a 2D array yields 1D rows
```python
>>> array = np.arange(20).reshape(4,5)
>>> list(array)
[array([0, 1, 2, 3]), array([4, 5, 6, 7]), array([ 8,  9, 10, 11])]
```
- Call `ThreadPoolExecutor.map()` on array
```python
>>> ThreadPoolExecutor.map(proc, array)
```
- Use `numpy.from_iter()` to build 1D result array
```python
>>> np.fromiter((a.sum() for a in array), dtype=int, count=array.shape[0])
array([ 6, 22, 38])
```

</v-clicks>


---
class: mitigation
---

# Configuring Worker Counts

<v-clicks depth=2>

- More threads can do more work
- More threads incur overhead
- `ThreadPoolExecutor()` `max_workers` parameter
- Default: `max_workers=min(32, (os.process_cpu_count() or 1) + 4)`
- For CPU-bound processes, fewer can be better
- Test and measure

</v-clicks>




<!-- IV -->

---
layout: center
class: text-center
---

<style scoped>
.slidev-layout {
  background-color: #1a2e2a;
  background-image: radial-gradient(rgba(255,255,255,0.05) 2px, transparent 2px);
  background-size: 48px 48px;
}
</style>

# Performance Panels

<div style="position:absolute;right:1%;bottom:-5%;font-size:450px !important;line-height:1 !important;opacity:0.04;pointer-events:none;filter:brightness(0) invert(1);">🚀</div>



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

# Code: Processing Harness

```python{1|3-4|6-}
def proc(row): ...

# single threaded
np.fromiter((proc(row) for row in array), dtype=float, count=array.shape[0])

# 8 threads
with ThreadPoolExecutor(max_workers=8) as ex:
    np.fromiter(ex.map(proc, array), dtype=float, count=array.shape[0])
```



---
class: mitigation
---

# Code: Processing Types

```python{1-2|4-5|7-}
def proc(row): # Many PyObjects
    return  max(Counter(row.tolist()).values())

def proc(row): # Few PyObjects
    return (row[row % 2 == 0] ** 2).sum()

def proc(row): # One PyObject
    return row.sum()
```


---
class: mitigation
---

# One Fixture is Not Enough

<v-clicks depth=2>

- Performance evaluation must consider shape
- Shape categories
    - Tall: many smaller rows
    - Square: row size and count equal
    - Wide: fewer larger rows
- Row-processing performance
    - Tall: more smaller units of work
    - Wide: fewer larger units of work
- 100M (1e8) and 1M (1e6) sizes


</v-clicks>




---
class: mitigation
---

# Per-row `max(Counter())` 1e8

<img class="plot" src="/images/ft-np-perf-counter-1e8.png" />



---
class: mitigation
---

# Per-row `max(Counter())` 1e6

<img class="plot" src="/images/ft-np-perf-counter-1e6.png" />




---
class: mitigation
---

# Per-row even square sum 1e8

<img class="plot" src="/images/ft-np-perf-ess-1e8.png" />



---
class: mitigation
---

# Per-row `sum()` 1e8

<img class="plot" src="/images/ft-np-perf-sum-1e8.png" />




<!-- V -->

---
layout: center
class: text-center
---

<style scoped>
.slidev-layout {
  background-color: #1a1a2e;
  background-image: radial-gradient(rgba(255,255,255,0.05) 2px, transparent 2px);
  background-size: 48px 48px;
}
</style>

# When Multi-Threading Goes Wrong

<div style="position:absolute;right:-6%;bottom:-10%;font-size:450px !important;line-height:1 !important;opacity:0.04;pointer-events:none;filter:brightness(0) invert(1);">🧵</div>



---
class: history
---

# Threading Overhead Can Degrade Performance

<v-clicks depth=2>

- Very small units of work
- Too many threads

</v-clicks>

<!-- These have already been seen and discussed -->

---
class: history
---

# Data Races

<v-clicks depth=2>

- Thread execution is indeterminate between threads
- In-place mutation leads to indeterminate results
- Requires locks
- Defend with immutable data structures
    - `tuple`
    - `np.ndarray.flags.writeable`
    - `frozendict` (3.15!)

</v-clicks>


---
class: history
---

# Data Races: In-Place Summation (Lost Update)

```python{1-4|6-7|9}
data = [0]
def increment(_):
    for _ in range(100_000):
        data[0] += 1  # read, add, write: not atomic

with ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(increment, range(8))

print(f"Expected: {800_000:,}, Found: {data[0]:,}")
```



---
class: history
---

# Data Races: In-Place Summation (Lost Update)

```bash{1-2|4-5|7-8}
$ ~/.env314/bin/python ex.py
Expected: 800,000, Found: 800,000

$ ~/.env314t/bin/python ex.py
Expected: 800,000, Found: 209,515

$ ~/.env314t/bin/python ex.py
Expected: 800,000, Found: 207,052
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



<!-- VI -->

---
layout: center
class: text-center
---

<style scoped>
.slidev-layout {
  background-color: #1a1a2e;
  background-image: radial-gradient(rgba(255,255,255,0.05) 2px, transparent 2px);
  background-size: 48px 48px;
}
</style>

# Bridging GIL and Free-Threaded Environments

<div style="position:absolute;right:0%;bottom:-10%;font-size:450px !important;line-height:1 !important;opacity:0.04;pointer-events:none;filter:brightness(0) invert(1);">🤝</div>


---
class: history
---

# Assumptions of Free Threading May not Hold

<v-clicks depth=2>

- The GIL can be reenabled at anytime!
- Your code might run under python3.14 instead of 3.14t
- Threads with the GIL can lead to serious performance degradation

</v-clicks>


---
class: history
---

# Dynamic Threading Engagement

<v-clicks depth=2>

- Check the GIL state before threading
- `sys._is_gil_enabled()`
- `conditional-futures`: `ConditionalThreadPoolExecutor`

</v-clicks>



---
class: history
---

# `sys._is_gil_enabled()`

```python{1-2|4-6|4-}
array = np.arange(100_000_000).reshape(10_000, 10_000)
def f(row): (row[row % 2 == 0]**2).sum()

if hasattr(sys, '_is_gil_enabled') and not sys._is_gil_enabled():
    with ThreadPoolExecutor() as ex:
        x = np.fromiter(ex.map(f, array), dtype=float, count=array.shape[0])
else:
    x = np.fromiter((f(row) for row in array),
        dtype=float,
        count=array.shape[0])
```



---
class: history
---

# `ConditionalThreadPoolExecutor`

<v-clicks depth=2>

- `pip install conditional_futures`
- An `Executor` subclass
- If GIL is active, falls-back on single threaded processing

</v-clicks>




---
class: history
---

# `ConditionalThreadPoolExecutor`

```python{1|3-4|5-}
from conditional_futures import ConditionalThreadPoolExecutor

array = np.arange(100_000_000).reshape(10_000, 10_000)
def f(row): (row[row % 2 == 0]**2).sum()

with ConditionalThreadPoolExecutor() as ex:
    x = np.fromiter(ex.map(f, array), dtype=float, count=array.shape[0])
```


---

# Talk to Your Agents about Concurrency

<v-clicks depth=2>

- My agents often implement serial first
- `python`:
    - Obvious I/O bound processes
- `rust`:
    - Trivial CPU-bound loop to parallel iterator with `rayon`
- Agents can rapidly do performance tests of alternate designs and fixtures

</v-clicks>




---

# Conclusions

<v-clicks depth=2>

- Multi-threading arrays: a pathological case
- Free-threading is no-longer experimental
- Growing package support
    - PyPI classifier: "Programming Language :: Python :: Free Threading"
    - Tracking top 360: https://hugovk.github.io/free-threaded-wheels/
- Adoption can be difficult

</v-clicks>



---
layout: center
class: text-center
---

# Thank You

https://flexatone.net

<!-- <PoweredBySlidev mt-10 /> -->
