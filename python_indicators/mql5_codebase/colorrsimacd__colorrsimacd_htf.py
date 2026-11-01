"""ColorRsiMACD — converted from MQL5: MQL5 Indicators/ColorRsiMACD_HTF/ColorRsiMACD.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 10, 2: 8}, 'colors': {1: [8421504, 8421376, 14822282, 6053069, 16711935], 2: [8421504, 16748574, 16711935]}, 'widths': {1: 2, 2: 3}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'ColorRsiMACD', 2: 'Signal Line'}, 'levels': [], 'description': [], 'name': 'ColorRsiMACD', 'source': 'MQL5 Indicators/ColorRsiMACD_HTF/ColorRsiMACD.mq5', 'folder': 'ColorRsiMACD_HTF', 'inputs': [{'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 7, 'label': 'метод усреднения гистограммы', 'sinput': False}, {'mql': 'Fast_XMA', 'py': 'Fast_XMA', 'param': 'Fast_XMA', 'type': 'uint', 'default': 12, 'label': 'период быстрого мувинга', 'sinput': False}, {'mql': 'Slow_XMA', 'py': 'Slow_XMA', 'param': 'Slow_XMA', 'type': 'uint', 'default': 26, 'label': 'период медленного мувинга', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 100, 'label': 'параметр усреднения мувингов,', 'sinput': False}, {'mql': 'Signal_Method', 'py': 'Signal_Method', 'param': 'Signal_Method', 'type': 'int', 'default': 4, 'label': 'метод усреднения сигнальной линии', 'sinput': False}, {'mql': 'Signal_XMA', 'py': 'Signal_XMA', 'param': 'Signal_XMA', 'type': 'int', 'default': 9, 'label': 'период сигнальной линии', 'sinput': False}, {'mql': 'Signal_Phase', 'py': 'Signal_Phase', 'param': 'Signal_Phase', 'type': 'int', 'default': 100, 'label': 'параметр сигнальной линии,', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
RSIPeriod = _input('RSIPeriod', 14)
RSIPrice = _input('RSIPrice', PRICE_CLOSE)
XMA_Method = _input('XMA_Method', MODE_T3)  # метод усреднения гистограммы
Fast_XMA = _input('Fast_XMA', 12)  # период быстрого мувинга
Slow_XMA = _input('Slow_XMA', 26)  # период медленного мувинга
XPhase = _input('XPhase', 100)  # параметр усреднения мувингов,
Signal_Method = _input('Signal_Method', MODE_JJMA)  # метод усреднения сигнальной линии
Signal_XMA = _input('Signal_XMA', 9)  # период сигнальной линии
Signal_Phase = _input('Signal_Phase', 100)  # параметр сигнальной линии,
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE_)  # ценовая константа
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
min_rates_3 = 0
XMACDBuffer = Arr(0, 0.0)
SignBuffer = Arr(0, 0.0)
ColorXMACDBuffer = Arr(0, 0.0)
ColorSignBuffer = Arr(0, 0.0)
Ind_Handle = 0

def OnInit():
    global Ind_Handle, min_rates_1, min_rates_2, min_rates_3, min_rates_total
    min_rates_1 = _int(RSIPeriod)
    min_rates_2 = min_rates_1 + GetStartBars(XMA_Method, Fast_XMA, XPhase)
    min_rates_3 = min_rates_2 + GetStartBars(XMA_Method, Slow_XMA, XPhase)
    min_rates_total = min_rates_3 + GetStartBars(Signal_Method, Signal_XMA, Signal_Phase) + 2
    Ind_Handle = iRSI(Symbol(), None, RSIPeriod, RSIPrice)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI')
        return INIT_FAILED
    SetIndexBuffer(0, XMACDBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorXMACDBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, SignBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ColorSignBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    XMA1.XMALengthCheck('Fast_XMA', Fast_XMA)
    XMA1.XMALengthCheck('Slow_XMA', Slow_XMA)
    XMA1.XMALengthCheck('Signal_XMA', Signal_XMA)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    XMA1.XMAPhaseCheck('Signal_Phase', Signal_Phase, Signal_Method)
    shortname = 'ColorRsiMACD'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < rates_total:
        return prev_calculated
    first1 = 0
    first2 = 0
    first3 = 0
    bar = 0
    RSI = Arr(1, 0.0, dyn=False)
    fast_rsi = 0.0
    slow_rsi = 0.0
    rsi_macd = 0.0
    sign_rsi = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first1 = min_rates_1
        first2 = min_rates_1 + 1
        first3 = min_rates_total + 1
    else:
        first1 = prev_calculated - 1
        first2 = first1
        first3 = first1
    bar = first1
    for bar in range(bar, rates_total):
        if CopyBuffer(Ind_Handle, 0, rates_total - 1 - bar, 1, RSI) <= 0:
            return 0
        fast_rsi = XMA1.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XPhase, Fast_XMA, RSI[0], bar, False)
        slow_rsi = XMA2.XMASeries(min_rates_2, prev_calculated, rates_total, XMA_Method, XPhase, Slow_XMA, fast_rsi, bar, False)
        rsi_macd = fast_rsi - slow_rsi
        sign_rsi = XMA3.XMASeries(min_rates_3, prev_calculated, rates_total, Signal_Method, Signal_Phase, Signal_XMA, rsi_macd, bar, False)
        XMACDBuffer[bar] = rsi_macd
        SignBuffer[bar] = sign_rsi
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first2
    for bar in range(bar, rates_total):
        ColorXMACDBuffer[bar] = 0.0
        if XMACDBuffer[bar] > 0:
            if XMACDBuffer[bar] > XMACDBuffer[bar - 1]:
                ColorXMACDBuffer[bar] = 1.0
            if XMACDBuffer[bar] < XMACDBuffer[bar - 1]:
                ColorXMACDBuffer[bar] = 2.0
        if XMACDBuffer[bar] < 0:
            if XMACDBuffer[bar] < XMACDBuffer[bar - 1]:
                ColorXMACDBuffer[bar] = 3.0
            if XMACDBuffer[bar] > XMACDBuffer[bar - 1]:
                ColorXMACDBuffer[bar] = 4.0
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first3
    for bar in range(bar, rates_total):
        ColorSignBuffer[bar] = 0.0
        if XMACDBuffer[bar] > SignBuffer[bar - 1]:
            ColorSignBuffer[bar] = 1.0
        if XMACDBuffer[bar] < SignBuffer[bar - 1]:
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorRsiMACD(_MQL5Indicator):
    name = 'ColorRsiMACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSIPeriod': 14,
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # метод усреднения гистограммы
        'Fast_XMA': 12,  # период быстрого мувинга
        'Slow_XMA': 26,  # период медленного мувинга
        'XPhase': 100,  # параметр усреднения мувингов,
        'Signal_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения сигнальной линии
        'Signal_XMA': 9,  # период сигнальной линии
        'Signal_Phase': 100,  # параметр сигнальной линии,
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
    }

