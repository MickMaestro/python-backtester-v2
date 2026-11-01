"""bears — converted from MQL5: MQL5 Indicators/Bears Power/bears.mq5

Bears Power
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 3}, 'colors': {1: [12632256]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Bears Power'], 'name': 'bears', 'source': 'MQL5 Indicators/Bears Power/bears.mq5', 'folder': 'Bears Power', 'inputs': [{'mql': 'InpBearsPeriod', 'py': 'InpBearsPeriod', 'param': 'InpBearsPeriod', 'type': 'int', 'default': 13, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpBearsPeriod = _input('InpBearsPeriod', 13)  # Period
ExtBearsBuffer = Arr(0, 0.0)
ExtTempBuffer = Arr(0, 0.0)
ExtEmaHandle = 0

def OnInit():
    global ExtEmaHandle
    SetIndexBuffer(0, ExtBearsBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtTempBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpBearsPeriod - 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Bears(' + _str(InpBearsPeriod) + ')')
    ExtEmaHandle = iMA(None, 0, InpBearsPeriod, 0, MODE_EMA, PRICE_CLOSE)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    limit = 0
    if rates_total < InpBearsPeriod:
        return 0
    calculated = BarsCalculated(ExtEmaHandle)
    if calculated < rates_total:
        Print('Not all data of ExtEmaHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if CopyBuffer(ExtEmaHandle, 0, 0, to_copy, ExtTempBuffer) <= 0:
        Print('getting ExtEmaHandle is failed! Error', GetLastError())
        return 0
    if prev_calculated < InpBearsPeriod:
        limit = InpBearsPeriod
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        ExtBearsBuffer[i] = Low[i] - ExtTempBuffer[i]
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Bears(_MQL5Indicator):
    name = 'bears'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpBearsPeriod': 13,  # Period
    }

