"""corrected_average — converted from MQL5: MQL5 Indicators/Corrected Average (CA)/corrected_average.mq5

Copyright: FinGeR alias Alexander Piechotta; Link: http://www.metatrader-wiki.com; Version: 2.2

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'FinGeR alias Alexander Piechotta', 'link': 'http://www.metatrader-wiki.com', 'version': '2.2', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [55295]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Corrected Average (CA)'}, 'levels': [], 'description': [], 'name': 'corrected_average', 'source': 'MQL5 Indicators/Corrected Average (CA)/corrected_average.mq5', 'folder': 'Corrected Average (CA)', 'inputs': [{'mql': 'Periode', 'py': 'Periode', 'param': 'Periode', 'type': 'int', 'default': 35, 'label': 'Averaging Period', 'sinput': False}, {'mql': 'Methode', 'py': 'Methode', 'param': 'Methode', 'type': 'int', 'default': 0, 'label': 'Smoothing Type', 'sinput': False}, {'mql': 'appliedPrice', 'py': 'appliedPrice', 'param': 'appliedPrice', 'type': 'int', 'default': 1, 'label': 'Type of Price', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Shift of indicator', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Periode = _input('Periode', 35)  # Averaging Period
Methode = _input('Methode', MODE_SMA)  # Smoothing Type
appliedPrice = _input('appliedPrice', PRICE_CLOSE)  # Type of Price
Shift = _input('Shift', 0)  # Shift of indicator
CABuffer = Arr(0, 0.0)
MABuffer = Arr(0, 0.0)
StdDevBuffer = Arr(0, 0.0)
MA_handle = 0
StdDev_handle = 0

def OnInit():
    global MA_handle, StdDev_handle
    SetIndexBuffer(0, CABuffer, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Corrected Average (CA) (' + DoubleToString(Periode, 1) + ')')
    SetIndexBuffer(1, MABuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, StdDevBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Periode)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    MA_handle = iMA(Symbol(), Period(), Periode, Shift, Methode, appliedPrice)
    StdDev_handle = iStdDev(Symbol(), Period(), Periode, Shift, Methode, appliedPrice)
    ArraySetAsSeries(MABuffer, True)
    ArraySetAsSeries(CABuffer, True)
    ArraySetAsSeries(StdDevBuffer, True)
    return 0

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < Periode:
        return 0
    calculated = BarsCalculated(MA_handle)
    if calculated < rates_total:
        Print('Not all data of MA_handle is calculated (', calculated, ' bars ). Error', GetLastError())
        return 0
    calculated = BarsCalculated(StdDev_handle)
    if calculated < rates_total:
        Print('Not all data of StdDev_handle is calculated (', calculated, ' bars ). Error', GetLastError())
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if False:
        return 0
    if CopyBuffer(MA_handle, 0, 0, to_copy, MABuffer) <= 0:
        Print('Getting fast MA failed! Error', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(StdDev_handle, 0, 0, to_copy, StdDevBuffer) <= 0:
        Print('Getting StdDev failed! Error', GetLastError())
        return 0
    v1 = 0.0
    v2 = 0.0
    k = 0.0
    counted = prev_calculated
    if counted < 0:
        return -1
    if counted > 0:
        counted -= 1
    limit = Bars(Symbol(), Period()) - counted
    for i in range(limit - 1, 0 - 1, -1):
        if i == (Bars(Symbol(), Period()) - 1):
            CABuffer[i] = MABuffer[i]
            continue
        v1 = MathPow(StdDevBuffer[i], 2)
        v2 = MathPow(CABuffer[i + 1] - MABuffer[i], 2)
        k = 0.0
        if v2 < v1 or v2 == 0:
            k = 0.0
        else:
            k = 1 - _fdiv(v1, v2)
        CABuffer[i] = CABuffer[i + 1] + (k * (MABuffer[i] - CABuffer[i + 1]))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CorrectedAverage(_MQL5Indicator):
    name = 'corrected_average'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Periode': 35,  # Averaging Period
        'Methode': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Smoothing Type
        'appliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Type of Price
        'Shift': 0,  # Shift of indicator
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

