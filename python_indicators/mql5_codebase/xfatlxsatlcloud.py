"""XFatlXSatlCloud — converted from MQL5: MQL5 Indicators/XFatlXSatlCloud/XFatlXSatlCloud.mq5

Гистограмма? построенная на разности между сглаженными фильтрами Fatl и Satl
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [10025880, 11823615], 2: [16711680], 3: [255]}, 'widths': {2: 2, 3: 2}, 'styles': {2: 0, 3: 0}, 'labels': {1: 'XFatlXSatlCloud Signal', 2: 'XFatl', 3: 'XSatl'}, 'levels': [], 'description': ['Гистограмма? построенная на разности между сглаженными фильтрами Fatl и Satl'], 'name': 'XFatlXSatlCloud', 'source': 'MQL5 Indicators/XFatlXSatlCloud/XFatlXSatlCloud.mq5', 'folder': 'XFatlXSatlCloud', 'inputs': [{'mql': 'XMA_Method1', 'py': 'XMA_Method1', 'param': 'XMA_Method1', 'type': 'int', 'default': 4, 'label': 'метод усреднения Fatl', 'sinput': False}, {'mql': 'XLength1', 'py': 'XLength1', 'param': 'XLength1', 'type': 'uint', 'default': 3, 'label': 'глубина усреднения Fatl', 'sinput': False}, {'mql': 'XPhase1', 'py': 'XPhase1', 'param': 'XPhase1', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания Fatl,', 'sinput': False}, {'mql': 'XMA_Method2', 'py': 'XMA_Method2', 'param': 'XMA_Method2', 'type': 'int', 'default': 4, 'label': 'метод усреднения Satl', 'sinput': False}, {'mql': 'XLength2', 'py': 'XLength2', 'param': 'XLength2', 'type': 'uint', 'default': 5, 'label': 'глубина усреднения Satl', 'sinput': False}, {'mql': 'XPhase2', 'py': 'XPhase2', 'param': 'XPhase2', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания Satl,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XMA_Method1 = _input('XMA_Method1', MODE_JJMA)  # метод усреднения Fatl
XLength1 = _input('XLength1', 3)  # глубина усреднения Fatl
XPhase1 = _input('XPhase1', 15)  # параметр сглаживания Fatl,
XMA_Method2 = _input('XMA_Method2', MODE_JJMA)  # метод усреднения Satl
XLength2 = _input('XLength2', 5)  # глубина усреднения Satl
XPhase2 = _input('XPhase2', 15)  # параметр сглаживания Satl,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
min_rates_3 = 0
min_rates_4 = 0

def OnInit():
    global min_rates_1, min_rates_2, min_rates_3, min_rates_4, min_rates_total
    min_rates_1 = 39
    min_rates_2 = min_rates_1 + GetStartBars(XMA_Method1, XLength1, XPhase1)
    min_rates_3 = 65
    min_rates_4 = min_rates_3 + GetStartBars(XMA_Method2, XLength2, XPhase2)
    min_rates_total = MathMax(min_rates_2, min_rates_4)
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, UpIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, DnIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'XFatlXSatlCloud')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    fatl = 0.0
    xfatl = 0.0
    satl = 0.0
    xsatl = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        fatl = FTL.FATLSeries(0, prev_calculated, rates_total, price, bar, False)
        xfatl = XMA1.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method1, XPhase1, XLength1, fatl, bar, False)
        satl = STL.SATLSeries(0, prev_calculated, rates_total, price, bar, False)
        xsatl = XMA2.XMASeries(min_rates_2, prev_calculated, rates_total, XMA_Method2, XPhase2, XLength2, satl, bar, False)
        UpBuffer[bar] = xfatl
        UpIndBuffer[bar] = UpBuffer[bar]
        DnBuffer[bar] = xsatl
        DnIndBuffer[bar] = DnBuffer[bar]
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()
FTL = _alloc(CFATL)
FTL.__init__()
STL = _alloc(CSATL)
STL.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XFatlXSatlCloud(_MQL5Indicator):
    name = 'XFatlXSatlCloud'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения Fatl
        'XLength1': 3,  # глубина усреднения Fatl
        'XPhase1': 15,  # параметр сглаживания Fatl,
        'XMA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения Satl
        'XLength2': 5,  # глубина усреднения Satl
        'XPhase2': 15,  # параметр сглаживания Satl,
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
    }

