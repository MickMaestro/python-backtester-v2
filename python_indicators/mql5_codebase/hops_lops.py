"""Hops-lops — converted from MQL5: MQL5 Indicators/HOPS and LOPS/Hops-lops.mq5

Highs of previous session
Lows of previous session
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Highs of previous session', 'Lows of previous session'], 'name': 'Hops-lops', 'source': 'MQL5 Indicators/HOPS and LOPS/Hops-lops.mq5', 'folder': 'HOPS and LOPS', 'inputs': [{'mql': 'inpTimeFrame', 'py': 'inpTimeFrame', 'param': 'inpTimeFrame', 'type': 'int', 'default': 16408, 'label': 'Time frame for Highs and Lows', 'sinput': False}, {'mql': 'inpHOPS', 'py': 'inpHOPS', 'param': None, 'type': 'color', 'default': 255, 'label': 'Color for high of previous session(s)', 'sinput': False}, {'mql': 'inpLOPS', 'py': 'inpLOPS', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Color for low of previous session(s)', 'sinput': False}, {'mql': 'inpPivot', 'py': 'inpPivot', 'param': None, 'type': 'color', 'default': 11119017, 'label': 'Color for pivot', 'sinput': False}, {'mql': 'inpUniqueID', 'py': 'inpUniqueID', 'param': None, 'type': 'string', 'default': 'HopsLops1', 'label': 'Unique ID for objects', 'sinput': False}, {'mql': 'inpLabelsShift', 'py': 'inpLabelsShift', 'param': 'inpLabelsShift', 'type': 'int', 'default': 10, 'label': 'Labels shift', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpTimeFrame = _input('inpTimeFrame', PERIOD_D1)  # Time frame for Highs and Lows
inpHOPS = _input('inpHOPS', clrRed)  # Color for high of previous session(s)
inpLOPS = _input('inpLOPS', clrBlue)  # Color for low of previous session(s)
inpPivot = _input('inpPivot', clrDarkGray)  # Color for pivot
inpUniqueID = _input('inpUniqueID', 'HopsLops1')  # Unique ID for objects
inpLabelsShift = _input('inpLabelsShift', 10)  # Labels shift
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, inpUniqueID + ':')
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _rates = Arr(2, 0, dyn=False, factory=MqlRates)
    _ratesCopied = CopyRates(Symbol(), inpTimeFrame, 1, 2, _rates)
    if _ratesCopied != 2:
        return prev_calculated
    P = (_rates[1].high + _rates[1].low + _rates[1].close) / 3
    R10 = _rates[1].low
    S10 = _rates[1].high
    R05 = _rates[0].low
    S05 = _rates[0].high
    _tf = timeFrameToString(inpTimeFrame)
    _time = time[rates_total - 1] + (PeriodSeconds(Period()) * inpLabelsShift)
    _createLine('pivot', P, _time, inpPivot, inpPivot, _tf + ' pivot line', STYLE_SOLID)
    _createLine('lops2', R05, _time, inpLOPS, inpLOPS, _tf + ' LOPS 2')
    _createLine('lops1', R10, _time, inpLOPS, inpLOPS, _tf + ' LOPS 1')
    _createLine('hops2', S05, _time, inpHOPS, inpHOPS, _tf + ' HOPS 2')
    _createLine('hops1', S10, _time, inpHOPS, inpHOPS, _tf + ' HOPS 1')
    ChartRedraw()
    return rates_total

def _createLine(_add, _price, _time, _color, _textColor, _text, _style=STYLE_DOT):
    _name = inpUniqueID + ':' + _add
    ObjectCreate(0, _name, OBJ_HLINE, 0, 0, 0)
    ObjectSetInteger(0, _name, OBJPROP_COLOR, _color)
    ObjectSetInteger(0, _name, OBJPROP_STYLE, _style)
    ObjectSetDouble(0, _name, OBJPROP_PRICE, 0, _price)
    _name = inpUniqueID + ':label:' + _add
    ObjectCreate(0, _name, OBJ_TEXT, 0, 0, 0)
    ObjectSetInteger(0, _name, OBJPROP_COLOR, _textColor)
    ObjectSetInteger(0, _name, OBJPROP_TIME, 0, _time)
    ObjectSetInteger(0, _name, OBJPROP_FONTSIZE, 8)
    ObjectSetDouble(0, _name, OBJPROP_PRICE, 0, _price)
    ObjectSetString(0, _name, OBJPROP_FONT, 'Arial')
    ObjectSetString(0, _name, OBJPROP_TEXT, _text)

def timeFrameToString(period):
    if period == PERIOD_CURRENT:
        period = Period()
    i = 0
    i = 0
    for i in range(i, ArraySize(_tfsPer)):
        if period == _tfsPer[i]:
            break
    else:
        i = _range_end(i, ArraySize(_tfsPer), 1)
    return _tfsStr[i]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HopsLops(_MQL5Indicator):
    name = 'Hops-lops'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Time frame for Highs and Lows
        'inpLabelsShift': 10,  # Labels shift
    }

