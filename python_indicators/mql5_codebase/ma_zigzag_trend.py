"""MA Zigzag Trend — converted from MQL5: MQL5 Indicators/MA Zigzag Trend/MA Zigzag Trend.mq5

MA Zigzag Trend Indicator
Copyright: 2017, Paran Software; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2017, Paran Software', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 9}, 'colors': {1: [16711680, 255]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'MA Zigzag Trend'}, 'levels': [], 'description': ['MA Zigzag Trend Indicator'], 'name': 'MA Zigzag Trend', 'source': 'MQL5 Indicators/MA Zigzag Trend/MA Zigzag Trend.mq5', 'folder': 'MA Zigzag Trend', 'inputs': [{'mql': 'InpSlowPeriod', 'py': 'InpSlowPeriod', 'param': 'InpSlowPeriod', 'type': 'int', 'default': 33, 'label': 'MA Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpSlowPeriod = _input('InpSlowPeriod', 33)  # MA Period
MAZigzag = Arr(0, 0.0)
ZigzagColor = Arr(0, 0.0)
PastTrendsVal = Arr(0, 0.0)
MA_Period = 0
MA_Handle = 0
prevVal = 0.0

def OnInit():
    global MA_Handle, MA_Period
    short_name = ""
    if InpSlowPeriod < 2:
        MA_Period = 55
    else:
        MA_Period = InpSlowPeriod
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, MAZigzag)
    SetIndexBuffer(1, ZigzagColor, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, PastTrendsVal, INDICATOR_DATA)
    short_name = 'MA(' + _str(MA_Period) + ') Zigzag  '
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    short_name = 'MA Zigzag  '
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetString(0, PLOT_LABEL, short_name)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, MA_Period)
    MA_Handle = iMA(None, 0, MA_Period, 0, MODE_SMA, PRICE_CLOSE)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global prevVal
    i = 0
    Pos = 0
    if rates_total < 2:
        return 0
    data_length = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        data_length = rates_total
    else:
        data_length = rates_total - prev_calculated
        if prev_calculated > 0:
            data_length += 1
    data_length = CopyBuffer(MA_Handle, 0, 0, data_length, PastTrendsVal)
    if data_length <= 0:
        Print('Getting MA is failed! Error ', GetLastError())
        return 0
    Pos = (MA_Period if (prev_calculated == 0) else (prev_calculated - 1))
    i = Pos
    for i in range(i, rates_total - 1):
        if ((PastTrendsVal[i + 1] - PastTrendsVal[i]) * (PastTrendsVal[i] - PastTrendsVal[i - 1])) < 0:
            hi = MathMax(MathMax(high[i], high[i - 1]), MathMax(high[i - 2], high[i - 3]))
            lo = MathMin(MathMin(low[i], low[i - 1]), MathMin(low[i - 2], low[i - 3]))
            if prevVal < PastTrendsVal[i]:
                MAZigzag[i] = hi
                ZigzagColor[i] = 1.0
            else:
                MAZigzag[i] = lo
                ZigzagColor[i] = 0.0
            prevVal = MAZigzag[i]
    else:
        i = _range_end(i, rates_total - 1, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MAZigzagTrend(_MQL5Indicator):
    name = 'MA Zigzag Trend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpSlowPeriod': 33,  # MA Period
    }

