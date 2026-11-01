"""AbsolutelyNoLagLwma_Digit — converted from MQL5: MQL5 Indicators/AbsolutelyNoLagLwma_Digit/AbsolutelyNoLagLwma_Digit.mq5

Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [15631086, 8421504, 16748574]}, 'widths': {1: 4}, 'styles': {1: 0}, 'labels': {1: 'AbsolutelyNoLagLwma_Digit'}, 'levels': [], 'description': [], 'name': 'AbsolutelyNoLagLwma_Digit', 'source': 'MQL5 Indicators/AbsolutelyNoLagLwma_Digit/AbsolutelyNoLagLwma_Digit.mq5', 'folder': 'AbsolutelyNoLagLwma_Digit', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'AbsolutelyNoLagLwma_Digit', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 7, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг по вертикали в пунктах', 'sinput': False}, {'mql': 'Digit', 'py': 'Digit', 'param': 'Digit', 'type': 'uint', 'default': 2, 'label': 'количество разрядов округления', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': 'показывать ценовые метки', 'sinput': False}, {'mql': 'UpPrice_color', 'py': 'UpPrice_color', 'param': None, 'type': 'color', 'default': 7451452, 'label': 'цвет цены выше мувинга', 'sinput': False}, {'mql': 'Price_color', 'py': 'Price_color', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'цвет цены равен мувингу', 'sinput': False}, {'mql': 'DnPrice_color', 'py': 'DnPrice_color', 'param': None, 'type': 'color', 'default': 255, 'label': 'цвет цены ниже мувинга', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
SirName = _input('SirName', 'AbsolutelyNoLagLwma_Digit')  # Первая часть имени графических объектов
Length = _input('Length', 7)  # глубина сглаживания
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг по вертикали в пунктах
Digit = _input('Digit', 2)  # количество разрядов округления
ShowPrice = _input('ShowPrice', True)  # показывать ценовые метки
UpPrice_color = _input('UpPrice_color', clrMediumSeaGreen)  # цвет цены выше мувинга
Price_color = _input('Price_color', clrGray)  # цвет цены равен мувингу
DnPrice_color = _input('DnPrice_color', clrRed)  # цвет цены ниже мувинга
ExtLineBuffer = Arr(0, 0.0)
ColorExtLineBuffer = Arr(0, 0.0)
min_rates_total = 0
dPriceShift = 0.0
PointPow10 = 0.0
Price_name = ""
Count = Arr(0, 0)
Price = Arr(0, 0.0)
Lwma = Arr(0, 0.0)

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

def OnDeinit(reason):
    ObjectDelete(0, Price_name)
    ChartRedraw(0)

def OnInit():
    global PointPow10, Price_name, dPriceShift, min_rates_total
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    min_rates_total = _int(Length * 2.0)
    PointPow10 = Point() * MathPow(10, Digit)
    Price_name = SirName + 'Price'
    ArrayResize(Count, Length)
    ArrayResize(Price, Length)
    ArrayResize(Lwma, Length)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box("")
    StringConcatenate(shortname, 'AbsolutelyNoLagLwma(', Length, ')')
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    SetIndexBuffer(1, ColorExtLineBuffer, INDICATOR_COLOR_INDEX)
    dPriceShift = Point() * PriceShift

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    weight = 0
    clr = 0
    sum_ = 0.0
    sumw = 0.0
    lwma2 = 0.0
    trend = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        ArrayInitialize(Count, 0)
        ArrayInitialize(Price, 0.0)
        ArrayInitialize(Lwma, 0.0)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        Price[Count[0]] = PriceSeries(IPC, bar, open, low, high, close)
        sum_ = 0.0
        sumw = 0.0
        for kkk in range(0, _int(Length)):
            weight = _int(Length) - kkk
            sumw += weight
            sum_ += weight * Price[Count[kkk]]
        if sumw:
            Lwma[Count[0]] = _fdiv(sum_, sumw)
        else:
            Lwma[Count[0]] = 0.0
        sum_ = 0.0
        sumw = 0.0
        for kkk in range(0, _int(Length)):
            weight = _int(Length) - kkk
            sumw += weight
            sum_ += weight * Lwma[Count[kkk]]
        if sumw:
            lwma2 = _fdiv(sum_, sumw)
        else:
            lwma2 = 0.0
        ExtLineBuffer[bar] = lwma2 + dPriceShift
        ExtLineBuffer[bar] = PointPow10 * MathRound(_fdiv(ExtLineBuffer[bar], PointPow10))
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count, Length)
    else:
        bar = _range_end(bar, rates_total, 1)
    if ShowPrice:
        bar0 = rates_total - 1
        lwma2 = NormalizeDouble(ExtLineBuffer[bar0], Digits())
        time0 = time[bar0] + (1 * PeriodSeconds())
        PrColor = Price_color
        if lwma2 < PriceSeries(IPC, bar0, open, low, high, close):
            PrColor = UpPrice_color
        elif lwma2 > PriceSeries(IPC, bar0, open, low, high, close):
            PrColor = DnPrice_color
        SetRightPrice(0, Price_name, 0, time0, ExtLineBuffer[bar0], PrColor)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total + 1
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
    ChartRedraw(0)
    return rates_total

def PriceSeries(applied_price, bar, Open, Low, High, Close):
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        return Close[bar]
    elif _sw1 == PRICE_OPEN:
        return Open[bar]
    elif _sw1 == PRICE_HIGH:
        return High[bar]
    elif _sw1 == PRICE_LOW:
        return Low[bar]
    elif _sw1 == PRICE_MEDIAN:
        return (High[bar] + Low[bar]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (Close[bar] + High[bar] + Low[bar]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * Close[bar]) + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 8:
        return (Open[bar] + Close[bar]) / 2.0
    elif _sw1 == 9:
        return (Open[bar] + Close[bar] + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 10:
        if Close[bar] > Open[bar]:
            return High[bar]
        else:
            if Close[bar] < Open[bar]:
                return Low[bar]
            else:
                return Close[bar]
    elif _sw1 == 11:
        if Close[bar] > Open[bar]:
            return (High[bar] + Close[bar]) / 2.0
        else:
            if Close[bar] < Open[bar]:
                return (Low[bar] + Close[bar]) / 2.0
            else:
                return Close[bar]
    elif _sw1 == 12:
        res = High[bar] + Low[bar] + Close[bar]
        if Close[bar] < Open[bar]:
            res = (res + Low[bar]) / 2
        if Close[bar] > Open[bar]:
            res = (res + High[bar]) / 2
        if Close[bar] == Open[bar]:
            res = (res + Close[bar]) / 2
        return (res - Low[bar] + (res - High[bar])) / 2
    else:
        return Close[bar]

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

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AbsolutelyNoLagLwmaDigit(_MQL5Indicator):
    name = 'AbsolutelyNoLagLwma_Digit'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Length': 7,  # глубина сглаживания
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг по горизонтали в барах
        'PriceShift': 0,  # cдвиг по вертикали в пунктах
        'Digit': 2,  # количество разрядов округления
        'ShowPrice': True,  # показывать ценовые метки
    }

