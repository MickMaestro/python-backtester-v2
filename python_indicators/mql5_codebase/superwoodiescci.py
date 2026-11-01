"""superwoodiescci — converted from MQL5: MQL5 Indicators/SuperWoodiesCCI/superwoodiescci.mq5

Copyright: Copyright © 2012, duckfu; Link: http://www.dopeness.org; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, duckfu', 'link': 'http://www.dopeness.org', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 10}, 'colors': {1: [8388736], 2: [16711680], 3: [255, 14822282, 3329330]}, 'widths': {1: 1, 2: 1, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'CCI', 2: 'TCCI', 3: 'SuperWoodiesCCI'}, 'levels': [0.0], 'description': [], 'name': 'superwoodiescci', 'source': 'MQL5 Indicators/SuperWoodiesCCI/superwoodiescci.mq5', 'folder': 'SuperWoodiesCCI', 'inputs': [{'mql': 'CCI_Period', 'py': 'CCI_Period', 'param': 'CCI_Period', 'type': 'uint', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'TCCI_Period', 'py': 'TCCI_Period', 'param': 'TCCI_Period', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 6, 'label': 'price type or handle', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CCI_Period = _input('CCI_Period', 50)
TCCI_Period = _input('TCCI_Period', 10)
applied_price = _input('applied_price', PRICE_TYPICAL)  # price type or handle
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
CCIBuffer = Arr(0, 0.0)
TCCIBuffer = Arr(0, 0.0)
HistBuffer = Arr(0, 0.0)
ColorHistBuffer = Arr(0, 0.0)
CCI_Handle = 0
TCCI_Handle = 0
min_rates_total = 0

def OnInit():
    global CCI_Handle, TCCI_Handle, min_rates_total
    min_rates_total = _int(MathMax(CCI_Period, TCCI_Period)) + 6
    CCI_Handle = iCCI(None, 0, CCI_Period, applied_price)
    if CCI_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iCCI indicator')
    TCCI_Handle = iCCI(None, 0, TCCI_Period, applied_price)
    if TCCI_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iCCI indicator')
    SetIndexBuffer(0, CCIBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(CCIBuffer, True)
    SetIndexBuffer(1, TCCIBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(TCCIBuffer, True)
    SetIndexBuffer(2, HistBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(HistBuffer, True)
    SetIndexBuffer(3, ColorHistBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorHistBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'SuperWoodiesCCI(', CCI_Period, ', ', CCI_Period, ', ', EnumToString(applied_price, 'ENUM_APPLIED_PRICE'), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(CCI_Handle) < rates_total or BarsCalculated(TCCI_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    j = 0
    uptrending = 0
    downtrending = 0
    clr = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(CCI_Handle, 0, 0, to_copy, CCIBuffer) <= 0:
        return 0
    if CopyBuffer(TCCI_Handle, 0, 0, to_copy, TCCIBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        clr = 1
        HistBuffer[bar] = CCIBuffer[bar]
        uptrending = 0
        j = 0
        for j in range(j, 6):
            if CCIBuffer[bar + j] > 0:
                uptrending += 1
            elif CCIBuffer[bar + j] < 0:
                uptrending = 0
        else:
            j = _range_end(j, 6, 1)
        if uptrending > 5:
            clr = 2
        downtrending = 0
        j = 0
        for j in range(j, 6):
            if CCIBuffer[bar + j] < 0:
                downtrending += 1
            elif CCIBuffer[bar + j] > 0:
                downtrending = 0
        else:
            j = _range_end(j, 6, 1)
        if downtrending > 5:
            clr = 0
        ColorHistBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Superwoodiescci(_MQL5Indicator):
    name = 'superwoodiescci'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CCI_Period': 50,
        'TCCI_Period': 10,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # price type or handle
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

