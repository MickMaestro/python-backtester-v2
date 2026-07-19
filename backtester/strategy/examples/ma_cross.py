"""Moving-average crossover: long on golden cross, short on death cross."""

from backtester.strategy.base import Strategy


class MaCross(Strategy):
    params = {
        "fast": 10,
        "slow": 30,
        "lots": 0.1,
        "sl_pips": 50.0,
        "tp_pips": 100.0,
    }

    def init(self):
        self.fast_ma = self.ind.sma(self.p.fast)
        self.slow_ma = self.ind.sma(self.p.slow)

    def on_bar(self, bar):
        if self.cross_over(self.fast_ma, self.slow_ma):
            self.close_all()
            self.buy(lots=self.p.lots, sl_pips=self.p.sl_pips, tp_pips=self.p.tp_pips)
        elif self.cross_under(self.fast_ma, self.slow_ma):
            self.close_all()
            self.sell(lots=self.p.lots, sl_pips=self.p.sl_pips, tp_pips=self.p.tp_pips)
