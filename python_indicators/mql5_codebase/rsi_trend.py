"""RSI Trend — converted from MQL5: MQL5 Indicators/RSI Trend Indicator/RSI Trend.mq5

RSI Trend
Copyright: 2017, Paran Software; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2017, Paran Software', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {}, 'colors': {1: [16711680, 255]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['RSI Trend'], 'name': 'RSI Trend', 'source': 'MQL5 Indicators/RSI Trend Indicator/RSI Trend.mq5', 'folder': 'RSI Trend Indicator', 'inputs': [{'mql': 'InpUpperRSI', 'py': 'InpUpperRSI', 'param': 'InpUpperRSI', 'type': 'int', 'default': 65, 'label': 'Upper limit of RSI changes', 'sinput': False}, {'mql': 'InpLowerRSI', 'py': 'InpLowerRSI', 'param': 'InpLowerRSI', 'type': 'int', 'default': 35, 'label': 'Lower limit of RSI changes', 'sinput': False}, {'mql': 'InpRSIPeriod', 'py': 'InpRSIPeriod', 'param': 'InpRSIPeriod', 'type': 'int', 'default': 14, 'label': 'RSI Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpUpperRSI = _input('InpUpperRSI', 65)  # Upper limit of RSI changes
InpLowerRSI = _input('InpLowerRSI', 35)  # Lower limit of RSI changes
InpRSIPeriod = _input('InpRSIPeriod', 14)  # RSI Period
LineBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
ExtRSIBuffer = Arr(0, 0.0)
RSI_Handle = 0
prevVal = 0.0

def OnInit():
    global RSI_Handle
    short_name = ""
    SetIndexBuffer(0, LineBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ExtRSIBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_COLOR_SECTION)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 5)
    short_name = 'RSI (' + _str(InpUpperRSI) + ' , ' + _str(InpLowerRSI) + ') Trend '
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    PlotIndexSetString(0, PLOT_LABEL, 'RSI Trend')
    RSI_Handle = iRSI(None, 0, InpRSIPeriod, PRICE_CLOSE)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global prevVal
    i = 0
    pos = 0
    if rates_total < 2:
        return 0
    data_length = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        data_length = rates_total
    else:
        data_length = rates_total - prev_calculated
        if prev_calculated > 0:
            data_length += 1
    data_length = CopyBuffer(RSI_Handle, 0, 0, data_length, ExtRSIBuffer)
    pos = (3 if (prev_calculated == 0) else (prev_calculated - 1))
    i = pos
    for i in range(i, rates_total - 1):
        diff1 = 0.0
        diff2 = 0.0
        diff1 = ExtRSIBuffer[i] - ExtRSIBuffer[i - 1]
        diff2 = ExtRSIBuffer[i - 1] - ExtRSIBuffer[i - 2]
        if (diff1 * diff2) < 0:
            if ExtRSIBuffer[i - 1] > InpUpperRSI or ExtRSIBuffer[i - 1] < InpLowerRSI:
                hi = MathMax(MathMax(high[i], high[i - 1]), MathMax(high[i - 2], high[i - 3]))
                lo = MathMin(MathMin(low[i], low[i - 1]), MathMin(low[i - 2], low[i - 3]))
                LineBuffer[i] = (hi if (ExtRSIBuffer[i - 1] > InpUpperRSI) else lo)
                ColorBuffer[i] = (1.0 if (prevVal > LineBuffer[i]) else 0.0)
                prevVal = LineBuffer[i]
    else:
        i = _range_end(i, rates_total - 1, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSITrend(_MQL5Indicator):
    name = 'RSI Trend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpUpperRSI': 65,  # Upper limit of RSI changes
        'InpLowerRSI': 35,  # Lower limit of RSI changes
        'InpRSIPeriod': 14,  # RSI Period
    }

