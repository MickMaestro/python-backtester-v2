"""PipsToAverage — converted from MQL5: MQL5 Indicators/PipsToAverage/PipsToAverage.mq5

Copyright: Manel Sanchon; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Manel Sanchon', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'PipsToAverage'}, 'levels': [], 'description': [], 'name': 'PipsToAverage', 'source': 'MQL5 Indicators/PipsToAverage/PipsToAverage.mq5', 'folder': 'PipsToAverage', 'inputs': [{'mql': 'Period_Average', 'py': 'Period_Average', 'param': 'Period_Average', 'type': 'int', 'default': 200, 'label': '', 'sinput': False}, {'mql': 'Period_PipsToAv', 'py': 'Period_PipsToAv', 'param': 'Period_PipsToAv', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
Period_Average = _input('Period_Average', 200)
Period_PipsToAv = _input('Period_PipsToAv', 7)
ExtBuffer = Arr(0, 0.0)
ExtEMABuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
PipsToAverage = Arr(0, 0.0)
max_ = 0.0
ExtEMAHandle = 0

def OnInit():
    global ExtEMAHandle
    SetIndexBuffer(0, PipsToAverage, INDICATOR_DATA)
    SetIndexBuffer(1, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ExtEMABuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 33)
    IndicatorSetString(INDICATOR_SHORTNAME, 'PipsToAverage(' + _str(Period_Average) + ';' + _str(Period_PipsToAv) + ')')
    ExtEMAHandle = iMA(None, 0, Period_Average, 0, MODE_EMA, PRICE_CLOSE)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if rates_total <= 33:
        return 0
    calculated = BarsCalculated(ExtEMAHandle)
    if calculated < rates_total:
        Print('Not all data of ExtEMAHandle is calculated (', calculated, 'bars ). Error', GetLastError())
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
    if CopyBuffer(ExtEMAHandle, 0, 0, to_copy, ExtEMABuffer) <= 0:
        Print('Getting EMA is failed! Error', GetLastError())
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
        ExtBuffer[i] = _fdiv(Close[i] - ExtEMABuffer[i], Point()) / 10
    else:
        i = _range_end(i, rates_total, 1)
    SmoothedMAOnBuffer(rates_total, prev_calculated, 1, Period_PipsToAv, ExtBuffer, PipsToAverage)
    i = limit
    for i in range(i, rates_total):
        if PipsToAverage[i] >= PipsToAverage[i - 1]:
            ExtColorBuffer[i] = 0.0
        else:
            ExtColorBuffer[i] = 1.0
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PipsToAverageIndicator(_MQL5Indicator):
    name = 'PipsToAverage'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period_Average': 200,
        'Period_PipsToAv': 7,
    }

