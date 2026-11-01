"""rsi — converted from MQL5: MQL5 Indicators/Relative Strength Index (RSI)/rsi.mq5

Relative Strength Index
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_minimum': 0.0, 'indicator_maximum': 100.0, 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [30.0, 70.0], 'description': ['Relative Strength Index'], 'name': 'rsi', 'source': 'MQL5 Indicators/Relative Strength Index (RSI)/rsi.mq5', 'folder': 'Relative Strength Index (RSI)', 'inputs': [{'mql': 'InpPeriodRSI', 'py': 'InpPeriodRSI', 'param': 'InpPeriodRSI', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodRSI = _input('InpPeriodRSI', 14)  # Period
ExtRSIBuffer = Arr(0, 0.0)
ExtPosBuffer = Arr(0, 0.0)
ExtNegBuffer = Arr(0, 0.0)
ExtPeriodRSI = 0

def OnInit():
    global ExtPeriodRSI
    if InpPeriodRSI < 1:
        ExtPeriodRSI = 12
        Print('Incorrect value for input variable InpPeriodRSI =', InpPeriodRSI, 'Indicator will use value =', ExtPeriodRSI, 'for calculations.')
    else:
        ExtPeriodRSI = InpPeriodRSI
    SetIndexBuffer(0, ExtRSIBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtPosBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, ExtNegBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtPeriodRSI)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSI(' + _str(ExtPeriodRSI) + ')')

def OnCalculate(rates_total, prev_calculated, begin, price):
    i = 0
    diff = 0.0
    if rates_total <= ExtPeriodRSI:
        return 0
    pos = prev_calculated - 1
    if pos <= ExtPeriodRSI:
        ExtRSIBuffer[0] = 0.0
        ExtPosBuffer[0] = 0.0
        ExtNegBuffer[0] = 0.0
        SumP = 0.0
        SumN = 0.0
        i = 1
        for i in range(i, ExtPeriodRSI + 1):
            ExtRSIBuffer[i] = 0.0
            ExtPosBuffer[i] = 0.0
            ExtNegBuffer[i] = 0.0
            diff = price[i] - price[i - 1]
            SumP += (diff if (diff > 0) else 0)
            SumN += ((-diff) if (diff < 0) else 0)
        else:
            i = _range_end(i, ExtPeriodRSI + 1, 1)
        ExtPosBuffer[ExtPeriodRSI] = _fdiv(SumP, ExtPeriodRSI)
        ExtNegBuffer[ExtPeriodRSI] = _fdiv(SumN, ExtPeriodRSI)
        ExtRSIBuffer[ExtPeriodRSI] = 100.0 - _fdiv(100.0, 1.0 + _fdiv(ExtPosBuffer[ExtPeriodRSI], ExtNegBuffer[ExtPeriodRSI]))
        pos = ExtPeriodRSI + 1
    i = pos
    for i in range(i, rates_total):
        diff = price[i] - price[i - 1]
        ExtPosBuffer[i] = _fdiv((ExtPosBuffer[i - 1] * (ExtPeriodRSI - 1)) + (diff if (diff > 0.0) else 0.0), ExtPeriodRSI)
        ExtNegBuffer[i] = _fdiv((ExtNegBuffer[i - 1] * (ExtPeriodRSI - 1)) + ((-diff) if (diff < 0.0) else 0.0), ExtPeriodRSI)
        ExtRSIBuffer[i] = 100.0 - _fdiv(100.0, 1 + _fdiv(ExtPosBuffer[i], ExtNegBuffer[i]))
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Rsi(_MQL5Indicator):
    name = 'rsi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodRSI': 14,  # Period
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }
    y_range = (0.0, 100.0)

