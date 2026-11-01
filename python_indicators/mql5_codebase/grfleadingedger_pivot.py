"""GRFLeadingEdger_Pivot — converted from MQL5: MQL5 Indicators/GRFLeadingEdger_Pivot/GRFLeadingEdger_Pivot.mq5

Copyright: Copyright © 2007, GammaRatForex; Link: http://www.gammarat.com/Forex/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, GammaRatForex', 'link': 'http://www.gammarat.com/Forex/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'GRFLeadingEdger_Pivot', 'source': 'MQL5 Indicators/GRFLeadingEdger_Pivot/GRFLeadingEdger_Pivot.mq5', 'folder': 'GRFLeadingEdger_Pivot', 'inputs': [{'mql': 'Symbols_Sirname', 'py': 'Symbols_Sirname', 'param': None, 'type': 'string', 'default': 'GRFLeadingEdger_Pivot_', 'label': 'Название для меток индикатора', 'sinput': False}, {'mql': 'Samples', 'py': 'Samples', 'param': 'Samples', 'type': 'uint', 'default': 60, 'label': '', 'sinput': False}, {'mql': 'LookAhead', 'py': 'LookAhead', 'param': 'LookAhead', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'StdLevel1', 'py': 'StdLevel1', 'param': 'StdLevel1', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'StdLevel2', 'py': 'StdLevel2', 'param': 'StdLevel2', 'type': 'double', 'default': 4.0, 'label': '', 'sinput': False}, {'mql': 'Up_Color', 'py': 'Up_Color', 'param': None, 'type': 'color', 'default': 8388352, 'label': 'Цвет верхней полосы индикатора', 'sinput': False}, {'mql': 'Dn_Color', 'py': 'Dn_Color', 'param': None, 'type': 'color', 'default': 65535, 'label': 'Цвет нижней полосы индикатора', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 0, 'label': 'номер бара для получения значений индикатора', 'sinput': False}, {'mql': 'SignalLen', 'py': 'SignalLen', 'param': 'SignalLen', 'type': 'uint', 'default': 40, 'label': 'Длина полос индикатора', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Symbols_Sirname = _input('Symbols_Sirname', 'GRFLeadingEdger_Pivot_')  # Название для меток индикатора
Samples = _input('Samples', 60)
LookAhead = _input('LookAhead', 0)
StdLevel1 = _input('StdLevel1', 2.0)
StdLevel2 = _input('StdLevel2', 4.0)
Up_Color = _input('Up_Color', clrSpringGreen)  # Цвет верхней полосы индикатора
Dn_Color = _input('Dn_Color', clrYellow)  # Цвет нижней полосы индикатора
SignalBar = _input('SignalBar', 0)  # номер бара для получения значений индикатора
SignalLen = _input('SignalLen', 40)  # Длина полос индикатора
pStdLevel1 = 0.0
pStdLevel2 = 0.0
min_rates_total = 0
UpName = ""
DnName = ""
PerSignalLen = 0

def CreateRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_RECTANGLE, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(chart_id, name, OBJPROP_ZORDER, True)
    ObjectSetInteger(chart_id, name, OBJPROP_FILL, True)

def SetRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)

def OnDeinit(reason):
    ObjectsDeleteAll(0, Symbols_Sirname, -1, -1)
    ChartRedraw(0)

def OnInit():
    global DnName, PerSignalLen, UpName, min_rates_total, pStdLevel1, pStdLevel2
    min_rates_total = _int(Samples)
    pStdLevel1 = StdLevel1 * Point()
    pStdLevel2 = StdLevel2 * Point()
    UpName = Symbols_Sirname + 'Upper Band'
    DnName = Symbols_Sirname + 'Lower Band'
    PerSignalLen = _int(SignalLen) * PeriodSeconds()
    IndicatorSetString(INDICATOR_SHORTNAME, 'GRFLeadingEdger_Pivot')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Dn1, _s_OnCalculate_Dn2, _s_OnCalculate_Up1, _s_OnCalculate_Up2, _s_OnCalculate_base_det
    if rates_total < min_rates_total:
        return 0
    c0 = 0.0
    c1 = 0.0
    alpha = 0.0
    beta = 0.0
    s0 = 0.0
    s1 = 0.0
    c01 = 0.0
    c11 = 0.0
    first = 0
    bar = 0
    kkk = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
        ArrayInitialize(_s_OnCalculate_a, 0)
        for iii in range(0, _int(Samples)):
            _s_OnCalculate_a[0][0] += iii * iii
            _s_OnCalculate_a[0][1] += iii
            _s_OnCalculate_a[1][0] += iii
            _s_OnCalculate_a[1][1] += 1
        _s_OnCalculate_base_det = det2(_s_OnCalculate_a)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        c0 = 0.0
        c1 = 0.0
        kkk = 0
        for kkk in range(kkk, _int(Samples)):
            res = get_avg(bar - kkk, high, low, close)
            c0 += kkk * res
            c1 += res
        else:
            kkk = _range_end(kkk, _int(Samples), 1)
        ArrayCopy(_s_OnCalculate_b, _s_OnCalculate_a)
        _s_OnCalculate_b[0][0] = c0
        _s_OnCalculate_b[1][0] = c1
        alpha = _fdiv(det2(_s_OnCalculate_b), _s_OnCalculate_base_det)
        ArrayCopy(_s_OnCalculate_b, _s_OnCalculate_a)
        _s_OnCalculate_b[0][1] = c0
        _s_OnCalculate_b[1][1] = c1
        beta = _fdiv(det2(_s_OnCalculate_b), _s_OnCalculate_base_det)
        Leading = (beta - (alpha * LookAhead)) * Point()
        c0 = 0.0
        c1 = 0.0
        c11 = 0.0
        c01 = 0.0
        kkk = 0
        for kkk in range(kkk, _int(Samples)):
            s0 = get_avg(bar - kkk, high, low, close)
            s1 = (kkk * alpha) + beta
            res = MathPow(s0 - s1, 2)
            if s0 < s1:
                c0 += res
                c01 += 1
            else:
                c1 += res
                c11 += 1
        else:
            kkk = _range_end(kkk, _int(Samples), 1)
        if not c01:
            c01 = 1.0
        if not c11:
            c11 = 1.0
        c01 = MathSqrt(_fdiv(1.0, _fdiv(0.5, MathPow(Samples, 2)) + _fdiv(_fdiv(0.5, c01), c01)))
        c11 = MathSqrt(_fdiv(1.0, _fdiv(0.5, MathPow(Samples, 2)) + _fdiv(_fdiv(0.5, c11), c11)))
        c0 = MathSqrt(_fdiv(c0, c01))
        c1 = MathSqrt(_fdiv(c1, c11))
        if MathAbs(StdLevel1) > 0:
            _s_OnCalculate_Up1 = Leading + (pStdLevel1 * c0)
            _s_OnCalculate_Dn1 = Leading - (pStdLevel1 * c1)
        if MathAbs(StdLevel2) > 0:
            _s_OnCalculate_Up2 = Leading + (pStdLevel2 * c0)
            _s_OnCalculate_Dn2 = Leading - (pStdLevel2 * c1)
    else:
        bar = _range_end(bar, rates_total, 1)
    bar0 = rates_total - 1
    bar1 = rates_total - _int(MathMax(SignalLen - 1, 0))
    time0 = time[bar0] + (2 * PeriodSeconds())
    time1 = time0 - PerSignalLen
    SetRectangle(0, UpName, 0, time1, _s_OnCalculate_Up1, time0, _s_OnCalculate_Up2, Up_Color, STYLE_SOLID, 1, UpName)
    SetRectangle(0, DnName, 0, time1, _s_OnCalculate_Dn1, time0, _s_OnCalculate_Dn2, Dn_Color, STYLE_SOLID, 1, DnName)
    ChartRedraw(0)
    return rates_total

def get_avg(index, High, Low, Close):
    return _fdiv(MathPow(High[index] * Low[index] * Close[index] * Close[index], 1 / 4.0), Point())

def det2(a):
    return (a[0][0] * a[1][1]) - (a[1][0] * a[0][1])

# ---- static local variables
_s_OnCalculate_base_det = 0.0
_s_OnCalculate_a = Arr(2, 0.0, dyn=False, dims=(2,))
_s_OnCalculate_b = Arr(2, 0.0, dyn=False, dims=(2,))
_s_OnCalculate_Up1 = 0.0
_s_OnCalculate_Up2 = 0.0
_s_OnCalculate_Dn1 = 0.0
_s_OnCalculate_Dn2 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GRFLeadingEdgerPivot(_MQL5Indicator):
    name = 'GRFLeadingEdger_Pivot'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Samples': 60,
        'LookAhead': 0,
        'StdLevel1': 2.0,
        'StdLevel2': 4.0,
        'SignalBar': 0,  # номер бара для получения значений индикатора
        'SignalLen': 40,  # Длина полос индикатора
    }

