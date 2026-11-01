"""i-CAiChannel — converted from MQL5: MQL5 Indicators/i-CAiChannel/i-CAiChannel.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [16443110], 2: [16748574], 3: [42495]}, 'widths': {2: 2, 3: 2}, 'styles': {2: 0, 3: 0}, 'labels': {1: 'i-CAiChannel Cloud', 2: 'Upper i-CAiChannel', 3: 'Lower i-CAiChannel'}, 'levels': [], 'description': [], 'name': 'i-CAiChannel', 'source': 'MQL5 Indicators/i-CAiChannel/i-CAiChannel.mq5', 'folder': 'i-CAiChannel', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 12, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Dev', 'py': 'Dev', 'param': 'Dev', 'type': 'uint', 'default': 1000, 'label': 'половина ширины канала в пунктах', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XMA_Method = _input('XMA_Method', MODE_SMA_)  # метод усреднения
XLength = _input('XLength', 12)  # глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр сглаживания,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Dev = _input('Dev', 1000)  # половина ширины канала в пунктах
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
ExtUp1Buffer = Arr(0, 0.0)
ExtUp2Buffer = Arr(0, 0.0)
ExtDn1Buffer = Arr(0, 0.0)
ExtDn2Buffer = Arr(0, 0.0)
dDev = 0.0
min_rates_total = 0

def OnInit():
    global dDev, min_rates_total
    min_rates_total = GetStartBars(XMA_Method, XLength, XPhase)
    dDev = Dev * Point()
    SetIndexBuffer(0, ExtUp1Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtDn1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    SetIndexBuffer(2, ExtUp2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    SetIndexBuffer(3, ExtDn2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'i-CAiChannel(', XLength, ', ', Smooth1, ', ', Dev, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_line_prev
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    xma = 0.0
    stdev = 0.0
    powstdev = 0.0
    powdxma = 0.0
    koeff = 0.0
    line = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        xma = XMA1.XMASeries(1, prev_calculated, rates_total, XMA_Method, XPhase, XLength, price, bar, False)
        stdev = STD.StdDevSeries(1, prev_calculated, rates_total, XLength, 1.0, price, xma, bar, False)
        powstdev = MathPow(stdev, 2)
        if bar <= min_rates_total:
            _s_OnCalculate_line_prev = xma
        powdxma = MathPow(_s_OnCalculate_line_prev - xma, 2)
        if powdxma < powstdev or (not powdxma):
            koeff = 0.0
        else:
            koeff = 1.0 - _fdiv(powstdev, powdxma)
        line = _s_OnCalculate_line_prev + (koeff * (xma - _s_OnCalculate_line_prev))
        ExtUp2Buffer[bar] = line + dDev
        ExtUp1Buffer[bar] = ExtUp2Buffer[bar]
        ExtDn2Buffer[bar] = line - dDev
        ExtDn1Buffer[bar] = ExtDn2Buffer[bar]
        if bar < (rates_total - 1):
            _s_OnCalculate_line_prev = line
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
STD = _alloc(CStdDeviation)
STD.__init__()

# ---- static local variables
_s_OnCalculate_line_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ICAiChannel(_MQL5Indicator):
    name = 'i-CAiChannel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения
        'XLength': 12,  # глубина сглаживания
        'XPhase': 15,  # параметр сглаживания,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Dev': 1000,  # половина ширины канала в пунктах
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

