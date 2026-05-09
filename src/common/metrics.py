"""
Common metrics for forecasting & inventory evaluation.

Main targets:
- WAPE, MASE for forecasting.
- Fill-rate, stockout days, total cost for inventory/ops.
"""

from typing import Iterable, Sequence

import numpy as np


def wape(y_true: Sequence[float], y_pred: Sequence[float]) -> float:
    y_true_arr = np.asarray(y_true, dtype=float)
    y_pred_arr = np.asarray(y_pred, dtype=float)
    denom = np.sum(np.abs(y_true_arr))
    if denom == 0:
        return 0.0
    return float(np.sum(np.abs(y_true_arr - y_pred_arr)) / denom)


def mase(
    y_true: Sequence[float],
    y_pred: Sequence[float],
    insample: Iterable[float],
    m: int = 1,
) -> float:
    """
    Mean Absolute Scaled Error (MASE).

    Parameters
    ----------
    y_true, y_pred : Sequence[float]
        Out-of-sample actual & forecast.
    insample : Iterable[float]
        In-sample series to calculate naive seasonal error.
    m : int
        Seasonal period (e.g., 1 for naive, 7/52 for seasonal).
    """
    y_true_arr = np.asarray(y_true, dtype=float)
    y_pred_arr = np.asarray(y_pred, dtype=float)

    insample_arr = np.asarray(list(insample), dtype=float)
    if len(insample_arr) <= m:
        # fallback: if insample is too short, return WAPE-like
        return wape(y_true_arr, y_pred_arr)

    naive_err = np.abs(insample_arr[m:] - insample_arr[:-m]).mean()
    if naive_err == 0:
        return 0.0
    return float(np.mean(np.abs(y_true_arr - y_pred_arr)) / naive_err)


