"""RSI mean-reversion: buy oversold bounces, sell overbought fades."""

from backtester.strategy.base import Strategy


class RsiReversion(Strategy):
    params = {
        "period": 14,
        "lower": 30.0,
        "upper": 70.0,
        "lots": 0.1,
        "sl_pips": 40.0,
        "tp_pips": 80.0,
    }

    def init(self):
        self.rsi = self.ind.rsi(self.p.period)

    def on_bar(self, bar):
        if self.position is not None:
            return  # one position at a time; exits are handled by SL/TP
        i = self.i
        if i < 1 or any(map(_isnan, (self.rsi[i - 1], self.rsi[i]))):
            return
        if self.rsi[i - 1] < self.p.lower <= self.rsi[i]:
            self.buy(lots=self.p.lots, sl_pips=self.p.sl_pips, tp_pips=self.p.tp_pips)
        elif self.rsi[i - 1] > self.p.upper >= self.rsi[i]:
            self.sell(lots=self.p.lots, sl_pips=self.p.sl_pips, tp_pips=self.p.tp_pips)


def _isnan(value: float) -> bool:
    return value != value
