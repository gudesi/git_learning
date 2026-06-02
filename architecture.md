# Institutional FX CTA Architecture

Version: 1.0

---

# 1. Purpose

This document defines the permanent architecture of the Institutional FX CTA Trading System.

The objective is to provide a stable reference for future development and prevent architectural drift.

This document is considered the source of truth for:

* Project structure
* Module boundaries
* Core domain models
* Dependency rules
* Data flow

Any architectural change should be documented here before implementation.

---

# 2. Architectural Principles

The system follows the following principles:

1. Single Responsibility Principle
2. Explicit Interfaces
3. Dependency Direction Only Flows Downward
4. No Circular Dependencies
5. Pure Business Logic Separated From Infrastructure
6. Deterministic Calculations
7. Testable Components
8. Long-Term Maintainability

---

# 3. Target Architecture

```text
git_learning/

├── core/
├── data/
├── signals/
├── portfolio/
├── risk/
├── execution/
├── backtest/
├── monitoring/
├── strategies/
├── tests/
└── main.py
```

---

# 4. Layer Responsibilities

## core

Shared definitions.

Contains:

* models
* enums
* constants
* configuration

Must not depend on any other project module.

---

## data

Market data access and feature generation.

Contains:

* market data providers
* MT5 adapters
* return calculations
* volatility estimators
* covariance calculations

Depends on:

```text
core
```

---

## signals

Signal generation layer.

Contains:

* Direction Score
* Momentum Score
* Trend Quality
* Risk Adjusted Momentum
* Final Score

Depends on:

```text
core
data
```

---

## portfolio

Portfolio construction layer.

Contains:

* candidate selection
* ranking
* target weight generation

Depends on:

```text
core
signals
```

---

## risk

Portfolio risk management.

Contains:

* position risk
* volatility targeting
* risk contribution
* currency exposure
* drawdown control

Depends on:

```text
core
portfolio
```

---

## execution

Execution and order management.

Contains:

* position sizing
* order management
* MT5 execution adapter
* stop management

Depends on:

```text
core
risk
```

---

## backtest

Historical simulation framework.

Contains:

* simulation engine
* walk-forward testing
* stress testing

Depends on:

```text
core
signals
portfolio
risk
execution
```

---

## monitoring

Monitoring and reporting.

Contains:

* dashboards
* reports
* alerts

Depends on:

```text
core
risk
execution
```

---

## strategies

Top-level orchestration layer.

Coordinates:

```text
Data
→ Signals
→ Portfolio
→ Risk
→ Execution
```

---

# 5. Core Domain Models

The following domain models are considered foundational.

## Instrument

Represents a tradeable FX instrument.

---

## Bar

Represents a daily OHLCV record.

---

## Signal

Represents a directional trading signal.

---

## Candidate

Represents a ranked portfolio candidate.

---

## Position

Represents an open position.

---

## Order

Represents an executable order.

---

## PortfolioState

Represents current portfolio state.

---

## RiskReport

Represents portfolio risk metrics.

---

# 6. Dependency Rules

Allowed:

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

Forbidden:

```text
execution → signals
execution → data

risk → signals

portfolio → execution
```

No module may import upward.

---

# 7. Daily Processing Pipeline

```text
Market Data
    ↓
Feature Generation
    ↓
Signal Generation
    ↓
Candidate Selection
    ↓
Portfolio Construction
    ↓
Risk Validation
    ↓
Execution Plan
    ↓
Order Submission
    ↓
Monitoring
```

---

# 8. Architectural Change Policy

Any change affecting:

* core models
* dependency rules
* data flow
* risk framework

must be documented in this file before implementation.

---