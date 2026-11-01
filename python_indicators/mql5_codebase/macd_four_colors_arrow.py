"""MACD Four Colors Arrow — converted from MQL5: MQL5 Indicators/MACD Four Colors Arrow/MACD Four Colors Arrow.mq5

New color Scheme
Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.001

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.001', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 12, 2: 12}, 'colors': {1: [16711680, 42495], 2: [255, 65535]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'MACD above zero', 2: 'MACD below zero'}, 'levels': [], 'description': ['New color Scheme'], 'name': 'MACD Four Colors Arrow', 'source': 'MQL5 Indicators/MACD Four Colors Arrow/MACD Four Colors Arrow.mq5', 'folder': 'MACD Four Colors Arrow', 'inputs': [{'mql': 'Inp_MACD_fast_ema_period', 'py': 'Inp_MACD_fast_ema_period', 'param': 'Inp_MACD_fast_ema_period', 'type': 'int', 'default': 12, 'label': 'MACD: period for Fast average calculation', 'sinput': False}, {'mql': 'Inp_MACD_slow_ema_period', 'py': 'Inp_MACD_slow_ema_period', 'param': 'Inp_MACD_slow_ema_period', 'type': 'int', 'default': 26, 'label': 'MACD: period for Slow average calculation', 'sinput': False}, {'mql': 'Inp_MACD_signal_period', 'py': 'Inp_MACD_signal_period', 'param': 'Inp_MACD_signal_period', 'type': 'int', 'default': 9, 'label': 'MACD: period for their difference averaging', 'sinput': False}, {'mql': 'Inp_MACD_applied_price', 'py': 'Inp_MACD_applied_price', 'param': 'Inp_MACD_applied_price', 'type': 'int', 'default': 1, 'label': 'MACD: type of price', 'sinput': False}, {'mql': 'InpAboveArrowCode', 'py': 'InpAboveArrowCode', 'param': 'InpAboveArrowCode', 'type': 'uchar', 'default': 246, 'label': "Arrow 'Above': code (font Wingdings)", 'sinput': False}, {'mql': 'InpAboveArrowShift', 'py': 'InpAboveArrowShift', 'param': 'InpAboveArrowShift', 'type': 'int', 'default': 10, 'label': "Arrow 'Above': vertical shift in pixel", 'sinput': False}, {'mql': 'InpBelowArrowCode', 'py': 'InpBelowArrowCode', 'param': 'InpBelowArrowCode', 'type': 'uchar', 'default': 248, 'label': "Arrow 'Below': code (font Wingdings)", 'sinput': False}, {'mql': 'InpBelowArrowShift', 'py': 'InpBelowArrowShift', 'param': 'InpBelowArrowShift', 'type': 'int', 'default': 10, 'label': "Arrow 'Below': vertical shift in pixel", 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_MACD_fast_ema_period = _input('Inp_MACD_fast_ema_period', 12)  # MACD: period for Fast average calculation
Inp_MACD_slow_ema_period = _input('Inp_MACD_slow_ema_period', 26)  # MACD: period for Slow average calculation
Inp_MACD_signal_period = _input('Inp_MACD_signal_period', 9)  # MACD: period for their difference averaging
Inp_MACD_applied_price = _input('Inp_MACD_applied_price', PRICE_CLOSE)  # MACD: type of price
InpAboveArrowCode = _input('InpAboveArrowCode', 246)  # Arrow 'Above': code (font Wingdings)
InpAboveArrowShift = _input('InpAboveArrowShift', 10)  # Arrow 'Above': vertical shift in pixel
InpBelowArrowCode = _input('InpBelowArrowCode', 248)  # Arrow 'Below': code (font Wingdings)
InpBelowArrowShift = _input('InpBelowArrowShift', 10)  # Arrow 'Below': vertical shift in pixel
MACDAboveZeroBuffer = Arr(0, 0.0)
MACDAboveZeroColors = Arr(0, 0.0)
MACDBelowZeroBuffer = Arr(0, 0.0)
MACDBelowZeroColors = Arr(0, 0.0)
MACDBuffer = Arr(0, 0.0)
handle_iMACD = 0  # variable for storing the handle of the iMACD indicator
bars_calculated = 0  # we will keep the number of values in the Moving Averages Convergence/Divergence indicator
m_init_error = False  # error on InInit

def OnInit():
    global handle_iMACD, m_init_error
    SetIndexBuffer(0, MACDAboveZeroBuffer)
    SetIndexBuffer(1, MACDAboveZeroColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, MACDBelowZeroBuffer)
    SetIndexBuffer(3, MACDBelowZeroColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, MACDBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, InpAboveArrowCode)
    PlotIndexSetInteger(1, PLOT_ARROW, InpBelowArrowCode)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, InpAboveArrowShift)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, -InpBelowArrowShift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, Inp_MACD_signal_period - 1)
    short_name = StringFormat('MACD Four Colors Arrow(%d,%d,%d)', Inp_MACD_fast_ema_period, Inp_MACD_slow_ema_period, Inp_MACD_signal_period)
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
    if not FillArraysFromBuffers(MACDBuffer, handle_iMACD, values_to_copy):
        return 0
    bars_calculated = calculated
    limit = prev_calculated - 1
    if prev_calculated == 0:
        MACDAboveZeroBuffer[0] = 0.0
        MACDAboveZeroColors[0] = 0.0
        MACDBelowZeroBuffer[0] = 0.0
        MACDBelowZeroColors[0] = 0.0
        limit = 1
    for i in range(limit, rates_total):
        MACDAboveZeroBuffer[i] = 0.0
        MACDAboveZeroColors[i] = 0.0
        MACDBelowZeroBuffer[i] = 0.0
        MACDBelowZeroColors[i] = 0.0
        if MACDBuffer[i] > MACDBuffer[i - 1] and MACDBuffer[i] < 0.0:
            MACDBelowZeroBuffer[i] = high[i]
            MACDBelowZeroColors[i] = 0.0
        else:
            if MACDBuffer[i] > MACDBuffer[i - 1] and MACDBuffer[i] > 0.0:
                MACDAboveZeroBuffer[i] = low[i]
                MACDAboveZeroColors[i] = 0.0
            else:
                if MACDBuffer[i] < MACDBuffer[i - 1] and MACDBuffer[i] > 0.0:
                    MACDAboveZeroBuffer[i] = low[i]
                    MACDAboveZeroColors[i] = 1.0
                else:
                    if MACDBuffer[i] < MACDBuffer[i - 1] and MACDBuffer[i] < 0.0:
                        MACDBelowZeroBuffer[i] = high[i]
                        MACDBelowZeroColors[i] = 1.0
    return rates_total

def FillArraysFromBuffers(macd_buffer, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, 0, amount, macd_buffer) < 0:
        PrintFormat('Failed to copy data from the iMACD indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    if handle_iMACD != INVALID_HANDLE:
        IndicatorRelease(handle_iMACD)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MACDFourColorsArrow(_MQL5Indicator):
    name = 'MACD Four Colors Arrow'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_MACD_fast_ema_period': 12,  # MACD: period for Fast average calculation
        'Inp_MACD_slow_ema_period': 26,  # MACD: period for Slow average calculation
        'Inp_MACD_signal_period': 9,  # MACD: period for their difference averaging
        'Inp_MACD_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MACD: type of price
        'InpAboveArrowCode': 246,  # Arrow 'Above': code (font Wingdings)
        'InpAboveArrowShift': 10,  # Arrow 'Above': vertical shift in pixel
        'InpBelowArrowCode': 248,  # Arrow 'Below': code (font Wingdings)
        'InpBelowArrowShift': 10,  # Arrow 'Below': vertical shift in pixel
    }

