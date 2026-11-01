"""ianchmom — converted from MQL5: MQL5 Indicators/iAnchMom/ianchmom.mq5

Copyright: Copyright © 2007, NNN; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, NNN', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [255, 16711935, 8421504, 16711680, 32768]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'iAnchMom'}, 'levels': [], 'description': [], 'name': 'ianchmom', 'source': 'MQL5 Indicators/iAnchMom/ianchmom.mq5', 'folder': 'iAnchMom', 'inputs': [{'mql': 'SMAPeriod', 'py': 'SMAPeriod', 'param': 'SMAPeriod', 'type': 'uint', 'default': 34, 'label': 'SMA period', 'sinput': False}, {'mql': 'EMAPeriod', 'py': 'EMAPeriod', 'param': 'EMAPeriod', 'type': 'uint', 'default': 20, 'label': 'EMA period', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant used for the indicator calculation', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SMAPeriod = _input('SMAPeriod', 34)  # SMA period
EMAPeriod = _input('EMAPeriod', 20)  # EMA period
IPC = _input('IPC', PRICE_CLOSE)  # Price constant used for the indicator calculation
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
SMA_Handle = 0
EMA_Handle = 0
min_rates_total = 0

def OnInit():
    global EMA_Handle, SMA_Handle, min_rates_total
    SMA_Handle = iMA(None, 0, SMAPeriod, 0, MODE_SMA, IPC)
    if SMA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the SMA indicator')
        return INIT_FAILED
    EMA_Handle = iMA(None, 0, EMAPeriod, 0, MODE_EMA, IPC)
    if EMA_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of the EMA indicator')
        return INIT_FAILED
    min_rates_total = _int(SMAPeriod + 1)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'iAnchMom(', SMAPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 4)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(SMA_Handle) < rates_total or BarsCalculated(EMA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    SMA = Arr(0, 0.0)
    EMA = Arr(0, 0.0)
    to_copy = 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total + 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(SMA_Handle, 0, 0, to_copy, SMA) <= 0:
        return 0
    if CopyBuffer(EMA_Handle, 0, 0, to_copy, EMA) <= 0:
        return 0
    ArraySetAsSeries(SMA, True)
    ArraySetAsSeries(EMA, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if SMA[bar]:
            IndBuffer[bar] = 100 * (_fdiv(EMA[bar], SMA[bar]) - 1.0)
        else:
            IndBuffer[bar] = EMPTY_VALUE
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ianchmom(_MQL5Indicator):
    name = 'ianchmom'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SMAPeriod': 34,  # SMA period
        'EMAPeriod': 20,  # EMA period
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price constant used for the indicator calculation
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

