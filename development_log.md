# Institutional FX CTA Development Log

---

# 2026-06-02

## Initial Project Setup

Created:

* deep-research-report.md
* roadmap.md
* architecture.md
* current_status.md
* development_log.md

Purpose:

Establish a persistent project memory system independent of ChatGPT conversation history.

---

## Architectural Decision #001

Decision:

Use layered architecture.

```text
core
↓
data
↓
signals
↓
portfolio
↓
risk
↓
execution
```

Reason:

* Clear dependency direction
* Easier testing
* Easier maintenance
* Lower coupling

Status:

Accepted

---

## Architectural Decision #002

Decision:

Freeze interfaces before implementing strategy logic.

Reason:

Changing interfaces later causes cascading refactoring across all modules.

Status:

Accepted

---

## Architectural Decision #003

Decision:

Develop system incrementally using roadmap tasks.

Reason:

The complete system is too large for a single implementation cycle.

Incremental delivery allows:

* code review
* testing
* validation
* controlled growth

Status:

Accepted

---

## Architectural Decision #004

Decision:

Use GitHub documents as project memory.

Source Documents:

```text
deep-research-report.md
roadmap.md
architecture.md
current_status.md
development_log.md
```

Reason:

ChatGPT conversation memory is temporary.

Project documents provide durable context across development sessions.

Status:

Accepted

---

# Future Entries

Every major decision should be recorded using the following template:

```text
Date:

Decision:

Reason:

Alternatives Considered:

Impact:

Status:
```

---

End of Document
