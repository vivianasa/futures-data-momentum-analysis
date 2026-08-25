"""Utilities for loading and resampling futures price data."""

import os

import pandas as pd
import pyodbc


def create_connection():
    """Create a database connection using environment variables."""

    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    if not all([server, database, username, password]):
        raise ValueError(
            "Database credentials must be supplied through environment variables."
        )

    connection_string = (
        "DRIVER={SQL Server};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password}"
    )

    return pyodbc.connect(connection_string)


def resample_prices(data: pd.DataFrame, frequency: str = "D") -> pd.DataFrame:
    """
    Resample futures price data and retain the final observation
    within each period.
    """

    return data.resample(frequency).last().dropna()
