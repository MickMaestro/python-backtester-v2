"""ColorXPWMA_Digit_StDev — converted from MQL5: MQL5 Indicators/ColorXPWMA_Digit_StDev/ColorXPWMA_Digit_StDev.mq5

Power weighted moving average
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 5}, 'types': {1: 8, 2: 5, 3: 5, 4: 5, 5: 5}, 'colors': {1: [16711935, 8421504, 3329330], 2: [255], 3: [16748574], 4: [255], 5: [16748574]}, 'widths': {1: 3, 2: 2, 3: 2, 4: 5, 5: 5}, 'styles': {1: 0}, 'labels': {1: 'ColoXPWMA_Digit', 2: 'Dn_Signal 1', 3: 'Up_Signal 1', 4: 'Dn_Signal 2', 5: 'Up_Signal 2'}, 'levels': [], 'description': ['Power weighted moving average'], 'name': 'ColorXPWMA_Digit_StDev', 'source': 'MQL5 Indicators/ColorXPWMA_Digit_StDev/ColorXPWMA_Digit_StDev.mq5', 'folder': 'ColorXPWMA_Digit_StDev', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'ColorXPWMA_Digit_StDev', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'iPeriod', 'py': 'iPeriod', 'param': 'iPeriod', 'type': 'uint', 'default': 14, 'label': 'период PWMA', 'sinput': False}, {'mql': 'iPower', 'py': 'iPower', 'param': 'iPower', 'type': 'double', 'default': 2.00001, 'label': 'степень PWMA', 'sinput': False}, {'mql': 'MA_SMethod', 'py': 'MA_SMethod', 'param': 'MA_SMethod', 'type': 'int', 'default': 0, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'MA_Length', 'py': 'MA_Length', 'param': 'MA_Length', 'type': 'uint', 'default': 5, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'MA_Phase', 'py': 'MA_Phase', 'param': 'MA_Phase', 'type': 'int', 'default': 15, 'label': 'параметр первого сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}, {'mql': 'Digit', 'py': 'Digit', 'param': 'Digit', 'type': 'uint', 'default': 2, 'label': 'количество разрядов округления', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': 'показывать ценовую метку', 'sinput': False}, {'mql': 'Price_color', 'py': 'Price_color', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'цвет ценовой метки', 'sinput': False}, {'mql': 'dK1', 'py': 'dK1', 'param': 'dK1', 'type': 'double', 'default': 1.5, 'label': 'коэффициент 1 для квадратичного фильтра', 'sinput': False}, {'mql': 'dK2', 'py': 'dK2', 'param': 'dK2', 'type': 'double', 'default': 2.5, 'label': 'коэффициент 2 для квадратичного фильтра', 'sinput': False}, {'mql': 'std_period', 'py': 'std_period', 'param': 'std_period', 'type': 'uint', 'default': 9, 'label': 'период квадратичного фильтра', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
SirName = _input('SirName', 'ColorXPWMA_Digit_StDev')  # Первая часть имени графических объектов
iPeriod = _input('iPeriod', 14)  # период PWMA
iPower = _input('iPower', 2.00001)  # степень PWMA
MA_SMethod = _input('MA_SMethod', MODE_SMA_)  # Метод усреднения
MA_Length = _input('MA_Length', 5)  # Глубина сглаживания
MA_Phase = _input('MA_Phase', 15)  # параметр первого сглаживания,
IPC = _input('IPC', PRICE_CLOSE_)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
Digit = _input('Digit', 2)  # количество разрядов округления
ShowPrice = _input('ShowPrice', True)  # показывать ценовую метку
Price_color = _input('Price_color', clrGray)  # цвет ценовой метки
dK1 = _input('dK1', 1.5)  # коэффициент 1 для квадратичного фильтра
dK2 = _input('dK2', 2.5)  # коэффициент 2 для квадратичного фильтра
std_period = _input('std_period', 9)  # период квадратичного фильтра
ExtLineBuffer = Arr(0, 0.0)
ColorExtLineBuffer = Arr(0, 0.0)
BearsBuffer1 = Arr(0, 0.0)
BullsBuffer1 = Arr(0, 0.0)
BearsBuffer2 = Arr(0, 0.0)
BullsBuffer2 = Arr(0, 0.0)
min_rates_1 = 0
min_rates_total = 0
dPriceShift = 0.0
PointPow10 = 0.0
Pw = Arr(0, 0.0)
SumPw = 0.0
XPWMA = Arr(0, 0.0)
Price_name = ""

def OnInit():
    global PointPow10, Price_name, SumPw, dPriceShift, min_rates_1, min_rates_total
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    min_rates_1 = _int(iPeriod)
    min_rates_total = min_rates_1 + GetStartBars(MA_SMethod, MA_Length, MA_Phase)
    ArrayResize(XPWMA, std_period)
    ArrayResize(Pw, iPeriod)
    SumPw = 0.0
    for kkk in range(0, _int(iPeriod)):
        Pw[kkk] = pow(_int(iPeriod) - kkk, iPower)
        SumPw += Pw[kkk]
    dPriceShift = Point() * PriceShift
    PointPow10 = Point() * MathPow(10, Digit)
    Price_name = SirName + 'Price'
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box("")
    StringConcatenate(shortname, 'ColorXPWMA_Digit_StDev(', iPeriod, ' ,', DoubleToString(iPower, 3), ')')
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    SetIndexBuffer(1, ColorExtLineBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BearsBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, BullsBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(4, BearsBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(5, BullsBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_ARROW, 159)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)

def OnDeinit(reason):
    ObjectDelete(0, Price_name)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    sum1 = 0.0
    pwma = 0.0
    xpwma = 0.0
    SMAdif = 0.0
    Sum = 0.0
    StDev = 0.0
    dstd = 0.0
    BEARS1 = 0.0
    BULLS1 = 0.0
    BEARS2 = 0.0
    BULLS2 = 0.0
    Filter1 = 0.0
    Filter2 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        sum1 = 0.0
        for kkk in range(0, _int(iPeriod)):
            sum1 += PriceSeries(IPC, bar - kkk, open, low, high, close) * Pw[kkk]
        pwma = (_fdiv(sum1, SumPw) if (SumPw != 0) else EMPTY_VALUE)
        xpwma = XMA1.XMASeries(min_rates_1, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, pwma, bar, False)
        xpwma += dPriceShift
        ExtLineBuffer[bar] = PointPow10 * MathRound(_fdiv(xpwma, PointPow10))
    else:
        bar = _range_end(bar, rates_total, 1)
    if ShowPrice:
        bar0 = rates_total - 1
        time0 = time[bar0] + (1 * PeriodSeconds())
        SetRightPrice(0, Price_name, 0, time0, ExtLineBuffer[bar0], Price_color)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        clr = 1.0
        trend = ExtLineBuffer[bar] - ExtLineBuffer[bar - 1]
        if not trend:
            clr = ColorExtLineBuffer[bar - 1]
        else:
            if trend > 0:
                clr = 2.0
            if trend < 0:
                clr = 0.0
        ColorExtLineBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first
    for bar in range(bar, rates_total):
        for iii in range(0, _int(std_period)):
            XPWMA[iii] = ExtLineBuffer[bar - iii] - ExtLineBuffer[bar - iii - 1]
        Sum = 0.0
        for iii in range(0, _int(std_period)):
            Sum += XPWMA[iii]
        SMAdif = Sum / std_period
        Sum = 0.0
        for iii in range(0, _int(std_period)):
            Sum += MathPow(XPWMA[iii] - SMAdif, 2)
        StDev = MathSqrt(Sum / std_period)
        dstd = NormalizeDouble(XPWMA[0], Digits() + 2)
        Filter1 = NormalizeDouble(dK1 * StDev, Digits() + 2)
        Filter2 = NormalizeDouble(dK2 * StDev, Digits() + 2)
        BEARS1 = EMPTY_VALUE
        BULLS1 = EMPTY_VALUE
        BEARS2 = EMPTY_VALUE
        BULLS2 = EMPTY_VALUE
        xpwma = ExtLineBuffer[bar]
        if dstd < (-Filter1) and dstd >= (-Filter2):
            BEARS1 = xpwma
        if dstd < (-Filter2):
            BEARS2 = xpwma
        if dstd > Filter1 and dstd <= Filter2:
            BULLS1 = xpwma
        if dstd > Filter2:
            BULLS2 = xpwma
        BullsBuffer1[bar] = BULLS1
        BearsBuffer1[bar] = BEARS1
        BullsBuffer2[bar] = BULLS2
        BearsBuffer2[bar] = BEARS2
    else:
        bar = _range_end(bar, rates_total, 1)
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
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorXPWMADigitStDev(_MQL5Indicator):
    name = 'ColorXPWMA_Digit_StDev'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iPeriod': 14,  # период PWMA
        'iPower': 2.00001,  # степень PWMA
        'MA_SMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения
        'MA_Length': 5,  # Глубина сглаживания
        'MA_Phase': 15,  # параметр первого сглаживания,
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
        'Digit': 2,  # количество разрядов округления
        'ShowPrice': True,  # показывать ценовую метку
        'dK1': 1.5,  # коэффициент 1 для квадратичного фильтра
        'dK2': 2.5,  # коэффициент 2 для квадратичного фильтра
        'std_period': 9,  # период квадратичного фильтра
    }

