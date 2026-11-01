"""Sidus — converted from ``sidus.mq5`` (Trading signals module based on Sidus).

Two shaded ribbons — fast/slow EMA and fast/slow LWMA — each coloured by which
edge is on top, with arrows where the LWMAs cross or the slow LWMA crosses the
slow EMA. Arrows sit 3/8 × ATR(15) from the bar; ``digit`` is the minimum
gap, in points, a cross must clear.

The source's second condition compares the previous slow LWMA with the
*current* slow EMA; that is kept as written.
"""

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5
from backtester.indicators.onarray import price_choice


class Sidus(Indicator):
    name = "Sidus"
    pane = Pane.PRICE
    params = {
        "fast_ema": 18, "slow_ema": 28, "fast_lwma": 5, "slow_lwma": 8,
        "price": price_choice(), "digit": 0,
    }
    plots = [
        Plot("ema_up", "Sidus EMA (up)", style=DrawStyle.FILL, color="#8a2be2",
             fill_with="ema_up_lo"),
        Plot("ema_down", "Sidus EMA (down)", style=DrawStyle.FILL, color="#ff00ff",
             fill_with="ema_down_lo"),
        Plot("lwma_up", "Sidus LWMA (up)", style=DrawStyle.FILL, color="#00ff00",
             fill_with="lwma_up_lo"),
        Plot("lwma_down", "Sidus LWMA (down)", style=DrawStyle.FILL, color="#ff0000",
             fill_with="lwma_down_lo"),
        Plot("buy", "Sidus Buy", style=DrawStyle.ARROW, color="#008080",
             symbol="arrow_up", size=12),
        Plot("sell", "Sidus Sell", style=DrawStyle.ARROW, color="#c71585",
             symbol="arrow_down", size=12),
    ]

    def calculate(self, df):
        price = mql5.applied_price(df, self.p.price)
        fst_ema = mql5.ema(price, int(self.p.fast_ema))
        slw_ema = mql5.ema(price, int(self.p.slow_ema))
        fst_lwma = mql5.lwma(price, int(self.p.fast_lwma))
        slw_lwma = mql5.lwma(price, int(self.p.slow_lwma))
        h = self.series(df, "high")
        l = self.series(df, "low")
        atr = mql5.atr(h, l, self.series(df, "close"), 15)
        gap = max(int(self.p.digit), 0) * mql5.point(df)
        n = len(price)

        buy = self.empty(n)
        sell = self.empty(n)
        start = int(max(self.p.fast_lwma, self.p.slow_lwma)) + 3
        for i in range(start, n):
            rng = atr[i] * 3.0 / 8.0
            if fst_lwma[i] > slw_lwma[i] + gap and fst_lwma[i - 1] <= slw_lwma[i - 1]:
                buy[i] = l[i] - rng
            if slw_lwma[i] > slw_ema[i] + gap and slw_lwma[i - 1] <= slw_ema[i]:
                buy[i] = l[i] - rng
            if fst_lwma[i] < slw_lwma[i] - gap and fst_lwma[i - 1] >= slw_lwma[i - 1]:
                sell[i] = h[i] + rng
            if slw_lwma[i] < slw_ema[i] - gap and slw_lwma[i - 1] >= slw_ema[i]:
                sell[i] = h[i] + rng

        out = {"buy": buy, "sell": sell}
        for key, a, b in (("ema", fst_ema, slw_ema), ("lwma", fst_lwma, slw_lwma)):
            up = a >= b
            down = a < b
            out[f"{key}_up"] = mql5.segments(a, up)
            out[f"{key}_up_lo"] = mql5.segments(b, up)
            out[f"{key}_down"] = mql5.segments(a, down)
            out[f"{key}_down_lo"] = mql5.segments(b, down)
        return out
