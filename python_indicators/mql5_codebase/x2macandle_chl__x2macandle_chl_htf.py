"""X2MACandle_Chl — converted from MQL5: MQL5 Indicators/X2MACandle_Chl_HTF/X2MACandle_Chl.mq5

Индикатор X2MA в свечном виде с двумя, заполненными цветным фоном каналами, построенными на среднеквадратичных отклонениях от High и Low индикаторных свеч
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 3}, 'types': {1: 7, 2: 7, 3: 17}, 'colors': {1: [15269855], 2: [16773887], 3: [7697919, 8421504, 14804852]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Upper Signal Cloud', 2: 'Lower Signal Cloud', 3: 'X2MACandle Open;X2MACandle High;X2MACandle Low;X2MACandle Close'}, 'levels': [], 'description': ['Индикатор X2MA в свечном виде с двумя, заполненными цветным фоном каналами, построенными на среднеквадратичных отклонениях от High и Low индикаторных свеч'], 'name': 'X2MACandle_Chl', 'source': 'MQL5 Indicators/X2MACandle_Chl_HTF/X2MACandle_Chl.mq5', 'folder': 'X2MACandle_Chl_HTF', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'метод усреднения первого сглаживания', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'int', 'default': 12, 'label': 'глубина  первого сглаживания', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'параметр первого сглаживания,', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 4, 'label': 'метод усреднения второго сглаживания', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'int', 'default': 5, 'label': 'глубина  второго сглаживания', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 15, 'label': 'параметр второго сглаживания,', 'sinput': False}, {'mql': 'Gap', 'py': 'Gap', 'param': 'Gap', 'type': 'uint', 'default': 10, 'label': 'размер неучитываемого гэпа в пунктах', 'sinput': False}, {'mql': 'BBLength', 'py': 'BBLength', 'param': 'BBLength', 'type': 'uint', 'default': 10, 'label': 'период Боллинджера', 'sinput': False}, {'mql': 'BandsDeviation', 'py': 'BandsDeviation', 'param': 'BandsDeviation', 'type': 'double', 'default': 1.0, 'label': 'девиация', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
MA_Method1 = _input('MA_Method1', MODE_SMA_)  # метод усреднения первого сглаживания
Length1 = _input('Length1', 12)  # глубина  первого сглаживания
Phase1 = _input('Phase1', 15)  # параметр первого сглаживания,
MA_Method2 = _input('MA_Method2', MODE_JJMA)  # метод усреднения второго сглаживания
Length2 = _input('Length2', 5)  # глубина  второго сглаживания
Phase2 = _input('Phase2', 15)  # параметр второго сглаживания,
Gap = _input('Gap', 10)  # размер неучитываемого гэпа в пунктах
BBLength = _input('BBLength', 10)  # период Боллинджера
BandsDeviation = _input('BandsDeviation', 1.0)  # девиация
UpUpBuffer = Arr(0, 0.0)
UpDnBuffer = Arr(0, 0.0)
DnUpBuffer = Arr(0, 0.0)
DnDnBuffer = Arr(0, 0.0)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0

def OnInit():
    global min_rates_1, min_rates_2, min_rates_total
    min_rates_1 = GetStartBars(MA_Method1, Length1, Phase1)
    min_rates_2 = min_rates_1 + GetStartBars(MA_Method2, Length2, Phase2)
    min_rates_total = min_rates_2 + _int(BBLength)
    IndInit(0, UpUpBuffer, INDICATOR_DATA)
    IndInit(1, UpDnBuffer, INDICATOR_DATA)
    PlotInit(0, 0.0, min_rates_total, 0)
    IndInit(2, DnUpBuffer, INDICATOR_DATA)
    IndInit(3, DnDnBuffer, INDICATOR_DATA)
    PlotInit(1, 0.0, min_rates_total, 0)
    SetIndexBuffer(4, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(8, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotInit(2, 0.0, min_rates_1, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = Box("")
    Smooth1 = XMAo1.GetString_MA_Method(MA_Method1)
    Smooth2 = XMAo1.GetString_MA_Method(MA_Method2)
    StringConcatenate(shortname, 'X2MACandle_Chl(', Length1, ', ', Length2, ', ', Smooth1, ', ', Smooth2, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    return INIT_SUCCEEDED

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    O = 0.0
    H = 0.0
    L = 0.0
    C = 0.0
    stdev = 0.0
    first = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    for bar in range(first, rates_total):
        O = XMAo1.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, open[bar], bar, False)
        O = XMAo2.XMASeries(min_rates_1, prev_calculated, rates_total, MA_Method2, Phase2, Length2, O, bar, False)
        H = XMAh1.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, high[bar], bar, False)
        H = XMAh2.XMASeries(min_rates_1, prev_calculated, rates_total, MA_Method2, Phase2, Length2, H, bar, False)
        L = XMAl1.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, low[bar], bar, False)
        L = XMAl2.XMASeries(min_rates_1, prev_calculated, rates_total, MA_Method2, Phase2, Length2, L, bar, False)
        C = XMAc1.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, close[bar], bar, False)
        C = XMAc2.XMASeries(min_rates_1, prev_calculated, rates_total, MA_Method2, Phase2, Length2, C, bar, False)
        Max = MathMax(O, C)
        Max = MathMax(Max, L)
        Max = MathMax(Max, H)
        Min = MathMin(O, C)
        Min = MathMin(Min, L)
        Min = MathMin(Min, H)
        ExtOpenBuffer[bar] = O
        ExtHighBuffer[bar] = Max
        ExtLowBuffer[bar] = Min
        ExtCloseBuffer[bar] = C
        if MathAbs(open[bar] - close[bar]) <= Gap:
            ExtOpenBuffer[bar] = ExtCloseBuffer[MathMax(bar - 1, 0)]
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
        stdev = STDh.StdDevSeries(min_rates_2, prev_calculated, rates_total, BBLength, BandsDeviation, high[bar], ExtHighBuffer[bar], bar, False)
        UpUpBuffer[bar] = ExtHighBuffer[bar] + stdev
        UpDnBuffer[bar] = ExtHighBuffer[bar]
        DnUpBuffer[bar] = ExtLowBuffer[bar]
        stdev = STDl.StdDevSeries(min_rates_2, prev_calculated, rates_total, BBLength, BandsDeviation, low[bar], ExtLowBuffer[bar], bar, False)
        DnDnBuffer[bar] = ExtLowBuffer[bar] - stdev
    return rates_total

# ---- global variables initialised from expressions
XMAo1 = _alloc(CXMA)
XMAo1.__init__()
XMAh1 = _alloc(CXMA)
XMAh1.__init__()
XMAl1 = _alloc(CXMA)
XMAl1.__init__()
XMAc1 = _alloc(CXMA)
XMAc1.__init__()
XMAo2 = _alloc(CXMA)
XMAo2.__init__()
XMAh2 = _alloc(CXMA)
XMAh2.__init__()
XMAl2 = _alloc(CXMA)
XMAl2.__init__()
XMAc2 = _alloc(CXMA)
XMAc2.__init__()
STDh = _alloc(CStdDeviation)
STDh.__init__()
STDl = _alloc(CStdDeviation)
STDl.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class X2MACandleChl(_MQL5Indicator):
    name = 'X2MACandle_Chl'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения первого сглаживания
        'Length1': 12,  # глубина  первого сглаживания
        'Phase1': 15,  # параметр первого сглаживания,
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения второго сглаживания
        'Length2': 5,  # глубина  второго сглаживания
        'Phase2': 15,  # параметр второго сглаживания,
        'Gap': 10,  # размер неучитываемого гэпа в пунктах
        'BBLength': 10,  # период Боллинджера
        'BandsDeviation': 1.0,  # девиация
    }

