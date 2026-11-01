"""MA on Momentum — converted from MQL5: MQL5 Indicators/MA on Momentum/MA on Momentum.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [11186720], 2: [16748574]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Momentum', 2: 'MA on Momentum'}, 'levels': [100.0], 'description': [], 'name': 'MA on Momentum', 'source': 'MQL5 Indicators/MA on Momentum/MA on Momentum.mq5', 'folder': 'MA on Momentum', 'inputs': [{'mql': 'Inp_Momentum_mom_period', 'py': 'Inp_Momentum_mom_period', 'param': 'Inp_Momentum_mom_period', 'type': 'int', 'default': 14, 'label': 'Momentum: averaging period', 'sinput': False}, {'mql': 'Inp_Momentum_applied_price', 'py': 'Inp_Momentum_applied_price', 'param': 'Inp_Momentum_applied_price', 'type': 'int', 'default': 1, 'label': 'Momentum: type of price', 'sinput': False}, {'mql': 'Inp_MA_ma_period', 'py': 'Inp_MA_ma_period', 'param': 'Inp_MA_ma_period', 'type': 'int', 'default': 6, 'label': 'MA: averaging period', 'sinput': False}, {'mql': 'Inp_MA_ma_method', 'py': 'Inp_MA_ma_method', 'param': 'Inp_MA_ma_method', 'type': 'int', 'default': 2, 'label': 'MA: smoothing type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_Momentum_mom_period = _input('Inp_Momentum_mom_period', 14)  # Momentum: averaging period
Inp_Momentum_applied_price = _input('Inp_Momentum_applied_price', PRICE_CLOSE)  # Momentum: type of price
Inp_MA_ma_period = _input('Inp_MA_ma_period', 6)  # MA: averaging period
Inp_MA_ma_method = _input('Inp_MA_ma_method', MODE_SMMA)  # MA: smoothing type
MomentumBuffer = Arr(0, 0.0)
MAonMomentumBuffer = Arr(0, 0.0)
handle_iMomentum = 0  # variable for storing the handle of the iMomentum indicator
handle_iMA = 0  # variable for storing the handle of the iMA indicator
bars_calculated = 0  # we will keep the number of values in the Momentum and MA indicators
m_init_error = False  # error on InInit

def OnInit():
    global handle_iMA, handle_iMomentum, m_init_error
    SetIndexBuffer(0, MomentumBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, MAonMomentumBuffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, 'Momentum' + '(' + IntegerToString(Inp_Momentum_mom_period) + ')')
    PlotIndexSetString(1, PLOT_LABEL, 'MA' + '(' + IntegerToString(Inp_MA_ma_period) + ')' + ' on Momentum' + '(' + IntegerToString(Inp_Momentum_mom_period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 3)
    handle_iMomentum = iMomentum(Symbol(), Period(), Inp_Momentum_mom_period, Inp_Momentum_applied_price)
    if handle_iMomentum == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMomentum indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    handle_iMA = iMA(Symbol(), Period(), Inp_MA_ma_period, 0, Inp_MA_ma_method, handle_iMomentum)
    if handle_iMA == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMA indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    if m_init_error:
        return 0
    values_to_copy = 0
    calculated_momentum = BarsCalculated(handle_iMomentum)
    if calculated_momentum <= 0:
        PrintFormat('BarsCalculated(Momentum) returned %d, error code %d', calculated_momentum, GetLastError())
        return 0
    calculated_ma = BarsCalculated(handle_iMA)
    if calculated_ma <= 0:
        PrintFormat('BarsCalculated(MA) returned %d, error code %d', calculated_ma, GetLastError())
        return 0
    if calculated_momentum != calculated_ma:
        PrintFormat('BarsCalculated(Momentum) returned %d, BarsCalculated(MA) returned %d', calculated_momentum, calculated_ma)
        return 0
    calculated = calculated_momentum
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBufferMA(MAonMomentumBuffer, 0, handle_iMA, values_to_copy):
        return 0
    if not FillArrayFromBufferMomentum(MomentumBuffer, handle_iMomentum, values_to_copy):
        return 0
    bars_calculated = calculated
    return rates_total

def FillArrayFromBufferMA(values, shift, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, -shift, amount, values) < 0:
        PrintFormat('Failed to copy data from the iMA indicator, error code %d', GetLastError())
        return False
    return True

def FillArrayFromBufferMomentum(values, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, 0, amount, values) < 0:
        PrintFormat('Failed to copy data from the iMomentum indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    if handle_iMomentum != INVALID_HANDLE:
        IndicatorRelease(handle_iMomentum)
    if handle_iMA != INVALID_HANDLE:
        IndicatorRelease(handle_iMA)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MAOnMomentum(_MQL5Indicator):
    name = 'MA on Momentum'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_Momentum_mom_period': 14,  # Momentum: averaging period
        'Inp_Momentum_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Momentum: type of price
        'Inp_MA_ma_period': 6,  # MA: averaging period
        'Inp_MA_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # MA: smoothing type
    }

