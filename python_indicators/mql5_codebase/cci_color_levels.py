"""CCI Color Levels — converted from MQL5: MQL5 Indicators/CCI Color Levels/CCI Color Levels.mq5

The indicator displays the color histogram sites of the chart above \\"Level UP\\" and below \\"Level DOWN\\"
Copyright: Copyright © 2018, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.001

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.001', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 4, 2: 1, 3: 4}, 'colors': {1: [16711680], 2: [8421504], 3: [255]}, 'widths': {1: 2, 2: 1, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Level UP', 2: 'CCI', 3: 'Level DOWN'}, 'levels': [], 'description': ['The indicator displays the color histogram sites of the chart above \\"Level UP\\" and below \\"Level DOWN\\"'], 'name': 'CCI Color Levels', 'source': 'MQL5 Indicators/CCI Color Levels/CCI Color Levels.mq5', 'folder': 'CCI Color Levels', 'inputs': [{'mql': 'Inp_CCI_ma_period', 'py': 'Inp_CCI_ma_period', 'param': 'Inp_CCI_ma_period', 'type': 'int', 'default': 14, 'label': 'Averaging period', 'sinput': False}, {'mql': 'Inp_CCI_LevelUP', 'py': 'Inp_CCI_LevelUP', 'param': 'Inp_CCI_LevelUP', 'type': 'double', 'default': 90.0, 'label': 'Level UP', 'sinput': False}, {'mql': 'Inp_CCI_LevelDOWN', 'py': 'Inp_CCI_LevelDOWN', 'param': 'Inp_CCI_LevelDOWN', 'type': 'double', 'default': -90.0, 'label': 'Level DOWN', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_CCI_ma_period = _input('Inp_CCI_ma_period', 14)  # Averaging period
Inp_CCI_LevelUP = _input('Inp_CCI_LevelUP', 90.0)  # Level UP
Inp_CCI_LevelDOWN = _input('Inp_CCI_LevelDOWN', -90.0)  # Level DOWN
BufferUpHigh = Arr(0, 0.0)  # when you call from the Expert Advisor, you must specify the number of the buffer 0
BufferUpLow = Arr(0, 0.0)
BufferCCI = Arr(0, 0.0)  # when you call from the Expert Advisor, you must specify the number of the buffer 2
BufferDownHigh = Arr(0, 0.0)
BufferDownLow = Arr(0, 0.0)  # when you call from the Expert Advisor, you must specify the number of the buffer 4
handle_iCCI = 0
bars_calculated = 0

def OnInit():
    global handle_iCCI
    if Inp_CCI_ma_period <= 0:
        printf('Incorrect value for input variable "Averaging period"=%d.', Inp_CCI_ma_period)
        return INIT_PARAMETERS_INCORRECT
    SetIndexBuffer(0, BufferUpHigh, INDICATOR_DATA)
    SetIndexBuffer(1, BufferUpLow, INDICATOR_DATA)
    SetIndexBuffer(2, BufferCCI, INDICATOR_DATA)
    SetIndexBuffer(3, BufferDownHigh, INDICATOR_DATA)
    SetIndexBuffer(4, BufferDownLow, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, Inp_CCI_LevelUP)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, Inp_CCI_LevelDOWN)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CCI Color Levels(' + _str(14) + ')')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Inp_CCI_ma_period - 1)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, Inp_CCI_ma_period - 1)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, Inp_CCI_ma_period - 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    handle_iCCI = iCCI(Symbol(), Period(), Inp_CCI_ma_period, PRICE_TYPICAL)
    if handle_iCCI == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iCCI indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    values_to_copy = 0
    calculated = BarsCalculated(handle_iCCI)
    if calculated <= 0:
        PrintFormat('BarsCalculated() returned %d, error code %d', calculated, GetLastError())
        return 0
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBuffer(BufferCCI, handle_iCCI, values_to_copy):
        return 0
    d = 0
    limit = rates_total - values_to_copy
    for i in range(limit, rates_total):
        if BufferCCI[i] <= Inp_CCI_LevelDOWN:
            BufferUpHigh[i] = 0.0
            BufferUpLow[i] = 0.0
            BufferDownHigh[i] = Inp_CCI_LevelDOWN
            BufferDownLow[i] = BufferCCI[i]
        elif BufferCCI[i] >= Inp_CCI_LevelUP:
            BufferUpHigh[i] = BufferCCI[i]
            BufferUpLow[i] = Inp_CCI_LevelUP
            BufferDownHigh[i] = 0.0
            BufferDownLow[i] = 0.0
        else:
            BufferUpHigh[i] = 0.0
            BufferUpLow[i] = 0.0
            BufferDownHigh[i] = 0.0
            BufferDownLow[i] = 0.0
    bars_calculated = calculated
    return rates_total

def FillArrayFromBuffer(values, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, 0, amount, values) < 0:
        PrintFormat('Failed to copy data from the iCCI indicator, error code %d', GetLastError())
        return False
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CCIColorLevels(_MQL5Indicator):
    name = 'CCI Color Levels'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_CCI_ma_period': 14,  # Averaging period
        'Inp_CCI_LevelUP': 90.0,  # Level UP
        'Inp_CCI_LevelDOWN': -90.0,  # Level DOWN
    }

