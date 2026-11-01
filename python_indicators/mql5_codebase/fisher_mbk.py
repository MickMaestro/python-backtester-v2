"""fisher_mbk — converted from MQL5: MQL5 Indicators/Fisher_mbk/fisher_mbk.mq5

Copyright: Copyright © 2005, Matt Kennel; Link: Yura.prokofiev@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Matt Kennel', 'link': 'Yura.prokofiev@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_maximum': 1.0, 'indicator_minimum': -1.0}, 'types': {1: 10}, 'colors': {1: [16711935, 15631086, 8421504, 16760576, 16711680]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Fisher_mbk'}, 'levels': [], 'description': [], 'name': 'fisher_mbk', 'source': 'MQL5 Indicators/Fisher_mbk/fisher_mbk.mq5', 'folder': 'Fisher_mbk', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'HMALenHiLo', 'py': 'HMALenHiLo', 'param': 'HMALenHiLo', 'type': 'double', 'default': 5.0, 'label': '', 'sinput': False}, {'mql': 'HMALenZ', 'py': 'HMALenZ', 'param': 'HMALenZ', 'type': 'double', 'default': 3.0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period = _input('period', 10)
HMALenHiLo = _input('HMALenHiLo', 5.0)
HMALenZ = _input('HMALenZ', 3.0)
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
mix_a = 0.0
mix_b = 0.0
mixprime_a = 0.0
mixprime_b = 0.0
min_rates_total = 0

def OnInit():
    global min_rates_total, mix_a, mix_b, mixprime_a, mixprime_b
    min_rates_total = _int(period + 1)
    mix_a = _fdiv(3.0, 2.0 + HMALenHiLo)
    mix_b = _fdiv(3.0, 2.0 + HMALenZ)
    mixprime_a = 1.0 - mix_a
    mixprime_b = 1.0 - mix_b
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Fisher_mbk')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, High, Low, Close, tick_volume, volume, spread):
    global _s_OnCalculate_ma1_a, _s_OnCalculate_ma1_b, _s_OnCalculate_ma2_a, _s_OnCalculate_ma2_b
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    MaxH = 0.0
    MinL = 0.0
    HiLo = 0.0
    Range = 0.0
    ma1 = 0.0
    ma2 = 0.0
    HMAofHiLo = 0.0
    Value = 0.0
    Diff = 0.0
    Ztransformed = 0.0
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        barl = limit + 1
        MaxH = High[ArrayMaximum(High, barl, period)]
        MinL = Low[ArrayMinimum(Low, barl, period)]
        Range = MaxH - MinL
        if Range:
            HiLo = _fdiv(2.0 * (Close[barl] - MinL), Range) - 1.0
        else:
            HiLo = 0.0
        _s_OnCalculate_ma1_a = HiLo
        _s_OnCalculate_ma2_a = _s_OnCalculate_ma1_a
        HMAofHiLo = (1.5 * ma1) - ma2
        Value = MathMin(MathMax(HMAofHiLo, -0.999), 0.999)
        Diff = 1 - Value
        if Diff:
            Ztransformed = MathLog(_fdiv(1 + Value, Diff))
        else:
            Ztransformed = 0.0
        _s_OnCalculate_ma1_b = Ztransformed
        _s_OnCalculate_ma2_b = _s_OnCalculate_ma1_b
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        MaxH = High[ArrayMaximum(High, bar, period)]
        MinL = Low[ArrayMinimum(Low, bar, period)]
        Range = MaxH - MinL
        if Range:
            HiLo = _fdiv(2.0 * (Close[bar] - MinL), Range) - 1.0
        else:
            HiLo = 0.0
        ma1 = (mixprime_a * _s_OnCalculate_ma1_a) + (mix_a * HiLo)
        ma2 = (mixprime_a * _s_OnCalculate_ma2_a) + (mix_a * ma1)
        HMAofHiLo = (1.5 * ma1) - ma2
        if bar:
            _s_OnCalculate_ma1_a = ma1
            _s_OnCalculate_ma2_a = ma2
        Value = MathMin(MathMax(HMAofHiLo, -0.999), 0.999)
        Diff = 1 - Value
        if Diff:
            Ztransformed = MathLog(_fdiv(1 + Value, Diff))
        else:
            Ztransformed = 0.0
        ma1 = (mixprime_b * _s_OnCalculate_ma1_b) + (mix_b * Ztransformed)
        ma2 = (mixprime_b * _s_OnCalculate_ma2_b) + (mix_b * ma1)
        IndBuffer[bar] = (1.5 * ma1) - ma2
        if bar:
            _s_OnCalculate_ma1_b = ma1
            _s_OnCalculate_ma2_b = ma2
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
_s_OnCalculate_ma1_a = 0.0
_s_OnCalculate_ma2_a = 0.0
_s_OnCalculate_ma1_b = 0.0
_s_OnCalculate_ma2_b = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FisherMbk(_MQL5Indicator):
    name = 'fisher_mbk'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 10,
        'HMALenHiLo': 5.0,
        'HMALenZ': 3.0,
    }
    y_range = (-1.0, 1.0)

