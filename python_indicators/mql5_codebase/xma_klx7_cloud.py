"""xma_klx7_cloud — converted from MQL5: MQL5 Indicators/XMA_KLx7_Cloud/xma_klx7_cloud.mq5

XMA Keltner Channel
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 11, 'indicator_plots': 6}, 'types': {1: 7, 2: 7, 3: 7, 4: 1, 5: 7, 6: 7}, 'colors': {1: [16776960], 2: [10025880], 3: [16443110], 4: [16711680], 5: [12695295], 6: [55295]}, 'widths': {4: 2}, 'styles': {4: 0}, 'labels': {1: 'Upper Sigma3 Cloud', 2: 'Upper Sigma2 Cloud', 3: 'Sigma1 Cloud', 4: 'XMA', 5: 'Lower Sigma2 Cloud', 6: 'Lower Sigma3 Cloud'}, 'levels': [], 'description': ['XMA Keltner Channel'], 'name': 'xma_klx7_cloud', 'source': 'MQL5 Indicators/XMA_KLx7_Cloud/xma_klx7_cloud.mq5', 'folder': 'XMA_KLx7_Cloud', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 100, 'label': 'Глубина  усреднения', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр первого усреднения', 'sinput': False}, {'mql': 'KeltnerPeriod', 'py': 'KeltnerPeriod', 'param': 'KeltnerPeriod', 'type': 'uint', 'default': 20, 'label': 'Период усреднения Кёлтнера', 'sinput': False}, {'mql': 'Ratio1', 'py': 'Ratio1', 'param': 'Ratio1', 'type': 'double', 'default': 1.0, 'label': 'Коэффициент первого уровня', 'sinput': False}, {'mql': 'Ratio2', 'py': 'Ratio2', 'param': 'Ratio2', 'type': 'double', 'default': 2.0, 'label': 'Коэффициент второго уровня', 'sinput': False}, {'mql': 'Ratio3', 'py': 'Ratio3', 'param': 'Ratio3', 'type': 'double', 'default': 3.0, 'label': 'Коэффициент третьего уровня', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}, {'mql': 'Middle_color', 'py': 'Middle_color', 'param': None, 'type': 'color', 'default': 16711680, 'label': '', 'sinput': False}, {'mql': 'Upper_color1', 'py': 'Upper_color1', 'param': None, 'type': 'color', 'default': 7451452, 'label': '', 'sinput': False}, {'mql': 'Lower_color1', 'py': 'Lower_color1', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'Upper_color2', 'py': 'Upper_color2', 'param': None, 'type': 'color', 'default': 16748574, 'label': '', 'sinput': False}, {'mql': 'Lower_color2', 'py': 'Lower_color2', 'param': None, 'type': 'color', 'default': 16711935, 'label': '', 'sinput': False}, {'mql': 'Upper_color3', 'py': 'Upper_color3', 'param': None, 'type': 'color', 'default': 16711680, 'label': '', 'sinput': False}, {'mql': 'Lower_color3', 'py': 'Lower_color3', 'param': None, 'type': 'color', 'default': 42495, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
KeltnerPeriod = _input('KeltnerPeriod', 20)  # Период усреднения Кёлтнера
Ratio1 = _input('Ratio1', 1.0)  # Коэффициент первого уровня
Ratio2 = _input('Ratio2', 2.0)  # Коэффициент второго уровня
Ratio3 = _input('Ratio3', 3.0)  # Коэффициент третьего уровня
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
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
min_rates_total = 0
upper_name1 = ""
middle_name = ""
lower_name1 = ""
upper_name2 = ""
lower_name2 = ""
upper_name3 = ""
lower_name3 = ""

def GetKeltner(period, bar, High, Low):
    Resalt = 0.0
    sum_ = 0.0
    for iii in range(0, period):
        sum_ += High[bar - iii] - Low[bar - iii]
    Resalt = _fdiv(sum_, period)
    return Resalt

def OnInit():
    global dPriceShift, lower_name1, lower_name2, lower_name3, middle_name, min_rates_total, upper_name1, upper_name2, upper_name3
    min_rates_total = GetStartBars(XMA_Method, XLength, XPhase) + 1
    min_rates_total += _int(KeltnerPeriod)
    XMA1.XMALengthCheck('XLength', XLength)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    dPriceShift = Point() * PriceShift
    if Ratio1 >= Ratio2:
        Print('Входной параметр Коэффициент второго уровня всегда должен быть больше входного параметра Коэффициент первого уровня! Исправьте значения этих входных параметров индикатора!')
        return INIT_FAILED
    if Ratio2 >= Ratio3:
        Print('Входной параметр Коэффициент третьего уровня всегда должен быть больше входного параметра Коэффициент второго уровня! Исправьте значения этих входных параметров индикатора!')
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
    StringConcatenate(shortname, 'XMA_KLx7_Cloud(', Smooth, ', ', XLength, ', ', KeltnerPeriod, ', ', DoubleToString(Ratio1, 2), ', ', DoubleToString(Ratio2, 2), ', ', DoubleToString(Ratio3, 2), ')')
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
    Keltner1 = 0.0
    Keltner2 = 0.0
    Keltner3 = 0.0
    Keltner = 0.0
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
        ExtLineBuffer0[bar] = xma + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        Keltner = GetKeltner(KeltnerPeriod, bar, high, low)
        Keltner1 = Ratio1 * Keltner
        Keltner2 = Ratio2 * Keltner
        Keltner3 = Ratio3 * Keltner
        line = ExtLineBuffer0[bar]
        DnBuffer2[bar] = line + Keltner1
        UpBuffer1[bar] = DnBuffer2[bar]
        UpBuffer3[bar] = line - Keltner1
        DnBuffer1[bar] = UpBuffer3[bar]
        DnBuffer4[bar] = line + Keltner2
        UpBuffer2[bar] = DnBuffer4[bar]
        UpBuffer5[bar] = line - Keltner2
        DnBuffer3[bar] = UpBuffer5[bar]
        UpBuffer4[bar] = line + Keltner3
        DnBuffer5[bar] = line - Keltner3
    else:
        bar = _range_end(bar, rates_total, 1)
    bar0 = rates_total - 1
    SetRightPrice(0, middle_name, 0, time[bar0], ExtLineBuffer0[bar0], Middle_color, 'Georgia')
    SetRightPrice(0, upper_name1, 0, time[bar0], UpBuffer1[bar0], Upper_color1, 'Georgia')
    SetRightPrice(0, lower_name1, 0, time[bar0], DnBuffer1[bar0], Lower_color1, 'Georgia')
    SetRightPrice(0, upper_name2, 0, time[bar0], UpBuffer2[bar0], Upper_color2, 'Georgia')
    SetRightPrice(0, lower_name2, 0, time[bar0], DnBuffer3[bar0], Lower_color2, 'Georgia')
    SetRightPrice(0, upper_name3, 0, time[bar0], UpBuffer4[bar0], Upper_color3, 'Georgia')
    SetRightPrice(0, lower_name3, 0, time[bar0], DnBuffer5[bar0], Lower_color3, 'Georgia')
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XmaKlx7Cloud(_MQL5Indicator):
    name = 'xma_klx7_cloud'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения
        'XLength': 100,  # Глубина  усреднения
        'XPhase': 15,  # Параметр первого усреднения
        'KeltnerPeriod': 20,  # Период усреднения Кёлтнера
        'Ratio1': 1.0,  # Коэффициент первого уровня
        'Ratio2': 2.0,  # Коэффициент второго уровня
        'Ratio3': 3.0,  # Коэффициент третьего уровня
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
    }

