"""alfos — converted from MQL5: MQL5 Indicators/AlfOs/alfos.mq5

Alf of Oscillator
Copyright: 2009, MetaQuotes Software Corp.; Link: http://forum.liteforex.org/showthread.php?p=6688#post6688

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://forum.liteforex.org/showthread.php?p=6688#post6688', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 3}, 'colors': {1: [12632256]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Alf of Oscillator'], 'name': 'alfos', 'source': 'MQL5 Indicators/AlfOs/alfos.mq5', 'folder': 'AlfOs', 'inputs': [{'mql': 'MA1', 'py': 'MA1', 'param': 'MA1', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'MA2', 'py': 'MA2', 'param': 'MA2', 'type': 'int', 'default': 26, 'label': '', 'sinput': False}, {'mql': 'CMO1', 'py': 'CMO1', 'param': 'CMO1', 'type': 'int', 'default': 55, 'label': '', 'sinput': False}, {'mql': 'CMO2', 'py': 'CMO2', 'param': 'CMO2', 'type': 'int', 'default': 55, 'label': '', 'sinput': False}, {'mql': 'Signal', 'py': 'Signal', 'param': 'Signal', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
MA1 = _input('MA1', 12)
MA2 = _input('MA2', 26)
CMO1 = _input('CMO1', 55)
CMO2 = _input('CMO2', 55)
Signal = _input('Signal', 9)
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)
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
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, MA2 + Signal - 2)
    IndicatorSetString(INDICATOR_SHORTNAME, 'AlfOs(' + _str(MA1) + ',' + _str(MA2) + ',' + _str(Signal) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'AlfOs')
    ExtFastMaHandle = iVIDyA(None, 0, CMO1, MA1, 0, InpAppliedPrice)
    ExtSlowMaHandle = iVIDyA(None, 0, CMO2, MA2, 0, InpAppliedPrice)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if rates_total < Signal:
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
    if CopyBuffer(ExtFastMaHandle, 0, 0, to_copy, ExtFastMaBuffer) <= 0:
        Print('Getting fast EMA is failed! Error', GetLastError())
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
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, Signal, ExtMacdBuffer, ExtSignalBuffer)
    i = limit
    for i in range(i, rates_total):
        ExtOsMABuffer[i] = ExtMacdBuffer[i] - ExtSignalBuffer[i]
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Alfos(_MQL5Indicator):
    name = 'alfos'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA1': 12,
        'MA2': 26,
        'CMO1': 55,
        'CMO2': 55,
        'Signal': 9,
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
    }

