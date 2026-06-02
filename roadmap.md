# Institutional FX CTA System Development Roadmap

**Version:** 1.0  
**Status:** Architecture Baseline  
**Purpose:** Define a complete development roadmap for implementing the strategy described in `deep-research-report.md`.

---

## 1. Project Objective

The goal of this project is to transform the research report into a fully functional institutional-grade FX CTA trading system.

The system must:

- Trade long and short.
- Operate on daily data.
- Support portfolio-level risk management.
- Support volatility targeting.
- Support cross-sectional momentum ranking.
- Support trend quality filtering.
- Support currency exposure control.
- Support portfolio construction and execution.
- Support backtesting and future live trading deployment.
- Remain maintainable and extensible over the long term.

The development process should prioritize:

1. Correct architecture.
2. Clear module boundaries.
3. Stable interfaces.
4. Incremental implementation.
5. Minimal future refactoring.

---

## 2. Development Philosophy

The project will be developed using a layered architecture.

**Development order:**
Architecture
↓
Domain Models
↓
Data Layer
↓
Signal Layer
↓
Portfolio Layer
↓
Risk Layer
↓
Execution Layer
↓
Backtesting Layer
↓
Monitoring Layer


**Key principle:**

> Freeze interfaces first, then implement logic.

This minimizes future redesign and allows every module to be developed independently.

---

## 3. Target Architecture

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

---

## 4. Layer Responsibilities

### 4.1 Core Layer

**Purpose:** Provide shared definitions used across the entire system.

**Contains:**

- Instrument
- Bar
- Signal
- Position
- Order
- PortfolioState
- RiskReport
- Enums, Constants, Configurations

**Rules:**

- No trading logic.
- No MT5 dependency.
- No external broker dependency.

---

### 4.2 Data Layer

**Purpose:** Provide clean and consistent market data.

**Responsibilities:**

- Historical Data Retrieval
- Market Data Validation
- Return Calculation
- Volatility Estimation
- ATR Calculation
- Covariance Matrix Calculation

**Outputs:** Prices, Returns, Features

---

### 4.3 Signal Layer

**Purpose:** Generate directional and ranking signals.

**Components:**

- **Direction Score:** R3M, R6M, R12M
- **Momentum Score:** Cross-sectional momentum ranking
- **Trend Quality:** Regression Slope, R²
- **Risk Adjusted Momentum:** Momentum / Volatility
- **Final Score:**  
  `0.8 × RiskAdjustedMomentum + 0.2 × TrendQuality`

**Outputs:** Long Candidates, Short Candidates, Final Rankings

---

### 4.4 Portfolio Layer

**Purpose:** Convert signals into target portfolios.

**Responsibilities:**

- Candidate Selection
- Ranking
- Portfolio Construction
- Target Weights

**Outputs:** Target Portfolio

---

### 4.5 Risk Layer

**Purpose:** Control risk at every level.

**Components:**

- Position Risk
- Portfolio Volatility (Target Volatility)
- Risk Contribution
- Currency Exposure (USD, EUR, JPY, GBP, CHF, AUD, NZD, CAD)
- Correlation Cluster Control
- Drawdown Control (Level 1, 2, 3, Emergency Stop)

**Outputs:** Risk Approved Portfolio

---

### 4.6 Execution Layer

**Purpose:** Transform portfolio decisions into executable orders.

**Responsibilities:**

- Position Sizing
- Order Creation
- Order Tracking
- Position Synchronization
- Stop Management
- Pyramiding
- Exit Logic

**Outputs:** Execution Plan, Orders

---

### 4.7 Backtest Layer

**Purpose:** Validate strategy performance.

**Responsibilities:**

- Historical Simulation
- Walk Forward Analysis
- Stress Testing
- Transaction Cost Modeling

**Outputs:** Performance Metrics

---

### 4.8 Monitoring Layer

**Purpose:** Provide operational visibility.

**Responsibilities:**

- Risk Monitoring
- Exposure Monitoring
- Drawdown Monitoring
- Trade Monitoring
- Alert Generation

**Outputs:** Reports, Dashboards, Alerts

---

## 5. Development Roadmap

Each milestone should be completed, tested, committed, and reviewed before moving to the next stage.

---

### Phase 0 — Architecture Freeze

**Task 1:** Project Architecture Design  
**Deliverables:** `Architecture.md`, Directory Structure, Dependency Rules  
**Status:** Completed

---

### Phase 1 — Domain Foundation

**Task 2:** Core Models — `core/models.py`  
**Objects:** Instrument, Bar, Signal, Candidate, Position, Order, PortfolioState, RiskReport

**Task 3:** Configuration System — `core/config.py`, `core/constants.py`, `core/enums.py`

---

### Phase 2 — Data Infrastructure

**Task 4:** Market Data Interface — `data/provider.py`  
**Task 5:** MT5 Data Adapter — `data/mt5_provider.py`  
**Task 6:** Feature Engineering — `data/features.py` (Returns, ATR, EWMA Volatility, Rolling Covariance)

---

### Phase 3 — Signal Engine

**Task 7:** Direction Score — `signals/direction.py`  
**Task 8:** Momentum Score — `signals/momentum.py`  
**Task 9:** Trend Quality — `signals/trend_quality.py`  
**Task 10:** Risk Adjusted Momentum — `signals/risk_adjusted_momentum.py`  
**Task 11:** Final Score Engine — `signals/final_score.py`

---

### Phase 4 — Portfolio Construction

**Task 12:** Candidate Pool Generator — `portfolio/candidate_pool.py`  
**Task 13:** Portfolio Builder — `portfolio/builder.py`

---

### Phase 5 — Risk Engine

**Task 14:** Position Risk Model — `risk/position_risk.py`  
**Task 15:** Volatility Targeting — `risk/volatility_target.py`  
**Task 16:** Risk Contribution Model — `risk/risk_contribution.py`  
**Task 17:** Currency Exposure Control — `risk/currency_exposure.py`  
**Task 18:** Correlation Cluster Management — `risk/clusters.py`  
**Task 19:** Drawdown Protection — `risk/drawdown.py`

---

### Phase 6 — Execution Engine

**Task 20:** Order Models — `execution/orders.py`  
**Task 21:** Position Sizing — `execution/position_sizing.py`  
**Task 22:** Trade State Machine — `execution/state_machine.py`  
**Task 23:** MT5 Execution Adapter — `execution/mt5_executor.py`

---

### Phase 7 — Backtesting

**Task 24:** Backtest Engine — `backtest/engine.py`  
**Task 25:** Walk Forward Framework — `backtest/walk_forward.py`  
**Task 26:** Stress Testing Framework — `backtest/stress_test.py`

---

### Phase 8 — Monitoring

**Task 27:** Monitoring Models — `monitoring/models.py`  
**Task 28:** Monitoring Reports — `monitoring/reporting.py`  
**Task 29:** Alert System — `monitoring/alerts.py`

---

### Phase 9 — System Integration

**Task 30:** Strategy Orchestrator — `strategies/cta_strategy.py`  
**Pipeline:** Market Data → Features → Signals → Portfolio → Risk → Execution Plan → Orders

**Task 31:** Application Entry Point — `main.py`  
**Task 32:** Integration Testing — `tests/` (End-to-End Simulation, Portfolio Validation, Risk Validation, Execution Validation)

---

## 6. Development Rules

Every new module must satisfy:

1. Single Responsibility Principle.
2. No circular dependencies.
3. Pure business logic separated from infrastructure.
4. Deterministic outputs.
5. Unit-testable design.
6. Explicit input/output interfaces.
7. No hidden global state.
8. No duplicated business logic.

---

## 7. Definition of Completion

The project is considered complete when:

- Daily signal generation works.
- Portfolio construction works.
- Risk controls work.
- Position sizing works.
- MT5 execution works.
- Historical backtesting works.
- Monitoring works.
- End-to-end integration tests pass.

At that point the system will represent a complete implementation of the strategy described in `deep-research-report.md`.