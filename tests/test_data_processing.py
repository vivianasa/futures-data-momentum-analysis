import pandas as pd

from src.data_processing import resample_prices


def test_resample_prices_keeps_last_observation_in_each_period():
    data = pd.DataFrame(
        {"close": [100, 102, 103, 105]},
        index=pd.to_datetime(
            [
                "2026-01-01 09:00",
                "2026-01-01 16:00",
                "2026-01-02 09:00",
                "2026-01-02 16:00",
            ]
        ),
    )

    result = resample_prices(data, frequency="D")

    assert result["close"].tolist() == [102, 105]
