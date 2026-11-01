"""Color_QEMA_Digit — converted from MQL5: MQL5 Indicators/Color_QEMA_Digit_HTF/Color_QEMA_Digit.mq5

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

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [42495, 8421376]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'Color_QEMA_Digit'}, 'levels': [], 'description': ['Pentuple Exponential Moving Average'], 'name': 'Color_QEMA_Digit', 'source': 'MQL5 Indicators/Color_QEMA_Digit_HTF/Color_QEMA_Digit.mq5', 'folder': 'Color_QEMA_Digit_HTF', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'Color_QEMA_Digit', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'EmaLength', 'py': 'EmaLength', 'param': 'EmaLength', 'type': 'double', 'default': 50.01, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}, {'mql': 'Digit', 'py': 'Digit', 'param': 'Digit', 'type': 'uint', 'default': 2, 'label': 'количество разрядов округления', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': 'показывать ценовую метку', 'sinput': False}, {'mql': 'Price_color', 'py': 'Price_color', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'цвет ценовой метки', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
SirName = _input('SirName', 'Color_QEMA_Digit')  # Первая часть имени графических объектов
EmaLength = _input('EmaLength', 50.01)  # глубина сглаживания
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
Digit = _input('Digit', 2)  # количество разрядов округления
ShowPrice = _input('ShowPrice', True)  # показывать ценовую метку
Price_color = _input('Price_color', clrGray)  # цвет ценовой метки
ExtLineBuffer = Arr(0, 0.0)
ColorExtLineBuffer = Arr(0, 0.0)
dPriceShift = 0.0
PointPow10 = 0.0
Price_name = ""
min_rates_total = 0

def OnInit():
    global PointPow10, Price_name, dPriceShift, min_rates_total
    min_rates_total = 6
    PointPow10 = Point() * MathPow(10, Digit)
    Price_name = SirName + 'Price'
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorExtLineBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtLineBuffer, False)
    ArraySetAsSeries(ColorExtLineBuffer, False)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'Color_QEMA_Digit( Length = ', EmaLength, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    dPriceShift = Point() * PriceShift

def OnDeinit(reason):
    ObjectDelete(0, Price_name)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    res = Arr(6, 0.0, dyn=False)
    QEMA = 0.0
    trend = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    ArraySetAsSeries(open, False)
    ArraySetAsSeries(high, False)
    ArraySetAsSeries(low, False)
    ArraySetAsSeries(close, False)
    bar = first
    for bar in range(bar, rates_total):
        res[0] = PriceSeries(IPC, bar, open, low, high, close)
        res[1] = EMA[0].EMASeries(0, prev_calculated, rates_total, EmaLength, res[0], bar, False)
        res[2] = EMA[1].EMASeries(1, prev_calculated, rates_total, EmaLength, res[1], bar, False)
        res[3] = EMA[2].EMASeries(2, prev_calculated, rates_total, EmaLength, res[2], bar, False)
        res[4] = EMA[3].EMASeries(3, prev_calculated, rates_total, EmaLength, res[3], bar, False)
        res[5] = EMA[4].EMASeries(4, prev_calculated, rates_total, EmaLength, res[4], bar, False)
        QEMA = (5 * res[1]) - (10 * res[2]) + (10 * res[3]) - (5 * res[4]) + res[5]
        ExtLineBuffer[bar] = (PointPow10 * MathRound(_fdiv(QEMA, PointPow10))) + dPriceShift
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
        clr = ColorExtLineBuffer[bar - 1]
        trend = ExtLineBuffer[bar] - ExtLineBuffer[bar - 1]
        if trend > 0:
            clr = 1.0
        if trend < 0:
            clr = 0.0
        ColorExtLineBuffer[bar] = clr
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
EMA = Arr(5, 0, dyn=False, factory=CMoving_Average)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorQEMADigit(_MQL5Indicator):
    name = 'Color_QEMA_Digit'
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
    }

