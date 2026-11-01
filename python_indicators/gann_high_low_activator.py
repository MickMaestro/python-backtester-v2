"""Gann High/Low Activator — converted from ``Gann_high-low_activator_2.mq5``
(mladen).

A moving average of the previous bar's high and another of its low form a zone.
Closing above the upper one turns the state up, below the lower one turns it
down, and the *opposite* band becomes the activator line — the level that has
to break for the state to flip back. The line is drawn in the state's colour.

The optional noise filter is the source's ``iFilter``: a value only moves when
its change clears a multiple of the recent change's standard deviation. It is
off by default (``filter = 0``), exactly as in the original.

Not converted: the multi-timeframe path (``iCustom`` on another timeframe plus
interpolation) and the alerts. This app charts one dataset at a time, so the
indicator computes on the loaded timeframe.
"""

import numpy as np

from backtester.indicators.base import Choice, DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


class GannHighLowActivator(Indicator):
    name = "Gann High/Low Activator"
    pane = Pane.PRICE
    params = {
        "period": 36,
        "method": Choice(list(mql5.MA_METHODS), default="ema"),
        "filter": 0.0,
        "filter_on": Choice(
            {"prices": "Filter the prices", "values": "Filter the averages",
             "all": "Filter all"},
            default="prices",
        ),
    }
    plots = [
        Plot("zone_high", "Gann zone", style=DrawStyle.FILL, color="#5a5a5a",
             fill_with="zone_low"),
        Plot("zone_low", "Gann zone low", style=DrawStyle.NONE),
        Plot("mid", "Gann middle", color="#808080", width=1, dash=True),
        Plot("activator", "Gann high/low", color="#696969", width=2),
        Plot("activator_up", "Activator up", color="#00bfff", width=2),
        Plot("activator_down", "Activator down", color="#db7093", width=2),
    ]

    def calculate(self, df):
        period = max(int(self.p.period), 1)
        price_filter = 0.0 if self.p.filter_on == "values" else float(self.p.filter)
        value_filter = 0.0 if self.p.filter_on == "prices" else float(self.p.filter)

        high = self.series(df, "high")
        low = self.series(df, "low")
        close = self.series(df, "close")
        n = len(df)

        # The averages run on the *previous* bar's high and low. Bar 0 has no
        # previous bar; seed it with its own value so the recursive averages
        # aren't poisoned by a NaN, then blank the first bar at the end.
        prev_high = mql5.shift_forward(high, 1)
        prev_low = mql5.shift_forward(low, 1)
        prev_high[0] = high[0]
        prev_low[0] = low[0]

        upper = mql5.noise_filter(
            mql5.running_ma(
                mql5.noise_filter(prev_high, period, price_filter), period, self.p.method
            ),
            period, value_filter,
        )
        lower = mql5.noise_filter(
            mql5.running_ma(
                mql5.noise_filter(prev_low, period, price_filter), period, self.p.method
            ),
            period, value_filter,
        )
        mid = (upper + lower) / 2.0
        filtered_close = mql5.noise_filter(close, period, price_filter)

        state = np.zeros(n)
        activator = self.empty(n)
        for i in range(n):
            if filtered_close[i] > upper[i]:
                state[i] = 1
            elif filtered_close[i] < lower[i]:
                state[i] = 2
            else:
                state[i] = state[i - 1] if i else 0

            if state[i] == 1:
                activator[i] = lower[i]
            elif state[i] == 2:
                activator[i] = upper[i]
            else:
                activator[i] = filtered_close[i]

        for series in (upper, lower, mid, activator):
            series[0] = np.nan

        return {
            "zone_high": upper,
            "zone_low": lower,
            "mid": mid,
            "activator": activator,
            "activator_up": mql5.segments(activator, state == 1),
            "activator_down": mql5.segments(activator, state == 2),
        }
