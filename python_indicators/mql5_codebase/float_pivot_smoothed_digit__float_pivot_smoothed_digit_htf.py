"""Float_Pivot_Smoothed_Digit — converted from MQL5: MQL5 Indicators/Float_Pivot_Smoothed_Digit_HTF/Float_Pivot_Smoothed_Digit.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 5}, 'types': {1: 7, 2: 1, 3: 1, 4: 1, 5: 7}, 'colors': {1: [15859441], 2: [16748574], 3: [13458026], 4: [9639167], 5: [16641789]}, 'widths': {2: 2, 3: 2, 4: 2}, 'styles': {2: 0, 3: 0, 4: 0}, 'labels': {1: 'Upper Cloud', 2: 'Upper FloatPivot', 3: 'Middle FloatPivot', 4: 'Lower FloatPivot', 5: 'Lower Cloud'}, 'levels': [], 'description': [], 'name': 'Float_Pivot_Smoothed_Digit', 'source': 'MQL5 Indicators/Float_Pivot_Smoothed_Digit_HTF/Float_Pivot_Smoothed_Digit.mq5', 'folder': 'Float_Pivot_Smoothed_Digit_HTF', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'Float_Pivot_Digit', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'IPeriod', 'py': 'IPeriod', 'param': 'IPeriod', 'type': 'int', 'default': 100, 'label': 'Период поиска экстремумов', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 5, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'HMA_Method', 'py': 'HMA_Method', 'param': 'HMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод сглаживания', 'sinput': False}, {'mql': 'HLength', 'py': 'HLength', 'param': 'HLength', 'type': 'uint', 'default': 12, 'label': 'Глубина  сглаживания', 'sinput': False}, {'mql': 'HPhase', 'py': 'HPhase', 'param': 'HPhase', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Digit', 'py': 'Digit', 'param': 'Digit', 'type': 'uint', 'default': 2, 'label': 'количество разрядов округления', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': 'показывать ценовые метки', 'sinput': False}, {'mql': 'Upper_color', 'py': 'Upper_color', 'param': None, 'type': 'color', 'default': 8421376, 'label': 'Цвет верхней ценовой метки', 'sinput': False}, {'mql': 'Middle_color', 'py': 'Middle_color', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Цвет средней ценовой метки', 'sinput': False}, {'mql': 'Lower_color', 'py': 'Lower_color', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Цвет нижней ценовой метки', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum ENUM_APPLIED_PRICE_
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
_enum('ENUM_APPLIED_PRICE_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
SirName = _input('SirName', 'Float_Pivot_Digit')  # Первая часть имени графических объектов
IPeriod = _input('IPeriod', 100)  # Период поиска экстремумов
IPC = _input('IPC', PRICE_MEDIAN_)  # ценовая константа
HMA_Method = _input('HMA_Method', MODE_SMA_)  # Метод сглаживания
HLength = _input('HLength', 12)  # Глубина  сглаживания
HPhase = _input('HPhase', 100)  # Параметр сглаживания,
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
Digit = _input('Digit', 2)  # количество разрядов округления
ShowPrice = _input('ShowPrice', True)  # показывать ценовые метки
Upper_color = _input('Upper_color', clrTeal)  # Цвет верхней ценовой метки
Middle_color = _input('Middle_color', clrBlue)  # Цвет средней ценовой метки
Lower_color = _input('Lower_color', clrMagenta)  # Цвет нижней ценовой метки
ExtUp1Buffer = Arr(0, 0.0)
ExtUp2Buffer = Arr(0, 0.0)
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
ExtCBuffer = Arr(0, 0.0)
ExtDn1Buffer = Arr(0, 0.0)
ExtDn2Buffer = Arr(0, 0.0)
min_rates_total = 0
upper_name = ""
middle_name = ""
lower_name = ""
PointPow10 = 0.0
Count = Arr(0, 0)
XHigh = Arr(0, 0.0)
XLow = Arr(0, 0.0)

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
    global PointPow10, lower_name, middle_name, min_rates_total, upper_name
    min_rates_total = GetStartBars(HMA_Method, HLength, HPhase) + 1
    min_rates_total += MathMax(3, IPeriod)
    upper_name = SirName + ' upper text lable'
    middle_name = SirName + ' middle text lable'
    lower_name = SirName + ' lower text lable'
    PointPow10 = Point() * MathPow(10, Digit)
    ArrayResize(Count, IPeriod)
    ArrayResize(XHigh, IPeriod)
    ArrayResize(XLow, IPeriod)
    ArraySetAsSeries(Count, True)
    ArraySetAsSeries(XHigh, True)
    ArraySetAsSeries(XLow, True)
    SetIndexBuffer(0, ExtUp1Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtUp2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    SetIndexBuffer(2, ExtABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    SetIndexBuffer(3, ExtBBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    SetIndexBuffer(4, ExtCBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    SetIndexBuffer(5, ExtDn1Buffer, INDICATOR_DATA)
    SetIndexBuffer(6, ExtDn2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'Float_Pivot_Smoothed_Digit(', IPeriod, ',', HLength, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnDeinit(reason):
    ObjectDelete(0, upper_name)
    ObjectDelete(0, middle_name)
    ObjectDelete(0, lower_name)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    if prev_calculated == 0:
        first = 0
        ArrayInitialize(Count, None)
        ArrayInitialize(XHigh, None)
        ArrayInitialize(XLow, None)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        pivot = XMAP.XMASeries(0, prev_calculated, rates_total, HMA_Method, HPhase, HLength, PriceSeries(IPC, bar, open, low, high, close), bar, False)
        XHigh[Count[0]] = XMAH.XMASeries(0, prev_calculated, rates_total, HMA_Method, HPhase, HLength, high[bar], bar, False)
        XLow[Count[0]] = XMAL.XMASeries(0, prev_calculated, rates_total, HMA_Method, HPhase, HLength, low[bar], bar, False)
        max_ = XHigh[ArrayMaximum(XHigh, 0, IPeriod)]
        min_ = XLow[ArrayMinimum(XLow, 0, IPeriod)]
        res = (max_ + min_ + pivot) / 3
        ExtUp1Buffer[bar] = PointPow10 * MathCeil(_fdiv(((2 * res) - min_ + res) / 2, PointPow10))
        ExtABuffer[bar] = ExtUp1Buffer[bar]
        ExtDn2Buffer[bar] = PointPow10 * MathFloor(_fdiv((res + ((2 * res) - max_)) / 2, PointPow10))
        ExtCBuffer[bar] = ExtDn2Buffer[bar]
        ExtDn1Buffer[bar] = PointPow10 * MathRound(_fdiv(res, PointPow10))
        ExtUp2Buffer[bar] = ExtDn1Buffer[bar]
        ExtBBuffer[bar] = ExtUp2Buffer[bar]
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count, IPeriod)
    else:
        bar = _range_end(bar, rates_total, 1)
    if ShowPrice:
        bar0 = rates_total - Shift - 1
        time0 = time[bar0]
        SetRightPrice(0, upper_name, 0, time0, ExtABuffer[bar0], Upper_color)
        SetRightPrice(0, middle_name, 0, time0, ExtBBuffer[bar0], Middle_color)
        SetRightPrice(0, lower_name, 0, time0, ExtCBuffer[bar0], Lower_color)
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
XMAL = _alloc(CXMA)
XMAL.__init__()
XMAH = _alloc(CXMA)
XMAH.__init__()
XMAP = _alloc(CXMA)
XMAP.__init__()

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FloatPivotSmoothedDigit(_MQL5Indicator):
    name = 'Float_Pivot_Smoothed_Digit'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'IPeriod': 100,  # Период поиска экстремумов
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW0_2', 12: 'Demark Price'}, default=5),  # ценовая константа
        'HMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод сглаживания
        'HLength': 12,  # Глубина  сглаживания
        'HPhase': 100,  # Параметр сглаживания,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'Digit': 2,  # количество разрядов округления
        'ShowPrice': True,  # показывать ценовые метки
    }

