"""rstl — converted from MQL5: MQL5 Indicators/RSTL/rstl.mq5

Copyright: Copyright 2002, Finware.ru Ltd.; Link: http://www.finware.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2002, Finware.ru Ltd.', 'link': 'http://www.finware.ru/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [13828244]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'RSTL'}, 'levels': [], 'description': [], 'name': 'rstl', 'source': 'MQL5 Indicators/RSTL/rstl.mq5', 'folder': 'RSTL', 'inputs': [{'mql': 'RSTLShift', 'py': 'RSTLShift', 'param': 'RSTLShift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of moving average in bars', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RSTLShift = _input('RSTLShift', 0)  # Horizontal shift of moving average in bars
RSTLPeriod = 99
ExtLineBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, RSTLShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, RSTLPeriod)
    shortname = Box("")
    StringConcatenate(shortname, 'RSTL(', RSTLShift, ')')
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (RSTLPeriod - 1 + begin):
        return 0
    first = 0
    bar = 0
    RSTL = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = RSTLPeriod - 1 + begin
        if begin > 0:
            PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, begin + RSTLPeriod)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        RSTL = (-0.00514293 * price[bar - 0]) - (0.00398417 * price[bar - 1]) - (0.00262594 * price[bar - 2]) - (0.00107121 * price[bar - 3]) + (0.00066887 * price[bar - 4]) + (0.00258172 * price[bar - 5]) + (0.00465269 * price[bar - 6]) + (0.00686394 * price[bar - 7]) + (0.00919334 * price[bar - 8]) + (0.0116172 * price[bar - 9]) + (0.01411056 * price[bar - 10]) + (0.01664635 * price[bar - 11]) + (0.01919533 * price[bar - 12]) + (0.02172747 * price[bar - 13]) + (0.0242132 * price[bar - 14]) + (0.02662203 * price[bar - 15]) + (0.02892446 * price[bar - 16]) + (0.03109071 * price[bar - 17]) + (0.03309496 * price[bar - 18]) + (0.03490921 * price[bar - 19]) + (0.03651145 * price[bar - 20]) + (0.03788045 * price[bar - 21]) + (0.03899804 * price[bar - 22]) + (0.03984915 * price[bar - 23]) + (0.04042329 * price[bar - 24]) + (0.04071263 * price[bar - 25]) + (0.04071263 * price[bar - 26]) + (0.04042329 * price[bar - 27]) + (0.03984915 * price[bar - 28]) + (0.03899804 * price[bar - 29]) + (0.03788045 * price[bar - 30]) + (0.03651145 * price[bar - 31]) + (0.03490921 * price[bar - 32]) + (0.03309496 * price[bar - 33]) + (0.03109071 * price[bar - 34]) + (0.02892446 * price[bar - 35]) + (0.02662203 * price[bar - 36]) + (0.0242132 * price[bar - 37]) + (0.02172747 * price[bar - 38]) + (0.01919533 * price[bar - 39]) + (0.01664635 * price[bar - 40]) + (0.01411056 * price[bar - 41]) + (0.0116172 * price[bar - 42]) + (0.00919334 * price[bar - 43]) + (0.00686394 * price[bar - 44]) + (0.00465269 * price[bar - 45]) + (0.00258172 * price[bar - 46]) + (0.00066887 * price[bar - 47]) - (0.00107121 * price[bar - 48]) - (0.00262594 * price[bar - 49]) - (0.00398417 * price[bar - 50]) - (0.00514293 * price[bar - 51]) - (0.00609634 * price[bar - 52]) - (0.00684602 * price[bar - 53]) - (0.00739452 * price[bar - 54]) - (0.00774847 * price[bar - 55]) - (0.0079163 * price[bar - 56]) - (0.0079094 * price[bar - 57]) - (0.00774085 * price[bar - 58]) - (0.00742482 * price[bar - 59]) - (0.00697718 * price[bar - 60]) - (0.00641613 * price[bar - 61]) - (0.00576108 * price[bar - 62]) - (0.00502957 * price[bar - 63]) - (0.00423873 * price[bar - 64]) - (0.00340812 * price[bar - 65]) - (0.00255923 * price[bar - 66]) - (0.00170217 * price[bar - 67]) - (0.00085902 * price[bar - 68]) - (4.113e-05 * price[bar - 69]) + (0.000737 * price[bar - 70]) + (0.00146422 * price[bar - 71]) + (0.00213007 * price[bar - 72]) + (0.00272649 * price[bar - 73]) + (0.00324752 * price[bar - 74]) + (0.00368922 * price[bar - 75]) + (0.00405 * price[bar - 76]) + (0.00433024 * price[bar - 77]) + (0.00453068 * price[bar - 78]) + (0.00465046 * price[bar - 79]) + (0.00469058 * price[bar - 80]) + (0.00466041 * price[bar - 81]) + (0.00457855 * price[bar - 82]) + (0.00442491 * price[bar - 83]) + (0.00423019 * price[bar - 84]) + (0.00399201 * price[bar - 85]) + (0.00372169 * price[bar - 86]) + (0.00342736 * price[bar - 87]) + (0.00311822 * price[bar - 88]) + (0.00280309 * price[bar - 89]) + (0.00249088 * price[bar - 90]) + (0.00219089 * price[bar - 91]) + (0.00191283 * price[bar - 92]) + (0.00166683 * price[bar - 93]) + (0.00146419 * price[bar - 94]) + (0.00131867 * price[bar - 95]) + (0.00124645 * price[bar - 96]) + (0.00126836 * price[bar - 97]) - (0.00401854 * price[bar - 98])
        ExtLineBuffer[bar] = RSTL
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Rstl(_MQL5Indicator):
    name = 'rstl'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSTLShift': 0,  # Horizontal shift of moving average in bars
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

