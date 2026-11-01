"""grfleadingedgemov — converted from MQL5: MQL5 Indicators/GRFLeadingEdgeMov_HTF/grfleadingedgemov.mq5

Copyright: Copyright © 2007, GammaRatForex; Link: http://www.gammarat.com/Forex/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, GammaRatForex', 'link': 'http://www.gammarat.com/Forex/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [9639167]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': [], 'name': 'grfleadingedgemov', 'source': 'MQL5 Indicators/GRFLeadingEdgeMov_HTF/grfleadingedgemov.mq5', 'folder': 'GRFLeadingEdgeMov_HTF', 'inputs': [{'mql': 'Samples', 'py': 'Samples', 'param': 'Samples', 'type': 'uint', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'LookAhead', 'py': 'LookAhead', 'param': 'LookAhead', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Samples = _input('Samples', 12)
LookAhead = _input('LookAhead', 0)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
LeadingEdgeBuffer = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0

def OnInit():
    global dPriceShift, min_rates_total
    min_rates_total = _int(Samples)
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, LeadingEdgeBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, 'LeadingEdge Trend')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
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
    b = Arr(2, 0.0, dyn=False, dims=(2,))
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
        ArrayCopy(b, _s_OnCalculate_a)
        b[0][0] = c0
        b[1][0] = c1
        alpha = _fdiv(det2(b), _s_OnCalculate_base_det)
        ArrayCopy(b, _s_OnCalculate_a)
        b[0][1] = c0
        b[1][1] = c1
        beta = _fdiv(det2(b), _s_OnCalculate_base_det)
        LeadingEdgeBuffer[bar] = ((beta - (alpha * LookAhead)) * Point()) + dPriceShift
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Grfleadingedgemov(_MQL5Indicator):
    name = 'grfleadingedgemov'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Samples': 12,
        'LookAhead': 0,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
    }

