"""vinini_bb — converted from MQL5: MQL5 Indicators/VininI_BB_HTF/vinini_bb.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [2330219], 2: [8421504], 3: [9662683]}, 'widths': {1: 3, 2: 3, 3: 3}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Upper VininI_BB', 2: 'Middle VininI_BB', 3: 'Lower VininI_BB'}, 'levels': [], 'description': [], 'name': 'vinini_bb', 'source': 'MQL5 Indicators/VininI_BB_HTF/vinini_bb.mq5', 'folder': 'VininI_BB_HTF', 'inputs': [{'mql': 'JMethod', 'py': 'JMethod', 'param': 'JMethod', 'type': 'int', 'default': 0, 'label': 'Метод первого усреднения', 'sinput': False}, {'mql': 'JLength', 'py': 'JLength', 'param': 'JLength', 'type': 'uint', 'default': 100, 'label': 'Глубина  первого сглаживания', 'sinput': False}, {'mql': 'JPhase', 'py': 'JPhase', 'param': 'JPhase', 'type': 'int', 'default': 15, 'label': 'Параметр первого среднения', 'sinput': False}, {'mql': 'BandsDeviation', 'py': 'BandsDeviation', 'param': 'BandsDeviation', 'type': 'double', 'default': 1.0, 'label': 'Девиация', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
JMethod = _input('JMethod', MODE_SMA)  # Метод первого усреднения
JLength = _input('JLength', 100)  # Глубина  первого сглаживания
JPhase = _input('JPhase', 15)  # Параметр первого среднения
BandsDeviation = _input('BandsDeviation', 1.0)  # Девиация
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
UpperBuffer = Arr(0, 0.0)
MiddleBuffer = Arr(0, 0.0)
lowerBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(JLength) + 1
    SetIndexBuffer(0, UpperBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, MiddleBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, lowerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'VininI_BB(JLength=', JLength, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    xma = 0.0
    stdev = 0.0
    first = 0
    bar = 0
    if prev_calculated == 0:
        first = 1
        UpperBuffer[first - 1] = 0.0
        lowerBuffer[first - 1] = 99999999.99999999
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        UpperBuffer[bar] = EMPTY_VALUE
        lowerBuffer[bar] = EMPTY_VALUE
        MiddleBuffer[bar] = EMPTY_VALUE
        price = PriceSeries(IPC, bar, open, low, high, close)
        xma = XMA1.XMASeries(1, prev_calculated, rates_total, JMethod, JPhase, JLength, price, bar, False)
        stdev = STD.StdDevSeries(1, prev_calculated, rates_total, JLength, BandsDeviation, price, xma, bar, False)
        stdev *= BandsDeviation
        UpperBuffer[bar] = UpperBuffer[bar - 1]
        lowerBuffer[bar] = lowerBuffer[bar - 1]
        if high[bar] > UpperBuffer[bar]:
            UpperBuffer[bar] = high[bar]
            lowerBuffer[bar] = high[bar] - (2.0 * stdev)
            if lowerBuffer[bar] < lowerBuffer[bar - 1]:
                lowerBuffer[bar] = lowerBuffer[bar - 1]
        if low[bar] < lowerBuffer[bar]:
            lowerBuffer[bar] = low[bar]
            UpperBuffer[bar] = low[bar] + (2.0 * stdev)
            if UpperBuffer[bar] > UpperBuffer[bar - 1]:
                UpperBuffer[bar] = UpperBuffer[bar - 1]
        MiddleBuffer[bar] = (UpperBuffer[bar] + lowerBuffer[bar]) * 0.5
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
STD = _alloc(CStdDeviation)
STD.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VininiBb(_MQL5Indicator):
    name = 'vinini_bb'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'JMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод первого усреднения
        'JLength': 100,  # Глубина  первого сглаживания
        'JPhase': 15,  # Параметр первого среднения
        'BandsDeviation': 1.0,  # Девиация
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

