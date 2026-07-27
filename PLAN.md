# Python Backtester — Development Plan

A desktop GUI application that replaces MT5's native strategy tester: download historical
data from MT5, run backtests with a Python strategy API, and watch a **visual replay** of
the backtest — candles drawing in sequence with trades opening, adjusting, and closing on
the chart.

> **Status:** Phases 1–7 are complete (this is the **v2** repository — the starting point
> carries the full v1 codebase forward). Phase 8 below — converting MQL5 custom
> indicators into Python indicators that draw on the app's charts — is the next block of
> work: planned, not yet implemented. Work continues one phase at a time, pushed for review.

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
├── engine/
│   └── trade_log.py          # Qt-free writer: per-moment bars + indicators → Parquet
├── strategy/
│   └── manual.py             # ManualStrategy: no-op on_bar, exposes broker to the GUI
└── ui/
    ├── manual_panel.py       # manual order-entry panel (direction, risk sizing, manage)
    ├── trade_log.py          # trade-log settings (QSettings) + dialog
    └── chart/
        └── order_lines.py    # three draggable lines (entry / TP / SL) + risk→lots math
```
Plus edits to `strategy/indicators.py` (applied-price selection; indicator registry so the
log can name what a strategy built), `ui/chart/chart_widget.py` (draggable order lines),
`engine/backtester.py` (opt-in position-event recording), `ui/chart_tab.py` +
`ui/backtest_tab.py` (applied-price picker, manual mode, speed slider, trade logging),
`ui/chart/replay_controller.py` (continuous speed from a slider), and `run_backtest.py`
(`--trade-log`).

**New modules planned for Phase 8 (MQL5 indicator conversion):**

```
backtester/
├── indicators/               # indicator plugin layer (distinct from strategy/indicators.py)
│   ├── base.py               # Indicator, Plot, DrawStyle, Pane, Level
│   ├── loader.py             # discovery + hot reload of indicators/*.py
│   └── builtin.py            # SMA/EMA/RSI/ATR as plugins
├── mql5/                     # .mq5 → Python conversion
│   ├── lexer.py  parser.py   # MQL5 subset front end
│   ├── metadata.py           # #property block, input declarations
│   ├── translate.py          # AST → Python source
│   ├── runtime.py            # MQL5 stdlib shim (iMA family, Math*, Array*, EMPTY_VALUE)
│   └── report.py             # what converted, what became a TODO, what was refused
└── ui/
    ├── indicators_tab.py     # library, inputs, preview, Import .mq5…
    ├── param_form.py         # param → widget form, extracted from backtest_tab
    └── chart/
        ├── indicator_layer.py  # price-pane plots, clipped to revealed bars
        └── indicator_pane.py   # separate sub-window with levels, X-linked
indicators/                   # user + converted indicator .py files (like strategies/)
```
Plus edits to `ui/chart/chart_widget.py` (attach/detach indicators, panes, overlay
clipping), `ui/chart_tab.py` + `ui/backtest_tab.py` (indicators on both charts),
`strategy/indicators.py` (`smma`, `lwma`, `IndicatorFactory.custom`), `strategy/base.py`,
and `packaging/backtester.spec` (bundle `indicators/`).

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

**Phase 7 — v2 features** ✅ *(done — see §7 for full design)*
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
- **7c. Trade context logs** — a checkbox in the (automatic) backtest setup that, when
  ticked, writes the bars and indicator values around every trade entry, SL/TP
  modification, and exit to a per-run folder. *(Originally specced as chart screenshots;
  replaced by data, which is analyzable — see §7c.)*
- *Milestone: manually trade EURUSD candle by candle with risk-based sizing; run an
  MA-cross backtest with an EMA on Typical price and a folder of per-trade context data.*

**Phase 8 — MQL5 indicator conversion** *(planned — see §8 for full design)*
- **8a. Python indicator plugin system** — indicators become loadable objects (multiple
  buffers, own chart window, draw styles, inputs) instead of the two hard-wired functions
  in the Chart tab; a new **Indicators tab** manages them, and they draw on the backtest
  replay chart too (clipped to revealed bars).
- **8b. `.mq5` importer** — pick an MQL5 custom indicator source file and convert it to a
  readable Python indicator file in `indicators/`: `#property` block → plots/window/levels,
  `input`s → parameters, `OnCalculate` → a vectorized/looped `calculate()`. Anything
  outside the supported subset is reported, not silently mistranslated.
- **8c. Fidelity, chaining, and strategy access** — compare a converted indicator against
  values exported from MT5 to prove the conversion, cover the `iMA`-family built-in
  handles, `iCustom` chaining between converted indicators, and `self.ind.custom(…)` so
  strategies can trade them.
- *Milestone: import a real `.mq5` oscillator, see it draw in its own pane under the
  candles matching MT5's values to within rounding, and trade it from a strategy.*

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

A **Mode** selector in the Backtest tab — *Strategy replay* (watch a strategy trade) vs
*Manual trading* (trade it yourself). Manual trading is an **alternative to watching the
standard replay**, not a separate screen: same tab, same chart, same playback, same results.
It runs a `ManualStrategy` whose `on_bar` does nothing, and the GUI injects the user's
orders straight into the simulated broker, so fills, SL/TP, spread, commission, swap,
equity, stats, and results all reuse the existing engine.

Choosing *Manual* swaps the setup panel: the strategy picker and parameter form give way to
the order-entry panel, and *Run Fast* is hidden (there is nothing to fast-run when you are
the strategy). The order logic lives in `manual_trader.py` so the tab itself stays readable.

**Session lifecycle.** *Start Manual Session* builds `Backtester(df, ManualStrategy(),
config)` and a `ReplayController`, advances a **warm-up** of ~100 bars so there is price
history for context, then **pauses** — the user trades forward from there. Reaching the end
of data force-closes open positions (as usual) and reports the run to the Results tab.

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

### 7c. Trade context logs

A **checkbox** in the automatic backtest setup — *Log trade context data* — writes, for
every moment a trade had, the bars around it and every indicator value the strategy
computed.

> **Superseded design.** This was originally specced as *trade screenshots*: a PNG of the
> chart at each entry and exit, rendered by a post-run pass over an offscreen chart. That
> was built and worked, but a picture is the wrong artifact — you cannot query it, diff it,
> or feed it anywhere. The same post-run pass now emits **data**, which answers "why did it
> trail the stop *there*" in a way an image never can, and drops the Qt dependency so the
> CLI can produce it too. The screenshot module was removed rather than kept alongside.

- **Folder**: `trade_logs/<symbol>_<tf>_<strategy>_<YYYYMMDD-HHMMSS>/`, one per run,
  holding `context.parquet`, `manifest.csv`, and `indicators.csv`.
- **`context.parquet` is long-form**, not one file per moment: `frame_id` tags the moment
  (`0007_entry`, `0007_modify_01`, `0007_exit`) and `offset` is each bar's distance from
  it (0 = the moment, negative = history), so a run loads in one `read_parquet` and slices
  by trade. Columns are the key fields, then every bar column, then every indicator.
- **The window** is either the **last N bars** up to the moment — the history the strategy
  had, no look-ahead — or the **whole calendar day** containing it, which does include what
  followed (a review tool, not a decision input; those rows carry `offset > 0`).
- **Indicators are discovered, not declared.** Strategies just assign them
  (`self.trend = self.ind.ema(50)`), so `collect_indicators` inspects the instance for
  numeric series as long as the data, minus the bar arrays `bind` attaches, and names each
  column after its attribute. `IndicatorFactory` now records every series it hands out with
  the call that produced it, so `indicators.csv` can say `trend → ema(50, Close)` — that
  registry keeps the array itself, since ids are reused once an array is collected.
- **Modifications are logged too**, not just entry/exit — an SL/TP change is a decision,
  and for a trailing stop it is *the* decision. The manifest carries the previous levels
  alongside the new ones, so a trailing stop reads as a chain of `old_sl → sl`.
- **The moments come from a recorded event stream.** With `record_events=True` the engine
  keeps every position opened/modified/closed event as a **snapshot**
  (`dataclasses.replace`) — `Position` is mutable, so storing the live object would report
  the final stop at every moment and quietly make every trailing-stop row wrong. Recording
  is opt-in per run, so an optimizer sweep never pays for it.
- **Qt-free writer** (`engine/trade_log.py`) with the settings and dialog in
  `ui/trade_log.py`, so `run_backtest.py --trade-log [bars|day]` produces the same folder
  headlessly.
- A **max moments per run** cap (default 1,000) with a cancellable progress dialog — a
  273-trade GER40 run of `trailing_trend` produces ~1,470 moments. Manual sessions don't
  log: the decisions were the user's, and there are no indicator series behind them.
- **Tests**: event recording and snapshot correctness; indicator discovery (recipes, bar
  arrays excluded, column-name clashes, hand-rolled series); window shapes for both modes
  including clipping at the start of the data; manifest/indicators contents; kind
  selection, cap, cancel; settings roundtrip and dialog behaviour.

## 8. Phase 8 design — MQL5 indicator conversion

**Goal:** take an existing MetaTrader 5 custom indicator (`.mq5` source) and turn it into a
Python indicator this app computes and draws on its charts — the Chart tab *and* the
backtest replay — with its inputs editable in the GUI and its buffers readable from a
strategy.

**Where today's code stands.** Indicators are currently two hard-wired functions
(`_INDICATORS = {"SMA": …, "EMA": …}` in `ui/chart_tab.py`) drawn through
`ChartWidget.add_overlay(name, values)`, which paints one fixed-width line on the price
pane over the *whole* array. An MQL5 indicator needs none of those assumptions: it has
several buffers, may live in its own window, draws lines/histograms/arrows in declared
colours, and carries its own inputs. So the plugin model (8a) has to land before the
converter (8b) has anywhere to put its output.

### 8a. Python indicator plugin system

New package `backtester/indicators/` (the vectorized maths stays in
`backtester/strategy/indicators.py` — the new package is the *plugin* layer, and the two
are imported under distinct paths):

```
backtester/indicators/
├── base.py       # Indicator base class, Plot / DrawStyle / Pane / Level specs
├── loader.py     # discovery + hot reload (mirrors strategy/loader.py)
└── builtin.py    # SMA/EMA/RSI/ATR wrapped as plugins, so there is one code path
indicators/       # user + converted indicator .py files (next to the app, like strategies/)
```

The authored API, deliberately shaped like `Strategy` so the existing param-form code and
the loader pattern carry over:

```python
from backtester.indicators.base import DrawStyle, Indicator, Level, Pane, Plot

class Supertrend(Indicator):
    display_name = "SuperTrend"
    pane = Pane.PRICE                     # or Pane.SEPARATE (own sub-window)
    params = {"period": 10, "multiplier": 3.0}
    plots = [
        Plot("Up",   style=DrawStyle.LINE, color="#26a69a", width=2),
        Plot("Down", style=DrawStyle.LINE, color="#ef5350", width=2),
    ]
    levels: list[Level] = []              # horizontal lines, e.g. RSI 30/70

    def calculate(self, df) -> dict[str, np.ndarray]:
        """Arrays aligned to df, NaN where undefined — the existing contract."""
```

- `params` keeps the numeric/bool convention `Strategy.params` uses, so the auto-generated
  form in `backtest_tab._rebuild_param_form` is **extracted to `ui/param_form.py`** and
  reused verbatim for indicator inputs (no second implementation to keep in step).
- `DrawStyle`: `LINE, HISTOGRAM, ARROW, SECTION, FILL, NONE` (NONE = a calculation-only
  buffer that is computed but not drawn — MQL5's `INDICATOR_CALCULATIONS`).
- `loader.py` mirrors `strategy/loader.py` exactly: fresh `compile()` on every discovery
  (so edits are never missed), `indicators/` next to `app.py` in a source checkout and next
  to the `.exe` when frozen, errors collected and surfaced rather than raised.

**Chart plumbing** (`ui/chart/`):
- `indicator_layer.py` — owns the items for each attached indicator on the price pane and
  applies the draw style; crucially it takes a **`set_visible_length(k)`** like
  `CandlestickItem` and `SeparatorLines` do. Today's `add_overlay` draws the full array;
  the Chart tab gets away with it because `set_data` clears overlays and the replay has
  none. Putting indicators on the replay chart without clipping would draw the indicator
  ahead of the revealed candles — i.e. leak the future — so clipping is part of this phase,
  wired from `ChartWidget.reveal_to`.
- `indicator_pane.py` — a stacked sub-pane for `Pane.SEPARATE` indicators, built the same
  way the equity sub-chart already is (`pg.PlotWidget` with
  `getPlotItem().setXLink(self.chart.plot.getPlotItem())`, `hideAxis("bottom")`), plus
  level lines and optional fixed min/max.
- `ChartWidget` gains `attach_indicator / detach_indicator / clear_indicators` and hosts
  zero or more panes below the candles; `add_overlay` stays as the thin single-line case.

**Indicators tab** (`ui/indicators_tab.py`) — the "section" this phase is really about:
- Left: the library of discovered indicators (built-ins + everything in `indicators/`),
  each showing its source file and status (*clean* / *has TODOs* / *load error*), with
  **Reload** and **Import .mq5…**.
- Right: the selected indicator's inputs (auto-form), its plots with colour/width/style
  overrides, and a **live preview chart** on the currently selected dataset.
- Attaching: a checkbox per indicator marks it *attached*; attached indicators + their
  parameter values are persisted in QSettings and applied to both the Chart tab and the
  Backtest tab's replay chart. The Chart tab's existing SMA/EMA toolbar controls stay as
  the quick path and are re-pointed at the plugin registry.

### 8b. The `.mq5` importer

New package `backtester/mql5/`:

```
backtester/mql5/
├── lexer.py       # MQL5 tokens (C-like), preprocessor lines, comments kept for labels
├── parser.py      # recursive-descent parser → AST for the supported subset
├── metadata.py    # #property block, input/sinput declarations, enums
├── translate.py   # AST → Python source
├── runtime.py     # the MQL5 standard-library shim the generated code imports
└── report.py      # ConversionReport: translated / TODO / unsupported, with line numbers
```

**Output is a file, not a hidden runtime.** Conversion writes a readable, PEP-8 Python
module into `indicators/` with a header naming the source `.mq5` and the converter version,
the `Indicator` subclass, and the translated body. The user can open it, fix a TODO, and
hit Reload — the same loop that already exists for strategies. A hidden interpreter would
make failures unfixable; generated source makes them a normal editing task.

**What maps to what:**

| MQL5 | Python indicator |
|---|---|
| `#property indicator_separate_window` / `_chart_window` | `pane = Pane.SEPARATE / Pane.PRICE` |
| `indicator_buffers N` / `indicator_plots M` | N buffers created; the first M become `plots`, the rest are `DrawStyle.NONE` |
| `indicator_label1/type1/color1/width1/style1` | one `Plot(...)` per index |
| `indicator_level1 30.0`, `indicator_minimum/maximum` | `levels = [Level(30.0)]`, pane y-range |
| `input int InpPeriod = 14; // Period` | `params = {"period": 14}`, label from the trailing comment (MT5 uses it the same way) |
| `OnInit()` + `SetIndexBuffer(k, Buf, …)` | NaN-filled `np.empty(len(df))` buffers created at the top of `calculate` |
| `OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread)` | `calculate(df)`; the arrays are the df columns |
| `OnCalculate(rates_total, prev_calculated, begin, price[])` | `calculate(df)` with an added `applied` param feeding `price_series(df, applied)` — reuses the Phase 7a `AppliedPrice` enum |
| `iMA / iRSI / iATR / iStdDev / iBands / iMACD / iCCI / iADX / iStochastic` handles + `CopyBuffer` | `runtime.py` shims computing MT5's formulas, returning arrays; `CopyBuffer(h, b, 0, rates_total, dst)` → an assignment |
| `MODE_SMA/EMA/SMMA/LWMA`, `PRICE_*` | existing `sma`/`ema` + **new `smma` and `lwma`** in `strategy/indicators.py`; `PRICE_*` → `AppliedPrice` |
| `EMPTY_VALUE`, `PLOT_EMPTY_VALUE`, `DBL_MAX` | `np.nan` |
| `MathAbs/Max/Min/Sqrt/Pow/Log/Floor/Ceil`, `ArrayInitialize/ArraySize/ArrayResize` | numpy/`math` equivalents |
| `_Symbol / _Period / _Point / _Digits` | dataset key + the stored contract spec (`DataStore.get(...)` already carries `point` and `digits`) |
| `clrRed`, `C'0,128,255'`, `0x00FF00` | hex colours — note MQL5 hex literals are **BGR**, not RGB |

**The three semantics that decide whether this works at all:**

1. **Index direction.** `OnCalculate`'s arrays are forward-indexed (0 = oldest) unless the
   indicator calls `ArraySetAsSeries(arr, true)`, which flips 0 to *newest*. The translator
   tracks the as-series flag per array through the function and rewrites series-indexed
   reads as `arr[n - 1 - i]`, emitting forward-indexed Python throughout (matching the rest
   of the app). If a flag is set conditionally, or through an alias the parser can't
   resolve statically, conversion **fails loudly** on that buffer rather than emitting code
   that is silently reversed — a reversed indicator looks plausible and is completely wrong.
2. **`prev_calculated`.** MT5 recomputes incrementally; this app precomputes the whole
   array once per dataset. The translator resolves the usual
   `int start = (prev_calculated == 0) ? period : prev_calculated - 1;` idiom to the
   `prev_calculated == 0` branch and always computes from bar 0, which is what a full
   precompute means. Documented, because it changes nothing for well-written indicators and
   *does* change behaviour for ones that hide state across calls (those get a warning).
3. **Unsupported constructs are refused, not guessed.** `ObjectCreate` and friends,
   `OnTimer`/`OnChartEvent`, file/network/`DLL` calls, `#import`, tick-level logic, and
   access to another symbol or timeframe (`iCustom`/`CopyRates` on a different chart) all
   emit a `# TODO(mql5): <original line>` plus a `raise NotImplementedError` in the affected
   branch, and land in the report with the source line number. A partial conversion that
   says exactly what it couldn't do is far more useful than a complete-looking wrong one.

**Import flow (Indicators tab → *Import .mq5…*):** file picker → parse → a report panel
showing detected window placement, plots, inputs, and every warning against its source
line, next to the generated Python; a **preview** renders it on the selected dataset
immediately. Buttons: *Save to `indicators/`*, *Copy source*, *Cancel*. Nothing is written
until the user saves.

### 8c. Fidelity, chaining, and strategy access

- **Prove the conversion.** *Compare with MT5…* loads a CSV of the indicator's buffer
  values exported from the MT5 terminal (Data Window → save, or a two-line dumper EA) for
  the same symbol/timeframe, aligns it on timestamps, and reports max / mean absolute
  error per buffer with the worst offenders listed. This is what turns "it looks about
  right" into a checkable claim, and it doubles as the regression harness.
- **Built-in handle coverage** — fill out the `iMA` family in `runtime.py`, each verified
  against MT5 output by the tool above.
- **`iCustom`** — resolve to another converted indicator in `indicators/`, so layered
  indicators convert as a set.
- **Strategy access** — `self.ind.custom("supertrend", period=10)["Up"]` in
  `IndicatorFactory`, so a converted indicator can be traded, optimized, and replayed like
  any built-in. Results are cached per (dataset, indicator, params) so the optimizer's
  worker processes don't recompute per combination.
- **Packaging** — `packaging/backtester.spec` bundles `indicators/` the way it already
  bundles `strategies/`, and the loader reads it from next to the `.exe` at runtime.
- **README** — a new *Custom indicators* section covering both authoring and importing.

### Tests

- **Parser/translator**: small `.mq5` snippets → expected Python, including the as-series
  rewrite, the `prev_calculated` idiom, buffer/plot extraction, and colour literal parsing
  (a BGR hex regression test).
- **Golden conversions**: three or four real indicators (a price-pane MA envelope, a
  separate-window oscillator with levels, an ATR-based trailing indicator) converted and
  checked against committed reference buffer CSVs within tolerance.
- **Runtime shim**: `iMA` in all four MA modes and `iRSI`/`iATR` against known values.
- **Refusals**: an indicator using `ObjectCreate` converts with a TODO and a report entry
  rather than raising at import time.
- **Chart (offscreen, as `tests/test_chart.py` already does)**: a multi-plot indicator
  renders, a separate pane is created and X-linked, and `reveal_to(k)` leaves nothing drawn
  past bar `k`.

### Phasing

8a → 8b → 8c, one push each. 8a is independently valuable (proper multi-buffer indicators
on the replay chart) even if the converter is never used, so it is worth doing first and
reviewing on its own.

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
- **Trade log volume** — moments are dominated by SL/TP modifications, not trades: a
  273-trade run of `trailing_trend` produces ~1,470 of them, and each writes a whole window
  of bars. Logging is opt-in, capped per run (default 1,000 moments), and cancellable; day
  mode on M1 data is the expensive corner (a day is 1,440 bars per moment).
- **Indicator discovery is by inspection** — strategies never declare their indicators, so
  the log finds numeric series on the instance. A strategy stashing an unrelated
  full-length numeric array would see it logged as an indicator (harmlessly, with no
  recipe); the bar arrays `bind` attaches are excluded by name.
- **MQL5 is a whole language** — a general transpiler is not the goal and would never
  finish. Scope is explicitly *single-symbol, single-timeframe `OnCalculate` indicators*;
  success is measured by that class converting cleanly and everything else being reported
  with a source line number. Expect to widen the subset from real files, not up front.
- **Silent mistranslation is the real danger** — a reversed array or an off-by-one warm-up
  produces a plausible-looking line that is wrong, and a backtest built on it is wrong
  too. Mitigations: refuse rather than guess on unresolved as-series flags, and make the
  MT5 value-comparison tool (8c) the standard way a conversion is accepted.
- **Per-bar loops in Python** — a translated `OnCalculate` loop over 100k bars runs in
  roughly 0.1–1 s. Acceptable for a one-off precompute; cache per (dataset, indicator,
  params), and vectorize the common patterns in `runtime.py` rather than in generated code.
- **Naming** — `backtester/indicators/` (plugin layer) alongside the existing
  `backtester/strategy/indicators.py` (maths) is a little close. Distinct import paths keep
  it unambiguous in code; revisit only if it proves confusing in practice.
- **Licensing** — converting a third-party indicator's source is the user's call, not the
  app's. Note it in the import dialog; do not ship converted third-party indicators.
