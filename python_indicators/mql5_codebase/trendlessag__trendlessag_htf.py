"""trendlessag — converted from MQL5: MQL5 Indicators/TrendlessAG_HTF/trendlessag.mq5

Осциллятор Бестрендовости написан в соответствии с описанием,
приведенным в книге Джо ДиНаполи \\"Торговля с применением уровней ДиНаполи\\"
Copyright: Copyright © 2012, Barmaley; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Barmaley', 'link': '', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'TrendlessAG'}, 'levels': [100.0, 80.0, 60.0, 0.0, -60.0, -80.0, -100.0], 'description': ['Осциллятор Бестрендовости написан в соответствии с описанием,', 'приведенным в книге Джо ДиНаполи \\"Торговля с применением уровней ДиНаполи\\"'], 'name': 'trendlessag', 'source': 'MQL5 Indicators/TrendlessAG_HTF/trendlessag.mq5', 'folder': 'TrendlessAG_HTF', 'inputs': [{'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'uint', 'default': 7, 'label': 'Период скользящей средней в формуле осциллятора', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 1, 'label': 'Метод усреднения скользящей средней в формуле осциллятора', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': 'Входная цена скользящей средней в формуле осциллятора', 'sinput': False}, {'mql': 'PointsCount', 'py': 'PointsCount', 'param': 'PointsCount', 'type': 'uint', 'default': 600, 'label': 'Количество точек для расчета индикатора. Форекс-клуб рекомендует месяц для часовиков', 'sinput': False}, {'mql': 'In100', 'py': 'In100', 'param': 'In100', 'type': 'uint', 'default': 90, 'label': 'Сколько % точек индикатора должны входить в интервал +-100%', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAPeriod = _input('MAPeriod', 7)  # Период скользящей средней в формуле осциллятора
MAType = _input('MAType', MODE_EMA)  # Метод усреднения скользящей средней в формуле осциллятора
MAPrice = _input('MAPrice', PRICE_CLOSE)  # Входная цена скользящей средней в формуле осциллятора
PointsCount = _input('PointsCount', 600)  # Количество точек для расчета индикатора. Форекс-клуб рекомендует месяц для часовиков
In100 = _input('In100', 90)  # Сколько % точек индикатора должны входить в интервал +-100%
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
Count = Arr(0, 0)
Start = 0
Value = Arr(0, 0.0)
Sort = Arr(0, 0.0)
min_rates_total = 0
MA_Handle = 0

def Recount_ArrayZeroPos(CoArr, Size):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def OnInit():
    global MA_Handle, Start, min_rates_total
    min_rates_total = _int(PointsCount + MAPeriod)
    Start = _int(_idiv(PointsCount * In100, 100))
    MA_Handle = iMA(None, 0, MAPeriod, 0, MAType, MAPrice)
    if MA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    ArrayResize(Count, PointsCount)
    ArrayResize(Value, PointsCount)
    ArrayResize(Sort, PointsCount)
    ArrayInitialize(Count, 0)
    ArrayInitialize(Value, 0.0)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TrendlessAG')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(MA_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    Ma = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = _int(rates_total - MAPeriod - 1)
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(Ma, True)
    ArraySetAsSeries(close, True)
    to_copy = limit + 1
    if CopyBuffer(MA_Handle, 0, 0, to_copy, Ma) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Res = close[bar] - Ma[bar]
        Value[Count[0]] = MathAbs(Res)
        if bar > 0:
            Recount_ArrayZeroPos(Count, PointsCount)
        if bar > (rates_total - min_rates_total - 1):
            continue
        ArrayCopy(Sort, Value, 0, 0, WHOLE_ARRAY)
        ArraySort(Sort)
        level_100 = Sort[Start]
        if level_100:
            Res *= _fdiv(100, level_100)
        else:
            Res = EMPTY_VALUE
        IndBuffer[bar] = Res
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Trendlessag(_MQL5Indicator):
    name = 'trendlessag'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAPeriod': 7,  # Период скользящей средней в формуле осциллятора
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Метод усреднения скользящей средней в формуле осциллятора
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Входная цена скользящей средней в формуле осциллятора
        'PointsCount': 600,  # Количество точек для расчета индикатора. Форекс-клуб рекомендует месяц для часовиков
        'In100': 90,  # Сколько % точек индикатора должны входить в интервал +-100%
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

