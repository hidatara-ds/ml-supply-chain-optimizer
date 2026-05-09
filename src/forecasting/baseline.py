"""
Baseline forecasting methods.

Purpose of this module:
- Provide super simple baselines as benchmarks:
  - Naive:          y_hat(t) = y(t-1)
  - Seasonal naive: y_hat(t) = y(t-52)  (for weekly data)

This implementation does not depend on any specific ML framework, only NumPy/Pandas.
"""

from typing import List, Optional, Tuple

import numpy as np
import pandas as pd


def global_naive_forecast(h: int, mean: float, std: float) -> List[float]:
    """
    Global baseline if there is no historical data per SKU-location.
    Similar to assuming constant demand around the mean with a slight bump at the end of the horizon.
    """
    base = np.full(h, mean)
    # simple seasonal-ish bump last steps of horizon
    if h >= 2:
        base[-2:] = mean + 0.5 * std
    return base.clip(min=0).astype(float).tolist()


def naive_and_seasonal_from_history(
    sub: pd.DataFrame,
    h: int,
    mean: float,
    std: float,
) -> Tuple[List[float], Optional[List[float]]]:
    """
    Baseline per SKU-location based on history:

    Parameters
    ----------
    sub : pd.DataFrame
        History for one store_id–product_id combination with columns:
        - 'units_sold'
        - optional: 'lag_52' for weekly seasonal naive.
    h : int
        Forecast horizon (number of steps ahead).
    mean, std : float
        Global fallback statistics if history is insufficient.

    Returns
    -------
    naive : list[float]
        Naive baseline: repeat the last units_sold value for the entire horizon.
    seasonal : Optional[list[float]]
        Seasonal naive (based on lag_52) if available & not NaN, else None.
    """
    if sub is None or len(sub) == 0:
        from .baseline import global_naive_forecast  # local import to avoid cycles

        return global_naive_forecast(h, mean, std), None

    sub_sorted = sub.sort_values(["year", "week"])

    # Naive: last actual value
    last_units = float(sub_sorted["units_sold"].iloc[-1])
    naive = [float(max(0.0, last_units))] * h

    seasonal: Optional[List[float]] = None
    if "lag_52" in sub_sorted.columns:
        val = sub_sorted["lag_52"].iloc[-1]
        if not pd.isna(val):
            seasonal_val = float(val)
            seasonal = [float(max(0.0, seasonal_val))] * h

    return naive, seasonal


