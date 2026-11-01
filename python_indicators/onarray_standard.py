"""Standard indicators from Integer's "IncOnArray" library — converted from the
``Test_*OnArray.mq5`` indicators in ``MQL5 Libraries/Inc*OnArray``.

Each MQL5 test indicator feeds chart prices into one ``C*OnArray`` class and
draws the result; each class here does the same. The maths lives in the
library, not the terminal, so values follow its conventions rather than the
built-in ``iADX``/``iRSI``/…: moving averages are ``CMAOnArray`` (EMA/SMMA
seeded with the first value), and every series starts at the first valid input.
See :mod:`backtester.indicators.onarray`.

Where a test indicator calls the short form of ``OnCalculate`` (one ``price[]``
array — MT5's "Apply to" setting), the class has a ``price`` parameter.
"""

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

from backtester.indicators import onarray as oa
from backtester.indicators.base import DrawStyle, Indicator, Level, Pane, Plot
from backtester.indicators import mql5


def _volume(df) -> np.ndarray:
    return df["tick_volume"].to_numpy(dtype=float)


def _deviation(data: np.ndarray, centre: np.ndarray, period: int) -> np.ndarray:
    """sqrt(mean((data[j] - centre[i])^2)) over the ``period`` bars ending at i."""
    n = len(data)
    out = np.full(n, np.nan)
    if period < 1 or n < period:
        return out
    windows = sliding_window_view(data, period)          # row k = bars k..k+period-1
    centres = centre[period - 1:][:, None]
    out[period - 1:] = np.sqrt(np.mean((windows - centres) ** 2, axis=1))
    return out


def _mean_abs_dev(data: np.ndarray, centre: np.ndarray, period: int) -> np.ndarray:
    n = len(data)
    out = np.full(n, np.nan)
    if period < 1 or n < period:
        return out
    windows = sliding_window_view(data, period)
    out[period - 1:] = np.mean(np.abs(windows - centre[period - 1:][:, None]), axis=1)
    return out


def _clv_volume(h, l, c, v) -> np.ndarray:
    """Close location value × volume — one bar's accumulation/distribution."""
    span = h - l
    with np.errstate(divide="ignore", invalid="ignore"):
        value = ((c - l) - (h - c)) / span * v
    return np.where(span != 0, value, 0.0)


def _directional(h, l, c):
    """Raw +DM, -DM and true range per bar (``SolvePD``), NaN on bar 0."""
    n = len(h)
    plus = np.full(n, np.nan)
    minus = np.full(n, np.nan)
    tr = np.full(n, np.nan)
    if n < 2:
        return plus, minus, tr
    pd_ = np.maximum(h[1:] - h[:-1], 0.0)
    md_ = np.maximum(l[:-1] - l[1:], 0.0)
    keep_p = pd_ > md_
    keep_m = md_ > pd_
    plus[1:] = np.where(keep_p, pd_, 0.0)
    minus[1:] = np.where(keep_m, md_, 0.0)
    pc = c[:-1]
    tr[1:] = np.maximum(
        np.maximum(np.abs(h[1:] - l[1:]), np.abs(h[1:] - pc)), np.abs(l[1:] - pc)
    )
    return plus, minus, tr


def _floor_first(values: np.ndarray, start: int) -> None:
    """The library nudges a zero first value to 1e-8 so its MA can start."""
    if 0 <= start < len(values) and values[start] == 0:
        values[start] = 0.00000001


# ------------------------------------------------------------------ averages


class MovingAverageOnArray(Indicator):
    name = "Moving Average"
    pane = Pane.PRICE
    params = {"period": 14, "method": oa.ma_choice("sma"), "price": oa.price_choice()}
    plots = [Plot("ma", "MA", color="#ff0000", width=1)]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        data = mql5.applied_price(df, self.p.price)
        out = oa.ma(data, period, self.p.method)
        return {"ma": oa.hide_before(out, oa.bars_required(period, self.p.method))}


class DemaOnArray(Indicator):
    name = "DEMA"
    pane = Pane.PRICE
    params = {"period": 14, "method": oa.ma_choice("ema"), "price": oa.price_choice()}
    plots = [Plot("dema", "DEMA", color="#ff0000", width=1)]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        data = mql5.applied_price(df, self.p.price)
        ma1 = oa.ma(data, period, self.p.method)
        ma2 = oa.ma(ma1, period, self.p.method)
        br = oa.bars_required(period, self.p.method)
        return {"dema": oa.hide_before(2.0 * ma1 - ma2, 2 * br)}


class TemaOnArray(Indicator):
    name = "TEMA"
    pane = Pane.PRICE
    params = {"period": 14, "method": oa.ma_choice("ema"), "price": oa.price_choice()}
    plots = [Plot("tema", "TEMA", color="#ff0000", width=1)]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        data = mql5.applied_price(df, self.p.price)
        ma1 = oa.ma(data, period, self.p.method)
        ma2 = oa.ma(ma1, period, self.p.method)
        ma3 = oa.ma(ma2, period, self.p.method)
        br = oa.bars_required(period, self.p.method)
        return {"tema": oa.hide_before(3.0 * ma1 - 3.0 * ma2 + ma3, 3 * br)}


class AmaOnArray(Indicator):
    name = "AMA (Kaufman Adaptive MA)"
    pane = Pane.PRICE
    params = {"period": 9, "fast_period": 2, "slow_period": 30, "price": oa.price_choice()}
    plots = [Plot("ama", "AMA", color="#ff0000", width=1)]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        fast = max(int(self.p.fast_period), 1)
        slow = max(int(self.p.slow_period), 1)
        data = mql5.applied_price(df, self.p.price)
        n = len(data)
        out = self.empty(n)
        s = oa.first_valid(data)
        if s is None or s + period - 1 >= n:
            return {"ama": out}
        fc = 2.0 / (fast + 1.0)
        sc = 2.0 / (slow + 1.0)
        signal = np.abs(data - mql5.shift_forward(data, period))
        noise = oa.window_sum(oa.abs_change(data), period)
        with np.errstate(divide="ignore", invalid="ignore"):
            er = np.where(noise != 0, signal / noise, 0.0)
        ssc = (er * (fc - sc) + sc) ** 2
        start = s + period - 1
        out[start] = data[start]
        for i in range(start + 1, n):
            out[i] = ssc[i] * (data[i] - out[i - 1]) + out[i - 1]
        begin = 10 * max(fast, slow) + period - 1
        return {"ama": oa.hide_before(out, begin)}


class VidyaOnArray(Indicator):
    name = "VIDYA"
    pane = Pane.PRICE
    params = {"cmo_period": 9, "ma_period": 12, "price": oa.price_choice()}
    plots = [Plot("vidya", "VIDYA", color="#ff0000", width=1)]

    def calculate(self, df):
        cmo_period = max(int(self.p.cmo_period), 1)
        ma_period = max(int(self.p.ma_period), 1)
        data = mql5.applied_price(df, self.p.price)
        n = len(data)
        out = self.empty(n)
        s = oa.first_valid(data)
        if s is None or s + cmo_period >= n:
            return {"vidya": out}
        k1 = 2.0 / (ma_period + 1.0)
        diff = np.diff(data, prepend=np.nan)
        up = oa.window_sum(np.where(diff > 0, diff, 0.0), cmo_period)
        down = oa.window_sum(np.where(diff < 0, -diff, 0.0), cmo_period)
        start = s + cmo_period
        out[start - 1] = data[start - 1]
        cmo = 0.0
        for i in range(start, n):
            total = up[i] + down[i]
            if total != 0:
                cmo = abs((up[i] - down[i]) / total)   # else the last CMO carries
            out[i] = data[i] * k1 * cmo + out[i - 1] * (1.0 - k1 * cmo)
        return {"vidya": oa.hide_before(out, cmo_period + 1 + ma_period * 10)}


class FramaOnArray(Indicator):
    name = "FRAMA"
    pane = Pane.PRICE
    params = {"period": 14}
    plots = [Plot("frama", "FRAMA", color="#ff0000", width=1)]

    def calculate(self, df):
        p = max(int(self.p.period), 1)
        h = self.series(df, "high")
        l = self.series(df, "low")
        c = self.series(df, "close")
        n = len(c)
        out = self.empty(n)
        s = oa.first_valid(c)
        if s is None or s + 2 * p - 2 >= n:
            return {"frama": out}
        hi1 = oa.window_max(h, p)
        lo1 = oa.window_min(l, p)
        hi2 = mql5.shift_forward(hi1, p)
        lo2 = mql5.shift_forward(lo1, p)
        n1 = (hi1 - lo1) / p
        n2 = (hi2 - lo2) / p
        n3 = (np.maximum(hi1, hi2) - np.minimum(lo1, lo2)) / (2 * p)
        with np.errstate(divide="ignore", invalid="ignore"):
            dim = (np.log(n1 + n2) - np.log(n3)) / np.log(2.0)
            alfa = np.exp(-4.6 * (dim - 1.0))
        # A flat window makes the dimension 0/0; hold the line there rather
        # than letting one NaN poison every later bar.
        alfa = np.where(np.isfinite(alfa), alfa, 0.0)
        start = s + 2 * p - 2
        out[start] = c[start]
        for i in range(start + 1, n):
            out[i] = alfa[i] * c[i] + (1.0 - alfa[i]) * out[i - 1]
        return {"frama": out}


# ------------------------------------------------------------------ channels


class BandsOnArray(Indicator):
    name = "Bollinger Bands"
    pane = Pane.PRICE
    params = {
        "period": 10, "method": oa.ma_choice("sma"), "deviation": 2.0,
        "price": oa.price_choice(),
    }
    plots = [
        Plot("upper", "Upper", color="#ff0000", width=1),
        Plot("lower", "Lower", color="#ff0000", width=1),
        Plot("middle", "Middle", color="#ff0000", width=1),
    ]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        data = mql5.applied_price(df, self.p.price)
        mid = oa.ma(data, period, self.p.method)
        dev = float(self.p.deviation) * _deviation(data, mid, period)
        start = oa.first_valid(mid)
        start = None if start is None else start + period
        br = oa.bars_required(period, self.p.method)
        return {
            "upper": oa.hide_before(oa.from_start(mid + dev, start), br),
            "lower": oa.hide_before(oa.from_start(mid - dev, start), br),
            "middle": oa.hide_before(mid, br),
        }


class EnvelopesOnArray(Indicator):
    name = "Envelopes"
    pane = Pane.PRICE
    params = {
        "period": 14, "method": oa.ma_choice("sma"), "deviation_pct": 0.1,
        "price": oa.price_choice(),
    }
    plots = [
        Plot("middle", "Middle", color="#ff0000", width=1),
        Plot("upper", "Upper", color="#ff0000", width=1),
        Plot("lower", "Lower", color="#ff0000", width=1),
    ]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        data = mql5.applied_price(df, self.p.price)
        mid = oa.ma(data, period, self.p.method)
        offset = data * float(self.p.deviation_pct) / 100.0
        br = oa.bars_required(period, self.p.method)
        return {
            "middle": oa.hide_before(mid, br),
            "upper": oa.hide_before(mid + offset, br),
            "lower": oa.hide_before(mid - offset, br),
        }


class PriceChannelOnArray(Indicator):
    name = "Price Channel"
    pane = Pane.PRICE
    params = {"period": 34}
    plots = [
        Plot("upper", "Upper", color="#ff0000", width=1),
        Plot("lower", "Lower", color="#ff0000", width=1),
        Plot("middle", "Middle", color="#ff0000", width=1),
    ]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        upper = oa.window_max(self.series(df, "high"), period)
        lower = oa.window_min(self.series(df, "low"), period)
        return {"upper": upper, "lower": lower, "middle": (upper + lower) / 2.0}


class IchimokuOnArray(Indicator):
    name = "Ichimoku"
    pane = Pane.PRICE
    params = {"tenkan": 9, "kijun": 26, "senkou": 52, "shift_spans": True}
    plots = [
        Plot("tenkan", "Tenkan-sen", color="#ff0000", width=1),
        Plot("kijun", "Kijun-sen", color="#00bfff", width=1),
        Plot("span_a", "Senkou Span A", color="#f0e68c", width=1),
        Plot("span_b", "Senkou Span B", color="#f4a460", width=1),
    ]

    def calculate(self, df):
        tenkan_p = max(int(self.p.tenkan), 1)
        kijun_p = max(int(self.p.kijun), 1)
        senkou_p = max(int(self.p.senkou), 1)
        h = self.series(df, "high")
        l = self.series(df, "low")
        # With shift on, the spans plotted at a bar are the ones computed
        # ``kijun`` bars earlier — the cloud's usual displacement, done without
        # drawing into the future.
        shift = kijun_p if self.p.shift_spans else 0
        tenkan = (oa.window_max(h, tenkan_p) + oa.window_min(l, tenkan_p)) / 2.0
        kijun = (oa.window_max(h, kijun_p) + oa.window_min(l, kijun_p)) / 2.0
        span_a = mql5.shift_forward((tenkan + kijun) / 2.0, shift)
        span_b = mql5.shift_forward(
            (oa.window_max(h, senkou_p) + oa.window_min(l, senkou_p)) / 2.0, shift
        )
        tk_begin = max(tenkan_p, kijun_p) - 1
        ab_begin = max(tenkan_p, kijun_p, senkou_p) + shift - 1
        return {
            "tenkan": oa.hide_before(tenkan, tk_begin),
            "kijun": oa.hide_before(kijun, tk_begin),
            "span_a": oa.hide_before(span_a, ab_begin),
            "span_b": oa.hide_before(span_b, ab_begin),
        }


class ParabolicSarOnArray(Indicator):
    name = "Parabolic SAR"
    pane = Pane.PRICE
    params = {"step": 0.02, "maximum": 0.2}
    plots = [Plot("sar", "SAR", style=DrawStyle.ARROW, color="#ff0000", size=4)]

    def calculate(self, df):
        step = float(self.p.step)
        cap = float(self.p.maximum)
        h = self.series(df, "high")
        l = self.series(df, "low")
        n = len(h)
        sar = self.empty(n)
        s = oa.first_valid(h)
        if s is None:
            return {"sar": sar}

        # Seed: the first bar that clearly breaks up or down sets the trend.
        start = None
        extreme = acc = 0.0
        for i in range(s + 2, n):
            if h[i] > h[i - 1] and l[i] >= l[i - 1]:
                sar[i - 1] = min(l[i - 1], l[i - 2])
                extreme, acc, start = h[i - 1], step, i
                break
            if l[i] < l[i - 1] and h[i] <= h[i - 1]:
                sar[i - 1] = max(h[i - 1], h[i - 2])
                extreme, acc, start = l[i - 1], -step, i
                break
        if start is None:
            return {"sar": sar}

        for i in range(start, n):
            if acc > 0:
                value = sar[i - 1] + acc * (extreme - sar[i - 1])
                value = min(l[i - 1], l[i - 2], value)
                if l[i] < value:                       # flip to a downtrend
                    sar[i] = extreme
                    acc, extreme = -step, l[i]
                    continue
                sar[i] = value
                if h[i] > extreme:
                    extreme = h[i]
                    acc = min(acc + step, cap)
            if acc < 0:
                value = sar[i - 1] + acc * (sar[i - 1] - extreme)
                value = max(h[i - 1], h[i - 2], value)
                if h[i] > value:                       # flip to an uptrend
                    sar[i] = extreme
                    acc, extreme = step, h[i]
                    continue
                sar[i] = value
                if l[i] < extreme:
                    extreme = l[i]
                    acc = max(acc - step, -cap)
        return {"sar": sar}


class FractalsOnArray(Indicator):
    name = "Fractals"
    pane = Pane.PRICE
    params = {}
    plots = [
        Plot("upper", "Upper fractal", style=DrawStyle.ARROW, color="#ff0000",
             symbol="t1", size=8, known_at="known"),
        Plot("lower", "Lower fractal", style=DrawStyle.ARROW, color="#ff0000",
             symbol="t", size=8, known_at="known"),
    ]

    def calculate(self, df):
        h = self.series(df, "high")
        l = self.series(df, "low")
        n = len(h)
        upper = self.empty(n)
        lower = self.empty(n)
        known = np.full(n, np.inf)
        s = oa.first_valid(h)
        if s is None:
            return {"upper": upper, "lower": lower, "known": known}

        def is_peak(x, i, sign):
            """The source's five patterns, written once for highs (sign=1)
            and lows (sign=-1): equal neighbours to the left are allowed."""
            v = x * sign
            m = v[i - 2]
            if not (m > v[i - 1] and m > v[i]):
                return False
            return (
                (m > v[i - 3] and m > v[i - 4])
                or (m == v[i - 3] and m > v[i - 4] and m > v[i - 5])
                or (m >= v[i - 3] and m == v[i - 4] and m > v[i - 5] and m > v[i - 6])
                or (m >= v[i - 3] and m == v[i - 4] and m == v[i - 5]
                    and m > v[i - 6] and m > v[i - 7])
                or (m >= v[i - 3] and m == v[i - 4] and m >= v[i - 5]
                    and m == v[i - 6] and m > v[i - 7] and m > v[i - 8])
            )

        for i in range(s + 8, n):
            # A fractal sits two bars back and is only confirmed now.
            if is_peak(h, i, 1.0):
                upper[i - 2] = h[i - 2]
            if is_peak(l, i, -1.0):
                lower[i - 2] = l[i - 2]
            known[i - 2] = i
        return {"upper": upper, "lower": lower, "known": known}


# ---------------------------------------------------------------- oscillators


class MacdOnArray(Indicator):
    name = "MACD"
    pane = Pane.SEPARATE
    params = {
        "fast_period": 12, "slow_period": 26, "signal_period": 9,
        "fast_method": oa.ma_choice("ema"), "slow_method": oa.ma_choice("ema"),
        "signal_method": oa.ma_choice("sma"), "price": oa.price_choice(),
    }
    plots = [
        Plot("main", "MACD", style=DrawStyle.HISTOGRAM, color="#7fffd4"),
        Plot("signal", "Signal", color="#ff0000", width=1),
    ]

    def _main_signal(self, df):
        data = mql5.applied_price(df, self.p.price)
        fast = oa.ma(data, int(self.p.fast_period), self.p.fast_method)
        slow = oa.ma(data, int(self.p.slow_period), self.p.slow_method)
        main = fast - slow
        signal = oa.ma(main, int(self.p.signal_period), self.p.signal_method)
        br_main = max(
            oa.bars_required(int(self.p.fast_period), self.p.fast_method),
            oa.bars_required(int(self.p.slow_period), self.p.slow_method),
        )
        br_signal = br_main + oa.bars_required(
            int(self.p.signal_period), self.p.signal_method
        ) - 1
        return main, signal, br_main, br_signal

    def calculate(self, df):
        main, signal, br_main, br_signal = self._main_signal(df)
        return {
            "main": oa.hide_before(main, br_main),
            "signal": oa.hide_before(signal, br_signal),
        }


class OsmaOnArray(MacdOnArray):
    name = "OsMA"
    plots = [Plot("osma", "OsMA", style=DrawStyle.HISTOGRAM, color="#7fffd4")]

    def calculate(self, df):
        main, signal, _br_main, br_signal = self._main_signal(df)
        return {"osma": oa.hide_before(main - signal, br_signal)}


class RsiOnArray(Indicator):
    name = "RSI"
    pane = Pane.SEPARATE
    params = {"period": 14, "method": oa.ma_choice("smma"), "price": oa.price_choice()}
    plots = [Plot("rsi", "RSI", color="#ff0000", width=1)]
    y_range = (0, 100)

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        data = mql5.applied_price(df, self.p.price)
        n = len(data)
        s = oa.first_valid(data)
        if s is None or s + 1 >= n:
            return {"rsi": self.empty(n)}
        diff = np.diff(data, prepend=np.nan)
        plus = np.where(diff > 0, diff, 0.0)
        minus = np.where(diff < 0, -diff, 0.0)
        plus[: s + 1] = np.nan
        minus[: s + 1] = np.nan
        _floor_first(plus, s + 1)
        _floor_first(minus, s + 1)
        ps = oa.ma(plus, period, self.p.method)
        ms = oa.ma(minus, period, self.p.method)
        with np.errstate(divide="ignore", invalid="ignore"):
            rsi = np.where(ms != 0, 100.0 - 100.0 / (1.0 + ps / ms), np.nan)
        rsi = oa.hold_previous(rsi, ~np.isfinite(rsi) & np.isfinite(ms))
        return {"rsi": oa.hide_before(rsi, oa.bars_required(period, self.p.method) + 1)}


class StochasticOnArray(Indicator):
    name = "Stochastic"
    pane = Pane.SEPARATE
    params = {
        "k_period": 5, "d_period": 3, "slowing": 3,
        "method": oa.ma_choice("sma"), "price": oa.price_choice(),
    }
    plots = [
        Plot("main", "Main", color="#ff0000", width=1),
        Plot("signal", "Signal", color="#ffff00", width=1),
    ]
    y_range = (0, 100)

    def calculate(self, df):
        k = max(int(self.p.k_period), 1)
        d = max(int(self.p.d_period), 1)
        slowing = max(int(self.p.slowing), 1)
        # The test indicator feeds one price series in as high, low and close.
        data = mql5.applied_price(df, self.p.price)
        hh = oa.window_max(data, k)
        ll = oa.window_min(data, k)
        span = oa.window_sum(hh - ll, slowing)
        pos = oa.window_sum(data - ll, slowing)
        with np.errstate(divide="ignore", invalid="ignore"):
            main = np.where(span != 0, 100.0 * pos / span, 100.0)
        main = np.where(np.isfinite(span), main, np.nan)
        signal = oa.ma(main, d, self.p.method)
        return {
            "main": oa.hide_before(main, k + slowing - 1),
            "signal": oa.hide_before(
                signal, oa.bars_required(d, self.p.method) + k + slowing - 2
            ),
        }


class WprOnArray(Indicator):
    name = "Williams %R"
    pane = Pane.SEPARATE
    params = {"period": 14}
    plots = [Plot("wpr", "%R", color="#ff0000", width=1)]
    y_range = (-100, 0)

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        h = self.series(df, "high")
        l = self.series(df, "low")
        c = self.series(df, "close")
        upper = oa.window_max(h, period)
        lower = oa.window_min(l, period)
        with np.errstate(divide="ignore", invalid="ignore"):
            wpr = -(upper - c) * 100.0 / (upper - lower)
        wpr = oa.hold_previous(wpr, upper == lower)
        s = oa.first_valid(h)
        return {"wpr": oa.from_start(wpr, None if s is None else s + period)}


class CciOnArray(Indicator):
    name = "CCI"
    pane = Pane.SEPARATE
    params = {"period": 14, "method": oa.ma_choice("sma"), "price": oa.price_choice()}
    plots = [Plot("cci", "CCI", color="#ff0000", width=1)]
    levels = [Level(100.0), Level(-100.0)]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        data = mql5.applied_price(df, self.p.price)
        mid = oa.ma(data, period, self.p.method)
        dev = _mean_abs_dev(data, mid, period) * 0.015
        with np.errstate(divide="ignore", invalid="ignore"):
            cci = np.where(dev != 0, (data - mid) / dev, 0.0)
        cci = np.where(np.isfinite(dev), cci, np.nan)
        start = oa.first_valid(mid)
        start = None if start is None else max(start, period)
        return {"cci": oa.hide_before(oa.from_start(cci, start),
                                      oa.bars_required(period, self.p.method))}


class MomentumOnArray(Indicator):
    name = "Momentum"
    pane = Pane.SEPARATE
    params = {"period": 14, "price": oa.price_choice()}
    plots = [Plot("momentum", "Momentum", color="#ff0000", width=1)]
    levels = [Level(100.0)]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        data = mql5.applied_price(df, self.p.price)
        back = mql5.shift_forward(data, period)
        with np.errstate(divide="ignore", invalid="ignore"):
            mom = data / back * 100.0
        mom = oa.hold_previous(mom, back == 0)
        s = oa.first_valid(data)
        return {"momentum": oa.from_start(mom, None if s is None else s + period)}


class CmoOnArray(Indicator):
    name = "CMO (Chande Momentum)"
    pane = Pane.SEPARATE
    params = {"period": 9, "price": oa.price_choice()}
    plots = [Plot("cmo", "CMO", color="#ff0000", width=1)]
    y_range = (-1, 1)

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        data = mql5.applied_price(df, self.p.price)
        diff = np.diff(data, prepend=np.nan)
        up = oa.window_sum(np.where(diff > 0, diff, 0.0), period)
        down = oa.window_sum(np.where(diff < 0, -diff, 0.0), period)
        total = up + down
        with np.errstate(divide="ignore", invalid="ignore"):
            cmo = (up - down) / total
        cmo = oa.hold_previous(cmo, total == 0)
        s = oa.first_valid(data)
        return {"cmo": oa.from_start(cmo, None if s is None else s + period)}


class EfficiencyRatioOnArray(Indicator):
    name = "Efficiency Ratio"
    pane = Pane.SEPARATE
    params = {"period": 34, "price": oa.price_choice()}
    plots = [Plot("er", "ER", color="#ff0000", width=1)]
    directional = False

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        data = mql5.applied_price(df, self.p.price)
        move = data - mql5.shift_forward(data, period)
        if not self.directional:
            move = np.abs(move)
        path = oa.window_sum(oa.abs_change(data), period)
        with np.errstate(divide="ignore", invalid="ignore"):
            er = move / path
        er = oa.hold_previous(er, path == 0)
        s = oa.first_valid(data)
        return {"er": oa.from_start(er, None if s is None else s + period)}


class DirectionalEfficiencyRatioOnArray(EfficiencyRatioOnArray):
    name = "Efficiency Ratio (Directional)"
    plots = [Plot("er", "ERD", color="#ff0000", width=1)]
    levels = [Level(0.0)]
    directional = True


class VhfOnArray(Indicator):
    name = "VHF (Vertical Horizontal Filter)"
    pane = Pane.SEPARATE
    params = {"period": 34, "price": oa.price_choice()}
    plots = [Plot("vhf", "VHF", color="#ff0000", width=1)]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        data = mql5.applied_price(df, self.p.price)
        span = oa.window_max(data, period) - oa.window_min(data, period)
        path = oa.window_sum(oa.abs_change(data), period)
        with np.errstate(divide="ignore", invalid="ignore"):
            vhf = span / path
        vhf = oa.hold_previous(vhf, path == 0)
        s = oa.first_valid(data)
        return {"vhf": oa.from_start(vhf, None if s is None else s + period)}


class TrixOnArray(Indicator):
    name = "TRIX"
    pane = Pane.SEPARATE
    params = {"period": 14, "method": oa.ma_choice("ema"), "price": oa.price_choice()}
    plots = [Plot("trix", "TRIX", color="#ff0000", width=1)]
    levels = [Level(0.0)]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        data = mql5.applied_price(df, self.p.price)
        m3 = oa.ma(oa.ma(oa.ma(data, period, self.p.method), period, self.p.method),
                   period, self.p.method)
        prev = mql5.shift_forward(m3, 1)
        with np.errstate(divide="ignore", invalid="ignore"):
            trix = np.where(prev != 0, (m3 - prev) / prev, 0.0)
        trix = np.where(np.isfinite(prev) & np.isfinite(m3), trix, np.nan)
        br = oa.bars_required(period, self.p.method)
        return {"trix": oa.hide_before(trix, br * 3 - 3 + 1)}


class StdDevOnArray(Indicator):
    name = "Standard Deviation"
    pane = Pane.SEPARATE
    params = {"period": 20, "method": oa.ma_choice("sma"), "price": oa.price_choice()}
    plots = [Plot("stddev", "StdDev", color="#ff0000", width=1)]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        data = mql5.applied_price(df, self.p.price)
        mid = oa.ma(data, period, self.p.method)
        dev = _deviation(data, mid, period)
        start = oa.first_valid(mid)
        start = None if start is None else start + period
        return {"stddev": oa.hide_before(oa.from_start(dev, start),
                                         oa.bars_required(period, self.p.method))}


class RviOnArray(Indicator):
    name = "RVI (Relative Vigor)"
    pane = Pane.SEPARATE
    params = {"period": 10, "method": oa.ma_choice("sma")}
    plots = [
        Plot("main", "Main", color="#ff0000", width=1),
        Plot("signal", "Signal", color="#ffff00", width=1),
    ]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        o = self.series(df, "open")
        h = self.series(df, "high")
        l = self.series(df, "low")
        c = self.series(df, "close")

        def weighted4(x):
            """x[i] + 2x[i-1] + 2x[i-2] + x[i-3]"""
            return (x + 2.0 * mql5.shift_forward(x, 1) + 2.0 * mql5.shift_forward(x, 2)
                    + mql5.shift_forward(x, 3))

        move = oa.ma(weighted4(c - o), period, self.p.method)
        span = oa.ma(weighted4(h - l), period, self.p.method)
        with np.errstate(divide="ignore", invalid="ignore"):
            main = np.where(span != 0, move / span, move)
        signal = weighted4(main) / 6.0
        br = oa.bars_required(period, self.p.method)
        return {
            "main": oa.hide_before(main, 3 + br - 1),
            "signal": oa.hide_before(signal, 3 + br - 1 + 3),
        }


class DeMarkerOnArray(Indicator):
    name = "DeMarker"
    pane = Pane.SEPARATE
    params = {"period": 14, "method": oa.ma_choice("sma")}
    plots = [Plot("demarker", "DeMarker", color="#ff0000", width=1)]
    y_range = (0, 1)

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        h = self.series(df, "high")
        l = self.series(df, "low")
        n = len(h)
        s = oa.first_valid(h)
        if s is None or s + 1 >= n:
            return {"demarker": self.empty(n)}
        up = np.maximum(np.diff(h, prepend=np.nan), 0.0)
        down = np.maximum(-np.diff(l, prepend=np.nan), 0.0)
        up[: s + 1] = np.nan
        down[: s + 1] = np.nan
        _floor_first(up, s + 1)
        _floor_first(down, s + 1)
        ups = oa.ma(up, period, self.p.method)
        downs = oa.ma(down, period, self.p.method)
        total = ups + downs
        with np.errstate(divide="ignore", invalid="ignore"):
            dem = np.where(total != 0, ups / total, 0.0)
        dem = np.where(np.isfinite(total), dem, np.nan)
        return {"demarker": oa.hide_before(dem, oa.bars_required(period, self.p.method) + 1)}


# --------------------------------------------------------- trend / volatility


class AdxOnArray(Indicator):
    name = "ADX"
    pane = Pane.SEPARATE
    params = {"period": 14, "method": oa.ma_choice("ema")}
    plots = [
        Plot("adx", "ADX", color="#00ff00", width=1),
        Plot("pdi", "+DI", color="#0000ff", width=1),
        Plot("mdi", "-DI", color="#ff0000", width=1),
    ]
    wilder = False

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        method = self.p.method
        h = self.series(df, "high")
        l = self.series(df, "low")
        c = self.series(df, "close")
        n = len(c)
        s = oa.first_valid(c)
        if s is None or s + 1 >= n:
            empty = self.empty(n)
            return {"adx": empty, "pdi": empty.copy(), "mdi": empty.copy()}

        plus, minus, tr = _directional(h, l, c)
        for arr in (plus, minus, tr):
            arr[: s + 1] = np.nan
        if self.wilder:
            # ADX Wilder: smooth the raw movements and the true range
            # separately, then divide — rather than dividing bar by bar.
            plus *= 100.0
            minus *= 100.0
            for arr in (plus, minus, tr):
                _floor_first(arr, s + 1)
            atr = oa.ma(tr, period, method)
            with np.errstate(divide="ignore", invalid="ignore"):
                pdi = np.where(atr != 0, oa.ma(plus, period, method) / atr, 0.0)
                mdi = np.where(atr != 0, oa.ma(minus, period, method) / atr, 0.0)
            pdi = np.where(np.isfinite(atr), pdi, np.nan)
            mdi = np.where(np.isfinite(atr), mdi, np.nan)
        else:
            with np.errstate(divide="ignore", invalid="ignore"):
                plus = np.where(tr != 0, 100.0 * plus / tr, 0.0)
                minus = np.where(tr != 0, 100.0 * minus / tr, 0.0)
            plus[: s + 1] = np.nan
            minus[: s + 1] = np.nan
            _floor_first(plus, s + 1)
            _floor_first(minus, s + 1)
            pdi = oa.ma(plus, period, method)
            mdi = oa.ma(minus, period, method)

        total = pdi + mdi
        with np.errstate(divide="ignore", invalid="ignore"):
            dx = np.where(total != 0, 100.0 * np.abs((pdi - mdi) / total), 0.0)
        dx = np.where(np.isfinite(total), dx, np.nan)
        dx[: s + 2] = np.nan               # the source fills DX from Start+1 on
        adx = oa.ma(dx, period, method)
        br = oa.bars_required(period, method)
        return {
            "adx": oa.hide_before(adx, br * 2),
            "pdi": oa.hide_before(pdi, br + 1),
            "mdi": oa.hide_before(mdi, br + 1),
        }


class AdxWilderOnArray(AdxOnArray):
    name = "ADX Wilder"
    params = {"period": 14, "method": oa.ma_choice("smma")}
    wilder = True


class AtrOnArray(Indicator):
    name = "ATR"
    pane = Pane.SEPARATE
    params = {"period": 14, "method": oa.ma_choice("sma")}
    plots = [Plot("atr", "ATR", color="#ff0000", width=1)]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        h = self.series(df, "high")
        l = self.series(df, "low")
        c = self.series(df, "close")
        pc = mql5.shift_forward(c, 1)
        tr = np.maximum(h, pc) - np.minimum(l, pc)
        atr = oa.ma(tr, period, self.p.method)
        return {"atr": oa.hide_before(atr, oa.bars_required(period, self.p.method) + 1)}


class BullsBearsOnArray(Indicator):
    name = "Bulls & Bears Power"
    pane = Pane.SEPARATE
    params = {"period": 13, "method": oa.ma_choice("ema")}
    plots = [
        Plot("bulls", "Bulls", color="#00bfff", width=1),
        Plot("bears", "Bears", color="#ff0000", width=1),
    ]
    levels = [Level(0.0)]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        mid = oa.ma(self.series(df, "close"), period, self.p.method)
        br = oa.bars_required(period, self.p.method)
        return {
            "bulls": oa.hide_before(self.series(df, "high") - mid, br),
            "bears": oa.hide_before(self.series(df, "low") - mid, br),
        }


class ChaikinVolatilityOnArray(Indicator):
    name = "Chaikin Volatility"
    pane = Pane.SEPARATE
    params = {"period": 10, "smooth_period": 10, "smooth_method": oa.ma_choice("ema")}
    plots = [Plot("chv", "CHV", color="#ff0000", width=1)]
    levels = [Level(0.0)]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        smooth = max(int(self.p.smooth_period), 1)
        rng = self.series(df, "high") - self.series(df, "low")
        rs = oa.ma(rng, smooth, self.p.smooth_method)
        back = mql5.shift_forward(rs, period)
        with np.errstate(divide="ignore", invalid="ignore"):
            chv = np.where(back != 0, 100.0 * (rs - back) / back, 0.0)
        chv = np.where(np.isfinite(back) & np.isfinite(rs), chv, np.nan)
        begin = oa.bars_required(smooth, self.p.smooth_method) + period - 1
        return {"chv": oa.hide_before(chv, begin)}


# -------------------------------------------------------------------- volume


class AccumulationDistributionOnArray(Indicator):
    name = "Accumulation/Distribution"
    pane = Pane.SEPARATE
    params = {"period": 0}
    plots = [Plot("ad", "A/D", color="#ff0000", width=1)]

    def calculate(self, df):
        period = max(int(self.p.period), 0)
        flow = _clv_volume(
            self.series(df, "high"), self.series(df, "low"),
            self.series(df, "close"), _volume(df),
        )
        n = len(flow)
        s = oa.first_valid(_volume(df))
        if s is None:
            return {"ad": self.empty(n)}
        out = self.empty(n)
        if period > 0:
            # 0 = accumulate over all bars; otherwise a rolling window.
            out[s:] = oa.window_sum(flow[s:], period)
        else:
            out[s:] = np.cumsum(flow[s:])
        return {"ad": out}


class ChaikinOscillatorOnArray(Indicator):
    name = "Chaikin Oscillator"
    pane = Pane.SEPARATE
    params = {"fast_period": 3, "slow_period": 10, "method": oa.ma_choice("ema")}
    plots = [Plot("cho", "CHO", color="#ff0000", width=1)]
    levels = [Level(0.0)]

    def calculate(self, df):
        fast = max(int(self.p.fast_period), 1)
        slow = max(int(self.p.slow_period), 1)
        flow = _clv_volume(
            self.series(df, "high"), self.series(df, "low"),
            self.series(df, "close"), _volume(df),
        )
        n = len(flow)
        s = oa.first_valid(_volume(df))
        if s is None or s + 1 >= n:
            return {"cho": self.empty(n)}
        # The source zeroes the first bar's A/D, so the line starts at bar s+1.
        ad = self.empty(n)
        ad[s] = 0.0
        ad[s + 1:] = np.cumsum(flow[s + 1:])
        cho = oa.ma(ad, fast, self.p.method) - oa.ma(ad, slow, self.p.method)
        br = max(oa.bars_required(fast, self.p.method),
                 oa.bars_required(slow, self.p.method)) + 1
        return {"cho": oa.hide_before(cho, s + 1 + br)}


class ForceIndexOnArray(Indicator):
    name = "Force Index"
    pane = Pane.SEPARATE
    params = {"period": 14, "method": oa.ma_choice("sma")}
    plots = [Plot("force", "Force", color="#ff0000", width=1)]
    levels = [Level(0.0)]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        mid = oa.ma(self.series(df, "close"), period, self.p.method)
        force = _volume(df) * (mid - mql5.shift_forward(mid, 1))
        return {"force": oa.hide_before(force, oa.bars_required(period, self.p.method) + 1)}


class MfiOnArray(Indicator):
    name = "MFI (Money Flow Index)"
    pane = Pane.SEPARATE
    params = {"period": 14, "method": oa.ma_choice("sma")}
    plots = [Plot("mfi", "MFI", color="#ff0000", width=1)]
    y_range = (0, 100)

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        price = mql5.applied_price(df, "typical")
        volume = _volume(df)
        n = len(price)
        s = oa.first_valid(volume)
        if s is None or s + 1 >= n:
            return {"mfi": self.empty(n)}
        flow = price * volume
        prev = mql5.shift_forward(price, 1)
        plus = np.where(price > prev, flow, 0.0)
        minus = np.where(price < prev, flow, 0.0)
        plus[:s] = np.nan
        minus[:s] = np.nan
        plus[s] = minus[s] = 0.00000001
        ps = oa.ma(plus, period, self.p.method)
        ms = oa.ma(minus, period, self.p.method)
        with np.errstate(divide="ignore", invalid="ignore"):
            mfi = np.where(ms != 0, 100.0 - 100.0 / (1.0 + ps / ms), 100.0)
        mfi = np.where(np.isfinite(ms), mfi, np.nan)
        return {"mfi": oa.hide_before(mfi, oa.bars_required(period, self.p.method) + 1)}


class ObvOnArray(Indicator):
    name = "OBV (On Balance Volume)"
    pane = Pane.SEPARATE
    params = {"period": 0}
    plots = [Plot("obv", "OBV", color="#ff0000", width=1)]

    def calculate(self, df):
        period = max(int(self.p.period), 0)
        c = self.series(df, "close")
        volume = _volume(df)
        n = len(c)
        signed = np.sign(np.diff(c, prepend=np.nan)) * volume
        out = self.empty(n)
        if period > 0:
            # 0 = accumulate over all bars; otherwise a rolling window.
            out = oa.window_sum(signed, period)
            s = oa.first_valid(volume)
            return {"obv": oa.from_start(out, None if s is None else max(s, 1) + period)}
        s = oa.first_valid(volume)
        if s is None:
            return {"obv": out}
        out[s] = volume[s]
        if s + 1 < n:
            out[s + 1:] = volume[s] + np.cumsum(signed[s + 1:])
        return {"obv": out}
