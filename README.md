## Supply Chain ML: Forecasting + Replenishment Optimizer

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.11x-green)
![Docker](https://img.shields.io/badge/Docker-ready-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![CI](https://github.com/hidatara-ds/supplychain-ml-forecasting-optimizer/actions/workflows/ci.yml/badge.svg)](https://github.com/hidatara-ds/supplychain-ml-forecasting-optimizer/actions)

An end-to-end demo for retail supply chain analytics: generate realistic dummy data, engineer features, train a weekly demand-forecast model, and optimize replenishment under budget using linear programming. Exposed via a FastAPI service.

### Problem Contract

This project is driven by a clear problem contract that defines what is forecasted and what the optimizer decides:

- **Forecast target**: weekly `demand_qty` per SKU × location, with horizon \(H = 4\) weeks ahead.
- **Optimizer output**: `order_qty` per SKU–location–period, minimizing total inventory cost (holding + stockout + ordering) under budget/capacity.
- **Key constraints**: lead time, MOQ, capacity, optional shelf-life, and budget cap.
- **Pass/fail KPIs**:
  - Forecasting: WAPE and MASE vs naive baseline.
  - Inventory/ops: fill-rate, stockout days, and total cost vs baseline or target.

For a more detailed description, see `docs/problem_contract.md`.

### Preview

Streamlit dashboard screenshots (example):

- Landing page (metrics + charts):
  - `assets/landingpage1.png`
  - `assets/landingpage2.png`
- SKU-location details table:
  - `assets/detail.png`

![Dashboard Preview 1](assets/landingpage1.png)
![Dashboard Preview 2](assets/landingpage2.png)
![SKU-Location Details](assets/detail.png)

### Tech Stack
- **Language**: Python 3.11
- **API**: FastAPI + Uvicorn
- **ML**: pandas, numpy, scikit-learn, LightGBM (fallback to RandomForest)
- **Optimization**: SciPy linprog
- **Packaging**: Docker

### Project Structure
```
app/            FastAPI app & services
  main.py
  services/
    inference.py
    optimizer.py
etl/            Dummy data + features + processed
  generate_dummy.py
  build_features.py
models/         Training code & artifacts
  train_forecast.py
  artifacts/
scripts/        Utilities (e.g., backtest placeholder)
tests/          Pytest for API
docker/         Dockerfile
```

### Prerequisites
- Python 3.11
- Windows PowerShell or a POSIX shell
- Optional: Docker (24+) for container runs

### Setup (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

### Setup (macOS/Linux)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Quickstart

#### Option A: Training & Evaluation Pipeline
1) Generate data and build features
```powershell
python etl/generate_dummy.py
python etl/build_features.py
```

2) Train forecasting model (with time-based split)
```powershell
python -m src.forecasting.train
```

3) Evaluate and generate predictions
```powershell
python -m src.forecasting.evaluate
```

#### Option B: Streamlit Dashboard (Visual)
After running the pipeline above, launch the dashboard:
```powershell
streamlit run streamlit_app.py
```
The dashboard will open in your browser (default: `http://localhost:8501`).

**Dashboard Features:**
- 📈 Summary metrics (WAPE for naive, seasonal, model)
- 📉 Forecast vs Actual comparison chart (interactive)
- 📊 Error distribution histograms
- 🔍 Detail metrics per SKU-location (optional)

#### Option C: FastAPI Service
```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

4) Smoke tests (for API)
```powershell
# PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
Invoke-RestMethod -Uri "http://localhost:8000/forecast" -Method Post -ContentType "application/json" -Body '{"horizon_weeks":4,"pairs":[{"store_id":"S001","product_id":"P001"}]}'
Invoke-RestMethod -Uri "http://localhost:8000/replenish" -Method Post -ContentType "application/json" -Body '{"target_service":0.95,"capacity":50000}'

# curl (macOS/Linux/Windows)
curl http://localhost:8000/health
curl -X POST http://localhost:8000/forecast -H "Content-Type: application/json" -d '{"horizon_weeks":4,"pairs":[{"store_id":"S001","product_id":"P001"}]}'
curl -X POST http://localhost:8000/replenish -H "Content-Type: application/json" -d '{"target_service":0.95,"capacity":50000}'
```

Alternatively, using Make (macOS/Linux or Windows with `make` installed):
```bash
make setup && make data && make train && make run
```

### API Reference
- **GET `/health`** → `{ "status": "ok" }`

- **POST `/forecast`**
  - Request
    ```json
    { "horizon_weeks": 8, "pairs": [{"store_id":"S001","product_id":"P001"}] }
    ```
  - Response (excerpt)
    ```json
    {
      "horizon_weeks": 8,
      "forecasts": [
        {"store_id":"S001","product_id":"P001","forecast":[6.2,6.1,6.0, ...]}
      ]
    }
    ```

- **POST `/replenish`**
  - Request
    ```json
    { "target_service": 0.95, "capacity": 50000 }
    ```
  - Response (excerpt)
    ```json
    {
      "target_service": 0.95,
      "capacity": 50000.0,
      "orders": [
        {"store_id":"S001","product_id":"P001","order_qty":12,"unit_price":50.0,"cost":600}
      ]
    }
    ```

Notes:
- If no trained model is found, `/forecast` returns a reasonable naive forecast.
- Replenishment solves a linear program; if the solver fails, it falls back to needs.

### Testing
```powershell
pytest -q
```

### Docker
```powershell
docker build -t scm-ml .
docker run -p 8000:8000 scm-ml
curl http://localhost:8000/health
```

### Troubleshooting
- Parquet errors: ensure `pyarrow` is installed (included in `requirements.txt`).
- Windows without `make`: use the PowerShell commands above or install make via `choco install make`.
- Port already in use: change `--port 8001` when running Uvicorn.

### Deployment

#### Streamlit Cloud (Recommended for MVP)
1. Push repo to GitHub
2. Login to [streamlit.io](https://streamlit.io/cloud)
3. Connect GitHub repo
4. Set main file: `streamlit_app.py`
5. Deploy!

**Note:** Ensure `data/processed/predictions.csv` exists before deploying, or generate it via GitHub Actions.

#### Vercel (Future: Next.js Frontend)
For production deployment with a custom UI, you can build a Next.js frontend that calls the FastAPI backend.

### Roadmap
- ✅ Streamlit dashboard for visualization
- ETA/lead-time module
- Anomaly detection
- Cloud Run deployment (GCP)
- Next.js frontend for production

# supplychain-ml-forecasting-optimizer