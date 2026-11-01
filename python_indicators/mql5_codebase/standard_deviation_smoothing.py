"""Standard Deviation smoothing — converted from MQL5: MQL5 Indicators/Standard Deviation smoothing/Standard Deviation smoothing.mq5

Copyright: Copyright © 2018, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.000', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [3145645]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'StdDev smoothing'}, 'levels': [], 'description': [], 'name': 'Standard Deviation smoothing', 'source': 'MQL5 Indicators/Standard Deviation smoothing/Standard Deviation smoothing.mq5', 'folder': 'Standard Deviation smoothing', 'inputs': [{'mql': 'Inp_StdDev_ma_period', 'py': 'Inp_StdDev_ma_period', 'param': 'Inp_StdDev_ma_period', 'type': 'int', 'default': 20, 'label': 'period of averaging', 'sinput': False}, {'mql': 'Inp_StdDev_ma_shift', 'py': 'Inp_StdDev_ma_shift', 'param': 'Inp_StdDev_ma_shift', 'type': 'int', 'default': 0, 'label': 'shift', 'sinput': False}, {'mql': 'Inp_StdDev_ma_method', 'py': 'Inp_StdDev_ma_method', 'param': 'Inp_StdDev_ma_method', 'type': 'int', 'default': 0, 'label': 'type of smoothing', 'sinput': False}, {'mql': 'Inp_StdDev_applied_price', 'py': 'Inp_StdDev_applied_price', 'param': 'Inp_StdDev_applied_price', 'type': 'int', 'default': 1, 'label': 'type of price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
Inp_StdDev_ma_period = _input('Inp_StdDev_ma_period', 20)  # period of averaging
Inp_StdDev_ma_shift = _input('Inp_StdDev_ma_shift', 0)  # shift
Inp_StdDev_ma_method = _input('Inp_StdDev_ma_method', MODE_SMA)  # type of smoothing
Inp_StdDev_applied_price = _input('Inp_StdDev_applied_price', PRICE_CLOSE)  # type of price
StdDevBuffer = Arr(0, 0.0)
StdDevBufferTemp = Arr(0, 0.0)
handle_iStdDev = 0  # variable for storing the handle_iStdDev of the iStdDev indicator
short_name = ""  # name of the indicator on a chart
bars_calculated = 0  # we will keep the number of values in the Standard Deviation indicator
m_weightsum = 0

def OnInit():
    global handle_iStdDev, m_weightsum, short_name
    m_weightsum = 0
    SetIndexBuffer(0, StdDevBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, StdDevBufferTemp, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_SHIFT, Inp_StdDev_ma_shift)
    handle_iStdDev = iStdDev(Symbol(), Period(), Inp_StdDev_ma_period, Inp_StdDev_ma_shift, Inp_StdDev_ma_method, Inp_StdDev_applied_price)
    if handle_iStdDev == INVALID_HANDLE:
        PrintFormat('Failed to create handle_iStdDev of the iStdDev indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        return INIT_FAILED
    short_name = StringFormat('StdDev smoothing(%d)', Inp_StdDev_ma_period)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    values_to_copy = 0
    calculated = BarsCalculated(handle_iStdDev)
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
    if not FillArrayFromBuffer(StdDevBufferTemp, Inp_StdDev_ma_shift, handle_iStdDev, values_to_copy):
        return 0
    if prev_calculated == 0:
        for i in range(0, Inp_StdDev_ma_period - 1):
            StdDevBufferTemp[i] = 0.0
    _sw1 = Inp_StdDev_ma_method
    if _sw1 == MODE_SMA:
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, 3, StdDevBufferTemp, StdDevBuffer)
    elif _sw1 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, 3, StdDevBufferTemp, StdDevBuffer)
    elif _sw1 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, 3, StdDevBufferTemp, StdDevBuffer)
    else:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, 9, StdDevBufferTemp, StdDevBuffer, _GlobRef(globals(), 'm_weightsum'))
    bars_calculated = calculated
    return rates_total

def FillArrayFromBuffer(std_buffer, std_shift, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, -std_shift, amount, std_buffer) < 0:
        PrintFormat('Failed to copy data from the iStdDev indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    Comment('')


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StandardDeviationSmoothing(_MQL5Indicator):
    name = 'Standard Deviation smoothing'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_StdDev_ma_period': 20,  # period of averaging
        'Inp_StdDev_ma_shift': 0,  # shift
        'Inp_StdDev_ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # type of smoothing
        'Inp_StdDev_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # type of price
    }

