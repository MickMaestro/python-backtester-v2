"""MACD Stochastic Square — converted from MQL5: MQL5 Indicators/MACD Stochastic Square/MACD Stochastic Square.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'separate', 'indicator_minimum': 1.0, 'indicator_maximum': 4.0, 'indicator_buffers': 8, 'indicator_plots': 2}, 'types': {1: 12, 2: 12}, 'colors': {1: [16711680, 255], 2: [16711680, 255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'MACD', 2: 'STO'}, 'levels': [2.0, 3.0], 'description': [], 'name': 'MACD Stochastic Square', 'source': 'MQL5 Indicators/MACD Stochastic Square/MACD Stochastic Square.mq5', 'folder': 'MACD Stochastic Square', 'inputs': [{'mql': 'Inp_MACD_fast_ema_period', 'py': 'Inp_MACD_fast_ema_period', 'param': 'Inp_MACD_fast_ema_period', 'type': 'int', 'default': 12, 'label': 'MACD: period for Fast average calculation', 'sinput': False}, {'mql': 'Inp_MACD_slow_ema_period', 'py': 'Inp_MACD_slow_ema_period', 'param': 'Inp_MACD_slow_ema_period', 'type': 'int', 'default': 26, 'label': 'MACD: period for Slow average calculation', 'sinput': False}, {'mql': 'Inp_MACD_signal_period', 'py': 'Inp_MACD_signal_period', 'param': 'Inp_MACD_signal_period', 'type': 'int', 'default': 9, 'label': 'MACD: period for their difference averaging', 'sinput': False}, {'mql': 'Inp_MACD_applied_price', 'py': 'Inp_MACD_applied_price', 'param': 'Inp_MACD_applied_price', 'type': 'int', 'default': 1, 'label': 'MACD: type of price', 'sinput': False}, {'mql': 'Inp_STO_Kperiod', 'py': 'Inp_STO_Kperiod', 'param': 'Inp_STO_Kperiod', 'type': 'int', 'default': 5, 'label': 'Stochastic: K-period (number of bars for calculations)', 'sinput': False}, {'mql': 'Inp_STO_Dperiod', 'py': 'Inp_STO_Dperiod', 'param': 'Inp_STO_Dperiod', 'type': 'int', 'default': 3, 'label': 'Stochastic: D-period (period of first smoothing)', 'sinput': False}, {'mql': 'Inp_STO_slowing', 'py': 'Inp_STO_slowing', 'param': 'Inp_STO_slowing', 'type': 'int', 'default': 3, 'label': 'Stochastic: final smoothing', 'sinput': False}, {'mql': 'Inp_STO_ma_method', 'py': 'Inp_STO_ma_method', 'param': 'Inp_STO_ma_method', 'type': 'int', 'default': 0, 'label': 'Stochastic: type of smoothing', 'sinput': False}, {'mql': 'Inp_STO_price_field', 'py': 'Inp_STO_price_field', 'param': 'Inp_STO_price_field', 'type': 'int', 'default': 0, 'label': 'Stochastic: stochastic calculation method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_MACD_fast_ema_period = _input('Inp_MACD_fast_ema_period', 12)  # MACD: period for Fast average calculation
Inp_MACD_slow_ema_period = _input('Inp_MACD_slow_ema_period', 26)  # MACD: period for Slow average calculation
Inp_MACD_signal_period = _input('Inp_MACD_signal_period', 9)  # MACD: period for their difference averaging
Inp_MACD_applied_price = _input('Inp_MACD_applied_price', PRICE_CLOSE)  # MACD: type of price
Inp_STO_Kperiod = _input('Inp_STO_Kperiod', 5)  # Stochastic: K-period (number of bars for calculations)
Inp_STO_Dperiod = _input('Inp_STO_Dperiod', 3)  # Stochastic: D-period (period of first smoothing)
Inp_STO_slowing = _input('Inp_STO_slowing', 3)  # Stochastic: final smoothing
Inp_STO_ma_method = _input('Inp_STO_ma_method', MODE_SMA)  # Stochastic: type of smoothing
Inp_STO_price_field = _input('Inp_STO_price_field', STO_LOWHIGH)  # Stochastic: stochastic calculation method
MACDBuffer = Arr(0, 0.0)
MACDColors = Arr(0, 0.0)
STOBuffer = Arr(0, 0.0)
STOColors = Arr(0, 0.0)
iMACDBuffer = Arr(0, 0.0)
iMACDSignalBuffer = Arr(0, 0.0)
iSTOBuffer = Arr(0, 0.0)
iSTOSignalBuffer = Arr(0, 0.0)
handle_iMACD = 0  # variable for storing the handle of the iMACD indicator
handle_iStochastic = 0  # variable for storing the handle of the iStochastic indicator
bars_calculated = 0  # we will keep the number of values in the indicators
m_init_error = False  # error on InInit

def OnInit():
    global handle_iMACD, handle_iStochastic, m_init_error
    SetIndexBuffer(0, MACDBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, MACDColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, STOBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, STOColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, iMACDBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, iMACDSignalBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, iSTOBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, iSTOSignalBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    PlotIndexSetInteger(0, PLOT_ARROW, 110)
    PlotIndexSetInteger(1, PLOT_ARROW, 110)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'MACD')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'STO')
    handle_iMACD = iMACD(Symbol(), Period(), Inp_MACD_fast_ema_period, Inp_MACD_slow_ema_period, Inp_MACD_signal_period, Inp_MACD_applied_price)
    if handle_iMACD == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMACD indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    handle_iStochastic = iStochastic(Symbol(), Period(), Inp_STO_Kperiod, Inp_STO_Dperiod, Inp_STO_slowing, Inp_STO_ma_method, Inp_STO_price_field)
    if handle_iStochastic == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iStochastic indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    if m_init_error:
        return 0
    if rates_total < 9:
        return 0
    values_to_copy = 0
    calculated_macd = BarsCalculated(handle_iMACD)
    if calculated_macd <= 0:
        PrintFormat('BarsCalculated(handle_iMACD) returned %d, error code %d', calculated_macd, GetLastError())
        return 0
    calculated_sto = BarsCalculated(handle_iStochastic)
    if calculated_sto <= 0:
        PrintFormat('BarsCalculated(handle_iStochastic) returned %d, error code %d', calculated_sto, GetLastError())
        return 0
    if calculated_macd != calculated_sto:
        PrintFormat('BarsCalculated(handle_iMACD) returned %d, BarsCalculated(handle_iStochastic) returned %d,', calculated_macd, calculated_sto)
        return 0
    calculated = calculated_macd
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArraysFromBuffersMACD(iMACDBuffer, iMACDSignalBuffer, handle_iMACD, values_to_copy):
        return 0
    if not FillArraysFromBuffersSTO(iSTOBuffer, iSTOSignalBuffer, handle_iStochastic, values_to_copy):
        return 0
    bars_calculated = calculated
    limit = rates_total - values_to_copy
    if limit == 0:
        MACDBuffer[0] = 0.0
        MACDColors[0] = 0.0
        STOBuffer[0] = 0.0
        STOColors[0] = 0.0
        limit = 1
    for i in range(limit, rates_total):
        MACDBuffer[i] = 2.0
        if iMACDSignalBuffer[i] < iMACDBuffer[i]:
            MACDColors[i] = 0.0
        else:
            MACDColors[i] = 1.0
        STOBuffer[i] = 3.0
        if iSTOSignalBuffer[i] < iSTOBuffer[i]:
            STOColors[i] = 0.0
        else:
            STOColors[i] = 1.0
    return rates_total

def FillArraysFromBuffersMACD(macd_buffer, signal_buffer, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, 0, amount, macd_buffer) < 0:
        PrintFormat('Failed to copy data from the iMACD indicator, error code %d', GetLastError())
        return False
    if CopyBuffer(ind_handle, 1, 0, amount, signal_buffer) < 0:
        PrintFormat('Failed to copy data from the iMACD indicator, error code %d', GetLastError())
        return False
    return True

def FillArraysFromBuffersSTO(main_buffer, signal_buffer, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, MAIN_LINE, 0, amount, main_buffer) < 0:
        PrintFormat('Failed to copy data from the iStochastic indicator, error code %d', GetLastError())
        return False
    if CopyBuffer(ind_handle, SIGNAL_LINE, 0, amount, signal_buffer) < 0:
        PrintFormat('Failed to copy data from the iStochastic indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    if handle_iMACD != INVALID_HANDLE:
        IndicatorRelease(handle_iMACD)
    if handle_iStochastic != INVALID_HANDLE:
        IndicatorRelease(handle_iStochastic)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MACDStochasticSquare(_MQL5Indicator):
    name = 'MACD Stochastic Square'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_MACD_fast_ema_period': 12,  # MACD: period for Fast average calculation
        'Inp_MACD_slow_ema_period': 26,  # MACD: period for Slow average calculation
        'Inp_MACD_signal_period': 9,  # MACD: period for their difference averaging
        'Inp_MACD_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MACD: type of price
        'Inp_STO_Kperiod': 5,  # Stochastic: K-period (number of bars for calculations)
        'Inp_STO_Dperiod': 3,  # Stochastic: D-period (period of first smoothing)
        'Inp_STO_slowing': 3,  # Stochastic: final smoothing
        'Inp_STO_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Stochastic: type of smoothing
        'Inp_STO_price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stochastic: stochastic calculation method
    }
    y_range = (1.0, 4.0)

