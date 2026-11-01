"""dma — converted from MQL5: MQL5 Indicators/DMA (Displaced Moving Averages)/dma.mq5

DMA Indicator (Displaced Moving Averages) displays three MA in the main window:
                                                                                
3-period moving average, shifted forward by three periods (SR DMA);
7-period moving average, shifted forward by five periods (MR DMA);
25-period moving average, shifted forward by five periods (LR DMA).
Copyright: Copyright © 2010, LenIFCHIK; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, LenIFCHIK', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [16711680], 3: [65280]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'SR DMA', 2: 'MR DMA', 3: 'LR DMA'}, 'levels': [], 'description': ['DMA Indicator (Displaced Moving Averages) displays three MA in the main window:', '                                                                                ', '3-period moving average, shifted forward by three periods (SR DMA);', '7-period moving average, shifted forward by five periods (MR DMA);', '25-period moving average, shifted forward by five periods (LR DMA).'], 'name': 'dma', 'source': 'MQL5 Indicators/DMA (Displaced Moving Averages)/dma.mq5', 'folder': 'DMA (Displaced Moving Averages)', 'inputs': [{'mql': 'SR_method', 'py': 'SR_method', 'param': 'SR_method', 'type': 'int', 'default': 0, 'label': 'SR MA smoothing type', 'sinput': False}, {'mql': 'SR_Period', 'py': 'SR_Period', 'param': 'SR_Period', 'type': 'uint', 'default': 3, 'label': 'SR MA smoothing period', 'sinput': False}, {'mql': 'SR_price_', 'py': 'SR_price_', 'param': 'SR_price_', 'type': 'int', 'default': 1, 'label': 'SR MA price constant', 'sinput': False}, {'mql': 'SR_Shift', 'py': 'SR_Shift', 'param': 'SR_Shift', 'type': 'int', 'default': 3, 'label': 'horizontal shift of SR MA in bars', 'sinput': False}, {'mql': 'MR_method', 'py': 'MR_method', 'param': 'MR_method', 'type': 'int', 'default': 0, 'label': 'MR MA smoothing type', 'sinput': False}, {'mql': 'MR_Period', 'py': 'MR_Period', 'param': 'MR_Period', 'type': 'uint', 'default': 7, 'label': 'MR MA smoothing period', 'sinput': False}, {'mql': 'MR_price_', 'py': 'MR_price_', 'param': 'MR_price_', 'type': 'int', 'default': 1, 'label': 'MR MA price constant', 'sinput': False}, {'mql': 'MR_Shift', 'py': 'MR_Shift', 'param': 'MR_Shift', 'type': 'int', 'default': 5, 'label': 'horizontal shift of MR MA in bars', 'sinput': False}, {'mql': 'LR_method', 'py': 'LR_method', 'param': 'LR_method', 'type': 'int', 'default': 0, 'label': 'LR MA smoothing type', 'sinput': False}, {'mql': 'LR_Period', 'py': 'LR_Period', 'param': 'LR_Period', 'type': 'uint', 'default': 25, 'label': 'LR MA smoothing period', 'sinput': False}, {'mql': 'LR_price_', 'py': 'LR_price_', 'param': 'LR_price_', 'type': 'int', 'default': 1, 'label': 'LR MA price constant', 'sinput': False}, {'mql': 'LR_Shift', 'py': 'LR_Shift', 'param': 'LR_Shift', 'type': 'int', 'default': 5, 'label': 'horizontal shift of LR MA in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SR_method = _input('SR_method', MODE_SMA)  # SR MA smoothing type
SR_Period = _input('SR_Period', 3)  # SR MA smoothing period
SR_price_ = _input('SR_price_', PRICE_CLOSE)  # SR MA price constant
SR_Shift = _input('SR_Shift', 3)  # horizontal shift of SR MA in bars
MR_method = _input('MR_method', MODE_SMA)  # MR MA smoothing type
MR_Period = _input('MR_Period', 7)  # MR MA smoothing period
MR_price_ = _input('MR_price_', PRICE_CLOSE)  # MR MA price constant
MR_Shift = _input('MR_Shift', 5)  # horizontal shift of MR MA in bars
LR_method = _input('LR_method', MODE_SMA)  # LR MA smoothing type
LR_Period = _input('LR_Period', 25)  # LR MA smoothing period
LR_price_ = _input('LR_price_', PRICE_CLOSE)  # LR MA price constant
LR_Shift = _input('LR_Shift', 5)  # horizontal shift of LR MA in bars
SR_Buffer = Arr(0, 0.0)
MR_Buffer = Arr(0, 0.0)
LR_Buffer = Arr(0, 0.0)
min_rates_total = 0
SR_Handle = 0
MR_Handle = 0
LR_Handle = 0

def OnInit():
    global LR_Handle, MR_Handle, SR_Handle, min_rates_total
    min_rates_total = _int(MathMax(MathMax(SR_Period, MR_Period), LR_Period))
    SR_Handle = iMA(None, PERIOD_CURRENT, SR_Period, 0, SR_method, SR_price_)
    if SR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA SR indicator')
    MR_Handle = iMA(None, PERIOD_CURRENT, MR_Period, 0, MR_method, MR_price_)
    if MR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA MR indicator')
    LR_Handle = iMA(None, PERIOD_CURRENT, LR_Period, 0, LR_method, LR_price_)
    if LR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA LR indicator')
    SetIndexBuffer(0, SR_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, SR_Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, SR_Period)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(SR_Buffer, True)
    SetIndexBuffer(1, MR_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, MR_Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, MR_Period)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(MR_Buffer, True)
    SetIndexBuffer(2, LR_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, LR_Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, LR_Period)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(LR_Buffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Displaced Moving Averages(', SR_Period, ',', MR_Period, ',', LR_Period, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((BarsCalculated(SR_Handle) < rates_total or BarsCalculated(MR_Handle) < rates_total) or BarsCalculated(LR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated + 1
    if CopyBuffer(SR_Handle, 0, 0, to_copy, SR_Buffer) <= 0:
        return 0
    if CopyBuffer(MR_Handle, 0, 0, to_copy, MR_Buffer) <= 0:
        return 0
    if CopyBuffer(LR_Handle, 0, 0, to_copy, LR_Buffer) <= 0:
        return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dma(_MQL5Indicator):
    name = 'dma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SR_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # SR MA smoothing type
        'SR_Period': 3,  # SR MA smoothing period
        'SR_price_': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # SR MA price constant
        'SR_Shift': 3,  # horizontal shift of SR MA in bars
        'MR_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MR MA smoothing type
        'MR_Period': 7,  # MR MA smoothing period
        'MR_price_': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MR MA price constant
        'MR_Shift': 5,  # horizontal shift of MR MA in bars
        'LR_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # LR MA smoothing type
        'LR_Period': 25,  # LR MA smoothing period
        'LR_price_': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # LR MA price constant
        'LR_Shift': 5,  # horizontal shift of LR MA in bars
    }

