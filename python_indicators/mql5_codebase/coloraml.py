"""coloraml — converted from MQL5: MQL5 Indicators/AML Adaptive Market Level/coloraml.mq5

Copyright: Adaptive Market Level; Link: andreybs@yandex.ru; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Adaptive Market Level', 'link': 'andreybs@yandex.ru', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [255, 8421504, 15624315]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'AML'}, 'levels': [], 'description': [], 'name': 'coloraml', 'source': 'MQL5 Indicators/AML Adaptive Market Level/coloraml.mq5', 'folder': 'AML Adaptive Market Level', 'inputs': [{'mql': 'Fractal', 'py': 'Fractal', 'param': 'Fractal', 'type': 'int', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'Lag', 'py': 'Lag', 'param': 'Lag', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Fractal = _input('Fractal', 6)
Lag = _input('Lag', 7)
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
AMLBuffer = Arr(0, 0.0)
ColorAMLBuffer = Arr(0, 0.0)
min_rates_total = 0
size = 0
Count = Arr(0, 0)
Smooth = Arr(0, 0.0)

def Recount_ArrayZeroPos(CoArr, Size):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def Range(period, start, High, Low):
    max_ = High[ArrayMaximum(High, start, period)]
    min_ = Low[ArrayMinimum(Low, start, period)]
    return max_ - min_

def OnInit():
    global min_rates_total, size
    min_rates_total = Fractal + Lag
    size = Lag + 1
    ArrayResize(Count, size)
    ArrayResize(Smooth, size)
    ArrayInitialize(Smooth, 0.0)
    ArrayInitialize(Count, 0.0)
    SetIndexBuffer(0, AMLBuffer, INDICATOR_DATA)
    ArraySetAsSeries(AMLBuffer, True)
    SetIndexBuffer(1, ColorAMLBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorAMLBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box("")
    StringConcatenate(shortname, 'AML(', Fractal, ', ', Lag, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    MaxBar = 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        ColorAMLBuffer[limit] = 1.0
    else:
        limit = rates_total - prev_calculated
    MaxBar = rates_total - min_rates_total - 3
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        R1 = Range(Fractal, bar, high, low) / Fractal
        R2 = Range(Fractal, bar + Fractal, high, low) / Fractal
        R3 = Range(2 * Fractal, bar, high, low) / (2 * Fractal)
        dim = 0.0
        if (R1 + R2) > 0 and R3 > 0:
            dim = (MathLog(R1 + R2) - MathLog(R3)) * 1.44269504088896
        alpha = MathExp((-Lag) * (dim - 1.0))
        alpha = MathMin(alpha, 1.0)
        alpha = MathMax(alpha, 0.01)
        price = (high[bar] + low[bar] + (2 * open[bar]) + (2 * close[bar])) / 6
        Smooth[Count[0]] = (alpha * price) + ((1.0 - alpha) * Smooth[Count[1]])
        if MathAbs(Smooth[Count[0]] - Smooth[Count[Lag]]) >= (Lag * Lag * Point()):
            AMLBuffer[bar] = Smooth[Count[0]]
        else:
            AMLBuffer[bar] = AMLBuffer[bar + 1]
        ColorAMLBuffer[bar] = ColorAMLBuffer[bar + 1]
        if AMLBuffer[bar] > AMLBuffer[bar + 1]:
            ColorAMLBuffer[bar] = 2.0
        if AMLBuffer[bar] < AMLBuffer[bar + 1]:
            ColorAMLBuffer[bar] = 0.0
        if bar:
            Recount_ArrayZeroPos(Count, Lag + 1)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Coloraml(_MQL5Indicator):
    name = 'coloraml'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Fractal': 6,
        'Lag': 7,
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

