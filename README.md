# Python Backtester

A desktop GUI alternative to MetaTrader 5's native strategy tester: download
historical data from your MT5 terminal, run backtests with a Python strategy
API, and watch a **visual replay** — candles drawing in sequence with trades
opening, adjusting, and closing on the chart.

See [PLAN.md](PLAN.md) for the full development plan.

## Roadmap

- [x] **Phase 1 — Data layer**: MT5 connection, bar download, local Parquet
      library with CSV import/export, Data Manager GUI
- [ ] Phase 2 — Backtest engine (headless): broker simulation, orders, PnL, stats
- [ ] Phase 3 — Candlestick chart (pyqtgraph): pan/zoom, crosshair, indicators
- [ ] Phase 4 — Visual replay: playback controls, live trade drawing
- [ ] Phase 5 — Results panel, fast-run mode, report export
- [ ] Phase 6 — Tick-accurate fills, parameter optimization, packaging

## Requirements

- Windows with [MetaTrader 5](https://www.metatrader5.com/) installed and
  logged in to a broker (needed for downloading data; CSV import works
  without it)
- Python 3.12+

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```powershell
python app.py
```

Open the **Data Manager** tab, click *Connect to MT5*, pick a symbol,
timeframe, and date range, then *Download*. Datasets are stored as Parquet
files in `data_library/` and can be exported to or imported from CSV.

## Tests

```powershell
pytest
```

## Notes

- Bar timestamps are stored in **MT5 server time** (as delivered by the
  terminal), naive (no timezone attached).
- Re-downloading a symbol/timeframe **merges** with existing data (duplicates
  dropped), so you can extend a dataset incrementally.
- If MT5 returns fewer bars than expected, raise *Max bars in chart* in the
  terminal under Tools → Options → Charts, and check your broker's history depth.
