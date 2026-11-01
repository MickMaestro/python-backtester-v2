"""envelopes — converted from MQL5: MQL5 Indicators/Envelopes/envelopes.mq5

Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711680], 2: [255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Upper band', 2: 'Lower band'}, 'levels': [], 'description': [], 'name': 'envelopes', 'source': 'MQL5 Indicators/Envelopes/envelopes.mq5', 'folder': 'Envelopes', 'inputs': [{'mql': 'InpMAPeriod', 'py': 'InpMAPeriod', 'param': 'InpMAPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpMAShift', 'py': 'InpMAShift', 'param': 'InpMAShift', 'type': 'int', 'default': 0, 'label': 'Shift', 'sinput': False}, {'mql': 'InpMAMethod', 'py': 'InpMAMethod', 'param': 'InpMAMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 0.1, 'label': 'Deviation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpMAPeriod = _input('InpMAPeriod', 14)  # Period
InpMAShift = _input('InpMAShift', 0)  # Shift
InpMAMethod = _input('InpMAMethod', MODE_SMA)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpDeviation = _input('InpDeviation', 0.1)  # Deviation
ExtUpBuffer = Arr(0, 0.0)
ExtDownBuffer = Arr(0, 0.0)
ExtMABuffer = Arr(0, 0.0)
ExtMAHandle = 0

def OnInit():
    global ExtMAHandle
    SetIndexBuffer(0, ExtUpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtDownBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtMABuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpMAPeriod - 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Env(' + _str(InpMAPeriod) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'Env(' + _str(InpMAPeriod) + ')Upper')
    PlotIndexSetString(1, PLOT_LABEL, 'Env(' + _str(InpMAPeriod) + ')Lower')
    PlotIndexSetInteger(0, PLOT_SHIFT, InpMAShift)
    PlotIndexSetInteger(1, PLOT_SHIFT, InpMAShift)
    ExtMAHandle = iMA(None, 0, InpMAPeriod, 0, InpMAMethod, InpAppliedPrice)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
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
    limit = prev_calculated - 1
    if limit < InpMAPeriod:
        limit = InpMAPeriod
    i = limit
    for i in range(i, rates_total):
        ExtUpBuffer[i] = (1 + (InpDeviation / 100.0)) * ExtMABuffer[i]
        ExtDownBuffer[i] = (1 - (InpDeviation / 100.0)) * ExtMABuffer[i]
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Envelopes(_MQL5Indicator):
    name = 'envelopes'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMAPeriod': 14,  # Period
        'InpMAShift': 0,  # Shift
        'InpMAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpDeviation': 0.1,  # Deviation
    }

