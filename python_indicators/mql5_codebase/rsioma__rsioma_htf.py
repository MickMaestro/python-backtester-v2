"""RSIOMA — converted from MQL5: MQL5 Indicators/RSIOMA_HTF/RSIOMA.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 10, 2: 1}, 'colors': {1: [9639167, 8388736, 8421504, 2263842, 64636], 2: [13828244]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'RSIOMA', 2: 'Trigger'}, 'levels': [], 'description': [], 'name': 'RSIOMA', 'source': 'MQL5 Indicators/RSIOMA_HTF/RSIOMA.mq5', 'folder': 'RSIOMA_HTF', 'inputs': [{'mql': 'RSIOMA_Method', 'py': 'RSIOMA_Method', 'param': 'RSIOMA_Method', 'type': 'int', 'default': 1, 'label': 'Метод усреднения RSIOMA', 'sinput': False}, {'mql': 'RSIOMA', 'py': 'RSIOMA', 'param': 'RSIOMA', 'type': 'uint', 'default': 14, 'label': 'Глубина усреднения RSIOMA', 'sinput': False}, {'mql': 'RSIOMAPhase', 'py': 'RSIOMAPhase', 'param': 'RSIOMAPhase', 'type': 'int', 'default': 15, 'label': 'Параметр усреднения RSIOMA', 'sinput': False}, {'mql': 'MARSIOMA_Method', 'py': 'MARSIOMA_Method', 'param': 'MARSIOMA_Method', 'type': 'int', 'default': 1, 'label': 'Метод усреднения MARSIOMA', 'sinput': False}, {'mql': 'MARSIOMA', 'py': 'MARSIOMA', 'param': 'MARSIOMA', 'type': 'uint', 'default': 21, 'label': 'Глубина усреднения RSIOMA', 'sinput': False}, {'mql': 'MARSIOMAPhase', 'py': 'MARSIOMAPhase', 'param': 'MARSIOMAPhase', 'type': 'int', 'default': 15, 'label': 'Параметр усреднения RSIOMA', 'sinput': False}, {'mql': 'MomPeriod', 'py': 'MomPeriod', 'param': 'MomPeriod', 'type': 'uint', 'default': 1, 'label': 'Период Моментума', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 20, 'label': 'Верхний уровень срабатывания', 'sinput': False}, {'mql': 'MiddleLevel', 'py': 'MiddleLevel', 'param': 'MiddleLevel', 'type': 'int', 'default': 0, 'label': 'Середина диапазона', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -20, 'label': 'Нижний уровень срабатывания', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
RSIOMA_Method = _input('RSIOMA_Method', MODE_EMA_)  # Метод усреднения RSIOMA
RSIOMA = _input('RSIOMA', 14)  # Глубина усреднения RSIOMA
RSIOMAPhase = _input('RSIOMAPhase', 15)  # Параметр усреднения RSIOMA
MARSIOMA_Method = _input('MARSIOMA_Method', MODE_EMA_)  # Метод усреднения MARSIOMA
MARSIOMA = _input('MARSIOMA', 21)  # Глубина усреднения RSIOMA
MARSIOMAPhase = _input('MARSIOMAPhase', 15)  # Параметр усреднения RSIOMA
MomPeriod = _input('MomPeriod', 1)  # Период Моментума
IPC = _input('IPC', PRICE_CLOSE_)  # Ценовая константа
HighLevel = _input('HighLevel', 20)  # Верхний уровень срабатывания
MiddleLevel = _input('MiddleLevel', 0)  # Середина диапазона
LowLevel = _input('LowLevel', -20)  # Нижний уровень срабатывания
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
TriggerBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
min_rates_3 = 0

def OnInit():
    global min_rates_1, min_rates_2, min_rates_3, min_rates_total
    min_rates_1 = GetStartBars(RSIOMA_Method, RSIOMA, RSIOMAPhase)
    min_rates_2 = _int(min_rates_1 + MomPeriod)
    min_rates_3 = _int(min_rates_2 + RSIOMA + 1)
    min_rates_total = min_rates_3 + GetStartBars(MARSIOMA_Method, MARSIOMA, RSIOMAPhase)
    XMA1.XMALengthCheck('RSIOMA', RSIOMA)
    XMA1.XMAPhaseCheck('RSIOMAPhase', RSIOMAPhase, RSIOMA_Method)
    XMA1.XMALengthCheck('MARSIOMA', MARSIOMA)
    XMA1.XMAPhaseCheck('RSIOMAPhase', RSIOMAPhase, MARSIOMA_Method)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, TriggerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSIOMA')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, MiddleLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrPurple)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrPurple)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_negative, _s_OnCalculate_prev_positive
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    x1xma = 0.0
    rel = 0.0
    RSI = 0.0
    positive = 0.0
    negative = 0.0
    sump = 0.0
    sumn = 0.0
    res = 0.0
    first = 0
    bar = 0
    clr = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        x1xma = XMA1.XMASeries(0, prev_calculated, rates_total, RSIOMA_Method, RSIOMAPhase, RSIOMA, price, bar, False)
        rel = Mom.MomentumSeries(min_rates_1, prev_calculated, rates_total, MomPeriod, x1xma, bar, False)
        sump = RSIOMA * XMA2.XMASeries(min_rates_2, prev_calculated, rates_total, MODE_SMA_, 0, RSIOMA, MathMax(rel, 0), bar, False)
        sumn = RSIOMA * XMA3.XMASeries(min_rates_2, prev_calculated, rates_total, MODE_SMA_, 0, RSIOMA, -MathMin(rel, 0), bar, False)
        if bar == min_rates_3:
            _s_OnCalculate_prev_positive = 0.0
            _s_OnCalculate_prev_negative = 0.0
        positive = ((_s_OnCalculate_prev_positive * (RSIOMA - 1)) + sump) / RSIOMA
        negative = ((_s_OnCalculate_prev_negative * (RSIOMA - 1)) + sumn) / RSIOMA
        if negative:
            res = 1.0 + _fdiv(positive, negative)
        else:
            res = 2.0
        if res:
            RSI = 50 - _fdiv(100, res)
        else:
            RSI = 0.0
        IndBuffer[bar] = RSI
        TriggerBuffer[bar] = XMA4.XMASeries(min_rates_3, prev_calculated, rates_total, MARSIOMA_Method, MARSIOMAPhase, MARSIOMA, RSI, bar, False)
        if bar < (rates_total - 1):
            _s_OnCalculate_prev_positive = positive
            _s_OnCalculate_prev_negative = negative
        clr = 2
        if RSI > MiddleLevel:
            if RSI > HighLevel:
                clr = 4
            else:
                clr = 3
        if RSI < MiddleLevel:
            if RSI < LowLevel:
                clr = 0
            else:
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
Mom = _alloc(CMomentum)
Mom.__init__()

# ---- static local variables
_s_OnCalculate_prev_positive = 0.0
_s_OnCalculate_prev_negative = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSIOMAIndicator(_MQL5Indicator):
    name = 'RSIOMA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSIOMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Метод усреднения RSIOMA
        'RSIOMA': 14,  # Глубина усреднения RSIOMA
        'RSIOMAPhase': 15,  # Параметр усреднения RSIOMA
        'MARSIOMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Метод усреднения MARSIOMA
        'MARSIOMA': 21,  # Глубина усреднения RSIOMA
        'MARSIOMAPhase': 15,  # Параметр усреднения RSIOMA
        'MomPeriod': 1,  # Период Моментума
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'HighLevel': 20,  # Верхний уровень срабатывания
        'MiddleLevel': 0,  # Середина диапазона
        'LowLevel': -20,  # Нижний уровень срабатывания
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

