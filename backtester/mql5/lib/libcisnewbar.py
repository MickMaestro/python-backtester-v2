"""libcisnewbar.mqh — MQL5 include file, translated by backtester.mql5 (translator 1.0).

Shared by the converted indicators that #include it. Generated: do not edit.
"""
# flake8: noqa
from backtester.mql5.runtime import *


class CisNewBar(MqlObject):
    _q_fields = ('m_lastbar_time', 'm_symbol', 'm_period', 'm_retcode', 'm_new_bars', 'm_comment')
    def __init__(self):
        self.m_lastbar_time = 0
        self.m_symbol = ""
        self.m_period = 0
        self.m_retcode = 0
        self.m_new_bars = 0
        self.m_comment = ""
        self.m_retcode = 0
        self.m_lastbar_time = 0
        self.m_new_bars = 0
        self.m_comment = ''
        self.m_symbol = Symbol()
        self.m_period = Period()
    def CisNewBar(self):
        pass
    def GetRetCode(self):
        return self.m_retcode
    def GetLastBarTime(self):
        return self.m_lastbar_time
    def GetNewBars(self):
        return self.m_new_bars
    def GetComment(self):
        return self.m_comment
    def GetSymbol(self):
        return self.m_symbol
    def GetPeriod(self):
        return self.m_period
    def SetLastBarTime(self, lastbar_time):
        self.m_lastbar_time = lastbar_time
    def SetSymbol(self, symbol):
        self.m_symbol = (Symbol() if (symbol == "" or symbol == '') else symbol)
    def SetPeriod(self, period):
        self.m_period = (Period() if (period == PERIOD_CURRENT) else period)
    def isNewBar_1(self, newbar_time):
        self.m_new_bars = 0
        self.m_retcode = 0
        self.m_comment = 'CisNewBar::isNewBar' + ' The checking of the new bar completed'
        if self.m_lastbar_time > newbar_time:
            self.m_comment = 'CisNewBar::isNewBar' + ' Synchronization error: last bar time ' + TimeToString(self.m_lastbar_time) + ', new bar time ' + TimeToString(newbar_time)
            self.m_retcode = -1
            return False
        if self.m_lastbar_time == 0:
            self.m_lastbar_time = newbar_time
            self.m_comment = 'CisNewBar::isNewBar' + ' Initialization of lastbar_time=' + TimeToString(self.m_lastbar_time)
            return False
        if self.m_lastbar_time < newbar_time:
            self.m_new_bars = 1
            self.m_lastbar_time = newbar_time
            return True
        return False
    def isNewBar_0(self):
        newbar_time = Box(0)
        lastbar_time = self.m_lastbar_time
        ResetLastError()
        if not SeriesInfoInteger(self.m_symbol, self.m_period, SERIES_LASTBAR_DATE, newbar_time):
            self.m_retcode = GetLastError()
            self.m_comment = 'CisNewBar::isNewBar' + ' Error in request of the time of last bar: ' + IntegerToString(self.m_retcode)
            return 0
        if not self.isNewBar_1(newbar_time.v):
            return 0
        self.m_new_bars = Bars(self.m_symbol, self.m_period, lastbar_time, newbar_time.v) - 1
        return self.m_new_bars

__all__ = ['CisNewBar']
