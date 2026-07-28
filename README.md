# Python Backtester

A desktop GUI alternative to MetaTrader 5's native strategy tester: download
historical data from your MT5 terminal, run backtests with a Python strategy
API, and watch a **visual replay** — candles drawing in sequence with trades
opening, adjusting, and closing on the chart.

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
- **Indicators…** loads indicators from the `indicators/` folder onto the
  chart — see *Chart indicators* below.
- The X axis is bar-index based, so weekends and session gaps don't leave
  holes in the chart. Zoomed far out, candles switch to a close-price line
  for speed; zoom in and candles return.
- **Display…** opens chart display settings: bullish/bearish candle colours,
  background, an optional grid (off by default) with its colour, and period
  separators — vertical lines at day boundaries labelled with the weekday
  (Friday, Tuesday…), on by default, with a configurable colour. Settings are
  saved and shared across every chart in the app.

## Chart indicators

**Indicators…** (Chart tab) lists everything in the **`indicators/`** folder,
lets you set each one's parameters, and draws it. The selection is app-wide, so
whatever you load also draws on the Backtest tab's replay chart — clipped to the
bars revealed so far, so an indicator never runs ahead of the candles.

Eight MetaTrader indicators ship converted, from the `.mq5` sources in
[`mql5_indicators/`](mql5_indicators/):

| Indicator | What it draws |
|---|---|
| **SSL Channel** | LWMA channel of highs/lows; the opposite band trails as a stop, with dots where a line starts |
| **Chandelier Exit** | Two ATR trailing stops at once (tight and wide), each ratcheting in the trend's favour |
| **Volty Channel Stop** | ATR envelope around a moving average; the band edge becomes the stop, with a dot per flip |
| **Gann High/Low Activator** | Averages of the previous bar's high and low as a zone, with the activator line coloured by state |
| **IBK Candles** | Three MA trend filters; **recolours the candles** blue/grey/violet by the trading direction |
| **RSI MA Arrows** | RSI of a smoothed price in its own pane (six RSI formulas, Heiken Ashi prices), plus arrows on the candles |
| **Bid Ratio** | Where the day is closing within its own range, 0–100, in its own pane |
| **XU ADR Levels** | Fibonacci targets around the day's open, measured in average daily ranges |

Each conversion is a plain, editable Python file with a header saying what it
came from and what was left out. Terminal-only behaviour — alerts, sounds,
notifications, chart objects, multi-timeframe `iCustom` calls — has no meaning
here and is documented as skipped rather than faked.

Writing your own is the same as writing a strategy: drop a `.py` file in
`indicators/` and hit **Reload** in the dialog.

```python
from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5

class Envelope(Indicator):
    name = "Envelope"
    pane = Pane.PRICE                      # or Pane.SEPARATE for its own window
    params = {"period": 20, "percent": 0.5}
    plots = [
        Plot("upper", "Upper", color="#26a69a"),
        Plot("lower", "Lower", color="#ef5350"),
    ]

    def calculate(self, df):
        middle = mql5.sma(self.series(df, "close"), self.p.period)
        band = middle * self.p.percent / 100.0
        return {"upper": middle + band, "lower": middle - band}
```

`calculate` returns one array per plot, aligned to the bars, NaN where the
value is undefined. Draw styles are `LINE`, `ARROW`, `HISTOGRAM`, `FILL`
(a shaded band to another plot), `CANDLE_COLOR` (a colour slot per candle) and
`NONE`. Parameters take ints, floats, bools, or a `Choice` for a dropdown; a
plot can set `pane=Pane.PRICE` to sit on the candles while the rest of the
indicator lives in its own window.

[`backtester/indicators/mql5.py`](backtester/indicators/mql5.py) carries the
MetaTrader maths the conversions share — moving averages in both the terminal's
and the mladen-family flavours, the full applied-price list including Heiken
Ashi, ATR, six RSI variants, and the noise filter.

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
- **Follow** scrolls the chart with the newest candle at a fixed zoom (it
  slides the window rather than compressing the candles, like MT5); pan or
  zoom to detach and inspect, tick Follow to snap back. **Shift** leaves blank
  space to the right of the newest candle. The crosshair readout only shows
  bars revealed so far — no peeking ahead.
- When the run finishes, the toolbar shows the summary (trades, net,
  profit factor, max drawdown), and the full breakdown opens in the Results tab.

If a dataset was downloaded before contract-spec capture was added, the
Backtest tab warns and assumes forex contract math — re-download the
dataset (any small range; it merges) to attach the broker's real spec.

Prefer results over animation? **⏩ Run Fast** executes the whole backtest on
a background thread with a progress bar, then draws the final chart (all
candles, every trade marker, full equity curve) and opens the Results tab.
Hit *Start Replay* afterwards to watch the same run animated — runs are
deterministic.

## Trade context logs

Tick **Log trade context data** and after the run every moment of every trade —
**entries, SL/TP modifications, and exits** — is written out as *data*: the bars
around it plus every indicator value the strategy computed, so a decision can be
inspected as numbers instead of eyeballed. It works the same for a replay or a
*Run Fast*, because logging is a post-run pass over the events the engine
recorded.

A run produces one folder, `trade_logs/<dataset>_<strategy>_<timestamp>/`:

| File | What's in it |
|---|---|
| `context.parquet` | every moment's window of bars, stacked into one table |
| `manifest.csv` | one row per moment — what happened and which window it wrote |
| `indicators.csv` | each indicator column and the call that produced it |

`context.parquet` is long-form: `frame_id` identifies the moment
(`0007_entry`, `0007_modify_01`, `0007_exit`), and `offset` is each bar's
distance from it — `0` is the moment itself, negative is history. So a whole run
loads in one `pd.read_parquet` and slices by trade:

```python
ctx = pd.read_parquet("trade_logs/GER40_H1_trailing_trend_20260727-2359/context.parquet")
ctx.columns
# frame_id, trade_id, kind, event_index, bar_index, offset,
# time, open, high, low, close, tick_volume, spread, real_volume, trend, rng

ctx[ctx.frame_id == "0001_modify_05"].tail(3)
#       frame_id   kind  bar_index  offset                time    close    trend      rng
# 0001_modify_05 modify        111      -2 2024-01-05 15:00:00 1.090920 1.088227 0.001609
# 0001_modify_05 modify        112      -1 2024-01-05 16:00:00 1.091865 1.088370 0.001633
# 0001_modify_05 modify        113       0 2024-01-05 17:00:00 1.092833 1.088545 0.001657
```

Indicator columns are named after the strategy's own attributes — `self.trend`
becomes `trend` — and `indicators.csv` says what each one was:

```
column,attribute,recipe
trend,trend,"ema(50, Close)"
rng,rng,atr(14)
```

`manifest.csv` carries trade id, kind, bar index, time, direction, lots, price,
SL/TP (plus the previous levels for a modification), net, close reason, and the
window each moment logged.

**Trade log…** configures it: which moments to log, the **context window**, and
a **max moments per run** cap (1,000 by default — a trailing stop modifies its
SL on most bars, so a 273-trade GER40 run produces ~1,470 moments). The window
is either:

- **Last N bars** (120 by default) — ending *at* the moment, so the log holds
  only what the strategy could see, no look-ahead; or
- **Whole day** — every bar of that calendar day, which does include what came
  after the moment. It's a review tool, not a decision input, and `offset > 0`
  marks those bars.

Manual sessions don't log — the decisions were yours, and there are no indicator
series behind them.

## Manual trading (an alternative to watching the replay)

The Backtest tab's **Mode** selector chooses how a run plays out:

- **Strategy replay** — watch a strategy trade (everything described above).
- **Manual trading** — *you* place and manage the trades as the chart replays.

Switching to Manual swaps the strategy picker and parameter form for an
order-entry panel (*Run Fast* disappears — you're the strategy now). Set
balance/spread/commission as usual and hit **Start Manual Session**: the replay
warms up ~100 bars so you have context, then hands over **paused**:

- **Three draggable lines** set the trade: a silver **Entry**, a green **Take
  profit**, and a red **Stop loss**. TP and SL each have a checkbox — a trade
  needs neither. The entry line tracks the live price by default; drag it to
  place it yourself (that pins it), and for a pending order it is the trigger.
- **Order type** is explicit: *Market* fills at the next bar's open, *Pending*
  places a stop/limit at the entry line (the kind is derived from which side of
  price the line sits).
- **Position size** three ways: a **% of balance** to risk, a **fixed cash**
  risk, or a **fixed lot size**. The risk modes size the trade from the stop
  distance (`lots = risk ÷ (stop distance × contract size)`) and therefore need
  an SL; without one, use fixed lots. A live preview spells out exactly what
  will be placed — order type, price, lots, and cash at risk — before you click.
- **Manage the trade**: drag the SL/TP lines to move them on the live position
  (the same call a strategy's trailing stop makes), **Close position** to exit
  at the next open, or **Cancel pending**.
- **Playback** is the same toolbar as the strategy replay: Play/Pause, **Step**
  one candle at a time, and a **speed slider** (1–250 bars/s), with *Follow*
  keeping the chart on price.

Orders go through the same simulated broker as automated strategies, so fills,
SL/TP, spread, commission, swap, and the equity curve behave identically. When
the replay reaches the end of the data, the session's trades and statistics
open in the Results tab, labelled as a manual session.

> Sizing depends on the instrument's contract spec. If a dataset was downloaded
> before spec capture existed, the tab says so and falls back to forex maths —
> re-download it (any small range; it merges). If the smallest tradeable lot
> would risk more than you asked for, the preview flags it rather than quietly
> sizing you up.

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
speed, trade log options, and window size are remembered between sessions.

## Optimizer tab

Grid-search a strategy's parameters to find robust settings:

- Check the parameters to sweep and give each a **From / To / Step**;
  unchecked parameters stay at their default. The total combination count is
  the product of the swept ranges (capped at 5,000).
- Choose what to **rank by** — net profit, profit factor, expectancy, win
  rate, Sharpe, or (ascending) max drawdown.
- **Workers** fans the grid across CPU processes (0 = run in-process). A few
  thousand combinations finish in seconds on a typical machine.
- Results fill a sortable table (parameter columns + key stats); **double-
  click a row to load those parameters into the Backtest tab** and replay or
  fast-run them.

Account settings (balance, spread, commission) are taken from the Backtest
tab's last-used values.

## Custom strategies

Drop a `.py` file in the **`strategies/`** folder (next to the app, or next
to the `.exe` in a packaged build) and every `Strategy` subclass in it appears
in the Backtest and Optimizer tabs as `filename.ClassName`. Click **Reload
strategies** to pick up edits without restarting (source is recompiled fresh,
so same-size edits are never missed). The bundled
[`strategies/trailing_trend.py`](strategies/trailing_trend.py) is an EMA trend
rider with an ATR trailing stop — a good one to watch in the replay, where the
stop line visibly trails price.

Custom strategies also work from the CLI: `--strategy trailing_trend.TrailingTrend`.

## Intrabar precision

By default, when both SL and TP fall inside one bar the engine assumes the SL
hit first (pessimistic — OHLC bars hide the intrabar path). If you also have a
**finer-timeframe dataset of the same symbol** (e.g. M5 or M1 alongside H1),
select it under **Intrabar** in the Backtest tab (or `--intrabar M5` on the
CLI) and SL/TP and pending-order triggers are resolved sub-bar by sub-bar for
a truthful answer to "which was hit first". Main bars not covered by the finer
data fall back to single-bar resolution automatically.

## Run a backtest (CLI)

The engine is GUI-independent; run it from the command line against any
dataset in your library:

```powershell
python run_backtest.py EURUSD H1
python run_backtest.py GER40 H1 --strategy ma_cross --param fast=12 --param slow=48 --trades 10
python run_backtest.py XAUUSD M15 --strategy rsi_reversion --commission 7 --balance 5000
python run_backtest.py GER40 H1 --strategy trailing_trend.TrailingTrend --trade-log day
```

Trade context logs work headlessly too: `--trade-log` (or `--trade-log day`)
writes the same folder the GUI does, with `--log-bars` for the window size and
`--log-dir` for where it goes.

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
buy_stop/sell_stop`, `modify(position, sl=…, tp=…)` (e.g. trailing stops),
`close(position)` / `close_all()`, indicators via `self.ind` (`sma, ema, rsi,
atr, highest, lowest`), and `cross_over/cross_under` helpers. Price series are
`self.opens/highs/lows/closes` and `self.time` (plural, so they don't shadow
the `self.close(position)` method); the current bar index is `self.i`.

Price-based indicators take an **applied price** — `self.ind.ema(20,
applied=AppliedPrice.TYPICAL)` (`from backtester.strategy.indicators import
AppliedPrice`). Options: `CLOSE` (default), `OPEN`, `HIGH`, `LOW`, `MEDIAN`
(HL/2), `TYPICAL` (HLC/3), `WEIGHTED` (HLCC/4). ATR is High/Low/Close-based
and ignores it.

### Execution model

- Bars are **bid** prices (MT5 convention): longs open at ask (bid + spread)
  and close at bid; shorts the reverse. Spread comes from the data's spread
  column, or a fixed `--spread` in points.
- Strategy decisions happen on a bar's close; market orders fill at the next
  bar's open. SL/TP and pending triggers are evaluated against each bar's
  high/low; a level gapped over at the open fills at the open.
- If SL and TP both fall inside one bar, **SL is assumed to hit first**
  (pessimistic — OHLC bars can't reveal the intrabar path). Supply finer-
  timeframe data (see *Intrabar precision*) to resolve this from data.
- Commission is charged per side per lot; swap accrues per night held.

## Tests

```powershell
pytest
```

## Packaging a Windows app

Build a standalone one-folder application (no Python install needed to run it):

```powershell
pip install pyinstaller
pyinstaller packaging/backtester.spec --noconfirm
```

The result is `dist/PythonBacktester/`; run `PythonBacktester.exe`. The
`strategies/` and `indicators/` folders are bundled and also read from next to
the executable at runtime, so end users can drop in their own `.py` files
without a rebuild. The `data_library/` is created next to the app on first use.

## Notes

- Bar timestamps are stored in **MT5 server time** (as delivered by the
  terminal), naive (no timezone attached).
- Re-downloading a symbol/timeframe **merges** with existing data (duplicates
  dropped), so you can extend a dataset incrementally.
- If MT5 returns fewer bars than expected, raise *Max bars in chart* in the
  terminal under Tools → Options → Charts, and check your broker's history depth.
