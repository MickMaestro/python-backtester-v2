"""VIDYA N Bars Borders — converted from MQL5: MQL5 Indicators/VIDYA N Bars Borders/VIDYA N Bars Borders.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [7451452], 2: [16711680], 3: [7451452]}, 'widths': {1: 1, 2: 2, 3: 1}, 'styles': {1: 1, 2: 0, 3: 1}, 'labels': {1: 'Upper', 2: 'VIDYA', 3: 'Lower'}, 'levels': [], 'description': [], 'name': 'VIDYA N Bars Borders', 'source': 'MQL5 Indicators/VIDYA N Bars Borders/VIDYA N Bars Borders.mq5', 'folder': 'VIDYA N Bars Borders', 'inputs': [{'mql': 'Inp_VIDyA_cmo_period', 'py': 'Inp_VIDyA_cmo_period', 'param': 'Inp_VIDyA_cmo_period', 'type': 'int', 'default': 15, 'label': 'VIDyA: period for Chande Momentum', 'sinput': False}, {'mql': 'Inp_VIDyA_ema_period', 'py': 'Inp_VIDyA_ema_period', 'param': 'Inp_VIDyA_ema_period', 'type': 'int', 'default': 12, 'label': 'VIDyA: EMA smoothing period', 'sinput': False}, {'mql': 'Inp_VIDyA_ma_shift', 'py': 'Inp_VIDyA_ma_shift', 'param': 'Inp_VIDyA_ma_shift', 'type': 'int', 'default': 0, 'label': 'VIDyA: horizontal shift on the price chart', 'sinput': False}, {'mql': 'Inp_VIDyA_applied_price', 'py': 'Inp_VIDyA_applied_price', 'param': 'Inp_VIDyA_applied_price', 'type': 'int', 'default': 1, 'label': 'VIDyA: type of price', 'sinput': False}, {'mql': 'Inp_n_bars', 'py': 'Inp_n_bars', 'param': 'Inp_n_bars', 'type': 'int', 'default': 6, 'label': 'N Bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_VIDyA_cmo_period = _input('Inp_VIDyA_cmo_period', 15)  # VIDyA: period for Chande Momentum
Inp_VIDyA_ema_period = _input('Inp_VIDyA_ema_period', 12)  # VIDyA: EMA smoothing period
Inp_VIDyA_ma_shift = _input('Inp_VIDyA_ma_shift', 0)  # VIDyA: horizontal shift on the price chart
Inp_VIDyA_applied_price = _input('Inp_VIDyA_applied_price', PRICE_CLOSE)  # VIDyA: type of price
Inp_n_bars = _input('Inp_n_bars', 6)  # N Bars
UpperBuffer = Arr(0, 0.0)
VIDYABuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
iATRBuffer = Arr(0, 0.0)
handle_iVIDyA = 0  # variable for storing the handle of the iVIDyA indicator
handle_iATR = 0  # variable for storing the handle of the iATR indicator
bars_calculated = 0  # we will keep the number of values in the indicators
m_init_error = False  # error on InInit

def OnInit():
    global handle_iATR, handle_iVIDyA, m_init_error
    SetIndexBuffer(0, UpperBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, VIDYABuffer, INDICATOR_DATA)
    SetIndexBuffer(2, LowerBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, iATRBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Inp_VIDyA_ema_period + Inp_VIDyA_cmo_period - 1)
    PlotIndexSetInteger(0, PLOT_SHIFT, Inp_VIDyA_ma_shift)
    PlotIndexSetInteger(1, PLOT_SHIFT, Inp_VIDyA_ma_shift)
    PlotIndexSetInteger(2, PLOT_SHIFT, Inp_VIDyA_ma_shift)
    str_input = IntegerToString(Inp_VIDyA_cmo_period) + ',' + IntegerToString(Inp_VIDyA_ema_period) + ',' + IntegerToString(Inp_VIDyA_ma_shift) + ',' + IntegerToString(Inp_n_bars)
    IndicatorSetString(INDICATOR_SHORTNAME, 'VIDYA N Bars Borders(' + str_input + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'Upper(' + str_input + ')')
    PlotIndexSetString(1, PLOT_LABEL, 'VIDYA(' + str_input + ')')
    PlotIndexSetString(2, PLOT_LABEL, 'Lower(' + str_input + ')')
    handle_iVIDyA = iVIDyA(Symbol(), Period(), Inp_VIDyA_cmo_period, Inp_VIDyA_ema_period, Inp_VIDyA_ma_shift, Inp_VIDyA_applied_price)
    if handle_iVIDyA == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iVIDyA indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    handle_iATR = iATR(Symbol(), Period(), Inp_n_bars)
    if handle_iATR == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iATR indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    values_to_copy = 0
    calculated = BarsCalculated(handle_iVIDyA)
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
    if not FillArrayFromBuffer_1(VIDYABuffer, Inp_VIDyA_ma_shift, handle_iVIDyA, values_to_copy):
        return 0
    if not FillArrayFromBuffer_2(iATRBuffer, handle_iATR, values_to_copy):
        return 0
    bars_calculated = calculated
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 0
    for i in range(limit, rates_total):
        UpperBuffer[i] = VIDYABuffer[i] + iATRBuffer[i]
        LowerBuffer[i] = VIDYABuffer[i] - iATRBuffer[i]
    return rates_total

def FillArrayFromBuffer_1(vidya_buffer, v_shift, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, -v_shift, amount, vidya_buffer) < 0:
        PrintFormat('Failed to copy data from the iVIDyA indicator, error code %d', GetLastError())
        return False
    return True

def FillArrayFromBuffer_2(values, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, 0, amount, values) < 0:
        PrintFormat('Failed to copy data from the iATR indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    if handle_iVIDyA != INVALID_HANDLE:
        IndicatorRelease(handle_iVIDyA)
    if handle_iATR != INVALID_HANDLE:
        IndicatorRelease(handle_iATR)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VIDYANBarsBorders(_MQL5Indicator):
    name = 'VIDYA N Bars Borders'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_VIDyA_cmo_period': 15,  # VIDyA: period for Chande Momentum
        'Inp_VIDyA_ema_period': 12,  # VIDyA: EMA smoothing period
        'Inp_VIDyA_ma_shift': 0,  # VIDyA: horizontal shift on the price chart
        'Inp_VIDyA_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # VIDyA: type of price
        'Inp_n_bars': 6,  # N Bars
    }

