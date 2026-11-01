"""MA On Stochastic Color N Bars — converted from MQL5: MQL5 Indicators/MA On Stochastic Color N Bars/MA On Stochastic Color N Bars.mq5

Copyright: Copyright © 2021, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2021, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.000', 'window': 'separate', 'indicator_minimum': 0.0, 'indicator_maximum': 100.0, 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [3329434, 16711680, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'MA on Stoch Color'}, 'levels': [], 'description': [], 'name': 'MA On Stochastic Color N Bars', 'source': 'MQL5 Indicators/MA On Stochastic Color N Bars/MA On Stochastic Color N Bars.mq5', 'folder': 'MA On Stochastic Color N Bars', 'inputs': [{'mql': 'Inp_STO_Kperiod', 'py': 'Inp_STO_Kperiod', 'param': 'Inp_STO_Kperiod', 'type': 'int', 'default': 5, 'label': 'Stochastic: K-period (number of bars for calculations)', 'sinput': False}, {'mql': 'Inp_STO_Dperiod', 'py': 'Inp_STO_Dperiod', 'param': 'Inp_STO_Dperiod', 'type': 'int', 'default': 3, 'label': 'Stochastic: D-period (period of first smoothing)', 'sinput': False}, {'mql': 'Inp_STO_slowing', 'py': 'Inp_STO_slowing', 'param': 'Inp_STO_slowing', 'type': 'int', 'default': 3, 'label': 'Stochastic: final smoothing', 'sinput': False}, {'mql': 'Inp_STO_ma_method', 'py': 'Inp_STO_ma_method', 'param': 'Inp_STO_ma_method', 'type': 'int', 'default': 0, 'label': 'Stochastic: type of smoothing', 'sinput': False}, {'mql': 'Inp_STO_price_field', 'py': 'Inp_STO_price_field', 'param': 'Inp_STO_price_field', 'type': 'int', 'default': 0, 'label': 'Stochastic: stochastic calculation method', 'sinput': False}, {'mql': 'Inp_MA_ma_period', 'py': 'Inp_MA_ma_period', 'param': 'Inp_MA_ma_period', 'type': 'int', 'default': 6, 'label': 'MA: averaging period', 'sinput': False}, {'mql': 'Inp_MA_ma_shift', 'py': 'Inp_MA_ma_shift', 'param': 'Inp_MA_ma_shift', 'type': 'int', 'default': 0, 'label': 'MA: horizontal shift', 'sinput': False}, {'mql': 'Inp_MA_ma_method', 'py': 'Inp_MA_ma_method', 'param': 'Inp_MA_ma_method', 'type': 'int', 'default': 0, 'label': 'MA: smoothing type', 'sinput': False}, {'mql': 'Inp_MA_trend_n_bars', 'py': 'Inp_MA_trend_n_bars', 'param': 'Inp_MA_trend_n_bars', 'type': 'uchar', 'default': 3, 'label': 'MA: trend N Bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_STO_Kperiod = _input('Inp_STO_Kperiod', 5)  # Stochastic: K-period (number of bars for calculations)
Inp_STO_Dperiod = _input('Inp_STO_Dperiod', 3)  # Stochastic: D-period (period of first smoothing)
Inp_STO_slowing = _input('Inp_STO_slowing', 3)  # Stochastic: final smoothing
Inp_STO_ma_method = _input('Inp_STO_ma_method', MODE_SMA)  # Stochastic: type of smoothing
Inp_STO_price_field = _input('Inp_STO_price_field', STO_LOWHIGH)  # Stochastic: stochastic calculation method
Inp_MA_ma_period = _input('Inp_MA_ma_period', 6)  # MA: averaging period
Inp_MA_ma_shift = _input('Inp_MA_ma_shift', 0)  # MA: horizontal shift
Inp_MA_ma_method = _input('Inp_MA_ma_method', MODE_SMA)  # MA: smoothing type
Inp_MA_trend_n_bars = _input('Inp_MA_trend_n_bars', 3)  # MA: trend N Bars
MAColorBuffer = Arr(0, 0.0)
MAColorColors = Arr(0, 0.0)
handle_iStochastic = 0  # variable for storing the handle of the iStochastic indicator
handle_iMA = 0  # variable for storing the handle of the iMA indicator
bars_calculated = 0  # we will keep the number of values in the Stochastic Oscillator indicator
m_init_error = False  # error on InInit

def OnInit():
    global handle_iMA, handle_iStochastic, m_init_error
    m_init_error = False
    SetIndexBuffer(0, MAColorBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, MAColorColors, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 20)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 80)
    plot_name = StringFormat('Stoch(%d,%d,%d)', Inp_STO_Kperiod, Inp_STO_Dperiod, Inp_STO_slowing)
    PlotIndexSetString(0, PLOT_LABEL, plot_name)
    _sw1 = Inp_MA_ma_method
    if _sw1 == MODE_EMA:
        plot_name = 'EMA'
    elif _sw1 == MODE_LWMA:
        plot_name = 'LWMA'
    elif _sw1 == MODE_SMA:
        plot_name = 'SMA'
    elif _sw1 == MODE_SMMA:
        plot_name = 'SMMA'
    else:
        plot_name = 'unknown ma'
    PlotIndexSetString(2, PLOT_LABEL, plot_name + '(' + IntegerToString(Inp_MA_ma_period) + ')')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Inp_STO_Kperiod + Inp_STO_slowing - 2)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, Inp_STO_Kperiod + Inp_STO_Dperiod)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, Inp_STO_Kperiod + Inp_STO_Dperiod + Inp_MA_ma_period)
    handle_iStochastic = iStochastic(Symbol(), Period(), Inp_STO_Kperiod, Inp_STO_Dperiod, Inp_STO_slowing, Inp_STO_ma_method, Inp_STO_price_field)
    if handle_iStochastic == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iStochastic indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        m_init_error = True
        return INIT_SUCCEEDED
    handle_iMA = iMA(Symbol(), Period(), Inp_MA_ma_period, Inp_MA_ma_shift, Inp_MA_ma_method, handle_iStochastic)
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
    calculated_sto = BarsCalculated(handle_iStochastic)
    if calculated_sto <= 0:
        PrintFormat('BarsCalculated() returned %d, error code %d', calculated_sto, GetLastError())
        return 0
    calculated_ma = BarsCalculated(handle_iMA)
    if calculated_ma <= 0:
        PrintFormat('BarsCalculated() returned %d, error code %d', calculated_ma, GetLastError())
        return 0
    if calculated_sto != calculated_ma:
        PrintFormat('BarsCalculated(STO) returned %d, BarsCalculated(MA) returned %d', calculated_sto, calculated_ma)
        return 0
    if (prev_calculated == 0 or calculated_sto != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated_sto > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated_sto
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBuffer(MAColorBuffer, Inp_MA_ma_shift, handle_iMA, values_to_copy):
        return 0
    bars_calculated = calculated_sto
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = Inp_MA_trend_n_bars
        for i in range(0, limit):
            MAColorColors[i] = 0.0
    for i in range(limit, rates_total):
        trend = 0
        for j in range(i - Inp_MA_trend_n_bars, i):
            if MAColorBuffer[j] < MAColorBuffer[j + 1]:
                trend += 1
            else:
                trend -= 1
        if trend == Inp_MA_trend_n_bars:
            MAColorColors[i] = 1.0
        elif (-trend) == Inp_MA_trend_n_bars:
            MAColorColors[i] = 2.0
        else:
            MAColorColors[i] = 0.0
        d = 0
    return rates_total

def FillArrayFromBuffer(values, shift, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, -shift, amount, values) < 0:
        PrintFormat('Failed to copy data from the iMA indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    if handle_iStochastic != INVALID_HANDLE:
        IndicatorRelease(handle_iStochastic)
    if handle_iMA != INVALID_HANDLE:
        IndicatorRelease(handle_iMA)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MAOnStochasticColorNBars(_MQL5Indicator):
    name = 'MA On Stochastic Color N Bars'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_STO_Kperiod': 5,  # Stochastic: K-period (number of bars for calculations)
        'Inp_STO_Dperiod': 3,  # Stochastic: D-period (period of first smoothing)
        'Inp_STO_slowing': 3,  # Stochastic: final smoothing
        'Inp_STO_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Stochastic: type of smoothing
        'Inp_STO_price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stochastic: stochastic calculation method
        'Inp_MA_ma_period': 6,  # MA: averaging period
        'Inp_MA_ma_shift': 0,  # MA: horizontal shift
        'Inp_MA_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA: smoothing type
        'Inp_MA_trend_n_bars': 3,  # MA: trend N Bars
    }
    y_range = (0.0, 100.0)

