"""Momentum ranking and portfolio construction utilities."""

import pandas as pd


def rank_by_momentum(
    returns: pd.DataFrame,
    symbol_col: str = "symbol",
    return_col: str = "log_return",
    descending: bool = True,
) -> pd.DataFrame:
    """
    Rank futures contracts according to their historical returns.

    Parameters
    ----------
    returns : pd.DataFrame
        Data containing futures symbols and returns.
    symbol_col : str
        Name of the futures symbol column.
    return_col : str
        Return measure used to construct the momentum signal.
    descending : bool
        If True, higher-return contracts receive higher rankings.

    Returns
    -------
    pd.DataFrame
        Average return and momentum rank for each contract.
    """

    required_columns = {symbol_col, return_col}
    missing_columns = required_columns.difference(returns.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    ranking = (
        returns
        .groupby(symbol_col, as_index=False)[return_col]
        .mean()
        .rename(columns={return_col: "momentum_signal"})
    )

    ranking = ranking.sort_values(
        "momentum_signal",
        ascending=not descending,
    ).reset_index(drop=True)

    ranking["rank"] = range(1, len(ranking) + 1)

    return ranking


def select_winners_and_losers(
    ranking: pd.DataFrame,
    n_winners: int = 2,
    n_losers: int = 2,
    symbol_col: str = "symbol",
):
    """
    Select winner and loser portfolios from a momentum ranking.

    Winners are contracts with the strongest historical performance.
    Losers are contracts with the weakest historical performance.
    """

    if n_winners <= 0 or n_losers <= 0:
        raise ValueError(
            "n_winners and n_losers must be positive integers."
        )

    if n_winners + n_losers > len(ranking):
        raise ValueError(
            "The requested winner and loser portfolios exceed "
            "the number of available contracts."
        )

    winners = ranking.head(n_winners)[symbol_col].tolist()
    losers = ranking.tail(n_losers)[symbol_col].tolist()

    return winners, losers


def construct_long_short_weights(
    winners,
    losers,
) -> pd.Series:
    """
    Construct an equally weighted long-short momentum portfolio.

    Winner contracts receive positive weights.
    Loser contracts receive negative weights.
    """

    if not winners or not losers:
        raise ValueError(
            "Both winner and loser portfolios must contain contracts."
        )

    long_weight = 1 / len(winners)
    short_weight = -1 / len(losers)

    weights = {
        symbol: long_weight
        for symbol in winners
    }

    weights.update({
        symbol: short_weight
        for symbol in losers
    })

    return pd.Series(weights, name="weight")
