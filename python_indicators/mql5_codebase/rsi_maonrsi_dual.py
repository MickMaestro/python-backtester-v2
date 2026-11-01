"""RSI_MAonRSI_Dual — converted from MQL5: MQL5 Indicators/RSI_MAonRSI_Dual/RSI_MAonRSI_Dual.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16748574], 2: [65280]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'RSI Fast', 2: 'RSI Slow'}, 'levels': [], 'description': [], 'name': 'RSI_MAonRSI_Dual', 'source': 'MQL5 Indicators/RSI_MAonRSI_Dual/RSI_MAonRSI_Dual.mq5', 'folder': 'RSI_MAonRSI_Dual', 'inputs': [{'mql': 'Inp_RSI_Fast_ma_period', 'py': 'Inp_RSI_Fast_ma_period', 'param': 'Inp_RSI_Fast_ma_period', 'type': 'int', 'default': 5, 'label': 'RSI Fast: averaging period', 'sinput': False}, {'mql': 'Inp_RSI_Slow_ma_period', 'py': 'Inp_RSI_Slow_ma_period', 'param': 'Inp_RSI_Slow_ma_period', 'type': 'int', 'default': 15, 'label': 'RSI Slow: averaging period', 'sinput': False}, {'mql': 'Inp_RSI_applied_price', 'py': 'Inp_RSI_applied_price', 'param': 'Inp_RSI_applied_price', 'type': 'int', 'default': 1, 'label': 'RSI: type of price', 'sinput': False}, {'mql': 'Inp_RSI_Level_Color', 'py': 'Inp_RSI_Level_Color', 'param': None, 'type': 'color', 'default': 6908265, 'label': 'RSI: Color line Levels', 'sinput': False}, {'mql': 'Inp_RSI_Level_Down', 'py': 'Inp_RSI_Level_Down', 'param': 'Inp_RSI_Level_Down', 'type': 'double', 'default': 25.0, 'label': 'RSI: Level Down', 'sinput': False}, {'mql': 'Inp_RSI_Level_Middle', 'py': 'Inp_RSI_Level_Middle', 'param': 'Inp_RSI_Level_Middle', 'type': 'double', 'default': 50.0, 'label': 'RSI: Level Middle', 'sinput': False}, {'mql': 'Inp_RSI_Level_Up', 'py': 'Inp_RSI_Level_Up', 'param': 'Inp_RSI_Level_Up', 'type': 'double', 'default': 75.0, 'label': 'RSI: Level Up', 'sinput': False}, {'mql': 'Inp_MA_ma_period', 'py': 'Inp_MA_ma_period', 'param': 'Inp_MA_ma_period', 'type': 'int', 'default': 6, 'label': 'MA: averaging period', 'sinput': False}, {'mql': 'Inp_MA_ma_method', 'py': 'Inp_MA_ma_method', 'param': 'Inp_MA_ma_method', 'type': 'int', 'default': 0, 'label': 'MA: smoothing type', 'sinput': False}, {'mql': 'Inp_MA_applied_price', 'py': 'Inp_MA_applied_price', 'param': 'Inp_MA_applied_price', 'type': 'int', 'default': 1, 'label': 'MA: type of price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_RSI_Fast_ma_period = _input('Inp_RSI_Fast_ma_period', 5)  # RSI Fast: averaging period
Inp_RSI_Slow_ma_period = _input('Inp_RSI_Slow_ma_period', 15)  # RSI Slow: averaging period
Inp_RSI_applied_price = _input('Inp_RSI_applied_price', PRICE_CLOSE)  # RSI: type of price
Inp_RSI_Level_Color = _input('Inp_RSI_Level_Color', clrDimGray)  # RSI: Color line Levels
Inp_RSI_Level_Down = _input('Inp_RSI_Level_Down', 25.0)  # RSI: Level Down
Inp_RSI_Level_Middle = _input('Inp_RSI_Level_Middle', 50.0)  # RSI: Level Middle
Inp_RSI_Level_Up = _input('Inp_RSI_Level_Up', 75.0)  # RSI: Level Up
Inp_MA_ma_period = _input('Inp_MA_ma_period', 6)  # MA: averaging period
Inp_MA_ma_method = _input('Inp_MA_ma_method', MODE_SMA)  # MA: smoothing type
Inp_MA_applied_price = _input('Inp_MA_applied_price', PRICE_CLOSE)  # MA: type of price
MAonRSI_Fast_Buffer = Arr(0, 0.0)
MAonRSI_Slow_Buffer = Arr(0, 0.0)
handle_iMAOnRSI_Fast = 0  # variable for storing the handle of the iRSI indicator
handle_iMAOnRSI_Slow = 0  # variable for storing the handle of the iRSI indicator
handle_iRSI_Fast = 0  # variable for storing the handle of the iRSI indicator
handle_iRSI_Slow = 0  # variable for storing the handle of the iRSI indicator
bars_calculated = 0  # we will keep the number of values in the Relative Strength Index indicator
m_init_error = False  # error on InInit

def OnInit():
    global handle_iMAOnRSI_Fast, handle_iMAOnRSI_Slow, handle_iRSI_Fast, handle_iRSI_Slow, m_init_error
    SetIndexBuffer(0, MAonRSI_Fast_Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, MAonRSI_Slow_Buffer, INDICATOR_DATA)
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
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSI_MAonRSI_Dual(' + IntegerToString(Inp_RSI_Fast_ma_period) + ',' + IntegerToString(Inp_RSI_Slow_ma_period) + ')')
    handle_iRSI_Fast = iRSI(Symbol(), Period(), Inp_RSI_Fast_ma_period, Inp_RSI_applied_price)
    if handle_iRSI_Fast == INVALID_HANDLE:
        PrintFormat("Failed to create handle of the iRSI ('Fast') indicator for the symbol %s/%s, error code %d", Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    handle_iRSI_Slow = iRSI(Symbol(), Period(), Inp_RSI_Slow_ma_period, Inp_RSI_applied_price)
    if handle_iRSI_Slow == INVALID_HANDLE:
        PrintFormat("Failed to create handle of the iRSI ('Slow') indicator for the symbol %s/%s, error code %d", Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    handle_iMAOnRSI_Fast = iMA(Symbol(), Period(), Inp_MA_ma_period, 0, Inp_MA_ma_method, handle_iRSI_Fast)
    if handle_iMAOnRSI_Fast == INVALID_HANDLE:
        PrintFormat("Failed to create handle of the iMA ('Fast') indicator for the symbol %s/%s, error code %d", Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    handle_iMAOnRSI_Slow = iMA(Symbol(), Period(), Inp_MA_ma_period, 0, Inp_MA_ma_method, handle_iRSI_Slow)
    if handle_iMAOnRSI_Slow == INVALID_HANDLE:
        PrintFormat("Failed to create handle of the iMA ('Slow') indicator for the symbol %s/%s, error code %d", Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    if m_init_error:
        return 0
    values_to_copy = 0
    calculated_ma_on_rsi_fast = BarsCalculated(handle_iMAOnRSI_Fast)
    if calculated_ma_on_rsi_fast <= 0:
        PrintFormat('BarsCalculated(handle_iMAOnRSI_Fast) returned %d, error code %d', calculated_ma_on_rsi_fast, GetLastError())
        return 0
    calculated_ma_on_rsi_slow = BarsCalculated(handle_iMAOnRSI_Slow)
    if calculated_ma_on_rsi_slow <= 0:
        PrintFormat('BarsCalculated(handle_iMAOnRSI_Slow) returned %d, error code %d', calculated_ma_on_rsi_slow, GetLastError())
        return 0
    if calculated_ma_on_rsi_fast != calculated_ma_on_rsi_slow:
        PrintFormat('BarsCalculated(handle_iMAOnRSI_Fast) returned %d, BarsCalculated(handle_iMAOnRSI_Slow) returned %d', calculated_ma_on_rsi_fast, calculated_ma_on_rsi_slow)
        return 0
    calculated = calculated_ma_on_rsi_fast
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBuffer(MAonRSI_Fast_Buffer, 0, handle_iMAOnRSI_Fast, values_to_copy):
        return 0
    if not FillArrayFromBuffer(MAonRSI_Slow_Buffer, 0, handle_iMAOnRSI_Slow, values_to_copy):
        return 0
    bars_calculated = calculated
    return rates_total

def FillArrayFromBuffer(values, shift, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, -shift, amount, values) < 0:
        PrintFormat('Failed to copy data from the iMA indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    if handle_iMAOnRSI_Fast != INVALID_HANDLE:
        IndicatorRelease(handle_iMAOnRSI_Fast)
    if handle_iMAOnRSI_Slow != INVALID_HANDLE:
        IndicatorRelease(handle_iMAOnRSI_Slow)
    if handle_iRSI_Fast != INVALID_HANDLE:
        IndicatorRelease(handle_iRSI_Fast)
    if handle_iRSI_Slow != INVALID_HANDLE:
        IndicatorRelease(handle_iRSI_Slow)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSIMAonRSIDual(_MQL5Indicator):
    name = 'RSI_MAonRSI_Dual'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_RSI_Fast_ma_period': 5,  # RSI Fast: averaging period
        'Inp_RSI_Slow_ma_period': 15,  # RSI Slow: averaging period
        'Inp_RSI_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # RSI: type of price
        'Inp_RSI_Level_Down': 25.0,  # RSI: Level Down
        'Inp_RSI_Level_Middle': 50.0,  # RSI: Level Middle
        'Inp_RSI_Level_Up': 75.0,  # RSI: Level Up
        'Inp_MA_ma_period': 6,  # MA: averaging period
        'Inp_MA_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA: smoothing type
        'Inp_MA_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA: type of price
    }

