"""RSI_MAonRSI_Filling — converted from MQL5: MQL5 Indicators/RSI_MAonRSI_Filling/RSI_MAonRSI_Filling.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 7}, 'colors': {1: [13828244], 2: [65535], 3: [12500735, 16760510]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'RSI', 2: 'MAonRSI', 3: 'Filling'}, 'levels': [], 'description': [], 'name': 'RSI_MAonRSI_Filling', 'source': 'MQL5 Indicators/RSI_MAonRSI_Filling/RSI_MAonRSI_Filling.mq5', 'folder': 'RSI_MAonRSI_Filling', 'inputs': [{'mql': 'Inp_RSI_ma_period', 'py': 'Inp_RSI_ma_period', 'param': 'Inp_RSI_ma_period', 'type': 'int', 'default': 14, 'label': 'RSI: averaging period', 'sinput': False}, {'mql': 'Inp_RSI_applied_price', 'py': 'Inp_RSI_applied_price', 'param': 'Inp_RSI_applied_price', 'type': 'int', 'default': 1, 'label': 'RSI: type of price', 'sinput': False}, {'mql': 'Inp_RSI_Level_Color', 'py': 'Inp_RSI_Level_Color', 'param': None, 'type': 'color', 'default': 6908265, 'label': 'RSI: Color line Levels', 'sinput': False}, {'mql': 'Inp_RSI_Level_Down', 'py': 'Inp_RSI_Level_Down', 'param': 'Inp_RSI_Level_Down', 'type': 'double', 'default': 20.0, 'label': 'RSI: Level Down', 'sinput': False}, {'mql': 'Inp_RSI_Level_Middle', 'py': 'Inp_RSI_Level_Middle', 'param': 'Inp_RSI_Level_Middle', 'type': 'double', 'default': 50.0, 'label': 'RSI: Level Middle', 'sinput': False}, {'mql': 'Inp_RSI_Level_Up', 'py': 'Inp_RSI_Level_Up', 'param': 'Inp_RSI_Level_Up', 'type': 'double', 'default': 80.0, 'label': 'RSI: Level Up', 'sinput': False}, {'mql': 'Inp_MA_ma_period', 'py': 'Inp_MA_ma_period', 'param': 'Inp_MA_ma_period', 'type': 'int', 'default': 21, 'label': 'MA: averaging period', 'sinput': False}, {'mql': 'Inp_MA_ma_method', 'py': 'Inp_MA_ma_method', 'param': 'Inp_MA_ma_method', 'type': 'int', 'default': 0, 'label': 'MA: smoothing type', 'sinput': False}, {'mql': 'Inp_MA_applied_price', 'py': 'Inp_MA_applied_price', 'param': 'Inp_MA_applied_price', 'type': 'int', 'default': 1, 'label': 'MA: type of price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_RSI_ma_period = _input('Inp_RSI_ma_period', 14)  # RSI: averaging period
Inp_RSI_applied_price = _input('Inp_RSI_applied_price', PRICE_CLOSE)  # RSI: type of price
Inp_RSI_Level_Color = _input('Inp_RSI_Level_Color', clrDimGray)  # RSI: Color line Levels
Inp_RSI_Level_Down = _input('Inp_RSI_Level_Down', 20.0)  # RSI: Level Down
Inp_RSI_Level_Middle = _input('Inp_RSI_Level_Middle', 50.0)  # RSI: Level Middle
Inp_RSI_Level_Up = _input('Inp_RSI_Level_Up', 80.0)  # RSI: Level Up
Inp_MA_ma_period = _input('Inp_MA_ma_period', 21)  # MA: averaging period
Inp_MA_ma_method = _input('Inp_MA_ma_method', MODE_SMA)  # MA: smoothing type
Inp_MA_applied_price = _input('Inp_MA_applied_price', PRICE_CLOSE)  # MA: type of price
RSIBuffer = Arr(0, 0.0)
MAonRSIBuffer = Arr(0, 0.0)
FillingBuffer1 = Arr(0, 0.0)
FillingBuffer2 = Arr(0, 0.0)
handle_iRSI = 0  # variable for storing the handle of the iRSI indicator
handle_iMAOnRSI = 0  # variable for storing the handle of the iRSI indicator
bars_calculated = 0  # we will keep the number of values in the Relative Strength Index indicator
m_init_error = False  # error on InInit

def OnInit():
    global handle_iMAOnRSI, handle_iRSI, m_init_error
    SetIndexBuffer(0, RSIBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, MAonRSIBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, FillingBuffer1, INDICATOR_DATA)
    SetIndexBuffer(3, FillingBuffer2, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, Inp_RSI_Level_Color)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, Inp_RSI_Level_Color)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, Inp_RSI_Level_Color)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASH)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASH)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, Inp_RSI_Level_Down)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, Inp_RSI_Level_Middle)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, Inp_RSI_Level_Up)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 100)
    handle_iRSI = iRSI(Symbol(), Period(), Inp_RSI_ma_period, Inp_RSI_applied_price)
    if handle_iRSI == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iRSI indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    handle_iMAOnRSI = iMA(Symbol(), Period(), Inp_MA_ma_period, 0, Inp_MA_ma_method, handle_iRSI)
    if handle_iMAOnRSI == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMA indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    if m_init_error:
        return 0
    values_to_copy = 0
    calculated_rsi = BarsCalculated(handle_iRSI)
    if calculated_rsi <= 0:
        PrintFormat('BarsCalculated(handle_iRSI) returned %d, error code %d', calculated_rsi, GetLastError())
        return 0
    calculated_ma_on_rsi = BarsCalculated(handle_iMAOnRSI)
    if calculated_ma_on_rsi <= 0:
        PrintFormat('BarsCalculated(handle_iMAOnRSI) returned %d, error code %d', calculated_ma_on_rsi, GetLastError())
        return 0
    if calculated_rsi != calculated_ma_on_rsi:
        PrintFormat('BarsCalculated(handle_iRSI) returned %d, BarsCalculated(handle_iMAOnRSI) returned %d', calculated_ma_on_rsi, GetLastError())
        return 0
    calculated = calculated_rsi
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBuffer_1(RSIBuffer, handle_iRSI, values_to_copy):
        return 0
    if not FillArrayFromBuffer_2(MAonRSIBuffer, 0, handle_iMAOnRSI, values_to_copy):
        return 0
    bars_calculated = calculated
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 0
    for i in range(0, rates_total):
        FillingBuffer1[i] = RSIBuffer[i]
        FillingBuffer2[i] = MAonRSIBuffer[i]
    return rates_total

def FillArrayFromBuffer_1(rsi_buffer, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, 0, amount, rsi_buffer) < 0:
        PrintFormat('Failed to copy data from the iRSI indicator, error code %d', GetLastError())
        return False
    return True

def FillArrayFromBuffer_2(values, shift, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, -shift, amount, values) < 0:
        PrintFormat('Failed to copy data from the iMA indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    if handle_iRSI != INVALID_HANDLE:
        IndicatorRelease(handle_iRSI)
    if handle_iMAOnRSI != INVALID_HANDLE:
        IndicatorRelease(handle_iMAOnRSI)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSIMAonRSIFilling(_MQL5Indicator):
    name = 'RSI_MAonRSI_Filling'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_RSI_ma_period': 14,  # RSI: averaging period
        'Inp_RSI_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # RSI: type of price
        'Inp_RSI_Level_Down': 20.0,  # RSI: Level Down
        'Inp_RSI_Level_Middle': 50.0,  # RSI: Level Middle
        'Inp_RSI_Level_Up': 80.0,  # RSI: Level Up
        'Inp_MA_ma_period': 21,  # MA: averaging period
        'Inp_MA_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA: smoothing type
        'Inp_MA_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA: type of price
    }

