import numpy as np
import pandas as pd
import pytest

from src.returns import calculate_returns, prepare_price_data


def test_prepare_price_data_sorts_and_cleans_input():
    data = pd.DataFrame(
        {
            "time": ["2026-01-02", "2026-01-01", "2026-01-01"],
            "symbol": ["A", "A", "B"],
            "close": [102, 100, "50"],
        }
    )

    result = prepare_price_data(data)

    assert result["symbol"].tolist() == ["A", "A", "B"]
    assert result["close"].tolist() == [100, 102, 50]
    assert pd.api.types.is_datetime64_any_dtype(result["time"])


def test_calculate_returns_computes_each_return_definition():
    data = pd.DataFrame(
        {
            "time": ["2026-01-01", "2026-01-02", "2026-01-01", "2026-01-02"],
            "symbol": ["A", "A", "B", "B"],
            "close": [100, 110, 50, 45],
        }
    )

    result = calculate_returns(data)

    a_second = result[(result["symbol"] == "A") & result["simple_return"].notna()].iloc[0]
    b_second = result[(result["symbol"] == "B") & result["simple_return"].notna()].iloc[0]

    assert a_second["simple_return"] == pytest.approx(0.10)
    assert a_second["gross_return"] == pytest.approx(1.10)
    assert a_second["log_return"] == pytest.approx(np.log(1.10))

    assert b_second["simple_return"] == pytest.approx(-0.10)
    assert b_second["gross_return"] == pytest.approx(0.90)
    assert b_second["log_return"] == pytest.approx(np.log(0.90))


def test_prepare_price_data_rejects_missing_columns():
    data = pd.DataFrame({"time": ["2026-01-01"], "symbol": ["A"]})

    with pytest.raises(ValueError, match="Missing required columns"):
        prepare_price_data(data)
