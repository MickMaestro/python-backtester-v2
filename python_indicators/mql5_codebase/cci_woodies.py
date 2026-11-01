"""CCI_Woodies — converted from MQL5: MQL5 Indicators/CCI_Woodies/CCI_Woodies.mq5

Copyright: Woodies; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Woodies', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [65280, 14524637]}, 'widths': {}, 'styles': {}, 'labels': {1: 'CCI_Woodies'}, 'levels': [], 'description': [], 'name': 'CCI_Woodies', 'source': 'MQL5 Indicators/CCI_Woodies/CCI_Woodies.mq5', 'folder': 'CCI_Woodies', 'inputs': [{'mql': 'FastPeriod', 'py': 'FastPeriod', 'param': 'FastPeriod', 'type': 'uint', 'default': 6, 'label': 'Период быстрого CCI индикатора', 'sinput': False}, {'mql': 'FastPrice', 'py': 'FastPrice', 'param': 'FastPrice', 'type': 'int', 'default': 5, 'label': 'Ценовая константа быстрого CCI индикатора', 'sinput': False}, {'mql': 'SlowPeriod', 'py': 'SlowPeriod', 'param': 'SlowPeriod', 'type': 'uint', 'default': 14, 'label': 'Период медленного CCI индикатора', 'sinput': False}, {'mql': 'SlowPrice', 'py': 'SlowPrice', 'param': 'SlowPrice', 'type': 'int', 'default': 5, 'label': 'Ценовая константа медленного CCI индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FastPeriod = _input('FastPeriod', 6)  # Период быстрого CCI индикатора
FastPrice = _input('FastPrice', PRICE_MEDIAN)  # Ценовая константа быстрого CCI индикатора
SlowPeriod = _input('SlowPeriod', 14)  # Период медленного CCI индикатора
SlowPrice = _input('SlowPrice', PRICE_MEDIAN)  # Ценовая константа медленного CCI индикатора
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
FastBuffer = Arr(0, 0.0)
SlowBuffer = Arr(0, 0.0)
min_rates_total = 0
Fast_Handle = 0
Slow_Handle = 0

def OnInit():
    global Fast_Handle, Slow_Handle, min_rates_total
    min_rates_total = _int(MathMax(FastPeriod, SlowPeriod))
    Fast_Handle = iCCI(Symbol(), PERIOD_CURRENT, FastPeriod, FastPrice)
    if Fast_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Fast iCCI')
        return INIT_FAILED
    Slow_Handle = iCCI(Symbol(), PERIOD_CURRENT, SlowPeriod, SlowPrice)
    if Slow_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Slow iCCI')
        return INIT_FAILED
    SetIndexBuffer(0, FastBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SlowBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box("")
    StringConcatenate(shortname, 'Instantaneous Trendline(', FastPeriod, ', ', SlowPeriod, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 100)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, -100)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASH)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (rates_total < min_rates_total or BarsCalculated(Fast_Handle) < rates_total) or BarsCalculated(Slow_Handle) < rates_total:
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated + 1
    if CopyBuffer(Fast_Handle, 0, 0, to_copy, FastBuffer) <= 0:
        return 0
    if CopyBuffer(Slow_Handle, 0, 0, to_copy, SlowBuffer) <= 0:
        return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CCIWoodies(_MQL5Indicator):
    name = 'CCI_Woodies'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastPeriod': 6,  # Период быстрого CCI индикатора
        'FastPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Ценовая константа быстрого CCI индикатора
        'SlowPeriod': 14,  # Период медленного CCI индикатора
        'SlowPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Ценовая константа медленного CCI индикатора
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

