"""Daily Range — converted from ``DailyRange-v1.16.mq5`` (XU v042).

Each day's candle drawn as a large translucent box behind that day's bars:
grey wicks from the high and low to the body, and a dark blue (up) or dark
red (down) body from open to close, for the last ``days`` days.

The source redraws the forming day as one box spanning the whole day so far.
On a chart of fixed bars that box instead grows bar by bar with the day's
range, and is replaced by the finished box when the day's last bar prints.
The high/low price labels are left out.
"""

import numpy as np

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5

WICK = "#202020"
UP_BODY = "#00004b"
DOWN_BODY = "#4b0000"

#: (key, colour, top part, bottom part) for each shaded piece of a day.
PIECES = (
    ("wick_hi", WICK, "high", "body_top"),
    ("body_up", UP_BODY, "body_top", "body_bottom"),
    ("body_dn", DOWN_BODY, "body_top", "body_bottom"),
    ("wick_lo", WICK, "body_bottom", "low"),
)


class XuDailyRange(Indicator):
    name = "XU Daily Range"
    pane = Pane.PRICE
    params = {"days": 14, "current_day_only": False}

    def setup(self):
        plots = []
        for stage in ("final", "live"):
            for parity in (0, 1):
                for key, colour, _top, _bottom in PIECES:
                    name = f"{stage}{parity}_{key}"
                    plots.append(Plot(
                        name, "Daily range", style=DrawStyle.FILL, color=colour,
                        fill_with=f"{name}_lo",
                        known_at="final_known" if stage == "final" else "",
                        expires_at=f"{stage}_expires",
                    ))
        self.plots = plots

    def calculate(self, df):
        days = mql5.day_index(df)
        n = len(days)
        running = mql5.running_daily(df)
        final = mql5.daily_ohlc(df)
        # Last bar of every day, by day number.
        last_bar = np.r_[np.nonzero(np.diff(days))[0], n - 1] if n else np.array([], int)

        keep = 1 if self.p.current_day_only else max(int(self.p.days), 1)
        n_days = len(last_bar)

        def expiry(offset):
            target = days + offset
            return np.where(target < n_days, last_bar[np.minimum(target, n_days - 1)], np.inf)

        out = {
            # A finished day shows once its last bar prints and stays until
            # ``days`` newer days have begun.
            "final_known": last_bar[days].astype(float),
            "final_expires": expiry(keep - 1).astype(float),
            # The forming day's box is current only while the day is forming.
            "live_expires": (last_bar[days] - 1).astype(float),
        }
        if keep - 1 < 0:
            out["final_expires"][:] = -np.inf

        for stage, source in (("final", {k: v[days] for k, v in final.items()}),
                              ("live", running)):
            o, h, l, c = source["open"], source["high"], source["low"], source["close"]
            parts = {
                "high": h, "low": l,
                "body_top": np.maximum(o, c), "body_bottom": np.minimum(o, c),
            }
            up = c >= o
            for parity in (0, 1):
                on_day = (days % 2) == parity
                for key, _colour, top, bottom in PIECES:
                    mask = on_day.copy()
                    if key == "body_up":
                        mask &= up
                    elif key == "body_dn":
                        mask &= ~up
                    name = f"{stage}{parity}_{key}"
                    out[name] = np.where(mask, parts[top], np.nan)
                    out[f"{name}_lo"] = np.where(mask, parts[bottom], np.nan)
        return out
