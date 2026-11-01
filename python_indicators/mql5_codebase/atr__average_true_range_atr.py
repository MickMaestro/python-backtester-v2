"""atr — converted from MQL5: MQL5 Indicators/Average True Range (ATR)/atr.mq5

Average True Range
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {}, 'styles': {}, 'labels': {1: 'ATR'}, 'levels': [], 'description': ['Average True Range'], 'name': 'atr', 'source': 'MQL5 Indicators/Average True Range (ATR)/atr.mq5', 'folder': 'Average True Range (ATR)', 'inputs': [{'mql': 'InpAtrPeriod', 'py': 'InpAtrPeriod', 'param': 'InpAtrPeriod', 'type': 'int', 'default': 14, 'label': 'ATR period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpAtrPeriod = _input('InpAtrPeriod', 14)  # ATR period
ExtATRBuffer = Arr(0, 0.0)
ExtTRBuffer = Arr(0, 0.0)
ExtPeriodATR = 0

def OnInit():
    global ExtPeriodATR
    if InpAtrPeriod <= 0:
        ExtPeriodATR = 14
        printf('Incorrect input parameter InpAtrPeriod = %d. Indicator will use value %d for calculations.', InpAtrPeriod, ExtPeriodATR)
    else:
        ExtPeriodATR = InpAtrPeriod
    SetIndexBuffer(0, ExtATRBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtTRBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpAtrPeriod)
    short_name = 'ATR(' + _str(ExtPeriodATR) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    PlotIndexSetString(0, PLOT_LABEL, short_name)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    limit = 0
    if rates_total <= ExtPeriodATR:
        return 0
    if prev_calculated == 0:
        ExtTRBuffer[0] = 0.0
        ExtATRBuffer[0] = 0.0
        i = 1
        for i in range(i, rates_total):
            ExtTRBuffer[i] = MathMax(High[i], Close[i - 1]) - MathMin(Low[i], Close[i - 1])
        else:
            i = _range_end(i, rates_total, 1)
        firstValue = 0.0
        i = 1
        for i in range(i, ExtPeriodATR + 1):
            ExtATRBuffer[i] = 0.0
            firstValue += ExtTRBuffer[i]
        else:
            i = _range_end(i, ExtPeriodATR + 1, 1)
        firstValue = _fdiv(firstValue, ExtPeriodATR)
        ExtATRBuffer[ExtPeriodATR] = firstValue
        limit = ExtPeriodATR + 1
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        ExtTRBuffer[i] = MathMax(High[i], Close[i - 1]) - MathMin(Low[i], Close[i - 1])
        ExtATRBuffer[i] = ExtATRBuffer[i - 1] + _fdiv(ExtTRBuffer[i] - ExtTRBuffer[i - ExtPeriodATR], ExtPeriodATR)
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Atr(_MQL5Indicator):
    name = 'atr'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpAtrPeriod': 14,  # ATR period
    }

