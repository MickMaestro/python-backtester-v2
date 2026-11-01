"""ATR Dual — converted from MQL5: MQL5 Indicators/ATR Dual/ATR Dual.mq5

ATR Dual
Copyright: Copyright © 2018, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.001

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.001', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 3}, 'colors': {1: [13749760], 2: [36095]}, 'widths': {}, 'styles': {1: 2}, 'labels': {1: 'ATR Master', 2: 'ATR Slave'}, 'levels': [], 'description': ['ATR Dual'], 'name': 'ATR Dual', 'source': 'MQL5 Indicators/ATR Dual/ATR Dual.mq5', 'folder': 'ATR Dual', 'inputs': [{'mql': 'Inp_ATR_Master_ma_period', 'py': 'Inp_ATR_Master_ma_period', 'param': 'Inp_ATR_Master_ma_period', 'type': 'int', 'default': 14, 'label': 'ATR "Master" averaging period', 'sinput': False}, {'mql': 'Inp_ATR_Slave_ma_period', 'py': 'Inp_ATR_Slave_ma_period', 'param': 'Inp_ATR_Slave_ma_period', 'type': 'int', 'default': 1, 'label': 'ATR "Slave" averaging period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_ATR_Master_ma_period = _input('Inp_ATR_Master_ma_period', 14)  # ATR "Master" averaging period
Inp_ATR_Slave_ma_period = _input('Inp_ATR_Slave_ma_period', 1)  # ATR "Slave" averaging period
iATRBuffer_Master = Arr(0, 0.0)
iATRBuffer_Slave = Arr(0, 0.0)
handle_iATR_Master = 0  # variable for storing the handle of the iATR indicator
handle_iATR_Slave = 0  # variable for storing the handle of the iATR indicator
bars_calculated = 0

def OnInit():
    global handle_iATR_Master, handle_iATR_Slave
    SetIndexBuffer(0, iATRBuffer_Master, INDICATOR_DATA)
    SetIndexBuffer(1, iATRBuffer_Slave, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    handle_iATR_Master = iATR(Symbol(), Period(), Inp_ATR_Master_ma_period)
    if handle_iATR_Master == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iATR indicator ("Master") for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        return INIT_FAILED
    handle_iATR_Slave = iATR(Symbol(), Period(), Inp_ATR_Slave_ma_period)
    if handle_iATR_Slave == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iATR indicator ("Slave") for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        return INIT_FAILED
    short_name = StringFormat('ATR Dual(%d,%d)', Inp_ATR_Master_ma_period, Inp_ATR_Slave_ma_period)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    values_to_copy = 0
    calculated_master = BarsCalculated(handle_iATR_Master)
    calculated_slave = BarsCalculated(handle_iATR_Slave)
    if (calculated_master <= 0 or calculated_slave <= 0) or calculated_master != calculated_slave:
        PrintFormat('BarsCalculated("Master") returned %d, BarsCalculated("Slave") returned %d,', calculated_master, calculated_slave)
        return 0
    if ((prev_calculated == 0 or calculated_master != bars_calculated) or calculated_slave != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated_master > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated_master
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBuffer(iATRBuffer_Master, handle_iATR_Master, values_to_copy):
        return 0
    if not FillArrayFromBuffer(iATRBuffer_Slave, handle_iATR_Slave, values_to_copy):
        return 0
    bars_calculated = calculated_master
    return rates_total

def FillArrayFromBuffer(values, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, 0, amount, values) < 0:
        PrintFormat('Failed to copy data from the iATR indicator, error code %d', GetLastError())
        return False
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ATRDual(_MQL5Indicator):
    name = 'ATR Dual'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_ATR_Master_ma_period': 14,  # ATR "Master" averaging period
        'Inp_ATR_Slave_ma_period': 1,  # ATR "Slave" averaging period
    }

