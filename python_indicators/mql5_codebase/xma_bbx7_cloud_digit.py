"""xma_bbx7_cloud_digit — converted from MQL5: MQL5 Indicators/XMA_BBx7_Cloud_Digit/xma_bbx7_cloud_digit.mq5

XMA Bollinger Bands
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 11, 'indicator_plots': 6}, 'types': {1: 7, 2: 7, 3: 7, 4: 1, 5: 7, 6: 7}, 'colors': {1: [16760576], 2: [65280], 3: [16443110], 4: [14822282], 5: [16711935], 6: [13850042]}, 'widths': {4: 2}, 'styles': {4: 0}, 'labels': {1: 'Upper Sigma3 Cloud', 2: 'Upper Sigma2 Cloud', 3: 'Sigma1 Cloud', 4: 'XMA', 5: 'Lower Sigma2 Cloud', 6: 'Lower Sigma3 Cloud'}, 'levels': [], 'description': ['XMA Bollinger Bands'], 'name': 'xma_bbx7_cloud_digit', 'source': 'MQL5 Indicators/XMA_BBx7_Cloud_Digit/xma_bbx7_cloud_digit.mq5', 'folder': 'XMA_BBx7_Cloud_Digit', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 100, 'label': 'Глубина  усреднения', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр первого усреднения', 'sinput': False}, {'mql': 'BandsDeviation1', 'py': 'BandsDeviation1', 'param': 'BandsDeviation1', 'type': 'double', 'default': 2.0, 'label': 'Девиация 1', 'sinput': False}, {'mql': 'BandsDeviation2', 'py': 'BandsDeviation2', 'param': 'BandsDeviation2', 'type': 'double', 'default': 3.0, 'label': 'Девиация 2', 'sinput': False}, {'mql': 'BandsDeviation3', 'py': 'BandsDeviation3', 'param': 'BandsDeviation3', 'type': 'double', 'default': 4.0, 'label': 'Девиация 3', 'sinput': False}, {'mql': 'Digit', 'py': 'Digit', 'param': 'Digit', 'type': 'uint', 'default': 2, 'label': 'Количество разрядов округления', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': 'Показывать ценовые метки', 'sinput': False}, {'mql': 'Middle_color', 'py': 'Middle_color', 'param': None, 'type': 'color', 'default': 16711680, 'label': '', 'sinput': False}, {'mql': 'Upper_color1', 'py': 'Upper_color1', 'param': None, 'type': 'color', 'default': 7451452, 'label': '', 'sinput': False}, {'mql': 'Lower_color1', 'py': 'Lower_color1', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'Upper_color2', 'py': 'Upper_color2', 'param': None, 'type': 'color', 'default': 16748574, 'label': '', 'sinput': False}, {'mql': 'Lower_color2', 'py': 'Lower_color2', 'param': None, 'type': 'color', 'default': 16711935, 'label': '', 'sinput': False}, {'mql': 'Upper_color3', 'py': 'Upper_color3', 'param': None, 'type': 'color', 'default': 16711680, 'label': '', 'sinput': False}, {'mql': 'Lower_color3', 'py': 'Lower_color3', 'param': None, 'type': 'color', 'default': 42495, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XMA_Method = _input('XMA_Method', MODE_SMA)  # Метод усреднения
XLength = _input('XLength', 100)  # Глубина  усреднения
XPhase = _input('XPhase', 15)  # Параметр первого усреднения
BandsDeviation1 = _input('BandsDeviation1', 2.0)  # Девиация 1
BandsDeviation2 = _input('BandsDeviation2', 3.0)  # Девиация 2
BandsDeviation3 = _input('BandsDeviation3', 4.0)  # Девиация 3
Digit = _input('Digit', 2)  # Количество разрядов округления
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
ShowPrice = _input('ShowPrice', True)  # Показывать ценовые метки
Middle_color = _input('Middle_color', clrBlue)
Upper_color1 = _input('Upper_color1', clrMediumSeaGreen)
Lower_color1 = _input('Lower_color1', clrRed)
Upper_color2 = _input('Upper_color2', clrDodgerBlue)
Lower_color2 = _input('Lower_color2', clrMagenta)
Upper_color3 = _input('Upper_color3', clrBlue)
Lower_color3 = _input('Lower_color3', clrOrange)
ExtLineBuffer0 = Arr(0, 0.0)
UpBuffer1 = Arr(0, 0.0)
DnBuffer1 = Arr(0, 0.0)
UpBuffer2 = Arr(0, 0.0)
DnBuffer2 = Arr(0, 0.0)
UpBuffer3 = Arr(0, 0.0)
DnBuffer3 = Arr(0, 0.0)
UpBuffer4 = Arr(0, 0.0)
DnBuffer4 = Arr(0, 0.0)
UpBuffer5 = Arr(0, 0.0)
DnBuffer5 = Arr(0, 0.0)
dPriceShift = 0.0
PointPow10 = 0.0
min_rates_total = 0
min_rates_1 = 0
upper_name1 = ""
middle_name = ""
lower_name1 = ""
upper_name2 = ""
lower_name2 = ""
upper_name3 = ""
lower_name3 = ""

def OnInit():
    global PointPow10, dPriceShift, lower_name1, lower_name2, lower_name3, middle_name, min_rates_1, min_rates_total, upper_name1, upper_name2, upper_name3
    min_rates_1 = GetStartBars(XMA_Method, XLength, XPhase) + 1
    min_rates_total = min_rates_1 + _int(XLength)
    PointPow10 = Point() * MathPow(10, Digit)
    XMA1.XMALengthCheck('XLength', XLength)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    dPriceShift = Point() * PriceShift
    if BandsDeviation1 >= BandsDeviation2:
        Print('Входной параметр Девиация 2 всегда должен быть больше входного параметра Девиация 1! Исправьте значения этих входных параметров индикатора!')
        return INIT_FAILED
    if BandsDeviation2 >= BandsDeviation3:
        Print('Входной параметр Девиация 3 всегда должен быть больше входного параметра Девиация 2! Исправьте значения этих входных параметров индикатора!')
        return INIT_FAILED
    upper_name1 = 'Price_Channel_Central upper text lable 1'
    middle_name = 'Price_Channel_Central middle text lable'
    lower_name1 = 'Price_Channel_Central lower text lable 1'
    upper_name2 = 'Price_Channel_Central upper text lable 2'
    lower_name2 = 'Price_Channel_Central lower text lable 2'
    upper_name3 = 'Price_Channel_Central upper text lable 3'
    lower_name3 = 'Price_Channel_Central lower text lable 3'
    SetIndexBuffer(0, UpBuffer4, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer4, INDICATOR_DATA)
    SetIndexBuffer(2, UpBuffer2, INDICATOR_DATA)
    SetIndexBuffer(3, DnBuffer2, INDICATOR_DATA)
    SetIndexBuffer(4, UpBuffer1, INDICATOR_DATA)
    SetIndexBuffer(5, DnBuffer1, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLineBuffer0, INDICATOR_DATA)
    SetIndexBuffer(7, UpBuffer3, INDICATOR_DATA)
    SetIndexBuffer(8, DnBuffer3, INDICATOR_DATA)
    SetIndexBuffer(9, UpBuffer5, INDICATOR_DATA)
    SetIndexBuffer(10, DnBuffer5, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(5, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box("")
    Smooth = XMA1.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'XMA_Bollinger Bands(', Smooth, ', ', XLength, ', ', DoubleToString(BandsDeviation1, 2), ', ', DoubleToString(BandsDeviation2, 2), ', ', DoubleToString(BandsDeviation3, 2), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, upper_name1)
    ObjectDelete(0, middle_name)
    ObjectDelete(0, lower_name1)
    ObjectDelete(0, upper_name2)
    ObjectDelete(0, lower_name2)
    ObjectDelete(0, upper_name3)
    ObjectDelete(0, lower_name3)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    xma = 0.0
    line = 0.0
    stdev = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        xma = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, price, bar, False)
        line = xma + dPriceShift
        ExtLineBuffer0[bar] = PointPow10 * MathRound(_fdiv(xma + dPriceShift, PointPow10))
        stdev = STD1.StdDevSeries(min_rates_1, prev_calculated, rates_total, XLength, BandsDeviation1, price, xma, bar, False)
        DnBuffer2[bar] = PointPow10 * MathCeil(_fdiv(line + stdev, PointPow10))
        UpBuffer1[bar] = DnBuffer2[bar]
        UpBuffer3[bar] = PointPow10 * MathFloor(_fdiv(line - stdev, PointPow10))
        DnBuffer1[bar] = UpBuffer3[bar]
        if ExtLineBuffer0[bar] >= UpBuffer1[bar]:
            DnBuffer2[bar] = ExtLineBuffer0[bar] + PointPow10
            UpBuffer1[bar] = DnBuffer2[bar]
        if ExtLineBuffer0[bar] <= DnBuffer1[bar]:
            UpBuffer3[bar] = ExtLineBuffer0[bar] - PointPow10
            DnBuffer1[bar] = UpBuffer3[bar]
        stdev = STD2.StdDevSeries(min_rates_1, prev_calculated, rates_total, XLength, BandsDeviation2, price, xma, bar, False)
        DnBuffer4[bar] = PointPow10 * MathCeil(_fdiv(line + stdev, PointPow10))
        UpBuffer2[bar] = DnBuffer4[bar]
        UpBuffer5[bar] = PointPow10 * MathFloor(_fdiv(line - stdev, PointPow10))
        DnBuffer3[bar] = UpBuffer5[bar]
        if UpBuffer1[bar] >= UpBuffer2[bar]:
            DnBuffer4[bar] = UpBuffer1[bar] + PointPow10
            UpBuffer2[bar] = DnBuffer4[bar]
        if DnBuffer1[bar] <= DnBuffer3[bar]:
            UpBuffer5[bar] = DnBuffer1[bar] - PointPow10
            DnBuffer3[bar] = UpBuffer5[bar]
        stdev = STD3.StdDevSeries(min_rates_1, prev_calculated, rates_total, XLength, BandsDeviation3, price, xma, bar, False)
        UpBuffer4[bar] = PointPow10 * MathCeil(_fdiv(line + stdev, PointPow10))
        DnBuffer5[bar] = PointPow10 * MathFloor(_fdiv(line - stdev, PointPow10))
        if UpBuffer2[bar] >= UpBuffer4[bar]:
            UpBuffer4[bar] = UpBuffer2[bar] + PointPow10
        if DnBuffer3[bar] <= DnBuffer5[bar]:
            DnBuffer5[bar] = DnBuffer3[bar] - PointPow10
    else:
        bar = _range_end(bar, rates_total, 1)
    if ShowPrice:
        bar0 = rates_total - 1
        time0 = time[bar0] + (Shift * PeriodSeconds())
        SetRightPrice(0, middle_name, 0, time0, ExtLineBuffer0[bar0], Middle_color, 'Georgia')
        SetRightPrice(0, upper_name1, 0, time0, UpBuffer1[bar0], Upper_color1, 'Georgia')
        SetRightPrice(0, lower_name1, 0, time0, DnBuffer1[bar0], Lower_color1, 'Georgia')
        SetRightPrice(0, upper_name2, 0, time0, UpBuffer2[bar0], Upper_color2, 'Georgia')
        SetRightPrice(0, lower_name2, 0, time0, DnBuffer3[bar0], Lower_color2, 'Georgia')
        SetRightPrice(0, upper_name3, 0, time0, UpBuffer4[bar0], Upper_color3, 'Georgia')
        SetRightPrice(0, lower_name3, 0, time0, DnBuffer5[bar0], Lower_color3, 'Georgia')
    ChartRedraw(0)
    return rates_total

def CreateRightPrice(chart_id, name, nwin, time, price, Color, Font):
    ObjectCreate(chart_id, name, OBJ_ARROW_RIGHT_PRICE, nwin, time, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetString(chart_id, name, OBJPROP_FONT, Font)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, 2)

def SetRightPrice(chart_id, name, nwin, time, price, Color, Font):
    if ObjectFind(chart_id, name) == -1:
        CreateRightPrice(chart_id, name, nwin, time, price, Color, Font)
    else:
        ObjectMove(chart_id, name, 0, time, price)

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
STD1 = _alloc(CStdDeviation)
STD1.__init__()
STD2 = _alloc(CStdDeviation)
STD2.__init__()
STD3 = _alloc(CStdDeviation)
STD3.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XmaBbx7CloudDigit(_MQL5Indicator):
    name = 'xma_bbx7_cloud_digit'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения
        'XLength': 100,  # Глубина  усреднения
        'XPhase': 15,  # Параметр первого усреднения
        'BandsDeviation1': 2.0,  # Девиация 1
        'BandsDeviation2': 3.0,  # Девиация 2
        'BandsDeviation3': 4.0,  # Девиация 3
        'Digit': 2,  # Количество разрядов округления
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
        'ShowPrice': True,  # Показывать ценовые метки
    }

