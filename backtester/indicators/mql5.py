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
    """MT5's ``iATR``: a simple moving average of true range.

    ATR.mq5 seeds bar ``period`` with the mean of the first ``period`` true
    ranges, then rolls ``atr[i-1] + (tr[i] - tr[i-period]) / period`` — a plain
    SMA, not Wilder's smoothing.
    """
    period = max(int(period), 1)
    tr = true_range(high, low, close)
    out = np.full(len(tr), EMPTY)
    if len(tr) <= period:
        return out
    out[period:] = pd.Series(tr[1:]).rolling(period).mean().to_numpy()[period - 1:]
    return out


def wpr(high, low, close, period: int = 14) -> np.ndarray:
    """MT5's ``iWPR``: -100 × (highest high − close) / range, held on a flat range."""
    period = max(int(period), 1)
    hh = pd.Series(high).rolling(period).max().to_numpy()
    ll = pd.Series(low).rolling(period).min().to_numpy()
    with np.errstate(divide="ignore", invalid="ignore"):
        out = -(hh - np.asarray(close, dtype=float)) * 100.0 / (hh - ll)
    out = np.where(hh == ll, np.nan, out)
    filled = pd.Series(out).ffill().to_numpy()
    filled[: period - 1] = EMPTY
    return filled


def cci(values: np.ndarray, period: int = 14) -> np.ndarray:
    """MT5's ``iCCI`` on an already-applied price series."""
    values = np.asarray(values, dtype=float)
    period = max(int(period), 1)
    n = len(values)
    out = np.full(n, EMPTY)
    if n < period:
        return out
    mean = sma(values, period)
    windows = np.lib.stride_tricks.sliding_window_view(values, period)
    centre = mean[period - 1:][:, None]
    dev = np.sum(np.abs(windows - centre), axis=1) * 0.015 / period
    with np.errstate(divide="ignore", invalid="ignore"):
        result = np.where(dev != 0, (values[period - 1:] - mean[period - 1:]) / dev, 0.0)
    out[period - 1:] = result
    return out


def rsi(values: np.ndarray, period: int = 14) -> np.ndarray:
    """MT5's ``iRSI``: Wilder smoothing seeded with the plain average of the
    first ``period`` changes."""
    values = np.asarray(values, dtype=float)
    period = max(int(period), 1)
    n = len(values)
    out = np.full(n, EMPTY)
    if n <= period:
        return out
    diff = np.diff(values, prepend=values[0])
    gains = np.where(diff > 0, diff, 0.0)
    losses = np.where(diff < 0, -diff, 0.0)
    pos = np.empty(n)
    neg = np.empty(n)
    pos[period] = gains[1: period + 1].mean()
    neg[period] = losses[1: period + 1].mean()
    for i in range(period + 1, n):
        pos[i] = (pos[i - 1] * (period - 1) + gains[i]) / period
        neg[i] = (neg[i - 1] * (period - 1) + losses[i]) / period
    p = pos[period:]
    m = neg[period:]
    with np.errstate(divide="ignore", invalid="ignore"):
        out[period:] = np.where(m != 0, 100.0 - 100.0 / (1.0 + p / m),
                                np.where(p != 0, 100.0, 50.0))
    return out


def momentum(values: np.ndarray, period: int = 14) -> np.ndarray:
    """MT5's ``iMomentum``: price / price ``period`` bars ago × 100."""
    values = np.asarray(values, dtype=float)
    back = shift_forward(values, period)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(back != 0, values * 100.0 / back, EMPTY)


def stddev(values: np.ndarray, period: int = 20, method: str = "sma") -> np.ndarray:
    """MT5's ``iStdDev``: deviation from the chosen MA over ``period`` bars."""
    values = np.asarray(values, dtype=float)
    period = max(int(period), 1)
    n = len(values)
    out = np.full(n, EMPTY)
    if n < period:
        return out
    centre = ma(values, period, method)
    windows = np.lib.stride_tricks.sliding_window_view(values, period)
    out[period - 1:] = np.sqrt(np.mean((windows - centre[period - 1:][:, None]) ** 2, axis=1))
    return out


def stochastic(high, low, close, k_period: int = 5, d_period: int = 3,
               slowing: int = 3, method: str = "sma") -> tuple[np.ndarray, np.ndarray]:
    """MT5's ``iStochastic`` (low/high price field): main and signal lines."""
    k_period = max(int(k_period), 1)
    slowing = max(int(slowing), 1)
    hh = pd.Series(high).rolling(k_period).max()
    ll = pd.Series(low).rolling(k_period).min()
    num = (pd.Series(close) - ll).rolling(slowing).sum()
    den = (hh - ll).rolling(slowing).sum()
    main = np.where(den.to_numpy() == 0, 100.0, (num / den).to_numpy() * 100.0)
    main = np.where(np.isfinite(den.to_numpy()), main, EMPTY)
    start = int(np.argmax(np.isfinite(main))) if np.isfinite(main).any() else len(main)
    signal = np.full(len(main), EMPTY)
    if start < len(main):
        signal[start:] = ma(main[start:], d_period, method)
    return main, signal


def macd(values: np.ndarray, fast: int = 12, slow: int = 26, signal: int = 9):
    """MT5's ``iMACD``: EMA difference and an SMA signal line."""
    main = ema(values, fast) - ema(values, slow)
    start = int(np.argmax(np.isfinite(main))) if np.isfinite(main).any() else len(main)
    sig = np.full(len(main), EMPTY)
    if start < len(main):
        sig[start:] = sma(main[start:], signal)
    return main, sig


def sar(high, low, step: float = 0.02, maximum: float = 0.2) -> np.ndarray:
    """MT5's ``iSAR`` (ParabolicSAR.mq5). The value on bar i+1 is projected
    on bar i, and bar i+1 flips it if its own range crosses it.

    ParabolicSAR.mq5 leaves the newest bar unchecked because live it is still
    forming; on history every bar is closed, so every bar is checked — its
    flip uses only that bar's own high/low."""
    high = np.asarray(high, dtype=float)
    low = np.asarray(low, dtype=float)
    n = len(high)
    out = np.full(n, EMPTY)
    if n < 3:
        return out
    af = np.zeros(n)
    ep = np.zeros(n)
    af[0] = af[1] = step
    out[0] = high[0]
    last_rev = 0
    long_ = False
    out[1] = high[last_rev: 2].max()
    ep[0] = ep[1] = low[1]
    for i in range(1, n):
        if long_:
            if out[i] > low[i]:
                long_ = False
                out[i] = high[last_rev: i + 1].max()
                ep[i] = low[i]
                last_rev = i
                af[i] = step
        else:
            if out[i] < high[i]:
                long_ = True
                out[i] = low[last_rev: i + 1].min()
                ep[i] = high[i]
                last_rev = i
                af[i] = step
        if long_:
            if high[i] > ep[i - 1] and i != last_rev:
                ep[i] = high[i]
                af[i] = min(af[i - 1] + step, maximum)
            elif i != last_rev:
                af[i], ep[i] = af[i - 1], ep[i - 1]
            if i + 1 < n:
                out[i + 1] = out[i] + af[i] * (ep[i] - out[i])
                if out[i + 1] > low[i] or out[i + 1] > low[i - 1]:
                    out[i + 1] = min(low[i], low[i - 1])
        else:
            if low[i] < ep[i - 1] and i != last_rev:
                ep[i] = low[i]
                af[i] = min(af[i - 1] + step, maximum)
            elif i != last_rev:
                af[i], ep[i] = af[i - 1], ep[i - 1]
            if i + 1 < n:
                out[i + 1] = out[i] + af[i] * (ep[i] - out[i])
                if out[i + 1] < high[i] or out[i + 1] < high[i - 1]:
                    out[i + 1] = max(high[i], high[i - 1])
    return out


def adx(high, low, close, period: int = 14) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """MT5's ``iADX``: (ADX, +DI, -DI), smoothed with EMA(period) as ADX.mq5 does."""
    high = np.asarray(high, dtype=float)
    low = np.asarray(low, dtype=float)
    close = np.asarray(close, dtype=float)
    n = len(high)
    pdi = np.full(n, EMPTY)
    mdi = np.full(n, EMPTY)
    out = np.full(n, EMPTY)
    if n < 2:
        return out, pdi, mdi
    up = np.r_[0.0, high[1:] - high[:-1]]
    dn = np.r_[0.0, low[:-1] - low[1:]]
    up = np.maximum(up, 0.0)
    dn = np.maximum(dn, 0.0)
    pdm = np.where(up > dn, up, 0.0)
    mdm = np.where(dn > up, dn, 0.0)
    tr = true_range(high, low, close)
    with np.errstate(divide="ignore", invalid="ignore"):
        p = np.where(tr != 0, 100.0 * pdm / tr, 0.0)
        m = np.where(tr != 0, 100.0 * mdm / tr, 0.0)
    alpha = 2.0 / (period + 1.0)

    def from_zero(x):
        # ADX.mq5's ExponentialMA recursion starts from a zeroed bar 0.
        return pd.Series(np.r_[0.0, x[1:]]).ewm(alpha=alpha, adjust=False).mean().to_numpy()

    pdi = from_zero(p)
    mdi = from_zero(m)
    total = pdi + mdi
    with np.errstate(divide="ignore", invalid="ignore"):
        dx = np.where(total != 0, 100.0 * np.abs(pdi - mdi) / total, 0.0)
    out = from_zero(dx)
    return out, pdi, mdi


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


# -------------------------------------------------------------------- zigzags


def zigzag(high, low, depth: int = 12, deviation: float = 0.0,
           backstep: int = 3, start: int | None = None) -> tuple[np.ndarray, np.ndarray]:
    """MetaQuotes' classic ZigZag (ZigZag.mq5 / ZigzagColor.mq5), full pass.

    Returns (peaks, troughs): NaN except at turning points. ``deviation`` is a
    price distance (the source's ``ExtDeviation * _Point``). A turning point
    only ever moves to a later bar, so each surviving one was already the
    leg's extreme on its own bar — known there, not before. ``start`` is the
    first bar scanned (``depth - 1`` in ZigZag.mq5, ``depth`` in the
    ZZOnBuffer library); pass the same array as high and low to zigzag a
    single series.
    """
    high = np.asarray(high, dtype=float)
    low = np.asarray(low, dtype=float)
    n = len(high)
    peaks = np.zeros(n)
    troughs = np.zeros(n)
    if n < 100:                  # the source draws nothing on short history
        return np.full(n, EMPTY), np.full(n, EMPTY)
    depth = max(int(depth), 1)
    backstep = max(int(backstep), 0)
    lowest_low = pd.Series(low).rolling(depth, min_periods=1).min().to_numpy()
    highest_high = pd.Series(high).rolling(depth, min_periods=1).max().to_numpy()
    low_map = np.zeros(n)
    high_map = np.zeros(n)
    last_low = last_high = 0.0
    # Never let the backstep look-back reach below bar 0 (Python would wrap).
    first = max(depth - 1 if start is None else int(start), backstep)
    for shift in range(first, n):
        val = lowest_low[shift]
        if val == last_low:
            val = 0.0
        else:
            last_low = val
            if low[shift] - val > deviation:
                val = 0.0
            else:
                for back in range(backstep, 0, -1):
                    res = low_map[shift - back]
                    if res != 0 and res > val:
                        low_map[shift - back] = 0.0
        low_map[shift] = val if low[shift] == val else 0.0

        val = highest_high[shift]
        if val == last_high:
            val = 0.0
        else:
            last_high = val
            if val - high[shift] > deviation:
                val = 0.0
            else:
                for back in range(backstep, 0, -1):
                    res = high_map[shift - back]
                    if res != 0 and res < val:
                        high_map[shift - back] = 0.0
        high_map[shift] = val if high[shift] == val else 0.0

    look_for = 0
    last_low = last_high = 0.0
    last_low_pos = last_high_pos = 0
    for shift in range(first, n):
        if look_for == 0:
            if last_low == 0 and last_high == 0:
                if high_map[shift] != 0:
                    last_high, last_high_pos, look_for = high[shift], shift, -1
                    peaks[shift] = last_high
                if low_map[shift] != 0:
                    last_low, last_low_pos, look_for = low[shift], shift, 1
                    troughs[shift] = last_low
        elif look_for == 1:
            if low_map[shift] != 0 and low_map[shift] < last_low and high_map[shift] == 0:
                troughs[last_low_pos] = 0.0
                last_low_pos, last_low = shift, low_map[shift]
                troughs[shift] = last_low
            if high_map[shift] != 0 and low_map[shift] == 0:
                last_high, last_high_pos, look_for = high_map[shift], shift, -1
                peaks[shift] = last_high
        else:
            if high_map[shift] != 0 and high_map[shift] > last_high and low_map[shift] == 0:
                peaks[last_high_pos] = 0.0
                last_high_pos, last_high = shift, high_map[shift]
                peaks[shift] = last_high
            if low_map[shift] != 0 and high_map[shift] == 0:
                last_low, last_low_pos, look_for = low_map[shift], shift, 1
                troughs[shift] = last_low
    return np.where(peaks != 0, peaks, EMPTY), np.where(troughs != 0, troughs, EMPTY)


def pivot_line(pivots: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """A zigzag through ``pivots`` (NaN except at turning points), drawable as
    an ordinary line, plus the bar each point becomes known.

    MT5 draws ``DRAW_ZIGZAG``/``DRAW_SECTION`` by joining non-empty values. A
    final pivot was already the leg's running extreme on its own bar, so it is
    known there; the straight run *between* two pivots depends on the later
    one, so it is known only once that pivot prints. Feeding ``known`` to
    ``Plot.known_at`` keeps the replay from drawing a leg before it exists.
    """
    pivots = np.asarray(pivots, dtype=float)
    n = len(pivots)
    line = np.full(n, EMPTY)
    known = np.full(n, np.inf)
    idx = np.nonzero(np.isfinite(pivots))[0]
    if len(idx) == 0:
        return line, known
    line[idx[0]: idx[-1] + 1] = np.interp(
        np.arange(idx[0], idx[-1] + 1), idx, pivots[idx]
    )
    known[idx] = idx
    for a, b in zip(idx[:-1], idx[1:]):
        known[a + 1: b] = b
    return line, known


def leg_colors(pivots: np.ndarray, slots: np.ndarray) -> np.ndarray:
    """Colour slot for every bar of a zigzag leg, taken from the slot at the
    leg's closing pivot (how ``DRAW_COLOR_ZIGZAG`` colours a section)."""
    pivots = np.asarray(pivots, dtype=float)
    out = np.full(len(pivots), EMPTY)
    idx = np.nonzero(np.isfinite(pivots))[0]
    for a, b in zip(idx[:-1], idx[1:]):
        out[a + 1: b + 1] = slots[b]
    return out


# ------------------------------------------------------------ instrument precision


def digits(df: pd.DataFrame) -> int:
    """MQL5's ``_Digits``: from the dataset's stored spec, else inferred as the
    fewest decimals that represent every price exactly."""
    stored = df.attrs.get("digits")
    if stored is not None:
        return int(stored)
    prices = df[["open", "high", "low", "close"]].to_numpy(dtype=float).ravel()
    prices = prices[np.isfinite(prices)][:5000]
    for d in range(0, 9):
        scaled = prices * 10.0**d
        if np.all(np.abs(scaled - np.round(scaled)) < 1e-6):
            return d
    return 5


def point(df: pd.DataFrame) -> float:
    """MQL5's ``_Point``: the stored spec's point, else 10^-digits."""
    stored = df.attrs.get("point")
    if stored:
        return float(stored)
    return 10.0 ** -digits(df)


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
