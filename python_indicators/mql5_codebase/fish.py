"""fish — converted from MQL5: MQL5 Indicators/Fish/fish.mq5

Copyright: Copyright © 2005, Yura Prokofiev; Link: Yura.prokofiev@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Yura Prokofiev', 'link': 'Yura.prokofiev@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [36095, 15631086, 8421504, 16760576, 3329330]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Fish'}, 'levels': [], 'description': [], 'name': 'fish', 'source': 'MQL5 Indicators/Fish/fish.mq5', 'folder': 'Fish', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period = _input('period', 10)
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(period + 1)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Fish')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, High, Low, Close, tick_volume, volume, spread):
    global _s_OnCalculate_Value1
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    price = 0.0
    MaxH = 0.0
    MinL = 0.0
    Range = 0.0
    Value = 0.0
    Diff = 0.0
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        barl = limit + 1
        MaxH = High[ArrayMaximum(High, barl, period)]
        MinL = Low[ArrayMinimum(Low, barl, period)]
        price = (High[barl] + Low[barl]) / 2
        Range = MaxH - MinL
        if Range:
            _s_OnCalculate_Value1 = 0.33 * 2 * (_fdiv(price - MinL, Range) - 0.5)
        _s_OnCalculate_Value1 = MathMin(MathMax(_s_OnCalculate_Value1, -0.999), 0.999)
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        MaxH = High[ArrayMaximum(High, bar, period)]
        MinL = Low[ArrayMinimum(Low, bar, period)]
        price = (High[bar] + Low[bar]) / 2
        Range = MaxH - MinL
        if Range:
            Value = (0.33 * 2 * (_fdiv(price - MinL, Range) - 0.5)) + (0.67 * _s_OnCalculate_Value1)
        Value = MathMin(MathMax(Value, -0.999), 0.999)
        Diff = 1 - Value
        if Diff:
            IndBuffer[bar] = (0.5 * MathLog(_fdiv(1 + Value, Diff))) + (0.5 * IndBuffer[bar + 1])
        else:
            IndBuffer[bar] = 1.0
        if bar:
            _s_OnCalculate_Value1 = Value
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        clr = 2
        if IndBuffer[bar] > 0:
            if IndBuffer[bar] > IndBuffer[bar + 1]:
                clr = 4
            if IndBuffer[bar] < IndBuffer[bar + 1]:
                clr = 3
        if IndBuffer[bar] < 0:
            if IndBuffer[bar] < IndBuffer[bar + 1]:
                clr = 0
            if IndBuffer[bar] > IndBuffer[bar + 1]:
                clr = 1
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Value1 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Fish(_MQL5Indicator):
    name = 'fish'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 10,
    }

