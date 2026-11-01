"""ColorLaguerre — converted from ``colorlaguerre.mq5`` (Trading signals module
based on ColorLaguerre).

Ehlers' Laguerre RSI: a four-stage Laguerre filter, then an RSI of the
stage-to-stage differences, 0..100. The line turns green on entering the top
zone or leaving the bottom one and red the other way, holding its colour
while it stays between the middle level and a band; it is drawn only once
coloured.

One fix: on a perfectly flat stretch the source multiplies the previous value
by 100 again (``LRSI*=100`` with no new ratio). Here the value is held.
"""

import numpy as np

from backtester.indicators.base import Indicator, Level, Pane, Plot
from backtester.indicators import mql5
from backtester.indicators.onarray import price_choice

HIGH, HIGH_MID, LOW_MID, LOW, EMPTY = 1, 2, 3, 4, 0


def _zone(value, high, middle, low):
    zone = EMPTY
    if value > high:
        zone = HIGH
    elif value > middle:
        zone = HIGH_MID
    if value < low:
        zone = LOW
    elif value <= middle:
        zone = LOW_MID
    return zone


class ColorLaguerre(Indicator):
    name = "ColorLaguerre"
    pane = Pane.SEPARATE
    params = {"gamma": 0.7, "high_level": 85, "middle_level": 50, "low_level": 15,
              "price": price_choice()}
    plots = [
        Plot("up", "Laguerre up", color="#00ff00", width=1),
        Plot("down", "Laguerre down", color="#ff0000", width=1),
    ]
    y_range = (0, 100)

    def setup(self):
        self.levels = [Level(float(min(max(v, 0), 100)), color="#0000ff") for v in
                       (self.p.high_level, self.p.middle_level, self.p.low_level)]

    def calculate(self, df):
        gamma = float(self.p.gamma)
        high, middle, low = (min(max(int(v), 0), 100) for v in
                             (self.p.high_level, self.p.middle_level, self.p.low_level))
        price = mql5.applied_price(df, self.p.price)
        n = len(price)
        line = self.empty(n)
        slot = np.zeros(n)
        if n < 3:
            return {"up": line, "down": line.copy()}

        l0 = l1 = l2 = l3 = price[1]
        lrsi = 0.0
        for i in range(1, n):
            l0a, l1a, l2a, l3a = l0, l1, l2, l3
            l0 = (1 - gamma) * price[i] + gamma * l0a
            l1 = -gamma * l0 + l0a + gamma * l1a
            l2 = -gamma * l1 + l1a + gamma * l2a
            l3 = -gamma * l2 + l2a + gamma * l3a
            cu = cd = 0.0
            for a, b in ((l0, l1), (l1, l2), (l2, l3)):
                if a >= b:
                    cu += a - b
                else:
                    cd += b - a
            if cu + cd != 0:
                lrsi = cu / (cu + cd) * 100.0
            line[i] = lrsi

            if i < 32:
                continue
            now = _zone(line[i], high, middle, low)
            before = _zone(line[i - 1], high, middle, low)
            if now == HIGH:
                slot[i] = 1
            elif now == LOW:
                slot[i] = 2
            elif now == HIGH_MID:
                slot[i] = {HIGH: 2, HIGH_MID: slot[i - 1], LOW_MID: 1, LOW: 1}.get(before, slot[i])
            elif now == LOW_MID:
                slot[i] = {HIGH: 2, HIGH_MID: 2, LOW_MID: slot[i - 1], LOW: 1}.get(before, slot[i])

        # Colour 0 is CLR_NONE in the source: those stretches are not drawn.
        return {
            "up": mql5.segments(line, slot == 1),
            "down": mql5.segments(line, slot == 2),
        }
