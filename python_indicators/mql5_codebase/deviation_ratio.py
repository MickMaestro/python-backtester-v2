"""Deviation_Ratio — converted from MQL5: MQL5 Indicators/Deviation Ratio/Deviation_Ratio.mq5

Deviation Ratio
Copyright: Copyright © 2020, Tadeáš Rusňák; Link: http://www.tadeasrusnak.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2020, Tadeáš Rusňák', 'link': 'http://www.tadeasrusnak.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16448255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Deviation Ratio'}, 'levels': [0.9], 'description': ['Deviation Ratio'], 'name': 'Deviation_Ratio', 'source': 'MQL5 Indicators/Deviation Ratio/Deviation_Ratio.mq5', 'folder': 'Deviation Ratio', 'inputs': [{'mql': 'Short_StDevPeriod', 'py': 'Short_StDevPeriod', 'param': 'Short_StDevPeriod', 'type': 'int', 'default': 6, 'label': 'Fast StDev period', 'sinput': False}, {'mql': 'Long_StDevPeriod', 'py': 'Long_StDevPeriod', 'param': 'Long_StDevPeriod', 'type': 'int', 'default': 27, 'label': 'Slow StDev period', 'sinput': False}, {'mql': 'Short_StDevMode', 'py': 'Short_StDevMode', 'param': 'Short_StDevMode', 'type': 'int', 'default': 0, 'label': 'Short StDev Moving Average method', 'sinput': False}, {'mql': 'Short_StDevPrice', 'py': 'Short_StDevPrice', 'param': 'Short_StDevPrice', 'type': 'int', 'default': 1, 'label': 'Short StDev Moving Average price data', 'sinput': False}, {'mql': 'Long_StDevMode', 'py': 'Long_StDevMode', 'param': 'Long_StDevMode', 'type': 'int', 'default': 0, 'label': 'Short StDev Moving Average method', 'sinput': False}, {'mql': 'Long_StDevPrice', 'py': 'Long_StDevPrice', 'param': 'Long_StDevPrice', 'type': 'int', 'default': 1, 'label': 'Long StDev Moving Average price data', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Short_StDevPeriod = _input('Short_StDevPeriod', 6)  # Fast StDev period
Long_StDevPeriod = _input('Long_StDevPeriod', 27)  # Slow StDev period
Short_StDevMode = _input('Short_StDevMode', MODE_SMA)  # Short StDev Moving Average method
Short_StDevPrice = _input('Short_StDevPrice', PRICE_CLOSE)  # Short StDev Moving Average price data
Long_StDevMode = _input('Long_StDevMode', MODE_SMA)  # Short StDev Moving Average method
Long_StDevPrice = _input('Long_StDevPrice', PRICE_CLOSE)  # Long StDev Moving Average price data
StDevShift = 0
ExtLineBuffer = Arr(0, 0.0)
Short_STDEV_Handle = 0
Long_STDEV_Handle = 0
StartBars = 0

def OnInit():
    global Long_STDEV_Handle, Short_STDEV_Handle, StartBars
    Short_STDEV_Handle = iStdDev(None, PERIOD_CURRENT, Short_StDevPeriod, 0, Short_StDevMode, Short_StDevPrice)
    if Short_STDEV_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the Standard Deviation indicator')
    Long_STDEV_Handle = iStdDev(None, PERIOD_CURRENT, Long_StDevPeriod, 0, Long_StDevMode, Long_StDevPrice)
    if Long_STDEV_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the Standard Deviation indicator')
    StartBars = MathMax(Short_StDevPeriod, Long_StDevPeriod)
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    shortname = Box("")
    StringConcatenate(shortname, 'Deviation Ratio (', Short_StDevPeriod, ' ', Long_StDevPeriod, ')')
    PlotIndexSetInteger(0, PLOT_SHIFT, StDevShift)
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(Short_STDEV_Handle) < rates_total or BarsCalculated(Long_STDEV_Handle) < rates_total) or rates_total < StartBars:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    SRange = Arr(0, 0.0)
    LRange = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
        limit = rates_total - 1
    else:
        to_copy = rates_total - prev_calculated + 1
        limit = rates_total - prev_calculated
    if CopyBuffer(Short_STDEV_Handle, 0, 0, to_copy, SRange) <= 0:
        return 0
    if CopyBuffer(Long_STDEV_Handle, 0, 0, to_copy, LRange) <= 0:
        return 0
    ArraySetAsSeries(SRange, True)
    ArraySetAsSeries(LRange, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if LRange[bar] != 0.0 and LRange[bar] != EMPTY_VALUE:
            ExtLineBuffer[bar] = _fdiv(SRange[bar], LRange[bar])
        else:
            ExtLineBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DeviationRatio(_MQL5Indicator):
    name = 'Deviation_Ratio'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Short_StDevPeriod': 6,  # Fast StDev period
        'Long_StDevPeriod': 27,  # Slow StDev period
        'Short_StDevMode': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Short StDev Moving Average method
        'Short_StDevPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Short StDev Moving Average price data
        'Long_StDevMode': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Short StDev Moving Average method
        'Long_StDevPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Long StDev Moving Average price data
    }

