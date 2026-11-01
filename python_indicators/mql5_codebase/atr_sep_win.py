"""ATR_sep_win — converted from MQL5: MQL5 Indicators/Brooky Trend Strength for MT5/ATR_sep_win.mq5

Copyright: © 2023, Ryan Lawrence Johnson; Link: https://www.mql5.com/en/users/rjo/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© 2023, Ryan Lawrence Johnson', 'link': 'https://www.mql5.com/en/users/rjo/seller', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {}, 'styles': {}, 'labels': {1: 'ATR'}, 'levels': [], 'description': [], 'name': 'ATR_sep_win', 'source': 'MQL5 Indicators/Brooky Trend Strength for MT5/ATR_sep_win.mq5', 'folder': 'Brooky Trend Strength for MT5', 'inputs': [{'mql': 'InpAtrPeriod', 'py': 'InpAtrPeriod', 'param': 'InpAtrPeriod', 'type': 'int', 'default': 14, 'label': 'ATR period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpAtrPeriod = _input('InpAtrPeriod', 14)  # ATR period
ExtATRBuffer = Arr(0, 0.0)
ExtTRBuffer = Arr(0, 0.0)
ExtPeriodATR = 0

def OnInit():
    global ExtPeriodATR
    if InpAtrPeriod <= 0:
        ExtPeriodATR = 14
        PrintFormat('Incorrect input parameter InpAtrPeriod = %d. Indicator will use value %d for calculations.', InpAtrPeriod, ExtPeriodATR)
    else:
        ExtPeriodATR = InpAtrPeriod
    SetIndexBuffer(0, ExtATRBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtTRBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpAtrPeriod)
    short_name = StringFormat('ATR(%d)', ExtPeriodATR)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    PlotIndexSetString(0, PLOT_LABEL, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total <= ExtPeriodATR:
        return 0
    i = 0
    start = 0
    if prev_calculated == 0:
        ExtTRBuffer[0] = 0.0
        ExtATRBuffer[0] = 0.0
        i = 1
        for i in range(i, rates_total):
            ExtTRBuffer[i] = MathMax(high[i], close[i - 1]) - MathMin(low[i], close[i - 1])
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
        start = ExtPeriodATR + 1
    else:
        start = prev_calculated - 1
    i = start
    for i in range(i, rates_total):
        ExtTRBuffer[i] = MathMax(high[i], close[i - 1]) - MathMin(low[i], close[i - 1])
        ExtATRBuffer[i] = ExtATRBuffer[i - 1] + _fdiv(ExtTRBuffer[i] - ExtTRBuffer[i - ExtPeriodATR], ExtPeriodATR)
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ATRSepWin(_MQL5Indicator):
    name = 'ATR_sep_win'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpAtrPeriod': 14,  # ATR period
    }

