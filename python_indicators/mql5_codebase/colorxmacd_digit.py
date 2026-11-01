"""ColorXMACD_Digit — converted from MQL5: MQL5 Indicators/ColorXMACD_Digit/ColorXMACD_Digit.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 10, 2: 8}, 'colors': {1: [8421376, 14822282, 8421504, 6053069, 16711935], 2: [65280, 15624315, 255]}, 'widths': {1: 2, 2: 3}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'XMACD', 2: 'Signal Line'}, 'levels': [], 'description': [], 'name': 'ColorXMACD_Digit', 'source': 'MQL5 Indicators/ColorXMACD_Digit/ColorXMACD_Digit.mq5', 'folder': 'ColorXMACD_Digit', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 7, 'label': 'метод усреднения гистограммы', 'sinput': False}, {'mql': 'Fast_XMA', 'py': 'Fast_XMA', 'param': 'Fast_XMA', 'type': 'int', 'default': 12, 'label': 'период быстрого мувинга', 'sinput': False}, {'mql': 'Slow_XMA', 'py': 'Slow_XMA', 'param': 'Slow_XMA', 'type': 'int', 'default': 26, 'label': 'период медленного мувинга', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 100, 'label': 'параметр усреднения мувингов,', 'sinput': False}, {'mql': 'Signal_Method', 'py': 'Signal_Method', 'param': 'Signal_Method', 'type': 'int', 'default': 4, 'label': 'метод усреднения сигнальной линии', 'sinput': False}, {'mql': 'Signal_XMA', 'py': 'Signal_XMA', 'param': 'Signal_XMA', 'type': 'int', 'default': 9, 'label': 'период сигнальной линии', 'sinput': False}, {'mql': 'Signal_XPhase', 'py': 'Signal_XPhase', 'param': 'Signal_XPhase', 'type': 'int', 'default': 100, 'label': 'параметр сигнальной линии,', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Digit', 'py': 'Digit', 'param': 'Digit', 'type': 'uint', 'default': 50, 'label': 'количество пунктов округления', 'sinput': False}, {'mql': 'AlertCount', 'py': 'AlertCount', 'param': 'AlertCount', 'type': 'uint', 'default': 0, 'label': 'количество подаваемых алертов', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_T3)  # метод усреднения гистограммы
Fast_XMA = _input('Fast_XMA', 12)  # период быстрого мувинга
Slow_XMA = _input('Slow_XMA', 26)  # период медленного мувинга
XPhase = _input('XPhase', 100)  # параметр усреднения мувингов,
Signal_Method = _input('Signal_Method', MODE_JJMA)  # метод усреднения сигнальной линии
Signal_XMA = _input('Signal_XMA', 9)  # период сигнальной линии
Signal_XPhase = _input('Signal_XPhase', 100)  # параметр сигнальной линии,
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE_)  # ценовая константа
Digit = _input('Digit', 50)  # количество пунктов округления
AlertCount = _input('AlertCount', 0)  # количество подаваемых алертов
start = 0
macd_start = 0
XMACDBuffer = Arr(0, 0.0)
SignBuffer = Arr(0, 0.0)
ColorXMACDBuffer = Arr(0, 0.0)
ColorSignBuffer = Arr(0, 0.0)

def OnInit():
    global macd_start, start
    macd_start = MathMax(GetStartBars(XMA_Method, Fast_XMA, XPhase), GetStartBars(XMA_Method, Slow_XMA, XPhase))
    start = macd_start + GetStartBars(Signal_Method, Signal_XMA, Signal_XPhase)
    SetIndexBuffer(0, XMACDBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, macd_start)
    PlotIndexSetString(0, PLOT_LABEL, 'XMACD')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorXMACDBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, macd_start + 1)
    SetIndexBuffer(2, SignBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, start)
    PlotIndexSetString(2, PLOT_LABEL, 'Signal XMA')
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, ColorSignBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, start + 1)
    XMA1.XMALengthCheck('Fast_XMA', Fast_XMA)
    XMA1.XMALengthCheck('Slow_XMA', Slow_XMA)
    XMA1.XMALengthCheck('Signal_XMA', Signal_XMA)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    XMA1.XMAPhaseCheck('Signal_XPhase', Signal_XPhase, Signal_Method)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(XMA_Method)
    Smooth2 = XMA1.GetString_MA_Method(Signal_Method)
    StringConcatenate(shortname, 'XMACD( ', Fast_XMA, ', ', Slow_XMA, ', ', Signal_XMA, ', ', Smooth1, ', ', Smooth2, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_DnCount, _s_OnCalculate_UpCount
    if rates_total < start:
        return 0
    first1 = 0
    first2 = 0
    first3 = 0
    bar = 0
    bar1 = 0
    bar2 = 0
    price_ = 0.0
    fast_xma = 0.0
    slow_xma = 0.0
    xmacd = 0.0
    sign_xma = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first1 = 0
        first2 = macd_start + 1
        first3 = start + 1
    else:
        first1 = prev_calculated - 1
        first2 = first1
        first3 = first1
    bar = first1
    for bar in range(bar, rates_total):
        price_ = PriceSeries(AppliedPrice, bar, open, low, high, close)
        fast_xma = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Fast_XMA, price_, bar, False)
        slow_xma = XMA2.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Slow_XMA, price_, bar, False)
        xmacd = _fdiv(fast_xma - slow_xma, Point())
        sign_xma = XMA3.XMASeries(macd_start, prev_calculated, rates_total, Signal_Method, Signal_XPhase, Signal_XMA, xmacd, bar, False)
        XMACDBuffer[bar] = Digit * MathRound(xmacd / Digit)
        SignBuffer[bar] = Digit * MathRound(sign_xma / Digit)
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first2
    for bar in range(bar, rates_total):
        clr = 2
        if XMACDBuffer[bar] > 0:
            if XMACDBuffer[bar] > XMACDBuffer[bar - 1]:
                clr = 0
            if XMACDBuffer[bar] < XMACDBuffer[bar - 1]:
                clr = 1
        if XMACDBuffer[bar] < 0:
            if XMACDBuffer[bar] < XMACDBuffer[bar - 1]:
                clr = 3
            if XMACDBuffer[bar] > XMACDBuffer[bar - 1]:
                clr = 4
        ColorXMACDBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first3
    for bar in range(bar, rates_total):
        ColorSignBuffer[bar] = 1.0
        if XMACDBuffer[bar] > SignBuffer[bar - 1]:
            ColorSignBuffer[bar] = 0.0
        if XMACDBuffer[bar] < SignBuffer[bar - 1]:
            ColorSignBuffer[bar] = 2.0
    else:
        bar = _range_end(bar, rates_total, 1)
    if rates_total != prev_calculated:
        _s_OnCalculate_UpCount = 0
        _s_OnCalculate_DnCount = 0
    bar1 = rates_total - 2
    bar2 = rates_total - 3
    if (_s_OnCalculate_UpCount < AlertCount and ColorSignBuffer[bar1] == 2) and ColorSignBuffer[bar2] == 1:
        _s_OnCalculate_UpCount += 1
        Alert('XMACD индикатор ' + Symbol() + EnumToString(PERIOD_CURRENT, 'ENUM_TIMEFRAMES') + ': Сигнал на покупку ' + Symbol())
    if (_s_OnCalculate_DnCount < AlertCount and ColorSignBuffer[bar1] == 1) and ColorSignBuffer[bar2] == 2:
        _s_OnCalculate_DnCount += 1
        Alert('XMACD индикатор ' + Symbol() + EnumToString(PERIOD_CURRENT, 'ENUM_TIMEFRAMES') + ': Сигнал на продажу ' + Symbol())
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()
XMA3 = _alloc(CXMA)
XMA3.__init__()

# ---- static local variables
_s_OnCalculate_UpCount = 0
_s_OnCalculate_DnCount = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorXMACDDigit(_MQL5Indicator):
    name = 'ColorXMACD_Digit'
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
        'Signal_XPhase': 100,  # параметр сигнальной линии,
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # ценовая константа
        'Digit': 50,  # количество пунктов округления
        'AlertCount': 0,  # количество подаваемых алертов
    }

