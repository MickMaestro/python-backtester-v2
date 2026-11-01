"""ATR in Percentage of Price — converted from MQL5: MQL5 Indicators/Percentage of price movement per candle - Simple and Crucial/ATR in Percentage of Price.mq5

Copyright: Created by abfs.tech; Link: https://www.abfs.tech; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Created by abfs.tech', 'link': 'https://www.abfs.tech', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16755200]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'ATR as Percentage of Price'}, 'levels': [], 'description': [''], 'name': 'ATR in Percentage of Price', 'source': 'MQL5 Indicators/Percentage of price movement per candle - Simple and Crucial/ATR in Percentage of Price.mq5', 'folder': 'Percentage of price movement per candle - Simple and Crucial', 'inputs': [{'mql': 'Period1', 'py': 'Period1', 'param': 'Period1', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Buffer1 = Arr(0, 0.0)
Period1 = _input('Period1', 14)
myPoint = 0.0  # initialized in OnInit
ATR_handle = 0
ATR = Arr(0, 0.0)
Open = Arr(0, 0.0)

def myAlert(type_, message):
    if type_ == 'print':
        Print(message)
    elif type_ == 'error':
        Print(type_ + ' | ATR in Percentage of Price @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
    elif type_ == 'order':
        pass
    elif type_ == 'modify':
        pass

def OnInit():
    global ATR_handle, myPoint
    SetIndexBuffer(0, Buffer1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    myPoint = Point()
    if Digits() == 5 or Digits() == 3:
        myPoint *= 10
    ATR_handle = iATR(None, PERIOD_CURRENT, Period1)
    if ATR_handle < 0:
        Print('The creation of iATR has failed: ATR_handle=', INVALID_HANDLE)
        Print('Runtime error = ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = rates_total - prev_calculated
    ArraySetAsSeries(Buffer1, True)
    if prev_calculated < 1:
        ArrayInitialize(Buffer1, EMPTY_VALUE)
    else:
        limit += 1
    if BarsCalculated(ATR_handle) <= 0:
        return 0
    if CopyBuffer(ATR_handle, 0, 0, rates_total, ATR) <= 0:
        return rates_total
    ArraySetAsSeries(ATR, True)
    if CopyOpen(Symbol(), PERIOD_CURRENT, 0, rates_total, Open) <= 0:
        return rates_total
    ArraySetAsSeries(Open, True)
    for i in range(limit - 1, 0 - 1, -1):
        if i >= MathMin(5000 - 1, rates_total - 1 - 50):
            continue
        if True:
            Buffer1[i] = _fdiv(ATR[i], Open[i]) * 100
        else:
            Buffer1[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ATRInPercentageOfPrice(_MQL5Indicator):
    name = 'ATR in Percentage of Price'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period1': 14,
    }

