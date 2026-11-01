"""colorstddev — converted from MQL5: MQL5 Indicators/ColorStdDev_HTF/colorstddev.mq5

Copyright: Copyright © 2010, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 16711680, 255, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'StdDev'}, 'levels': [], 'description': [], 'name': 'colorstddev', 'source': 'MQL5 Indicators/ColorStdDev_HTF/colorstddev.mq5', 'folder': 'ColorStdDev_HTF', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'uint', 'default': 12, 'label': 'Период усреднения', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 1, 'label': 'Метод усреднения гистограммы', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'MaxTrendLevel', 'py': 'MaxTrendLevel', 'param': 'MaxTrendLevel', 'type': 'uint', 'default': 100, 'label': 'Уровень максимального тренда', 'sinput': False}, {'mql': 'MiddLeTrendLevel', 'py': 'MiddLeTrendLevel', 'param': 'MiddLeTrendLevel', 'type': 'uint', 'default': 40, 'label': 'Уровень умеренного тренда', 'sinput': False}, {'mql': 'FlatLevel', 'py': 'FlatLevel', 'param': 'FlatLevel', 'type': 'uint', 'default': 10, 'label': 'Уровень флета', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Blue = 0xFF0000  # MQL4 colour name
Gray = 0x808080  # MQL4 colour name
Magenta = 0xFF00FF  # MQL4 colour name

# ---- inputs and global variables
period = _input('period', 12)  # Период усреднения
MA_Method = _input('MA_Method', MODE_EMA)  # Метод усреднения гистограммы
applied_price = _input('applied_price', PRICE_CLOSE)  # Ценовая константа
MaxTrendLevel = _input('MaxTrendLevel', 100)  # Уровень максимального тренда
MiddLeTrendLevel = _input('MiddLeTrendLevel', 40)  # Уровень умеренного тренда
FlatLevel = _input('FlatLevel', 10)  # Уровень флета
StdDevBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
StdDev_Handle = 0
min_rates_total = 0

def OnInit():
    global StdDev_Handle, min_rates_total
    min_rates_total = _int(period)
    StdDev_Handle = iStdDev(None, 0, period, 0, MA_Method, applied_price)
    if StdDev_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора StdDev')
    SetIndexBuffer(0, StdDevBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(StdDevBuffer, True)
    SetIndexBuffer(1, ColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'ColorStdDev( ', period, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, MaxTrendLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, MiddLeTrendLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, FlatLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, Magenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, Blue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, Gray)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(StdDev_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(StdDev_Handle, 0, 0, to_copy, StdDevBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        StdDevBuffer[bar] = _fdiv(StdDevBuffer[bar], Point())
        ColorBuffer[bar] = 0.0
        if StdDevBuffer[bar] > MaxTrendLevel:
            ColorBuffer[bar] = 3.0
        elif StdDevBuffer[bar] > MiddLeTrendLevel:
            ColorBuffer[bar] = 2.0
        elif StdDevBuffer[bar] > FlatLevel:
            ColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorstddev(_MQL5Indicator):
    name = 'colorstddev'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 12,  # Период усреднения
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Метод усреднения гистограммы
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Ценовая константа
        'MaxTrendLevel': 100,  # Уровень максимального тренда
        'MiddLeTrendLevel': 40,  # Уровень умеренного тренда
        'FlatLevel': 10,  # Уровень флета
    }

