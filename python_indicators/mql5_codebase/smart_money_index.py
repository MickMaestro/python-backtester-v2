"""Smart_Money_Index — converted from MQL5: MQL5 Indicators/SMI/Smart_Money_Index.mq5

Smart money index
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [8721863]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'SMI'}, 'levels': [], 'description': ['Smart money index'], 'name': 'Smart_Money_Index', 'source': 'MQL5 Indicators/SMI/Smart_Money_Index.mq5', 'folder': 'SMI', 'inputs': [{'mql': 'InpOpenHour', 'py': 'InpOpenHour', 'param': 'InpOpenHour', 'type': 'uchar', 'default': 3, 'label': 'Open hour', 'sinput': False}, {'mql': 'InpSessionLength', 'py': 'InpSessionLength', 'param': 'InpSessionLength', 'type': 'uchar', 'default': 8, 'label': 'Session length', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpOpenHour = _input('InpOpenHour', 3)  # Open hour
InpSessionLength = _input('InpSessionLength', 8)  # Session length
BufferSMI = Arr(0, 0.0)
open_hour = 0
session_length = 0

def OnInit():
    global open_hour, session_length
    open_hour = (22 if (InpOpenHour > 22) else InpOpenHour)
    session_length = (24 if (InpSessionLength > 24) else 1 if (InpSessionLength < 1) else InpSessionLength)
    SetIndexBuffer(0, BufferSMI, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SMI')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferSMI, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferSMI, 0)
    for i in range(limit, 0 - 1, -1):
        if i == (rates_total - 2):
            BufferSMI[i + 1] = 0.0
        t = time[i]
        t = t - (open_hour * 3600)
        t = _long(floor(_idiv(t, 86400) + 0.5)) * 86400
        t = t + (open_hour * 3600)
        from_ = (t if (Period() < PERIOD_D1) else TimeOpenDay(time[i], open_hour))
        to = from_ + (session_length * 3600)
        x1 = BarShift("", PERIOD_CURRENT, from_)
        x2 = BarShift("", PERIOD_CURRENT, to)
        if ((x1 > (rates_total - 1) or x2 > (rates_total - 2)) or x1 == WRONG_VALUE) or x2 == WRONG_VALUE:
            continue
        if x1 == i or x2 == i:
            shift = (0 if (Period() < PERIOD_D1) else 1)
            BufferSMI[i] = BufferSMI[i + 1] - (close[x1 + shift] - open[x1 + shift]) + (close[x2] - open[x2])
        else:
            BufferSMI[i] = BufferSMI[i + 1]
    return rates_total

def TimeOpenDay(time, hour_begin):
    tm = MqlDateTime()
    if TimeToStruct(time, tm):
        tm.hour = hour_begin
        tm.min = 0
        return StructToTime(tm)
    return 0

def BarShift(symbol_name, timeframe, time, exact=False):
    res = Bars(symbol_name, timeframe, time + 1, UINT_MAX)
    if exact:
        if (timeframe != PERIOD_MN1 or time > TimeCurrent()) and res == Bars(symbol_name, timeframe, time - PeriodSeconds(timeframe) + 1, UINT_MAX):
            return -1
    return res


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SmartMoneyIndex(_MQL5Indicator):
    name = 'Smart_Money_Index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpOpenHour': 3,  # Open hour
        'InpSessionLength': 8,  # Session length
    }

