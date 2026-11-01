"""MMATH — converted from ``MMATH-v1.07.mq5`` (XU v057).

Murrey Math price lines. The octave (frame ``frame`` of the price's fractal)
is anchored at a base fitted to the last ``range_bars`` bars and only moves
when price leaves the −2/8 … +10/8 band, so the grid holds steady through
normal swings. Drawn: the −2/8 … +2/8-beyond-8/8 lines in Murrey's colours,
the four "Franka" one-third lines, the 3/8–5/8 "happy" zone and the two
extension zones, plus — optionally — the 1/64 "baby" lines inside each band.

The source draws the *current* grid as horizontal lines across the last
``InpLineWidth`` bars. Here each bar shows the grid as it stood on that bar,
so the history reads as steps and never shows a later grid early. Left out:
the time-square verticals, conflict rings, ladder panel, waist/neck lines and
the manual octave buttons (all off by default or interactive). ``baby_lines``
is off by default here (on in the source) because it adds 84 lines.
"""

import math

import numpy as np

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5

# (label, colour, dashed) for eighths −2 … +10, then the Franka lines.
LINES = (
    ("−2/8", "#ff0000", False), ("−1/8", "#ff4500", False), ("0/8", "#1e90ff", True),
    ("1/8", "#ffd700", False), ("2/8", "#da70d6", False), ("3/8", "#00ff00", False),
    ("4/8", "#ffffff", False), ("5/8", "#00ff00", False), ("6/8", "#da70d6", False),
    ("7/8", "#ffd700", False), ("8/8", "#1e90ff", True), ("+1/8", "#ff4500", False),
    ("+2/8", "#ff0000", False),
)
FRANKA = (("Franka +33.3%", 8 + 8 / 3), ("Franka −33.3%", -8 / 3),
          ("Franka 33.3%", 8 / 3), ("Franka 66.6%", 8 - 8 / 3))


def fractal_for(v: float) -> float:
    """``DetermineFractal``: the octave scale for a price."""
    for top, bottom, value in (
        (250000, 25000, 100000), (25000, 2500, 10000), (2500, 250, 1000),
        (250, 25, 100), (25, 12.5, 12.5), (12.5, 6.25, 12.5), (6.25, 3.125, 6.25),
        (3.125, 1.5625, 3.125), (1.5625, 0.390625, 1.5625), (0.390625, 0, 0.1953125),
    ):
        if bottom < v <= top:
            return value
    return 0.0


def fitted_base(fractal, high, low):
    price_range = high - low
    if price_range <= 0 or fractal <= 0:
        return None
    logb2 = max(math.floor(math.log(fractal / price_range) / math.log(2.0)), 0.0)
    frame_fit = fractal * 0.5 ** logb2
    if frame_fit <= 0:
        return None
    raw_min = math.floor(low / frame_fit) * frame_fit
    return raw_min if raw_min + frame_fit > high else raw_min + frame_fit


def micro_fit_step(octave, base, high, low, enabled):
    nat = octave / 8.0
    if not enabled or high <= low:
        return nat, 1.0
    best_score, best_mult = -1e100, 1.0
    for mult in (0.5, 1.0, 2.0):
        step = nat * mult
        margin_lo = low - base
        margin_hi = base + 8 * step - high
        if margin_lo < 0 or margin_hi < 0:
            score = -(max(-margin_lo, 0) + max(-margin_hi, 0))
        else:
            score = min(margin_lo, margin_hi) + 0.25 * (8 * step - (high - low))
        if mult == 1.0:
            score += 1e-6
        if score > best_score:
            best_score, best_mult = score, mult
    return nat * best_mult, best_mult


class Mmath(Indicator):
    name = "MMATH (Murrey Math)"
    pane = Pane.PRICE
    params = {
        "frame": 8, "range_bars": 0, "hybrid_mode": True, "micro_fit": False,
        "show_zones": True, "baby_lines": False,
    }

    def setup(self):
        plots = [
            Plot("happy_top", "Zone Happy 3/8-5/8", style=DrawStyle.FILL, color="#203830",
                 fill_with="happy_bot"),
            Plot("upper_top", "Zone Upper Ext", style=DrawStyle.FILL, color="#382030",
                 fill_with="upper_bot"),
            Plot("lower_top", "Zone Lower Ext", style=DrawStyle.FILL, color="#382030",
                 fill_with="lower_bot"),
        ]
        # The grid spans a whole octave and more; like MT5, keep the chart
        # scaled to price rather than to the outermost lines.
        if self.p.baby_lines:
            for k in range(-16, 81):
                if k % 8:
                    plots.append(Plot(f"baby{k}", "Baby line", color="#3a3a3a", width=1,
                                      autoscale=False))
        for idx, (label, colour, dashed) in enumerate(LINES):
            plots.append(Plot(f"mml{idx}", label, color=colour, width=2, dash=dashed,
                              autoscale=False))
        for idx, (label, _eighths) in enumerate(FRANKA):
            plots.append(Plot(f"franka{idx}", label, color="#ffa500", width=1, dash=True,
                              autoscale=False))
        self.plots = plots

    def calculate(self, df):
        frame = max(int(self.p.frame), 1)
        lookback = int(self.p.range_bars) if int(self.p.range_bars) >= 1 else frame
        h = self.series(df, "high")
        l = self.series(df, "low")
        c = self.series(df, "close")
        n = len(c)
        range_hi = mql5.highest(h, lookback)
        range_lo = mql5.lowest(l, lookback)

        bases = np.full(n, np.nan)
        steps = np.full(n, np.nan)
        active_base, active_mult, has_base = 0.0, 1.0, False
        for i in range(n):
            price = c[i]
            fractal = fractal_for(price)
            if price <= 0 or fractal <= 0:
                continue
            octave = fractal / frame
            half = octave / 2.0
            base_nat = math.floor(price / octave) * octave
            target, target_mult = base_nat, 1.0
            if range_hi[i] > range_lo[i]:
                target = base_nat
                if self.p.hybrid_mode:
                    fit = fitted_base(fractal, range_hi[i], range_lo[i])
                    if fit is not None and abs(fit - base_nat) > half:
                        target = base_nat + half if fit > base_nat else base_nat - half
                _step, target_mult = micro_fit_step(
                    octave, target, range_hi[i], range_lo[i], self.p.micro_fit)
            if not has_base:
                active_base, active_mult, has_base = target, target_mult, True
            else:
                step = octave / 8.0 * active_mult
                if price > active_base + 10 * step or price < active_base - 2 * step:
                    active_base, active_mult = target, target_mult
                else:
                    active_mult = target_mult
                    if self.p.micro_fit and range_hi[i] > range_lo[i]:
                        active_base = target
            bases[i] = active_base
            steps[i] = octave / 8.0 * active_mult

        out = {}
        for idx in range(len(LINES)):
            out[f"mml{idx}"] = bases + (idx - 2) * steps
        for idx, (_label, eighths) in enumerate(FRANKA):
            out[f"franka{idx}"] = bases + eighths * steps
        zones = bool(self.p.show_zones)
        nan = np.full(n, np.nan)
        out["happy_top"] = bases + 5 * steps if zones else nan
        out["happy_bot"] = bases + 3 * steps if zones else nan
        out["upper_top"] = bases + 10 * steps if zones else nan
        out["upper_bot"] = bases + 8 * steps if zones else nan
        out["lower_top"] = bases + 0 * steps if zones else nan
        out["lower_bot"] = bases - 2 * steps if zones else nan
        if self.p.baby_lines:
            for k in range(-16, 81):
                if k % 8:
                    out[f"baby{k}"] = bases + k * steps / 8.0
        return out
