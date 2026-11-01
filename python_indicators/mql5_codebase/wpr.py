"""wpr — converted from MQL5: MQL5 Indicators/WPR/wpr.mq5

Williams’ Percent Range
Copyright: Copyright © 2005, Dark Han; Link: http://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Dark Han', 'link': 'http://www.metaquotes.net/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1, 'indicator_maximum': 0.0, 'indicator_minimum': -100.0}, 'types': {1: 1}, 'colors': {1: [13850042]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'WPR'}, 'levels': [-30.0, -70.0], 'description': ['Williams’ Percent Range'], 'name': 'wpr', 'source': 'MQL5 Indicators/WPR/wpr.mq5', 'folder': 'WPR', 'inputs': [{'mql': 'ExtWPRPeriod', 'py': 'ExtWPRPeriod', 'param': 'ExtWPRPeriod', 'type': 'uint', 'default': 11, 'label': 'Период усреднения', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_APPLIED_PRICE_
PRICE_CLOSE_ = 1
PRICE_HIGH_ = 2
PRICE_LOW_ = 3
_enum('ENUM_APPLIED_PRICE_', {1: 'PRICE_CLOSE_', 2: 'PRICE_HIGH_', 3: 'PRICE_LOW_'})

# ---- inputs and global variables
ExtWPRPeriod = _input('ExtWPRPeriod', 11)  # Период усреднения
IPC = _input('IPC', PRICE_CLOSE_)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtLineBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(ExtWPRPeriod)
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    shortname = Box("")
    StringConcatenate(shortname, 'WPR(', ExtWPRPeriod, ' ', EnumToString(IPC, 'ENUM_APPLIED_PRICE_'), ')')
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtLineBuffer, True)
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
        ExtLineBuffer[bar] = 50.0
        HH = high[ArrayMaximum(high, bar, ExtWPRPeriod)]
        LL = low[ArrayMinimum(low, bar, ExtWPRPeriod)]
        range_ = HH - LL
        if not CompareDouble(range_, 0.0):
            _sw1 = IPC
            if _sw1 == PRICE_CLOSE_:
                ExtLineBuffer[bar] = _fdiv(-100 * (HH - close[bar]), range_)
            elif _sw1 == PRICE_HIGH_:
                ExtLineBuffer[bar] = _fdiv(-100 * (HH - high[bar]), range_)
            elif _sw1 == PRICE_LOW_:
                ExtLineBuffer[bar] = _fdiv(-100 * (HH - low[bar]), range_)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def CompareDouble(Number1, Number2):
    Compare = NormalizeDouble(Number1 - Number2, 8) == 0
    return Compare


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Wpr(_MQL5Indicator):
    name = 'wpr'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ExtWPRPeriod': 11,  # Период усреднения
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_HIGH', 3: 'PRICE_LOW'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }
    y_range = (-100.0, 0.0)

