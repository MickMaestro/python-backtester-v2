"""ColorPEMA_Digit_r — converted from MQL5: MQL5 Indicators/ColorPEMA_Digit_r/ColorPEMA_Digit_r.mq5

Pentuple Exponential Moving Average
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16711935, 8421504, 16748574]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'PEMA'}, 'levels': [], 'description': ['Pentuple Exponential Moving Average'], 'name': 'ColorPEMA_Digit_r', 'source': 'MQL5 Indicators/ColorPEMA_Digit_r/ColorPEMA_Digit_r.mq5', 'folder': 'ColorPEMA_Digit_r', 'inputs': [{'mql': 'EmaLength', 'py': 'EmaLength', 'param': 'EmaLength', 'type': 'double', 'default': 50.01, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}, {'mql': 'Digit', 'py': 'Digit', 'param': 'Digit', 'type': 'uint', 'default': 2, 'label': 'количество разрядов округления', 'sinput': False}, {'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'ColorPEMA_Digit', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': 'показывать ценовую метку', 'sinput': False}, {'mql': 'RecountMode', 'py': 'RecountMode', 'param': 'RecountMode', 'type': 'int', 'default': 3, 'label': 'Способ ограничения расчётов индикатора', 'sinput': False}, {'mql': 'CountBars', 'py': 'CountBars', 'param': 'CountBars', 'type': 'uint', 'default': 500, 'label': 'количество баров для расчёта индикатора', 'sinput': False}, {'mql': 'ReCountTime', 'py': 'ReCountTime', 'param': 'ReCountTime', 'type': 'uint', 'default': 60, 'label': 'время в секундах между расчётами индикатора', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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

# enum ENUM_RECOUNT_MODE
ONLY_BARS_RECOUNT = 1
ONLY_TIME_RECOUNT = 2
FULL_RECOUNT = 3
_enum('ENUM_RECOUNT_MODE', {1: 'ONLY_BARS_RECOUNT', 2: 'ONLY_TIME_RECOUNT', 3: 'FULL_RECOUNT'})

# ---- inputs and global variables
EmaLength = _input('EmaLength', 50.01)  # глубина сглаживания
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
Digit = _input('Digit', 2)  # количество разрядов округления
SirName = _input('SirName', 'ColorPEMA_Digit')  # Первая часть имени графических объектов
ShowPrice = _input('ShowPrice', True)  # показывать ценовую метку
RecountMode = _input('RecountMode', FULL_RECOUNT)  # Способ ограничения расчётов индикатора
CountBars = _input('CountBars', 500)  # количество баров для расчёта индикатора
ReCountTime = _input('ReCountTime', 60)  # время в секундах между расчётами индикатора
ExtLineBuffer = Arr(0, 0.0)
ColorExtLineBuffer = Arr(0, 0.0)
dPriceShift = 0.0
PointPow10 = 0.0
min_rates_total = 0
count_bars = 0
Price_name = ""
UpPrice_color = 0  # цвет ценовой метки для роста
DnPrice_color = 0  # цвет ценовой метки для падения

def OnInit():
    global DnPrice_color, PointPow10, Price_name, UpPrice_color, count_bars, dPriceShift, min_rates_total
    min_rates_total = 9 + 1
    count_bars = _int(MathMax(CountBars, min_rates_total))
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtLineBuffer, False)
    SetIndexBuffer(1, ColorExtLineBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorExtLineBuffer, False)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'ColorPEMA_Digit_r(', EmaLength, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    dPriceShift = Point() * PriceShift
    PointPow10 = Point() * MathPow(10, Digit)
    Price_name = SirName + 'Price'
    DnPrice_color = _uint(PlotIndexGetInteger(0, PLOT_LINE_COLOR, 0))
    UpPrice_color = _uint(PlotIndexGetInteger(0, PLOT_LINE_COLOR, 2))

def OnDeinit(reason):
    ObjectDelete(0, Price_name)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_recount_time
    if (prev_calculated > rates_total or prev_calculated <= 0) or prev_calculated != rates_total:
        _s_OnCalculate_recount_time = 0
    _sw1 = RecountMode
    if _sw1 == ONLY_BARS_RECOUNT:
        pass
    else:
        if (TimeCurrent() - _s_OnCalculate_recount_time) < _int(ReCountTime):
            return rates_total
        else:
            _s_OnCalculate_recount_time = TimeCurrent()
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    res = Arr(9, 0.0, dyn=False)
    pema = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    _sw2 = RecountMode
    if _sw2 == ONLY_TIME_RECOUNT:
        pass
    else:
        barx = rates_total - 1 - count_bars
        first = MathMax(first, barx)
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, barx + 7)
    ArraySetAsSeries(open, False)
    ArraySetAsSeries(high, False)
    ArraySetAsSeries(low, False)
    ArraySetAsSeries(close, False)
    bar = first
    for bar in range(bar, rates_total):
        res[0] = PriceSeries(IPC, bar, open, low, high, close)
        start = rates_total - 1 - count_bars
        res[1] = EMA[0].EMASeries(MathMax(start + 0, 0), prev_calculated, rates_total, EmaLength, res[0], bar, False)
        res[2] = EMA[1].EMASeries(MathMax(start + 1, 1), prev_calculated, rates_total, EmaLength, res[1], bar, False)
        res[3] = EMA[2].EMASeries(MathMax(start + 2, 2), prev_calculated, rates_total, EmaLength, res[2], bar, False)
        res[4] = EMA[3].EMASeries(MathMax(start + 3, 3), prev_calculated, rates_total, EmaLength, res[3], bar, False)
        res[5] = EMA[4].EMASeries(MathMax(start + 4, 4), prev_calculated, rates_total, EmaLength, res[4], bar, False)
        res[6] = EMA[5].EMASeries(MathMax(start + 5, 5), prev_calculated, rates_total, EmaLength, res[5], bar, False)
        res[7] = EMA[6].EMASeries(MathMax(start + 6, 6), prev_calculated, rates_total, EmaLength, res[6], bar, False)
        res[8] = EMA[7].EMASeries(MathMax(start + 7, 7), prev_calculated, rates_total, EmaLength, res[7], bar, False)
        pema = (8 * res[1]) - (28 * res[2]) + (56 * res[3]) - (70 * res[4]) + (56 * res[5]) - (28 * res[6]) + (8 * res[7]) - res[8]
        pema += dPriceShift
        ExtLineBuffer[bar] = PointPow10 * MathRound(_fdiv(pema, PointPow10))
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        clr = 1
        trend = ExtLineBuffer[bar] - ExtLineBuffer[bar - 1]
        if not trend:
            clr = _int(ColorExtLineBuffer[bar - 1])
        else:
            if trend > 0:
                clr = 2
            if trend < 0:
                clr = 0
        ColorExtLineBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    if ShowPrice:
        clr = DnPrice_color
        bar0 = rates_total - 1
        if ColorExtLineBuffer[bar0] != 0:
            clr = UpPrice_color
        time0 = time[bar0] + (1 * PeriodSeconds())
        SetRightPrice(0, Price_name, 0, time0, ExtLineBuffer[bar0], clr)
    ChartRedraw(0)
    return rates_total

def CreateRightPrice(chart_id, name, nwin, time, price, Color):
    ObjectCreate(chart_id, name, OBJ_ARROW_RIGHT_PRICE, nwin, time, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, 2)

def SetRightPrice(chart_id, name, nwin, time, price, Color):
    if ObjectFind(chart_id, name) == -1:
        CreateRightPrice(chart_id, name, nwin, time, price, Color)
    else:
        ObjectMove(chart_id, name, 0, time, price)

# ---- global variables initialised from expressions
EMA = Arr(8, 0, dyn=False, factory=CMoving_Average)

# ---- static local variables
_s_OnCalculate_recount_time = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorPEMADigitR(_MQL5Indicator):
    name = 'ColorPEMA_Digit_r'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'EmaLength': 50.01,  # глубина сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # cдвиг индикатора по вертикали в пунктах
        'Digit': 2,  # количество разрядов округления
        'ShowPrice': True,  # показывать ценовую метку
        'RecountMode': _Choice({1: 'Обрезаем только пересчёт баров', 2: 'Обрезаем только пересчёт во времени', 3: 'Полная оптимизация пересчётов'}, default=3),  # Способ ограничения расчётов индикатора
        'CountBars': 500,  # количество баров для расчёта индикатора
        'ReCountTime': 60,  # время в секундах между расчётами индикатора
    }

