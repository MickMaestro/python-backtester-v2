"""GRFLeadingEdge — converted from MQL5: MQL5 Indicators/GRFLeadingEdger_Pivot_HTF/GRFLeadingEdge.mq5

Copyright: Copyright © 2007, GammaRatForex; Link: http://www.gammarat.com/Forex/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, GammaRatForex', 'link': 'http://www.gammarat.com/Forex/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'colors': {1: [3329330], 2: [16711680], 3: [255], 4: [255], 5: [16711680]}, 'widths': {1: 2, 2: 1, 3: 1, 4: 1, 5: 1}, 'styles': {1: 0, 2: 4, 3: 4, 4: 4, 5: 4}, 'labels': {}, 'levels': [], 'description': [], 'name': 'GRFLeadingEdge', 'source': 'MQL5 Indicators/GRFLeadingEdger_Pivot_HTF/GRFLeadingEdge.mq5', 'folder': 'GRFLeadingEdger_Pivot_HTF', 'inputs': [{'mql': 'Samples', 'py': 'Samples', 'param': 'Samples', 'type': 'uint', 'default': 60, 'label': '', 'sinput': False}, {'mql': 'LookAhead', 'py': 'LookAhead', 'param': 'LookAhead', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'StdLevel1', 'py': 'StdLevel1', 'param': 'StdLevel1', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'StdLevel2', 'py': 'StdLevel2', 'param': 'StdLevel2', 'type': 'double', 'default': 4.0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Samples = _input('Samples', 60)
LookAhead = _input('LookAhead', 0)
StdLevel1 = _input('StdLevel1', 2.0)
StdLevel2 = _input('StdLevel2', 4.0)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
LeadingEdgeBuffer = Arr(0, 0.0)
LeadingEdgeBufferPlus1 = Arr(0, 0.0)
LeadingEdgeBufferNeg1 = Arr(0, 0.0)
LeadingEdgeBufferPlus2 = Arr(0, 0.0)
LeadingEdgeBufferNeg2 = Arr(0, 0.0)
pStdLevel1 = 0.0
pStdLevel2 = 0.0
dPriceShift = 0.0
min_rates_total = 0

def OnInit():
    global dPriceShift, min_rates_total, pStdLevel1, pStdLevel2
    min_rates_total = _int(Samples)
    pStdLevel1 = StdLevel1 * Point()
    pStdLevel2 = StdLevel2 * Point()
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, LeadingEdgeBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, 'LeadingEdge Trend')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, LeadingEdgeBufferPlus2, INDICATOR_DATA)
    SetIndexBuffer(2, LeadingEdgeBufferPlus1, INDICATOR_DATA)
    SetIndexBuffer(3, LeadingEdgeBufferNeg1, INDICATOR_DATA)
    SetIndexBuffer(4, LeadingEdgeBufferNeg2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(1, PLOT_LABEL, 'LeadingEdge +' + DoubleToString(StdLevel2, 1))
    PlotIndexSetString(2, PLOT_LABEL, 'LeadingEdge +' + DoubleToString(StdLevel1, 1))
    PlotIndexSetString(3, PLOT_LABEL, 'LeadingEdge -' + DoubleToString(StdLevel1, 1))
    PlotIndexSetString(4, PLOT_LABEL, 'LeadingEdge -' + DoubleToString(StdLevel2, 1))
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'LeadingEdge Trend')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_base_det
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
        Leading = ((beta - (alpha * LookAhead)) * Point()) + dPriceShift
        LeadingEdgeBuffer[bar] = Leading
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
            LeadingEdgeBufferPlus1[bar] = Leading + (pStdLevel1 * c0)
            LeadingEdgeBufferNeg1[bar] = Leading - (pStdLevel1 * c1)
        if MathAbs(StdLevel2) > 0:
            LeadingEdgeBufferPlus2[bar] = Leading + (pStdLevel2 * c0)
            LeadingEdgeBufferNeg2[bar] = Leading - (pStdLevel2 * c1)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def get_avg(index, High, Low, Close):
    return _fdiv(MathPow(High[index] * Low[index] * Close[index] * Close[index], 1 / 4.0), Point())

def det2(a):
    return (a[0][0] * a[1][1]) - (a[1][0] * a[0][1])

# ---- static local variables
_s_OnCalculate_base_det = 0.0
_s_OnCalculate_a = Arr(2, 0.0, dyn=False, dims=(2,))
_s_OnCalculate_b = Arr(2, 0.0, dyn=False, dims=(2,))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GRFLeadingEdge(_MQL5Indicator):
    name = 'GRFLeadingEdge'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Samples': 60,
        'LookAhead': 0,
        'StdLevel1': 2.0,
        'StdLevel2': 4.0,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # cдвиг индикатора по вертикали в пунктах
    }

