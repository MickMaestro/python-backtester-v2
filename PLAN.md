# Python Backtester — Development Plan

A desktop GUI application that replaces MT5's native strategy tester: download historical
data from MT5, run backtests with a Python strategy API, and watch a **visual replay** of
the backtest — candles drawing in sequence with trades opening, adjusting, and closing on
the chart.

> **Status:** Phases 1–6 are complete (this is the **v2** repository — the starting point
> carries the full v1 codebase forward). Phase 7 below is the next block of work: it is
> planned, not yet implemented. Work continues one phase at a time, pushed for review.

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

**New modules added in Phase 7 (v2):**

```
backtester/
├── strategy/
│   └── manual.py             # ManualStrategy: no-op on_bar, exposes broker to the GUI
└── ui/
    ├── manual_panel.py       # manual order-entry panel (direction, risk sizing, manage)
    ├── screenshots.py        # ScreenshotCapturer: entry/exit PNG pairs + manifest
    └── chart/
        └── order_lines.py    # three draggable lines (entry / TP / SL) + risk→lots math
```
Plus edits to `strategy/indicators.py` (applied-price selection), `ui/chart/chart_widget.py`
(draggable order lines, fixed-size export grab), `ui/chart_tab.py` + `ui/backtest_tab.py`
(applied-price picker, manual mode, speed slider, screenshot checkbox), and
`ui/chart/replay_controller.py` (continuous speed from a slider).

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

**Phase 6 — Stretch** ✅ *(done — minus multi-symbol portfolio, deferred)*
- Tick/M1 intrabar accuracy mode, parameter optimization (grid search, multiprocessing)
  with results table, strategy hot-reload, PyInstaller build.

**Phase 7 — v2 features** *(planned — the next block of work; see §7 for full design)*
- **7a. Applied price for indicators** — every indicator (SMA, EMA, RSI, highest/lowest,
  and where meaningful, others) can be computed on a chosen applied price: Close, Open,
  High, Low, Median (HL/2), Typical (HLC/3), Weighted (HLCC/4). Selectable in the Chart
  tab's indicator controls and as an argument in the strategy API.
- **7b. Manual trading mode** — a play-and-trade mode: the replay runs while the user
  places and manages trades by hand using three draggable chart lines (entry, take-profit,
  stop-loss; TP/SL optional). Position size chosen as a % of balance to risk, a fixed cash
  risk, or a fixed lot size. Playback has a pause button, a speed **slider**, and a
  skip-to-next-candle button. Manual trades run through the same broker/engine, so stats,
  equity, and results work identically.
- **7c. Trade screenshots** — a checkbox in the (automatic) backtest setup that, when
  ticked, saves a chart screenshot at every trade's entry and exit, named as pairs
  (`0001_entry.png` / `0001_exit.png`) in a per-run folder with a manifest.
- *Milestone: manually trade EURUSD candle by candle with risk-based sizing; run an
  MA-cross backtest with an EMA on Typical price and a folder of entry/exit screenshots.*

## 7. Phase 7 design (v2 features)

### 7a. Applied price for indicators

Today `IndicatorFactory` methods take a `source` column name (`"close"`, `"high"`, …).
Generalize this to MT5's standard **applied prices** so an SMA/EMA/RSI can run on a derived
series, not just a raw column.

- New `AppliedPrice` enum in `indicators.py`:
  `CLOSE, OPEN, HIGH, LOW, MEDIAN, TYPICAL, WEIGHTED`.
- New helper `price_series(df, applied) -> np.ndarray`:
  - Median = (High + Low) / 2
  - Typical = (High + Low + Close) / 3
  - Weighted = (High + Low + 2·Close) / 4
  - the rest are the raw columns.
- Indicator methods gain an `applied: AppliedPrice = AppliedPrice.CLOSE` argument
  (`source` kept as an alias for a raw column name for back-compat). ATR is intrinsically
  H/L/C-based, so it ignores applied price (documented); `highest`/`lowest` still accept a
  source but also accept an applied price.
- **Chart tab**: add an *Apply to* dropdown next to the indicator/period controls; the
  overlay label becomes e.g. `EMA(20, Typical)`.
- **Strategy API**: `self.ind.ema(20, applied=AppliedPrice.MEDIAN)`. Document in README.
- **Tests**: median/typical/weighted values on a hand-built frame; overlay label text.

### 7b. Manual trading mode

A dedicated **Manual tab** running a `ManualStrategy` whose `on_bar` does nothing; the GUI
injects the user's orders straight into the simulated broker, so fills, SL/TP, spread,
commission, swap, equity, stats, and results all reuse the existing engine.

> *Rectified from the original sketch (a mode toggle inside the Backtest tab).* A separate
> tab keeps the tested automatic backtest untouched and each screen focused; it composes the
> existing `ChartWidget`, `TradeLayer`, `ReplayController`, and equity plot rather than
> duplicating engine logic. The only cost is a similar-looking playback toolbar, which
> differs anyway (speed **slider** + order entry vs the automatic tab's speed combo).

**Session lifecycle.** *Start* builds `Backtester(df, ManualStrategy(), config)` and a
`ReplayController`, advances a **warm-up** of ~100 bars so there is price history for
context, then **pauses** — the user trades forward from there. Reaching the end of data
force-closes open positions (as usual) and emits the run to the Results tab. *Restart*
rebuilds a fresh session.

**How orders reach the engine.** The replay already steps the engine generator bar-by-bar
on the main thread via `ReplayController`. `ManualStrategy` (or `Backtester`) exposes its
`SimBroker`; the manual panel calls `broker.market_order / limit_order / stop_order /
modify_position / close_position` while paused or between steps. Because the broker fills
market orders at the **next bar's open** and evaluates SL/TP against subsequent bars, a
manual order placed on bar *i* fills on bar *i+1* — the same realistic timing as strategies.

**Three draggable chart lines** (`order_lines.py`, draggable pyqtgraph `InfiniteLine`s):
- **Entry** (blue), **Take-Profit** (green), **Stop-Loss** (red). TP/SL are individually
  toggleable — a trade needs neither.
- Dragging a line updates the order-entry preview live; once a position is open, dragging
  TP/SL calls `broker.modify_position` (visually identical to a strategy trailing a stop).

**Order-entry panel** (`manual_panel.py`):
- **Order type**: an explicit *Market* / *Pending* selector, plus **Buy** / **Sell**
  buttons. *Rectified:* the original sketch inferred market-vs-pending from how close the
  entry line sat to price, which needs an arbitrary tolerance and can surprise the user.
  An explicit selector is unambiguous and testable:
  - *Market* — fills at the next bar's open; the entry line is hidden (there is no trigger
    price to choose). Risk sizing uses the **current close as the entry estimate**, since
    the true fill (next open) isn't known yet — a small, normal discrepancy.
  - *Pending* — the entry line is shown and its price is the trigger; the limit/stop kind
    is derived from side vs current price (buy above → buy-stop, buy below → buy-limit;
    sell above → sell-limit, sell below → sell-stop).
  - A live **preview label** always states the resolved order ("Buy Stop @ 25100 · 0.42
    lots · risking 250.00"), so what will happen is visible before clicking.
- **Risk sizing** (radio, one active):
  1. **% of balance to risk** — `risk_cash = pct/100 · balance`
  2. **Fixed cash risk** — `risk_cash = amount`
  3. **Fixed lot size** — lots entered directly
  For (1)/(2): `lots = risk_cash / (|entry − SL| · contract_size)`, rounded to the lot step
  (0.01). Risk sizing **requires an SL** (no SL ⇒ no risk distance); if SL is off, those
  modes are disabled with a hint, or the user switches to fixed lots. A live preview shows
  the computed lots and the cash-at-risk before placing.
- **Manage**: *Close* (market at next open), *Cancel pending*, and drag-to-modify SL/TP.
- An open-position badge (direction, lots, entry, floating P/L) — reuse the replay badge.

**Playback controls** (shared, surfaced prominently in Manual mode):
- **Pause/Play** button (exists).
- **Speed slider** — replaces the discrete speed combo with a continuous slider
  (e.g. 1–200 bars/sec, log-ish scale); `ReplayController.set_speed` already takes a float.
- **Skip-to-next-candle** button — one-bar `Step` (exists), so the user can advance
  deliberately and place orders candle by candle.

**Tests**: risk→lots math (with/without SL, lot-step rounding); a market order placed via
the panel fills at the next bar and appears in results; drag-modify updates the position's
SL. GUI wiring smoke-tested offscreen.

**Open question**: whether Manual mode also allows *scaling in/out* (multiple positions) —
the broker already supports multiple open positions, so start with one-at-a-time for a
clean UX and revisit.

### 7c. Trade screenshots

A **checkbox** in the automatic backtest setup — *Capture trade screenshots* — saves a
chart image at each trade's entry and exit.

- **Naming**: `NNNN_entry.png` / `NNNN_exit.png` (zero-padded trade id) so the two frames
  are an obvious pair. A `manifest.csv` maps id → files, direction, lots, entry/exit
  time & price, and net.
- **Folder**: `screenshots/<symbol>_<tf>_<strategy>_<YYYYMMDD-HHMMSS>/` next to the app
  (base dir configurable), one folder per run.
- **Capture path** (`screenshots.py`, `ScreenshotCapturer`): render deterministically with
  a **post-run pass** so it works for both fast and replay runs and gives consistent
  framing — for each trade, reveal candles up to the entry bar, centre the entry region,
  grab the chart to a fixed-size `QPixmap` (e.g. 1280×720) → entry PNG; reveal to the exit
  bar, centre the exit region, grab → exit PNG. (Live grab-on-event during replay is a
  possible fast path but framing is inconsistent, so the render pass is the default.)
- Runs on a copy/offscreen chart so it doesn't disturb the user's current view; guard for
  large trade counts (warn/limit, e.g. skip past N trades or make it opt-in per range).
- **Tests**: capturing a small run writes the right number of paired files + a manifest row
  per trade; filenames pair correctly.

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
- **Manual risk sizing without an SL** — % / cash risk modes need a stop distance; with no
  SL there is nothing to size against. Disable those modes (or require an SL) rather than
  guess, and always show the computed lots before the order is placed.
- **Screenshot volume & performance** — a run with thousands of trades would write
  thousands of PNGs and take a while to render. Make capture opt-in, warn past a threshold,
  render off the user's live chart, and consider a bar-range limit.
- **Offscreen chart grab sizing** — grabbing a widget with no valid size yields a blank
  image; render screenshots at a fixed export resolution on a sized (possibly hidden)
  chart so output is consistent regardless of window state.
