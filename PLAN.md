# Python Backtester — Development Plan

A desktop GUI application that replaces MT5's native strategy tester: download historical
data from MT5, run backtests with a Python strategy API, and watch a **visual replay** of
the backtest — candles drawing in sequence with trades opening, adjusting, and closing on
the chart.

---

## 1. Technology choices

| Concern | Choice | Rationale |
|---|---|---|
| Language | Python 3.12 (venv) | `MetaTrader5` wheels can lag behind the newest Python; 3.12 is the safe target. Verify 3.13 support at setup — use it if available. |
| GUI framework | **PySide6** (Qt for Python) | Mature, native-feeling desktop UI, docking panels, timers for replay playback. |
| Charting | **pyqtgraph** | GPU-accelerated Qt plotting; smooth candlestick replay with tens of thousands of bars. (`finplot`, built on pyqtgraph, is a shortcut option for candlesticks — evaluate in Phase 3.) |
| Data download | **`MetaTrader5`** pip package | Pulls bars (`copy_rates_range`) and ticks (`copy_ticks_range`) straight from the user's installed MT5 terminal. Windows-only, which matches this machine. |
| Data storage | **Parquet** (via `pyarrow`) as primary, **CSV export/import** for portability | Parquet is ~10x smaller and far faster to load than CSV; CSV supported so users can bring data from other sources. |
| DataFrames | pandas (numpy under the hood) | Standard; pyqtgraph consumes numpy arrays directly. |
| Packaging (later) | PyInstaller | Single-folder Windows distributable. |

## 2. Application layout (what the user sees)

Main window with tabs / dock panels:

1. **Data Manager tab**
   - Connect to MT5 terminal (auto-detect running terminal; show account/broker info).
   - Pick symbol, timeframe (M1…MN1, plus ticks), date range → download → save to local store.
   - Library view of downloaded datasets (symbol, timeframe, range, bar count, file size)
     with re-download/update, delete, export-to-CSV, import-from-CSV.
2. **Backtest tab**
   - Select dataset + strategy (Python file) + parameters (auto-generated form from the
     strategy's declared params).
   - Account settings: initial balance, leverage, spread model (fixed / from data),
     commission, swap, slippage.
   - Run modes: **Fast run** (no animation, results ASAP) and **Replay run** (visual).
3. **Chart / Replay view** (the centerpiece)
   - Candlestick chart with pan/zoom, crosshair, OHLC readout, indicator overlays.
   - Playback controls: ▶ pause ⏸, step-one-bar, speed control (e.g. 1×–500× bars/sec),
     jump-to-date, restart.
   - Trade visualization drawn live during replay:
     - entry/exit arrows (buy ▲ green, sell ▼ red), dotted line connecting entry→exit
       colored by win/loss;
     - horizontal SL/TP lines for open positions that **move when the strategy modifies
       them** (trailing stops visibly trail);
     - open-position badge showing direction, lots, floating P/L.
   - Bottom sub-panel: live equity/balance curve synced to the chart's clock.
4. **Results panel**
   - Trade list (entry/exit time & price, lots, P/L, pips, duration) — clicking a trade
     jumps the chart to it.
   - Stats: net profit, profit factor, win rate, max drawdown (absolute/%), Sharpe,
     expectancy, avg win/loss, longest losing streak, exposure.
   - Export report (CSV of trades + summary).

## 3. Architecture

```
Python Backtester/
├── app.py                     # entry point
├── requirements.txt
├── backtester/
│   ├── data/
│   │   ├── mt5_client.py      # MT5 connection, symbol/timeframe download
│   │   ├── store.py           # Parquet library: save/load/update, CSV import/export
│   │   └── models.py          # Bar, Tick, DatasetInfo dataclasses
│   ├── engine/
│   │   ├── backtester.py      # event loop: feeds bars to strategy, advances clock
│   │   ├── broker.py          # simulated broker: order matching, fills, margin,
│   │   │                      #   spread/commission/swap, SL/TP triggering
│   │   ├── orders.py          # Order/Position/Deal objects (market, limit, stop)
│   │   ├── events.py          # BarEvent, OrderFilled, PositionModified, ... (queue
│   │   │                      #   consumed by both stats and the GUI replay)
│   │   └── stats.py           # equity tracking + performance metrics
│   ├── strategy/
│   │   ├── base.py            # Strategy API: params, on_bar(), buy/sell/modify/close
│   │   ├── indicators.py      # SMA/EMA/RSI/ATR... (vectorized, precomputed)
│   │   └── examples/          # MA cross, RSI mean-reversion, breakout
│   └── ui/
│       ├── main_window.py
│       ├── data_tab.py
│       ├── backtest_tab.py
│       ├── chart/
│       │   ├── candlestick_item.py   # custom pyqtgraph GraphicsObject
│       │   ├── chart_widget.py       # chart + overlays + trade markers
│       │   └── replay_controller.py  # QTimer-driven playback, speed, step
│       └── results_panel.py
└── tests/                     # engine unit tests (fills, SL/TP, PnL, stats)
```

**Key design decision — engine/GUI separation:** the engine is a pure-Python generator
that yields events (`new bar`, `order opened`, `SL modified`, `position closed`, `equity
point`). Fast mode drains it in a worker thread; replay mode drains it on a `QTimer` at
the chosen speed and hands each event to the chart. Same engine, one code path, no
GUI dependency in the engine → fully unit-testable.

**Execution realism:** bar-by-bar `on_bar()` strategy callbacks; intrabar SL/TP fills
resolved against the bar's H/L with MT5-style pessimistic ordering (configurable). Phase 6
option: use stored M1 or tick data to resolve intrabar sequences exactly.

## 4. Strategy API (sketch)

```python
class MaCross(Strategy):
    params = {"fast": 10, "slow": 30, "lots": 0.1, "sl_pips": 50, "tp_pips": 100}

    def init(self):
        self.fast_ma = self.indicator.sma(self.p.fast)
        self.slow_ma = self.indicator.sma(self.p.slow)

    def on_bar(self, bar):
        if self.cross_over(self.fast_ma, self.slow_ma) and not self.position:
            self.buy(lots=self.p.lots, sl_pips=self.p.sl_pips, tp_pips=self.p.tp_pips)
        elif self.cross_under(self.fast_ma, self.slow_ma) and self.position.is_long:
            self.close_all()
```

`params` drives the auto-generated settings form in the Backtest tab (and later, the
optimizer).

## 5. Build phases

**Phase 1 — Scaffolding + data layer** (foundation)
- venv, requirements, package skeleton, minimal main window.
- `mt5_client.py`: connect, list symbols, download bars for symbol/timeframe/range.
- `store.py`: Parquet save/load, dataset catalog (JSON or SQLite index), CSV import/export.
- Data Manager tab wired end-to-end. *Milestone: download EURUSD H1 2020–2025 and see it in the library.*

**Phase 2 — Backtest engine (headless)**
- Bar feed, broker simulation (market orders, SL/TP, spread, commission), positions, PnL,
  event stream, stats.
- Strategy base class + MA-cross example; run from a script/test, print stats.
- Unit tests for fill logic and PnL math. *Milestone: headless backtest produces a sane trade list.*

**Phase 3 — Chart**
- Custom candlestick item in pyqtgraph (viewport-windowed rendering so 100k+ bars stay
  smooth), pan/zoom, crosshair, indicator overlay lines. *Milestone: load any dataset and browse it fluidly.*

**Phase 4 — Replay** (the differentiator)
- `replay_controller`: QTimer stepping the engine event stream; play/pause/step/speed/jump.
- Live trade drawing: arrows, entry→exit lines, moving SL/TP lines, open-position badge,
  synced equity sub-chart. *Milestone: watch MA-cross trade EURUSD candle by candle.*

**Phase 5 — Results & UX**
- Results panel (trade list ↔ chart jump, full stats), fast-run mode with progress bar
  then optional "replay this result", report export, settings persistence (QSettings).

**Phase 6 — Stretch**
- Tick/M1 intrabar accuracy mode, parameter optimization (grid search, multiprocessing)
  with results table, multi-symbol portfolio tests, strategy hot-reload, PyInstaller build.

## 6. Risks / open questions

- **`MetaTrader5` package vs Python 3.13** — check wheel availability at setup; fall back
  to a 3.12 venv if needed. Requires an installed, logged-in MT5 terminal.
- **Broker history depth** — MT5 terminals only serve what the broker provides (often
  limited tick/M1 history). Mitigate with incremental updates and CSV import from other
  sources.
- **Timezones** — MT5 returns server time; store everything as UTC with the server offset
  recorded in dataset metadata.
- **Replay performance at high speed** — batch chart updates per timer tick (append N bars
  per frame) instead of one repaint per bar.
- **Look-ahead bias** — indicators are precomputed vectorized, but the strategy may only
  read values up to the current bar index; enforce in the API.
