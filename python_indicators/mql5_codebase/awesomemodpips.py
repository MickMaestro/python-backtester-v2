"""AwesomeModPips — converted from MQL5: MQL5 Indicators/AwesomeModPips/AwesomeModPips.mq5

Copyright: Manel Sanchon; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Manel Sanchon', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'AOModPips'}, 'levels': [], 'description': [], 'name': 'AwesomeModPips', 'source': 'MQL5 Indicators/AwesomeModPips/AwesomeModPips.mq5', 'folder': 'AwesomeModPips', 'inputs': [{'mql': 'shortmean', 'py': 'shortmean', 'param': 'shortmean', 'type': 'int', 'default': 30, 'label': '', 'sinput': False}, {'mql': 'longmean', 'py': 'longmean', 'param': 'longmean', 'type': 'int', 'default': 60, 'label': '', 'sinput': False}, {'mql': 'meanAO', 'py': 'meanAO', 'param': 'meanAO', 'type': 'int', 'default': 30, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
shortmean = _input('shortmean', 30)
longmean = _input('longmean', 60)
meanAO = _input('meanAO', 30)
ExtAOBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
ExtFastBuffer = Arr(0, 0.0)
ExtSlowBuffer = Arr(0, 0.0)
EMA_AOBuffer = Arr(0, 0.0)
max_ = 0.0
ExtFastEMAHandle = 0
ExtSlowEMAHandle = 0

def OnInit():
    global ExtFastEMAHandle, ExtSlowEMAHandle
    SetIndexBuffer(0, EMA_AOBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ExtAOBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtFastBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ExtSlowBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 33)
    IndicatorSetString(INDICATOR_SHORTNAME, 'AwesomeModPips(' + _str(shortmean) + ',' + _str(longmean) + ';' + _str(meanAO) + ')')
    ExtFastEMAHandle = iMA(None, 0, shortmean, 0, MODE_EMA, PRICE_CLOSE)
    ExtSlowEMAHandle = iMA(None, 0, longmean, 0, MODE_EMA, PRICE_CLOSE)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if rates_total <= 33:
        return 0
    calculated = BarsCalculated(ExtFastEMAHandle)
    if calculated < rates_total:
        Print('Not all data of ExtFastEMAHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    calculated = BarsCalculated(ExtSlowEMAHandle)
    if calculated < rates_total:
        Print('Not all data of ExtSlowEMAHandle is calculated (', calculated, 'bars ). Error', GetLastError())
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
    if CopyBuffer(ExtFastEMAHandle, 0, 0, to_copy, ExtFastBuffer) <= 0:
        Print('Getting fast EMA is failed! Error', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(ExtSlowEMAHandle, 0, 0, to_copy, ExtSlowBuffer) <= 0:
        Print('Getting slow EMA is failed! Error', GetLastError())
        return 0
    i = 0
    limit = 0
    if prev_calculated <= 33:
        i = 0
        for i in range(i, 33):
            ExtAOBuffer[i] = 0.0
        else:
            i = _range_end(i, 33, 1)
        limit = 33
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        ExtAOBuffer[i] = _fdiv(ExtFastBuffer[i] - ExtSlowBuffer[i], Point()) / 10
    else:
        i = _range_end(i, rates_total, 1)
    SmoothedMAOnBuffer(rates_total, prev_calculated, 1, meanAO, ExtAOBuffer, EMA_AOBuffer)
    i = limit
    for i in range(i, rates_total):
        if EMA_AOBuffer[i] >= EMA_AOBuffer[i - 1]:
            ExtColorBuffer[i] = 0.0
        else:
            ExtColorBuffer[i] = 1.0
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AwesomeModPips(_MQL5Indicator):
    name = 'AwesomeModPips'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'shortmean': 30,
        'longmean': 60,
        'meanAO': 30,
    }

