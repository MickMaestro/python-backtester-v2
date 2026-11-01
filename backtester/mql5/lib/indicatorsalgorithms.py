"""indicatorsalgorithms.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *
from backtester.mql5.lib.smoothalgorithms import *  # SmoothAlgorithms.mqh


class CLRMA(MqlObject):
    _q_fields = ('m_SMA', 'm_LWMA')
    def __init__(self, *args):
        self.m_SMA = CMoving_Average()
        self.m_LWMA = CMoving_Average()
    def LRMASeries(self, begin, prev_calculated, rates_total, Length, series, bar, set_):
        sma = 0.0
        lwma = 0.0
        lrma = 0.0
        sma = self.m_SMA.SMASeries(begin, prev_calculated, rates_total, Length, series, bar, set_)
        lwma = self.m_LWMA.LWMASeries(begin, prev_calculated, rates_total, Length, series, bar, set_)
        lrma = (3.0 * lwma) - (2.0 * sma)
        return lrma

class CVidyaBands(MqlObject):
    _q_fields = ('m_VIDYA', 'm_STD')
    def __init__(self, *args):
        self.m_VIDYA = CCMO()
        self.m_STD = CStdDeviation()
    def VidyaBandsSeries(self, begin, prev_calculated, rates_total, CMO_period, EMA_period, BBLength, deviation, series, bar, set_, DnMovSeries, MovSeries, UpMovSeries):
        MovSeries.v = self.m_VIDYA.VIDYASeries(begin, prev_calculated, rates_total, CMO_period, EMA_period, series, bar, set_)
        StdDev = self.m_STD.StdDevSeries(begin + CMO_period + 1, prev_calculated, rates_total, BBLength, deviation, series, MovSeries.v, bar, set_)
        DnMovSeries.v = MovSeries.v - StdDev
        UpMovSeries.v = MovSeries.v + StdDev
        return StdDev

class CBBands(MqlObject):
    _q_fields = ('m_STD', 'm_MA')
    def __init__(self, *args):
        self.m_STD = CStdDeviation()
        self.m_MA = CMoving_Average()
    def BBandsSeries(self, begin, prev_calculated, rates_total, Length, deviation, MA_Method, series, bar, set_, DnMovSeries, MovSeries, UpMovSeries):
        MovSeries.v = self.m_MA.MASeries(begin, prev_calculated, rates_total, Length, MA_Method, series, bar, set_)
        StdDev = self.m_STD.StdDevSeries(begin, prev_calculated, rates_total, Length, deviation, series, MovSeries.v, bar, set_)
        DnMovSeries.v = MovSeries.v - StdDev
        UpMovSeries.v = MovSeries.v + StdDev
        return StdDev
    def BBandsSeries_(self, begin, prev_calculated, rates_total, MALength, MA_Method, BBLength, deviation, series, bar, set_, DnMovSeries, MovSeries, UpMovSeries):
        MovSeries.v = self.m_MA.MASeries(begin, prev_calculated, rates_total, MALength, MA_Method, series, bar, set_)
        StdDev = self.m_STD.StdDevSeries(begin + MALength + 1, prev_calculated, rates_total, BBLength, deviation, series, MovSeries.v, bar, set_)
        DnMovSeries.v = MovSeries.v - StdDev
        UpMovSeries.v = MovSeries.v + StdDev
        return StdDev

__all__ = ['CLRMA', 'CVidyaBands', 'CBBands']
