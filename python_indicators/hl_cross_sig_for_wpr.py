"""HL Cross Signal for WPR — converted from ``HLCrossSigForWPR.mq5`` (Bigeev
Rustem, v2.00), which ships in the ``MQL5 Include`` folder because
HLCrossSigForWPR_HTF reads it with ``iCustom``.

A breakout system: a buy arrow when the bar takes out the highest high of the
previous ``supr_period`` bars above the median-price SMA with Williams %R
above ``h_line`` (a sell mirror below ``l_line``), then trailing stop and
take-profit dots for the open side and an entry level offset by ``q`` of
the stop distance.

Details kept from the source:

- empty buffer slots are 0 (``NULL``), not EMPTY_VALUE, and the logic reads
  them that way — e.g. ``close >= SellStop[prev]`` is true whenever the
  previous sell stop is unset — so the signals match MT5; zeros are only
  turned into gaps for drawing;
- stops/takes ratchet only while the opposite side's level is unset;
- the spread term uses each bar's stored spread × point;
- MA/WPR/ATR are the terminal's ``iMA`` (SMA of the median price), ``iWPR``
  and ``iATR``.
"""

import numpy as np

from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.indicators import mql5


class HLCrossSigForWPR(Indicator):
    name = "HL Cross Signal for WPR"
    pane = Pane.PRICE
    params = {"supr_period": 6, "ma_period": 21, "risk": 0, "atr_period": 120, "q": 0.7,
              "wpr_period": 12, "h_line": -38, "l_line": -62}
    plots = [
        Plot("sell_stop", "Sell Stop", style=DrawStyle.ARROW, color="#ff0000", symbol="d", size=5),
        Plot("buy_stop", "Buy Stop", style=DrawStyle.ARROW, color="#00ff00", symbol="d", size=5),
        Plot("sell_take", "Sell TakeProfit", style=DrawStyle.ARROW, color="#ff00ff", symbol="o", size=6),
        Plot("buy_take", "Buy TakeProfit", style=DrawStyle.ARROW, color="#00ffff", symbol="o", size=6),
        Plot("sell", "Sell Signal", style=DrawStyle.ARROW, color="#ff00ff", symbol="arrow_down", size=12),
        Plot("buy", "Buy Signal", style=DrawStyle.ARROW, color="#00ffff", symbol="arrow_up", size=12),
        Plot("sell_input", "Sell Input", style=DrawStyle.ARROW, color="#ff0000", symbol="s", size=8),
        Plot("buy_input", "Buy Input", style=DrawStyle.ARROW, color="#00ff00", symbol="s", size=8),
    ]

    def calculate(self, df):
        p = self.p
        n = len(df)
        keys = ("sell_stop", "buy_stop", "sell_take", "buy_take", "sell", "buy", "sell_input", "buy_input")
        min_rates_total = int(max(p.ma_period, max(p.wpr_period, max(p.atr_period, p.supr_period + 1))))
        if n < min_rates_total:
            return {k: self.empty(n) for k in keys}
        point = mql5.point(df)
        risk = p.risk * point
        risk10 = 10 * risk
        h = self.series(df, "high")
        l = self.series(df, "low")
        c = self.series(df, "close")
        spread = (df["spread"].to_numpy(dtype=float) if "spread" in df.columns else np.zeros(n)) * point
        median = (h + l) / 2.0
        ma = mql5.sma(median, int(p.ma_period))
        ma1 = median                                       # iMA period 1 = the price itself
        wpr = mql5.wpr(h, l, c, int(p.wpr_period))
        atr = mql5.atr(h, l, c, int(p.atr_period))

        # Forward-indexed buffers; "previous bar" (MQL bar+1) is i-1.
        buf = {k: np.zeros(n) for k in keys}
        SS, BS, ST, BT = buf["sell_stop"], buf["buy_stop"], buf["sell_take"], buf["buy_take"]
        SELL, BUY, SI, BI = buf["sell"], buf["buy"], buf["sell_input"], buf["buy_input"]
        sp = int(p.supr_period)
        flag = 0
        start = min_rates_total                            # limit = rates_total-min_rates_total-1
        for i in range(start, n):
            lo = i - sp
            if lo < 0:
                continue
            lhigh = h[lo:i].max()
            llow = l[lo:i].min()
            s = spread[i]
            if flag <= 0:
                if ((h[i] >= lhigh and c[i] > ma1[i] and c[i] > ma[i] and h[i] > ma[i] and wpr[i] >= p.h_line)
                        or (c[i] >= SS[i - 1] and h[i] > lhigh)):
                    BUY[i] = min(c[i], llow + 2 * atr[i])
                    if p.risk != 0 and BUY[i] - llow > risk:
                        BUY[i] = llow + risk10
                    if c[i] < llow + risk10:
                        BUY[i] = c[i]
                    flag = 1
            if flag >= 0:
                if ((l[i] <= llow and c[i] < ma1[i] and c[i] < ma[i] and l[i] < ma[i] and wpr[i] <= p.l_line)
                        or (c[i] <= BS[i - 1] and l[i] < llow)):
                    SELL[i] = max(c[i], lhigh - 2 * atr[i])
                    if p.risk != 0 and lhigh - SELL[i] > risk:
                        SELL[i] = lhigh - risk10
                    if c[i] > lhigh - risk10:
                        SELL[i] = c[i]
                    flag = -1
            if flag > 0:
                BS[i] = llow - s * 2
                BT[i] = lhigh + s * 3
                if BS[i] < BS[i - 1] and not SS[i - 1]:
                    BS[i] = BS[i - 1]
                if BT[i] < BT[i - 1] and not ST[i - 1]:
                    BT[i] = BT[i - 1]
            if flag < 0:
                SS[i] = lhigh + s * 3
                ST[i] = llow - s * 2
                if SS[i] > SS[i - 1] and not BS[i - 1]:
                    SS[i] = SS[i - 1]
                if ST[i] > ST[i - 1] and not BT[i - 1]:
                    ST[i] = ST[i - 1]
            if BUY[i]:
                BI[i] = BUY[i] + (BUY[i] - BS[i]) * p.q
            if SELL[i]:
                SI[i] = SELL[i] - (SS[i] - SELL[i]) * p.q + s
        out = {}
        for k, arr in buf.items():
            arr = np.where(arr == 0.0, np.nan, arr)       # NULL slots are not drawn
            arr[:min_rates_total] = np.nan                 # PLOT_DRAW_BEGIN
            out[k] = arr
        return out
