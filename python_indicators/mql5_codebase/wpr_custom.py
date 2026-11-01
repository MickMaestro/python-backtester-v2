"""WPR Custom — converted from MQL5: MQL5 Indicators/WPR Custom/WPR Custom.mq5

Larry Williams' Percent Range Custom
From the advisor you can set: the color of the line, the thickness of the line, the value of two levels
 - color of the line
 - thickness of the line
 - value of two levels
Copyright: Copyright © 2018, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.000', 'window': 'separate', 'indicator_maximum': 0.0, 'indicator_minimum': -100.0, 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ["Larry Williams' Percent Range Custom", 'From the advisor you can set: the color of the line, the thickness of the line, the value of two levels', ' - color of the line', ' - thickness of the line', ' - value of two levels'], 'name': 'WPR Custom', 'source': 'MQL5 Indicators/WPR Custom/WPR Custom.mq5', 'folder': 'WPR Custom', 'inputs': [{'mql': 'Inp_WPR_Period', 'py': 'Inp_WPR_Period', 'param': 'Inp_WPR_Period', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'Inp_WPR_Color', 'py': 'Inp_WPR_Color', 'param': None, 'type': 'color', 'default': 16748574, 'label': 'Color line', 'sinput': False}, {'mql': 'Inp_WPR_Width', 'py': 'Inp_WPR_Width', 'param': 'Inp_WPR_Width', 'type': 'int', 'default': 1, 'label': 'Width', 'sinput': False}, {'mql': 'Inp_WPR_Level1', 'py': 'Inp_WPR_Level1', 'param': 'Inp_WPR_Level1', 'type': 'int', 'default': -20, 'label': 'Value Level #1', 'sinput': False}, {'mql': 'Inp_WPR_Level2', 'py': 'Inp_WPR_Level2', 'param': 'Inp_WPR_Level2', 'type': 'double', 'default': -80.0, 'label': 'Value Level #2', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_WPR_Period = _input('Inp_WPR_Period', 14)  # Period
Inp_WPR_Color = _input('Inp_WPR_Color', clrDodgerBlue)  # Color line
Inp_WPR_Width = _input('Inp_WPR_Width', 1)  # Width
Inp_WPR_Level1 = _input('Inp_WPR_Level1', _int(-20.0))  # Value Level #1
Inp_WPR_Level2 = _input('Inp_WPR_Level2', -80.0)  # Value Level #2
ExtWPRBuffer = Arr(0, 0.0)
ExtPeriodWPR = 0

def OnInit():
    global ExtPeriodWPR
    if Inp_WPR_Period < 3:
        ExtPeriodWPR = 14
        Print('Incorrect InpWPRPeriod value. Indicator will use value=', ExtPeriodWPR)
    else:
        ExtPeriodWPR = Inp_WPR_Period
    IndicatorSetString(INDICATOR_SHORTNAME, '%R' + '(' + _str(ExtPeriodWPR) + ')')
    SetIndexBuffer(0, ExtWPRBuffer)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtPeriodWPR - 1)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, Inp_WPR_Color)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, Inp_WPR_Width)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, Inp_WPR_Level1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, Inp_WPR_Level2)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < ExtPeriodWPR:
        return 0
    i = prev_calculated - 1
    if i < (ExtPeriodWPR - 1):
        i = ExtPeriodWPR - 1
    while i < rates_total:
        dMaxHigh = MaxAr(high, ExtPeriodWPR, i)
        dMinLow = MinAr(low, ExtPeriodWPR, i)
        if dMaxHigh != dMinLow:
            ExtWPRBuffer[i] = _fdiv((-(dMaxHigh - close[i])) * 100, dMaxHigh - dMinLow)
        else:
            ExtWPRBuffer[i] = ExtWPRBuffer[i - 1]
        i += 1
    return rates_total

def MaxAr(array, period, cur_position):
    Highest = array[cur_position]
    for i in range(cur_position - 1, cur_position - period, -1):
        if Highest < array[i]:
            Highest = array[i]
    return Highest

def MinAr(array, period, cur_position):
    Lowest = array[cur_position]
    for i in range(cur_position - 1, cur_position - period, -1):
        if Lowest > array[i]:
            Lowest = array[i]
    return Lowest


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WPRCustom(_MQL5Indicator):
    name = 'WPR Custom'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_WPR_Period': 14,  # Period
        'Inp_WPR_Width': 1,  # Width
        'Inp_WPR_Level1': -20,  # Value Level #1
        'Inp_WPR_Level2': -80.0,  # Value Level #2
    }
    y_range = (-100.0, 0.0)

