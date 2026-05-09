## Problem Contract

This document defines the "problem contract" that serves as the reference for the entire forecasting and replenishment optimizer pipeline in this project.

### A. What are we forecasting?

- **Forecast target**: `demand_qty` (demand / sales quantity) per combination of:
  - **SKU** (product_id)
  - **Location** (store_id)
  - **Time period**: week
- **Horizon**: \(H = 4\) weeks ahead for each SKU–location.
- **Time granularity**: **weekly**, consistent with the horizon and dummy/training data structure.

Operationally, the model will receive a list of `(store_id, product_id)` pairs and return a time series of weekly demand forecasts for the next 4 weeks for each pair.

### B. What is the optimizer output?

- **Main output**: `order_qty` per combination of:
  - SKU
  - Location
  - Period (e.g., weekly order)

- **Objective function (main)**:
  - **Minimize total inventory cost**, which includes:
    - **holding cost**,
    - **stockout / shortage cost**,
    - **ordering cost**,
  - or equivalently achieve a minimum **target service level** with the lowest possible total cost.

Mathematically, the optimizer solves the problem of allocating budget/capacity to SKU–location combinations based on the demand forecast to produce economical ordering decisions (`order_qty`) while still meeting the target service level.

### C. Minimum constraints

The optimizer at least considers (or is ready to be extended to consider) the following constraints:

- **Lead time**:
  - The delay between when an order is placed and when the stock is available at the location.
  - Affects when `order_qty` needs to be placed so that there is enough stock when demand occurs.

- **MOQ (Minimum Order Quantity)**:
  - The minimum order limit per SKU (e.g., per carton / pack).
  - `order_qty` is rounded or constrained to meet this MOQ.

- **Capacity constraint**:
  - The maximum limit of total volume or order value (e.g., warehouse capacity, pallet slots, or distribution capacity).
  - Can be modeled as:
    - total quantity limit, or
    - total cost value limit (budget/cap).

- **Shelf-life / expiry** (if relevant for certain product categories):
  - Limits how far ahead we dare to pile up stock.
  - Reduces or prohibits overstock that potentially expires before being sold.

- **Budget cap**:
  - The upper limit of total spending (e.g., per week / per replenishment cycle).
  - The optimizer allocates this budget to SKU–locations with the highest economic priority (e.g., margin, criticality, or service level impact).

### D. Pass / fail KPIs

The success contract of the solution is measured by a combination of the following forecasting KPIs and operational / inventory KPIs:

- **Forecasting KPIs**:
  - **WAPE (Weighted Absolute Percentage Error)**:
    - More stable for data with many zero/low demand compared to MAPE.
    - Evaluated per horizon (e.g., 1–4 weeks ahead) and aggregated per SKU–location and total portfolio.
  - **MASE (Mean Absolute Scaled Error)**:
    - Compares model error against a naive baseline (e.g., naive last week).
    - A value \< 1 indicates the model is better than the naive baseline.

- **Inventory / Operational KPIs**:
  - **Fill-rate**:
    - The proportion of demand that can be met from on-hand stock.
    - Typical target: e.g., \(\ge 95\%\) (can be adjusted according to business needs).
  - **Stockout days**:
    - The number of days/weeks where stock = 0 when there is demand.
    - The fewer the better; can be used as a maximum constraint.
  - **Total cost**:
    - The sum of holding + stockout + ordering costs within a certain horizon.
    - Used to compare scenarios (baseline vs optimizer) and as an objective to be minimized.

The combination of the above KPIs defines whether the solution "passes/fails": the forecast model is considered good if WAPE/MASE meets the target; the optimizer is considered successful if it can achieve or exceed the fill-rate/stockout target with a reasonable total cost or lower than the baseline policy.