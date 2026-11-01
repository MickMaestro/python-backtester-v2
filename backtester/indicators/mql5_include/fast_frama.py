"""``fastframa.mqh`` — Ehlers' FRAMA (fractal adaptive MA), incremental
version — line-by-line port. Also its ``PriceSeries`` (which adds a 13th
applied price, ``(5·C + 2·O + H + L)/9``).

``CFRAMA::FRAMASeries`` is called once per bar with forward-indexed
``low``/``high`` arrays. The source keeps ``bar_prev``, ``ALFA``, ``frama``
and ``frama_prev`` in **function-level ``static`` variables**, which C++/MQL5
share between *all* instances of the class. That is reproduced (class
attributes), so — exactly as in MT5 — two CFRAMA objects in one indicator
interfere with each other. Call :meth:`CFRAMA.reset_statics` before a fresh
full recalculation (MT5 gets a fresh copy each time the indicator loads).
"""

from __future__ import annotations

from .mql_runtime import EMPTY_VALUE, MathExp, MathLog, fdiv
from .smooth_algorithms import PriceSeries as _price_series_12


class CFRAMA:
    # function-level statics of FRAMASeries (shared by all instances)
    _bar_prev = 0
    _ALFA = 0.0
    _frama = 0.0
    _frama_prev = EMPTY_VALUE

    @classmethod
    def reset_statics(cls) -> None:
        cls._bar_prev = 0
        cls._ALFA = 0.0
        cls._frama = 0.0
        cls._frama_prev = EMPTY_VALUE

    def __init__(self):
        self.m_min_near = self.m_max_near = 0.0
        self.m_min_far = self.m_max_far = 0.0
        self.m_min_all = self.m_max_all = 0.0

    def FRAMASeries(self, begin, prev_calculated, rates_total, period, price, low, high, bar):
        cls = CFRAMA
        if int(rates_total) < 2 * period or begin >= rates_total - 1:
            return EMPTY_VALUE
        if bar < begin:
            return EMPTY_VALUE
        if int(bar) < 2 * period:
            return price
        if cls._frama_prev == EMPTY_VALUE:
            self.m_min_near = self.LOWEST(bar, period, low)
            self.m_max_near = self.HIGHEST(bar, period, high)
            self.m_min_far = self.LOWEST(bar - period, period, low)
            self.m_max_far = self.HIGHEST(bar - period, period, high)
            self.m_min_all = min(self.m_min_near, self.m_min_far)
            self.m_max_all = max(self.m_max_near, self.m_max_far)
            cls._frama_prev = cls._frama = price
            cls._bar_prev = bar
            return price
        if cls._bar_prev < bar:
            if low[bar - period] == self.m_min_near:
                self.m_min_near = self.LOWEST(bar, period, low)
            if high[bar - period] == self.m_max_near:
                self.m_max_near = self.HIGHEST(bar, period, high)
            if low[bar - period] < self.m_min_far:
                self.m_min_far = low[bar - period]
            elif low[bar - 2 * period] == self.m_min_far:
                self.m_min_far = self.LOWEST(bar - period, period, low)
            if high[bar - period] > self.m_max_far:
                self.m_max_far = high[bar - period]
            elif high[bar - 2 * period] == self.m_max_far:
                self.m_max_far = self.HIGHEST(bar - period, period, high)
            self.m_min_all = min(self.m_min_near, self.m_min_far)
            self.m_max_all = max(self.m_max_near, self.m_max_far)
            cls._ALFA = self.ALFA_CALC(period)
            cls._frama_prev = cls._frama
            cls._bar_prev = bar
        if low[bar] < self.m_min_near:
            self.m_min_near = low[bar]
            self.m_min_all = min(self.m_min_near, self.m_min_far)
            cls._ALFA = self.ALFA_CALC(period)
        if high[bar] > self.m_max_near:
            self.m_max_near = high[bar]
            self.m_max_all = max(self.m_max_near, self.m_max_far)
            cls._ALFA = self.ALFA_CALC(period)
        cls._frama = cls._ALFA * price + (1 - cls._ALFA) * cls._frama_prev
        return cls._frama

    @staticmethod
    def LOWEST(StartPos, Depth, low):
        res = low[StartPos]
        for i in range(StartPos - Depth + 1, StartPos):
            if low[i] < res:
                res = low[i]
        return res

    @staticmethod
    def HIGHEST(StartPos, Depth, high):
        res = high[StartPos]
        for i in range(StartPos - Depth + 1, StartPos):
            if high[i] > res:
                res = high[i]
        return res

    def ALFA_CALC(self, period):
        N1 = (self.m_max_near - self.m_min_near) / period
        N2 = (self.m_max_far - self.m_min_far) / period
        N3 = (self.m_max_all - self.m_min_all) / (2 * period)
        D = fdiv(MathLog(N1 + N2) - MathLog(N3), MathLog(2.0))
        return MathExp(-4.6 * (D - 1.0))


def PriceSeries(applied_price, bar, Open, Low, High, Close) -> float:
    """SmoothAlgorithms' 12 applied prices plus 13 = (5·C + 2·O + H + L)/9."""
    if int(applied_price) == 13:
        return (Close[bar] * 5 + Open[bar] * 2 + High[bar] + Low[bar]) / 9
    return _price_series_12(applied_price, bar, Open, Low, High, Close)
