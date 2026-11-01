"""f_rsi — converted from MQL5: MQL5 Indicators/F_RSI_HTF/f_rsi.mq5

Индикатор RSI с динамическими уровнями
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 7, 2: 1}, 'colors': {1: [16443110], 2: [9639167]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'RSI Cloud', 2: 'RSI'}, 'levels': [70.0, 50.0, 30.0], 'description': ['Индикатор RSI с динамическими уровнями'], 'name': 'f_rsi', 'source': 'MQL5 Indicators/F_RSI_HTF/f_rsi.mq5', 'folder': 'F_RSI_HTF', 'inputs': [{'mql': 'PeriodRSI', 'py': 'PeriodRSI', 'param': 'PeriodRSI', 'type': 'uint', 'default': 7, 'label': 'Период индикатора RSI', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 2, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'Dev', 'py': 'Dev', 'param': 'Dev', 'type': 'double', 'default': 1.0, 'label': 'Девиация', 'sinput': False}, {'mql': 'Applied_price', 'py': 'Applied_price', 'param': 'Applied_price', 'type': 'int', 'default': 1, 'label': 'Тип цены или handle', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
PeriodRSI = _input('PeriodRSI', 7)  # Период индикатора RSI
XMA_Method = _input('XMA_Method', MODE_SMMA)  # Метод усреднения
XPhase = _input('XPhase', 15)  # Параметр сглаживания
Dev = _input('Dev', 1.0)  # Девиация
Applied_price = _input('Applied_price', PRICE_CLOSE)  # Тип цены или handle
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Line1Buffer = Arr(0, 0.0)
Line2Buffer = Arr(0, 0.0)
Line3Buffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0

def OnInit():
    global min_rates_1, min_rates_2, min_rates_total
    min_rates_1 = 1
    min_rates_2 = min_rates_1 + GetStartBars(XMA_Method, PeriodRSI, XPhase)
    min_rates_total = min_rates_2 + _int(PeriodRSI)
    SetIndexBuffer(0, Line2Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, Line3Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(2, Line1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box("")
    StringConcatenate(shortname, 'F_RSI(', PeriodRSI, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    rl = 0.0
    rsi = 0.0
    ps = 0.0
    ng = 0.0
    srsi = 0.0
    sqr = 0.0
    s_dv = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        rl = PriceSeries(Applied_price, bar, open, low, high, close) - PriceSeries(Applied_price, bar - 1, open, low, high, close)
        ps = MathMax(0, rl)
        ng = -MathMin(0, rl)
        ps = XMA1.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XPhase, PeriodRSI, ps, bar, False)
        ng = XMA2.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XPhase, PeriodRSI, ng, bar, False)
        if (not ng) or (not (1 + _fdiv(ps, ng))):
            rsi = 100.0
        else:
            rsi = 100.0 - _fdiv(100.0, 1 + _fdiv(ps, ng))
        Line1Buffer[bar] = rsi
        srsi = XMA3.XMASeries(min_rates_2, prev_calculated, rates_total, MODE_SMA_, 0, PeriodRSI, rsi, bar, False)
        sqr = 0.0
        for kkk in range(_int(PeriodRSI) - 1, 0 - 1, -1):
            index = MathMax(0, bar - kkk)
            sqr += (Line1Buffer[index] - srsi) * (Line1Buffer[index] - srsi)
        s_dv = MathPow(sqr / PeriodRSI, 0.5)
        Line2Buffer[bar] = 50 + (Dev * s_dv)
        Line3Buffer[bar] = 50 - (Dev * s_dv)
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


class FRsi(_MQL5Indicator):
    name = 'f_rsi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PeriodRSI': 7,  # Период индикатора RSI
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=2),  # Метод усреднения
        'XPhase': 15,  # Параметр сглаживания
        'Dev': 1.0,  # Девиация
        'Applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Тип цены или handle
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

