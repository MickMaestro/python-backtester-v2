"""XU ADR Levels — converted from ``XU v50 Mt5.mq5``.

Fibonacci-flavoured targets measured from the day's open in units of the
average daily range. The ADR is the source's blend: the mean of yesterday's
range and the 5-, 10- and 20-day average ranges. Levels sit at 21.4%, 38.2%,
61.8%, 78.6%, 100%, 121.4%, 138.2% and 161.8% of it either side of the open,
with a buy/sell pair at a smaller percentage.

The original draws today's levels as chart objects that get redrawn each day.
Here every bar carries its own day's levels, so the whole history is visible
and the levels step at each day boundary. The ADR uses days *before* the
current one, as the source does, so nothing is lit by hindsight.

Not converted: the on-chart text labels, the per-symbol pip-size table (this
app already knows each dataset's contract spec), and the auto-refresh timer.
"""

import numpy as np
import pandas as pd

from backtester.indicators.base import Indicator, Pane, Plot

#: The levels the source draws lines for, in percent of the ADR.
LEVELS = (21.4, 38.2, 61.8, 78.6, 100.0, 121.4, 138.2, 161.8)


class XuAdrLevels(Indicator):
    name = "XU ADR Levels"
    pane = Pane.PRICE
    params = {"open_position_percent": 10.0, "levels": len(LEVELS)}

    def setup(self):
        count = max(0, min(int(self.p.levels), len(LEVELS)))
        self.plots = [
            Plot("open", "Day open", color="#c8c8c8", width=1.5),
            Plot("buy", "Buy level", color="#00ffff", width=1.5, dash=True),
            Plot("sell", "Sell level", color="#ff69b4", width=1.5, dash=True),
        ]
        for i, percent in enumerate(LEVELS[:count], start=1):
            self.plots.append(
                Plot(f"up_{i}", f"+{percent:g}%", color="#696969", width=1, dash=True)
            )
            self.plots.append(
                Plot(f"down_{i}", f"-{percent:g}%", color="#696969", width=1, dash=True)
            )

    def calculate(self, df):
        daily = _daily_frame(df)
        day_range = daily["high"] - daily["low"]

        # Averages of the ranges *before* each day: shift, then roll.
        previous = pd.Series(day_range).shift(1)
        adr1 = previous
        adr5 = previous.rolling(5, min_periods=1).mean()
        adr10 = previous.rolling(10, min_periods=1).mean()
        adr20 = previous.rolling(20, min_periods=1).mean()
        adr = ((adr1 + adr5 + adr10 + adr20) / 4.0).to_numpy()

        index = daily["index"]
        adr_per_bar = adr[index]
        open_per_bar = daily["open"].to_numpy()[index]

        out = {"open": open_per_bar}
        offset = adr_per_bar * (float(self.p.open_position_percent) / 100.0)
        out["buy"] = open_per_bar + offset
        out["sell"] = open_per_bar - offset

        count = max(0, min(int(self.p.levels), len(LEVELS)))
        for i, percent in enumerate(LEVELS[:count], start=1):
            distance = adr_per_bar * (percent / 100.0)
            out[f"up_{i}"] = open_per_bar + distance
            out[f"down_{i}"] = open_per_bar - distance
        return out


def _daily_frame(df) -> dict:
    """Per-day open/high/low plus the day index of every bar."""
    days = df["time"].to_numpy().astype("datetime64[D]")
    _unique, index = np.unique(days, return_inverse=True)
    frame = pd.DataFrame(
        {
            "day": index,
            "open": df["open"].to_numpy(dtype=float),
            "high": df["high"].to_numpy(dtype=float),
            "low": df["low"].to_numpy(dtype=float),
        }
    )
    grouped = frame.groupby("day", sort=True)
    return {
        "open": grouped["open"].first(),
        "high": grouped["high"].max().to_numpy(),
        "low": grouped["low"].min().to_numpy(),
        "index": index,
    }
