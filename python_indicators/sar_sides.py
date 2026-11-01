"""SAR Above/Below — converted from ``notifyicon_test_indicator.mq5`` (Notify Icon
library's test indicator).

MT5's Parabolic SAR split by side: orange-red dots while SAR is above the
close (downtrend), blue while below. The source's point is to show a Windows
tray balloon when the side flips; that notification is left out.
"""

import numpy as np

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


class SarSides(Indicator):
    name = "SAR Above/Below"
    pane = Pane.PRICE
    params = {"step": 0.02, "maximum": 0.2}
    plots = [
        Plot("upper", "Upper SAR", style=DrawStyle.ARROW, color="#ff4500", size=5),
        Plot("lower", "Lower SAR", style=DrawStyle.ARROW, color="#1e90ff", size=5),
    ]

    def calculate(self, df):
        sar = mql5.sar(self.series(df, "high"), self.series(df, "low"),
                       float(self.p.step), float(self.p.maximum))
        close = self.series(df, "close")
        above = sar > close
        return {"upper": np.where(above, sar, np.nan),
                "lower": np.where(~above & np.isfinite(sar), sar, np.nan)}
