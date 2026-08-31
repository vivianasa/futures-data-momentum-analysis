import pandas as pd
import pytest

from src.momentum import (
    construct_long_short_weights,
    rank_by_momentum,
    select_winners_and_losers,
)


def test_rank_by_momentum_orders_contracts_by_average_return():
    returns = pd.DataFrame(
        {
            "symbol": ["A", "A", "B", "B", "C", "C"],
            "log_return": [0.02, 0.03, -0.01, 0.00, 0.01, 0.01],
        }
    )

    ranking = rank_by_momentum(returns)

    assert ranking["symbol"].tolist() == ["A", "C", "B"]
    assert ranking["rank"].tolist() == [1, 2, 3]


def test_select_winners_and_losers_returns_extreme_rankings():
    ranking = pd.DataFrame(
        {
            "symbol": ["A", "B", "C", "D"],
            "momentum_signal": [0.4, 0.2, -0.1, -0.3],
            "rank": [1, 2, 3, 4],
        }
    )

    winners, losers = select_winners_and_losers(
        ranking,
        n_winners=1,
        n_losers=1,
    )

    assert winners == ["A"]
    assert losers == ["D"]


def test_construct_long_short_weights_is_balanced():
    weights = construct_long_short_weights(
        winners=["A", "B"],
        losers=["C", "D"],
    )

    assert weights["A"] == pytest.approx(0.5)
    assert weights["B"] == pytest.approx(0.5)
    assert weights["C"] == pytest.approx(-0.5)
    assert weights["D"] == pytest.approx(-0.5)
    assert weights.sum() == pytest.approx(0.0)


def test_select_winners_and_losers_validates_portfolio_size():
    ranking = pd.DataFrame({"symbol": ["A", "B"], "rank": [1, 2]})

    with pytest.raises(ValueError, match="exceed"):
        select_winners_and_losers(ranking, n_winners=2, n_losers=1)
