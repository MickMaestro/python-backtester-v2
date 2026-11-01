"""correlation — converted from MQL5: MQL5 Indicators/Pearson correlation indicator/correlation.mq5

Copyright: Copyright 2012, iC; Link: http://www.icreator.biz/; Version: 1.2

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, iC', 'link': 'http://www.icreator.biz/', 'version': '1.2', 'window': 'separate', 'indicator_minimum': -1.0, 'indicator_maximum': 1.0, 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 8, 2: 10}, 'colors': {}, 'widths': {1: 2, 2: 1}, 'styles': {2: 2}, 'labels': {}, 'levels': [], 'description': [], 'name': 'correlation', 'source': 'MQL5 Indicators/Pearson correlation indicator/correlation.mq5', 'folder': 'Pearson correlation indicator', 'inputs': [{'mql': '_SecondSymbol', 'py': '_SecondSymbol', 'param': None, 'type': 'string', 'default': 'EURUSD', 'label': 'Second symbol', 'sinput': False}, {'mql': '_SettPeriod', 'py': '_SettPeriod', 'param': '_SettPeriod', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': '_AppliedPrice', 'py': '_AppliedPrice', 'param': '_AppliedPrice', 'type': 'int', 'default': 7, 'label': 'Price', 'sinput': False}, {'mql': '_Color1', 'py': '_Color1', 'param': None, 'type': 'color', 'default': 0, 'label': 'Min correlation', 'sinput': False}, {'mql': '_Color2', 'py': '_Color2', 'param': None, 'type': 'color', 'default': 2237106, 'label': 'Max correlation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
_SecondSymbol = _input('_SecondSymbol', 'EURUSD')  # Second symbol
_SettPeriod = _input('_SettPeriod', 20)  # Period
_AppliedPrice = _input('_AppliedPrice', PRICE_WEIGHTED)  # Price
_Color1 = _input('_Color1', clrBlack)  # Min correlation
_Color2 = _input('_Color2', clrFireBrick)  # Max correlation
buf = Arr(0, 0.0)
buf2 = Arr(0, 0.0)
arr1 = Arr(0, 0.0)
arr2 = Arr(0, 0.0)
colors1 = Arr(0, 0.0)
colors2 = Arr(0, 0.0)
a3 = Arr(0, 0.0)
h1 = 0
h2 = 0

class CRGB(MqlObject):
    _q_fields = ('r', 'g', 'b')
    def __init__(self, *args):
        self.r = 0
        self.g = 0
        self.b = 0

def OnInit():
    global h1, h2
    SetIndexBuffer(0, buf)
    SetIndexBuffer(1, colors1, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, buf2)
    SetIndexBuffer(3, colors2, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, arr1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, arr2, INDICATOR_CALCULATIONS)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, 3)
    IndicatorSetString(INDICATOR_SHORTNAME, Symbol() + '/' + _SecondSymbol + ', ' + IntegerToString(_SettPeriod) + ', ' + EnumToString(_AppliedPrice, 'ENUM_APPLIED_PRICE') + ',')
    setPlotColor(0, _Color1, _Color2)
    setPlotColor(1, _Color1, _Color2)
    h1 = iMA(Symbol(), 0, 1, 0, MODE_SMA, _AppliedPrice)
    h2 = iMA(_SecondSymbol, 0, 1, 0, MODE_SMA, _AppliedPrice)
    ArrayResize(a3, _SettPeriod * 2)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    j = 0
    c = 0
    limit = 0
    bars1 = 0
    bars2 = 0
    averX1 = 0.0
    averX2 = 0.0
    v1 = 0.0
    v2 = 0.0
    v3 = 0.0
    a1 = Arr(1, 0.0, dyn=False)
    a2 = Arr(1, 0.0, dyn=False)
    tm = Arr(1, 0, dyn=False)
    cont = False
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = _SettPeriod - 1
        ArrayInitialize(buf, 0)
        ArrayInitialize(buf2, 0)
        if not SymbolSelect(_SecondSymbol, True):
            printf('Wrong symbol! [ %s ]', _SecondSymbol)
            return 0
        bars1 = Bars(Symbol(), 0)
        bars2 = Bars(_SecondSymbol, 0)
        if bars1 == 0 or bars2 == 0:
            Print('The data is not formed yet! Wait...')
            return 0
        elif bars1 < _SettPeriod or bars2 < _SettPeriod:
            Print('Bars is not enough to calculate!')
            return 0
        if BarsCalculated(h1) < bars1:
            printf('Not all data of MA is calculated. Error %i. [ %s ]', GetLastError(), Symbol())
            return 0
        if BarsCalculated(h2) < bars2:
            printf('Not all data of MA is calculated. Error %i. [ %s ]', GetLastError(), _SecondSymbol)
            return 0
        if CopyTime(_SecondSymbol, 0, bars2 - 1, 1, tm) <= 0:
            Print('Error copying time.')
            return 0
        i = 0
        for i in range(i, bars1):
            if time[i] >= tm[0]:
                limit = i + _SettPeriod - 1
                break
        else:
            i = _range_end(i, bars1, 1)
    else:
        limit = prev_calculated - 1
    i = limit
    while i < rates_total:
        averX1 = 0.0
        averX2 = 0.0
        j = 0
        for j in range(j, _SettPeriod):
            if CopyBuffer(h1, 0, _DT(time[i - j]), 1, a1) <= 0 or CopyBuffer(h2, 0, _DT(time[i - j]), 1, a2) <= 0:
                i += _SettPeriod - j - 1
                cont = True
                break
            a3[j] = a1[0]
            a3[_SettPeriod + j] = a2[0]
            averX1 += a1[0] / _SettPeriod
            averX2 += a2[0] / _SettPeriod
        else:
            j = _range_end(j, _SettPeriod, 1)
        if cont:
            cont = False
            i += 1
            continue
        v1 = 0.0
        v2 = 0.0
        v3 = 0.0
        j = 0
        for j in range(j, _SettPeriod):
            v1 += (a3[j] - averX1) * (a3[_SettPeriod + j] - averX2)
            v2 += pow(a3[j] - averX1, 2)
            v3 += pow(a3[_SettPeriod + j] - averX2, 2)
        else:
            j = _range_end(j, _SettPeriod, 1)
        if (v1 == 0 or v2 == 0) or v3 == 0:
            return 0
        buf[i] = _fdiv(v1, sqrt(v2 * v3))
        buf2[i] = buf[i]
        c = getPlotColor(buf[i])
        colors1[i] = c
        colors2[i] = c
        i += 1
    return rates_total

def setPlotColor(plot, col1, col2):
    i = 0
    c1 = CRGB()
    c2 = CRGB()
    dr = 0.0
    dg = 0.0
    db = 0.0
    s = ""
    PlotIndexSetInteger(plot, PLOT_COLOR_INDEXES, 64)
    ColorToRGB(col1, c1)
    ColorToRGB(col2, c2)
    dr = float(c2.r - c1.r) / 64
    dg = float(c2.g - c1.g) / 64
    db = float(c2.b - c1.b) / 64
    i = 0
    for i in range(i, 64):
        s = StringFormat('%i,%i,%i', c1.r + _int(NormalizeDouble(dr * (i + 1), 0)), c1.g + _int(NormalizeDouble(dg * (i + 1), 0)), c1.b + _int(NormalizeDouble(db * (i + 1), 0)))
        PlotIndexSetInteger(plot, PLOT_LINE_COLOR, i, StringToColor(s))
    else:
        i = _range_end(i, 64, 1)

def getPlotColor(current):
    return _int(NormalizeDouble((64 - 1) * fabs(current), 0))

def ColorToRGB(col, res):
    s = ""
    s2 = ""
    n = 0
    s = ColorToString(col)
    n = StringFind(s, ',')
    s2 = StringSubstr(s, 0, n)
    res.r = _int(StringToInteger(s2))
    s = StringSubstr(s, n + 1)
    n = StringFind(s, ',')
    s2 = StringSubstr(s, 0, n)
    res.g = _int(StringToInteger(s2))
    s = StringSubstr(s, n + 1)
    s2 = StringSubstr(s, 0)
    res.b = _int(StringToInteger(s2))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Correlation(_MQL5Indicator):
    name = 'correlation'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        '_SettPeriod': 20,  # Period
        '_AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=7),  # Price
    }
    y_range = (-1.0, 1.0)

