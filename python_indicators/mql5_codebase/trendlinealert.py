"""trendlinealert — converted from MQL5: MQL5 Indicators/TrendLine Touch Alert/trendlinealert.mq5

Copyright: Coders' Guru; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': "Coders' Guru", 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'trendlinealert', 'source': 'MQL5 Indicators/TrendLine Touch Alert/trendlinealert.mq5', 'folder': 'TrendLine Touch Alert', 'inputs': [{'mql': 'TrendLineName', 'py': 'TrendLineName', 'param': None, 'type': 'string', 'default': 'WL1', 'label': 'Enter Trend Line Name', 'sinput': False}, {'mql': 'TouchDirection', 'py': 'TouchDirection', 'param': 'TouchDirection', 'type': 'int', 'default': 0, 'label': 'Enter the Touch Direction', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Direction
up = 0
dn = 1
both = 2
_enum('Direction', {0: 'up', 1: 'dn', 2: 'both'})

# ---- inputs and global variables
TrendLineName = _input('TrendLineName', 'WL1')  # Enter Trend Line Name
TouchDirection = _input('TouchDirection', 0)  # Enter the Touch Direction

def OnInit():
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if TrendLineName != '':
        TrendValue = GetTrend(TrendLineName)
        Comment('Trend Line(' + TrendLineName + ') value = ' + DoubleToString(TrendValue, Digits()))
        if TrendValue > 0:
            ArraySetAsSeries(close, True)
            ArraySetAsSeries(low, True)
            ArraySetAsSeries(high, True)
            if ((TouchDirection == 0 or TouchDirection == 2) and close[0] >= TrendValue) and low[0] < TrendValue:
                AlertOnce('Price touched UP the trendline!', 0)
                SendMailOnce('UP', 'Price touched UP the trendline!', 0)
            if ((TouchDirection == 0 or TouchDirection == 2) and close[0] <= TrendValue) and high[0] > TrendValue:
                AlertOnce('Price touched DOWN the trendline!', 1)
                SendMailOnce('DOWN', 'Price touched DOWN the trendline!', 1)
    return rates_total

def GetTrend(trend_name):
    cnt = 0
    while cnt < ObjectsTotal(0):
        objName = ObjectName(0, cnt)
        if StringFind(objName, trend_name) > -1:
            return ObjectGetValueByTime(0, objName, TimeCurrent())
        cnt += 1
    return 0.0

def AlertOnce(msg, ref):
    if _s_AlertOnce_LastAlert[ref] == 0 or _s_AlertOnce_LastAlert[ref] < Bars(Symbol(), Period()):
        Alert(msg)
        _s_AlertOnce_LastAlert[ref] = Bars(Symbol(), Period())
        return True
    return False

def SendMailOnce(subject, body, ref):
    if _s_SendMailOnce_LastAlert[ref] == 0 or _s_SendMailOnce_LastAlert[ref] < Bars(Symbol(), Period()):
        SendMail(subject, body)
        _s_SendMailOnce_LastAlert[ref] = Bars(Symbol(), Period())
        return True
    return False

# ---- static local variables
_s_AlertOnce_LastAlert = Arr(3, 0, dyn=False)
_s_SendMailOnce_LastAlert = Arr(3, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Trendlinealert(_MQL5Indicator):
    name = 'trendlinealert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TouchDirection': _Choice({0: 'Up Direction', 1: 'Down Direction', 2: 'Both Directiond'}, default=0),  # Enter the Touch Direction
    }

