---
name: Bug report
about: Create a report to help us improve
title: "[BUG]"
labels: ''
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Desktop (please complete the following information):**
 - OS: [e.g. iOS]
 - duckduckgo_search version [e.g. 3.0.0]

**Additional context**
Run this code and show results, change text() to the function that is causing the problem
```python
import logging
from duckduckgo_search import DDGS

logging.basicConfig(level=logging.DEBUG)

for r in DDGS().text("something"):
    pass
```
