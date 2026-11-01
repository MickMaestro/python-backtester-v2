"""``IndicatorsAlgorithms.mqh`` (Nikolay Kositsin, 2010) — line-by-line port.

Three composite per-bar classes built on :mod:`.smooth_algorithms`:

- ``CLRMA``: linear-regression MA, ``3·LWMA − 2·SMA``.
- ``CVidyaBands``: VIDYA with standard-deviation bands around it.
- ``CBBands``: Bollinger-style bands around any of the four classic MAs.

Same calling convention as the library: one call per bar inside the
indicator's loop. MQL5's ``double&`` out-parameters (``DnMovSeries``,
``MovSeries``, ``UpMovSeries``) are returned as a tuple after the result::

    std, dn, mid, up = bands.BBandsSeries(begin, prev, total, 20, 2.0,
                                          MODE_SMA, price, bar, False)
"""

from __future__ import annotations

from .smooth_algorithms import CCMO, CMoving_Average, CStdDeviation


class CLRMA:
    def __init__(self):
        self.m_SMA = CMoving_Average()
        self.m_LWMA = CMoving_Average()

    def LRMASeries(self, begin, prev_calculated, rates_total, Length, series, bar, set):
        sma = self.m_SMA.SMASeries(begin, prev_calculated, rates_total, Length, series, bar, set)
        lwma = self.m_LWMA.LWMASeries(begin, prev_calculated, rates_total, Length, series, bar, set)
        # During warm-up both are EMPTY_VALUE, and so is 3·E − 2·E — as in MQL5.
        return 3.0 * lwma - 2.0 * sma


class CVidyaBands:
    def __init__(self):
        self.m_VIDYA = CCMO()
        self.m_STD = CStdDeviation()

    def VidyaBandsSeries(self, begin, prev_calculated, rates_total, CMO_period, EMA_period,
                         BBLength, deviation, series, bar, set):
        """Returns ``(StdDev, DnMovSeries, MovSeries, UpMovSeries)``."""
        MovSeries = self.m_VIDYA.VIDYASeries(begin, prev_calculated, rates_total, CMO_period,
                                             EMA_period, series, bar, set)
        StdDev = self.m_STD.StdDevSeries(begin + CMO_period + 1, prev_calculated, rates_total,
                                         BBLength, deviation, series, MovSeries, bar, set)
        return StdDev, MovSeries - StdDev, MovSeries, MovSeries + StdDev


class CBBands:
    def __init__(self):
        self.m_STD = CStdDeviation()
        self.m_MA = CMoving_Average()

    def BBandsSeries(self, begin, prev_calculated, rates_total, Length, deviation, MA_Method,
                     series, bar, set):
        """Returns ``(StdDev, DnMovSeries, MovSeries, UpMovSeries)``."""
        MovSeries = self.m_MA.MASeries(begin, prev_calculated, rates_total, Length, MA_Method,
                                       series, bar, set)
        StdDev = self.m_STD.StdDevSeries(begin, prev_calculated, rates_total, Length, deviation,
                                         series, MovSeries, bar, set)
        return StdDev, MovSeries - StdDev, MovSeries, MovSeries + StdDev

    def BBandsSeries_(self, begin, prev_calculated, rates_total, MALength, MA_Method, BBLength,
                      deviation, series, bar, set):
        """Separate MA and band lengths. Returns ``(StdDev, Dn, Mov, Up)``."""
        MovSeries = self.m_MA.MASeries(begin, prev_calculated, rates_total, MALength, MA_Method,
                                       series, bar, set)
        StdDev = self.m_STD.StdDevSeries(begin + MALength + 1, prev_calculated, rates_total,
                                         BBLength, deviation, series, MovSeries, bar, set)
        return StdDev, MovSeries - StdDev, MovSeries, MovSeries + StdDev
