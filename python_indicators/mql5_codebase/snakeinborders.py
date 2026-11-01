"""SnakeInBorders — converted from MQL5: MQL5 Indicators/SnakeInBorders/SnakeInBorders.mq5

Коридор отфильтрованного рынка, ограниченный двумя бордюрами
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 7}, 'colors': {1: [14822282], 2: [16443110]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Mart', 2: 'Channels'}, 'levels': [], 'description': ['Коридор отфильтрованного рынка, ограниченный двумя бордюрами'], 'name': 'SnakeInBorders', 'source': 'MQL5 Indicators/SnakeInBorders/SnakeInBorders.mq5', 'folder': 'SnakeInBorders', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 3, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'SnakeRange', 'py': 'SnakeRange', 'param': 'SnakeRange', 'type': 'uint', 'default': 2, 'label': "полупериод расчета оси Snake'а Axis", 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр первого усреднения,', 'sinput': False}, {'mql': 'FilterPeriod', 'py': 'FilterPeriod', 'param': 'FilterPeriod', 'type': 'uint', 'default': 24, 'label': 'период фильтрации', 'sinput': False}, {'mql': 'MartFiltr', 'py': 'MartFiltr', 'param': 'MartFiltr', 'type': 'double', 'default': 2.0, 'label': 'коэффициент фильтрации рынка. Чем MartFiltr больше, тем уже коридор отфильтрованного рынка. Данный коэффициент следует подбирать. По умолчанию 2;', 'sinput': False}, {'mql': 'HardCalc', 'py': 'HardCalc', 'param': 'HardCalc', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 7, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}, {'mql': 'Upper_color', 'py': 'Upper_color', 'param': None, 'type': 'color', 'default': 7451452, 'label': '', 'sinput': False}, {'mql': 'Lower_color', 'py': 'Lower_color', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XMA_Method = _input('XMA_Method', MODE_LWMA_)  # метод усреднения
SnakeRange = _input('SnakeRange', 2)  # полупериод расчета оси Snake'а Axis
XPhase = _input('XPhase', 15)  # параметр первого усреднения,
FilterPeriod = _input('FilterPeriod', 24)  # период фильтрации
MartFiltr = _input('MartFiltr', 2.0)
HardCalc = _input('HardCalc', True)
IPC = _input('IPC', PRICE_WEIGHTED_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
Upper_color = _input('Upper_color', clrMediumSeaGreen)
Lower_color = _input('Lower_color', clrRed)
MartBuffer = Arr(0, 0.0)
BorderTopBuffer = Arr(0, 0.0)
BorderBotBuffer = Arr(0, 0.0)
AxisBuffer = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0
min_rates_1 = 0
SnakeRange1 = 0
upper_name = ""
lower_name = ""

def OnInit():
    global SnakeRange1, dPriceShift, lower_name, min_rates_total, upper_name
    SnakeRange1 = _int(SnakeRange) + 1
    min_rates_total = GetStartBars(XMA_Method, SnakeRange1, XPhase) + 1
    XMA1.XMALengthCheck('XLength', SnakeRange1)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    dPriceShift = Point() * PriceShift
    upper_name = 'SnakeInBorders upper text lable'
    lower_name = 'SnakeInBorders lower text lable'
    SetIndexBuffer(0, MartBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, BorderTopBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, BorderBotBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    SetIndexBuffer(3, AxisBuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(MartBuffer, True)
    ArraySetAsSeries(BorderTopBuffer, True)
    ArraySetAsSeries(BorderBotBuffer, True)
    ArraySetAsSeries(AxisBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SnakeInBorders')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnDeinit(reason):
    ObjectDelete(0, upper_name)
    ObjectDelete(0, lower_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    maxbar = rates_total - 1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    for bar in range(limit, 0 - 1, -1):
        price = PriceSeries(IPC, bar, open, high, low, close)
        AxisBuffer[bar] = XMA1.XMASeries(maxbar, prev_calculated, rates_total, XMA_Method, XPhase, SnakeRange1, price, bar, True)
        MainCalculation(bar, open, high, low, close, rates_total)
        BorderTopBuffer[bar] += dPriceShift
        BorderBotBuffer[bar] += dPriceShift
        MartBuffer[bar] += dPriceShift
    bar0 = 0
    SetRightPrice(0, upper_name, 0, time[bar0], BorderTopBuffer[bar0], Upper_color, 'Georgia')
    SetRightPrice(0, lower_name, 0, time[bar0], BorderBotBuffer[bar0], Lower_color, 'Georgia')
    return rates_total

def MainCalculation(Pos, Open, High, Low, Close, Rates_Total):
    MartAxis(Pos, Open, Low, High, Close, Rates_Total)
    if HardCalc == True:
        SmoothOverMart2(Pos, Rates_Total)
    else:
        SmoothOverMart(Pos, Rates_Total)
    return

def MartAxis(Pos, Open, High, Low, Close, Rates_Total):
    SnakeWeight = 0
    i = 0
    w = 0
    ww = 0
    shift = 0
    SnakeSum = 0.0
    shift = _int(MathMin(Pos + SnakeRange + 2, Rates_Total - 1))
    for shift in range(shift, Pos, -1):
        SnakeSum = 0.0
        SnakeWeight = 0
        i = 0
        w = _int(MathMin(shift + SnakeRange, Rates_Total - 1))
        ww = shift - _int(SnakeRange)
        if ww < Pos:
            ww = Pos
        while w >= shift:
            i += 1
            SnakeSum += i * PriceSeries(IPC, w, Open, Low, High, Close)
            SnakeWeight += i
            w -= 1
        while w >= ww:
            i -= 1
            SnakeSum += i * PriceSeries(IPC, w, Open, Low, High, Close)
            SnakeWeight += i
            w -= 1
        if not SnakeWeight:
            SnakeWeight = 1
        AxisBuffer[shift] = _fdiv(SnakeSum, SnakeWeight)
    else:
        shift = _range_end(shift, Pos, -1)
    return

def SmoothOverMart(Pos, Rates_Total):
    shift = 0
    a = 0.0
    t = 0.0
    b = 0.0
    shift = _int(MathMin(Pos + SnakeRange + 2, Rates_Total - 1))
    for shift in range(shift, Pos - 1, -1):
        t = AxisBuffer[ArrayMaximum(AxisBuffer, shift, FilterPeriod)]
        b = AxisBuffer[ArrayMinimum(AxisBuffer, shift, FilterPeriod)]
        a = AxisBuffer[shift]
        BorderTopBuffer[shift] = (((2 * (1 + MartFiltr) * a) + (t - b)) / 2) / (1 + MartFiltr)
        BorderBotBuffer[shift] = (((2 * (1 + MartFiltr) * a) - (t - b)) / 2) / (1 + MartFiltr)
        MartBuffer[shift] = (((2 * (2 + MartFiltr) * a) - (t + b)) / 2) / (1 + MartFiltr)
    else:
        shift = _range_end(shift, Pos - 1, -1)
    return

def SmoothOverMart2(shift, Rates_Total):
    a = 0.0
    t = 0.0
    b = 0.0
    t = AxisBuffer[ArrayMaximum(AxisBuffer, shift, FilterPeriod)]
    b = AxisBuffer[ArrayMinimum(AxisBuffer, shift, FilterPeriod)]
    a = AxisBuffer[shift]
    BorderTopBuffer[shift] = (((2 * (1 + MartFiltr) * a) + (t - b)) / 2) / (1 + MartFiltr)
    BorderBotBuffer[shift] = (((2 * (1 + MartFiltr) * a) - (t - b)) / 2) / (1 + MartFiltr)
    MartBuffer[shift] = (((2 * (2 + MartFiltr) * a) - (t + b)) / 2) / (1 + MartFiltr)
    return

def CreateRightPrice(chart_id, name, nwin, time, price, Color, Font):
    ObjectCreate(chart_id, name, OBJ_ARROW_RIGHT_PRICE, nwin, time, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetString(chart_id, name, OBJPROP_FONT, Font)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

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


class SnakeInBorders(_MQL5Indicator):
    name = 'SnakeInBorders'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # метод усреднения
        'SnakeRange': 2,  # полупериод расчета оси Snake'а Axis
        'XPhase': 15,  # параметр первого усреднения,
        'FilterPeriod': 24,  # период фильтрации
        'MartFiltr': 2.0,  # коэффициент фильтрации рынка. Чем MartFiltr больше, тем уже коридор отфильтрованного рынка. Данный коэффициент следует подбирать. По умолчанию 2;
        'HardCalc': True,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=7),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # cдвиг индикатора по вертикали в пунктах
    }

