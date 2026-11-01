"""Two iMA Formula — converted from MQL5: MQL5 Indicators/Two iMA Formula/Two iMA Formula.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.004

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.004', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [3329434]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Two iMA Formula'}, 'levels': [], 'description': [], 'name': 'Two iMA Formula', 'source': 'MQL5 Indicators/Two iMA Formula/Two iMA Formula.mq5', 'folder': 'Two iMA Formula', 'inputs': [{'mql': 'Inp_MA_Fast_ma_period', 'py': 'Inp_MA_Fast_ma_period', 'param': 'Inp_MA_Fast_ma_period', 'type': 'int', 'default': 9, 'label': 'MA Fast: averaging period', 'sinput': False}, {'mql': 'Inp_MA_Fast_ma_shift', 'py': 'Inp_MA_Fast_ma_shift', 'param': 'Inp_MA_Fast_ma_shift', 'type': 'int', 'default': 0, 'label': 'MA Fast: horizontal shift', 'sinput': False}, {'mql': 'Inp_MA_Fast_ma_method', 'py': 'Inp_MA_Fast_ma_method', 'param': 'Inp_MA_Fast_ma_method', 'type': 'int', 'default': 0, 'label': 'MA Fast: smoothing type', 'sinput': False}, {'mql': 'Inp_MA_Fast_applied_price', 'py': 'Inp_MA_Fast_applied_price', 'param': 'Inp_MA_Fast_applied_price', 'type': 'int', 'default': 1, 'label': 'MA Fast: type of price', 'sinput': False}, {'mql': 'Inp_MA_Slow_ma_period', 'py': 'Inp_MA_Slow_ma_period', 'param': 'Inp_MA_Slow_ma_period', 'type': 'int', 'default': 26, 'label': 'MA Slow: averaging period', 'sinput': False}, {'mql': 'Inp_MA_Slow_ma_shift', 'py': 'Inp_MA_Slow_ma_shift', 'param': 'Inp_MA_Slow_ma_shift', 'type': 'int', 'default': 0, 'label': 'MA Slow: horizontal shift', 'sinput': False}, {'mql': 'Inp_MA_Slow_ma_method', 'py': 'Inp_MA_Slow_ma_method', 'param': 'Inp_MA_Slow_ma_method', 'type': 'int', 'default': 0, 'label': 'MA Slow: smoothing type', 'sinput': False}, {'mql': 'Inp_MA_Slow_applied_price', 'py': 'Inp_MA_Slow_applied_price', 'param': 'Inp_MA_Slow_applied_price', 'type': 'int', 'default': 1, 'label': 'MA Slow: type of price', 'sinput': False}, {'mql': 'InpFormula', 'py': 'InpFormula', 'param': 'InpFormula', 'type': 'int', 'default': 0, 'label': 'Formula:', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_FORMULA
f_0 = 0
f_1 = 1
f_2 = 2
_enum('ENUM_FORMULA', {0: 'f_0', 1: 'f_1', 2: 'f_2'})

# ---- inputs and global variables
Inp_MA_Fast_ma_period = _input('Inp_MA_Fast_ma_period', 9)  # MA Fast: averaging period
Inp_MA_Fast_ma_shift = _input('Inp_MA_Fast_ma_shift', 0)  # MA Fast: horizontal shift
Inp_MA_Fast_ma_method = _input('Inp_MA_Fast_ma_method', MODE_SMA)  # MA Fast: smoothing type
Inp_MA_Fast_applied_price = _input('Inp_MA_Fast_applied_price', PRICE_CLOSE)  # MA Fast: type of price
Inp_MA_Slow_ma_period = _input('Inp_MA_Slow_ma_period', 26)  # MA Slow: averaging period
Inp_MA_Slow_ma_shift = _input('Inp_MA_Slow_ma_shift', 0)  # MA Slow: horizontal shift
Inp_MA_Slow_ma_method = _input('Inp_MA_Slow_ma_method', MODE_SMA)  # MA Slow: smoothing type
Inp_MA_Slow_applied_price = _input('Inp_MA_Slow_applied_price', PRICE_CLOSE)  # MA Slow: type of price
InpFormula = _input('InpFormula', f_0)  # Formula:
Two_iMA_Buffer = Arr(0, 0.0)
FastBuffer = Arr(0, 0.0)
SlowBuffer = Arr(0, 0.0)
handle_iMA_Fast = 0  # variable for storing the handle of the iMA indicator
handle_iMA_Slow = 0  # variable for storing the handle of the iMA indicator
bars_calculated = 0  # we will keep the number of values in the Moving Average indicator
m_init_error = False  # error on InInit

def OnInit():
    global handle_iMA_Fast, handle_iMA_Slow, m_init_error
    SetIndexBuffer(0, Two_iMA_Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, FastBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, SlowBuffer, INDICATOR_CALCULATIONS)
    handle_iMA_Fast = iMA(Symbol(), Period(), Inp_MA_Fast_ma_period, Inp_MA_Fast_ma_shift, Inp_MA_Fast_ma_method, Inp_MA_Fast_applied_price)
    if handle_iMA_Fast == INVALID_HANDLE:
        PrintFormat("Failed to create handle of the iMA ('Fast') indicator for the symbol %s/%s, error code %d", Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    handle_iMA_Slow = iMA(Symbol(), Period(), Inp_MA_Slow_ma_period, Inp_MA_Slow_ma_shift, Inp_MA_Slow_ma_method, Inp_MA_Slow_applied_price)
    if handle_iMA_Slow == INVALID_HANDLE:
        PrintFormat("Failed to create handle of the iMA ('Slow') indicator for the symbol %s/%s, error code %d", Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    mode_fast = ""
    _sw1 = Inp_MA_Fast_ma_method
    if _sw1 == MODE_EMA:
        mode_fast = 'EMA'
    elif _sw1 == MODE_LWMA:
        mode_fast = 'LWMA'
    elif _sw1 == MODE_SMA:
        mode_fast = 'SMA'
    elif _sw1 == MODE_SMMA:
        mode_fast = 'SMMA'
    else:
        mode_fast = 'unknown mode'
    price_fast = StringSubstr(EnumToString(Inp_MA_Fast_applied_price, 'ENUM_APPLIED_PRICE'), 6, -1)
    mode_slow = ""
    _sw2 = Inp_MA_Slow_ma_method
    if _sw2 == MODE_EMA:
        mode_slow = 'EMA'
    elif _sw2 == MODE_LWMA:
        mode_slow = 'LWMA'
    elif _sw2 == MODE_SMA:
        mode_slow = 'SMA'
    elif _sw2 == MODE_SMMA:
        mode_slow = 'SMMA'
    else:
        mode_slow = 'unknown mode'
    price_slow = StringSubstr(EnumToString(Inp_MA_Fast_applied_price, 'ENUM_APPLIED_PRICE'), 6, -1)
    mode_formula = ""
    _sw3 = InpFormula
    if _sw3 == f_0:
        mode_formula = 'Fast-Slow'
        PlotIndexSetString(0, PLOT_LABEL, 'Fast-Slow')
    elif _sw3 == f_1:
        mode_formula = 'Fast/Slow'
        PlotIndexSetString(0, PLOT_LABEL, 'Fast/Slow')
    else:
        mode_formula = '(Fast-Slow)/Slow'
        PlotIndexSetString(0, PLOT_LABEL, '(Fast-Slow)/Slow')
    short_name = StringFormat('Two iMA Formula(%d,%d,%s,%s)(%d,%d,%s,%s)(%s)', Inp_MA_Fast_ma_period, Inp_MA_Fast_ma_shift, mode_fast, price_fast, Inp_MA_Slow_ma_period, Inp_MA_Slow_ma_shift, mode_slow, price_slow, EnumToString(InpFormula, 'ENUM_FORMULA'))
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    if m_init_error:
        return 0
    values_to_copy = 0
    calculated_fast = BarsCalculated(handle_iMA_Fast)
    if calculated_fast <= 0:
        PrintFormat('BarsCalculated(handle_iMA_Fast) returned %d, error code %d', calculated_fast, GetLastError())
        return 0
    calculated_slow = BarsCalculated(handle_iMA_Slow)
    if calculated_slow <= 0:
        PrintFormat('BarsCalculated(handle_iMA_Slow) returned %d, error code %d', calculated_slow, GetLastError())
        return 0
    if calculated_fast != calculated_slow:
        PrintFormat('BarsCalculated(handle_iMA_Fast) returned %d, BarsCalculated(handle_iMA_Slow) returned %d', calculated_fast, calculated_slow)
        return 0
    calculated = calculated_fast
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBuffer(FastBuffer, Inp_MA_Fast_ma_shift, handle_iMA_Fast, values_to_copy):
        return 0
    if not FillArrayFromBuffer(SlowBuffer, Inp_MA_Slow_ma_shift, handle_iMA_Slow, values_to_copy):
        return 0
    bars_calculated = calculated
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 0
    for i in range(limit, rates_total):
        _sw4 = InpFormula
        if _sw4 == f_0:
            Two_iMA_Buffer[i] = FastBuffer[i] - SlowBuffer[i]
        elif _sw4 == f_1:
            if SlowBuffer[i] > 0.0:
                Two_iMA_Buffer[i] = _fdiv(FastBuffer[i], SlowBuffer[i])
            else:
                Two_iMA_Buffer[i] = 0.0
        else:
            if SlowBuffer[i] > 0.0:
                Two_iMA_Buffer[i] = _fdiv(FastBuffer[i] - SlowBuffer[i], SlowBuffer[i])
            else:
                Two_iMA_Buffer[i] = 0.0
    return rates_total

def FillArrayFromBuffer(values, shift, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, -shift, amount, values) < 0:
        PrintFormat('Failed to copy data from the iMA indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    Print('OnDeinit', ', IN')
    windows_total = _int(ChartGetInteger(0, CHART_WINDOWS_TOTAL))
    for i in range(windows_total - 1, 0 - 1, -1):
        for j in range(ChartIndicatorsTotal(0, i) - 1, 0 - 1, -1):
            name = ChartIndicatorName(0, i, j)
            Print('windows #:', i, ", indicator short name '", name, "'")
            if name == ('MA(' + IntegerToString(Inp_MA_Fast_ma_period) + ')') or name == ('MA(' + IntegerToString(Inp_MA_Slow_ma_period) + ')'):
                ChartIndicatorDelete(0, i, name)
    if handle_iMA_Fast != INVALID_HANDLE:
        IndicatorRelease(handle_iMA_Fast)
    if handle_iMA_Slow != INVALID_HANDLE:
        IndicatorRelease(handle_iMA_Slow)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TwoIMAFormula(_MQL5Indicator):
    name = 'Two iMA Formula'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_MA_Fast_ma_period': 9,  # MA Fast: averaging period
        'Inp_MA_Fast_ma_shift': 0,  # MA Fast: horizontal shift
        'Inp_MA_Fast_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA Fast: smoothing type
        'Inp_MA_Fast_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA Fast: type of price
        'Inp_MA_Slow_ma_period': 26,  # MA Slow: averaging period
        'Inp_MA_Slow_ma_shift': 0,  # MA Slow: horizontal shift
        'Inp_MA_Slow_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA Slow: smoothing type
        'Inp_MA_Slow_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA Slow: type of price
        'InpFormula': _Choice({0: 'Fast-Slow', 1: 'Fast/Slow', 2: '(Fast-Slow)/Slow'}, default=0),  # Formula:
    }

