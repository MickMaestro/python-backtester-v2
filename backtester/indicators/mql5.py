"""MQL5 runtime shim: the standard-library maths converted indicators lean on.

Everything an ``OnCalculate`` body typically reaches for — moving averages,
applied prices, ATR, RSI variants — with MetaTrader's exact formulas, written
forward-indexed (bar 0 = oldest) to match the rest of this app.

Two flavours of moving average live here, because MQL5 indicators use both:

- :func:`ma` is the terminal's ``iMA``: undefined (NaN) until it has a full
  window, which is what ``PLOT_DRAW_BEGIN`` reflects on a real chart.
- :func:`running_ma` is the hand-rolled "iCustomMa" found in the mladen-family
  indicators: defined from the very first bar over whatever window exists so
  far. Substituting one for the other shifts every value in the warm-up
  region, so each conversion uses the one its source did.

MT5 leaves uncalculated buffer entries as zero; here they are NaN. That is a
deliberate difference: comparisons against NaN are False, so a warm-up bar
produces no signal instead of a false one against a garbage zero.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

EMPTY = np.nan


# --------------------------------------------------------------- moving averages


def sma(values: np.ndarray, period: int) -> np.ndarray:
    if period <= 1:
        return np.asarray(values, dtype=float).copy()
    return pd.Series(values).rolling(period).mean().to_numpy()


def ema(values: np.ndarray, period: int) -> np.ndarray:
    """MT5's EMA: the recursion runs from the first bar, drawn from period-1."""
    if period <= 1:
        return np.asarray(values, dtype=float).copy()
    out = pd.Series(values).ewm(span=period, adjust=False).mean().to_numpy().copy()
    out[: period - 1] = EMPTY
    return out


def smma(values: np.ndarray, period: int) -> np.ndarray:
    """Smoothed/Wilder MA: seeded with the SMA of the first ``period`` bars."""
    values = np.asarray(values, dtype=float)
    if period <= 1:
        return values.copy()
    out = np.full(len(values), EMPTY)
    if len(values) < period:
        return out
    seed = float(np.mean(values[:period]))
    tail = pd.Series(np.concatenate([[seed], values[period:]]))
    smoothed = tail.ewm(alpha=1.0 / period, adjust=False).mean().to_numpy()
    out[period - 1 :] = smoothed
    return out


def lwma(values: np.ndarray, period: int) -> np.ndarray:
    """Linear weighted MA: newest bar carries weight ``period``."""
    values = np.asarray(values, dtype=float)
    if period <= 1:
        return values.copy()
    weights = np.arange(1.0, period + 1.0)
    convolved = np.convolve(values, weights[::-1], mode="full")[: len(values)]
    out = convolved / weights.sum()
    out[: period - 1] = EMPTY
    return out


def tema(values: np.ndarray, period: int) -> np.ndarray:
    """Triple EMA: ``3*e1 - 3*e2 + e3``."""
    values = np.asarray(values, dtype=float)
    if period <= 1:
        return values.copy()
    e1 = pd.Series(values).ewm(span=period, adjust=False).mean()
    e2 = e1.ewm(span=period, adjust=False).mean()
    e3 = e2.ewm(span=period, adjust=False).mean()
    out = (3.0 * e1 - 3.0 * e2 + e3).to_numpy().copy()
    out[: period - 1] = EMPTY
    return out


MA_METHODS = ("sma", "ema", "smma", "lwma", "tema")


def ma(values: np.ndarray, period: int, method: str = "sma") -> np.ndarray:
    """``iMA`` — dispatch by method name."""
    return {
        "sma": sma, "ema": ema, "smma": smma, "lwma": lwma, "tema": tema,
    }[str(method).lower()](values, period)


# ------------------------------------------------- running ("iCustomMa") variants


def running_sma(values: np.ndarray, period: int) -> np.ndarray:
    """SMA over an expanding window until ``period`` bars exist."""
    values = np.asarray(values, dtype=float)
    if period <= 1:
        return values.copy()
    out = pd.Series(values).rolling(period, min_periods=1).mean().to_numpy()
    return out


def running_ema(values: np.ndarray, period: float) -> np.ndarray:
    """EMA seeded with the first bar's value — no NaN warm-up."""
    values = np.asarray(values, dtype=float)
    if period <= 1:
        return values.copy()
    alpha = 2.0 / (1.0 + period)
    return pd.Series(values).ewm(alpha=alpha, adjust=False).mean().to_numpy().copy()


def running_smma(values: np.ndarray, period: float, start: int | None = None) -> np.ndarray:
    """Smoothed MA that copies the price until the recursion starts.

    ``start`` is the first bar that smooths (the mladen indicators disagree on
    it: the Gann activator waits ``period`` bars, the RSI one starts at 2).
    """
    values = np.asarray(values, dtype=float)
    if period <= 1:
        return values.copy()
    start = int(period) if start is None else start
    start = max(1, min(start, len(values)))
    out = values.copy()
    if start < len(values):
        tail = pd.Series(values[start - 1 :])
        out[start - 1 :] = (
            tail.ewm(alpha=1.0 / period, adjust=False).mean().to_numpy()
        )
    return out


def running_lwma(values: np.ndarray, period: int) -> np.ndarray:
    """LWMA over an expanding window, weights ``period`` … ``period-k``."""
    values = np.asarray(values, dtype=float)
    if period <= 1:
        return values.copy()
    out = lwma(values, period)
    # Head: only the bars that exist, with the weights they would have had.
    for i in range(min(period - 1, len(values))):
        weights = np.arange(period, period - i - 1, -1.0)
        out[i] = float(np.dot(weights, values[i::-1][: len(weights)]) / weights.sum())
    return out


def running_tema(values: np.ndarray, period: float) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    if period <= 1:
        return values.copy()
    alpha = 2.0 / (1.0 + period)
    e1 = pd.Series(values).ewm(alpha=alpha, adjust=False).mean()
    e2 = e1.ewm(alpha=alpha, adjust=False).mean()
    e3 = e2.ewm(alpha=alpha, adjust=False).mean()
    return (e3 + 3.0 * (e1 - e2)).to_numpy().copy()


def running_ma(values: np.ndarray, period: float, method: str = "ema") -> np.ndarray:
    return {
        "sma": running_sma, "ema": running_ema, "smma": running_smma,
        "lwma": running_lwma, "tema": running_tema,
    }[str(method).lower()](values, period)


def shift_forward(values: np.ndarray, bars: int) -> np.ndarray:
    """MT5's MA ``shift``: move the series ``bars`` to the right."""
    values = np.asarray(values, dtype=float)
    if bars == 0:
        return values.copy()
    out = np.full(len(values), EMPTY)
    if bars > 0:
        if bars < len(values):
            out[bars:] = values[: len(values) - bars]
    else:
        out[:bars] = values[-bars:]
    return out


def previous(values: np.ndarray) -> np.ndarray:
    """The value one bar back — MQL5's ``buffer[bar+1]`` in series indexing."""
    return shift_forward(values, 1)


# ------------------------------------------------------------------ applied price

#: MT5's ENUM_APPLIED_PRICE plus the extended set the mladen indicators use.
PRICES = (
    "close", "open", "high", "low", "median", "typical", "weighted",
    "average", "median_body", "trend_biased", "trend_biased_extreme",
)
#: ENUM_APPLIED_PRICE ordinals, for sources that pass the raw integer.
MT5_PRICE_BY_INDEX = {
    0: "close", 1: "close", 2: "open", 3: "high", 4: "low",
    5: "median", 6: "typical", 7: "weighted",
}


def heiken_ashi(df: pd.DataFrame, better: bool = False) -> dict[str, np.ndarray]:
    """Heiken Ashi O/H/L/C. ``better`` uses the body-weighted close variant."""
    o = df["open"].to_numpy(dtype=float)
    h = df["high"].to_numpy(dtype=float)
    l = df["low"].to_numpy(dtype=float)
    c = df["close"].to_numpy(dtype=float)
    n = len(o)

    if better:
        span = h - l
        body = c - o
        with np.errstate(divide="ignore", invalid="ignore"):
            ratio = np.where(span != 0, body / np.where(span == 0, 1.0, span), 0.0)
        ha_close = (o + c) / 2.0 + ratio * np.abs(body / 2.0)
        ha_close = np.where(span != 0, ha_close, (o + c) / 2.0)
    else:
        ha_close = (o + h + l + c) / 4.0

    ha_open = np.empty(n)
    if n:
        ha_open[0] = (o[0] + c[0]) / 2.0
        # Recursive by definition: each open is the previous candle's midpoint.
        for i in range(1, n):
            ha_open[i] = (ha_open[i - 1] + ha_close[i - 1]) / 2.0
    ha_high = np.maximum(h, np.maximum(ha_open, ha_close))
    ha_low = np.minimum(l, np.minimum(ha_open, ha_close))
    return {"open": ha_open, "high": ha_high, "low": ha_low, "close": ha_close}


def _combine(name: str, o, h, l, c) -> np.ndarray:
    if name == "close":
        return c
    if name == "open":
        return o
    if name == "high":
        return h
    if name == "low":
        return l
    if name == "median":
        return (h + l) / 2.0
    if name == "typical":
        return (h + l + c) / 3.0
    if name == "weighted":
        return (h + l + 2.0 * c) / 4.0
    if name == "average":
        return (h + l + c + o) / 4.0
    if name == "median_body":
        return (o + c) / 2.0
    if name == "trend_biased":
        return np.where(c > o, (h + c) / 2.0, (l + c) / 2.0)
    if name == "trend_biased_extreme":
        return np.where(c > o, h, np.where(c < o, l, c))
    raise ValueError(f"Unknown applied price: {name!r}")


def applied_price(df: pd.DataFrame, price) -> np.ndarray:
    """A price series by name.

    Accepts the plain names in :data:`PRICES`, an ``ha_``/``hab_`` prefix for
    the Heiken Ashi and "better formula" variants, or an ENUM_APPLIED_PRICE
    ordinal.
    """
    if isinstance(price, (int, np.integer)) and not isinstance(price, bool):
        price = MT5_PRICE_BY_INDEX.get(int(price), "close")
    name = str(price).lower()

    if name.startswith(("ha_", "hab_")):
        better = name.startswith("hab_")
        ha = heiken_ashi(df, better=better)
        return _combine(
            name.split("_", 1)[1], ha["open"], ha["high"], ha["low"], ha["close"]
        )
    return _combine(
        name,
        df["open"].to_numpy(dtype=float),
        df["high"].to_numpy(dtype=float),
        df["low"].to_numpy(dtype=float),
        df["close"].to_numpy(dtype=float),
    )


#: Every applied price a converted indicator can offer, label included.
PRICE_CHOICES = {
    **{name: name.replace("_", " ").title() for name in PRICES},
    **{f"ha_{name}": f"Heiken Ashi {name.replace('_', ' ').title()}" for name in PRICES},
    **{
        f"hab_{name}": f"Heiken Ashi (better) {name.replace('_', ' ').title()}"
        for name in PRICES
    },
}


# ------------------------------------------------------------------------ ranges


def true_range(high, low, close) -> np.ndarray:
    prev_close = shift_forward(np.asarray(close, dtype=float), 1)
    high = np.asarray(high, dtype=float)
    low = np.asarray(low, dtype=float)
    ranges = np.vstack(
        [high - low, np.abs(high - prev_close), np.abs(low - prev_close)]
    )
    out = np.nanmax(ranges, axis=0)
    return out


def atr(high, low, close, period: int = 14) -> np.ndarray:
    """MT5's ``iATR``: a smoothed average of true range."""
    tr = true_range(high, low, close)
    out = np.full(len(tr), EMPTY)
    if len(tr) <= period:
        return out
    seed = float(np.mean(tr[1 : period + 1]))
    tail = pd.Series(np.concatenate([[seed], tr[period + 1 :]]))
    out[period:] = tail.ewm(alpha=1.0 / period, adjust=False).mean().to_numpy()
    return out


def highest(values: np.ndarray, period: int) -> np.ndarray:
    return pd.Series(values).rolling(period, min_periods=1).max().to_numpy()


def lowest(values: np.ndarray, period: int) -> np.ndarray:
    return pd.Series(values).rolling(period, min_periods=1).min().to_numpy()


# -------------------------------------------------------------------------- RSI

RSI_METHODS = ("rsi", "slow", "rapid", "harris", "rsx", "cuttler")


def rsi_variant(values: np.ndarray, period: float, method: str = "rsi") -> np.ndarray:
    """The six RSI flavours the mladen "RSI MA" family offers.

    ``rsi`` is that family's smoothed change/absolute-change ratio, not
    Wilder's classic formula — it is what the source computes.
    """
    values = np.asarray(values, dtype=float)
    n = len(values)
    out = np.full(n, 50.0)
    period = max(float(period), 1.0)
    method = str(method).lower()

    if method == "rsi":
        alpha = 1.0 / period
        change = np.zeros(n)
        changa = np.zeros(n)
        span = int(period)
        for i in range(n):
            if i < span:
                k = 0
                total = 0.0
                while k < span and (i - k - 1) >= 0:
                    total += abs(values[i - k] - values[i - k - 1])
                    k += 1
                change[i] = (values[i] - values[0]) / max(k, 1)
                changa[i] = total / max(k, 1)
            else:
                delta = values[i] - values[i - 1]
                change[i] = change[i - 1] + alpha * (delta - change[i - 1])
                changa[i] = changa[i - 1] + alpha * (abs(delta) - changa[i - 1])
            out[i] = 50.0 * (change[i] / changa[i] + 1.0) if changa[i] != 0 else 50.0
        return out

    diff = np.diff(values, prepend=values[:1])
    gains = np.where(diff > 0, diff, 0.0)
    losses = np.where(diff < 0, -diff, 0.0)
    span = int(period)

    if method in ("rapid", "cuttler"):
        up = pd.Series(gains).rolling(span, min_periods=1).sum().to_numpy()
        dn = pd.Series(losses).rolling(span, min_periods=1).sum().to_numpy()
        if method == "rapid":
            total = up + dn
            return np.where(total == 0, 50.0, 100.0 * up / np.where(total == 0, 1, total))
        return np.where(dn > 0, 100.0 - 100.0 / (1.0 + up / np.where(dn == 0, 1, dn)), 50.0)

    if method == "harris":
        ups = pd.Series(gains).rolling(span, min_periods=1).sum().to_numpy()
        dns = pd.Series(losses).rolling(span, min_periods=1).sum().to_numpy()
        up_count = pd.Series((diff > 0).astype(float)).rolling(span, min_periods=1).sum().to_numpy()
        dn_count = pd.Series((diff < 0).astype(float)).rolling(span, min_periods=1).sum().to_numpy()
        avg_up = np.where(up_count > 0, ups / np.where(up_count == 0, 1, up_count), 0.0)
        avg_dn = np.where(dn_count > 0, dns / np.where(dn_count == 0, 1, dn_count), 0.0)
        rs = np.where(avg_dn != 0, avg_up / np.where(avg_dn == 0, 1, avg_dn), 1.0)
        return 100.0 - 100.0 / (1.0 + rs)

    if method == "slow":
        up = pd.Series(gains).rolling(span, min_periods=1).sum().to_numpy()
        dn = pd.Series(losses).rolling(span, min_periods=1).sum().to_numpy()
        total = up + dn
        target = np.where(total == 0, 50.0, 100.0 * up / np.where(total == 0, 1, total))
        value = 50.0
        for i in range(n):
            if i < 1:
                out[i] = 50.0
            else:
                value = value + (1.0 / period) * (target[i] - value)
                out[i] = value
            value = out[i]
        return out

    if method == "rsx":
        kg = 3.0 / (2.0 + period)
        hg = 1.0 - kg
        work = np.zeros((n, 13))
        span = int(period)
        for i in range(n):
            if i < span:
                out[i] = 50.0
                continue
            mom = values[i] - values[i - 1]
            moa = abs(mom)
            for k in range(3):
                kk = k * 2
                work[i][kk + 1] = kg * mom + hg * work[i - 1][kk + 1]
                work[i][kk + 2] = kg * work[i][kk + 1] + hg * work[i - 1][kk + 2]
                mom = 1.5 * work[i][kk + 1] - 0.5 * work[i][kk + 2]
                work[i][kk + 7] = kg * moa + hg * work[i - 1][kk + 7]
                work[i][kk + 8] = kg * work[i][kk + 7] + hg * work[i - 1][kk + 8]
                moa = 1.5 * work[i][kk + 7] - 0.5 * work[i][kk + 8]
            out[i] = min(max((mom / moa + 1.0) * 50.0, 0.0), 100.0) if moa != 0 else 50.0
        return out

    raise ValueError(f"Unknown RSI method: {method!r}")


# ----------------------------------------------------------------------- filters


def noise_filter(values: np.ndarray, period: int, factor: float) -> np.ndarray:
    """mladen's ``iFilter``: hold the previous value while the change is small.

    A bar moves the output only when |change| is at least ``factor`` standard
    deviations of the recent change; otherwise the last value is carried.
    """
    values = np.asarray(values, dtype=float)
    if factor <= 0 or period <= 0:
        return values.copy()
    out = values.copy()
    changes = np.abs(np.diff(values, prepend=values[:1]))
    changes[0] = 0.0
    avg = pd.Series(changes).rolling(period, min_periods=1).mean().to_numpy()
    deviation = np.sqrt(
        pd.Series((changes - avg) ** 2).rolling(period, min_periods=1).mean().to_numpy()
    )
    threshold = factor * deviation
    for i in range(1, len(values)):
        if abs(values[i] - out[i - 1]) < threshold[i]:
            out[i] = out[i - 1]
    return out


# ------------------------------------------------------------------- colouring


def segments(values: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """``values`` where ``mask`` holds, NaN elsewhere — but keeping the bar
    *before* each run so coloured stretches join up instead of leaving a gap
    at every state change. This is what MQL5 indicators hand-roll as
    ``PlotPoint``/``CleanPoint`` pairs of buffers.
    """
    values = np.asarray(values, dtype=float)
    mask = np.asarray(mask, dtype=bool)
    keep = mask.copy()
    keep[:-1] |= mask[1:]
    return np.where(keep, values, EMPTY)


# ------------------------------------------------------------------ time helpers


def day_index(df: pd.DataFrame) -> np.ndarray:
    """A 0-based index of the calendar day each bar belongs to."""
    days = df["time"].to_numpy().astype("datetime64[D]")
    _, index = np.unique(days, return_inverse=True)
    return index


def daily_ohlc(df: pd.DataFrame) -> dict[str, np.ndarray]:
    """Per-day open/high/low/close aggregates, indexed by :func:`day_index`."""
    days = day_index(df)
    frame = pd.DataFrame(
        {
            "day": days,
            "open": df["open"].to_numpy(dtype=float),
            "high": df["high"].to_numpy(dtype=float),
            "low": df["low"].to_numpy(dtype=float),
            "close": df["close"].to_numpy(dtype=float),
        }
    )
    grouped = frame.groupby("day", sort=True)
    return {
        "open": grouped["open"].first().to_numpy(),
        "high": grouped["high"].max().to_numpy(),
        "low": grouped["low"].min().to_numpy(),
        "close": grouped["close"].last().to_numpy(),
    }


def running_daily(df: pd.DataFrame) -> dict[str, np.ndarray]:
    """Day-so-far open/high/low/close at every bar (no look-ahead).

    MT5's ``iHigh(symbol, PERIOD_D1, 0)`` is the day *as it stands now*; on a
    historical chart that has to be the day up to this bar, not the finished
    day, or every value would be lit by hindsight.
    """
    days = day_index(df)
    frame = pd.DataFrame(
        {
            "day": days,
            "open": df["open"].to_numpy(dtype=float),
            "high": df["high"].to_numpy(dtype=float),
            "low": df["low"].to_numpy(dtype=float),
            "close": df["close"].to_numpy(dtype=float),
        }
    )
    grouped = frame.groupby("day", sort=False)
    return {
        "open": grouped["open"].transform("first").to_numpy(),
        "high": grouped["high"].cummax().to_numpy(),
        "low": grouped["low"].cummin().to_numpy(),
        "close": frame["close"].to_numpy(),
        "index": days,
    }
