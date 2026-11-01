"""XU RSI MA1 AutoScale — converted from ``XU RSI MA1_AutoScale.mq5`` (XU v042).

mladen's "RSI of a smoothed price": the price is first smoothed with the
chosen average over the RSI period, the chosen RSI flavour is taken of that,
and an average of the RSI is drawn over it. With ``auto_scale`` on, both
periods are scaled from their H1 baseline (13 / 21) by the timeframe — e.g.
×3.5 / ×2.8 on M5 — exactly as the source's table does; the timeframe is read
from the bar spacing.

The RSI line is blue above ``level_up``, magenta below ``level_down`` and grey
between (or coloured by the RSI/average cross or the slope). Divergences
between price pivots and RSI pivots (``pivot_strength`` bars each side) are
drawn on both the price chart and the RSI pane. Labels follow the source,
which pairs each pivot with the next newer one.

On the replay a divergence appears once its newer pivot is confirmed. The
source only pairs pivots that both sit inside its last ``div_lookback`` bars;
here that becomes "no more than ``div_lookback − pivot_strength − 1`` bars
apart", which is what a live chart accumulates. Arrows, alerts and the
optional MT5 zones are left out.
"""

import numpy as np
import pandas as pd

from backtester.indicators.base import Choice, Indicator, Level, Pane, Plot
from backtester.indicators import mql5

#: Timeframe (minutes) → (RSI multiplier, average multiplier); H1 = 1.0.
TF_TABLE = {
    1: (8.0, 6.0), 2: (6.0, 4.5), 3: (4.5, 3.5), 4: (4.0, 3.0), 5: (3.5, 2.8),
    6: (3.0, 2.5), 10: (2.5, 2.2), 12: (2.3, 2.0), 15: (2.0, 1.8), 20: (1.7, 1.6),
    30: (1.5, 1.4), 60: (1.0, 1.0), 120: (0.75, 0.8), 180: (0.6, 0.7),
    240: (0.5, 0.6), 360: (0.4, 0.5), 480: (0.35, 0.45), 720: (0.3, 0.4),
    1440: (0.25, 0.35), 10080: (0.2, 0.3), 43200: (0.15, 0.25),
}

RSI_TYPES = {"rsi": "Regular RSI", "slow": "Wilders' RSI", "rapid": "Rapid RSI",
             "harris": "Harris RSI", "rsx": "RSX", "cuttler": "Cuttler's RSI"}

DIV_KINDS = (
    ("reg_bull", "Regular Bullish", "#00ff00"),
    ("hid_bull", "Hidden Bullish", "#008000"),
    ("reg_bear", "Regular Bearish", "#ff4500"),
    ("hid_bear", "Hidden Bearish", "#ffa500"),
)


def timeframe_minutes(df) -> int:
    if len(df) < 3:
        return 60
    step = pd.to_datetime(df["time"]).diff().dropna()
    return int(round(step.min().total_seconds() / 60.0)) or 60


def _pivots(data: np.ndarray, strength: int, low: bool) -> np.ndarray:
    """Strict pivots: lower (higher) than ``strength`` bars on each side."""
    n = len(data)
    out = np.zeros(n, dtype=bool)
    for i in range(strength, n - strength):
        v = data[i]
        if not np.isfinite(v):
            continue
        neighbours = np.r_[data[i - strength: i], data[i + 1: i + strength + 1]]
        out[i] = np.all(neighbours > v) if low else np.all(neighbours < v)
    return out


class XuRsiMa(Indicator):
    name = "XU RSI MA1 AutoScale"
    pane = Pane.SEPARATE
    params = {
        "base_rsi_period": 13, "base_average_period": 21,
        "rsi_type": Choice(RSI_TYPES, default="rsi"),
        "price": Choice(mql5.PRICE_CHOICES, default="close"),
        "average_type": Choice(list(mql5.MA_METHODS), default="ema"),
        "show_average": True, "auto_scale": True,
        "level_up": 52.0, "level_down": 48.0,
        "color_on": Choice({"level": "RSI crosses levels", "ma": "RSI crosses average",
                            "slope": "RSI slope"}, default="level"),
        "show_divergence": True, "div_lookback": 30, "pivot_strength": 2,
    }

    def setup(self):
        self.levels = [Level(float(self.p.level_up)), Level(float(self.p.level_down))]
        self.y_range = (-3, 103)
        plots = [
            Plot("up", "RSI (up)", color="#1e90ff", width=3),
            Plot("down", "RSI (down)", color="#ff00ff", width=3),
            Plot("flat", "RSI (neutral)", color="#808080", width=3),
            Plot("avg", "Average", color="#fffafa", width=2),
        ]
        for key, label, colour in DIV_KINDS:
            plots.append(Plot(f"{key}_rsi", f"{label} (RSI)", color=colour, width=2,
                              known_at=f"{key}_known"))
            plots.append(Plot(f"{key}_price", f"{label} (price)", color=colour, width=2,
                              known_at=f"{key}_known", pane=Pane.PRICE))
        self.plots = plots

    def periods(self, df) -> tuple[int, int]:
        rsi_p, avg_p = int(self.p.base_rsi_period), int(self.p.base_average_period)
        if self.p.auto_scale:
            rsi_m, avg_m = TF_TABLE.get(timeframe_minutes(df), (1.0, 1.0))
            rsi_p = max(int(round(rsi_p * rsi_m)), 2)
            avg_p = max(int(round(avg_p * avg_m)), 2)
        return max(rsi_p, 1), avg_p

    def calculate(self, df):
        rsi_p, avg_p = self.periods(df)
        method = self.p.average_type
        price = mql5.applied_price(df, self.p.price)
        smoothed = (mql5.running_smma(price, rsi_p, start=2) if method == "smma"
                    else mql5.running_ma(price, rsi_p, method))
        rsi = mql5.rsi_variant(smoothed, rsi_p, self.p.rsi_type)
        avg = (mql5.running_smma(rsi, avg_p, start=2) if method == "smma"
               else mql5.running_ma(rsi, avg_p, method))
        n = len(rsi)

        trend = np.zeros(n)
        up, down = float(self.p.level_up), float(self.p.level_down)
        for i in range(1, n):
            if self.p.color_on == "level":
                trend[i] = 1 if rsi[i] > up else -1 if rsi[i] < down else 0
            elif self.p.color_on == "ma":
                trend[i] = 1 if rsi[i] > avg[i] else -1 if rsi[i] < avg[i] else trend[i - 1]
            else:
                trend[i] = (1 if rsi[i] > rsi[i - 1] else -1 if rsi[i] < rsi[i - 1]
                            else trend[i - 1])
        out = {
            "up": mql5.segments(rsi, trend == 1),
            "down": mql5.segments(rsi, trend == -1),
            "flat": mql5.segments(rsi, trend == 0),
            "avg": avg if self.p.show_average else np.full(n, np.nan),
        }
        out.update(self._divergences(df, rsi))
        return out

    def _divergences(self, df, rsi):
        n = len(rsi)
        out = {}
        for key, _label, _colour in DIV_KINDS:
            out[f"{key}_rsi"] = np.full(n, np.nan)
            out[f"{key}_price"] = np.full(n, np.nan)
            out[f"{key}_known"] = np.full(n, np.inf)
        if not self.p.show_divergence:
            return out
        s = max(int(self.p.pivot_strength), 1)
        max_gap = max(int(self.p.div_lookback) - s - 1, 1)
        h = self.series(df, "high")
        l = self.series(df, "low")

        def draw(key, a, b, pa, pb, ra, rb):
            span = np.arange(a, b + 1)
            out[f"{key}_price"][span] = np.interp(span, [a, b], [pa, pb])
            out[f"{key}_rsi"][span] = np.interp(span, [a, b], [ra, rb])
            out[f"{key}_known"][span] = b + s

        for low_side in (True, False):
            prices = l if low_side else h
            both = _pivots(prices, s, low_side) & _pivots(rsi, s, low_side)
            idx = np.nonzero(both)[0]
            # Pair each pivot (older, a) with the next newer one (b), as the
            # source's newest-first scan does.
            for a, b in zip(idx[:-1], idx[1:]):
                if b - a > max_gap:
                    continue
                pa, pb, ra, rb = prices[a], prices[b], rsi[a], rsi[b]
                if low_side:
                    if pa < pb and ra > rb:
                        draw("reg_bull", a, b, pa, pb, ra, rb)
                    if pa > pb and ra < rb:
                        draw("hid_bull", a, b, pa, pb, ra, rb)
                else:
                    if pa > pb and ra < rb:
                        draw("reg_bear", a, b, pa, pb, ra, rb)
                    if pa < pb and ra > rb:
                        draw("hid_bear", a, b, pa, pb, ra, rb)
        return out
