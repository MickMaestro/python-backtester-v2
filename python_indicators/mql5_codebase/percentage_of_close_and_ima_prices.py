"""Percentage of CLose and iMA prices — converted from MQL5: MQL5 Indicators/Percentage of CLose and iMA prices/Percentage of CLose and iMA prices.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Above_MA', 2: 'Below_MA'}, 'levels': [], 'description': [], 'name': 'Percentage of CLose and iMA prices', 'source': 'MQL5 Indicators/Percentage of CLose and iMA prices/Percentage of CLose and iMA prices.mq5', 'folder': 'Percentage of CLose and iMA prices', 'inputs': [{'mql': 'Inp_MA_ma_period', 'py': 'Inp_MA_ma_period', 'param': 'Inp_MA_ma_period', 'type': 'int', 'default': 36, 'label': 'MA: averaging period', 'sinput': False}, {'mql': 'Inp_MA_ma_shift', 'py': 'Inp_MA_ma_shift', 'param': 'Inp_MA_ma_shift', 'type': 'int', 'default': 0, 'label': 'MA: horizontal shift', 'sinput': False}, {'mql': 'Inp_MA_ma_method', 'py': 'Inp_MA_ma_method', 'param': 'Inp_MA_ma_method', 'type': 'int', 'default': 0, 'label': 'MA: smoothing type', 'sinput': False}, {'mql': 'Inp_MA_applied_price', 'py': 'Inp_MA_applied_price', 'param': 'Inp_MA_applied_price', 'type': 'int', 'default': 1, 'label': 'MA: type of price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_MA_ma_period = _input('Inp_MA_ma_period', 36)  # MA: averaging period
Inp_MA_ma_shift = _input('Inp_MA_ma_shift', 0)  # MA: horizontal shift
Inp_MA_ma_method = _input('Inp_MA_ma_method', MODE_SMA)  # MA: smoothing type
Inp_MA_applied_price = _input('Inp_MA_applied_price', PRICE_CLOSE)  # MA: type of price
Above_MABuffer = Arr(0, 0.0)
Below_MABuffer = Arr(0, 0.0)
MA_Buffer = Arr(0, 0.0)
handle_iMA = 0  # variable for storing the handle of the iMA indicator
bars_calculated = 0  # we will keep the number of values in the Moving Average indicator
m_init_error = False  # error on InInit

def OnInit():
    global handle_iMA, m_init_error
    SetIndexBuffer(0, Above_MABuffer, INDICATOR_DATA)
    SetIndexBuffer(1, Below_MABuffer, INDICATOR_DATA)
    SetIndexBuffer(2, MA_Buffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    handle_iMA = iMA(Symbol(), Period(), Inp_MA_ma_period, Inp_MA_ma_shift, Inp_MA_ma_method, Inp_MA_applied_price)
    if handle_iMA == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMA indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    if m_init_error or rates_total <= (Inp_MA_ma_period * 2):
        return 0
    values_to_copy = 0
    calculated = BarsCalculated(handle_iMA)
    if calculated <= 0:
        PrintFormat('BarsCalculated(handle_iMA) returned %d, error code %d', calculated, GetLastError())
        return 0
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBuffer(MA_Buffer, Inp_MA_ma_shift, handle_iMA, values_to_copy):
        return 0
    bars_calculated = calculated
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = Inp_MA_ma_period * 2
    for i in range(limit, rates_total):
        above = 0.0
        below = 0.0
        for j in range(i - Inp_MA_ma_period + 1, i + 1):
            if close[j] > MA_Buffer[j]:
                above += 1
            if close[j] < MA_Buffer[j]:
                below += 1
            d = 0
        Above_MABuffer[i] = (above * 100.0) / float(Inp_MA_ma_period)
        Below_MABuffer[i] = (below * 100.0) / float(Inp_MA_ma_period)
    return rates_total

def FillArrayFromBuffer(values, shift, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, -shift, amount, values) < 0:
        PrintFormat('Failed to copy data from the iMA indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    if handle_iMA != INVALID_HANDLE:
        IndicatorRelease(handle_iMA)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PercentageOfCLoseAndIMAPrices(_MQL5Indicator):
    name = 'Percentage of CLose and iMA prices'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_MA_ma_period': 36,  # MA: averaging period
        'Inp_MA_ma_shift': 0,  # MA: horizontal shift
        'Inp_MA_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA: smoothing type
        'Inp_MA_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA: type of price
    }

