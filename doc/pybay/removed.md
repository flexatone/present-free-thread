

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





---
class: mitigation
---

# Per-row `sum()` 1e6

<img class="plot" src="/images/ft-np-perf-sum-1e6.png" />




---
class: mitigation
---

# Per-row `max(Counter())` 1e6

<img class="plot" src="/images/ft-np-perf-counter-1e6.png" />





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

# Free-Threading C-Extensions: Stable ABI (`abi3t`)


- `PyModExport_*()`: new entry point returning slots (PEP 793, 3.15)
- One binary for GIL and free-threaded builds (PEP 803)
```c {10-11|3-9|1-2,4|7}
#define Py_TARGET_ABI3T 0x30f0000 // target abi3t for 3.15+
PyABIInfo_VAR(abi_info);
static PySlot slots[] = {
    PySlot_STATIC_DATA(Py_mod_abi, &abi_info),
    PySlot_STATIC_DATA(Py_mod_name, "mymodule"),
    PySlot_FUNC(Py_mod_exec, mymodule_exec),
    PySlot_DATA(Py_mod_gil, Py_MOD_GIL_NOT_USED),
    PySlot_END
};
PyMODEXPORT_FUNC
PyModExport_mymodule(void) { return slots; }
```

<!-- Py_TARGET_ABI3T is defined before #include <Python.h>; wheel tag abi3.abi3t -->

