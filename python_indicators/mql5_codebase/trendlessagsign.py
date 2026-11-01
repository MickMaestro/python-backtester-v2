"""trendlessagsign — converted from MQL5: MQL5 Indicators/TrendlessAGSign/trendlessagsign.mq5

Семафорный стрелочный сигнальный индикатор, фиксирующий пробой нулевой линии Осциллятора Бестрендовости
Copyright: Copyright © 2012, Barmaley; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Barmaley', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [9639167], 2: [14822282]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'TrendlessAGSign Sell', 2: 'TrendlessAGSign Buy'}, 'levels': [], 'description': ['Семафорный стрелочный сигнальный индикатор, фиксирующий пробой нулевой линии Осциллятора Бестрендовости'], 'name': 'trendlessagsign', 'source': 'MQL5 Indicators/TrendlessAGSign/trendlessagsign.mq5', 'folder': 'TrendlessAGSign', 'inputs': [{'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'uint', 'default': 7, 'label': 'Период скользящей средней в формуле осциллятора', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 1, 'label': 'Метод усреднения скользящей средней в формуле осциллятора', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': 'Входная цена скользящей средней в формуле осциллятора', 'sinput': False}, {'mql': 'PointsCount', 'py': 'PointsCount', 'param': 'PointsCount', 'type': 'uint', 'default': 600, 'label': 'Количество точек для расчета индикатора. Форекс-клуб рекомендует месяц для часовиков', 'sinput': False}, {'mql': 'In100', 'py': 'In100', 'param': 'In100', 'type': 'uint', 'default': 90, 'label': 'Сколько % точек индикатора должны входить в интервал +-100%', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAPeriod = _input('MAPeriod', 7)  # Период скользящей средней в формуле осциллятора
MAType = _input('MAType', MODE_EMA)  # Метод усреднения скользящей средней в формуле осциллятора
MAPrice = _input('MAPrice', PRICE_CLOSE)  # Входная цена скользящей средней в формуле осциллятора
PointsCount = _input('PointsCount', 600)  # Количество точек для расчета индикатора. Форекс-клуб рекомендует месяц для часовиков
In100 = _input('In100', 90)  # Сколько % точек индикатора должны входить в интервал +-100%
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
Count = Arr(0, 0)
Start = 0
Value = Arr(0, 0.0)
Sort = Arr(0, 0.0)
min_rates_total = 0
ATR_Handle = 0
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
    global ATR_Handle, MA_Handle, Start, min_rates_total
    min_rates_total = _int(PointsCount + MAPeriod)
    ATR_Period = 10
    min_rates_total = MathMax(min_rates_total, ATR_Period)
    Start = _int(_idiv(PointsCount * In100, 100))
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    MA_Handle = iMA(None, 0, MAPeriod, 0, MAType, MAPrice)
    if MA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    ArrayResize(Count, PointsCount)
    ArrayResize(Value, PointsCount)
    ArrayResize(Sort, PointsCount)
    ArrayInitialize(Count, 0)
    ArrayInitialize(Value, 0.0)
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 171)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 171)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    ArraySetAsSeries(BuyBuffer, True)
    shortname = 'TrendlessAGSign'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Res1, _s_OnCalculate_TrendlessAG1
    if (BarsCalculated(MA_Handle) < rates_total or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    TrendlessAG0 = 0.0
    Res0 = 0.0
    ATR = Arr(0, 0.0)
    Ma = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_TrendlessAG1 = 0.0
        _s_OnCalculate_Res1 = 0.0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    if CopyBuffer(MA_Handle, 0, 0, to_copy, Ma) <= 0:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(Ma, True)
    TrendlessAG0 = _s_OnCalculate_TrendlessAG1
    for bar in range(limit, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        Res0 = close[bar] - Ma[bar]
        Value[Count[0]] = MathAbs(Res0)
        if bar > 0:
            Recount_ArrayZeroPos(Count, PointsCount)
        if bar > (rates_total - min_rates_total - 1):
            continue
        ArrayCopy(Sort, Value, 0, 0, WHOLE_ARRAY)
        ArraySort(Sort)
        level_100 = Sort[Start]
        if level_100:
            Res0 *= _fdiv(100, level_100)
        else:
            Res0 = EMPTY_VALUE
        if Res0 > 0.0 and _s_OnCalculate_Res1 <= 0.0:
            BuyBuffer[bar] = low[bar] - ((ATR[0] * 3) / 8)
        if Res0 < 0.0 and _s_OnCalculate_Res1 >= 0.0:
            SellBuffer[bar] = high[bar] + ((ATR[0] * 3) / 8)
        if bar:
            _s_OnCalculate_TrendlessAG1 = TrendlessAG0
            _s_OnCalculate_Res1 = Res0
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1
_s_OnCalculate_TrendlessAG1 = 0.0
_s_OnCalculate_Res1 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Trendlessagsign(_MQL5Indicator):
    name = 'trendlessagsign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'MAPeriod': 7,  # Период скользящей средней в формуле осциллятора
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Метод усреднения скользящей средней в формуле осциллятора
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Входная цена скользящей средней в формуле осциллятора
        'PointsCount': 600,  # Количество точек для расчета индикатора. Форекс-клуб рекомендует месяц для часовиков
        'In100': 90,  # Сколько % точек индикатора должны входить в интервал +-100%
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

