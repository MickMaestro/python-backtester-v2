"""Nikolay Kositsin's ``SmoothAlgorithms.mqh`` — the ``CXMA`` smoothing family
used by the GODZILLA-era indicators (Candles_Smoothed, Heiken_Ashi_Smoothed,
ColorJFatl, SlopeDirectionLine, ColorRSI-MACD, T3, …).

Each function takes a forward-indexed series that is valid from ``begin`` on
and returns the smoothed series, NaN where the library returns EMPTY_VALUE.
The library's ``BarCheck4/5`` save-and-restore of state around the forming
bar only matters for live ticks and is not reproduced.

Start offsets follow the library exactly — e.g. its LWMA starts one bar
later than a textbook LWMA, and JJMA needs 30 bars before its first value —
because indicators chain these and size their warm-up from ``GetStartBars``.
"""

from __future__ import annotations

import math

import numpy as np
import pandas as pd

from .base import Choice

EMPTY = np.nan

#: ``Smooth_Method`` in its declared order.
METHODS = ("sma", "ema", "smma", "lwma", "jjma", "jurx", "parma", "t3", "vidya", "ama")
METHOD_LABELS = {
    "sma": "SMA", "ema": "EMA", "smma": "SMMA", "lwma": "LWMA",
    "jjma": "JJMA (Jurik)", "jurx": "JurX", "parma": "ParMA (parabolic)",
    "t3": "T3 (Tillson)", "vidya": "VIDYA", "ama": "AMA (Kaufman)",
}


def method_choice(default: str = "sma") -> Choice:
    return Choice(METHOD_LABELS, default=default)


def start_bars(method: str, length: int, phase: int) -> int:
    """``CXMA::GetStartBars`` — bars a method needs before its first value."""
    return {
        "sma": length, "ema": 0, "smma": length + 1, "lwma": length,
        "jjma": 30, "jurx": 0, "parma": length, "t3": 0,
        "vidya": phase + 2, "ama": length + 2,
    }[method]


def xma(values: np.ndarray, method: str, length: int, phase: int = 0,
        begin: int = 0) -> np.ndarray:
    """``CXMA::XMASeries`` over a whole series.

    ``phase`` means different things per method, as in the library: JJMA's
    phase (−100…100), T3's curvature (×0.01), VIDYA's CMO period, AMA's slow
    period.
    """
    values = np.asarray(values, dtype=float)
    length = max(int(length), 1)
    begin = max(int(begin), 0)
    if method == "sma":
        return sma(values, length, begin)
    if method == "ema":
        return ema(values, length, begin)
    if method == "smma":
        return smma(values, length, begin)
    if method == "lwma":
        return lwma(values, length, begin)
    if method == "jjma":
        return jjma(values, length, phase, begin)
    if method == "jurx":
        return jurx(values, length, begin)
    if method == "parma":
        return parma(values, length, begin)
    if method == "t3":
        return t3(values, length, phase, begin)
    if method == "vidya":
        return vidya(values, max(int(phase), 1), length, begin)
    if method == "ama":
        return ama(values, length, 2, max(int(phase), 1), 2.0, begin)
    raise ValueError(f"Unknown smoothing method: {method!r}")


# ----------------------------------------------------------- classic averages


def _tail(values: np.ndarray, begin: int) -> pd.Series:
    return pd.Series(values[begin:])


def sma(values, length: int, begin: int = 0) -> np.ndarray:
    out = np.full(len(values), EMPTY)
    if begin < len(values):
        out[begin:] = _tail(values, begin).rolling(length).mean().to_numpy()
    return out


def ema(values, length: float, begin: int = 0) -> np.ndarray:
    out = np.full(len(values), EMPTY)
    if begin < len(values):
        alpha = 2.0 / (max(float(length), 1.0) + 1.0)
        out[begin:] = _tail(values, begin).ewm(alpha=alpha, adjust=False).mean().to_numpy()
    return out


def smma(values, length: int, begin: int = 0) -> np.ndarray:
    """Seeded with the SMA of the first ``length`` bars, then (prev·(L−1)+x)/L."""
    values = np.asarray(values, dtype=float)
    n = len(values)
    out = np.full(n, EMPTY)
    first = begin + length - 1
    if first >= n:
        return out
    out[first] = float(np.mean(values[begin: first + 1]))
    if length == 1:
        out[first:] = values[first:]
        return out
    for i in range(first + 1, n):
        out[i] = (out[i - 1] * (length - 1) + values[i]) / length
    return out


def lwma(values, length: int, begin: int = 0) -> np.ndarray:
    """Weights ``length``…1, newest heaviest; the library's first value comes
    at ``begin + length`` (it primes a ``length+1`` ring first)."""
    values = np.asarray(values, dtype=float)
    n = len(values)
    out = np.full(n, EMPTY)
    first = begin + length
    if first >= n:
        return out
    weights = np.arange(1.0, length + 1.0)             # oldest → newest
    windows = np.lib.stride_tricks.sliding_window_view(values[begin:], length)
    result = windows @ weights / weights.sum()          # row k ends at begin+k+length-1
    out[begin + length - 1:] = result
    out[:first] = EMPTY
    return out


# --------------------------------------------------------------- Jurik family


def jjma(values, length: float, phase: float, begin: int = 0) -> np.ndarray:
    """``CJJMA::JJMASeries`` — Jurik's JMA as the library implements it."""
    values = np.asarray(values, dtype=float)
    n = len(values)
    out = np.full(n, EMPTY)
    if begin >= n:
        return out

    # JJMAInit
    if -100 <= phase <= 100:
        k_phase = phase / 100.0 + 1.5
    else:
        k_phase = 2.5 if phase > 100 else 0.5
    vel_a = (length - 1.0) / 2.0 if length >= 1.0000000002 else 0.0000000001
    vel_a *= 0.9
    krj = vel_a / (vel_a + 2.0)
    vel_c = math.sqrt(vel_a)
    sense = math.log(vel_c) / math.log(2.0) + 2.0
    kfd = max(sense, 0.0)
    degree = kfd - 2.0 if kfd >= 2.5 else 0.5
    krx = vel_c * kfd
    kct = krx / (krx + 1.0)

    data = np.empty(129)
    data[:64] = -1000000.0
    data[64:] = 1000000.0
    hoop1 = np.zeros(128)
    hoop2 = np.zeros(11)
    array = np.zeros(62)
    djma = sum1 = sum2 = ser1 = ser2 = 0.0
    pos1 = pos2 = loop1 = loop2 = 0
    count1 = count2 = count3 = 0
    storage1 = storage2 = 0.0
    midd1, midd2 = 63, 64
    started = False
    jma = values[begin]
    var2 = 0.0

    for bar in range(begin, n):
        series = values[bar]
        if loop1 < 61:
            loop1 += 1
            array[loop1] = series
        extent = 0.0
        if loop1 > 30:
            if not started:
                started = True
                back = 29
                ser2 = array[1]
                ser1 = ser2
            else:
                back = 0
            for rrr in range(back, -1, -1):
                ser0 = series if rrr == 0 else array[31 - rrr]
                dser1 = ser0 - ser1
                dser2 = ser0 - ser2
                var2 = max(abs(dser1), abs(dser2))
                res = var2
                newvel = res + 0.0000000001
                count1 = 127 if count1 <= 1 else count1 - 1
                count2 = 10 if count2 <= 1 else count2 - 1
                if count3 < 128:
                    count3 += 1
                sum1 += newvel - hoop2[count2]
                hoop2[count2] = newvel
                sm_vel = sum1 / 10.0 if count3 > 10 else sum1 / count3

                if count3 > 127:
                    old = hoop1[count1]
                    hoop1[count1] = sm_vel
                    numb = 64
                    pos_b = numb
                    while numb > 1:
                        if data[pos_b] < old:
                            numb //= 2
                            pos_b += numb
                        elif data[pos_b] <= old:
                            numb = 1
                        else:
                            numb //= 2
                            pos_b -= numb
                else:
                    hoop1[count1] = sm_vel
                    if midd1 + midd2 > 127:
                        midd2 -= 1
                        pos_b = midd2
                    else:
                        midd1 += 1
                        pos_b = midd1
                    pos2 = 96 if midd1 > 96 else midd1
                    pos1 = 32 if midd2 < 32 else midd2

                numb = 64
                pos_a = numb
                while numb > 1:
                    if data[pos_a] >= sm_vel:
                        if data[pos_a - 1] <= sm_vel:
                            numb = 1
                        else:
                            numb //= 2
                            pos_a -= numb
                    else:
                        numb //= 2
                        pos_a += numb
                    if pos_a == 127 and sm_vel > data[127]:
                        pos_a = 128

                if count3 > 127:
                    if pos_b >= pos_a:
                        if pos2 + 1 > pos_a:
                            if pos1 - 1 < pos_a:
                                sum2 += sm_vel
                            elif pos1 > pos_a and pos1 - 1 < pos_b:
                                sum2 += data[pos1 - 1]
                    elif pos1 >= pos_a:
                        if pos2 + 1 < pos_a and pos2 + 1 > pos_b:
                            sum2 += data[pos2 + 1]
                    elif pos2 + 2 > pos_a:
                        sum2 += sm_vel
                    elif pos2 + 1 < pos_a and pos2 + 1 > pos_b:
                        sum2 += data[pos2 + 1]

                    if pos_b > pos_a:
                        if pos1 - 1 < pos_b:
                            if pos2 + 1 > pos_b:
                                sum2 -= data[pos_b]
                            elif pos2 < pos_b and pos2 + 1 > pos_a:
                                sum2 -= data[pos2]
                    else:
                        if pos2 + 1 > pos_b and pos1 - 1 < pos_b:
                            sum2 -= data[pos_b]
                        elif pos1 > pos_b and pos1 < pos_a:
                            sum2 -= data[pos1]

                if pos_b <= pos_a:
                    if pos_b == pos_a:
                        data[pos_a] = sm_vel
                    else:
                        data[pos_b: pos_a - 1] = data[pos_b + 1: pos_a]
                        data[pos_a - 1] = sm_vel
                else:
                    data[pos_a + 1: pos_b + 1] = data[pos_a: pos_b].copy()
                    data[pos_a] = sm_vel

                if count3 <= 127:
                    sum2 = float(np.sum(data[pos1: pos2 + 1]))
                resalt = sum2 / (pos2 - pos1 + 1.0)

                loop2 = 31 if loop2 > 30 else loop2 + 1
                if loop2 <= 30:
                    ser1 = ser0 if dser1 > 0.0 else ser0 - dser1 * kct
                    ser2 = ser0 if dser2 < 0.0 else ser0 - dser2 * kct
                    jma = series
                    if loop2 != 30:
                        continue
                    storage1 = series
                    d_supr = math.ceil(krx) if math.ceil(krx) >= 1 else 1.0
                    suprem2 = float(math.floor(d_supr)) if d_supr > 0 else 0.0
                    var2 = math.floor(krx) if math.floor(krx) >= 1 else 1.0
                    suprem1 = float(math.floor(var2)) if var2 > 0 else 0.0
                    if suprem2 == suprem1:
                        factor = 1.0
                    else:
                        factor = (krx - suprem1) / (suprem2 - suprem1)
                    shift1 = int(suprem1) if suprem1 <= 29 else 29
                    shift2 = int(suprem2) if suprem2 <= 29 else 29
                    dser3 = series - array[loop1 - shift1]
                    dser4 = series - array[loop1 - shift2]
                    djma = dser3 * (1.0 - factor) / suprem1 + dser4 * factor / suprem2
                else:
                    res_pow = (res / resalt) ** degree if resalt else 0.0
                    var1 = min(kfd, res_pow)
                    var2 = 1.0 if var1 < 1.0 else min(kfd, res_pow)
                    extent = var2
                    pow1 = kct ** math.sqrt(extent)
                    ser1 = ser0 if dser1 > 0.0 else ser0 - dser1 * pow1
                    ser2 = ser0 if dser2 < 0.0 else ser0 - dser2 * pow1

            if loop2 > 30:
                pow2 = krj ** extent
                storage1 = storage1 * pow2 + (1.0 - pow2) * series
                storage2 = storage2 * krj + (series - storage1) * (1.0 - krj)
                extr = k_phase * storage2 + storage1
                pow2x2 = pow2 * pow2
                ratio = pow2x2 - 2.0 * pow2 + 1.0
                djma = djma * pow2x2 + (extr - jma) * ratio
                jma += djma
        if loop1 > 30:
            out[bar] = jma
    return out


def jurx(values, length: float, begin: int = 0) -> np.ndarray:
    """``CJurX::JurXSeries`` — Jurik's triple two-pole smoother."""
    values = np.asarray(values, dtype=float)
    n = len(values)
    out = np.full(n, EMPTY)
    if begin >= n:
        return out
    length = max(float(length), 1.0)
    kg = 3.0 / (length + 2.0)
    hg = 1.0 - kg
    f = [values[begin]] * 6
    for i in range(begin, n):
        x = values[i]
        f[0] = hg * f[0] + kg * x
        f[1] = kg * f[0] + hg * f[1]
        v1 = 1.5 * f[0] - 0.5 * f[1]
        f[2] = hg * f[2] + kg * v1
        f[3] = kg * f[2] + hg * f[3]
        v2 = 1.5 * f[2] - 0.5 * f[3]
        f[4] = hg * f[4] + kg * v2
        f[5] = kg * f[4] + hg * f[5]
        out[i] = 1.5 * f[4] - 0.5 * f[5]
    return out


def t3(values, length: float, curvature: float, begin: int = 0) -> np.ndarray:
    """``CT3::T3Series`` — Tillson's T3, ``curvature`` = volume factor × 100."""
    values = np.asarray(values, dtype=float)
    n = len(values)
    out = np.full(n, EMPTY)
    if begin >= n:
        return out
    length = max(float(length), 1.0)
    b = curvature / 100.0
    b2, b3 = b * b, b * b * b
    c1 = -b3
    c2 = 3 * (b2 + b3)
    c3 = -3 * (2 * b2 + b + b3)
    c4 = 1 + 3 * b + b3 + 3 * b2
    nn = 1 + 0.5 * (length - 1)
    w1 = 2 / (nn + 1)
    w2 = 1 - w1
    e = [values[begin]] * 6
    for i in range(begin, n):
        e[0] = w1 * values[i] + w2 * e[0]
        for k in range(1, 6):
            e[k] = w1 * e[k - 1] + w2 * e[k]
        out[i] = c1 * e[5] + c2 * e[4] + c3 * e[3] + c4 * e[2]
    return out


# ------------------------------------------------------------------- others


def parma(values, length: int, begin: int = 0) -> np.ndarray:
    """``CParMA::ParMASeries`` — a least-squares parabola through the last
    ``length`` bars, evaluated at the newest bar."""
    values = np.asarray(values, dtype=float)
    n = len(values)
    out = np.full(n, EMPTY)
    first = begin + length - 1
    if first >= n or length < 3:
        return out
    x = np.arange(1.0, length + 1.0)
    design = np.vstack([np.ones(length), x, x * x]).T
    # The fitted value at x = length is a fixed linear combination of the window.
    weights = np.array([1.0, length, length * length]) @ np.linalg.pinv(design)
    windows = np.lib.stride_tricks.sliding_window_view(values[begin:], length)
    out[first:] = windows @ weights
    return out


def cmo_abs(values, cmo_length: int, begin: int = 0) -> np.ndarray:
    """``CCMO::CMOSeries`` — |CMO| over ``cmo_length`` price changes; the
    library holds the previous value when the window has no movement."""
    values = np.asarray(values, dtype=float)
    n = len(values)
    out = np.full(n, EMPTY)
    first = begin + cmo_length + 2
    if first >= n:
        return out
    diff = np.diff(values, prepend=np.nan)
    up = pd.Series(np.where(diff > 0, diff, 0.0)).rolling(cmo_length).sum().to_numpy()
    dn = pd.Series(np.where(diff < 0, -diff, 0.0)).rolling(cmo_length).sum().to_numpy()
    total = up + dn
    with np.errstate(divide="ignore", invalid="ignore"):
        raw = np.where(total > 0, np.abs((up - dn) / total), np.nan)
    held = pd.Series(raw[first:]).ffill().fillna(0.000000001).to_numpy()
    out[first:] = held
    return out


def vidya(values, cmo_length: int, ema_length: float, begin: int = 0) -> np.ndarray:
    """``CCMO::VIDYASeries`` — an EMA whose speed scales with |CMO|."""
    values = np.asarray(values, dtype=float)
    n = len(values)
    out = np.full(n, EMPTY)
    first = begin + cmo_length + 2
    if first >= n:
        return out
    cmo = cmo_abs(values, cmo_length, begin)
    k = 2.0 / (float(ema_length) + 1.0)
    level = values[first]
    for i in range(first, n):
        f = cmo[i] * k
        level = f * values[i] + (1 - f) * level
        out[i] = level
    return out


def ama(values, length: int, fast: int, slow: int, rate: float,
        begin: int = 0) -> np.ndarray:
    """``CAMA::AMASeries`` — Kaufman's adaptive MA, smoothing constant
    raised to ``rate``."""
    values = np.asarray(values, dtype=float)
    n = len(values)
    out = np.full(n, EMPTY)
    first = begin + length + 2
    if first >= n:
        return out
    slow_sc = 2.0 / (slow + 1)
    fast_sc = 2.0 / (fast + 1)
    d_sc = fast_sc - slow_sc
    change = np.abs(np.diff(values, prepend=np.nan))
    noise = pd.Series(change).rolling(length).sum().to_numpy() + 0.000000001
    signal = np.abs(values - np.r_[np.full(length, np.nan), values[:-length]])
    level = values[first - 1]
    for i in range(first, n):
        sc = signal[i] / noise[i] * d_sc + slow_sc
        level = level + sc ** rate * (values[i] - level)
        out[i] = level
    return out


# --------------------------------------------------------------- price series


#: The library's extended ``Applied_price_`` enum (1-based).
PRICE_OPTIONS = {
    "close": "Close", "open": "Open", "high": "High", "low": "Low",
    "median": "Median (HL/2)", "typical": "Typical (HLC/3)",
    "weighted": "Weighted (HLCC/4)", "simple": "Simple (OC/2)",
    "quarter": "Quarter (HLOC/4)", "trendfollow0": "TrendFollow 1",
    "trendfollow1": "TrendFollow 2", "demark": "DeMark",
}


def price_choice(default: str = "close") -> Choice:
    return Choice(PRICE_OPTIONS, default=default)


def price_series(df: pd.DataFrame, price: str) -> np.ndarray:
    """``PriceSeries()`` for the library's extended applied-price set."""
    o = df["open"].to_numpy(dtype=float)
    h = df["high"].to_numpy(dtype=float)
    l = df["low"].to_numpy(dtype=float)
    c = df["close"].to_numpy(dtype=float)
    if price == "close":
        return c
    if price == "open":
        return o
    if price == "high":
        return h
    if price == "low":
        return l
    if price == "median":
        return (h + l) / 2.0
    if price == "typical":
        return (c + h + l) / 3.0
    if price == "weighted":
        return (2 * c + h + l) / 4.0
    if price == "simple":
        return (o + c) / 2.0
    if price == "quarter":
        return (o + c + h + l) / 4.0
    if price == "trendfollow0":
        return np.where(c > o, h, np.where(c < o, l, c))
    if price == "trendfollow1":
        return np.where(c > o, (h + c) / 2.0, np.where(c < o, (l + c) / 2.0, c))
    if price == "demark":
        res = h + l + c
        res = np.where(c < o, (res + l) / 2, np.where(c > o, (res + h) / 2, (res + c) / 2))
        return ((res - l) + (res - h)) / 2
    raise ValueError(f"Unknown applied price: {price!r}")
