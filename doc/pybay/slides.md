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
Yes, its some operations are slow, but we get have such readability and flexability
Yes, numerical ops are also slow but we have access to excellent C-libraries like NumPy and Arrow
But when aspect of Python performance remained hard to justify: no true CPU concurrency
-->







---
class: history
---

# Risks of Python Package Installation

<v-clicks depth=2>

- Arbitrary Code Execution (ACE)
- Your privileges are enough
- Transitive dependencies increase complexity

</v-clicks>



---
class: history
---

# Origins of Package-Based Attacks

<v-clicks depth=2>

- Compromised maintainer credentials
    - Injection of malicious code (trojan, hijacking)
    - Addition of a malicious dependency (e.g. Axios)
- Typosquatting & Masquerading
    - `requesuts`, `grokwrapper`
- Dependency confusion (e.g. PyTorch `torchtriton`)
- Social Engineering
    - Fake recruiters, fake IT support

</v-clicks>


---
class: history
---

# Why I Care

<v-clicks depth=2>

- Supply chain risks in my organization
- Recognition that no controls are foolproof
- Developed system-wide Python vulnerability scanner `fetter`

</v-clicks>

---
class: history
---

# Why You Should Care

<v-clicks depth=2>

- Users are gateways into organizations
- Credential & API key theft can have severe consequences
- Practical mitigations are available

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
    - homebrew
- Compiling Python with `--disable-gil`

</v-clicks>


---
class: history
---

# Running

<v-clicks depth=2>

- `python3.14t`
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
― Configurable worker counts
    - More threads can degrade performance
- Executor `map()` processes one function with many args
```python
    with ThreadPoolExecutor() as ex:
        result = list(ex.map(f, args))
```

</v-clicks>




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

- `ThreadPoolExecutor.map()`
- `numpy.from_iter()`
― Processing rows into a 2D array
― Processing rows into other PyObjects

</v-clicks>






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
