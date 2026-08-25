"""Performance and risk metrics for momentum portfolios."""

import numpy as np
import pandas as pd


def calculate_nav(
    returns: pd.Series,
    initial_nav: float = 1.0,
) -> pd.Series:
    """
    Calculate the cumulative net asset value (NAV).

    Parameters
    ----------
    returns : pd.Series
        Periodic simple returns.
    initial_nav : float
        Initial portfolio NAV.

    Returns
    -------
    pd.Series
        Cumulative NAV series.
    """

    clean_returns = returns.dropna().astype(float)

    return initial_nav * (1 + clean_returns).cumprod()


def annualized_return(
    returns: pd.Series,
    periods_per_year: int = 52,
) -> float:
    """Calculate annualized compound return."""

    clean_returns = returns.dropna().astype(float)

    if clean_returns.empty:
        return np.nan

    total_growth = (1 + clean_returns).prod()
    n_periods = len(clean_returns)

    return total_growth ** (periods_per_year / n_periods) - 1


def annualized_volatility(
    returns: pd.Series,
    periods_per_year: int = 52,
) -> float:
    """Calculate annualized return volatility."""

    clean_returns = returns.dropna().astype(float)

    return clean_returns.std(ddof=1) * np.sqrt(periods_per_year)


def sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    periods_per_year: int = 52,
) -> float:
    """Calculate the annualized Sharpe ratio."""

    clean_returns = returns.dropna().astype(float)

    volatility = annualized_volatility(
        clean_returns,
        periods_per_year,
    )

    if volatility == 0 or np.isnan(volatility):
        return np.nan

    mean_return = clean_returns.mean() * periods_per_year

    return (mean_return - risk_free_rate) / volatility


def sortino_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    periods_per_year: int = 52,
) -> float:
    """Calculate the annualized Sortino ratio."""

    clean_returns = returns.dropna().astype(float)
    downside_returns = clean_returns[clean_returns < 0]

    if downside_returns.empty:
        return np.nan

    downside_deviation = (
        downside_returns.std(ddof=1)
        * np.sqrt(periods_per_year)
    )

    if downside_deviation == 0 or np.isnan(downside_deviation):
        return np.nan

    mean_return = clean_returns.mean() * periods_per_year

    return (mean_return - risk_free_rate) / downside_deviation


def max_drawdown(nav: pd.Series) -> float:
    """
    Calculate maximum drawdown from a NAV series.

    Returns a positive number representing the largest
    peak-to-trough decline.
    """

    clean_nav = nav.dropna().astype(float)

    if clean_nav.empty:
        return np.nan

    running_max = clean_nav.cummax()
    drawdown = clean_nav / running_max - 1

    return abs(drawdown.min())


def historical_var(
    returns: pd.Series,
    confidence_level: float = 0.95,
) -> float:
    """
    Calculate historical Value at Risk (VaR).

    The returned value is expressed as a positive loss.
    """

    clean_returns = returns.dropna().astype(float)

    if clean_returns.empty:
        return np.nan

    quantile = clean_returns.quantile(1 - confidence_level)

    return max(0.0, -quantile)


def performance_summary(
    returns: pd.Series,
    periods_per_year: int = 52,
    risk_free_rate: float = 0.0,
) -> pd.Series:
    """Generate a summary of portfolio performance metrics."""

    nav = calculate_nav(returns)

    return pd.Series({
        "Annualized Return": annualized_return(
            returns,
            periods_per_year,
        ),
        "Annualized Volatility": annualized_volatility(
            returns,
            periods_per_year,
        ),
        "Sharpe Ratio": sharpe_ratio(
            returns,
            risk_free_rate,
            periods_per_year,
        ),
        "Sortino Ratio": sortino_ratio(
            returns,
            risk_free_rate,
            periods_per_year,
        ),
        "Maximum Drawdown": max_drawdown(nav),
        "95% Historical VaR": historical_var(
            returns,
            confidence_level=0.95,
        ),
    })
