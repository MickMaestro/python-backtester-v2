"""blauhlm — converted from MQL5: MQL5 Indicators/BlauHLM_HTF/blauhlm.mq5

HLM Oscillator
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 10}, 'colors': {1: [16711680, 8388736], 2: [9639167, 42495, 8421504, 3329434, 8421376]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'Blau HLM Signal', 2: 'Blau HLM'}, 'levels': [], 'description': ['HLM Oscillator'], 'name': 'blauhlm', 'source': 'MQL5 Indicators/BlauHLM_HTF/blauhlm.mq5', 'folder': 'BlauHLM_HTF', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 1, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 2, 'label': 'Период моментума', 'sinput': False}, {'mql': 'XLength1', 'py': 'XLength1', 'param': 'XLength1', 'type': 'uint', 'default': 20, 'label': 'Глубина первого усреднения', 'sinput': False}, {'mql': 'XLength2', 'py': 'XLength2', 'param': 'XLength2', 'type': 'uint', 'default': 5, 'label': 'Глубина второго усреднения', 'sinput': False}, {'mql': 'XLength3', 'py': 'XLength3', 'param': 'XLength3', 'type': 'uint', 'default': 3, 'label': 'Глубина третьего усреднения', 'sinput': False}, {'mql': 'XLength4', 'py': 'XLength4', 'param': 'XLength4', 'type': 'uint', 'default': 3, 'label': 'Глубина усреднения сигнальной линии', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_EMA)  # Метод усреднения
XLength = _input('XLength', 2)  # Период моментума
XLength1 = _input('XLength1', 20)  # Глубина первого усреднения
XLength2 = _input('XLength2', 5)  # Глубина второго усреднения
XLength3 = _input('XLength3', 3)  # Глубина третьего усреднения
XLength4 = _input('XLength4', 3)  # Глубина усреднения сигнальной линии
XPhase = _input('XPhase', 15)  # Параметр сглаживания
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
min_rates_3 = 0
min_rates_4 = 0

def OnInit():
    global min_rates_1, min_rates_2, min_rates_3, min_rates_4, min_rates_total
    min_rates_1 = _int(XLength)
    min_rates_2 = min_rates_1 + XMA1.GetStartBars(XMA_Method, XLength1, XPhase)
    min_rates_3 = min_rates_2 + XMA1.GetStartBars(XMA_Method, XLength2, XPhase)
    min_rates_4 = min_rates_3 + XMA1.GetStartBars(XMA_Method, XLength3, XPhase)
    min_rates_total = min_rates_4 + XMA1.GetStartBars(XMA_Method, XLength4, XPhase)
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BlauHLM')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    hmu = 0.0
    lmd = 0.0
    hlm = 0.0
    xhlm = 0.0
    xxhlm = 0.0
    xxxhlm = 0.0
    sign = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        hmu = high[bar] - high[bar - (XLength - 1)]
        lmd = -(low[bar] - low[bar - (XLength - 1)])
        hmu = (hmu if (hmu > 0) else 0)
        lmd = (lmd if (lmd > 0) else 0)
        hlm = hmu - lmd
        hlm = _fdiv(hlm, Point())
        xhlm = XMA1.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XPhase, XLength1, hlm, bar, False)
        xxhlm = XMA2.XMASeries(min_rates_2, prev_calculated, rates_total, XMA_Method, XPhase, XLength2, xhlm, bar, False)
        xxxhlm = XMA3.XMASeries(min_rates_3, prev_calculated, rates_total, XMA_Method, XPhase, XLength3, xxhlm, bar, False)
        sign = XMA4.XMASeries(min_rates_4, prev_calculated, rates_total, XMA_Method, XPhase, XLength4, xxxhlm, bar, False)
        IndBuffer[bar] = xxxhlm
        UpBuffer[bar] = xxxhlm
        DnBuffer[bar] = sign
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        clr = 2
        if IndBuffer[bar] > 0:
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                clr = 4
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                clr = 3
        if IndBuffer[bar] < 0:
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                clr = 0
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                clr = 1
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()
XMA3 = _alloc(CXMA)
XMA3.__init__()
XMA4 = _alloc(CXMA)
XMA4.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Blauhlm(_MQL5Indicator):
    name = 'blauhlm'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Метод усреднения
        'XLength': 2,  # Период моментума
        'XLength1': 20,  # Глубина первого усреднения
        'XLength2': 5,  # Глубина второго усреднения
        'XLength3': 3,  # Глубина третьего усреднения
        'XLength4': 3,  # Глубина усреднения сигнальной линии
        'XPhase': 15,  # Параметр сглаживания
    }

