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

- Remove the GIL, free the threads
- “No GIL” is “free-threaded”
- Python 3.13 (experimental), Python 3.14 (supported)

</v-clicks>



---
class: history
---

# GIL-Bound Threading: Python 3.14

```python {1-2|4|5-6|8-10|12-}
>>> from concurrent.futures import ThreadPoolExecutor
>>> import numpy as np

>>> array = np.arange(100_000_000).reshape(10_000, 10_000)
>>> def f(row): return (row[row % 2 == 0]**2).sum()
...

>>> %timeit np.fromiter((f(row) for row in array), dtype=float,
count=array.shape[0])
360 ms ± 3.34 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

>>> %timeit with ThreadPoolExecutor() as ex:
np.fromiter(ex.map(f, array), dtype=float, count=array.shape[0])
373 ms ± 24.4 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

---
class: history
---

# Free-Threading: Python 3.14t

```python {1-6|8-10|12-}
>>> from concurrent.futures import ThreadPoolExecutor
>>> import numpy as np

>>> array = np.arange(100_000_000).reshape(10_000, 10_000)
>>> def f(row): return (row[row % 2 == 0]**2).sum()
...

>>> %timeit np.fromiter((f(row) for row in array), dtype=float,
count=array.shape[0])
360 ms ± 1.7 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

>>> %timeit with ThreadPoolExecutor(max_workers=8) as ex:
np.fromiter(ex.map(f, array), dtype=float, count=array.shape[0])
83.7 ms ± 819 μs per loop (mean ± std. dev. of 7 runs, 10 loops each)
```

---
class: history
---

# The Global Interpreter Lock

<v-clicks depth=2>

- A lock on bytecode execution
- Only one thread can execute bytecode at a time
- Protects interpreter internals & reference counts
- Sometimes defends against data-races

</v-clicks>


<!-- pthread_mutex_lock() -->


---
class: history
---

# The Journey to No-GIL

<v-clicks depth=2>

- Over a decade of work to remove the GIL
- Thread-safe reference counting
    - Biased: `ob_ref_local`, `ob_ref_shared`
    - Per-thread reference counting
    - Deferred
    - Immortal objects
- Memory safe throughout the standard library
- A new memory allocator (mimalloc)
    - Per-thread allocation

</v-clicks>


<!-- ob_ref_local is local to the object’s owning thread,
if the current thread is the owner, INCREF/DECREF can update ob_ref_local cheaply, non-atomically;
if another thread touches the object, it updates ob_ref_shared using atomic operations.
-->


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


<!-- More impactful than specializing interpreter and JIT  -->


---
class: history
---

# Why I Care

<v-clicks depth=2>

- Lots of CPU-bound processing
- Lots of embarrassingly parallel row-wise calculations
- Multiprocessing overhead overwhelmed concurrency benefits
- Free-threading unlocks material performance gains

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
    - DataFrames
    - Records from a DB
- NumPy early to offer free-threaded wheels
- Few NumPy routines use threads
- NumPy is already fast and (sometimes) GIL-free
- Faster NumPy processing is extraordinary

</v-clicks>


<!-- only linear algeabra libraries use threads -->




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
    - `uv python install 3.14t`
    - MacOS: homebrew: `brew install python-freethreading`
    - Debian / Ubuntu: `apt`:
        ```bash
        sudo add-apt-repository ppa:deadsnakes/ppa
        sudo apt update
        sudo apt install python3.14-nogil
        ```
    - Windows: nuget: `nuget install python-freethreaded`
- Compiling from source: `--disable-gil`

</v-clicks>


---
class: history
---

# Running

<v-clicks depth=2>

- The binary may not have a `t`
- Can be any of `python`, `python3`, `python3.14`, and `python3.14t`
- `python3` might be GIL or no-GIL

</v-clicks>


---
class: history
---

# Discovery

<v-clicks depth=2>

- Neither binary name nor `--version`
```bash
$ python --version
Python 3.14.0
```
- See in REPL or with `-VV`
```bash
$ python -VV
Python 3.14.0 free-threading build (main, Oct  8 2025, 09:33:34) [GCC 13.3.0]
```
- Check `Py_GIL_DISABLED` via `sysconfig`
```bash
$ python3 -c "import sysconfig;print(sysconfig.get_config_var('Py_GIL_DISABLED'))"
1
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
- The GIL can be reenabled during runtime
- Runtime GIL status: `sys._is_gil_enabled()`

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

- Binary wheels must opt-in to compatibility
- Incompatible packages re-enable the GIL on import
- Pure-Python packages are always compatible

</v-clicks>



---
class: history
---

# Raising the Dead

```python{1-3|4-8|9-}
>>> import sys
>>> sys._is_gil_enabled()
False
>>> import psycopg2
<frozen importlib._bootstrap>:491: RuntimeWarning: The global interpreter lock
(GIL) has been enabled to load module 'psycopg2._psycopg', which has not
declared that it can run safely without the GIL. To override this behavior and
keep the GIL disabled (at your own risk), run with PYTHON_GIL=0 or -Xgil=0.
>>> sys._is_gil_enabled()
True
```


---
class: history
---

# Free-Threading C-Extensions: Single-Phase Init


- `Py_GIL_DISABLED`: compile-time macro
- `PyUnstable_Module_SetGIL()`: register no-GIL support
```c {1-5,9-10|6-8}
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

<!-- #ifdef is a preprocessor directive -->


---
class: history
---

# Free-Threading C-Extensions: Multi-Phase Init


- `Py_mod_gil` module slot: register no-GIL support
- No `#ifdef` on `Py_GIL_DISABLED` needed
```c {9-10|6-8|1-5|3}
static PyModuleDef_Slot slots[] = {
    {Py_mod_exec, mymodule_exec},
    {Py_mod_gil, Py_MOD_GIL_NOT_USED},
    {0, NULL}
};
static PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT, .m_name = "mymodule", .m_slots = slots,
};
PyMODINIT_FUNC
PyInit_mymodule(void) { return PyModuleDef_Init(&moduledef); }
```



---
class: history
---

# Compatible Does Not Mean Thread-Safe

<v-clicks depth=2>

- Declaring `Py_MOD_GIL_NOT_USED` does not ensure thread-safety
- Easy to accidentally rely on the GIL
- Shared mutable module state
- Quantsight-Labs: https://py-free-threading.github.io

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

# Running Threads in Python

<v-clicks depth=2>

- `Thread` objects (Python 1.5.1, 1998)
- Concurrent futures `ThreadPoolExecutor` (Python 3.2, 2011)

</v-clicks>


---
class: mitigation
---

# Using `ThreadPoolExecutor`

<v-clicks depth=2>

- Context manager for multi-threaded processing
- Configurable worker counts
- Two executors
    - `map()` processes one function with many args
    - `submit()` creates futures that block on `result()`

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

# Using `ThreadPoolExecutor` with 2D arrays

<v-clicks depth=2>

- Iterating a 2D array yields 1D rows
```python
>>> array = np.arange(12).reshape(3,4)
>>> list(array)
[array([0, 1, 2, 3]), array([4, 5, 6, 7]), array([ 8,  9, 10, 11])]
```
- Call `ThreadPoolExecutor.map()` with `proc` and `array`
```python
>>> ex.map(proc, array)
```
- Use `np.fromiter()` to build 1D result
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
- `max_workers` configures maximum `ThreadPoolExecutor()` thread count
- I/O bound default: `min(32, (os.process_cpu_count() or 1) + 4)`
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
def proc(row): # One PyObject
    return row.sum()

def proc(row): # Few PyObjects
    return (row[row % 2 == 0] ** 2).sum()

def proc(row): # Many PyObjects
    return max(Counter(row.tolist()).values())
```


---
class: mitigation
---

# One Fixture is Not Enough

<v-clicks depth=2>

- Performance evaluation must consider shape
- Three shapes of the same elements
    - Tall: many smaller rows
    - Square: row size and count equal
    - Wide: fewer larger rows
- Row-processing performance
    - Tall: more smaller units of work
    - Wide: fewer larger units of work
- 100M (1e8) and 1M (1e6) elements


</v-clicks>




---
class: mitigation
---

# Per-row `sum()`

```python{1-2}
def proc(row): # One PyObject
    return row.sum()

def proc(row): # Few PyObjects
    return (row[row % 2 == 0] ** 2).sum()

def proc(row): # Many PyObjects
    return max(Counter(row.tolist()).values())
```


---
class: mitigation
---

# Per-row `sum()` 1e8

<img class="plot" src="/images/ft-np-perf-sum-1e8.png" />


---
class: mitigation
---

# Per-row `sum()` 1e6

<img class="plot" src="/images/ft-np-perf-sum-1e6.png" />




---
class: mitigation
---

# Per-row even squared sum

```python{4-5}
def proc(row): # One PyObject
    return row.sum()

def proc(row): # Few PyObjects
    return (row[row % 2 == 0] ** 2).sum()

def proc(row): # Many PyObjects
    return max(Counter(row.tolist()).values())
```



---
class: mitigation
---

# Per-row even square sum 1e8

<img class="plot" src="/images/ft-np-perf-ess-1e8.png" />




---
class: mitigation
---

# Per-row `max(Counter())`

```python{7-}
def proc(row): # One PyObject
    return row.sum()

def proc(row): # Few PyObjects
    return (row[row % 2 == 0] ** 2).sum()

def proc(row): # Many PyObjects
    return max(Counter(row.tolist()).values())
```


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

# Generalizations

<v-clicks depth=2>

- The greater the row cost, the more threads benefit
- Creating `PyObject` a significant row cost
- Set `max_workers`

</v-clicks>



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

- Thread overhead greater than unit of work
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
- Managed with locks
- The GIL protected against many data races

</v-clicks>


---
class: history
---

# Data Races: In-Place Summation

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

# Data Races: In-Place Summation

```bash{1-2|4-5|7-8}
$ ~/.env314/bin/python ex.py
Expected: 800,000, Found: 800,000

$ ~/.env314t/bin/python ex.py
Expected: 800,000, Found: 209,515

$ ~/.env314t/bin/python ex.py
Expected: 800,000, Found: 207,052
```

<!-- reading, computing, and writing are not not atomic;
multiple threads will read the same source value and calculate the same result
four-way lost-update collision
worst case would 100,000: maximally synchronized collision
 -->


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

- The GIL can be reenabled
- Your code might run under `python3.14` instead of `python3.14t`
- Threading with the GIL can degrade performance

</v-clicks>


---
class: history
---

# Dynamic Threading Engagement

<v-clicks depth=2>

- Check the GIL state before threading
- Two approaches
    - `sys._is_gil_enabled()`
    - `conditional-futures`: `ConditionalThreadPoolExecutor`

</v-clicks>



---
class: history
---

# `sys._is_gil_enabled()`

```python{1-2|4-6|4-}
array = np.arange(100_000_000).reshape(10_000, 10_000)
def f(row): return (row[row % 2 == 0]**2).sum()

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

- One implementation for both cases
- If GIL is active uses single-thread, else `ThreadPoolExecutor`
- A fully compatible `Executor` subclass
- `pip install conditional-futures`

</v-clicks>




---
class: history
---

# `ConditionalThreadPoolExecutor`

```python{1|3-4|6-}
from conditional_futures import ConditionalThreadPoolExecutor

array = np.arange(100_000_000).reshape(10_000, 10_000)
def f(row): return (row[row % 2 == 0]**2).sum()

with ConditionalThreadPoolExecutor() as ex:
    x = np.fromiter(ex.map(f, array), dtype=float, count=array.shape[0])
```




---

# Talk to Your Agents about Concurrency

<v-clicks depth=2>

- My agents often implement serial first
- `python`
    - I/O bound processes
    - Well-known case of threading benefit even with GIL
- `rust`
    - CPU-bound loop
    - Trivial enhancement with `rayon` parallel iterators
- Review and ask
- Agents can rapidly benchmark alternatives

</v-clicks>




---

# Conclusions

<v-clicks depth=2>

- Multi-threading arrays: a pathological case
- Adoption can be difficult
- Growing package support
    - Tracking top 360: https://hugovk.dev/free-threaded-wheels
    - 217 of 360
- Free-threading is the future

</v-clicks>


<!-- Hugo van Kemenade -->



---
layout: center
class: text-center
---

# Thank You

https://flexatone.net

<!-- <PoweredBySlidev mt-10 /> -->
