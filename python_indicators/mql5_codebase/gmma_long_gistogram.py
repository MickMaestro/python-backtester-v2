"""gmma_long_gistogram — converted from MQL5: MQL5 Indicators/GMMA_Long_Gistogram/gmma_long_gistogram.mq5

Copyright: Copyright © 2010, dmmikl86; Link: mhs_86@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, dmmikl86', 'link': 'mhs_86@mail.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [255, 16711935, 8421504, 8421376, 65280]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'GMMA_Long_Gistogram'}, 'levels': [0.0], 'description': [], 'name': 'gmma_long_gistogram', 'source': 'MQL5 Indicators/GMMA_Long_Gistogram/gmma_long_gistogram.mq5', 'folder': 'GMMA_Long_Gistogram', 'inputs': [{'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
ExtBuffer = Arr(0, 0.0)
ColorExtBuffer = Arr(0, 0.0)
min_rates_total = 0
InpInd_Handle = Arr(6, 0, dyn=False)

def OnInit():
    global min_rates_total
    min_rates_total = 61
    InpInd_Handle[0] = iMA(Symbol(), PERIOD_CURRENT, 30, 0, MODE_EMA, PRICE_CLOSE)
    if InpInd_Handle[0] == INVALID_HANDLE:
        Print(' Failed to get the iMA indicator handle')
    InpInd_Handle[1] = iMA(Symbol(), PERIOD_CURRENT, 35, 0, MODE_EMA, PRICE_CLOSE)
    if InpInd_Handle[1] == INVALID_HANDLE:
        Print(' Failed to get the iMA indicator handle')
    InpInd_Handle[2] = iMA(Symbol(), PERIOD_CURRENT, 40, 0, MODE_EMA, PRICE_CLOSE)
    if InpInd_Handle[2] == INVALID_HANDLE:
        Print(' Failed to get the iMA indicator handle')
    InpInd_Handle[3] = iMA(Symbol(), PERIOD_CURRENT, 45, 0, MODE_EMA, PRICE_CLOSE)
    if InpInd_Handle[3] == INVALID_HANDLE:
        Print(' Failed to get the iMA indicator handle')
    InpInd_Handle[4] = iMA(Symbol(), PERIOD_CURRENT, 50, 0, MODE_EMA, PRICE_CLOSE)
    if InpInd_Handle[4] == INVALID_HANDLE:
        Print(' Failed to get the iMA indicator handle')
    InpInd_Handle[5] = iMA(Symbol(), PERIOD_CURRENT, 60, 0, MODE_EMA, PRICE_CLOSE)
    if InpInd_Handle[5] == INVALID_HANDLE:
        Print(' Failed to get the iMA indicator handle')
    SetIndexBuffer(0, ExtBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtBuffer, True)
    SetIndexBuffer(1, ColorExtBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorExtBuffer, True)
    shortname = 'GMMA_Long_Gistogram'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    for numb in range(0, 6):
        if BarsCalculated(InpInd_Handle[numb]) < min_rates_total:
            return 0
    limit = 0
    bar = 0
    to_copy = 0
    EMA0 = Arr(0, 0.0)
    EMA1 = Arr(0, 0.0)
    EMA2 = Arr(0, 0.0)
    EMA3 = Arr(0, 0.0)
    EMA4 = Arr(0, 0.0)
    EMA5 = Arr(0, 0.0)
    ArraySetAsSeries(EMA0, True)
    ArraySetAsSeries(EMA1, True)
    ArraySetAsSeries(EMA2, True)
    ArraySetAsSeries(EMA3, True)
    ArraySetAsSeries(EMA4, True)
    ArraySetAsSeries(EMA5, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(InpInd_Handle[0], 0, 0, to_copy, EMA0) <= 0:
        return 0
    if CopyBuffer(InpInd_Handle[1], 0, 0, to_copy, EMA1) <= 0:
        return 0
    if CopyBuffer(InpInd_Handle[2], 0, 0, to_copy, EMA2) <= 0:
        return 0
    if CopyBuffer(InpInd_Handle[3], 0, 0, to_copy, EMA3) <= 0:
        return 0
    if CopyBuffer(InpInd_Handle[4], 0, 0, to_copy, EMA4) <= 0:
        return 0
    if CopyBuffer(InpInd_Handle[5], 0, 0, to_copy, EMA5) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtBuffer[bar] = EMA0[bar] - EMA0[bar + 1] + ((EMA1[bar] - EMA1[bar + 1]) * 1.2) + ((EMA2[bar] - EMA2[bar + 1]) * 1.4) + ((EMA3[bar] - EMA3[bar + 1]) * 1.6) + ((EMA4[bar] - EMA4[bar + 1]) * 1.8) + ((EMA5[bar] - EMA5[bar + 1]) * 2)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ColorExtBuffer[bar] = 2.0
        if ExtBuffer[bar] > 0:
            if ExtBuffer[bar] > ExtBuffer[bar + 1]:
                ColorExtBuffer[bar] = 4.0
            if ExtBuffer[bar] < ExtBuffer[bar + 1]:
                ColorExtBuffer[bar] = 3.0
        if ExtBuffer[bar] < 0:
            if ExtBuffer[bar] > ExtBuffer[bar + 1]:
                ColorExtBuffer[bar] = 1.0
            if ExtBuffer[bar] < ExtBuffer[bar + 1]:
                ColorExtBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GmmaLongGistogram(_MQL5Indicator):
    name = 'gmma_long_gistogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

