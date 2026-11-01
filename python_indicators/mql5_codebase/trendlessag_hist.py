"""trendlessag_hist — converted from MQL5: MQL5 Indicators/TrendlessAG_Hist/trendlessag_hist.mq5

Осциллятор Бестрендовости написан в соответствии с описанием,
приведенным в книге Джо ДиНаполи \\"Торговля с применением уровней ДиНаполи\\".
Дополнительно использовано сглаживание итогового индикатора.
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16711935, 9639167, 8421504, 16748574, 2330219]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'TrendlessAG_Hist'}, 'levels': [100.0, 80.0, 60.0, 0.0, -60.0, -80.0, -100.0], 'description': ['Осциллятор Бестрендовости написан в соответствии с описанием,', 'приведенным в книге Джо ДиНаполи \\"Торговля с применением уровней ДиНаполи\\".', 'Дополнительно использовано сглаживание итогового индикатора.'], 'name': 'trendlessag_hist', 'source': 'MQL5 Indicators/TrendlessAG_Hist/trendlessag_hist.mq5', 'folder': 'TrendlessAG_Hist', 'inputs': [{'mql': 'XMA_Method1', 'py': 'XMA_Method1', 'param': 'XMA_Method1', 'type': 'int', 'default': 1, 'label': 'Метод усреднения  в формуле осциллятора', 'sinput': False}, {'mql': 'XLength1', 'py': 'XLength1', 'param': 'XLength1', 'type': 'int', 'default': 7, 'label': 'Период скользящей средней в формуле осциллятора', 'sinput': False}, {'mql': 'XPhase1', 'py': 'XPhase1', 'param': 'XPhase1', 'type': 'int', 'default': 15, 'label': 'Параметр скользящей средней в формуле осциллятора,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Входная цена скользящей средней в формуле осциллятора', 'sinput': False}, {'mql': 'PointsCount', 'py': 'PointsCount', 'param': 'PointsCount', 'type': 'uint', 'default': 600, 'label': 'Количество точек для расчета индикатора. Форекс-клуб рекомендует месяц для часовиков', 'sinput': False}, {'mql': 'In100', 'py': 'In100', 'param': 'In100', 'type': 'uint', 'default': 90, 'label': 'Сколько % точек индикатора должны входить в интервал +-100%', 'sinput': False}, {'mql': 'XMA_Method2', 'py': 'XMA_Method2', 'param': 'XMA_Method2', 'type': 'int', 'default': 4, 'label': 'Метод сглаживания индикатора', 'sinput': False}, {'mql': 'XLength2', 'py': 'XLength2', 'param': 'XLength2', 'type': 'int', 'default': 5, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'XPhase2', 'py': 'XPhase2', 'param': 'XPhase2', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
XMA_Method1 = _input('XMA_Method1', MODE_EMA)  # Метод усреднения  в формуле осциллятора
XLength1 = _input('XLength1', 7)  # Период скользящей средней в формуле осциллятора
XPhase1 = _input('XPhase1', 15)  # Параметр скользящей средней в формуле осциллятора,
IPC = _input('IPC', PRICE_CLOSE)  # Входная цена скользящей средней в формуле осциллятора
PointsCount = _input('PointsCount', 600)  # Количество точек для расчета индикатора. Форекс-клуб рекомендует месяц для часовиков
In100 = _input('In100', 90)  # Сколько % точек индикатора должны входить в интервал +-100%
XMA_Method2 = _input('XMA_Method2', MODE_JJMA)  # Метод сглаживания индикатора
XLength2 = _input('XLength2', 5)  # Глубина сглаживания
XPhase2 = _input('XPhase2', 100)  # Параметр сглаживания
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
Count = Arr(0, 0)
Start = 0
Value = Arr(0, 0.0)
Sort = Arr(0, 0.0)

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
    global Start, min_rates_1, min_rates_2, min_rates_total
    min_rates_1 = XMA1.GetStartBars(XMA_Method1, XLength1, XPhase1)
    min_rates_2 = _int(PointsCount + min_rates_1)
    min_rates_total = min_rates_2 + XMA1.GetStartBars(XMA_Method2, XLength2, XPhase2) + 2
    Start = _int(_idiv(PointsCount * In100, 100))
    ArrayResize(Count, PointsCount)
    ArrayResize(Value, PointsCount)
    ArrayResize(Sort, PointsCount)
    ArrayInitialize(Count, 0)
    ArrayInitialize(Value, 0.0)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TrendlessAG_Hist')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    x1xma = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        x1xma = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method1, XPhase1, XLength1, price, bar, False)
        Res = price - x1xma
        Value[Count[0]] = MathAbs(Res)
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count, PointsCount)
        if bar < min_rates_2:
            continue
        ArrayCopy(Sort, Value, 0, 0, WHOLE_ARRAY)
        ArraySort(Sort)
        level_100 = Sort[Start]
        if level_100:
            Res *= _fdiv(100, level_100)
        else:
            Res = EMPTY_VALUE
        IndBuffer[bar] = XMA2.XMASeries(min_rates_2, prev_calculated, rates_total, XMA_Method2, XPhase2, XLength2, Res, bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        ColorIndBuffer[bar] = 2.0
        if IndBuffer[bar] > 0:
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                ColorIndBuffer[bar] = 4.0
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                ColorIndBuffer[bar] = 3.0
        if IndBuffer[bar] < 0:
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                ColorIndBuffer[bar] = 0.0
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                ColorIndBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendlessagHist(_MQL5Indicator):
    name = 'trendlessag_hist'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Метод усреднения  в формуле осциллятора
        'XLength1': 7,  # Период скользящей средней в формуле осциллятора
        'XPhase1': 15,  # Параметр скользящей средней в формуле осциллятора,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Входная цена скользящей средней в формуле осциллятора
        'PointsCount': 600,  # Количество точек для расчета индикатора. Форекс-клуб рекомендует месяц для часовиков
        'In100': 90,  # Сколько % точек индикатора должны входить в интервал +-100%
        'XMA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод сглаживания индикатора
        'XLength2': 5,  # Глубина сглаживания
        'XPhase2': 100,  # Параметр сглаживания
    }

