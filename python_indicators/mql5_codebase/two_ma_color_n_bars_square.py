"""Two MA Color N Bars Square — converted from MQL5: MQL5 Indicators/Two MA Color N Bars Square/Two MA Color N Bars Square.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'separate', 'indicator_minimum': 1.0, 'indicator_maximum': 4.0, 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 12, 2: 12}, 'colors': {1: [3329434, 16711680, 255], 2: [3329434, 16711680, 255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'MA 0', 2: 'MA 1'}, 'levels': [], 'description': [], 'name': 'Two MA Color N Bars Square', 'source': 'MQL5 Indicators/Two MA Color N Bars Square/Two MA Color N Bars Square.mq5', 'folder': 'Two MA Color N Bars Square', 'inputs': [{'mql': 'Inp_MA_0_ma_period', 'py': 'Inp_MA_0_ma_period', 'param': 'Inp_MA_0_ma_period', 'type': 'int', 'default': 12, 'label': 'MA 0: averaging period', 'sinput': False}, {'mql': 'Inp_MA_0_ma_shift', 'py': 'Inp_MA_0_ma_shift', 'param': 'Inp_MA_0_ma_shift', 'type': 'int', 'default': 0, 'label': 'MA 0: horizontal shift', 'sinput': False}, {'mql': 'Inp_MA_0_ma_method', 'py': 'Inp_MA_0_ma_method', 'param': 'Inp_MA_0_ma_method', 'type': 'int', 'default': 0, 'label': 'MA 0: smoothing type', 'sinput': False}, {'mql': 'Inp_MA_0_applied_price', 'py': 'Inp_MA_0_applied_price', 'param': 'Inp_MA_0_applied_price', 'type': 'int', 'default': 1, 'label': 'MA 0: type of price', 'sinput': False}, {'mql': 'Inp_MA_0_trend_n_bars', 'py': 'Inp_MA_0_trend_n_bars', 'param': 'Inp_MA_0_trend_n_bars', 'type': 'uchar', 'default': 3, 'label': 'MA 0: trend N Bars', 'sinput': False}, {'mql': 'Inp_MA_1_ma_period', 'py': 'Inp_MA_1_ma_period', 'param': 'Inp_MA_1_ma_period', 'type': 'int', 'default': 36, 'label': 'MA 1: averaging period', 'sinput': False}, {'mql': 'Inp_MA_1_ma_shift', 'py': 'Inp_MA_1_ma_shift', 'param': 'Inp_MA_1_ma_shift', 'type': 'int', 'default': 0, 'label': 'MA 1: horizontal shift', 'sinput': False}, {'mql': 'Inp_MA_1_ma_method', 'py': 'Inp_MA_1_ma_method', 'param': 'Inp_MA_1_ma_method', 'type': 'int', 'default': 0, 'label': 'MA 1: smoothing type', 'sinput': False}, {'mql': 'Inp_MA_1_applied_price', 'py': 'Inp_MA_1_applied_price', 'param': 'Inp_MA_1_applied_price', 'type': 'int', 'default': 1, 'label': 'MA 1: type of price', 'sinput': False}, {'mql': 'Inp_MA_1_trend_n_bars', 'py': 'Inp_MA_1_trend_n_bars', 'param': 'Inp_MA_1_trend_n_bars', 'type': 'uchar', 'default': 5, 'label': 'MA 1: trend N Bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_MA_0_ma_period = _input('Inp_MA_0_ma_period', 12)  # MA 0: averaging period
Inp_MA_0_ma_shift = _input('Inp_MA_0_ma_shift', 0)  # MA 0: horizontal shift
Inp_MA_0_ma_method = _input('Inp_MA_0_ma_method', MODE_SMA)  # MA 0: smoothing type
Inp_MA_0_applied_price = _input('Inp_MA_0_applied_price', PRICE_CLOSE)  # MA 0: type of price
Inp_MA_0_trend_n_bars = _input('Inp_MA_0_trend_n_bars', 3)  # MA 0: trend N Bars
Inp_MA_1_ma_period = _input('Inp_MA_1_ma_period', 36)  # MA 1: averaging period
Inp_MA_1_ma_shift = _input('Inp_MA_1_ma_shift', 0)  # MA 1: horizontal shift
Inp_MA_1_ma_method = _input('Inp_MA_1_ma_method', MODE_SMA)  # MA 1: smoothing type
Inp_MA_1_applied_price = _input('Inp_MA_1_applied_price', PRICE_CLOSE)  # MA 1: type of price
Inp_MA_1_trend_n_bars = _input('Inp_MA_1_trend_n_bars', 5)  # MA 1: trend N Bars
MA_0_Buffer = Arr(0, 0.0)
MA_0_Colors = Arr(0, 0.0)
MA_1_Buffer = Arr(0, 0.0)
MA_1_Colors = Arr(0, 0.0)
iMA_0_Buffer = Arr(0, 0.0)
iMA_1_Buffer = Arr(0, 0.0)
handle_iMA_0 = 0  # variable for storing the handle of the iMA indicator
handle_iMA_1 = 0  # variable for storing the handle of the iMA indicator
bars_calculated = 0  # we will keep the number of values in the Moving Average indicator
m_min_bars = 0
m_init_error = False  # error on InInit

def OnInit():
    global handle_iMA_0, handle_iMA_1, m_init_error, m_min_bars
    SetIndexBuffer(0, MA_0_Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, MA_0_Colors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, MA_1_Buffer, INDICATOR_DATA)
    SetIndexBuffer(3, MA_1_Colors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, iMA_0_Buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, iMA_1_Buffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 3)
    PlotIndexSetInteger(0, PLOT_SHIFT, Inp_MA_0_ma_shift)
    PlotIndexSetInteger(0, PLOT_ARROW, 110)
    PlotIndexSetInteger(1, PLOT_ARROW, 110)
    handle_iMA_0 = iMA(Symbol(), Period(), Inp_MA_0_ma_period, Inp_MA_0_ma_shift, Inp_MA_0_ma_method, Inp_MA_0_applied_price)
    if handle_iMA_0 == INVALID_HANDLE:
        PrintFormat("Failed to create handle of the iMA indicator ('0') for the symbol %s/%s, error code %d", Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    handle_iMA_1 = iMA(Symbol(), Period(), Inp_MA_1_ma_period, Inp_MA_1_ma_shift, Inp_MA_1_ma_method, Inp_MA_1_applied_price)
    if handle_iMA_1 == INVALID_HANDLE:
        PrintFormat("Failed to create handle of the iMA indicator ('1') for the symbol %s/%s, error code %d", Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    plot_0_label = StringFormat('MA 0(%d, %d, %s, %s, %d)', Inp_MA_0_ma_period, Inp_MA_0_ma_shift, StringSubstr(EnumToString(Inp_MA_0_ma_method, 'ENUM_MA_METHOD'), 5, -1), StringSubstr(EnumToString(Inp_MA_0_applied_price, 'ENUM_APPLIED_PRICE'), 6, -1), Inp_MA_0_trend_n_bars)
    plot_1_label = StringFormat('MA 1(%d, %d, %s, %s, %d)', Inp_MA_1_ma_period, Inp_MA_1_ma_shift, StringSubstr(EnumToString(Inp_MA_1_ma_method, 'ENUM_MA_METHOD'), 5, -1), StringSubstr(EnumToString(Inp_MA_1_applied_price, 'ENUM_APPLIED_PRICE'), 6, -1), Inp_MA_1_trend_n_bars)
    PlotIndexSetString(0, PLOT_LABEL, plot_0_label)
    PlotIndexSetString(1, PLOT_LABEL, plot_1_label)
    m_min_bars = Inp_MA_0_ma_period + Inp_MA_0_ma_shift + Inp_MA_0_trend_n_bars
    if m_min_bars < (Inp_MA_1_ma_period + Inp_MA_1_ma_shift + Inp_MA_1_trend_n_bars):
        m_min_bars = Inp_MA_1_ma_period + Inp_MA_1_ma_shift + Inp_MA_1_trend_n_bars
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    if m_init_error:
        return 0
    if rates_total <= m_min_bars:
        return 0
    values_to_copy = 0
    calculated_0 = BarsCalculated(handle_iMA_0)
    if calculated_0 <= 0:
        PrintFormat('BarsCalculated(handle_iMA_0) returned %d, error code %d', calculated_0, GetLastError())
        return 0
    calculated_1 = BarsCalculated(handle_iMA_1)
    if calculated_1 <= 0:
        PrintFormat('BarsCalculated(handle_iMA_1) returned %d, error code %d', calculated_1, GetLastError())
        return 0
    if calculated_0 != calculated_1:
        PrintFormat('BarsCalculated(handle_iMA_0) returned %d, BarsCalculated(handle_iMA_1) returned %d', calculated_0, calculated_1)
        return 0
    calculated = calculated_0
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBuffer(iMA_0_Buffer, Inp_MA_0_ma_shift, handle_iMA_0, values_to_copy):
        return 0
    if not FillArrayFromBuffer(iMA_1_Buffer, Inp_MA_1_ma_shift, handle_iMA_1, values_to_copy):
        return 0
    bars_calculated = calculated
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = m_min_bars
        for i in range(0, limit):
            MA_0_Colors[i] = 0.0
            MA_1_Colors[i] = 0.0
    for i in range(limit, rates_total):
        MA_0_Buffer[i] = 1.0
        MA_1_Buffer[i] = 2.0
        trend_0 = 0
        for j in range(i - Inp_MA_0_trend_n_bars, i):
            if iMA_0_Buffer[j] < iMA_0_Buffer[j + 1]:
                trend_0 += 1
            else:
                trend_0 -= 1
        if trend_0 == Inp_MA_0_trend_n_bars:
            MA_0_Colors[i] = 1.0
        elif (-trend_0) == Inp_MA_0_trend_n_bars:
            MA_0_Colors[i] = 2.0
        else:
            MA_0_Colors[i] = 0.0
        trend_1 = 0
        for j in range(i - Inp_MA_1_trend_n_bars, i):
            if iMA_1_Buffer[j] < iMA_1_Buffer[j + 1]:
                trend_1 += 1
            else:
                trend_1 -= 1
        if trend_1 == Inp_MA_1_trend_n_bars:
            MA_1_Colors[i] = 1.0
        elif (-trend_1) == Inp_MA_1_trend_n_bars:
            MA_1_Colors[i] = 2.0
        else:
            MA_1_Colors[i] = 0.0
    return rates_total

def FillArrayFromBuffer(values, shift, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, -shift, amount, values) < 0:
        PrintFormat('Failed to copy data from the iMA indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    if handle_iMA_0 != INVALID_HANDLE:
        IndicatorRelease(handle_iMA_0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TwoMAColorNBarsSquare(_MQL5Indicator):
    name = 'Two MA Color N Bars Square'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_MA_0_ma_period': 12,  # MA 0: averaging period
        'Inp_MA_0_ma_shift': 0,  # MA 0: horizontal shift
        'Inp_MA_0_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA 0: smoothing type
        'Inp_MA_0_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA 0: type of price
        'Inp_MA_0_trend_n_bars': 3,  # MA 0: trend N Bars
        'Inp_MA_1_ma_period': 36,  # MA 1: averaging period
        'Inp_MA_1_ma_shift': 0,  # MA 1: horizontal shift
        'Inp_MA_1_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA 1: smoothing type
        'Inp_MA_1_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA 1: type of price
        'Inp_MA_1_trend_n_bars': 5,  # MA 1: trend N Bars
    }
    y_range = (1.0, 4.0)

