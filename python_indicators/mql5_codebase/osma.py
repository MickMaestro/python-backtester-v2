"""osma — converted from MQL5: MQL5 Indicators/Moving Average of Oscillator (OsMA)/osma.mq5

Moving Average of Oscillator
aka MACD histogram
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 3}, 'colors': {1: [12632256]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Moving Average of Oscillator', 'aka MACD histogram'], 'name': 'osma', 'source': 'MQL5 Indicators/Moving Average of Oscillator (OsMA)/osma.mq5', 'folder': 'Moving Average of Oscillator (OsMA)', 'inputs': [{'mql': 'InpFastEMAPeriod', 'py': 'InpFastEMAPeriod', 'param': 'InpFastEMAPeriod', 'type': 'int', 'default': 12, 'label': 'Fast EMA period', 'sinput': False}, {'mql': 'InpSlowEMAPeriod', 'py': 'InpSlowEMAPeriod', 'param': 'InpSlowEMAPeriod', 'type': 'int', 'default': 26, 'label': 'Slow EMA period', 'sinput': False}, {'mql': 'InpSignalSMAPeriod', 'py': 'InpSignalSMAPeriod', 'param': 'InpSignalSMAPeriod', 'type': 'int', 'default': 9, 'label': 'Signal SMA period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpFastEMAPeriod = _input('InpFastEMAPeriod', 12)  # Fast EMA period
InpSlowEMAPeriod = _input('InpSlowEMAPeriod', 26)  # Slow EMA period
InpSignalSMAPeriod = _input('InpSignalSMAPeriod', 9)  # Signal SMA period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
ExtOsMABuffer = Arr(0, 0.0)
ExtMacdBuffer = Arr(0, 0.0)
ExtSignalBuffer = Arr(0, 0.0)
ExtFastMaBuffer = Arr(0, 0.0)
ExtSlowMaBuffer = Arr(0, 0.0)
ExtFastMaHandle = 0
ExtSlowMaHandle = 0

def OnInit():
    global ExtFastMaHandle, ExtSlowMaHandle
    SetIndexBuffer(0, ExtOsMABuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtMacdBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, ExtSignalBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtFastMaBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ExtSlowMaBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 2)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpSlowEMAPeriod + InpSignalSMAPeriod - 2)
    IndicatorSetString(INDICATOR_SHORTNAME, 'OsMA(' + _str(InpFastEMAPeriod) + ',' + _str(InpSlowEMAPeriod) + ',' + _str(InpSignalSMAPeriod) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'OsMA')
    ExtFastMaHandle = iMA(None, 0, InpFastEMAPeriod, 0, MODE_EMA, InpAppliedPrice)
    ExtSlowMaHandle = iMA(None, 0, InpSlowEMAPeriod, 0, MODE_EMA, InpAppliedPrice)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if rates_total < InpSignalSMAPeriod:
        return 0
    calculated = BarsCalculated(ExtFastMaHandle)
    if calculated < rates_total:
        Print('Not all data of ExtFastMaHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    calculated = BarsCalculated(ExtSlowMaHandle)
    if calculated < rates_total:
        Print('Not all data of ExtSlowMaHandle is calculated (', calculated, 'bars ). Error', GetLastError())
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
    if CopyBuffer(ExtFastMaHandle, 0, 0, to_copy, ExtFastMaBuffer) <= 0:
        Print('Getting fast EMA is failed! Error', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(ExtSlowMaHandle, 0, 0, to_copy, ExtSlowMaBuffer) <= 0:
        Print('Getting slow SMA is failed! Error', GetLastError())
        return 0
    i = 0
    limit = 0
    if prev_calculated == 0:
        limit = 0
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        ExtMacdBuffer[i] = ExtFastMaBuffer[i] - ExtSlowMaBuffer[i]
    else:
        i = _range_end(i, rates_total, 1)
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, InpSignalSMAPeriod, ExtMacdBuffer, ExtSignalBuffer)
    i = limit
    for i in range(i, rates_total):
        ExtOsMABuffer[i] = ExtMacdBuffer[i] - ExtSignalBuffer[i]
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Osma(_MQL5Indicator):
    name = 'osma'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpFastEMAPeriod': 12,  # Fast EMA period
        'InpSlowEMAPeriod': 26,  # Slow EMA period
        'InpSignalSMAPeriod': 9,  # Signal SMA period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

