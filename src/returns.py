"""Return calculations for futures price data."""

import numpy as np
import pandas as pd


def prepare_price_data(
    data: pd.DataFrame,
    time_col: str = "time",
    symbol_col: str = "symbol",
    price_col: str = "close",
) -> pd.DataFrame:
    """
    Validate and sort futures price data before return calculation.

    Parameters
    ----------
    data : pd.DataFrame
        Futures price data.
    time_col : str
        Name of the timestamp column.
    symbol_col : str
        Name of the futures symbol column.
    price_col : str
        Name of the price column.

    Returns
    -------
    pd.DataFrame
        Cleaned and chronologically sorted price data.
    """

    required_columns = {time_col, symbol_col, price_col}
    missing_columns = required_columns.difference(data.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    result = data.copy()

    result[time_col] = pd.to_datetime(result[time_col])
    result[price_col] = pd.to_numeric(result[price_col], errors="coerce")

    result = result.dropna(
        subset=[time_col, symbol_col, price_col]
    )

    result = result.sort_values(
        [symbol_col, time_col]
    ).reset_index(drop=True)

    return result


def calculate_returns(
    data: pd.DataFrame,
    time_col: str = "time",
    symbol_col: str = "symbol",
    price_col: str = "close",
) -> pd.DataFrame:
    """
    Calculate simple, gross, and log returns for each futures series.

    Simple return:
        P_t / P_(t-1) - 1

    Gross return:
        P_t / P_(t-1)

    Log return:
        log(P_t / P_(t-1))
    """

    result = prepare_price_data(
        data=data,
        time_col=time_col,
        symbol_col=symbol_col,
        price_col=price_col,
    )

    previous_price = result.groupby(symbol_col)[price_col].shift(1)

    result["simple_return"] = (
        result[price_col] / previous_price - 1
    )

    result["gross_return"] = (
        result[price_col] / previous_price
    )

    result["log_return"] = np.log(
        result[price_col] / previous_price
    )

    return result
