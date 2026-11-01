"""RSI Dual Cloud — converted from MQL5: MQL5 Indicators/RSI Dual Cloud/RSI Dual Cloud.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'separate', 'indicator_minimum': 0.0, 'indicator_maximum': 100.0, 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 7, 4: 7}, 'colors': {1: [16748574], 2: [65280], 3: [15527167, 16711680], 4: [255, 16772332]}, 'widths': {1: 2, 2: 2, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'RSI Fast', 2: 'RSI Slow', 3: 'Cloud UP', 4: 'Cloud DOWN'}, 'levels': [], 'description': [], 'name': 'RSI Dual Cloud', 'source': 'MQL5 Indicators/RSI Dual Cloud/RSI Dual Cloud.mq5', 'folder': 'RSI Dual Cloud', 'inputs': [{'mql': 'Inp_RSI_LevelUP', 'py': 'Inp_RSI_LevelUP', 'param': 'Inp_RSI_LevelUP', 'type': 'double', 'default': 75.0, 'label': 'RSI Fast and Slow: Level UP', 'sinput': False}, {'mql': 'Inp_RSI_LevelDOWN', 'py': 'Inp_RSI_LevelDOWN', 'param': 'Inp_RSI_LevelDOWN', 'type': 'double', 'default': 25.0, 'label': 'RSI Fast and Slow: Level DOWN', 'sinput': False}, {'mql': 'InpLineMode', 'py': 'InpLineMode', 'param': 'InpLineMode', 'type': 'int', 'default': 0, 'label': 'Cloud mode:', 'sinput': False}, {'mql': 'Inp_RSI_Fast_ma_period', 'py': 'Inp_RSI_Fast_ma_period', 'param': 'Inp_RSI_Fast_ma_period', 'type': 'int', 'default': 5, 'label': 'RSI Fast: averaging period', 'sinput': False}, {'mql': 'Inp_RSI_Fast_applied_price', 'py': 'Inp_RSI_Fast_applied_price', 'param': 'Inp_RSI_Fast_applied_price', 'type': 'int', 'default': 1, 'label': 'RSI Fast: type of price', 'sinput': False}, {'mql': 'Inp_RSI_Slow_ma_period', 'py': 'Inp_RSI_Slow_ma_period', 'param': 'Inp_RSI_Slow_ma_period', 'type': 'int', 'default': 15, 'label': 'RSI Slow: averaging period', 'sinput': False}, {'mql': 'Inp_RSI_Slow_applied_price', 'py': 'Inp_RSI_Slow_applied_price', 'param': 'Inp_RSI_Slow_applied_price', 'type': 'int', 'default': 1, 'label': 'RSI Slow: type of price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_LINE_MODE
fast = 0
slow = 1
h_l = 2
_enum('ENUM_LINE_MODE', {0: 'fast', 1: 'slow', 2: 'h_l'})

# ---- inputs and global variables
Inp_RSI_LevelUP = _input('Inp_RSI_LevelUP', 75.0)  # RSI Fast and Slow: Level UP
Inp_RSI_LevelDOWN = _input('Inp_RSI_LevelDOWN', 25.0)  # RSI Fast and Slow: Level DOWN
InpLineMode = _input('InpLineMode', fast)  # Cloud mode:
Inp_RSI_Fast_ma_period = _input('Inp_RSI_Fast_ma_period', 5)  # RSI Fast: averaging period
Inp_RSI_Fast_applied_price = _input('Inp_RSI_Fast_applied_price', PRICE_CLOSE)  # RSI Fast: type of price
Inp_RSI_Slow_ma_period = _input('Inp_RSI_Slow_ma_period', 15)  # RSI Slow: averaging period
Inp_RSI_Slow_applied_price = _input('Inp_RSI_Slow_applied_price', PRICE_CLOSE)  # RSI Slow: type of price
RSIFastBuffer = Arr(0, 0.0)
RSISlowBuffer = Arr(0, 0.0)
Cloud_Up1_Buffer = Arr(0, 0.0)
Cloud_Up2_Buffer = Arr(0, 0.0)
Cloud_Down1_Buffer = Arr(0, 0.0)
Cloud_Down2_Buffer = Arr(0, 0.0)
handle_iRSI_Fast = 0  # variable for storing the handle of the iRSI indicator
handle_iRSI_Slow = 0  # variable for storing the handle of the iRSI indicator
bars_calculated = 0  # we will keep the number of values in the Relative Strength Index indicators
m_init_error = False  # error on InInit

def OnInit():
    global handle_iRSI_Fast, handle_iRSI_Slow, m_init_error
    SetIndexBuffer(0, RSIFastBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, RSISlowBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, Cloud_Up1_Buffer, INDICATOR_DATA)
    SetIndexBuffer(3, Cloud_Up2_Buffer, INDICATOR_DATA)
    SetIndexBuffer(4, Cloud_Down1_Buffer, INDICATOR_DATA)
    SetIndexBuffer(5, Cloud_Down2_Buffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, Inp_RSI_LevelUP)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, Inp_RSI_LevelDOWN)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Inp_RSI_Fast_ma_period)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, Inp_RSI_Slow_ma_period)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSI Dual Cloud(' + IntegerToString(Inp_RSI_Fast_ma_period) + ',' + IntegerToString(Inp_RSI_Slow_ma_period) + ')')
    handle_iRSI_Fast = iRSI(Symbol(), Period(), Inp_RSI_Fast_ma_period, Inp_RSI_Fast_applied_price)
    if handle_iRSI_Fast == INVALID_HANDLE:
        PrintFormat("Failed to create handle of the iRSI indicator ('Fast') for the symbol %s/%s, error code %d", Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    handle_iRSI_Slow = iRSI(Symbol(), Period(), Inp_RSI_Slow_ma_period, Inp_RSI_Slow_applied_price)
    if handle_iRSI_Slow == INVALID_HANDLE:
        PrintFormat("Failed to create handle of the iRSI indicator ('Slow') for the symbol %s/%s, error code %d", Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    values_to_copy = 0
    calculated_fast = BarsCalculated(handle_iRSI_Fast)
    if calculated_fast <= 0:
        PrintFormat('BarsCalculated(handle_iRSI_Fast) returned %d, error code %d', calculated_fast, GetLastError())
        return 0
    calculated_slow = BarsCalculated(handle_iRSI_Slow)
    if calculated_slow <= 0:
        PrintFormat('BarsCalculated(handle_iRSI_Slow) returned %d, error code %d', calculated_slow, GetLastError())
        return 0
    if calculated_fast != calculated_slow:
        PrintFormat('BarsCalculated(handle_iRSI_Fast) returned %d, BarsCalculated(handle_iRSI_Slow) returned %d', calculated_fast, calculated_slow)
        return 0
    calculated = calculated_fast
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBuffer(RSIFastBuffer, handle_iRSI_Fast, values_to_copy):
        return 0
    if not FillArrayFromBuffer(RSISlowBuffer, handle_iRSI_Slow, values_to_copy):
        return 0
    bars_calculated = calculated
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 0
    for i in range(limit, rates_total):
        if InpLineMode == fast:
            Cloud_Up1_Buffer[i] = 100.0
            Cloud_Up2_Buffer[i] = RSIFastBuffer[i]
            Cloud_Down1_Buffer[i] = 0.0
            Cloud_Down2_Buffer[i] = RSIFastBuffer[i]
            continue
        if InpLineMode == slow:
            Cloud_Up1_Buffer[i] = 100.0
            Cloud_Up2_Buffer[i] = RSISlowBuffer[i]
            Cloud_Down1_Buffer[i] = 0.0
            Cloud_Down2_Buffer[i] = RSISlowBuffer[i]
            continue
        Cloud_Up1_Buffer[i] = 100.0
        Cloud_Up2_Buffer[i] = (RSIFastBuffer[i] if (RSIFastBuffer[i] > RSISlowBuffer[i]) else RSISlowBuffer[i])
        Cloud_Down1_Buffer[i] = 0.0
        Cloud_Down2_Buffer[i] = (RSIFastBuffer[i] if (RSIFastBuffer[i] < RSISlowBuffer[i]) else RSISlowBuffer[i])
    return rates_total

def FillArrayFromBuffer(rsi_buffer, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, 0, amount, rsi_buffer) < 0:
        PrintFormat('Failed to copy data from the iRSI indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    if handle_iRSI_Fast != INVALID_HANDLE:
        IndicatorRelease(handle_iRSI_Fast)
    if handle_iRSI_Slow != INVALID_HANDLE:
        IndicatorRelease(handle_iRSI_Slow)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSIDualCloud(_MQL5Indicator):
    name = 'RSI Dual Cloud'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_RSI_LevelUP': 75.0,  # RSI Fast and Slow: Level UP
        'Inp_RSI_LevelDOWN': 25.0,  # RSI Fast and Slow: Level DOWN
        'InpLineMode': _Choice({0: 'Fast', 1: 'Slow', 2: 'Highest Lowest'}, default=0),  # Cloud mode:
        'Inp_RSI_Fast_ma_period': 5,  # RSI Fast: averaging period
        'Inp_RSI_Fast_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # RSI Fast: type of price
        'Inp_RSI_Slow_ma_period': 15,  # RSI Slow: averaging period
        'Inp_RSI_Slow_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # RSI Slow: type of price
    }
    y_range = (0.0, 100.0)

