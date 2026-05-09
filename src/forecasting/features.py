"""
Feature engineering utilities for demand forecasting.

Notes:
- Currently, the original pipeline is still in `etl/build_features.py`.
- This module is prepared as a new home for feature engineering logic
  (e.g., read raw data, weekly aggregation, lag/rolling features, etc.).
"""

from pathlib import Path
from typing import Optional

import pandas as pd


def load_processed_features(path: Path = Path("data/processed/weekly_features.parquet")) -> Optional[pd.DataFrame]:
    """
    Simple helper to read processed features if they exist.
    """
    if not path.exists():
        return None
    return pd.read_parquet(path)


