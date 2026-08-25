"""Example workflow for futures momentum analysis."""

import pandas as pd

from src.returns import calculate_returns
from src.momentum import (
    rank_by_momentum,
    select_winners_and_losers,
    construct_long_short_weights,
)
from src.performance import performance_summary


def main():
    # Example futures price data
    data = pd.DataFrame({
        "time": [
            "2026-01-01", "2026-01-02", "2026-01-03",
            "2026-01-01", "2026-01-02", "2026-01-03",
            "2026-01-01", "2026-01-02", "2026-01-03",
            "2026-01-01", "2026-01-02", "2026-01-03",
        ],
        "symbol": [
            "A", "A", "A",
            "B", "B", "B",
            "C", "C", "C",
            "D", "D", "D",
        ],
        "close": [
            100, 102, 105,
            100, 101, 102,
            100, 99, 97,
            100, 98, 95,
        ],
    })

    # Step 1: Calculate returns
    returns = calculate_returns(data)

    # Step 2: Rank contracts by momentum
    ranking = rank_by_momentum(returns.dropna())

    # Step 3: Select winners and losers
    winners, losers = select_winners_and_losers(
        ranking,
        n_winners=1,
        n_losers=1,
    )

    # Step 4: Construct long-short portfolio weights
    weights = construct_long_short_weights(
        winners,
        losers,
    )

    print("Momentum ranking:")
    print(ranking)

    print("\nWinners:", winners)
    print("Losers:", losers)

    print("\nPortfolio weights:")
    print(weights)

    # Example portfolio returns for performance evaluation
    portfolio_returns = pd.Series([
        0.01,
        -0.005,
        0.012,
        0.004,
        -0.003,
        0.008,
    ])

    summary = performance_summary(
        portfolio_returns,
        periods_per_year=52,
    )

    print("\nPerformance summary:")
    print(summary)


if __name__ == "__main__":
    main()
