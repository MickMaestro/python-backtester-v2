"""MA on DeMarker Arrow — converted from MQL5: MQL5 Indicators/MA on DeMarker Arrow/MA on DeMarker Arrow.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.002

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.002', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [11186720], 2: [3329434], 3: [16748574], 4: [4678655]}, 'widths': {1: 2, 2: 2, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'DeM', 2: 'MA on DeM', 3: 'Up', 4: 'Down'}, 'levels': [], 'description': [], 'name': 'MA on DeMarker Arrow', 'source': 'MQL5 Indicators/MA on DeMarker Arrow/MA on DeMarker Arrow.mq5', 'folder': 'MA on DeMarker Arrow', 'inputs': [{'mql': 'Inp_DeM_ma_period', 'py': 'Inp_DeM_ma_period', 'param': 'Inp_DeM_ma_period', 'type': 'int', 'default': 14, 'label': 'DeM: averaging period', 'sinput': False}, {'mql': 'Inp_DeM_LevelUP', 'py': 'Inp_DeM_LevelUP', 'param': 'Inp_DeM_LevelUP', 'type': 'double', 'default': 0.7, 'label': 'DeM: Level UP', 'sinput': False}, {'mql': 'Inp_DeM_LevelDOWN', 'py': 'Inp_DeM_LevelDOWN', 'param': 'Inp_DeM_LevelDOWN', 'type': 'double', 'default': 0.3, 'label': 'DeM: Level DOWN', 'sinput': False}, {'mql': 'Inp_MA_ma_period', 'py': 'Inp_MA_ma_period', 'param': 'Inp_MA_ma_period', 'type': 'int', 'default': 6, 'label': 'MA: averaging period', 'sinput': False}, {'mql': 'Inp_MA_ma_method', 'py': 'Inp_MA_ma_method', 'param': 'Inp_MA_ma_method', 'type': 'int', 'default': 1, 'label': 'MA: smoothing type', 'sinput': False}, {'mql': 'InpUpArrowCode', 'py': 'InpUpArrowCode', 'param': 'InpUpArrowCode', 'type': 'uchar', 'default': 71, 'label': "Arrow 'Up': code (font Wingdings)", 'sinput': False}, {'mql': 'InpUpArrowShift', 'py': 'InpUpArrowShift', 'param': 'InpUpArrowShift', 'type': 'int', 'default': 10, 'label': "Arrow 'Up': vertical shift in pixel", 'sinput': False}, {'mql': 'InpDownArrowCode', 'py': 'InpDownArrowCode', 'param': 'InpDownArrowCode', 'type': 'uchar', 'default': 72, 'label': "Arrow 'Down': code (font Wingdings)", 'sinput': False}, {'mql': 'InpDownArrowShift', 'py': 'InpDownArrowShift', 'param': 'InpDownArrowShift', 'type': 'int', 'default': 10, 'label': "Arrow 'Down': vertical shift in pixel", 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_DeM_ma_period = _input('Inp_DeM_ma_period', 14)  # DeM: averaging period
Inp_DeM_LevelUP = _input('Inp_DeM_LevelUP', 0.7)  # DeM: Level UP
Inp_DeM_LevelDOWN = _input('Inp_DeM_LevelDOWN', 0.3)  # DeM: Level DOWN
Inp_MA_ma_period = _input('Inp_MA_ma_period', 6)  # MA: averaging period
Inp_MA_ma_method = _input('Inp_MA_ma_method', MODE_EMA)  # MA: smoothing type
InpUpArrowCode = _input('InpUpArrowCode', 71)  # Arrow 'Up': code (font Wingdings)
InpUpArrowShift = _input('InpUpArrowShift', 10)  # Arrow 'Up': vertical shift in pixel
InpDownArrowCode = _input('InpDownArrowCode', 72)  # Arrow 'Down': code (font Wingdings)
InpDownArrowShift = _input('InpDownArrowShift', 10)  # Arrow 'Down': vertical shift in pixel
DeMBuffer = Arr(0, 0.0)
MAonDeMBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DownBuffer = Arr(0, 0.0)
handle_iDeMarker = 0  # variable for storing the handle of the iDeMarker indicator
handle_iMA = 0  # variable for storing the handle of the iMA indicator
bars_calculated = 0  # we will keep the number of values in the DeMarker and MA indicators
m_init_error = False  # error on InInit

def OnInit():
    global handle_iDeMarker, handle_iMA, m_init_error
    SetIndexBuffer(0, DeMBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, MAonDeMBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, DownBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, Inp_DeM_LevelUP)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, Inp_DeM_LevelDOWN)
    PlotIndexSetInteger(2, PLOT_ARROW, InpUpArrowCode)
    PlotIndexSetInteger(3, PLOT_ARROW, InpDownArrowCode)
    PlotIndexSetInteger(2, PLOT_ARROW_SHIFT, InpUpArrowShift)
    PlotIndexSetInteger(3, PLOT_ARROW_SHIFT, -InpDownArrowShift)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetString(0, PLOT_LABEL, 'DeM' + '(' + IntegerToString(Inp_DeM_ma_period) + ')')
    PlotIndexSetString(1, PLOT_LABEL, 'MA' + '(' + IntegerToString(Inp_MA_ma_period) + ')' + ' on DeM' + '(' + IntegerToString(Inp_DeM_ma_period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 3)
    handle_iDeMarker = iDeMarker(Symbol(), Period(), Inp_DeM_ma_period)
    if handle_iDeMarker == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iDeMarker indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    handle_iMA = iMA(Symbol(), Period(), Inp_MA_ma_period, 0, Inp_MA_ma_method, handle_iDeMarker)
    if handle_iMA == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMA indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    if m_init_error:
        return 0
    values_to_copy = 0
    calculated_dem = BarsCalculated(handle_iDeMarker)
    if calculated_dem <= 0:
        PrintFormat('BarsCalculated(DeMarker) returned %d, error code %d', calculated_dem, GetLastError())
        return 0
    calculated_ma = BarsCalculated(handle_iMA)
    if calculated_ma <= 0:
        PrintFormat('BarsCalculated(MA) returned %d, error code %d', calculated_ma, GetLastError())
        return 0
    if calculated_dem != calculated_ma:
        PrintFormat('BarsCalculated(DeMarker) returned %d, BarsCalculated(MA) returned %d', calculated_dem, calculated_ma)
        return 0
    calculated = calculated_dem
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBufferMA(MAonDeMBuffer, 0, handle_iMA, values_to_copy):
        return 0
    if not FillArrayFromBufferDeMarker(DeMBuffer, handle_iDeMarker, values_to_copy):
        return 0
    bars_calculated = calculated
    if rates_total < 3:
        return 0
    limit = prev_calculated - 1
    if prev_calculated == 0:
        UpBuffer[0] = 0.0
        DownBuffer[0] = 0.0
        limit = 1
    for i in range(limit, rates_total):
        UpBuffer[i] = 0.0
        DownBuffer[i] = 0.0
        if (DeMBuffer[i - 1] < MAonDeMBuffer[i - 1] and DeMBuffer[i] > MAonDeMBuffer[i]) and DeMBuffer[i - 1] < Inp_DeM_LevelDOWN:
            UpBuffer[i] = MAonDeMBuffer[i]
        elif (DeMBuffer[i - 1] > MAonDeMBuffer[i - 1] and DeMBuffer[i] < MAonDeMBuffer[i]) and DeMBuffer[i - 1] > Inp_DeM_LevelUP:
            DownBuffer[i] = MAonDeMBuffer[i]
    return rates_total

def FillArrayFromBufferMA(values, shift, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, -shift, amount, values) < 0:
        PrintFormat('Failed to copy data from the iMA indicator, error code %d', GetLastError())
        return False
    return True

def FillArrayFromBufferDeMarker(values, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, 0, amount, values) < 0:
        PrintFormat('Failed to copy data from the iDeMarker indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    if handle_iDeMarker != INVALID_HANDLE:
        IndicatorRelease(handle_iDeMarker)
    if handle_iMA != INVALID_HANDLE:
        IndicatorRelease(handle_iMA)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MAOnDeMarkerArrow(_MQL5Indicator):
    name = 'MA on DeMarker Arrow'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_DeM_ma_period': 14,  # DeM: averaging period
        'Inp_DeM_LevelUP': 0.7,  # DeM: Level UP
        'Inp_DeM_LevelDOWN': 0.3,  # DeM: Level DOWN
        'Inp_MA_ma_period': 6,  # MA: averaging period
        'Inp_MA_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # MA: smoothing type
        'InpUpArrowCode': 71,  # Arrow 'Up': code (font Wingdings)
        'InpUpArrowShift': 10,  # Arrow 'Up': vertical shift in pixel
        'InpDownArrowCode': 72,  # Arrow 'Down': code (font Wingdings)
        'InpDownArrowShift': 10,  # Arrow 'Down': vertical shift in pixel
    }

