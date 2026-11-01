"""KI_signals — converted from MQL5: MQL5 Indicators/KI_signals/KI_signals.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16711935, 14524637, 8421504, 16760576, 16711680]}, 'widths': {}, 'styles': {}, 'labels': {1: 'KI_signals Open;High;Low;Close'}, 'levels': [], 'description': [], 'name': 'KI_signals', 'source': 'MQL5 Indicators/KI_signals/KI_signals.mq5', 'folder': 'KI_signals', 'inputs': [{'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 2, 'label': 'Вариант торговых сигналов', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 7, 'label': 'метод усреднения гистограммы', 'sinput': False}, {'mql': 'Fast_XMA', 'py': 'Fast_XMA', 'param': 'Fast_XMA', 'type': 'uint', 'default': 12, 'label': 'период быстрого мувинга', 'sinput': False}, {'mql': 'Slow_XMA', 'py': 'Slow_XMA', 'param': 'Slow_XMA', 'type': 'uint', 'default': 26, 'label': 'период медленного мувинга', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 100, 'label': 'параметр усреднения мувингов,', 'sinput': False}, {'mql': 'Signal_Method', 'py': 'Signal_Method', 'param': 'Signal_Method', 'type': 'int', 'default': 4, 'label': 'метод усреднения сигнальной линии', 'sinput': False}, {'mql': 'Signal_XMA', 'py': 'Signal_XMA', 'param': 'Signal_XMA', 'type': 'int', 'default': 9, 'label': 'период сигнальной линии', 'sinput': False}, {'mql': 'Signal_Phase', 'py': 'Signal_Phase', 'param': 'Signal_Phase', 'type': 'int', 'default': 100, 'label': 'параметр сигнальной линии,', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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

# enum ENUM_APPLIED_MODE_
HISTOGRAM = 0
SIGNAL = 1
CROSS = 2
_enum('ENUM_APPLIED_MODE_', {0: 'HISTOGRAM', 1: 'SIGNAL', 2: 'CROSS'})

# ---- inputs and global variables
Mode = _input('Mode', CROSS)  # Вариант торговых сигналов
XMA_Method = _input('XMA_Method', MODE_T3)  # метод усреднения гистограммы
Fast_XMA = _input('Fast_XMA', 12)  # период быстрого мувинга
Slow_XMA = _input('Slow_XMA', 26)  # период медленного мувинга
XPhase = _input('XPhase', 100)  # параметр усреднения мувингов,
Signal_Method = _input('Signal_Method', MODE_JJMA)  # метод усреднения сигнальной линии
Signal_XMA = _input('Signal_XMA', 9)  # период сигнальной линии
Signal_Phase = _input('Signal_Phase', 100)  # параметр сигнальной линии,
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE_)  # ценовая константа
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0

def OnInit():
    global min_rates_1, min_rates_total
    min_rates_1 = MathMax(GetStartBars(XMA_Method, Fast_XMA, XPhase), GetStartBars(XMA_Method, Slow_XMA, XPhase))
    min_rates_total = min_rates_1 + GetStartBars(Signal_Method, Signal_XMA, Signal_Phase) + 2
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    XMA1.XMALengthCheck('Fast_XMA', Fast_XMA)
    XMA1.XMALengthCheck('Slow_XMA', Slow_XMA)
    XMA1.XMALengthCheck('Signal_XMA', Signal_XMA)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    XMA1.XMAPhaseCheck('Signal_Phase', Signal_Phase, Signal_Method)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(XMA_Method)
    Smooth2 = XMA1.GetString_MA_Method(Signal_Method)
    StringConcatenate(shortname, 'KI_signals( ', Fast_XMA, ', ', Slow_XMA, ', ', Signal_XMA, ', ', Smooth1, ', ', Smooth2, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_sign_xma_prev, _s_OnCalculate_xmacd_prev
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    price_ = 0.0
    fast_xma = 0.0
    slow_xma = 0.0
    xmacd = 0.0
    sign_xma = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price_ = PriceSeries(AppliedPrice, bar, open, low, high, close)
        fast_xma = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Fast_XMA, price_, bar, False)
        slow_xma = XMA2.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, Slow_XMA, price_, bar, False)
        xmacd = fast_xma - slow_xma
        sign_xma = XMA3.XMASeries(min_rates_1, prev_calculated, rates_total, Signal_Method, Signal_Phase, Signal_XMA, xmacd, bar, False)
        ExtCloseBuffer[bar] = 0.0
        ExtHighBuffer[bar] = 0.0
        ExtLowBuffer[bar] = 0.0
        ExtOpenBuffer[bar] = 0.0
        ExtColorBuffer[bar] = 2.0
        _sw1 = Mode
        if _sw1 == HISTOGRAM:
            if _s_OnCalculate_xmacd_prev <= 0 and xmacd > 0:
                ExtCloseBuffer[bar] = close[bar]
                ExtHighBuffer[bar] = high[bar]
                ExtLowBuffer[bar] = low[bar]
                ExtOpenBuffer[bar] = open[bar]
                if close[bar] < open[bar]:
                    ExtColorBuffer[bar] = 0.0
                else:
                    ExtColorBuffer[bar] = 1.0
            if _s_OnCalculate_xmacd_prev >= 0 and xmacd < 0:
                ExtCloseBuffer[bar] = close[bar]
                ExtHighBuffer[bar] = high[bar]
                ExtLowBuffer[bar] = low[bar]
                ExtOpenBuffer[bar] = open[bar]
                if close[bar] < open[bar]:
                    ExtColorBuffer[bar] = 3.0
                else:
                    ExtColorBuffer[bar] = 4.0
        elif _sw1 == SIGNAL:
            if _s_OnCalculate_sign_xma_prev >= 0 and sign_xma < 0:
                ExtCloseBuffer[bar] = close[bar]
                ExtHighBuffer[bar] = high[bar]
                ExtLowBuffer[bar] = low[bar]
                ExtOpenBuffer[bar] = open[bar]
                if close[bar] < open[bar]:
                    ExtColorBuffer[bar] = 0.0
                else:
                    ExtColorBuffer[bar] = 1.0
            if _s_OnCalculate_sign_xma_prev <= 0 and sign_xma > 0:
                ExtCloseBuffer[bar] = close[bar]
                ExtHighBuffer[bar] = high[bar]
                ExtLowBuffer[bar] = low[bar]
                ExtOpenBuffer[bar] = open[bar]
                if close[bar] < open[bar]:
                    ExtColorBuffer[bar] = 3.0
                else:
                    ExtColorBuffer[bar] = 4.0
        elif _sw1 == CROSS:
            if _s_OnCalculate_xmacd_prev >= _s_OnCalculate_sign_xma_prev and xmacd < sign_xma:
                ExtCloseBuffer[bar] = close[bar]
                ExtHighBuffer[bar] = high[bar]
                ExtLowBuffer[bar] = low[bar]
                ExtOpenBuffer[bar] = open[bar]
                if close[bar] < open[bar]:
                    ExtColorBuffer[bar] = 0.0
                else:
                    ExtColorBuffer[bar] = 1.0
            if _s_OnCalculate_xmacd_prev <= _s_OnCalculate_sign_xma_prev and xmacd > sign_xma:
                ExtCloseBuffer[bar] = close[bar]
                ExtHighBuffer[bar] = high[bar]
                ExtLowBuffer[bar] = low[bar]
                ExtOpenBuffer[bar] = open[bar]
                if close[bar] < open[bar]:
                    ExtColorBuffer[bar] = 3.0
                else:
                    ExtColorBuffer[bar] = 4.0
        if bar < (rates_total - 1):
            _s_OnCalculate_xmacd_prev = xmacd
            _s_OnCalculate_sign_xma_prev = sign_xma
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

# ---- static local variables
_s_OnCalculate_xmacd_prev = 0.0
_s_OnCalculate_sign_xma_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KISignals(_MQL5Indicator):
    name = 'KI_signals'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Mode': _Choice({0: 'изменение направления гистограммы', 1: 'изменение направления сигнальной линии', 2: 'пересечение гистограммы и сигнальной линии'}, default=2),  # Вариант торговых сигналов
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # метод усреднения гистограммы
        'Fast_XMA': 12,  # период быстрого мувинга
        'Slow_XMA': 26,  # период медленного мувинга
        'XPhase': 100,  # параметр усреднения мувингов,
        'Signal_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения сигнальной линии
        'Signal_XMA': 9,  # период сигнальной линии
        'Signal_Phase': 100,  # параметр сигнальной линии,
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
    }

