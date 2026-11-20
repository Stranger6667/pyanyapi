---
name: Bug report
about: Create a report to help us improve
title: "[BUG]"
labels: 'Status: Review Needed, Type: Bug'
assignees: Stranger6667

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
A minimal snippet that reproduces the problem, and the full traceback if there is one.

```python
from pyanyapi.parsers import JSONParser

api = JSONParser({"value": "container > value"}).parse('{"container": {"value": 1}}')
```

**Expected behavior**
A clear and concise description of what you expected to happen.

**Environment (please complete the following information):**

- OS: [e.g. Linux or Windows]
- Python version: [e.g. 3.13.1]
- lxml version: [e.g. 6.1.3]
- PyYAML version: [e.g. 6.0.3]
- PyAnyAPI version: [e.g. 1.0.0]

**Additional context**
Add any other context about the problem here.
