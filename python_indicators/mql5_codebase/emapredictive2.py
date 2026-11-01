"""emapredictive2 — converted from MQL5: MQL5 Indicators/EMAPredictive2_HTF/emapredictive2.mq5

Copyright: Matthew (Dr Chaos) Kennel; Link: ftp://lyapunov.ucsd.edu/pub/nonlinear; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Matthew (Dr Chaos) Kennel', 'link': 'ftp://lyapunov.ucsd.edu/pub/nonlinear', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711935]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'EMAPredictive2'}, 'levels': [], 'description': [], 'name': 'emapredictive2', 'source': 'MQL5 Indicators/EMAPredictive2_HTF/emapredictive2.mq5', 'folder': 'EMAPredictive2_HTF', 'inputs': [{'mql': 'LongPeriod', 'py': 'LongPeriod', 'param': 'LongPeriod', 'type': 'double', 'default': 25.0, 'label': '', 'sinput': False}, {'mql': 'ShortPeriod', 'py': 'ShortPeriod', 'param': 'ShortPeriod', 'type': 'double', 'default': 8.0, 'label': '', 'sinput': False}, {'mql': 'ExtraTimeForward', 'py': 'ExtraTimeForward', 'param': 'ExtraTimeForward', 'type': 'double', 'default': 1.0, 'label': 'How much to further extrapolate location', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LongPeriod = _input('LongPeriod', 25.0)
ShortPeriod = _input('ShortPeriod', 8.0)
ExtraTimeForward = _input('ExtraTimeForward', 1.0)  # How much to further extrapolate location
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
IndBuffer = Arr(0, 0.0)
dPriceShift = 0.0
p1 = 0.0
p3 = 0.0
t1 = 0.0
t3 = 0.0
t = 0.0
min_rates_total = 0

def OnInit():
    global dPriceShift, min_rates_total, p1, p3, t, t1, t3
    min_rates_total = 2
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EMAPredictive2')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    dPriceShift = Point() * PriceShift
    p1 = _fdiv(2.0, LongPeriod + 1.0)
    p3 = _fdiv(2.0, ShortPeriod + 1.0)
    t1 = (LongPeriod - 1.0) / 2.0
    t3 = (ShortPeriod - 1.0) / 2.0
    t = ShortPeriod + ExtraTimeForward

def OnCalculate(rates_total, prev_calculated, begin, price):
    global _s_OnCalculate_ma1_, _s_OnCalculate_ma3_
    if rates_total < (min_rates_total + begin):
        return 0
    first = 0
    bar = 0
    ma1 = 0.0
    ma3 = 0.0
    val = 0.0
    slope1 = 0.0
    predict = 0.0
    if prev_calculated == 0:
        first = min_rates_total + begin
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, first)
        _s_OnCalculate_ma1_ = price[first - 1]
        _s_OnCalculate_ma3_ = _s_OnCalculate_ma1_
    else:
        first = prev_calculated - 1
    ma1 = _s_OnCalculate_ma1_
    ma3 = _s_OnCalculate_ma3_
    bar = first
    for bar in range(bar, rates_total):
        val = price[bar]
        ma1 = (p1 * val) + ((1.0 - p1) * ma1)
        ma3 = (p3 * val) + ((1.0 - p3) * ma3)
        slope1 = _fdiv(ma3 - ma1, t1 - t3)
        predict = ma3 + (slope1 * t)
        IndBuffer[bar] = predict + dPriceShift
        if bar < (rates_total - 1):
            _s_OnCalculate_ma1_ = ma1
            _s_OnCalculate_ma3_ = ma3
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_ma1_ = 0.0
_s_OnCalculate_ma3_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Emapredictive2(_MQL5Indicator):
    name = 'emapredictive2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LongPeriod': 25.0,
        'ShortPeriod': 8.0,
        'ExtraTimeForward': 1.0,  # How much to further extrapolate location
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

