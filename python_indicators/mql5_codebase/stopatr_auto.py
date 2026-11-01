"""StopATR_auto — converted from MQL5: MQL5 Indicators/StopATR_auto/StopATR_auto.mq5

Copyright: Copyright © 2017, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711680], 2: [255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'ATR Max', 2: 'ATR Min'}, 'levels': [], 'description': [], 'name': 'StopATR_auto', 'source': 'MQL5 Indicators/StopATR_auto/StopATR_auto.mq5', 'folder': 'StopATR_auto', 'inputs': [{'mql': 'InpAtrPeriod', 'py': 'InpAtrPeriod', 'param': 'InpAtrPeriod', 'type': 'int', 'default': 77, 'label': 'ATR period', 'sinput': False}, {'mql': 'Target', 'py': 'Target', 'param': 'Target', 'type': 'double', 'default': 2.5, 'label': 'Target', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpAtrPeriod = _input('InpAtrPeriod', 77)  # ATR period
Target = _input('Target', 2.5)  # Target
ExtATRBufferMax = Arr(0, 0.0)
ExtATRBufferMin = Arr(0, 0.0)
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
    SetIndexBuffer(0, ExtATRBufferMax, INDICATOR_DATA)
    SetIndexBuffer(1, ExtATRBufferMin, INDICATOR_DATA)
    SetIndexBuffer(2, ExtATRBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtTRBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpAtrPeriod)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, InpAtrPeriod)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    short_name = 'ATR(' + _str(ExtPeriodATR) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    PlotIndexSetString(0, PLOT_LABEL, short_name + ' Max')
    PlotIndexSetString(1, PLOT_LABEL, short_name + ' Min')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    limit = 0
    if rates_total <= ExtPeriodATR:
        return 0
    if prev_calculated == 0:
        ExtTRBuffer[0] = 0.0
        ExtATRBuffer[0] = 0.0
        ExtATRBufferMax[0] = 0.0
        ExtATRBufferMin[0] = 0.0
        i = 1
        for i in range(i, rates_total):
            ExtTRBuffer[i] = MathMax(high[i], close[i - 1]) - MathMin(low[i], close[i - 1])
        else:
            i = _range_end(i, rates_total, 1)
        firstValue = 0.0
        i = 1
        for i in range(i, ExtPeriodATR + 1):
            ExtATRBufferMax[i] = 0.0
            ExtATRBufferMin[i] = 0.0
            ExtATRBuffer[i] = 0.0
            firstValue += ExtTRBuffer[i]
        else:
            i = _range_end(i, ExtPeriodATR + 1, 1)
        firstValue = _fdiv(firstValue, ExtPeriodATR)
        ExtATRBufferMax[ExtPeriodATR] = firstValue
        ExtATRBufferMin[ExtPeriodATR] = firstValue
        ExtATRBuffer[ExtPeriodATR] = firstValue
        limit = ExtPeriodATR + 1
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        ExtTRBuffer[i] = MathMax(high[i], close[i - 1]) - MathMin(low[i], close[i - 1])
        ExtATRBuffer[i] = ExtATRBuffer[i - 1] + _fdiv(ExtTRBuffer[i] - ExtTRBuffer[i - ExtPeriodATR], ExtPeriodATR)
        ExtATRBufferMax[i] = open[i] + (Target * ExtATRBuffer[i])
        ExtATRBufferMin[i] = open[i] - (Target * ExtATRBuffer[i])
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StopATRAuto(_MQL5Indicator):
    name = 'StopATR_auto'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpAtrPeriod': 77,  # ATR period
        'Target': 2.5,  # Target
    }

