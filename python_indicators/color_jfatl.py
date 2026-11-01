"""ColorJFatl — converted from ``colorjfatl.mq5`` (Trading signals module based
on ColorJFatl).

FATL (a 39-tap "fast adaptive trend line" digital filter) smoothed again with
Jurik's JMA. The line is gold while rising, magenta while falling, grey when
flat.
"""

import numpy as np

from backtester.indicators import smoothing as sm
from backtester.indicators.base import Indicator, Pane, Plot
from backtester.indicators import mql5

FATL_TABLE = np.array([
    +0.4360409450, +0.3658689069, +0.2460452079, +0.1104506886,
    -0.0054034585, -0.0760367731, -0.0933058722, -0.0670110374,
    -0.0190795053, +0.0259609206, +0.0502044896, +0.0477818607,
    +0.0249252327, -0.0047706151, -0.0272432537, -0.0338917071,
    -0.0244141482, -0.0055774838, +0.0128149838, +0.0226522218,
    +0.0208778257, +0.0100299086, -0.0036771622, -0.0136744850,
    -0.0160483392, -0.0108597376, -0.0016060704, +0.0069480557,
    +0.0110573605, +0.0095711419, +0.0040444064, -0.0023824623,
    -0.0067093714, -0.0072003400, -0.0047717710, +0.0005541115,
    +0.0007860160, +0.0130129076, +0.0040364019,
])


def fatl(values: np.ndarray) -> np.ndarray:
    """sum_k table[k] * price[i-k], from the first full window on."""
    out = np.full(len(values), np.nan)
    size = len(FATL_TABLE)
    if len(values) >= size:
        out[size - 1:] = np.convolve(values, FATL_TABLE, mode="valid")
    return out


class ColorJFatl(Indicator):
    name = "ColorJFatl"
    pane = Pane.PRICE
    params = {
        "jma_length": 5, "jma_phase": -100, "price": sm.price_choice(),
        "fatl_shift": 0, "price_shift": 0,
    }
    plots = [
        Plot("flat", "JFatl", color="#808080", width=2),
        Plot("up", "JFatl rising", color="#ffd700", width=2),
        Plot("down", "JFatl falling", color="#ff00ff", width=2),
    ]

    def calculate(self, df):
        price = sm.price_series(df, self.p.price)
        begin = len(FATL_TABLE) - 1
        line = sm.jjma(fatl(price), int(self.p.jma_length), int(self.p.jma_phase), begin)
        line = line + int(self.p.price_shift) * mql5.point(df)
        prev = mql5.previous(line)
        rising = line > prev
        falling = line < prev
        flat = ~rising & ~falling & np.isfinite(line)
        shift = int(self.p.fatl_shift)
        return {
            key: mql5.shift_forward(mql5.segments(line, mask), shift)
            for key, mask in (("flat", flat), ("up", rising), ("down", falling))
        }
