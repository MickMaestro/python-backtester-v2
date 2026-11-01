"""gann_multi_trend — converted from MQL5: MQL5 Indicators/Gann_Multi_Trend/gann_multi_trend.mq5

Copyright: Copyright © 2011, Mikhail Pashnin.; Link: http://www.mql4.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Mikhail Pashnin.', 'link': 'http://www.mql4.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [65280], 2: [255], 3: [65280], 4: [255], 5: [65280], 6: [255]}, 'widths': {1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'Bulls Gann Multi 1', 2: 'Bears Gann Multi 1', 3: 'Bulls Gann Multi 2', 4: 'Bears Gann Multi 2', 5: 'Bulls Gann Multi 3', 6: 'Bears Gann Multi 3'}, 'levels': [], 'description': [], 'name': 'gann_multi_trend', 'source': 'MQL5 Indicators/Gann_Multi_Trend/gann_multi_trend.mq5', 'folder': 'Gann_Multi_Trend', 'inputs': [{'mql': 'GannPeriod1', 'py': 'GannPeriod1', 'param': 'GannPeriod1', 'type': 'uint', 'default': 3, 'label': 'micro trend period', 'sinput': False}, {'mql': 'GannPeriod2', 'py': 'GannPeriod2', 'param': 'GannPeriod2', 'type': 'uint', 'default': 5, 'label': 'middle trend period', 'sinput': False}, {'mql': 'GannPeriod3', 'py': 'GannPeriod3', 'param': 'GannPeriod3', 'type': 'uint', 'default': 8, 'label': 'main trend period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
GannPeriod1 = _input('GannPeriod1', 3)  # micro trend period
GannPeriod2 = _input('GannPeriod2', 5)  # middle trend period
GannPeriod3 = _input('GannPeriod3', 8)  # main trend period
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
BullsBuffer1 = Arr(0, 0.0)
BearsBuffer1 = Arr(0, 0.0)
BullsBuffer2 = Arr(0, 0.0)
BearsBuffer2 = Arr(0, 0.0)
BullsBuffer3 = Arr(0, 0.0)
BearsBuffer3 = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(MathMax(MathMax(GannPeriod1, GannPeriod2), GannPeriod3))
    SetIndexBuffer(0, BullsBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, GannPeriod1)
    ArraySetAsSeries(BullsBuffer1, True)
    SetIndexBuffer(1, BearsBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, GannPeriod1)
    ArraySetAsSeries(BearsBuffer1, True)
    SetIndexBuffer(2, BullsBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, GannPeriod2)
    ArraySetAsSeries(BullsBuffer2, True)
    SetIndexBuffer(3, BearsBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, GannPeriod2)
    ArraySetAsSeries(BearsBuffer2, True)
    SetIndexBuffer(4, BullsBuffer3, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, GannPeriod3)
    ArraySetAsSeries(BullsBuffer3, True)
    SetIndexBuffer(5, BearsBuffer3, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, GannPeriod3)
    ArraySetAsSeries(BearsBuffer3, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Gann Multi Trend(', GannPeriod1, ', ', GannPeriod2, ', ', GannPeriod3, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        SetBufferData(BearsBuffer1, BullsBuffer1, GannPeriod1, bar, low, high)
        SetBufferData(BearsBuffer2, BullsBuffer2, GannPeriod2, bar, low, high)
        SetBufferData(BearsBuffer3, BullsBuffer3, GannPeriod3, bar, low, high)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def SetBufferData(upBuffer, dnBuffer, period, index, Low, High):
    max_ = High[ArrayMaximum(High, index + 1, period)]
    min_ = Low[ArrayMinimum(Low, index + 1, period)]
    if High[index] >= max_ and Low[index] > min_:
        dnBuffer[index] = EMPTY_VALUE
        upBuffer[index] = High[index]
        return
    if Low[index] <= min_ and High[index] < max_:
        upBuffer[index] = EMPTY_VALUE
        dnBuffer[index] = Low[index]
        return
    if Low[index] <= min_ and High[index] >= max_:
        upBuffer[index] = High[index]
        dnBuffer[index] = Low[index]
        return
    upBuffer[index] = upBuffer[index + 1]
    dnBuffer[index] = dnBuffer[index + 1]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GannMultiTrend(_MQL5Indicator):
    name = 'gann_multi_trend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'GannPeriod1': 3,  # micro trend period
        'GannPeriod2': 5,  # middle trend period
        'GannPeriod3': 8,  # main trend period
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

