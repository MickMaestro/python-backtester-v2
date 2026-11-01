"""wpr3 — converted from MQL5: MQL5 Indicators/WPR3/wpr3.mq5

Williams’ Percent Range
Copyright: Copyright © 2005, Dark Han; Link: http://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Dark Han', 'link': 'http://www.metaquotes.net/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3, 'indicator_maximum': 0.0, 'indicator_minimum': -100.0}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [2330219], 2: [8421504], 3: [9662683]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'High WPR', 2: 'Close WPR', 3: 'Low WPR'}, 'levels': [-30.0, -70.0], 'description': ['Williams’ Percent Range'], 'name': 'wpr3', 'source': 'MQL5 Indicators/WPR3/wpr3.mq5', 'folder': 'WPR3', 'inputs': [{'mql': 'ExtWPRPeriod', 'py': 'ExtWPRPeriod', 'param': 'ExtWPRPeriod', 'type': 'uint', 'default': 11, 'label': 'Период усреднения', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_APPLIED_PRICE_
PRICE_CLOSE_ = 1
PRICE_HIGH_ = 2
PRICE_LOW_ = 3
_enum('ENUM_APPLIED_PRICE_', {1: 'PRICE_CLOSE_', 2: 'PRICE_HIGH_', 3: 'PRICE_LOW_'})

# ---- inputs and global variables
ExtWPRPeriod = _input('ExtWPRPeriod', 11)  # Период усреднения
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
UpperBuffer = Arr(0, 0.0)
MiddleBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(ExtWPRPeriod)
    shortname = Box("")
    StringConcatenate(shortname, 'WPR3(', ExtWPRPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    SetIndexBuffer(0, UpperBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpperBuffer, True)
    SetIndexBuffer(1, MiddleBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(MiddleBuffer, True)
    SetIndexBuffer(2, LowerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(LowerBuffer, True)
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
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        LowerBuffer[bar] = 50.0
        UpperBuffer[bar] = LowerBuffer[bar]
        MiddleBuffer[bar] = UpperBuffer[bar]
        HH = high[ArrayMaximum(high, bar, ExtWPRPeriod)]
        LL = low[ArrayMinimum(low, bar, ExtWPRPeriod)]
        range_ = HH - LL
        if not CompareDouble(range_, 0.0):
            MiddleBuffer[bar] = _fdiv(-100 * (HH - close[bar]), range_)
            UpperBuffer[bar] = _fdiv(-100 * (HH - high[bar]), range_)
            LowerBuffer[bar] = _fdiv(-100 * (HH - low[bar]), range_)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def CompareDouble(Number1, Number2):
    Compare = NormalizeDouble(Number1 - Number2, 8) == 0
    return Compare


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Wpr3(_MQL5Indicator):
    name = 'wpr3'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ExtWPRPeriod': 11,  # Период усреднения
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }
    y_range = (-100.0, 0.0)

