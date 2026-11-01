"""HEX-Indicator (Heikin-Ashi-Extended) — converted from MQL5: MQL5 Indicators/Extended Heikin Ashi Indicator/HEX-Indicator (Heikin-Ashi-Extended).mq5

Copyright: Copyright (C) 2010-2020 Dominik Egert; Link: http://www.freie-netze.de

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright (C) 2010-2020 Dominik Egert', 'link': 'http://www.freie-netze.de', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16748574, 255, 8421504]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Heiken Ashi Open;Heiken Ashi High;Heiken Ashi Low;Heiken Ashi Close'}, 'levels': [], 'description': [], 'name': 'HEX-Indicator (Heikin-Ashi-Extended)', 'source': 'MQL5 Indicators/Extended Heikin Ashi Indicator/HEX-Indicator (Heikin-Ashi-Extended).mq5', 'folder': 'Extended Heikin Ashi Indicator', 'inputs': [{'mql': 'Periods', 'py': 'Periods', 'param': 'Periods', 'type': 'int', 'default': 1, 'label': 'Reference period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Periods = _input('Periods', 1)  # Reference period
ExtOBuffer = Arr(0, 0.0)
ExtHBuffer = Arr(0, 0.0)
ExtLBuffer = Arr(0, 0.0)
ExtCBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtOBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Heiken Ashi')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    limit = 0
    symbol_digits_factor = _uint(MathPow(10, SymbolInfoInteger(Symbol(), SYMBOL_DIGITS)))
    if prev_calculated == 0:
        ExtLBuffer[0] = Low[0]
        ExtHBuffer[0] = High[0]
        ExtOBuffer[0] = Open[0]
        ExtCBuffer[0] = Close[0]
        limit = Periods
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        haOpen = (ExtOBuffer[i - Periods] + ExtCBuffer[i - Periods]) / 2.0
        haClose = (Open[i] + High[i] + Low[i] + Close[i]) / 4.0
        haHigh = MathMax(High[i], MathMax(haOpen, haClose))
        haLow = MathMin(Low[i], MathMin(haOpen, haClose))
        ExtLBuffer[i] = haLow
        ExtHBuffer[i] = haHigh
        ExtOBuffer[i] = haOpen
        ExtCBuffer[i] = haClose
        if (MathMax(ExtCBuffer[i - Periods], ExtOBuffer[i - Periods]) > haClose or (MathMin(haClose, haOpen) > haLow and MathMax(haClose, haOpen) == haHigh)) or MathMin(haClose, haOpen) < haLow:
            ExtColorBuffer[i] = 1.0
        if (MathMin(ExtCBuffer[i - Periods], ExtOBuffer[i - Periods]) < haClose or (MathMin(haClose, haOpen) == haLow and MathMax(haClose, haOpen) < haHigh)) or MathMax(haClose, haOpen) < haHigh:
            ExtColorBuffer[i] = 0.0
        if MathMin(haOpen, haClose) > haLow and MathMax(haOpen, haClose) < haHigh:
            ExtColorBuffer[i] = ExtColorBuffer[i - 1]
        if ((MathMin(ExtOBuffer[i - 1], ExtCBuffer[i - 1]) > ExtLBuffer[i - 1] and MathMax(ExtOBuffer[i - 1], ExtCBuffer[i - 1]) < ExtHBuffer[i - 1]) and MathMin(haOpen, haClose) > haLow) and MathMax(haOpen, haClose) < haHigh:
            ExtColorBuffer[i] = 2.0
        if (haHigh - haLow) < _idiv(Spread[i], symbol_digits_factor):
            ExtColorBuffer[i] = 2.0
        if haOpen == haClose:
            ExtColorBuffer[i] = ExtColorBuffer[i - 1]
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HEXIndicatorHeikinAshiExtended(_MQL5Indicator):
    name = 'HEX-Indicator (Heikin-Ashi-Extended)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Periods': 1,  # Reference period
    }

