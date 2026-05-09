## Data Dictionary

This document describes the **dataset format** used for forecasting training and as input to the optimizer. If the actual data is not yet final, the schema below serves as a **sample schema** that can later be mapped to the actual data source.

### 1. Core Dataset Format

Each row represents a demand observation for one combination of **date × SKU × location**.

#### Core Columns Table

| Column        | Type (recommended) | Example         | Description                                                               |
|---------------|--------------------|-----------------|---------------------------------------------------------------------------|
| `date`        | `date` / `string` (YYYY-MM-DD) | `2025-01-06`   | Date of demand observation (daily or start of week granularity).          |
| `sku_id`      | `string`           | `P001`          | Unique product / SKU ID.                                                  |
| `location_id` | `string`           | `S001`          | Unique location ID (store, DC, region).                                   |
| `demand_qty`  | `float` / `int`    | `12.0`          | Actual demand / sales quantity on that date (forecast target).            |

> Note: The recommended granularity is consistent with the **Problem Contract** (weekly). If historical data is daily, aggregation to weekly can be done in the ETL stage.

### 2. Optional Columns (Additional Features)

The columns below are optional. If available, they can be used as additional features for the forecasting model or as parameters for the optimizer.

#### 2.1. Price & Promo

| Column         | Type (recommended) | Example | Description                                                            |
|----------------|--------------------|---------|------------------------------------------------------------------------|
| `price`        | `float`            | `49.90` | Selling price per SKU unit on that date/location.                      |
| `promo_flag`   | `int` / `bool`     | `1`     | Promo period indicator (1 = promo, 0 = no promo).                      |
| `holiday_flag` | `int` / `bool`     | `0`     | Holiday / high season indicator (1 = holiday/high season, 0 = not).    |

#### 2.2. Inventory & Supply

| Column           | Type (recommended) | Example | Description                                                               |
|------------------|--------------------|---------|---------------------------------------------------------------------------|
| `on_hand`        | `float` / `int`    | `35`    | On-hand stock at the beginning/observation period.                        |
| `on_order`       | `float` / `int`    | `20`    | Quantity already ordered but not yet received (open PO).                  |
| `lead_time_days` | `int`              | `7`     | Average lead time (days) from order until stock arrives at the location.  |

#### 2.3. Product & Supplier Master Data

| Column       | Type (recommended) | Example    | Description                                           |
|--------------|--------------------|------------|-------------------------------------------------------|
| `supplier_id`| `string`           | `SUP01`    | Main supplier ID for the SKU.                         |
| `category`   | `string`           | `Beverage` | Product category (e.g., category, subcategory, segment).|

### 3. Sample Schema

Example table schema in pseudo-SQL format:

```sql
CREATE TABLE demand_history (
    date           DATE           NOT NULL,
    sku_id         VARCHAR(50)    NOT NULL,
    location_id    VARCHAR(50)    NOT NULL,
    demand_qty     FLOAT          NOT NULL,

    -- Optional features
    price          FLOAT          NULL,
    promo_flag     TINYINT        NULL,
    holiday_flag   TINYINT        NULL,

    on_hand        FLOAT          NULL,
    on_order       FLOAT          NULL,
    lead_time_days INT            NULL,

    supplier_id    VARCHAR(50)    NULL,
    category       VARCHAR(100)   NULL
);
```

The schema above can be adapted to other formats (CSV, Parquet, Pandas DataFrame). The important thing is that each column follows the **name** and **meaning** as defined in this data dictionary table, so that the ETL pipeline, model, and optimizer can connect consistently.