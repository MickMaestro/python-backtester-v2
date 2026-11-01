"""i-bb-width — converted from MQL5: MQL5 Indicators/i-BB-Width_HTF/i-bb-width.mq5

Ширина Полос Боллинджера
Copyright: Copyright © 2007, Ким Игорь В. aka KimIV.; Link: http://www.kimiv.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Ким Игорь В. aka KimIV.', 'link': 'http://www.kimiv.ru/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'i-BB-Width'}, 'levels': [], 'description': ['Ширина Полос Боллинджера'], 'name': 'i-bb-width', 'source': 'MQL5 Indicators/i-BB-Width_HTF/i-bb-width.mq5', 'folder': 'i-BB-Width_HTF', 'inputs': [{'mql': 'bands_period', 'py': 'bands_period', 'param': 'bands_period', 'type': 'uint', 'default': 20, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'deviation', 'py': 'deviation', 'param': 'deviation', 'type': 'double', 'default': 2.0, 'label': 'Девиация', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 1, 'label': 'Тип цены или handle', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
bands_period = _input('bands_period', 20)  # Глубина сглаживания
deviation = _input('deviation', 2.0)  # Девиация
applied_price = _input('applied_price', PRICE_CLOSE)  # Тип цены или handle
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
BB_Handle = 0
min_rates_total = 0

def OnInit():
    global BB_Handle, min_rates_total
    min_rates_total = bands_period
    BB_Handle = iBands(None, 0, _int(bands_period), 0, deviation, applied_price)
    if BB_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iBands')
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'i-BB-Width(', bands_period, ', ', deviation, ', ', EnumToString(applied_price, 'ENUM_APPLIED_PRICE'), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(BB_Handle) < rates_total or rates_total < _int(min_rates_total):
        return 0
    UpBB = Arr(0, 0.0)
    DnBB = Arr(0, 0.0)
    limit = 0
    bar = 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = _int(rates_total - min_rates_total - 1)
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(UpBB, True)
    ArraySetAsSeries(DnBB, True)
    if CopyBuffer(BB_Handle, UPPER_BAND, 0, to_copy, UpBB) <= 0:
        return 0
    if CopyBuffer(BB_Handle, LOWER_BAND, 0, to_copy, DnBB) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer[bar] = _fdiv(UpBB[bar] - DnBB[bar], Point())
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IBbWidth(_MQL5Indicator):
    name = 'i-bb-width'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'bands_period': 20,  # Глубина сглаживания
        'deviation': 2.0,  # Девиация
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Тип цены или handle
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

