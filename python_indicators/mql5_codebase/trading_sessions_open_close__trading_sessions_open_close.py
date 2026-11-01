"""trading_sessions_open_close — converted from MQL5: MQL5 Indicators/Trading Sessions Open - Close/trading_sessions_open_close.mq5

Copyright: VDVSoft; Link: vdv_2001@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'VDVSoft', 'link': 'vdv_2001@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 7, 2: 7, 3: 7}, 'colors': {1: [14804223], 2: [16443110], 3: [10025880]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Asian session High; Asian session Low', 2: 'European session High; European session Low', 3: 'American session'}, 'levels': [], 'description': [], 'name': 'trading_sessions_open_close', 'source': 'MQL5 Indicators/Trading Sessions Open - Close/trading_sessions_open_close.mq5', 'folder': 'Trading Sessions Open - Close', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
AsiaHigh = Arr(0, 0.0)
AsiaLow = Arr(0, 0.0)
EuropaHigh = Arr(0, 0.0)
EuropaLow = Arr(0, 0.0)
AmericaHigh = Arr(0, 0.0)
AmericaLow = Arr(0, 0.0)
AsiaOpen = 0
AsiaClose = 9
AsiaOpenSummertime = 1  # The Asian session shifts
AsiaCloseSummertime = 10  # after the time changes
EuropaOpen = 6
EuropaClose = 15
AmericaOpen = 13
AmericaClose = 22
ShiftTime = 0  # Displacement of the buffer for construction of the future sessions
HighForFutureSession = 0.0  # High for the future session
LowForFutureSession = 0.0  # Low for the future session

def OnInit():
    global ShiftTime
    if PeriodSeconds(Period()) >= PeriodSeconds(PERIOD_H2):
        return -1
    ShiftTime = _idiv(PeriodSeconds(PERIOD_D1), PeriodSeconds(Period()))
    SetIndexBuffer(0, AsiaHigh, INDICATOR_DATA)
    SetIndexBuffer(1, AsiaLow, INDICATOR_DATA)
    SetIndexBuffer(2, EuropaHigh, INDICATOR_DATA)
    SetIndexBuffer(3, EuropaLow, INDICATOR_DATA)
    SetIndexBuffer(4, AmericaHigh, INDICATOR_DATA)
    SetIndexBuffer(5, AmericaLow, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_SHIFT, ShiftTime)
    PlotIndexSetInteger(1, PLOT_SHIFT, ShiftTime)
    PlotIndexSetInteger(2, PLOT_SHIFT, ShiftTime)
    PlotIndexSetInteger(3, PLOT_SHIFT, ShiftTime)
    PlotIndexSetInteger(4, PLOT_SHIFT, ShiftTime)
    PlotIndexSetInteger(5, PLOT_SHIFT, ShiftTime)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global HighForFutureSession, LowForFutureSession
    i = 1
    HighForFutureSession = MathMax(high[rates_total - 1], high[rates_total - 2])
    LowForFutureSession = MathMin(low[rates_total - 1], low[rates_total - 2])
    time1 = MqlDateTime()
    time2 = MqlDateTime()
    if prev_calculated == 0:
        i = ShiftTime + 1
        ArrayInitialize(AsiaHigh, 0.0)
        ArrayInitialize(AsiaLow, 0.0)
        ArrayInitialize(EuropaHigh, 0.0)
        ArrayInitialize(EuropaLow, 0.0)
        ArrayInitialize(AmericaHigh, 0.0)
        ArrayInitialize(AmericaLow, 0.0)
    else:
        i = prev_calculated - ShiftTime
    while i < rates_total:
        TimeToStruct(time[i - 1], time1)
        TimeToStruct(time[i], time2)
        if time1.day != time2.day:
            DrawTimeZone(time[i], i)
        i += 1
    return rates_total

def Summertime(time):
    if TimeDaylightSavings() != 0:
        return True
    else:
        return False

def DrawTimeZone(Start, Index):
    rates_total = 0
    shift = 0
    shift_end = 0
    _startIndex = Index - ShiftTime
    iHigh_ = Arr(0, 0.0)
    iLow_ = Arr(0, 0.0)
    HighSession = 0.0
    LowSession = 0.0
    AsiaStart = 0
    AsiaEnd = 0
    EuropaStart = 0
    EuropaEnd = 0
    AmericaStart = 0
    AmericaEnd = 0
    _start = Start + (TimeTradeServer() - TimeGMT())
    AsiaStart = _start + ((AsiaOpenSummertime if Summertime(Start) else AsiaOpen) * PeriodSeconds(PERIOD_H1))
    AsiaEnd = _start + ((AsiaCloseSummertime if Summertime(Start) else AsiaClose) * PeriodSeconds(PERIOD_H1)) - 1
    rates_total = CopyHigh(None, Period(), _DT(AsiaStart), _DT(AsiaEnd), iHigh_)
    if rates_total <= 0:
        HighSession = HighForFutureSession
    else:
        HighSession = iHigh_[ArrayMaximum(iHigh_, 0, rates_total)]
    rates_total = CopyLow(None, Period(), _DT(AsiaStart), _DT(AsiaEnd), iLow_)
    if rates_total <= 0:
        LowSession = LowForFutureSession
    else:
        LowSession = iLow_[ArrayMinimum(iLow_, 0, rates_total)]
    shift = _int(_idiv(AsiaStart - Start, PeriodSeconds(Period())))
    shift_end = _int(_idiv(AsiaEnd - Start, PeriodSeconds(Period())) + 1)
    for i in range(shift, shift_end):
        AsiaHigh[_startIndex + i] = HighSession
        AsiaLow[_startIndex + i] = LowSession
    EuropaStart = _start + (EuropaOpen * PeriodSeconds(PERIOD_H1))
    EuropaEnd = _start + (EuropaClose * PeriodSeconds(PERIOD_H1)) - 1
    rates_total = CopyHigh(None, Period(), _DT(EuropaStart), _DT(EuropaEnd), iHigh_)
    if rates_total <= 0:
        HighSession = HighForFutureSession
    else:
        HighSession = iHigh_[ArrayMaximum(iHigh_, 0, rates_total)]
    rates_total = CopyLow(None, Period(), _DT(EuropaStart), _DT(EuropaEnd), iLow_)
    if rates_total <= 0:
        LowSession = LowForFutureSession
    else:
        LowSession = iLow_[ArrayMinimum(iLow_, 0, rates_total)]
    shift = _int(_idiv(EuropaStart - Start, PeriodSeconds(Period())))
    shift_end = _int(_idiv(EuropaEnd - Start, PeriodSeconds(Period())) + 1)
    for i in range(shift, shift_end):
        EuropaHigh[_startIndex + i] = HighSession
        EuropaLow[_startIndex + i] = LowSession
    AmericaStart = _start + (AmericaOpen * PeriodSeconds(PERIOD_H1))
    AmericaEnd = _start + (AmericaClose * PeriodSeconds(PERIOD_H1)) - 1
    rates_total = CopyHigh(None, Period(), _DT(AmericaStart), _DT(AmericaEnd), iHigh_)
    if rates_total <= 0:
        HighSession = HighForFutureSession
    else:
        HighSession = iHigh_[ArrayMaximum(iHigh_, 0, rates_total)]
    rates_total = CopyLow(None, Period(), _DT(AmericaStart), _DT(AmericaEnd), iLow_)
    if rates_total <= 0:
        LowSession = LowForFutureSession
    else:
        LowSession = iLow_[ArrayMinimum(iLow_, 0, rates_total)]
    shift = _int(_idiv(AmericaStart - Start, PeriodSeconds(Period())))
    shift_end = _int(_idiv(AmericaEnd - Start, PeriodSeconds(Period())) + 1)
    for i in range(shift, shift_end):
        AmericaHigh[_startIndex + i] = HighSession
        AmericaLow[_startIndex + i] = LowSession
    ArrayResize(iHigh_, 0)
    ArrayResize(iLow_, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TradingSessionsOpenClose(_MQL5Indicator):
    name = 'trading_sessions_open_close'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
    }

