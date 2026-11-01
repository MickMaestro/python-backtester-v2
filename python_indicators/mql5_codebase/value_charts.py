"""value_charts — converted from MQL5: MQL5 Indicators/Value Charts/value_charts.mq5

Copyright: 2011, FxGeek.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '2011, FxGeek.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 1}, 'types': {1: 16}, 'colors': {1: [255, 32768, 16711680]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'Open;High;Low;Close'}, 'levels': [8.0, 6.0, -6.0, -8.0], 'description': [], 'name': 'value_charts', 'source': 'MQL5 Indicators/Value Charts/value_charts.mq5', 'folder': 'Value Charts', 'inputs': [{'mql': 'Periode', 'py': 'Periode', 'param': 'Periode', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'Show_Arrow', 'py': 'Show_Arrow', 'param': 'Show_Arrow', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Arrow_Width', 'py': 'Arrow_Width', 'param': 'Arrow_Width', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Arrow_Up', 'py': 'Arrow_Up', 'param': None, 'type': 'color', 'default': 32768, 'label': '', 'sinput': False}, {'mql': 'Arrow_Down', 'py': 'Arrow_Down', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
Periode = _input('Periode', 5)
Show_Arrow = _input('Show_Arrow', True)
Arrow_Width = _input('Arrow_Width', 0)
Arrow_Up = _input('Arrow_Up', clrGreen)
Arrow_Down = _input('Arrow_Down', clrRed)
ExtOBuffer = Arr(0, 0.0)
ExtHBuffer = Arr(0, 0.0)
ExtLBuffer = Arr(0, 0.0)
ExtCBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
RangeAverage = Arr(0, 0.0)
MiddleAverage = Arr(0, 0.0)
_AValue = 0.0
_BValue = 0.0

def OnInit():
    SetIndexBuffer(0, ExtOBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, RangeAverage, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, MiddleAverage, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Value Chart ' + IntegerToString(Periode))

def OnDeinit(reason):
    ClearMyObjects()
    Print('Deinit Value Chart, reason = ' + IntegerToString(reason))

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    global _AValue, _BValue
    i = 0
    limit = 0
    if rates_total < Periode:
        return 0
    if prev_calculated < Periode:
        limit = Periode
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        RangeAverage[i] = High[i] - Low[i]
        _AValue = 0.2 * SimpleMA(i, Periode, RangeAverage)
        MiddleAverage[i] = (High[i] + Low[i]) / 2.0
        _BValue = SimpleMA(i, Periode, MiddleAverage)
        ExtOBuffer[i] = _fdiv(Open[i] - _BValue, _AValue)
        ExtHBuffer[i] = _fdiv(High[i] - _BValue, _AValue)
        ExtLBuffer[i] = _fdiv(Low[i] - _BValue, _AValue)
        ExtCBuffer[i] = _fdiv(Close[i] - _BValue, _AValue)
        if ExtCBuffer[i] < ExtOBuffer[i]:
            ExtColorBuffer[i] = 0.0
        if ExtCBuffer[i] > ExtOBuffer[i]:
            ExtColorBuffer[i] = 1.0
        if ExtLBuffer[i] <= -8:
            ExtColorBuffer[i] = 2.0
            if Show_Arrow:
                Trace('Value Chart' + IntegerToString(i), 1, Low[i], Time[i], Arrow_Up)
        if ExtHBuffer[i] >= 8:
            ExtColorBuffer[i] = 2.0
            if Show_Arrow:
                Trace('Value Chart' + IntegerToString(i), -1, High[i], Time[i], Arrow_Down)
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total

def Trace(name, sens, price, time, couleur):
    ObjectCreate(0, name, OBJ_ARROW, 0, time, price)
    if sens == 1:
        ObjectSetInteger(0, name, OBJPROP_ARROWCODE, 233)
    if sens == -1:
        ObjectSetInteger(0, name, OBJPROP_ARROWCODE, 234)
    ObjectSetInteger(0, name, OBJPROP_COLOR, couleur)
    ObjectSetInteger(0, name, OBJPROP_WIDTH, Arrow_Width)

def ClearMyObjects():
    name = ""
    for i in range(ObjectsTotal(0, 0), 0 - 1, -1):
        name = ObjectName(0, i)
        if StringSubstr(name, 0, 5) == 'Value':
            ObjectDelete(0, name)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ValueCharts(_MQL5Indicator):
    name = 'value_charts'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Periode': 5,
        'Show_Arrow': True,
        'Arrow_Width': 0,
    }

