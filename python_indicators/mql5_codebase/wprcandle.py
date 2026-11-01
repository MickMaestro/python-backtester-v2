"""wprcandle — converted from MQL5: MQL5 Indicators/WPRCandle/wprcandle.mq5

Williams’ Percent Range
Copyright: Copyright © 2005, Dark Han; Link: http://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Dark Han', 'link': 'http://www.metaquotes.net/', 'version': '1.00', 'indicator_maximum': 0.0, 'indicator_minimum': -100.0, 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [9639167, 16711680, 8421376]}, 'widths': {}, 'styles': {}, 'labels': {1: 'WPRCandle Open;WPRCandle High;WPRCandle Low;WPRCandle Close'}, 'levels': [-70.0, -50.0, -30.0], 'description': ['Williams’ Percent Range'], 'name': 'wprcandle', 'source': 'MQL5 Indicators/WPRCandle/wprcandle.mq5', 'folder': 'WPRCandle', 'inputs': [{'mql': 'ExtWPRPeriod', 'py': 'ExtWPRPeriod', 'param': 'ExtWPRPeriod', 'type': 'uint', 'default': 11, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtWPRPeriod = _input('ExtWPRPeriod', 11)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(ExtWPRPeriod)
    shortname = Box("")
    StringConcatenate(shortname, 'WPRCandle(', ExtWPRPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    range_ = 0.0
    HH = 0.0
    LL = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtCloseBuffer[bar] = 50.0
        ExtLowBuffer[bar] = ExtCloseBuffer[bar]
        ExtHighBuffer[bar] = ExtLowBuffer[bar]
        ExtOpenBuffer[bar] = ExtHighBuffer[bar]
        HH = high[ArrayMaximum(high, bar, ExtWPRPeriod)]
        LL = low[ArrayMinimum(low, bar, ExtWPRPeriod)]
        range_ = HH - LL
        if not CompareDouble(range_, 0.0):
            ExtOpenBuffer[bar] = _fdiv(-100 * (HH - open[bar]), range_)
            ExtCloseBuffer[bar] = _fdiv(-100 * (HH - close[bar]), range_)
            ExtHighBuffer[bar] = _fdiv(-100 * (HH - high[bar]), range_)
            ExtLowBuffer[bar] = _fdiv(-100 * (HH - low[bar]), range_)
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def CompareDouble(Number1, Number2):
    Compare = NormalizeDouble(Number1 - Number2, 8) == 0
    return Compare


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Wprcandle(_MQL5Indicator):
    name = 'wprcandle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ExtWPRPeriod': 11,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }
    y_range = (-100.0, 0.0)

