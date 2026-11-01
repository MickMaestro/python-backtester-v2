"""FlatTrend — converted from MQL5: MQL5 Indicators/FlatTrend/FlatTrend.mq5

Copyright: Kirk Sloan; Link: http://www.metaquotes.net; Version: 1.002

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Kirk Sloan', 'link': 'http://www.metaquotes.net', 'version': '1.002', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 4}, 'types': {1: 3, 2: 3, 3: 3, 4: 3}, 'colors': {1: [255], 2: [16711680], 3: [255], 4: [16711680]}, 'widths': {1: 2, 2: 2, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Sell', 2: 'Buy', 3: 'End Sell', 4: 'End Buy'}, 'levels': [], 'description': [], 'name': 'FlatTrend', 'source': 'MQL5 Indicators/FlatTrend/FlatTrend.mq5', 'folder': 'FlatTrend', 'inputs': [{'mql': 'InpSignalTimeframe', 'py': 'InpSignalTimeframe', 'param': 'InpSignalTimeframe', 'type': 'int', 'default': 0, 'label': 'signal timeframe', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpSignalTimeframe = _input('InpSignalTimeframe', PERIOD_CURRENT)  # signal timeframe
ExtMapBuffer0 = Arr(0, 0.0)
ExtMapBuffer1 = Arr(0, 0.0)
ExtMapBuffer2 = Arr(0, 0.0)
ExtMapBuffer3 = Arr(0, 0.0)
ADXBuffer = Arr(0, 0.0)  # adx indicator buffer
DI_plusBuffer = Arr(0, 0.0)  # adx plus DI buffer
DI_minusBuffer = Arr(0, 0.0)  # adx minus DI buffer
handle_iADX = 0  # variable for storing the handle of the iADX indicator
bars_calculated_adx = 0  # we will keep the number of values in the Average Directional Movement Index indicator
SARBuffer = Arr(0, 0.0)  # sar indicator buffer
handle_iSAR = 0  # variable for storing the handle of the iSAR indicator
bars_calculated_sar = 0  # we will keep the number of values in the Parabolic SAR indicator

def OnInit():
    global handle_iADX, handle_iSAR
    SetIndexBuffer(0, ExtMapBuffer0, INDICATOR_DATA)
    SetIndexBuffer(1, ExtMapBuffer1, INDICATOR_DATA)
    SetIndexBuffer(2, ExtMapBuffer2, INDICATOR_DATA)
    SetIndexBuffer(3, ExtMapBuffer3, INDICATOR_DATA)
    SetIndexBuffer(4, ADXBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, DI_plusBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, DI_minusBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, SARBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    handle_iADX = iADX(Symbol(), InpSignalTimeframe, 14)
    if handle_iADX == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iADX indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(InpSignalTimeframe, 'ENUM_TIMEFRAMES'), GetLastError())
        return INIT_FAILED
    handle_iSAR = iSAR(Symbol(), InpSignalTimeframe, 0.02, 0.2)
    if handle_iSAR == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iSAR indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(InpSignalTimeframe, 'ENUM_TIMEFRAMES'), GetLastError())
        return INIT_FAILED
    ArrayInitialize(ExtMapBuffer0, 0.0)
    ArrayInitialize(ExtMapBuffer1, 0.0)
    ArrayInitialize(ExtMapBuffer2, 0.0)
    ArrayInitialize(ExtMapBuffer3, 0.0)
    ArrayInitialize(ADXBuffer, 0.0)
    ArrayInitialize(DI_plusBuffer, 0.0)
    ArrayInitialize(DI_minusBuffer, 0.0)
    ArrayInitialize(SARBuffer, 0.0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated_adx, bars_calculated_sar
    values_to_copy_adx = 0
    calculated_adx = BarsCalculated(handle_iADX)
    if calculated_adx <= 0:
        PrintFormat('BarsCalculated(ADX) returned %d, error code %d', calculated_adx, GetLastError())
        return 0
    if (prev_calculated == 0 or calculated_adx != bars_calculated_adx) or rates_total > (prev_calculated + 1):
        if calculated_adx > rates_total:
            values_to_copy_adx = rates_total
        else:
            values_to_copy_adx = calculated_adx
    else:
        values_to_copy_adx = rates_total - prev_calculated + 1
    if not FillArraysFromBuffersADX(ADXBuffer, DI_plusBuffer, DI_minusBuffer, handle_iADX, values_to_copy_adx):
        return 0
    bars_calculated_adx = calculated_adx
    values_to_copy_sar = 0
    calculated_sar = BarsCalculated(handle_iSAR)
    if calculated_sar <= 0:
        PrintFormat('BarsCalculated(SAR) returned %d, error code %d', calculated_sar, GetLastError())
        return 0
    if (prev_calculated == 0 or calculated_sar != bars_calculated_sar) or rates_total > (prev_calculated + 1):
        if calculated_sar > rates_total:
            values_to_copy_sar = rates_total
        else:
            values_to_copy_sar = calculated_sar
    else:
        values_to_copy_sar = rates_total - prev_calculated + 1
    if not FillArrayFromBufferSAR(SARBuffer, handle_iSAR, values_to_copy_sar):
        return 0
    bars_calculated_sar = calculated_sar
    if values_to_copy_adx != values_to_copy_sar:
        Alert('Ахтунг')
        return 0
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 0
    for i in range(limit, rates_total):
        ExtMapBuffer0[i] = 0.0
        ExtMapBuffer1[i] = 0.0
        ExtMapBuffer2[i] = 0.0
        ExtMapBuffer3[i] = 0.0
        if SARBuffer[i] < close[i]:
            if DI_plusBuffer[i] > DI_minusBuffer[i]:
                ExtMapBuffer1[i] = 1.0
            else:
                ExtMapBuffer3[i] = 1.0
        else:
            if DI_plusBuffer[i] > DI_minusBuffer[i]:
                ExtMapBuffer2[i] = 1.0
            else:
                ExtMapBuffer0[i] = 1.0
    return rates_total

def FillArraysFromBuffersADX(adx_values, DIplus_values, DIminus_values, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, 0, amount, adx_values) < 0:
        PrintFormat('Failed to copy data from the iADX indicator, error code %d', GetLastError())
        return False
    if CopyBuffer(ind_handle, 1, 0, amount, DIplus_values) < 0:
        PrintFormat('Failed to copy data from the iADX indicator, error code %d', GetLastError())
        return False
    if CopyBuffer(ind_handle, 2, 0, amount, DIminus_values) < 0:
        PrintFormat('Failed to copy data from the iADX indicator, error code %d', GetLastError())
        return False
    return True

def FillArrayFromBufferSAR(sar_buffer, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, 0, amount, sar_buffer) < 0:
        PrintFormat('Failed to copy data from the iSAR indicator, error code %d', GetLastError())
        return False
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FlatTrend(_MQL5Indicator):
    name = 'FlatTrend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpSignalTimeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # signal timeframe
    }

