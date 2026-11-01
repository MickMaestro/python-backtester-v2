"""XU Sessions — converted from ``XU Sessions BT + Clock.mq5`` (XU v042).

Horizontal lines at the high and low of the Asia, Europe and America sessions
(GMT hours as inputs) for the last ``history_days`` days, with optional
midpoints.

The source finds the broker's GMT offset from the live terminal clock. A
history chart has no live clock, so it is a parameter here,
``server_gmt_offset`` (bar times are broker server time; 2 suits most EET
brokers in winter, 3 in summer). As with Daily Range, a session still in
progress is drawn at its high/low so far, growing bar by bar, and is
replaced by its final lines once it ends. The world clocks, GMT label, bias
label and on/off button are left out.
"""

import numpy as np
import pandas as pd

from backtester.indicators.base import Indicator, Pane, Plot
from backtester.indicators import mql5

SESSIONS = (("asia", "Asia", "#a52a2a"), ("euro", "Europe", "#1e90ff"),
            ("amer", "America", "#00ff00"))


class XuSessions(Indicator):
    name = "XU Sessions"
    pane = Pane.PRICE
    params = {
        "asia_open_gmt": 0.0, "asia_close_gmt": 9.0,
        "europe_open_gmt": 8.0, "europe_close_gmt": 16.0,
        "america_open_gmt": 14.5, "america_close_gmt": 22.0,
        "server_gmt_offset": 2, "history_days": 6, "show_midpoints": False,
    }

    def setup(self):
        plots = []
        for key, label, colour in SESSIONS:
            for stage in ("final", "live"):
                kw = {"expires_at": f"{key}_{stage}_expires"}
                if stage == "final":
                    kw["known_at"] = f"{key}_known"
                plots.append(Plot(f"{key}_{stage}_h", f"{label} high", color=colour, width=3, **kw))
                plots.append(Plot(f"{key}_{stage}_l", f"{label} low", color=colour, width=3, **kw))
                if self.p.show_midpoints:
                    plots.append(Plot(f"{key}_{stage}_m", f"{label} mid", color=colour,
                                      width=1, dash=True, **kw))
        self.plots = plots

    def calculate(self, df):
        t = pd.to_datetime(df["time"]).to_numpy()
        h = self.series(df, "high")
        l = self.series(df, "low")
        n = len(t)
        days = mql5.day_index(df)
        n_days = int(days.max()) + 1 if n else 0
        day_last = np.r_[np.nonzero(np.diff(days))[0], n - 1] if n else np.array([], int)
        day_starts = t.astype("datetime64[D]")
        offset_h = float(self.p.server_gmt_offset)
        keep = max(int(self.p.history_days), 1)
        hours = {
            "asia": (self.p.asia_open_gmt, self.p.asia_close_gmt),
            "euro": (self.p.europe_open_gmt, self.p.europe_close_gmt),
            "amer": (self.p.america_open_gmt, self.p.america_close_gmt),
        }

        out = {}
        for key, _label, _colour in SESSIONS:
            open_h, close_h = (float(v) + offset_h for v in hours[key])
            start = day_starts + np.timedelta64(int(round(open_h * 3600)), "s")
            end = day_starts + np.timedelta64(int(round(close_h * 3600)), "s")
            # Each bar belongs to the session of its own calendar day when its
            # time falls in [open, close).
            in_session = (t >= start) & (t < end)
            group = np.where(in_session, days, -1)

            final_h = np.full(n, np.nan)
            final_l = np.full(n, np.nan)
            live_h = np.full(n, np.nan)
            live_l = np.full(n, np.nan)
            known = np.full(n, np.inf)
            final_exp = np.full(n, -np.inf)
            live_exp = np.full(n, -np.inf)
            if in_session.any():
                frame = pd.DataFrame({"g": group[in_session], "h": h[in_session],
                                      "l": l[in_session]})
                idx = np.nonzero(in_session)[0]
                grouped = frame.groupby("g")
                final_h[idx] = grouped["h"].transform("max").to_numpy()
                final_l[idx] = grouped["l"].transform("min").to_numpy()
                live_h[idx] = grouped["h"].cummax().to_numpy()
                live_l[idx] = grouped["l"].cummin().to_numpy()
                last_in_session = pd.Series(idx).groupby(frame["g"].to_numpy()).transform("max").to_numpy()
                known[idx] = last_in_session
                live_exp[idx] = last_in_session - 1
                # Shown for this day and the next ``history_days - 1`` days.
                target = days[idx] + keep - 1
                final_exp[idx] = np.where(target < n_days,
                                          day_last[np.minimum(target, n_days - 1)], np.inf)

            out[f"{key}_known"] = known
            out[f"{key}_final_expires"] = final_exp
            out[f"{key}_live_expires"] = live_exp
            for stage, hi, lo in (("final", final_h, final_l), ("live", live_h, live_l)):
                out[f"{key}_{stage}_h"] = hi
                out[f"{key}_{stage}_l"] = lo
                out[f"{key}_{stage}_m"] = (hi + lo) / 2.0
        return out
