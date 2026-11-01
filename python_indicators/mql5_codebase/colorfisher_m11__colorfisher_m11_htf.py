"""ColorFisher_m11 — converted from MQL5: MQL5 Indicators/ColorFisher_m11_HTF/ColorFisher_m11.mq5

Copyright: Copyright © 23.07.2006, MartinG; Link: http://home.arcor.de/cam06/fisher; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 23.07.2006, MartinG', 'link': 'http://home.arcor.de/cam06/fisher', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16760576, 16711680, 8421504, 8388736, 11823615]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'ColorFisher_m11'}, 'levels': [], 'description': [], 'name': 'ColorFisher_m11', 'source': 'MQL5 Indicators/ColorFisher_m11_HTF/ColorFisher_m11.mq5', 'folder': 'ColorFisher_m11_HTF', 'inputs': [{'mql': 'RangePeriods', 'py': 'RangePeriods', 'param': 'RangePeriods', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'PriceSmoothing', 'py': 'PriceSmoothing', 'param': 'PriceSmoothing', 'type': 'double', 'default': 0.3, 'label': '', 'sinput': False}, {'mql': 'IndexSmoothing', 'py': 'IndexSmoothing', 'param': 'IndexSmoothing', 'type': 'double', 'default': 0.3, 'label': '', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'double', 'default': 1.01, 'label': 'уровень перезакупа', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'double', 'default': -1.01, 'label': 'уровень перепроданности', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RangePeriods = _input('RangePeriods', 10)
PriceSmoothing = _input('PriceSmoothing', 0.3)
IndexSmoothing = _input('IndexSmoothing', 0.3)
HighLevel = _input('HighLevel', 1.01)  # уровень перезакупа
LowLevel = _input('LowLevel', -1.01)  # уровень перепроданности
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(RangePeriods) + 1
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box('')
    StringConcatenate(shortname, 'Fisher_m11(', RangePeriods, ', ', DoubleToString(PriceSmoothing, 2), ', ', DoubleToString(IndexSmoothing, 2), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 0.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrMediumSeaGreen)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrRed)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Fish_prev
    if rates_total < min_rates_total:
        return 0
    LowestLow = 0.0
    HighestHigh = 0.0
    GreatestRange = 0.0
    MidPrice = 0.0
    diff = 0.0
    res = 0.0
    PriceLocation = 0.0
    SmoothedLocation = 0.0
    FishIndex = 0.0
    Fish = 0.0
    first = 0
    bar = 0
    clr = 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
        _s_OnCalculate_Fish_prev = 0.0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        barx = rates_total - 1 - bar
        HighestHigh = high[ArrayMaximum(high, barx, RangePeriods)]
        LowestLow = low[ArrayMinimum(low, barx, RangePeriods)]
        res = 0.1 * Point()
        if (HighestHigh - LowestLow) < res:
            HighestHigh = LowestLow + res
        GreatestRange = HighestHigh - LowestLow
        MidPrice = (high[barx] + low[barx]) / 2.0
        if GreatestRange:
            PriceLocation = _fdiv(MidPrice - LowestLow, GreatestRange)
            PriceLocation = (2.0 * PriceLocation) - 1.0
        else:
            PriceLocation = 0.99
        Fish = (PriceSmoothing * _s_OnCalculate_Fish_prev) + ((1.0 - PriceSmoothing) * PriceLocation)
        SmoothedLocation = Fish
        SmoothedLocation = MathMin(SmoothedLocation, 0.99)
        SmoothedLocation = MathMax(SmoothedLocation, -0.99)
        diff = 1.0 - SmoothedLocation
        if diff:
            FishIndex = MathLog(_fdiv(1 + SmoothedLocation, diff))
        else:
            FishIndex = 0.0
        IndBuffer[bar] = (IndexSmoothing * IndBuffer[bar - 1]) + ((1.0 - IndexSmoothing) * FishIndex)
        if bar < (rates_total - 1):
            _s_OnCalculate_Fish_prev = Fish
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        clr = 2
        if IndBuffer[bar] > 0:
            if IndBuffer[bar] > HighLevel:
                clr = 0
            else:
                clr = 1
        if IndBuffer[bar] < 0:
            if IndBuffer[bar] < LowLevel:
                clr = 4
            else:
                clr = 3
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Fish_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorFisherM11(_MQL5Indicator):
    name = 'ColorFisher_m11'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RangePeriods': 10,
        'PriceSmoothing': 0.3,
        'IndexSmoothing': 0.3,
        'HighLevel': 1.01,  # уровень перезакупа
        'LowLevel': -1.01,  # уровень перепроданности
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

