"""force_index — converted from MQL5: MQL5 Indicators/Force Index  (FRC)/force_index.mq5

Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'force_index', 'source': 'MQL5 Indicators/Force Index  (FRC)/force_index.mq5', 'folder': 'Force Index  (FRC)', 'inputs': [{'mql': 'InpForcePeriod', 'py': 'InpForcePeriod', 'param': 'InpForcePeriod', 'type': 'int', 'default': 13, 'label': 'Period', 'sinput': False}, {'mql': 'InpMAMethod', 'py': 'InpMAMethod', 'param': 'InpMAMethod', 'type': 'int', 'default': 0, 'label': 'MA method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpAppliedVolume', 'py': 'InpAppliedVolume', 'param': 'InpAppliedVolume', 'type': 'int', 'default': 0, 'label': 'Volumes', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpForcePeriod = _input('InpForcePeriod', 13)  # Period
InpMAMethod = _input('InpMAMethod', MODE_SMA)  # MA method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpAppliedVolume = _input('InpAppliedVolume', VOLUME_TICK)  # Volumes
ExtForceBuffer = Arr(0, 0.0)
ExtMABuffer = Arr(0, 0.0)
ExtMAHandle = 0

def OnInit():
    global ExtMAHandle
    SetIndexBuffer(0, ExtForceBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtMABuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpForcePeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Force(' + _str(InpForcePeriod) + ')')
    ExtMAHandle = iMA(None, 0, InpForcePeriod, 0, InpMAMethod, InpAppliedPrice)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    limit = 0
    if rates_total < InpForcePeriod:
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
    if prev_calculated < InpForcePeriod:
        limit = InpForcePeriod
    else:
        limit = prev_calculated - 1
    if InpAppliedVolume == VOLUME_TICK:
        i = limit
        for i in range(i, rates_total):
            ExtForceBuffer[i] = TickVolume[i] * (ExtMABuffer[i] - ExtMABuffer[i - 1])
        else:
            i = _range_end(i, rates_total, 1)
    else:
        i = limit
        for i in range(i, rates_total):
            ExtForceBuffer[i] = Volume[i] * (ExtMABuffer[i] - ExtMABuffer[i - 1])
        else:
            i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ForceIndex(_MQL5Indicator):
    name = 'force_index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpForcePeriod': 13,  # Period
        'InpMAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpAppliedVolume': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volumes
    }

