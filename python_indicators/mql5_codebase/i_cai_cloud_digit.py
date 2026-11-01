"""i-CAi_Cloud_Digit — converted from MQL5: MQL5 Indicators/i-CAi_Cloud_Digit/i-CAi_Cloud_Digit.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 7, 2: 7, 3: 8}, 'colors': {1: [15130800], 2: [13353215], 3: [16748574, 16711935]}, 'widths': {3: 5}, 'styles': {3: 0}, 'labels': {1: 'Upper Cloud', 2: 'Lower Cloud', 3: 'i-CAi_Digit'}, 'levels': [], 'description': [], 'name': 'i-CAi_Cloud_Digit', 'source': 'MQL5 Indicators/i-CAi_Cloud_Digit/i-CAi_Cloud_Digit.mq5', 'folder': 'i-CAi_Cloud_Digit', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'i-CAi_Digit', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 12, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Digit', 'py': 'Digit', 'param': 'Digit', 'type': 'uint', 'default': 2, 'label': 'количество разрядов округления', 'sinput': False}, {'mql': 'Dev', 'py': 'Dev', 'param': 'Dev', 'type': 'uint', 'default': 20, 'label': 'девиация заливки фоном', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': 'показывать ценовые меток', 'sinput': False}, {'mql': 'Price_color', 'py': 'Price_color', 'param': None, 'type': 'color', 'default': 13828244, 'label': 'цвета ценовых меток', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
SirName = _input('SirName', 'i-CAi_Digit')  # Первая часть имени графических объектов
XMA_Method = _input('XMA_Method', MODE_SMA_)  # метод усреднения
XLength = _input('XLength', 12)  # глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр сглаживания,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Digit = _input('Digit', 2)  # количество разрядов округления
Dev = _input('Dev', 20)  # девиация заливки фоном
ShowPrice = _input('ShowPrice', True)  # показывать ценовые меток
Price_color = _input('Price_color', clrDarkViolet)  # цвета ценовых меток
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
LineBuffer = Arr(0, 0.0)
ColorLineBuffer = Arr(0, 0.0)
UpCloudBuffer1 = Arr(0, 0.0)
UpCloudBuffer2 = Arr(0, 0.0)
DnCloudBuffer1 = Arr(0, 0.0)
DnCloudBuffer2 = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0
PointPow10 = 0.0
Price_name = ""

def OnInit():
    global PointPow10, Price_name, min_rates_total
    min_rates_total = GetStartBars(XMA_Method, XLength, XPhase)
    PointPow10 = Point() * MathPow(10, Digit)
    Price_name = SirName + 'Price'
    SetIndexBuffer(0, UpCloudBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, UpCloudBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, DnCloudBuffer1, INDICATOR_DATA)
    SetIndexBuffer(3, DnCloudBuffer2, INDICATOR_DATA)
    SetIndexBuffer(4, LineBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ColorLineBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'i-CAi_Digit(', XLength, ', ', Smooth1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnDeinit(reason):
    ObjectDelete(0, Price_name)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    xma = 0.0
    stdev = 0.0
    powstdev = 0.0
    powdxma = 0.0
    koeff = 0.0
    prev = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        xma = XMA1.XMASeries(1, prev_calculated, rates_total, XMA_Method, XPhase, XLength, price, bar, False)
        stdev = STD.StdDevSeries(1, prev_calculated, rates_total, XLength, 1.0, price, xma, bar, False)
        powstdev = MathPow(stdev, 2)
        if bar > min_rates_total:
            prev = LineBuffer[bar - 1]
        else:
            prev = xma
        powdxma = MathPow(prev - xma, 2)
        if powdxma < powstdev or (not powdxma):
            koeff = 0.0
        else:
            koeff = 1.0 - _fdiv(powstdev, powdxma)
        LineBuffer[bar] = prev + (koeff * (xma - prev))
        DnCloudBuffer1[bar] = PointPow10 * MathRound(_fdiv(LineBuffer[bar], PointPow10))
        UpCloudBuffer2[bar] = DnCloudBuffer1[bar]
        LineBuffer[bar] = UpCloudBuffer2[bar]
        UpCloudBuffer1[bar] = LineBuffer[bar] * Dev
        DnCloudBuffer2[bar] = LineBuffer[bar] / Dev
    else:
        bar = _range_end(bar, rates_total, 1)
    if ShowPrice:
        bar0 = rates_total - 1
        time0 = time[bar0] + (1 * PeriodSeconds())
        SetRightPrice(0, Price_name, 0, time0, LineBuffer[bar0], Price_color)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        clr = _int(ColorLineBuffer[bar - 1])
        if LineBuffer[bar - 1] < LineBuffer[bar]:
            clr = 0
        if LineBuffer[bar - 1] > LineBuffer[bar]:
            clr = 1
        ColorLineBuffer[bar] = clr
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
STD = _alloc(CStdDeviation)
STD.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ICAiCloudDigit(_MQL5Indicator):
    name = 'i-CAi_Cloud_Digit'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения
        'XLength': 12,  # глубина сглаживания
        'XPhase': 15,  # параметр сглаживания,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Digit': 2,  # количество разрядов округления
        'Dev': 20,  # девиация заливки фоном
        'ShowPrice': True,  # показывать ценовые меток
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

