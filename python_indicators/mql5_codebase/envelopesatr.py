"""EnvelopesATR — converted from MQL5: MQL5 Indicators/Envelopes ATR MT5/EnvelopesATR.mq5

Copyright: 2016, Tor; Link: http://einvestor.ru/

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2016, Tor', 'link': 'http://einvestor.ru/', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [16711680], 2: [255], 3: [16760576], 4: [36095]}, 'widths': {}, 'styles': {}, 'labels': {1: 'MA Upper band', 2: 'MA Lower band', 3: 'ATR Upper band', 4: 'Atr Lower band'}, 'levels': [], 'description': [], 'name': 'EnvelopesATR', 'source': 'MQL5 Indicators/Envelopes ATR MT5/EnvelopesATR.mq5', 'folder': 'Envelopes ATR MT5', 'inputs': [{'mql': 'InpATRperiod', 'py': 'InpATRperiod', 'param': 'InpATRperiod', 'type': 'int', 'default': 14, 'label': 'ATR Period', 'sinput': False}, {'mql': 'InpMAPeriod', 'py': 'InpMAPeriod', 'param': 'InpMAPeriod', 'type': 'int', 'default': 14, 'label': 'MA Period', 'sinput': False}, {'mql': 'InpMAShift', 'py': 'InpMAShift', 'param': 'InpMAShift', 'type': 'int', 'default': 0, 'label': 'Shift', 'sinput': False}, {'mql': 'InpMAMethod', 'py': 'InpMAMethod', 'param': 'InpMAMethod', 'type': 'int', 'default': 0, 'label': 'MA Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'MA Applied price', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 0.1, 'label': 'Deviation %', 'sinput': False}, {'mql': 'EnvelopesType', 'py': 'EnvelopesType', 'param': 'EnvelopesType', 'type': 'int', 'default': 2, 'label': 'Envelopes Type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum TypeEnv
DEV = 0
DAT = 1
DDA = 2
_enum('TypeEnv', {0: 'DEV', 1: 'DAT', 2: 'DDA'})

# ---- inputs and global variables
InpATRperiod = _input('InpATRperiod', 14)  # ATR Period
InpMAPeriod = _input('InpMAPeriod', 14)  # MA Period
InpMAShift = _input('InpMAShift', 0)  # Shift
InpMAMethod = _input('InpMAMethod', MODE_SMA)  # MA Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # MA Applied price
InpDeviation = _input('InpDeviation', 0.1)  # Deviation %
EnvelopesType = _input('EnvelopesType', DDA)  # Envelopes Type
ExtUpBuffer = Arr(0, 0.0)
ExtDownBuffer = Arr(0, 0.0)
ExtUp2Buffer = Arr(0, 0.0)
ExtDown2Buffer = Arr(0, 0.0)
ExtMABuffer = Arr(0, 0.0)
ExtATRBuffer = Arr(0, 0.0)
ExtMAHandle = 0
ExtATRHandle = 0

def OnInit():
    global ExtATRHandle, ExtMAHandle
    if EnvelopesType == 0:
        SetIndexBuffer(0, ExtUpBuffer, INDICATOR_DATA)
        SetIndexBuffer(1, ExtDownBuffer, INDICATOR_DATA)
        SetIndexBuffer(2, ExtUp2Buffer, INDICATOR_CALCULATIONS)
        SetIndexBuffer(3, ExtDown2Buffer, INDICATOR_CALCULATIONS)
    if EnvelopesType == 1:
        SetIndexBuffer(0, ExtUpBuffer, INDICATOR_CALCULATIONS)
        SetIndexBuffer(1, ExtDownBuffer, INDICATOR_CALCULATIONS)
        SetIndexBuffer(2, ExtUp2Buffer, INDICATOR_DATA)
        SetIndexBuffer(3, ExtDown2Buffer, INDICATOR_DATA)
    if EnvelopesType == 2:
        SetIndexBuffer(0, ExtUpBuffer, INDICATOR_DATA)
        SetIndexBuffer(1, ExtDownBuffer, INDICATOR_DATA)
        SetIndexBuffer(2, ExtUp2Buffer, INDICATOR_DATA)
        SetIndexBuffer(3, ExtDown2Buffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtMABuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, ExtATRBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpMAPeriod - 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Env(' + _str(InpMAPeriod) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'Env(' + _str(InpMAPeriod) + ')Upper')
    PlotIndexSetString(1, PLOT_LABEL, 'Env(' + _str(InpMAPeriod) + ')Lower')
    PlotIndexSetString(2, PLOT_LABEL, 'EnvATR(' + _str(InpMAPeriod) + ')Upper')
    PlotIndexSetString(3, PLOT_LABEL, 'EnvATR(' + _str(InpMAPeriod) + ')Lower')
    PlotIndexSetInteger(0, PLOT_SHIFT, InpMAShift)
    PlotIndexSetInteger(1, PLOT_SHIFT, InpMAShift)
    PlotIndexSetInteger(2, PLOT_SHIFT, InpMAShift)
    PlotIndexSetInteger(3, PLOT_SHIFT, InpMAShift)
    ExtMAHandle = iMA(None, 0, InpMAPeriod, 0, InpMAMethod, InpAppliedPrice)
    ExtATRHandle = iATR(None, 0, InpATRperiod)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    limit = 0
    if rates_total < InpMAPeriod:
        return 0
    calculated = BarsCalculated(ExtMAHandle)
    if calculated < rates_total:
        Print('Not all data of ExtMAHandle is calculated (', calculated, 'bars ). Error', GetLastError())
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
    if CopyBuffer(ExtMAHandle, 0, 0, to_copy, ExtMABuffer) <= 0:
        Print('Getting MA data is failed! Error', GetLastError())
        return 0
    if CopyBuffer(ExtATRHandle, 0, 0, to_copy, ExtATRBuffer) <= 0:
        Print('Getting ATR data is failed! Error', GetLastError())
        return 0
    limit = prev_calculated - 1
    if limit < InpMAPeriod:
        limit = InpMAPeriod
    i = limit
    for i in range(i, rates_total):
        ExtUpBuffer[i] = EMPTY_VALUE
        ExtDownBuffer[i] = EMPTY_VALUE
        ExtUp2Buffer[i] = EMPTY_VALUE
        ExtDown2Buffer[i] = EMPTY_VALUE
        if EnvelopesType == 0 or EnvelopesType == 2:
            ExtUpBuffer[i] = (1 + (InpDeviation / 100.0)) * ExtMABuffer[i]
            ExtDownBuffer[i] = (1 - (InpDeviation / 100.0)) * ExtMABuffer[i]
        if EnvelopesType == 1 or EnvelopesType == 2:
            ExtUp2Buffer[i] = ExtMABuffer[i] + ExtATRBuffer[i]
            ExtDown2Buffer[i] = ExtMABuffer[i] - ExtATRBuffer[i]
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EnvelopesATR(_MQL5Indicator):
    name = 'EnvelopesATR'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpATRperiod': 14,  # ATR Period
        'InpMAPeriod': 14,  # MA Period
        'InpMAShift': 0,  # Shift
        'InpMAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA Applied price
        'InpDeviation': 0.1,  # Deviation %
        'EnvelopesType': _Choice({0: 'Deviation %', 1: 'Deviation by ATR', 2: 'Deviation % + Deviation by ATR'}, default=2),  # Envelopes Type
    }

