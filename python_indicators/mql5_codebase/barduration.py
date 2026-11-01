"""BarDuration — converted from MQL5: MQL5 Indicators/BarDuration/BarDuration.mq5

Display histogram of custom bars' durations in minutes. Applicable for renko boxes, PnF, equivolume bars, etc.
Copyright: Copyright (c) 2025, Marketeer; Link: https://www.mql5.com/en/users/marketeer

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright (c) 2025, Marketeer', 'link': 'https://www.mql5.com/en/users/marketeer', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 3}, 'colors': {1: [14772545]}, 'widths': {1: 3}, 'styles': {}, 'labels': {1: 'Duration (min)'}, 'levels': [], 'description': ["Display histogram of custom bars' durations in minutes. Applicable for renko boxes, PnF, equivolume bars, etc."], 'name': 'BarDuration', 'source': 'MQL5 Indicators/BarDuration/BarDuration.mq5', 'folder': 'BarDuration', 'inputs': [{'mql': 'Directional', 'py': 'Directional', 'param': 'Directional', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Directional = _input('Directional', False)
Buffer1 = Arr(0, 0.0)

class Session(MqlObject):
    _q_fields = ('from_', 'to')
    def __init__(self):
        self.from_ = 0
        self.to = 0
        ZeroMemory(self)

def OnInit():
    SetIndexBuffer(0, Buffer1, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = rates_total
    if prev_calculated <= 0:
        ArrayInitialize(Buffer1, EMPTY_VALUE)
        ArraySetAsSeries(Buffer1, True)
    else:
        limit = rates_total - prev_calculated + 1
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    for i in range(0, limit):
        stop = GetTradeScheduleBreak(Symbol(), time[i])
        if i:
            Buffer1[i] = ((((close[i] > open[i] or (not Directional)) * 2) - 1) * float(fmin(time[i - 1], stop) - time[i])) / 60
        else:
            Buffer1[i] = ((((close[i] > open[i] or (not Directional)) * 2) - 1) * float(fmin(TimeCurrent(), stop) - time[0])) / 60
    return rates_total

def DayOfWeek(_t):
    return _imod(_idiv(_t, 86400) + 4, 7)

def GetTradeScheduleBreak(symbol, now):
    global _s_GetTradeScheduleBreak_sessions
    time = _imod(_ulong(now), _s_GetTradeScheduleBreak_day)
    date = _long(_idiv(now, _s_GetTradeScheduleBreak_day) * _s_GetTradeScheduleBreak_day)
    from_ = 0
    to = 0
    i = 0
    d = DayOfWeek(now)
    if not ArrayRange(_s_GetTradeScheduleBreak_schedule, 0):
        for j in range(0, 7):
            i = 0
            while SymbolInfoSessionQuote(symbol, j, ((i := i + 1) - 1), from_, to):
                if i > ArrayRange(_s_GetTradeScheduleBreak_schedule, 0):
                    ArrayResize(_s_GetTradeScheduleBreak_schedule, i)
                _s_GetTradeScheduleBreak_schedule[i - 1][j].from_ = from_
                _s_GetTradeScheduleBreak_schedule[i - 1][j].to = to
        _s_GetTradeScheduleBreak_sessions = ArrayRange(_s_GetTradeScheduleBreak_schedule, 0)
    i = 0
    while i < _s_GetTradeScheduleBreak_sessions:
        if time >= _ulong(_s_GetTradeScheduleBreak_schedule[i][d].from_) and time < _ulong(_s_GetTradeScheduleBreak_schedule[i][d].to):
            return date + _s_GetTradeScheduleBreak_schedule[i][d].to
        i += 1
    return 32535215940

# ---- static local variables
_s_GetTradeScheduleBreak_day = 60 * 60 * 24
_s_GetTradeScheduleBreak_schedule = Arr(0, 0, factory=Session, dims=(7,))
_s_GetTradeScheduleBreak_sessions = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BarDuration(_MQL5Indicator):
    name = 'BarDuration'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Directional': False,
    }

