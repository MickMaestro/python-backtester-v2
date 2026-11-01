"""Crossover on the current bar — converted from MQL5: MQL5 Indicators/Crossover on the current bar/Crossover on the current bar.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 12}, 'colors': {1: [16711680, 255, 8421504]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Crossover'}, 'levels': [], 'description': [], 'name': 'Crossover on the current bar', 'source': 'MQL5 Indicators/Crossover on the current bar/Crossover on the current bar.mq5', 'folder': 'Crossover on the current bar', 'inputs': [{'mql': 'Inp_MA_Fast_ma_period', 'py': 'Inp_MA_Fast_ma_period', 'param': 'Inp_MA_Fast_ma_period', 'type': 'int', 'default': 12, 'label': 'MA Fast: averaging period', 'sinput': False}, {'mql': 'Inp_MA_Fast_ma_shift', 'py': 'Inp_MA_Fast_ma_shift', 'param': 'Inp_MA_Fast_ma_shift', 'type': 'int', 'default': 0, 'label': 'MA Fast: horizontal shift', 'sinput': False}, {'mql': 'Inp_MA_Fast_ma_method', 'py': 'Inp_MA_Fast_ma_method', 'param': 'Inp_MA_Fast_ma_method', 'type': 'int', 'default': 0, 'label': 'MA Fast: smoothing type', 'sinput': False}, {'mql': 'Inp_MA_Fast_applied_price', 'py': 'Inp_MA_Fast_applied_price', 'param': 'Inp_MA_Fast_applied_price', 'type': 'int', 'default': 1, 'label': 'MA Fast: type of price', 'sinput': False}, {'mql': 'Inp_MA_Slow_ma_period', 'py': 'Inp_MA_Slow_ma_period', 'param': 'Inp_MA_Slow_ma_period', 'type': 'int', 'default': 26, 'label': 'MA Slow: averaging period', 'sinput': False}, {'mql': 'Inp_MA_Slow_ma_shift', 'py': 'Inp_MA_Slow_ma_shift', 'param': 'Inp_MA_Slow_ma_shift', 'type': 'int', 'default': 0, 'label': 'MA Slow: horizontal shift', 'sinput': False}, {'mql': 'Inp_MA_Slow_ma_method', 'py': 'Inp_MA_Slow_ma_method', 'param': 'Inp_MA_Slow_ma_method', 'type': 'int', 'default': 0, 'label': 'MA Slow: smoothing type', 'sinput': False}, {'mql': 'Inp_MA_Slow_applied_price', 'py': 'Inp_MA_Slow_applied_price', 'param': 'Inp_MA_Slow_applied_price', 'type': 'int', 'default': 1, 'label': 'MA Slow: type of price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_MA_Fast_ma_period = _input('Inp_MA_Fast_ma_period', 12)  # MA Fast: averaging period
Inp_MA_Fast_ma_shift = _input('Inp_MA_Fast_ma_shift', 0)  # MA Fast: horizontal shift
Inp_MA_Fast_ma_method = _input('Inp_MA_Fast_ma_method', MODE_SMA)  # MA Fast: smoothing type
Inp_MA_Fast_applied_price = _input('Inp_MA_Fast_applied_price', PRICE_CLOSE)  # MA Fast: type of price
Inp_MA_Slow_ma_period = _input('Inp_MA_Slow_ma_period', 26)  # MA Slow: averaging period
Inp_MA_Slow_ma_shift = _input('Inp_MA_Slow_ma_shift', 0)  # MA Slow: horizontal shift
Inp_MA_Slow_ma_method = _input('Inp_MA_Slow_ma_method', MODE_SMA)  # MA Slow: smoothing type
Inp_MA_Slow_applied_price = _input('Inp_MA_Slow_applied_price', PRICE_CLOSE)  # MA Slow: type of price
CrossoverBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
iMAFastBuffer = Arr(0, 0.0)
iMASlowBuffer = Arr(0, 0.0)
handle_iMA_Fast = 0  # variable for storing the handle of the iMA indicator
handle_iMA_Slow = 0  # variable for storing the handle of the iMA indicator
m_start = 0
bars_calculated = 0  # we will keep the number of values in the Moving Average indicator
m_init_error = False  # error on InInit

def OnInit():
    global handle_iMA_Fast, handle_iMA_Slow, m_init_error, m_start
    SetIndexBuffer(0, CrossoverBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, iMAFastBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, iMASlowBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    handle_iMA_Fast = iMA(Symbol(), Period(), Inp_MA_Fast_ma_period, Inp_MA_Fast_ma_shift, Inp_MA_Fast_ma_method, Inp_MA_Fast_applied_price)
    if handle_iMA_Fast == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMA indicator ("Fast") for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    handle_iMA_Slow = iMA(Symbol(), Period(), Inp_MA_Slow_ma_period, Inp_MA_Slow_ma_shift, Inp_MA_Slow_ma_method, Inp_MA_Slow_applied_price)
    if handle_iMA_Slow == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMA indicator ("Slow") for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    m_start = Inp_MA_Fast_ma_period + Inp_MA_Fast_ma_shift
    if m_start < (Inp_MA_Slow_ma_period + Inp_MA_Slow_ma_shift):
        m_start = Inp_MA_Slow_ma_period + Inp_MA_Slow_ma_shift
    m_start += 1
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    if rates_total < m_start or m_init_error:
        return 0
    values_to_copy = 0
    calculated_fast = BarsCalculated(handle_iMA_Fast)
    if calculated_fast <= 0:
        PrintFormat('BarsCalculated(handle_iMA_Fast) returned %d, error code %d', calculated_fast, GetLastError())
        return 0
    calculated_slow = BarsCalculated(handle_iMA_Slow)
    if calculated_slow <= 0:
        PrintFormat('BarsCalculated(handle_iMA_Slow) returned %d, error code %d', calculated_slow, GetLastError())
        return 0
    if calculated_fast != calculated_slow:
        return 0
    calculated = calculated_fast
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBuffer(iMAFastBuffer, Inp_MA_Fast_ma_shift, handle_iMA_Fast, values_to_copy):
        return 0
    if not FillArrayFromBuffer(iMASlowBuffer, Inp_MA_Slow_ma_shift, handle_iMA_Slow, values_to_copy):
        return 0
    bars_calculated = calculated
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = m_start
    for i in range(limit, rates_total):
        CrossoverBuffer[i] = 0.0
        ColorBuffer[i] = 2.0
        if iMAFastBuffer[i - 1] < iMASlowBuffer[i - 1] and iMAFastBuffer[i] > iMASlowBuffer[i]:
            CrossoverBuffer[i] = 1.0
            ColorBuffer[i] = 0.0
        elif iMAFastBuffer[i - 1] > iMASlowBuffer[i - 1] and iMAFastBuffer[i] < iMASlowBuffer[i]:
            CrossoverBuffer[i] = 1.0
            ColorBuffer[i] = 1.0
    return rates_total

def FillArrayFromBuffer(values, shift, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, -shift, amount, values) < 0:
        PrintFormat('Failed to copy data from the iMA indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    if handle_iMA_Fast != INVALID_HANDLE:
        IndicatorRelease(handle_iMA_Fast)
    if handle_iMA_Slow != INVALID_HANDLE:
        IndicatorRelease(handle_iMA_Slow)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CrossoverOnTheCurrentBar(_MQL5Indicator):
    name = 'Crossover on the current bar'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_MA_Fast_ma_period': 12,  # MA Fast: averaging period
        'Inp_MA_Fast_ma_shift': 0,  # MA Fast: horizontal shift
        'Inp_MA_Fast_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA Fast: smoothing type
        'Inp_MA_Fast_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA Fast: type of price
        'Inp_MA_Slow_ma_period': 26,  # MA Slow: averaging period
        'Inp_MA_Slow_ma_shift': 0,  # MA Slow: horizontal shift
        'Inp_MA_Slow_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA Slow: smoothing type
        'Inp_MA_Slow_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA Slow: type of price
    }

