# Futures Data & Momentum Analysis

A modular Python toolkit for futures data processing, return calculation,
momentum portfolio construction, and performance evaluation.

## Overview

This project provides reusable components for a quantitative research workflow
using futures price data.

The current implementation includes:

- Database connection through environment variables
- Futures price resampling and preprocessing
- Simple, gross, and log return calculations
- Cross-sectional momentum ranking
- Winner and loser portfolio selection
- Equal-weighted long-short portfolio construction
- Portfolio performance and risk evaluation

## Research Workflow

```text
Futures Price Data
        ↓
Data Processing & Resampling
        ↓
Return Calculation
        ↓
Momentum Ranking
        ↓
Winner / Loser Selection
        ↓
Long-Short Portfolio
        ↓
Performance & Risk Evaluation
```

## Repository Structure

```text
futures-data-momentum-analysis/
│
├── README.md
├── .gitignore
│
└── src/
    ├── data_processing.py
    ├── returns.py
    ├── momentum.py
    └── performance.py
```

## Modules

### `data_processing.py`

Utilities for database connection and futures price resampling.

Database credentials are supplied through environment variables rather than
being stored directly in the source code.

### `returns.py`

Prepares futures price data and calculates:

- Simple returns
- Gross returns
- Log returns

### `momentum.py`

Implements the main momentum portfolio construction steps:

- Rank contracts by historical performance
- Select winner and loser portfolios
- Construct equally weighted long-short positions

### `performance.py`

Provides portfolio performance and risk measures, including:

- Net asset value (NAV)
- Annualized return
- Annualized volatility
- Sharpe ratio
- Sortino ratio
- Maximum drawdown
- Historical Value at Risk (VaR)

## Technologies

- Python
- pandas
- NumPy
- pyodbc
- SQL

## Data and Security

The public version of this repository does not contain proprietary datasets,
database credentials, or institution-specific connection details.

Database credentials, when required, are loaded from environment variables.

## Purpose

This repository is a cleaned and modularized version of earlier quantitative
finance work. It is designed to demonstrate a structured workflow for futures
data processing, momentum portfolio construction, and performance analysis.
