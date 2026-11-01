"""CCI Color — converted from MQL5: MQL5 Indicators/CCI Color/CCI Color.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.001

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.001', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [255, 16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'CCI'}, 'levels': [], 'description': [], 'name': 'CCI Color', 'source': 'MQL5 Indicators/CCI Color/CCI Color.mq5', 'folder': 'CCI Color', 'inputs': [{'mql': 'Inp_CCI_ma_period', 'py': 'Inp_CCI_ma_period', 'param': 'Inp_CCI_ma_period', 'type': 'int', 'default': 14, 'label': 'Averaging period', 'sinput': False}, {'mql': 'Inp_CCI_LevelUP', 'py': 'Inp_CCI_LevelUP', 'param': 'Inp_CCI_LevelUP', 'type': 'double', 'default': 100.0, 'label': 'Level UP', 'sinput': False}, {'mql': 'Inp_CCI_LevelDOWN', 'py': 'Inp_CCI_LevelDOWN', 'param': 'Inp_CCI_LevelDOWN', 'type': 'double', 'default': -100.0, 'label': 'Level DOWN', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_CCI_ma_period = _input('Inp_CCI_ma_period', 14)  # Averaging period
Inp_CCI_LevelUP = _input('Inp_CCI_LevelUP', 100.0)  # Level UP
Inp_CCI_LevelDOWN = _input('Inp_CCI_LevelDOWN', -100.0)  # Level DOWN
CCI_Buffer = Arr(0, 0.0)
CCC_Colors = Arr(0, 0.0)
handle_iCCI = 0  # variable for storing the handle of the iCCI indicator
bars_calculated = 0  # we will keep the number of values in the Commodity Channel Index indicator
m_init_error = False  # error on InInit

def OnInit():
    global handle_iCCI, m_init_error
    if Inp_CCI_ma_period <= 0:
        printf('Incorrect value for input variable "Averaging period"=%d.', Inp_CCI_ma_period)
        return INIT_PARAMETERS_INCORRECT
    SetIndexBuffer(0, CCI_Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, CCC_Colors, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, Inp_CCI_LevelUP)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, Inp_CCI_LevelDOWN)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CCI Color(' + IntegerToString(Inp_CCI_ma_period) + ')')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Inp_CCI_ma_period - 1)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    handle_iCCI = iCCI(Symbol(), Period(), Inp_CCI_ma_period, PRICE_TYPICAL)
    if handle_iCCI == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iCCI indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    if m_init_error:
        return 0
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
    if not FillArrayFromBuffer(CCI_Buffer, handle_iCCI, values_to_copy):
        return 0
    if rates_total < 3:
        return 0
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 1
    for i in range(limit, rates_total):
        if CCI_Buffer[i - 1] < 0.0 and CCI_Buffer[i] >= 0.0:
            CCC_Colors[i] = 1.0
        if CCI_Buffer[i - 1] > 0.0 and CCI_Buffer[i] <= 0.0:
            CCC_Colors[i] = 0.0
        if CCI_Buffer[i] >= 0.0:
            CCC_Colors[i] = 1.0
        else:
            CCC_Colors[i] = 0.0
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


class CCIColor(_MQL5Indicator):
    name = 'CCI Color'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_CCI_ma_period': 14,  # Averaging period
        'Inp_CCI_LevelUP': 100.0,  # Level UP
        'Inp_CCI_LevelDOWN': -100.0,  # Level DOWN
    }

