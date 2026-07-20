"""Example user strategy: EMA trend rider with an ATR trailing stop.

Drop your own .py files in this folder — every ``Strategy`` subclass is
picked up by the app (Backtest and Optimizer tabs) after a Reload. Watch
this one in the replay: the SL line visibly trails behind price.
"""

from backtester.strategy.base import Strategy


class TrailingTrend(Strategy):
    params = {
        "ema": 50,
        "atr": 14,
        "atr_mult": 3.0,
        "lots": 0.1,
    }

    def init(self):
        self.trend = self.ind.ema(self.p.ema)
        self.rng = self.ind.atr(self.p.atr)

    def on_bar(self, bar):
        atr = self.rng[self.i]
        if atr != atr:  # indicator warm-up (NaN)
            return
        stop_distance = self.p.atr_mult * atr

        if self.position is None:
            if self.cross_over(self.closes, self.trend):
                self.buy(lots=self.p.lots, sl=bar.close - stop_distance)
            elif self.cross_under(self.closes, self.trend):
                self.sell(lots=self.p.lots, sl=bar.close + stop_distance)
            return

        position = self.position
        if position.is_long:
            new_sl = bar.close - stop_distance
            if position.sl is None or new_sl > position.sl:
                self.modify(position, sl=new_sl)  # ratchet up only
            if self.cross_under(self.closes, self.trend):
                self.close(position)
        else:
            new_sl = bar.close + stop_distance
            if position.sl is None or new_sl < position.sl:
                self.modify(position, sl=new_sl)  # ratchet down only
            if self.cross_over(self.closes, self.trend):
                self.close(position)
