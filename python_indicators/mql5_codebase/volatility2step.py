"""Volatility2Step — converted from MQL5: MQL5 Indicators/Volatility2Step/Volatility2Step.mq5

Copyright: Copyright © 2007, Eva Ruft; Link: briz18@rambler.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Eva Ruft', 'link': 'briz18@rambler.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 3}, 'colors': {1: [14822282]}, 'widths': {1: 4}, 'styles': {1: 0}, 'labels': {1: 'Volatility2Step'}, 'levels': [], 'description': [], 'name': 'Volatility2Step', 'source': 'MQL5 Indicators/Volatility2Step/Volatility2Step.mq5', 'folder': 'Volatility2Step', 'inputs': [{'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 0, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'VolatilityPeriod', 'py': 'VolatilityPeriod', 'param': 'VolatilityPeriod', 'type': 'uint', 'default': 5, 'label': 'период индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'LevelsTotal', 'py': 'LevelsTotal', 'param': 'LevelsTotal', 'type': 'uint', 'default': 20, 'label': 'количество уровеней', 'sinput': False}, {'mql': 'StartLevel', 'py': 'StartLevel', 'param': 'StartLevel', 'type': 'uint', 'default': 100, 'label': 'стартовый уровень', 'sinput': False}, {'mql': 'LevelsStep', 'py': 'LevelsStep', 'param': 'LevelsStep', 'type': 'uint', 'default': 100, 'label': 'расстояние между уровнями', 'sinput': False}, {'mql': 'LevelsColor', 'py': 'LevelsColor', 'param': None, 'type': 'color', 'default': 36095, 'label': 'цвет уровеней', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAType = _input('MAType', MODE_SMA)  # метод усреднения
VolatilityPeriod = _input('VolatilityPeriod', 5)  # период индикатора
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
LevelsTotal = _input('LevelsTotal', 20)  # количество уровеней
StartLevel = _input('StartLevel', 100)  # стартовый уровень
LevelsStep = _input('LevelsStep', 100)  # расстояние между уровнями
LevelsColor = _input('LevelsColor', clrDarkOrange)  # цвет уровеней
IndBuffer = Arr(0, 0.0)
min_rates_total = 0
HMA_Handle = 0
LMA_Handle = 0

def OnInit():
    global HMA_Handle, LMA_Handle, min_rates_total
    min_rates_total = _int(VolatilityPeriod)
    HMA_Handle = iMA(None, 0, VolatilityPeriod, 0, MAType, PRICE_HIGH)
    if HMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
    LMA_Handle = iMA(None, 0, VolatilityPeriod, 0, MAType, PRICE_LOW)
    if LMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    shortname = 'Volatility2Step(' + _str(VolatilityPeriod) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, LevelsTotal)
    for numb in range(0, _int(LevelsTotal)):
        level = _int(StartLevel + (LevelsStep * numb))
        IndicatorSetDouble(INDICATOR_LEVELVALUE, numb, level)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, numb, LevelsColor)
        IndicatorSetInteger(INDICATOR_LEVELSTYLE, numb, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(HMA_Handle) < rates_total or BarsCalculated(LMA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    HMA = Arr(0, 0.0)
    LMA = Arr(0, 0.0)
    Volatility = 0.0
    Res = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(HMA, True)
    ArraySetAsSeries(LMA, True)
    if CopyBuffer(HMA_Handle, 0, 0, to_copy, HMA) <= 0:
        return 0
    if CopyBuffer(LMA_Handle, 0, 0, to_copy, LMA) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Volatility = _fdiv(HMA[bar] - LMA[bar], Point())
        IndBuffer[bar] = 0.0
        if Volatility >= StartLevel:
            Res = MathMax(Volatility - StartLevel, 0)
            IndBuffer[bar] = StartLevel + (LevelsStep * _int(Res / LevelsStep))
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Volatility2Step(_MQL5Indicator):
    name = 'Volatility2Step'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # метод усреднения
        'VolatilityPeriod': 5,  # период индикатора
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'LevelsTotal': 20,  # количество уровеней
        'StartLevel': 100,  # стартовый уровень
        'LevelsStep': 100,  # расстояние между уровнями
    }

