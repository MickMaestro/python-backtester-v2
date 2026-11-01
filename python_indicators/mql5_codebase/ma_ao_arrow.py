"""MA AO Arrow — converted from MQL5: MQL5 Indicators/MA AO Arrow/MA AO Arrow.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [15570276], 2: [8036607]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'BUY', 2: 'SELL'}, 'levels': [], 'description': [], 'name': 'MA AO Arrow', 'source': 'MQL5 Indicators/MA AO Arrow/MA AO Arrow.mq5', 'folder': 'MA AO Arrow', 'inputs': [{'mql': 'Inp_MA_ma_period', 'py': 'Inp_MA_ma_period', 'param': 'Inp_MA_ma_period', 'type': 'int', 'default': 36, 'label': 'MA: averaging period', 'sinput': False}, {'mql': 'Inp_MA_ma_shift', 'py': 'Inp_MA_ma_shift', 'param': 'Inp_MA_ma_shift', 'type': 'int', 'default': 0, 'label': 'MA: horizontal shift', 'sinput': False}, {'mql': 'Inp_MA_ma_method', 'py': 'Inp_MA_ma_method', 'param': 'Inp_MA_ma_method', 'type': 'int', 'default': 0, 'label': 'MA: smoothing type', 'sinput': False}, {'mql': 'Inp_MA_applied_price', 'py': 'Inp_MA_applied_price', 'param': 'Inp_MA_applied_price', 'type': 'int', 'default': 1, 'label': 'MA: type of price', 'sinput': False}, {'mql': 'Inp_BUY_Arrow_Code', 'py': 'Inp_BUY_Arrow_Code', 'param': 'Inp_BUY_Arrow_Code', 'type': 'uchar', 'default': 241, 'label': "Arrow 'BUY': code (font Wingdings)", 'sinput': False}, {'mql': 'Inp_BUY_Arrow_Shift', 'py': 'Inp_BUY_Arrow_Shift', 'param': 'Inp_BUY_Arrow_Shift', 'type': 'int', 'default': 10, 'label': "Arrow 'BUY': vertical shift in pixel", 'sinput': False}, {'mql': 'Inp_SELL_Arrow_Code', 'py': 'Inp_SELL_Arrow_Code', 'param': 'Inp_SELL_Arrow_Code', 'type': 'uchar', 'default': 242, 'label': "Arrow 'SELL': code (font Wingdings)", 'sinput': False}, {'mql': 'Inp_SELL_Arrow_Shift', 'py': 'Inp_SELL_Arrow_Shift', 'param': 'Inp_SELL_Arrow_Shift', 'type': 'int', 'default': 10, 'label': "Arrow 'SELL': vertical shift in pixel", 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_MA_ma_period = _input('Inp_MA_ma_period', 36)  # MA: averaging period
Inp_MA_ma_shift = _input('Inp_MA_ma_shift', 0)  # MA: horizontal shift
Inp_MA_ma_method = _input('Inp_MA_ma_method', MODE_SMA)  # MA: smoothing type
Inp_MA_applied_price = _input('Inp_MA_applied_price', PRICE_CLOSE)  # MA: type of price
Inp_BUY_Arrow_Code = _input('Inp_BUY_Arrow_Code', 241)  # Arrow 'BUY': code (font Wingdings)
Inp_BUY_Arrow_Shift = _input('Inp_BUY_Arrow_Shift', 10)  # Arrow 'BUY': vertical shift in pixel
Inp_SELL_Arrow_Code = _input('Inp_SELL_Arrow_Code', 242)  # Arrow 'SELL': code (font Wingdings)
Inp_SELL_Arrow_Shift = _input('Inp_SELL_Arrow_Shift', 10)  # Arrow 'SELL': vertical shift in pixel
BUYBuffer = Arr(0, 0.0)
SELLBuffer = Arr(0, 0.0)
iMABuffer = Arr(0, 0.0)
iAOBuffer = Arr(0, 0.0)
handle_iMA = 0  # variable for storing the handle of the iMA indicator
handle_iAO = 0  # variable for storing the handle of the iAO indicator
bars_calculated = 0  # we will keep the number of values in the Moving Averages Convergence/Divergence indicator
m_init_error = False  # error on InInit

def OnInit():
    global handle_iAO, handle_iMA, m_init_error
    SetIndexBuffer(0, BUYBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SELLBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, iMABuffer, INDICATOR_DATA)
    SetIndexBuffer(3, iAOBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, Inp_BUY_Arrow_Code)
    PlotIndexSetInteger(1, PLOT_ARROW, Inp_SELL_Arrow_Code)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, Inp_BUY_Arrow_Shift)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, -Inp_SELL_Arrow_Shift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    handle_iMA = iMA(Symbol(), Period(), Inp_MA_ma_period, Inp_MA_ma_shift, Inp_MA_ma_method, Inp_MA_applied_price)
    if handle_iMA == INVALID_HANDLE:
        PrintFormat("Failed to create handle of the iMA indicator ('Fast') for the symbol %s/%s, error code %d", Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    handle_iAO = iAO(Symbol(), Period())
    if handle_iAO == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iAO indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    if m_init_error:
        return 0
    if rates_total < 4:
        return 0
    values_to_copy = 0
    calculated_ma = BarsCalculated(handle_iMA)
    if calculated_ma <= 0:
        PrintFormat('BarsCalculated(handle_iMA) returned %d, error code %d', calculated_ma, GetLastError())
        return 0
    calculated_ao = BarsCalculated(handle_iAO)
    if calculated_ao <= 0:
        PrintFormat('BarsCalculated(handle_iMA_Medium) returned %d, error code %d', calculated_ao, GetLastError())
        return 0
    if calculated_ma != calculated_ao:
        PrintFormat('BarsCalculated(handle_iMA) returned %d, BarsCalculated(handle_iAO) returned %d', calculated_ma, calculated_ao)
        return 0
    calculated = calculated_ma
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBuffer(iMABuffer, Inp_MA_ma_shift, handle_iMA, values_to_copy):
        return 0
    if not FillArraysFromBuffer(iAOBuffer, handle_iAO, values_to_copy):
        return 0
    bars_calculated = calculated
    limit = rates_total - values_to_copy
    if limit < 3:
        limit = 3
    for i in range(limit, rates_total):
        BUYBuffer[i] = 0.0
        SELLBuffer[i] = 0.0
        if (iAOBuffer[i - 1] > 0.0 and iAOBuffer[i - 2] > 0.0) and iAOBuffer[i - 3] > 0.0:
            if iAOBuffer[i - 1] > iAOBuffer[i - 2] and iAOBuffer[i - 2] < iAOBuffer[i - 3]:
                if low[i] > iMABuffer[i]:
                    BUYBuffer[i] = low[i]
                    continue
        if (iAOBuffer[i - 1] < 0.0 and iAOBuffer[i - 2] < 0.0) and iAOBuffer[i - 3] < 0.0:
            if iAOBuffer[i - 1] < iAOBuffer[i - 2] and iAOBuffer[i - 2] > iAOBuffer[i - 3]:
                if high[i] < iMABuffer[i]:
                    SELLBuffer[i] = high[i]
                    continue
    return rates_total

def FillArrayFromBuffer(values, shift, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, -shift, amount, values) < 0:
        PrintFormat('Failed to copy data from the iMA indicator, error code %d', GetLastError())
        return False
    return True

def FillArraysFromBuffer(values, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, 0, amount, values) < 0:
        PrintFormat('Failed to copy data from the iAO indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    if handle_iMA != INVALID_HANDLE:
        IndicatorRelease(handle_iMA)
    if handle_iAO != INVALID_HANDLE:
        IndicatorRelease(handle_iAO)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MAAOArrow(_MQL5Indicator):
    name = 'MA AO Arrow'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_MA_ma_period': 36,  # MA: averaging period
        'Inp_MA_ma_shift': 0,  # MA: horizontal shift
        'Inp_MA_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA: smoothing type
        'Inp_MA_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA: type of price
        'Inp_BUY_Arrow_Code': 241,  # Arrow 'BUY': code (font Wingdings)
        'Inp_BUY_Arrow_Shift': 10,  # Arrow 'BUY': vertical shift in pixel
        'Inp_SELL_Arrow_Code': 242,  # Arrow 'SELL': code (font Wingdings)
        'Inp_SELL_Arrow_Shift': 10,  # Arrow 'SELL': vertical shift in pixel
    }

