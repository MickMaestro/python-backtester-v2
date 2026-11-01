"""New-bar detection: ``LibCisNewBar.mqh`` (Lizar, 2010), ``OnNewBarCalculate.mqh``
and the ``CIsNewBar`` class from ``TradeAlgorithms.mqh`` — ports.

In the terminal these classes answer "did a new bar open since the last
tick?". A converted indicator recalculates over complete history, where every
bar is new exactly once, so they are mostly useful when porting a source
line by line, or when replaying bar by bar. Times are integer seconds since
1970 (MQL5 ``datetime``) — ``int(pd.Timestamp(t).timestamp())``.
"""

from __future__ import annotations

from bisect import bisect_left, bisect_right


class CisNewBar:
    """``LibCisNewBar.mqh``."""

    def __init__(self, symbol: str = "", period: int = 0, times=None):
        self.m_retcode = 0
        self.m_lastbar_time = 0
        self.m_new_bars = 0
        self.m_comment = ""
        self.m_symbol = symbol
        self.m_period = period
        #: Bar open times (ascending) standing in for the terminal's series
        #: data, used by the argument-less :meth:`isNewBar`.
        self.times = list(times) if times is not None else []

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

    def SetLastBarTime(self, lastbar_time: int):
        self.m_lastbar_time = int(lastbar_time)

    def SetSymbol(self, symbol: str):
        self.m_symbol = symbol

    def SetPeriod(self, period: int):
        self.m_period = period

    def isNewBar(self, newbar_time: int | None = None):
        """With a time: ``bool isNewBar(datetime)``. Without: ``int isNewBar()``
        — the number of new bars, read from :attr:`times`."""
        if newbar_time is None:
            if not self.times:
                self.m_retcode = -1
                self.m_comment = "isNewBar: no bar times available"
                return 0
            lastbar_time = self.m_lastbar_time
            new_time = int(self.times[-1])
            if not self._is_new(new_time):
                return 0
            # Bars(symbol, period, lastbar_time, newbar_time) - 1
            count = bisect_right(self.times, new_time) - bisect_left(self.times, lastbar_time)
            self.m_new_bars = count - 1
            return self.m_new_bars
        return self._is_new(int(newbar_time))

    def _is_new(self, newbar_time: int) -> bool:
        self.m_new_bars = 0
        self.m_retcode = 0
        self.m_comment = "isNewBar: the checking of the new bar completed"
        if self.m_lastbar_time > newbar_time:
            self.m_comment = (f"isNewBar: synchronization error: last bar time "
                              f"{self.m_lastbar_time}, new bar time {newbar_time}")
            self.m_retcode = -1
            return False
        if self.m_lastbar_time == 0:
            self.m_lastbar_time = newbar_time
            self.m_comment = f"isNewBar: initialization of lastbar_time={self.m_lastbar_time}"
            return False
        if self.m_lastbar_time < newbar_time:
            self.m_new_bars = 1
            self.m_lastbar_time = newbar_time
            return True
        return False


class CIsNewBar:
    """``TradeAlgorithms.mqh``'s variant: ``IsNewBar(symbol, timeframe)`` is
    true on the first call and whenever the newest bar time changes. Feed it
    the newest bar time with :meth:`IsNewBarTime`."""

    def __init__(self):
        self.m_TOld = -1

    def IsNewBarTime(self, newest_bar_time: int) -> bool:
        TNew = int(newest_bar_time)
        if TNew != self.m_TOld and TNew:
            self.m_TOld = TNew
            return True
        return False


def on_new_bar_calculate(times, period_seconds: int, current_time: int, chart: CisNewBar) -> bool:
    """``OnNewBarCalculate.mqh``'s ``OnCalculate`` gate: true when the bar
    containing ``current_time`` (rounded down to the period) is new — the
    point at which the include calls the indicator's ``OnNewBarCalculate``."""
    new_time = int(current_time) // int(period_seconds) * int(period_seconds)
    return chart.isNewBar(new_time)
