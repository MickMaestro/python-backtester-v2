"""X2MACandle — converted from MQL5: MQL5 Indicators/X2MACandle/X2MACandle.mq5

Индикатор X2MA в свечном виде
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [255, 8421504, 11186720]}, 'widths': {}, 'styles': {}, 'labels': {1: 'X2MACandle Open;X2MACandle High;X2MACandle Low;X2MACandle Close'}, 'levels': [], 'description': ['Индикатор X2MA в свечном виде'], 'name': 'X2MACandle', 'source': 'MQL5 Indicators/X2MACandle/X2MACandle.mq5', 'folder': 'X2MACandle', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'метод усреднения первого сглаживания', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'int', 'default': 12, 'label': 'глубина  первого сглаживания', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'параметр первого сглаживания,', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 4, 'label': 'метод усреднения второго сглаживания', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'int', 'default': 5, 'label': 'глубина  второго сглаживания', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 15, 'label': 'параметр второго сглаживания,', 'sinput': False}, {'mql': 'Gap', 'py': 'Gap', 'param': 'Gap', 'type': 'uint', 'default': 10, 'label': 'размер неучитываемого гэпа в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
MA_Method1 = _input('MA_Method1', MODE_SMA_)  # метод усреднения первого сглаживания
Length1 = _input('Length1', 12)  # глубина  первого сглаживания
Phase1 = _input('Phase1', 15)  # параметр первого сглаживания,
MA_Method2 = _input('MA_Method2', MODE_JJMA)  # метод усреднения второго сглаживания
Length2 = _input('Length2', 5)  # глубина  второго сглаживания
Phase2 = _input('Phase2', 15)  # параметр второго сглаживания,
Gap = _input('Gap', 10)  # размер неучитываемого гэпа в пунктах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_ = 0

def OnInit():
    global min_rates_1, min_rates_total
    min_rates_1 = GetStartBars(MA_Method1, Length1, Phase1)
    min_rates_total = min_rates_1 + GetStartBars(MA_Method2, Length2, Phase2)
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = Box("")
    Smooth1 = XMAo1.GetString_MA_Method(MA_Method1)
    Smooth2 = XMAo1.GetString_MA_Method(MA_Method2)
    StringConcatenate(shortname, 'X2MACandle(', Length1, ', ', Length2, ', ', Smooth1, ', ', Smooth2, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    O = 0.0
    H = 0.0
    L = 0.0
    C = 0.0
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
        if bar < min_rates_total:
            continue
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
            ExtOpenBuffer[bar] = ExtCloseBuffer[bar - 1]
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class X2MACandle(_MQL5Indicator):
    name = 'X2MACandle'
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
    }

