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
But when aspect of Python performance remained hard to justify: no true CPU concurrency
And frankly, it was embarrassing!
-->




---
class: history
---

# Embarrassingly Parallel Operations

<v-clicks depth=2>

- Embarrassing because no dependencies between tasks
- Independent processing on collections of data
    - Applying the same function to numerous files or images
    - Processing numerous simulations scenarios
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

# GIL-Bound Threading

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

# Free-Threading

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

# The GIL

<v-clicks depth=2>

- The GIL ensured no data races
- Only one thread could execute bytecode at time
- Over a decade of work to remove the GIL has succeeded
- "No GIL" is "free-threaded"

</v-clicks>



---
class: history
---

# The Journey to No-GIL

<v-clicks depth=2>

- Thread-safe reference counting
    - Per-thread, deferred, biased ref counts
    - Immortal objects
- Built-in locking in containers
- A new memory allocator (mimalloc)
- Garbage collection synchronization

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

# Free-threading is the greatest enhancement to Python performance





---
class: history
---

# Why I Care

<v-clicks depth=2>

- Lots of CPU-bound processing
- Lots of column or row wise calculations
- Multiprocessing overhead would overwhelm concurrency benefits

</v-clicks>

---
class: history
---

# Why You Should Care

<v-clicks depth=2>

- Free-threading offers the quickest path to material better performance
- Easy to use

</v-clicks>


---
class: history
---

# Why NumPy

<v-clicks depth=2>

- Example of processing NumPy 2D arrays generalize
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

- Two different binaries available
    - Python.org
    - homebrew: `brew install python-freethreading`
    - apt:
        ```bash
        sudo add-apt-repository ppa:deadsnakes/ppa
        sudo apt update
        sudo apt install python3.14-nogil
        ```
- Compiling Python with `--disable-gil`

</v-clicks>


---
class: history
---

# Running

<v-clicks depth=2>

- `python3.14t`
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
- Native Python package / wheel are always compatible
- Importing non-compatible wheels will re-enable the GIL

</v-clicks>



---
class: history
---

# Building Free-Threading Compatible C-Extensions

<v-clicks depth=2>

- `Py_GIL_DISABLED`: constant for discovery runtime type
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
- More threads can degrade performance
- Executor `map()` processes one function with many args

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
- NumPy arrays can be made immutable
    - `flags.writeable`
- Immutability makes data races impossible

</v-clicks>


---
class: mitigation
---

# Using `ThreadPoolExecutor` with 2D arrays

<v-clicks depth=2>

- `ThreadPoolExecutor.map()` of 1D arrays
- `numpy.from_iter()` to build 1D array
- Processing rows into a 2D array
- Processing rows into other PyObjects

</v-clicks>


---
class: mitigation
---

# Configuring Worker Counts

<v-clicks depth=2>

- More threads can do more work per wall time
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

- Thread execution indeterminacy
- In-place mutation

</v-clicks>



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

# Conclusions

<v-clicks depth=2>

- Free-threading is no-longer experimental
- Growing package support
    ― PyPI classifier: "Programming Language :: Python :: Free Threading"
    ― Tracking top 360: https://hugovk.github.io/free-threaded-wheels/
- Adoption can be difficult

</v-clicks>



---
layout: center
class: text-center
---

# Thank You

https://flexatone.net

<!-- <PoweredBySlidev mt-10 /> -->
