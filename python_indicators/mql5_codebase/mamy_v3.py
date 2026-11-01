"""MAMy v3 — converted from MQL5: MQL5 Indicators/MAMy v3/MAMy v3.mq5

Copyright: Copyright © 2006, Victor Chebotariov; Link: http://www.chebotariov.com/; Version: 1.001

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Victor Chebotariov', 'link': 'http://www.chebotariov.com/', 'version': '1.001', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [64636], 2: [255]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Open (Green)', 2: 'Close (Red)'}, 'levels': [], 'description': [], 'name': 'MAMy v3', 'source': 'MQL5 Indicators/MAMy v3/MAMy v3.mq5', 'folder': 'MAMy v3', 'inputs': [{'mql': 'Inp_MA_ma_period', 'py': 'Inp_MA_ma_period', 'param': 'Inp_MA_ma_period', 'type': 'int', 'default': 3, 'label': 'MA: averaging period', 'sinput': False}, {'mql': 'Inp_MA_ma_method', 'py': 'Inp_MA_ma_method', 'param': 'Inp_MA_ma_method', 'type': 'int', 'default': 3, 'label': 'MA: smoothing type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_MA_ma_period = _input('Inp_MA_ma_period', 3)  # MA: averaging period
Inp_MA_ma_method = _input('Inp_MA_ma_method', MODE_LWMA)  # MA: smoothing type
MAMyOpenBuffer = Arr(0, 0.0)
MAMyCloseBuffer = Arr(0, 0.0)
iMA_CLOSE = Arr(0, 0.0)
iMA_OPEN = Arr(0, 0.0)
iMA_WEIGHTED = Arr(0, 0.0)
handle_iMA_PRICE_CLOSE = 0
handle_iMA_PRICE_OPEN = 0
handle_iMA_PRICE_WEIGHTED = 0
bars_calculated = 0

def OnInit():
    global handle_iMA_PRICE_CLOSE, handle_iMA_PRICE_OPEN, handle_iMA_PRICE_WEIGHTED
    SetIndexBuffer(0, MAMyOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, MAMyCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, iMA_CLOSE, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, iMA_OPEN, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, iMA_WEIGHTED, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_SHIFT, 0)
    PlotIndexSetInteger(1, PLOT_SHIFT, 0)
    handle_iMA_PRICE_CLOSE = iMA(Symbol(), Period(), Inp_MA_ma_period, 0, Inp_MA_ma_method, PRICE_CLOSE)
    if handle_iMA_PRICE_CLOSE == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMA indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        return INIT_FAILED
    handle_iMA_PRICE_OPEN = iMA(Symbol(), Period(), Inp_MA_ma_period, 0, Inp_MA_ma_method, PRICE_OPEN)
    if handle_iMA_PRICE_OPEN == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMA indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        return INIT_FAILED
    handle_iMA_PRICE_WEIGHTED = iMA(Symbol(), Period(), Inp_MA_ma_period, 0, Inp_MA_ma_method, PRICE_WEIGHTED)
    if handle_iMA_PRICE_WEIGHTED == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMA indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    values_to_copy = 0
    calculated_PRICE_CLOSE = BarsCalculated(handle_iMA_PRICE_CLOSE)
    if calculated_PRICE_CLOSE <= 0:
        PrintFormat('BarsCalculated() returned %d, error code %d', calculated_PRICE_CLOSE, GetLastError())
        return 0
    if (prev_calculated == 0 or calculated_PRICE_CLOSE != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated_PRICE_CLOSE > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated_PRICE_CLOSE
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBuffer(iMA_CLOSE, 0, handle_iMA_PRICE_CLOSE, values_to_copy):
        return 0
    if not FillArrayFromBuffer(iMA_OPEN, 0, handle_iMA_PRICE_OPEN, values_to_copy):
        return 0
    if not FillArrayFromBuffer(iMA_WEIGHTED, 0, handle_iMA_PRICE_WEIGHTED, values_to_copy):
        return 0
    bars_calculated = calculated_PRICE_CLOSE
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 1
        MAMyOpenBuffer[0] = 0.0
        MAMyCloseBuffer[0] = 0.0
    for i in range(limit, rates_total):
        MAMyCloseBuffer[i] = iMA_CLOSE[i] - iMA_WEIGHTED[i]
        if (((((iMA_CLOSE[i] < iMA_CLOSE[i - 1] and iMA_WEIGHTED[i] < iMA_WEIGHTED[i - 1]) and iMA_CLOSE[i] < iMA_WEIGHTED[i]) and iMA_WEIGHTED[i] < iMA_OPEN[i]) and iMA_WEIGHTED[i - 1] < iMA_OPEN[i - 1]) and MAMyCloseBuffer[i] <= MAMyCloseBuffer[i - 1]) or (((((iMA_CLOSE[i] > iMA_CLOSE[i - 1] and iMA_WEIGHTED[i] > iMA_WEIGHTED[i - 1]) and iMA_CLOSE[i] > iMA_WEIGHTED[i]) and iMA_WEIGHTED[i] > iMA_OPEN[i]) and iMA_WEIGHTED[i - 1] > iMA_OPEN[i - 1]) and MAMyCloseBuffer[i] >= MAMyCloseBuffer[i - 1]):
            MAMyOpenBuffer[i] = iMA_WEIGHTED[i] - iMA_OPEN[i] + (iMA_CLOSE[i] - iMA_WEIGHTED[i])
        else:
            MAMyOpenBuffer[i] = 0.0
        if ((MAMyOpenBuffer[i] >= 0.0 and MAMyOpenBuffer[i] > MAMyOpenBuffer[i - 1]) and MAMyCloseBuffer[i] < 0.0) and MAMyCloseBuffer[i - 1] >= 0.0:
            MAMyCloseBuffer[i] = 0.0
        else:
            MAMyCloseBuffer[i] = iMA_CLOSE[i] - iMA_WEIGHTED[i]
    return rates_total

def FillArrayFromBuffer(values, shift, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, -shift, amount, values) < 0:
        PrintFormat('Failed to copy data from the iMA indicator, error code %d', GetLastError())
        return False
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MAMyV3(_MQL5Indicator):
    name = 'MAMy v3'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_MA_ma_period': 3,  # MA: averaging period
        'Inp_MA_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=3),  # MA: smoothing type
    }

