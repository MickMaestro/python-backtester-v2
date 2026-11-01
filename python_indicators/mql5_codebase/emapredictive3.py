"""emapredictive3 — converted from MQL5: MQL5 Indicators/EMAPredictive3/emapredictive3.mq5

Copyright: Copyright © 2007, Matthew (Dr Chaos) Kennel; Link: ftp://lyapunov.ucsd.edu/pub/nonlinear; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Matthew (Dr Chaos) Kennel', 'link': 'ftp://lyapunov.ucsd.edu/pub/nonlinear', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [2237106]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'EMAPredictive3'}, 'levels': [], 'description': [], 'name': 'emapredictive3', 'source': 'MQL5 Indicators/EMAPredictive3/emapredictive3.mq5', 'folder': 'EMAPredictive3', 'inputs': [{'mql': 'ShortPeriod', 'py': 'ShortPeriod', 'param': 'ShortPeriod', 'type': 'double', 'default': 8.0, 'label': '', 'sinput': False}, {'mql': 'LongPeriod', 'py': 'LongPeriod', 'param': 'LongPeriod', 'type': 'double', 'default': 25.0, 'label': '', 'sinput': False}, {'mql': 'ExtraTimeForward', 'py': 'ExtraTimeForward', 'param': 'ExtraTimeForward', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ShortPeriod = _input('ShortPeriod', 8.0)
LongPeriod = _input('LongPeriod', 25.0)
ExtraTimeForward = _input('ExtraTimeForward', 1.0)
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
min_rates_total = 0
p1 = 0.0
p3 = 0.0
t = 0.0
t1 = 0.0
t3 = 0.0

def OnInit():
    global min_rates_total, p1, p3, t, t1, t3
    min_rates_total = _int(MathMax(LongPeriod, ShortPeriod))
    p1 = _fdiv(2.0, LongPeriod + 1.0)
    p3 = _fdiv(2.0, ShortPeriod + 1.0)
    t1 = (LongPeriod - 1.0) / 2.0
    t3 = (ShortPeriod - 1.0) / 2.0
    t = ShortPeriod + ExtraTimeForward
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(IndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EMAPredictive3')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, begin, price):
    global _s_OnCalculate_ma1_, _s_OnCalculate_ma3_
    if rates_total < (min_rates_total + begin):
        return 0
    limit = 0
    bar = 0
    ma1 = 0.0
    ma3 = 0.0
    val = 0.0
    slope1 = 0.0
    predict = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1 - begin
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + begin)
        start = limit + 1
        _s_OnCalculate_ma1_ = price[start]
        _s_OnCalculate_ma3_ = price[start]
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(price, True)
    ma1 = _s_OnCalculate_ma1_
    ma3 = _s_OnCalculate_ma3_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        val = price[bar]
        ma1 = (p1 * val) + ((1.0 - p1) * ma1)
        ma3 = (p3 * val) + ((1.0 - p3) * ma3)
        slope1 = _fdiv(ma3 - ma1, t1 - t3)
        predict = ma3 + (slope1 * t)
        IndBuffer[bar] = predict
        if bar:
            _s_OnCalculate_ma1_ = ma1
            _s_OnCalculate_ma3_ = ma3
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_ma1_ = 0.0
_s_OnCalculate_ma3_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Emapredictive3(_MQL5Indicator):
    name = 'emapredictive3'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'ShortPeriod': 8.0,
        'LongPeriod': 25.0,
        'ExtraTimeForward': 1.0,
        'Shift': 0,  # horizontal shift of the indicator in bars
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

