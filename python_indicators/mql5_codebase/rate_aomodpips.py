"""Rate_AOModPips — converted from MQL5: MQL5 Indicators/Rate_AOModPips/Rate_AOModPips.mq5

Copyright: Manel Sanchon; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Manel Sanchon', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'Rate_AOModPips'}, 'levels': [], 'description': [], 'name': 'Rate_AOModPips', 'source': 'MQL5 Indicators/Rate_AOModPips/Rate_AOModPips.mq5', 'folder': 'Rate_AOModPips', 'inputs': [{'mql': 'short_mean', 'py': 'short_mean', 'param': 'short_mean', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'long_mean', 'py': 'long_mean', 'param': 'long_mean', 'type': 'int', 'default': 30, 'label': '', 'sinput': False}, {'mql': 'meanAO', 'py': 'meanAO', 'param': 'meanAO', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'meanSpeed', 'py': 'meanSpeed', 'param': 'meanSpeed', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
short_mean = _input('short_mean', 10)
long_mean = _input('long_mean', 30)
meanAO = _input('meanAO', 7)
meanSpeed = _input('meanSpeed', 7)
ExtAOBuffer = Arr(0, 0.0)
ExtBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
SpeedAOMod = Arr(0, 0.0)
max_ = 0.0
ExtAOHandle = 0

def OnInit():
    global ExtAOHandle
    SetIndexBuffer(0, SpeedAOMod, INDICATOR_DATA)
    SetIndexBuffer(1, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ExtBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtAOBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 33)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Rate_AOModPips(' + _str(short_mean) + ',' + _str(long_mean) + ';' + _str(meanAO) + ',' + _str(meanSpeed) + ')')
    ExtAOHandle = iCustom(None, 0, 'AwesomeModPips', short_mean, long_mean, meanAO)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if rates_total <= 33:
        return 0
    calculated = BarsCalculated(ExtAOHandle)
    if calculated < rates_total:
        Print('Not all data of ExtAOHandle is calculated (', calculated, 'bars ). Error', GetLastError())
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
    if CopyBuffer(ExtAOHandle, 0, 0, to_copy, ExtAOBuffer) <= 0:
        Print('Getting fast AO is failed! Error', GetLastError())
        return 0
    i = 0
    limit = 0
    if prev_calculated <= 33:
        i = 0
        for i in range(i, 33):
            ExtBuffer[i] = 0.0
        else:
            i = _range_end(i, 33, 1)
        limit = 33
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        ExtBuffer[i] = ExtAOBuffer[i] - ExtAOBuffer[i - 1]
    else:
        i = _range_end(i, rates_total, 1)
    SmoothedMAOnBuffer(rates_total, prev_calculated, 1, meanSpeed, ExtBuffer, SpeedAOMod)
    i = limit
    for i in range(i, rates_total):
        if SpeedAOMod[i] >= SpeedAOMod[i - 1]:
            ExtColorBuffer[i] = 0.0
        else:
            ExtColorBuffer[i] = 1.0
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RateAOModPips(_MQL5Indicator):
    name = 'Rate_AOModPips'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'short_mean': 10,
        'long_mean': 30,
        'meanAO': 7,
        'meanSpeed': 7,
    }

