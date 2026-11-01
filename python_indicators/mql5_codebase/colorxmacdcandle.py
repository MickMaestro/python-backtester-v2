"""ColorXMACDCandle — converted from MQL5: MQL5 Indicators/ColorXMACDCandle/ColorXMACDCandle.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 2}, 'types': {1: 17, 2: 8}, 'colors': {1: [16711935, 8421504, 16711680], 2: [8421504, 65280, 255]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'MACDCandle Open;MACDCandle High;MACDCandle Low;MACDCandle Close', 2: 'Signal Line'}, 'levels': [], 'description': [], 'name': 'ColorXMACDCandle', 'source': 'MQL5 Indicators/ColorXMACDCandle/ColorXMACDCandle.mq5', 'folder': 'ColorXMACDCandle', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 7, 'label': 'метод усреднения гистограммы', 'sinput': False}, {'mql': 'Fast_XMA', 'py': 'Fast_XMA', 'param': 'Fast_XMA', 'type': 'int', 'default': 12, 'label': 'период быстрого мувинга', 'sinput': False}, {'mql': 'Slow_XMA', 'py': 'Slow_XMA', 'param': 'Slow_XMA', 'type': 'int', 'default': 26, 'label': 'период медленного мувинга', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 100, 'label': 'параметр усреднения мувингов,', 'sinput': False}, {'mql': 'Signal_Method', 'py': 'Signal_Method', 'param': 'Signal_Method', 'type': 'int', 'default': 4, 'label': 'метод усреднения сигнальной линии', 'sinput': False}, {'mql': 'Signal_XMA', 'py': 'Signal_XMA', 'param': 'Signal_XMA', 'type': 'int', 'default': 9, 'label': 'период сигнальной линии', 'sinput': False}, {'mql': 'Signal_Phase', 'py': 'Signal_Phase', 'param': 'Signal_Phase', 'type': 'int', 'default': 100, 'label': 'параметр сигнальной линии,', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'ценовая константа сигнальной линии', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_'})

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_T3)  # метод усреднения гистограммы
Fast_XMA = _input('Fast_XMA', 12)  # период быстрого мувинга
Slow_XMA = _input('Slow_XMA', 26)  # период медленного мувинга
XPhase = _input('XPhase', 100)  # параметр усреднения мувингов,
Signal_Method = _input('Signal_Method', MODE_JJMA)  # метод усреднения сигнальной линии
Signal_XMA = _input('Signal_XMA', 9)  # период сигнальной линии
Signal_Phase = _input('Signal_Phase', 100)  # параметр сигнальной линии,
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE_)  # ценовая константа сигнальной линии
min_rates_total = 0
min_rates_1 = 0
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
SignBuffer = Arr(0, 0.0)
ColorSignBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_1, min_rates_total
    min_rates_1 = MathMax(GetStartBars(XMA_Method, Fast_XMA, XPhase), GetStartBars(XMA_Method, Slow_XMA, XPhase))
    min_rates_total = min_rates_1 + GetStartBars(Signal_Method, Signal_XMA, Signal_Phase) + 2
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, SignBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, ColorSignBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    XMA1.XMALengthCheck('Fast_XMA', Fast_XMA)
    XMA1.XMALengthCheck('Slow_XMA', Slow_XMA)
    XMA1.XMALengthCheck('Signal_XMA', Signal_XMA)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    XMA1.XMAPhaseCheck('Signal_Phase', Signal_Phase, Signal_Method)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(XMA_Method)
    Smooth2 = XMA1.GetString_MA_Method(Signal_Method)
    StringConcatenate(shortname, 'XMACD( ', Fast_XMA, ', ', Slow_XMA, ', ', Signal_XMA, ', ', Smooth1, ', ', Smooth2, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first1 = 0
    first2 = 0
    bar = 0
    fast_xma = 0.0
    slow_xma = 0.0
    sign_xma = 0.0
    oxmacd = 0.0
    cxmacd = 0.0
    hxmacd = 0.0
    lxmacd = 0.0
    Max = 0.0
    Min = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first1 = 0
        first2 = min_rates_total + 1
    else:
        first1 = prev_calculated - 1
        first2 = first1
    bar = first1
    for bar in range(bar, rates_total):
        fast_xma = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Fast_XMA, open[bar], bar, False)
        slow_xma = XMA2.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Slow_XMA, open[bar], bar, False)
        oxmacd = _fdiv(fast_xma - slow_xma, Point())
        fast_xma = XMA3.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Fast_XMA, close[bar], bar, False)
        slow_xma = XMA4.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Slow_XMA, close[bar], bar, False)
        cxmacd = _fdiv(fast_xma - slow_xma, Point())
        fast_xma = XMA5.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Fast_XMA, high[bar], bar, False)
        slow_xma = XMA6.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Slow_XMA, high[bar], bar, False)
        hxmacd = _fdiv(fast_xma - slow_xma, Point())
        fast_xma = XMA7.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Fast_XMA, low[bar], bar, False)
        slow_xma = XMA8.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Slow_XMA, low[bar], bar, False)
        lxmacd = _fdiv(fast_xma - slow_xma, Point())
        Max = MathMax(oxmacd, cxmacd)
        Min = MathMin(oxmacd, cxmacd)
        ExtCloseBuffer[bar] = cxmacd
        ExtOpenBuffer[bar] = oxmacd
        ExtHighBuffer[bar] = MathMax(Max, hxmacd)
        ExtLowBuffer[bar] = MathMin(Min, lxmacd)
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
        _sw1 = AppliedPrice
        if _sw1 == PRICE_OPEN_:
            sign_xma = XMA9.XMASeries(min_rates_1, prev_calculated, rates_total, Signal_Method, Signal_Phase, Signal_XMA, oxmacd, bar, False)
        elif _sw1 == PRICE_CLOSE_:
            sign_xma = XMA9.XMASeries(min_rates_1, prev_calculated, rates_total, Signal_Method, Signal_Phase, Signal_XMA, cxmacd, bar, False)
        elif _sw1 == PRICE_HIGH_:
            sign_xma = XMA9.XMASeries(min_rates_1, prev_calculated, rates_total, Signal_Method, Signal_Phase, Signal_XMA, hxmacd, bar, False)
        elif _sw1 == PRICE_LOW_:
            sign_xma = XMA9.XMASeries(min_rates_1, prev_calculated, rates_total, Signal_Method, Signal_Phase, Signal_XMA, lxmacd, bar, False)
        SignBuffer[bar] = sign_xma
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first2
    for bar in range(bar, rates_total):
        ColorSignBuffer[bar] = 0.0
        if SignBuffer[bar] > SignBuffer[bar - 1]:
            ColorSignBuffer[bar] = 1.0
        if SignBuffer[bar] < SignBuffer[bar - 1]:
            ColorSignBuffer[bar] = 2.0
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
XMA5 = _alloc(CXMA)
XMA5.__init__()
XMA6 = _alloc(CXMA)
XMA6.__init__()
XMA7 = _alloc(CXMA)
XMA7.__init__()
XMA8 = _alloc(CXMA)
XMA8.__init__()
XMA9 = _alloc(CXMA)
XMA9.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorXMACDCandle(_MQL5Indicator):
    name = 'ColorXMACDCandle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # метод усреднения гистограммы
        'Fast_XMA': 12,  # период быстрого мувинга
        'Slow_XMA': 26,  # период медленного мувинга
        'XPhase': 100,  # параметр усреднения мувингов,
        'Signal_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения сигнальной линии
        'Signal_XMA': 9,  # период сигнальной линии
        'Signal_Phase': 100,  # параметр сигнальной линии,
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low'}, default=1),  # ценовая константа сигнальной линии
    }

