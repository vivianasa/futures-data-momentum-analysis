import numpy as np
import pandas as pd
import pytest

from src.performance import (
    annualized_return,
    annualized_volatility,
    calculate_nav,
    historical_var,
    max_drawdown,
    performance_summary,
    sharpe_ratio,
)


def test_calculate_nav_compounds_simple_returns():
    returns = pd.Series([0.10, -0.05, 0.02])

    nav = calculate_nav(returns)

    expected = pd.Series([1.10, 1.045, 1.0659])
    pd.testing.assert_series_equal(nav.reset_index(drop=True), expected)


def test_max_drawdown_matches_peak_to_trough_decline():
    nav = pd.Series([1.0, 1.2, 0.9, 1.1])

    result = max_drawdown(nav)

    assert result == pytest.approx(0.25)


def test_historical_var_is_reported_as_positive_loss():
    returns = pd.Series([-0.10, -0.03, 0.00, 0.02, 0.04])

    result = historical_var(returns, confidence_level=0.80)

    assert result == pytest.approx(0.044)


def test_sharpe_ratio_is_nan_for_zero_volatility():
    returns = pd.Series([0.01, 0.01, 0.01])

    result = sharpe_ratio(returns)

    assert np.isnan(result)


def test_performance_summary_contains_core_metrics():
    returns = pd.Series([0.01, -0.005, 0.012, 0.004, -0.003, 0.008])

    summary = performance_summary(returns)

    expected_metrics = {
        "Annualized Return",
        "Annualized Volatility",
        "Sharpe Ratio",
        "Sortino Ratio",
        "Maximum Drawdown",
        "95% Historical VaR",
    }
    assert set(summary.index) == expected_metrics
