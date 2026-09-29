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

# "Python is slow."

<!--
We have all heard this said many times
For many of us who have used Python for decades, you cannot help but bristle a little bit
Yes, some operations are slow, but we get have such readability and flexability
Yes, numerical ops are also slow but we have access to excellent C-libraries like NumPy and Arrow
But one aspect of Python performance remained hard to justify: no true CPU concurrency
And frankly, it was embarrassing!
-->




---
class: history
---

# Embarrassingly Parallel Operations

<v-clicks depth=2>

- Concurrency is not always easy
- Easy concurrency is embarrassing: no dependencies
- Processing isolated data partitions
    - Applying the same function to numerous files or images
    - Processing numerous simulation scenarios
    - Processing records from a DB query
    - Processing rows or columns from an array

</v-clicks>


---
class: history
---

# But Python Has Long Supported Concurrency

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

# GIL-Bound Threading: Python 3.14

```python {1-6|8-9|11-12}
>>> from concurrent.futures import ThreadPoolExecutor
>>> import numpy as np

>>> array = np.arange(100_000_000).reshape(10_000, 10_000)
>>> def f(row): (row[row % 2 == 0]**2).sum()
...

>>> %timeit np.fromiter((f(row) for row in array), dtype=float, count=array.shape[0])
313 ms ± 4.92 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

>>> %timeit with ThreadPoolExecutor() as ex: np.fromiter(ex.map(f, array), dtype=float, count=array.shape[0])
383 ms ± 12.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

---
class: history
---

# Free-Threading: Python 3.14t

```python {1-6|8-9|11-12}
>>> from concurrent.futures import ThreadPoolExecutor
>>> import numpy as np

>>> array = np.arange(100_000_000).reshape(10_000, 10_000)
>>> def f(row): (row[row % 2 == 0]**2).sum()
...

>>> %timeit np.fromiter((f(row) for row in array), dtype=float, count=array.shape[0])
306 ms ± 2.25 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

>>> %timeit with ThreadPoolExecutor() as ex: np.fromiter(ex.map(f, array), dtype=float, count=array.shape[0])
71 ms ± 682 μs per loop (mean ± std. dev. of 7 runs, 10 loops each)
```

---
class: history
---

# The Global Interpreter Lock

<v-clicks depth=2>

- The GIL ensures no data races
- Only one thread can execute bytecode at a time
- Over a decade of work to remove the GIL
- "No GIL" is "free-threaded"

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

<div style="position:absolute;right:0%;bottom:-10%;font-size:450px !important;line-height:1 !important;opacity:0.03;pointer-events:none;filter:brightness(0.1) invert(1);">📦</div>



---
class: history
---

# Installing & Building

<v-clicks depth=2>

- Two different binaries: `python3.14` and `python3.14t`
- Distributors
    - Python.org
    - homebrew: `brew install python-freethreading`
    - apt:
        ```bash
        sudo add-apt-repository ppa:deadsnakes/ppa
        sudo apt update
        sudo apt install python3.14-nogil
        ```
- Compiling: `--disable-gil`

</v-clicks>


---
class: history
---

# Running

<v-clicks depth=2>

- A `python3.14t` build has `python3.14` and `python3.14t` binaries
- Virtual environments will will have only `python3.14` and `python`
- Interactive announces
```bash
$ py_src_3.14.0t/bin/python3.14
Python 3.14.0 free-threading build (main, Oct  8 2025, 09:33:34) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.

$ py_src_3.14.0t/bin/python3.14t
Python 3.14.0 free-threading build (main, Oct  8 2025, 09:33:34) [GCC 13.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
```
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

# The GIL Is Now a Zombie

<v-clicks depth=2>

- The GIL is disabled, not removed
- Reenabling the GIL
    - `PYTHON_GIL=1` environment variable
    - `-X gil=1` flag at launch

</v-clicks>




---
class: history
---

# Running

<v-clicks depth=2>

- A `python3.14t` build has `python`
- The GIL is disabled, not removed
- Reenabling the GIL
    - `PYTHON_GIL=1` environment variable
    - `-X gil=1` flag at launch

</v-clicks>




---
class: history
---

# The Requirement of Compatible Packages

<v-clicks depth=2>

- Binary wheels must be specially built
- Importing non-compatible wheels will re-enable the GIL
- Native Python package / wheel are always compatible

</v-clicks>



---
class: history
---

# Building Free-Threading Compatible C-Extensions

<v-clicks depth=2>

- `Py_GIL_DISABLED`: constant for discovery of runtime type
- `PyUnstable_Module_SetGIL()`: register no-GIL support
```c
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

<div style="position:absolute;right:-5%;bottom:-5%;font-size:450px !important;line-height:1 !important;opacity:0.03;pointer-events:none;filter:brightness(0) invert(1);">🛡️</div>



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

# `ThreadPoolExecutor` Ordered, Arg Lists

```python
from concurrent.futures import ThreadPoolExecutor

def add(a, b):
    return a + b

left = [1, 2, 3, 4]
right = [10, 20, 30, 40]

with ThreadPoolExecutor() as executor:
    results = list(executor.map(add, left, right))
```


---
class: mitigation
---

# `ThreadPoolExecutor` Ordered, Arg Tuples

```python
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
class: mitigation
---

# Multi-Threading NumPy Processes

<v-clicks depth=2>

- Many NumPy processes are already no-GIL
- A high bar
- NumPy arrays can be made immutable
    - `flags.writeable`
- Immutability makes data races impossible

</v-clicks>


---
class: mitigation
---

# Using `ThreadPoolExecutor` with 2D arrays

<v-clicks depth=2>

- `ThreadPoolExecutor.map()` of 1D array rows
- `numpy.from_iter()` to build 1D array
- Processing rows into a 1D array
- Processing rows into other PyObjects

</v-clicks>


---
class: mitigation
---

# Configuring Worker Counts

<v-clicks depth=2>

- More threads can do more work
- More threads incur overhead
- `max_workers` parameter
    - Default: `max_workers=min(32, (os.process_cpu_count() or 1) + 4)`
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

<div style="position:absolute;right:-5%;bottom:-5%;font-size:450px !important;line-height:1 !important;opacity:0.03;pointer-events:none;filter:brightness(0) invert(1);">🛡️</div>



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

<div style="position:absolute;right:0%;bottom:-10%;font-size:450px !important;line-height:1 !important;opacity:0.03;pointer-events:none;filter:brightness(0.1) invert(1);">📦</div>



---
class: history
---

# Threading Overhead Can Degrade Performance

<v-clicks depth=2>

- Very small units of work
- Too many threads

</v-clicks>



---
class: history
---

# Data Races

<v-clicks depth=2>

- Thread indeterminacy with in-place mutation
- Defend with immutable data structures
    - `tuple`
    - `np.ndarray.flags.writeable`
    - `frozendict` (3.15!)

</v-clicks>


---
class: history
---

# Data Races: In-Place Summation

```python
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

# Data Races: In-Place Summation

```bash
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

```python
rng = np.random.default_rng(0)
signal, kernel = rng.random(1_000_000), rng.random(10)
chunk = 100
out = np.zeros(len(signal) + len(kernel) - 1)

def process(start):
    result = np.convolve(signal[start:start + chunk], kernel)
    out[start:start + len(result)] += result

with ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(process, range(0, len(signal), chunk))

print(f"Mismatched elements: {(~np.isclose(out, np.convolve(signal, kernel))).sum():,} of {len(out):,}")
```



---
class: history
---

# Data Races: In-Place Convolution

```bash
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

<div style="position:absolute;right:0%;bottom:-10%;font-size:450px !important;line-height:1 !important;opacity:0.03;pointer-events:none;filter:brightness(0.1) invert(1);">📦</div>


---
class: history
---

# Assumptions of Free Threading May not Hold

<v-clicks depth=2>

- The GIL can be enabled at anytime!
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

```python
array = np.arange(100_000_000).reshape(10_000, 10_000)
def f(row): (row[row % 2 == 0]**2).sum()

if hasattr(sys, '_is_gil_enabled') and not sys._is_gil_enabled():
    with ThreadPoolExecutor() as ex:
        x = np.fromiter(ex.map(f, array), dtype=float, count=array.shape[0])
else:
    x = np.fromiter((f(row) for row in array), dtype=float, count=array.shape[0])
```




---
class: history
---

# `ConditionalThreadPoolExecutor`

- `pip install conditional_futures`
- An `Executor` subclass
- If GIL is active, falls-back on single threaded processing

```python

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
    - When identified, easily refactored
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
