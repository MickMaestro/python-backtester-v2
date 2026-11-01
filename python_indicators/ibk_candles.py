"""IBK Candles — converted from ``IBK-Candles v2.0.mq5`` (IBK, 2025).

Three moving-average trend filters at different speeds. Each keeps a state that
turns up when price closes above an average of the highs and down when it
closes below an average of the lows, so the state holds through the middle
ground instead of flipping on every touch. When the fast and medium filters
agree, that is the trading direction — and the candles are recoloured to show
it: blue for buys only, violet for sells only, grey while they disagree.

The candle recolouring is the same idea as the source's ``DRAW_COLOR_CANDLES``
buffer. Not converted: the background zone rectangles and the corner status
panel, which say the same thing as the candle colour, and the alerts.
"""

import numpy as np

from backtester.indicators.base import Choice, DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5

_METHODS = Choice(list(mql5.MA_METHODS), default="ema")


class IbkCandles(Indicator):
    name = "IBK Candles"
    pane = Pane.PRICE
    params = {
        "show_candles": True,
        "trend_period": 960,       # T2MA — the slow trend
        "signal_period": 80,       # T1MA — the medium filter
        "fast_period": 16,         # S1MA — the fast filter
        "method": Choice(list(mql5.MA_METHODS), default="ema"),
        "shift": 2,
        "show_trend_ma": True,
        "show_signal_ma": False,
        "show_fast_ma": False,
    }
    plots = [
        Plot("trend_ma", "Trend MA", color="#0000ff", width=3),
        Plot("trend_ma_down", "Trend MA down", color="#dc143c", width=3),
        Plot("signal_ma", "Signal MA", color="#008000", width=2.5),
        Plot("signal_ma_down", "Signal MA down", color="#bdb76b", width=2.5),
        Plot("fast_ma", "Fast MA", color="#0000ff", width=2),
        Plot("fast_ma_down", "Fast MA down", color="#dc143c", width=2),
        Plot(
            "candle_color", "Candles", style=DrawStyle.CANDLE_COLOR,
            colors=("#00bfff", "#d4d4d4", "#ee82ee"),   # buys / wait / sells
        ),
    ]

    def calculate(self, df):
        close = self.series(df, "close")
        n = len(df)

        trend_ma, trend_state = self._filter(df, int(self.p.trend_period))
        signal_ma, signal_state = self._filter(df, int(self.p.signal_period))
        fast_ma, fast_state = self._filter(df, int(self.p.fast_period))

        # Direction only when the medium and fast filters agree, matching the
        # source's TRX/ZONE logic (which uses T1 and S1, not the slow T2).
        direction = np.zeros(n)
        direction[(signal_state == 1) & (fast_state == 1)] = 1
        direction[(signal_state == -1) & (fast_state == -1)] = -1

        # Candle colour slots: 0 buys-only, 1 waiting, 2 sells-only.
        candle_color = np.where(direction > 0, 0.0, np.where(direction < 0, 2.0, 1.0))
        if not self.p.show_candles:
            candle_color = self.empty(n)

        out = {"candle_color": candle_color}
        for key, values, state, show in (
            ("trend_ma", trend_ma, trend_state, self.p.show_trend_ma),
            ("signal_ma", signal_ma, signal_state, self.p.show_signal_ma),
            ("fast_ma", fast_ma, fast_state, self.p.show_fast_ma),
        ):
            if not show:
                out[key] = self.empty(n)
                out[f"{key}_down"] = self.empty(n)
                continue
            out[key] = values
            out[f"{key}_down"] = mql5.segments(values, state == -1)
        return out

    def _filter(self, df, period: int) -> tuple[np.ndarray, np.ndarray]:
        """One MA trend filter: its plotted line and its state per bar."""
        period = max(period, 1)
        shift = int(self.p.shift)
        method = self.p.method
        close = self.series(df, "close")

        high_ma = mql5.shift_forward(
            mql5.ma(self.series(df, "high"), period, method), shift
        )
        low_ma = mql5.shift_forward(
            mql5.ma(self.series(df, "low"), period, method), shift
        )
        line = mql5.shift_forward(mql5.ma(close, period, method), shift)

        # The state is read against the previous bar's averages and carried
        # forward while price sits between them.
        above = close > mql5.shift_forward(high_ma, 1)
        below = close < mql5.shift_forward(low_ma, 1)
        state = np.zeros(len(close))
        current = 0.0
        for i in range(len(close)):
            if above[i]:
                current = 1.0
            elif below[i]:
                current = -1.0
            state[i] = current
        return line, state
