# Python Backtester

A desktop GUI alternative to MetaTrader 5's native strategy tester: download
historical data from your MT5 terminal, run backtests with a Python strategy
API, and watch a **visual replay** — candles drawing in sequence with trades
opening, adjusting, and closing on the chart.

See [PLAN.md](PLAN.md) for the full development plan.

## Roadmap

- [x] **Phase 1 — Data layer**: MT5 connection, bar download, local Parquet
      library with CSV import/export, Data Manager GUI
- [x] **Phase 2 — Backtest engine (headless)**: simulated broker (market /
      limit / stop orders, SL/TP, spread, commission, swap), strategy API
      with indicators, performance stats, CLI runner
- [x] **Phase 3 — Candlestick chart (pyqtgraph)**: viewport-windowed candle
      rendering (100k+ bars stay fluid), pan/zoom, crosshair with OHLC
      readout, indicator overlays, Chart tab in the GUI
- [x] **Phase 4 — Visual replay**: Backtest tab with play/pause/step/speed/
      fast-forward, candles drawing in sequence, live trade arrows and
      win/loss connectors, moving SL/TP lines, synced equity sub-chart
- [x] **Phase 5 — Results & UX**: Results tab (stats summary, sortable trade
      list, double-click to jump to the chart), fast-run mode with progress
      bar, trades/summary export, persistent settings
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
Downloads also capture the symbol's contract spec (point size, digits,
contract size) so backtest PnL is computed correctly for forex pairs,
indices, metals, etc.

## Chart tab

Pick any dataset from the library in the **Chart** tab and browse it:

- Drag / mouse-wheel to pan and zoom the time axis; the price axis auto-fits
  whatever is visible.
- Crosshair follows the mouse with a time + OHLC + volume readout above the
  chart.
- Overlay SMA/EMA lines with any period (Add / Clear in the toolbar).
- The X axis is bar-index based, so weekends and session gaps don't leave
  holes in the chart. Zoomed far out, candles switch to a close-price line
  for speed; zoom in and candles return.

## Backtest tab (visual replay)

The replacement for MT5's visual strategy tester. Pick a dataset and a
strategy (its parameters appear as an editable form), set balance / spread /
commission, and hit **Start Replay**:

- Candles draw in sequence at your chosen speed (1–250 bars/s), with
  **Play/Pause**, **Step** (one bar at a time), and **To End**
  (fast-forward, no animation).
- Trades appear live as they happen: ▲ buy / ▼ sell entry arrows, ✕ exit
  marks, and a dashed entry→exit connector colored by win/loss.
- Open positions show dashed **SL/TP lines that move** when the strategy
  modifies them — trailing stops visibly trail.
- A status row tracks balance, equity, floating PnL, and open/closed trade
  counts; an equity + balance sub-chart below the candles stays synced to
  the replay clock.
- **Follow** keeps the chart scrolling with the newest bar; pan or zoom to
  detach and inspect, tick Follow to snap back. The crosshair readout only
  shows bars revealed so far — no peeking ahead.
- When the run finishes, the toolbar shows the summary (trades, net,
  profit factor, max drawdown). Full results panel lands in Phase 5.

If a dataset was downloaded before contract-spec capture was added, the
Backtest tab warns and assumes forex contract math — re-download the
dataset (any small range; it merges) to attach the broker's real spec.

Prefer results over animation? **⏩ Run Fast** executes the whole backtest on
a background thread with a progress bar, then draws the final chart (all
candles, every trade marker, full equity curve) and opens the Results tab.
Hit *Start Replay* afterwards to watch the same run animated — runs are
deterministic.

## Results tab

After any run (replay or fast), the Results tab holds:

- the full performance summary (net profit, profit factor, win rate,
  expectancy, drawdown, Sharpe, streaks…),
- a sortable trade list — entry/exit times and prices, duration, pips, net
  (color-coded), commission, swap, and close reason,
- **double-click a trade to jump to it on the chart**, zoomed to the
  entry→exit region,
- export buttons for a trades CSV and a summary text report.

Your last-used dataset, strategy, parameter values, account settings, replay
speed, and window size are remembered between sessions.

## Run a backtest (CLI)

The engine is GUI-independent; until the chart phases land, run it from the
command line against any dataset in your library:

```powershell
python run_backtest.py EURUSD H1
python run_backtest.py GER40 H1 --strategy ma_cross --param fast=12 --param slow=48 --trades 10
python run_backtest.py XAUUSD M15 --strategy rsi_reversion --commission 7 --balance 5000
```

Built-in example strategies: `ma_cross`, `rsi_reversion`. A strategy is a
small Python class:

```python
from backtester.strategy.base import Strategy

class MaCross(Strategy):
    params = {"fast": 10, "slow": 30, "lots": 0.1, "sl_pips": 50.0, "tp_pips": 100.0}

    def init(self):
        self.fast_ma = self.ind.sma(self.p.fast)
        self.slow_ma = self.ind.sma(self.p.slow)

    def on_bar(self, bar):
        if self.cross_over(self.fast_ma, self.slow_ma):
            self.close_all()
            self.buy(lots=self.p.lots, sl_pips=self.p.sl_pips, tp_pips=self.p.tp_pips)
        elif self.cross_under(self.fast_ma, self.slow_ma):
            self.close_all()
            self.sell(lots=self.p.lots, sl_pips=self.p.sl_pips, tp_pips=self.p.tp_pips)
```

Available: `buy/sell` (market, fills next bar open), `buy_limit/sell_limit/
buy_stop/sell_stop`, `modify` (SL/TP, e.g. trailing stops), `close/close_all`,
indicators via `self.ind` (`sma, ema, rsi, atr, highest, lowest`), and
`cross_over/cross_under` helpers.

### Execution model

- Bars are **bid** prices (MT5 convention): longs open at ask (bid + spread)
  and close at bid; shorts the reverse. Spread comes from the data's spread
  column, or a fixed `--spread` in points.
- Strategy decisions happen on a bar's close; market orders fill at the next
  bar's open. SL/TP and pending triggers are evaluated against each bar's
  high/low; a level gapped over at the open fills at the open.
- If SL and TP both fall inside one bar, **SL is assumed to hit first**
  (pessimistic — OHLC bars can't reveal the intrabar path). Phase 6 adds
  tick/M1-based resolution.
- Commission is charged per side per lot; swap accrues per night held.

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
