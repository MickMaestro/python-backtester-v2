"""MACD AO Colors — converted from MQL5: MQL5 Indicators/MACD AO Colors/MACD AO Colors.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 10, 2: 1}, 'colors': {1: [3329330, 255], 2: [255]}, 'widths': {1: 3, 2: 1}, 'styles': {1: 0, 2: 2}, 'labels': {1: 'MACD', 2: 'Signal'}, 'levels': [], 'description': [], 'name': 'MACD AO Colors', 'source': 'MQL5 Indicators/MACD AO Colors/MACD AO Colors.mq5', 'folder': 'MACD AO Colors', 'inputs': [{'mql': 'Inp_MACD_fast_ema_period', 'py': 'Inp_MACD_fast_ema_period', 'param': 'Inp_MACD_fast_ema_period', 'type': 'int', 'default': 12, 'label': 'MACD: period for Fast average calculation', 'sinput': False}, {'mql': 'Inp_MACD_slow_ema_period', 'py': 'Inp_MACD_slow_ema_period', 'param': 'Inp_MACD_slow_ema_period', 'type': 'int', 'default': 26, 'label': 'MACD: period for Slow average calculation', 'sinput': False}, {'mql': 'Inp_MACD_signal_period', 'py': 'Inp_MACD_signal_period', 'param': 'Inp_MACD_signal_period', 'type': 'int', 'default': 9, 'label': 'MACD: period for their difference averaging', 'sinput': False}, {'mql': 'Inp_MACD_applied_price', 'py': 'Inp_MACD_applied_price', 'param': 'Inp_MACD_applied_price', 'type': 'int', 'default': 1, 'label': 'MACD: type of price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_MACD_fast_ema_period = _input('Inp_MACD_fast_ema_period', 12)  # MACD: period for Fast average calculation
Inp_MACD_slow_ema_period = _input('Inp_MACD_slow_ema_period', 26)  # MACD: period for Slow average calculation
Inp_MACD_signal_period = _input('Inp_MACD_signal_period', 9)  # MACD: period for their difference averaging
Inp_MACD_applied_price = _input('Inp_MACD_applied_price', PRICE_CLOSE)  # MACD: type of price
MACDBuffer = Arr(0, 0.0)
MACDColors = Arr(0, 0.0)
SignalBuffer = Arr(0, 0.0)
handle_iMACD = 0  # variable for storing the handle of the iMACD indicator
bars_calculated = 0  # we will keep the number of values in the Moving Averages Convergence/Divergence indicator
m_init_error = False  # error on InInit

def OnInit():
    global handle_iMACD, m_init_error
    SetIndexBuffer(0, MACDBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, MACDColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, SignalBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, Inp_MACD_signal_period - 1)
    short_name = StringFormat('MACD AO(%d,%d,%d)', Inp_MACD_fast_ema_period, Inp_MACD_slow_ema_period, Inp_MACD_signal_period)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    handle_iMACD = iMACD(Symbol(), Period(), Inp_MACD_fast_ema_period, Inp_MACD_slow_ema_period, Inp_MACD_signal_period, Inp_MACD_applied_price)
    if handle_iMACD == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMACD indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    if m_init_error:
        return 0
    values_to_copy = 0
    calculated = BarsCalculated(handle_iMACD)
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
    if not FillArraysFromBuffers(MACDBuffer, SignalBuffer, handle_iMACD, values_to_copy):
        return 0
    bars_calculated = calculated
    limit = prev_calculated - 1
    if prev_calculated == 0:
        MACDColors[0] = 0.0
        limit = 1
    for i in range(limit, rates_total):
        if MACDBuffer[i] > MACDBuffer[i - 1]:
            MACDColors[i] = 0.0
        else:
            MACDColors[i] = 1.0
    return rates_total

def FillArraysFromBuffers(macd_buffer, signal_buffer, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, 0, amount, macd_buffer) < 0:
        PrintFormat('Failed to copy data from the iMACD indicator, error code %d', GetLastError())
        return False
    if CopyBuffer(ind_handle, 1, 0, amount, signal_buffer) < 0:
        PrintFormat('Failed to copy data from the iMACD indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    if handle_iMACD != INVALID_HANDLE:
        IndicatorRelease(handle_iMACD)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MACDAOColors(_MQL5Indicator):
    name = 'MACD AO Colors'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_MACD_fast_ema_period': 12,  # MACD: period for Fast average calculation
        'Inp_MACD_slow_ema_period': 26,  # MACD: period for Slow average calculation
        'Inp_MACD_signal_period': 9,  # MACD: period for their difference averaging
        'Inp_MACD_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MACD: type of price
    }

