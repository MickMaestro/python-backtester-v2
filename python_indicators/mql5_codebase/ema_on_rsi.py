"""EMA on RSI — converted from MQL5: MQL5 Indicators/EMA on RSI/EMA on RSI.mq5

Copyright: Created with EABuilder.com; Link: https://eabuilder.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Created with EABuilder.com', 'link': 'https://eabuilder.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16755200]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'EMA on RSI'}, 'levels': [], 'description': [''], 'name': 'EMA on RSI', 'source': 'MQL5 Indicators/EMA on RSI/EMA on RSI.mq5', 'folder': 'EMA on RSI', 'inputs': [{'mql': 'RSI_Period', 'py': 'RSI_Period', 'param': 'RSI_Period', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'EMA_Period', 'py': 'EMA_Period', 'param': 'EMA_Period', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Buffer1 = Arr(0, 0.0)
RSI_Period = _input('RSI_Period', 21)
EMA_Period = _input('EMA_Period', 21)
myPoint = 0.0  # initialized in OnInit
RSI_handle = 0
RSI = Arr(0, 0.0)
MA_handle = 0
MA = Arr(0, 0.0)

def myAlert(type_, message):
    if type_ == 'print':
        Print(message)
    elif type_ == 'error':
        Print(type_ + ' | EMA on RSI @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
    elif type_ == 'order':
        pass
    elif type_ == 'modify':
        pass

def OnInit():
    global MA_handle, RSI_handle, myPoint
    SetIndexBuffer(0, Buffer1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    myPoint = Point()
    if Digits() == 5 or Digits() == 3:
        myPoint *= 10
    RSI_handle = iRSI(None, PERIOD_CURRENT, RSI_Period, PRICE_CLOSE)
    if RSI_handle < 0:
        Print('The creation of iRSI has failed: RSI_handle=', INVALID_HANDLE)
        Print('Runtime error = ', GetLastError())
        return INIT_FAILED
    MA_handle = iMA(None, PERIOD_CURRENT, EMA_Period, 0, MODE_EMA, RSI_handle)
    if MA_handle < 0:
        Print('The creation of iMA has failed: MA_handle=', INVALID_HANDLE)
        Print('Runtime error = ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = rates_total - prev_calculated
    ArraySetAsSeries(Buffer1, True)
    if prev_calculated < 1:
        ArrayInitialize(Buffer1, 0)
    else:
        limit += 1
    if BarsCalculated(MA_handle) <= 0:
        return 0
    if CopyBuffer(MA_handle, 0, 0, rates_total, MA) <= 0:
        return rates_total
    ArraySetAsSeries(MA, True)
    for i in range(limit - 1, 0 - 1, -1):
        if i >= MathMin(5000 - 1, rates_total - 1 - 50):
            continue
        if True:
            Buffer1[i] = MA[i]
        else:
            Buffer1[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EMAOnRSI(_MQL5Indicator):
    name = 'EMA on RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSI_Period': 21,
        'EMA_Period': 21,
    }

