"""fishertransform — converted from MQL5: MQL5 Indicators/FisherTransform_HTF/fishertransform.mq5

Copyright: Coded by Witold Wozniak; Link: www.mqlsoft.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Coded by Witold Wozniak', 'link': 'www.mqlsoft.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Fisher', 2: 'Trigger'}, 'levels': [0.0], 'description': [], 'name': 'fishertransform', 'source': 'MQL5 Indicators/FisherTransform_HTF/fishertransform.mq5', 'folder': 'FisherTransform_HTF', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 10, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 10)  # Период индикатора
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
FisherBuffer = Arr(0, 0.0)
TriggerBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, FisherBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Length)
    SetIndexBuffer(1, TriggerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, Length)
    shortname = Box("")
    StringConcatenate(shortname, 'FisherTransform(', Length, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Value_
    if rates_total < Length:
        return 0
    first = 0
    bar = 0
    kkk = 0
    price = 0.0
    price1 = 0.0
    MaxH = 0.0
    MinL = 0.0
    Value = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = Length - 1
        _s_OnCalculate_Value_ = 0.0
        FisherBuffer[first - 1] = 0.0
    else:
        first = prev_calculated - 1
    Value = _s_OnCalculate_Value_
    bar = first
    for bar in range(bar, rates_total):
        if rates_total != prev_calculated and bar == (rates_total - 1):
            _s_OnCalculate_Value_ = Value
        price = (high[bar] + low[bar]) / 2.0
        MaxH = price
        MinL = price
        for iii in range(0, Length):
            kkk = bar - iii
            price1 = (high[kkk] + low[kkk]) / 2.0
            if price1 > MaxH:
                MaxH = price1
            if price1 < MinL:
                MinL = price1
        res = MaxH - MinL
        if res:
            Value = (0.5 * 2.0 * (_fdiv(price - MinL, res) - 0.5)) + (0.5 * Value)
        else:
            Value = 0.0
        if Value > 0.9999:
            Value = 0.9999
        if Value < -0.9999:
            Value = -0.9999
        FisherBuffer[bar] = (0.25 * MathLog(_fdiv(1 + Value, 1 - Value))) + (0.5 * FisherBuffer[bar - 1])
        TriggerBuffer[bar] = FisherBuffer[bar - 1]
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Value_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Fishertransform(_MQL5Indicator):
    name = 'fishertransform'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 10,  # Период индикатора
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

