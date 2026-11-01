"""MA on RMI — converted from MQL5: MQL5 Indicators/MA on RMI/MA on RMI.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [11186720], 2: [3329434]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'RMI', 2: 'MA on RMI'}, 'levels': [], 'description': [], 'name': 'MA on RMI', 'source': 'MQL5 Indicators/MA on RMI/MA on RMI.mq5', 'folder': 'MA on RMI', 'inputs': [{'mql': 'InpRmiPeriod', 'py': 'InpRmiPeriod', 'param': 'InpRmiPeriod', 'type': 'ushort', 'default': 14, 'label': 'RMI Period', 'sinput': False}, {'mql': 'InpMomPeriod', 'py': 'InpMomPeriod', 'param': 'InpMomPeriod', 'type': 'ushort', 'default': 10, 'label': 'Momentum Period', 'sinput': False}, {'mql': 'Inp_MA_ma_period', 'py': 'Inp_MA_ma_period', 'param': 'Inp_MA_ma_period', 'type': 'int', 'default': 6, 'label': 'MA: averaging period', 'sinput': False}, {'mql': 'Inp_MA_ma_method', 'py': 'Inp_MA_ma_method', 'param': 'Inp_MA_ma_method', 'type': 'int', 'default': 1, 'label': 'MA: smoothing type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpRmiPeriod = _input('InpRmiPeriod', 14)  # RMI Period
InpMomPeriod = _input('InpMomPeriod', 10)  # Momentum Period
Inp_MA_ma_period = _input('Inp_MA_ma_period', 6)  # MA: averaging period
Inp_MA_ma_method = _input('Inp_MA_ma_method', MODE_EMA)  # MA: smoothing type
RMIBuffer = Arr(0, 0.0)
MAonRMIBuffer = Arr(0, 0.0)
handle_iCustom = 0  # variable for storing the handle of the RMI indicator
handle_iMA = 0  # variable for storing the handle of the iMA indicator
bars_calculated = 0  # we will keep the number of values in the RMI and MA indicators
m_init_error = False  # error on InInit

def OnInit():
    global handle_iCustom, handle_iMA, m_init_error
    SetIndexBuffer(0, RMIBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, MAonRMIBuffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, 'RMI' + '(' + IntegerToString(InpRmiPeriod) + ',' + IntegerToString(InpMomPeriod) + ')')
    PlotIndexSetString(1, PLOT_LABEL, 'MA on RMI' + '(' + IntegerToString(Inp_MA_ma_period) + ')')
    handle_iCustom = iCustom(Symbol(), Period(), 'rmi', InpRmiPeriod, InpMomPeriod)
    if handle_iCustom == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iCustom indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    handle_iMA = iMA(Symbol(), Period(), Inp_MA_ma_period, 0, Inp_MA_ma_method, handle_iCustom)
    if handle_iMA == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMA indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    values_to_copy = 0
    calculated_rmi = BarsCalculated(handle_iCustom)
    if calculated_rmi <= 0:
        PrintFormat('BarsCalculated(handle_iCustom) returned %d, error code %d', calculated_rmi, GetLastError())
        return 0
    calculated_ma = BarsCalculated(handle_iMA)
    if calculated_ma <= 0:
        PrintFormat('BarsCalculated(MA) returned %d, error code %d', calculated_ma, GetLastError())
        return 0
    if calculated_rmi != calculated_ma:
        PrintFormat('BarsCalculated(handle_iCustom) returned %d, BarsCalculated(handle_iMA) returned %d', calculated_rmi, calculated_ma)
        return 0
    calculated = calculated_rmi
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBufferMA(MAonRMIBuffer, 0, handle_iMA, values_to_copy):
        return 0
    if not FillArrayFromBufferCCI(RMIBuffer, handle_iCustom, values_to_copy):
        return 0
    bars_calculated = calculated
    return rates_total

def FillArrayFromBufferMA(values, shift, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, -shift, amount, values) < 0:
        PrintFormat('Failed to copy data from the iMA indicator, error code %d', GetLastError())
        return False
    return True

def FillArrayFromBufferCCI(values, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, 0, amount, values) < 0:
        PrintFormat('Failed to copy data from the iCCI indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    if handle_iCustom != INVALID_HANDLE:
        IndicatorRelease(handle_iCustom)
    if handle_iMA != INVALID_HANDLE:
        IndicatorRelease(handle_iMA)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MAOnRMI(_MQL5Indicator):
    name = 'MA on RMI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpRmiPeriod': 14,  # RMI Period
        'InpMomPeriod': 10,  # Momentum Period
        'Inp_MA_ma_period': 6,  # MA: averaging period
        'Inp_MA_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # MA: smoothing type
    }

