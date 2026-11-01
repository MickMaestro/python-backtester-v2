"""XWAMI — converted from MQL5: MQL5 Indicators/XWAMI/XWAMI.mq5

Momentum Indicator by Anthony W.Warren
Этот индикатор Моментума был описан в статье «Оптимизация импульса» Энтони У. Уоррена в журнале S & C в апреле 1994 г.
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [14822282, 36095]}, 'widths': {}, 'styles': {}, 'labels': {1: 'XWAMI'}, 'levels': [], 'description': ['Momentum Indicator by Anthony W.Warren', 'Этот индикатор Моментума был описан в статье «Оптимизация импульса» Энтони У. Уоррена в журнале S & C в апреле 1994 г.'], 'name': 'XWAMI', 'source': 'MQL5 Indicators/XWAMI/XWAMI.mq5', 'folder': 'XWAMI', 'inputs': [{'mql': 'iPeriod', 'py': 'iPeriod', 'param': 'iPeriod', 'type': 'uint', 'default': 1, 'label': 'период моментума', 'sinput': False}, {'mql': 'XMethod1', 'py': 'XMethod1', 'param': 'XMethod1', 'type': 'int', 'default': 7, 'label': 'метод усреднения 1', 'sinput': False}, {'mql': 'XLength1', 'py': 'XLength1', 'param': 'XLength1', 'type': 'uint', 'default': 4, 'label': 'глубина усреднения 1', 'sinput': False}, {'mql': 'XPhase1', 'py': 'XPhase1', 'param': 'XPhase1', 'type': 'int', 'default': 15, 'label': 'параметр усреднения 1,', 'sinput': False}, {'mql': 'XMethod2', 'py': 'XMethod2', 'param': 'XMethod2', 'type': 'int', 'default': 4, 'label': 'метод усреднения 2', 'sinput': False}, {'mql': 'XLength2', 'py': 'XLength2', 'param': 'XLength2', 'type': 'uint', 'default': 13, 'label': 'глубина усреднения 2', 'sinput': False}, {'mql': 'XPhase2', 'py': 'XPhase2', 'param': 'XPhase2', 'type': 'int', 'default': 15, 'label': 'параметр усреднения 2,', 'sinput': False}, {'mql': 'XMethod3', 'py': 'XMethod3', 'param': 'XMethod3', 'type': 'int', 'default': 4, 'label': 'метод усреднения 3', 'sinput': False}, {'mql': 'XLength3', 'py': 'XLength3', 'param': 'XLength3', 'type': 'uint', 'default': 13, 'label': 'глубина усреднения 3', 'sinput': False}, {'mql': 'XPhase3', 'py': 'XPhase3', 'param': 'XPhase3', 'type': 'int', 'default': 15, 'label': 'параметр усреднения 3,', 'sinput': False}, {'mql': 'XMethod4', 'py': 'XMethod4', 'param': 'XMethod4', 'type': 'int', 'default': 4, 'label': 'метод усреднения сигнальной линии', 'sinput': False}, {'mql': 'XLength4', 'py': 'XLength4', 'param': 'XLength4', 'type': 'uint', 'default': 4, 'label': 'глубина усреднения сигнальной линии', 'sinput': False}, {'mql': 'XPhase4', 'py': 'XPhase4', 'param': 'XPhase4', 'type': 'int', 'default': 15, 'label': 'параметр усреднения сигнальной линии,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
iPeriod = _input('iPeriod', 1)  # период моментума
XMethod1 = _input('XMethod1', MODE_T3)  # метод усреднения 1
XLength1 = _input('XLength1', 4)  # глубина усреднения 1
XPhase1 = _input('XPhase1', 15)  # параметр усреднения 1,
XMethod2 = _input('XMethod2', MODE_JJMA)  # метод усреднения 2
XLength2 = _input('XLength2', 13)  # глубина усреднения 2
XPhase2 = _input('XPhase2', 15)  # параметр усреднения 2,
XMethod3 = _input('XMethod3', MODE_JJMA)  # метод усреднения 3
XLength3 = _input('XLength3', 13)  # глубина усреднения 3
XPhase3 = _input('XPhase3', 15)  # параметр усреднения 3,
XMethod4 = _input('XMethod4', MODE_JJMA)  # метод усреднения сигнальной линии
XLength4 = _input('XLength4', 4)  # глубина усреднения сигнальной линии
XPhase4 = _input('XPhase4', 15)  # параметр усреднения сигнальной линии,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
min_rates_3 = 0
min_rates_4 = 0

def OnInit():
    global min_rates_1, min_rates_2, min_rates_3, min_rates_4, min_rates_total
    min_rates_1 = _int(iPeriod)
    min_rates_2 = min_rates_1 + GetStartBars(XMethod1, XLength1, XPhase1)
    min_rates_3 = min_rates_2 + GetStartBars(XMethod2, XLength2, XPhase2)
    min_rates_4 = min_rates_3 + GetStartBars(XMethod3, XLength3, XPhase3)
    min_rates_total = min_rates_4 + GetStartBars(XMethod4, XLength4, XPhase4)
    SetIndexBuffer(0, UpIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    SetIndexBuffer(1, DnIndBuffer, INDICATOR_DATA)
    shortname = Box("")
    StringConcatenate(shortname, 'XWAMI(', XLength1, ', ', XLength2, ', ', XLength3, ', ', XLength4, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_1
    else:
        first = prev_calculated - 1
    for bar in range(first, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        price_prev = PriceSeries(IPC, bar - iPeriod, open, low, high, close)
        diff = price - price_prev
        xdiff = XMA1.XMASeries(min_rates_1, prev_calculated, rates_total, XMethod1, XPhase1, XLength1, diff, bar, False)
        xxdiff = XMA2.XMASeries(min_rates_2, prev_calculated, rates_total, XMethod2, XPhase2, XLength2, xdiff, bar, False)
        xxxdiff = XMA3.XMASeries(min_rates_3, prev_calculated, rates_total, XMethod3, XPhase3, XLength3, xxdiff, bar, False)
        xxxxdiff = XMA4.XMASeries(min_rates_4, prev_calculated, rates_total, XMethod4, XPhase4, XLength4, xxxdiff, bar, False)
        UpIndBuffer[bar] = _fdiv(xxxdiff, Point())
        DnIndBuffer[bar] = _fdiv(xxxxdiff, Point())
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


class XWAMI(_MQL5Indicator):
    name = 'XWAMI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iPeriod': 1,  # период моментума
        'XMethod1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # метод усреднения 1
        'XLength1': 4,  # глубина усреднения 1
        'XPhase1': 15,  # параметр усреднения 1,
        'XMethod2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения 2
        'XLength2': 13,  # глубина усреднения 2
        'XPhase2': 15,  # параметр усреднения 2,
        'XMethod3': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения 3
        'XLength3': 13,  # глубина усреднения 3
        'XPhase3': 15,  # параметр усреднения 3,
        'XMethod4': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения сигнальной линии
        'XLength4': 4,  # глубина усреднения сигнальной линии
        'XPhase4': 15,  # параметр усреднения сигнальной линии,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

