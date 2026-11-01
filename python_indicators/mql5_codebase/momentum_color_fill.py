"""momentum_color_fill — converted from MQL5: MQL5 Indicators/Momentum Color Fill/momentum_color_fill.mq5

Copyright: Alexander Piechotta (FinGeR); Link: http://www.metatrader-wiki.com/

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Alexander Piechotta (FinGeR)', 'link': 'http://www.metatrader-wiki.com/', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 7, 2: 1}, 'colors': {1: [4678655, 13422920], 2: [16777215]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'momentum_color_fill', 'source': 'MQL5 Indicators/Momentum Color Fill/momentum_color_fill.mq5', 'folder': 'Momentum Color Fill', 'inputs': [{'mql': 'InpMomentumPeriod', 'py': 'InpMomentumPeriod', 'param': 'InpMomentumPeriod', 'type': 'int', 'default': 14, 'label': 'period', 'sinput': False}, {'mql': 'InpLevel', 'py': 'InpLevel', 'param': 'InpLevel', 'type': 'int', 'default': 100, 'label': 'level line', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpMomentumPeriod = _input('InpMomentumPeriod', 14)  # period
InpLevel = _input('InpLevel', 100)  # level line
ExtMomentumBuffer = Arr(0, 0.0)
ExtMomentumBuffer2 = Arr(0, 0.0)
ExtMomentumBuffer3 = Arr(0, 0.0)
ExtMomentumPeriod = 0

def OnInit():
    global ExtMomentumPeriod
    if InpMomentumPeriod < 0:
        ExtMomentumPeriod = 14
        Print('Input parameter InpMomentumPeriod has wrong value. Indicator will use value ', ExtMomentumPeriod)
    else:
        ExtMomentumPeriod = InpMomentumPeriod
    SetIndexBuffer(0, ExtMomentumBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtMomentumBuffer2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, ExtMomentumBuffer3, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Momentum Color Fill' + ' (' + _str(ExtMomentumPeriod) + ')')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtMomentumPeriod - 1)
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, InpLevel)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)

def OnCalculate(rates_total, prev_calculated, begin, price):
    StartCalcPosition = ExtMomentumPeriod - 1 + begin
    if rates_total < StartCalcPosition:
        return 0
    if begin > 0:
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartCalcPosition + (ExtMomentumPeriod - 1))
    pos = prev_calculated - 1
    if pos < StartCalcPosition:
        pos = begin + ExtMomentumPeriod
    for i in range(pos, rates_total):
        ExtMomentumBuffer2[i] = InpLevel
        ExtMomentumBuffer[i] = _fdiv(price[i] * 100, price[i - ExtMomentumPeriod])
        ExtMomentumBuffer3[i] = ExtMomentumBuffer[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MomentumColorFill(_MQL5Indicator):
    name = 'momentum_color_fill'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMomentumPeriod': 14,  # period
        'InpLevel': 100,  # level line
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

