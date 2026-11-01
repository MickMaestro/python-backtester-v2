"""FastStochastic — converted from MQL5: MQL5 Indicators/FastStochastic_HTF/FastStochastic.mq5

Быстрый стохастик, выполненный в виде цветной гистограммы
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 11, 2: 8}, 'colors': {1: [8421504, 3329330, 8421376, 3937500, 8388736], 2: [8421504, 16711680, 16711935]}, 'widths': {1: 3, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Main', 2: 'Signal'}, 'levels': [70.0, 50.0, 30.0], 'description': ['Быстрый стохастик, выполненный в виде цветной гистограммы'], 'name': 'FastStochastic', 'source': 'MQL5 Indicators/FastStochastic_HTF/FastStochastic.mq5', 'folder': 'FastStochastic_HTF', 'inputs': [{'mql': 'InpKPeriod', 'py': 'InpKPeriod', 'param': 'InpKPeriod', 'type': 'int', 'default': 5, 'label': 'K period', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'метод усреднения сигнальной линии', 'sinput': False}, {'mql': 'InpDPeriod', 'py': 'InpDPeriod', 'param': 'InpDPeriod', 'type': 'uint', 'default': 3, 'label': 'D period', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания сигнальной линии,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
InpKPeriod = _input('InpKPeriod', 5)  # K period
XMA_Method = _input('XMA_Method', MODE_SMA)  # метод усреднения сигнальной линии
InpDPeriod = _input('InpDPeriod', 3)  # D period
XPhase = _input('XPhase', 15)  # параметр сглаживания сигнальной линии,
IPC = _input('IPC', PRICE_CLOSE)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
UpSTOH = Arr(0, 0.0)
DnSTOH = Arr(0, 0.0)
SIGN = Arr(0, 0.0)
ColorSTOH = Arr(0, 0.0)
ColorSIGN = Arr(0, 0.0)
min_rates_total = 0
min_rates_ = 0

def OnInit():
    global min_rates_, min_rates_total
    min_rates_ = InpKPeriod
    min_rates_total = min_rates_ + 1 + XMA1.GetStartBars(XMA_Method, InpDPeriod, XPhase)
    SetIndexBuffer(0, UpSTOH, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpSTOH, True)
    SetIndexBuffer(1, DnSTOH, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(DnSTOH, True)
    SetIndexBuffer(2, ColorSTOH, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ColorSTOH, True)
    SetIndexBuffer(3, SIGN, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(SIGN, True)
    SetIndexBuffer(4, ColorSIGN, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ColorSIGN, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'FastStochastic(' + _str(InpKPeriod) + ',' + _str(InpDPeriod) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Prev_Main
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    maxbar = 0
    HH = 0.0
    LL = 0.0
    Range = 0.0
    Main = 0.0
    Price = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_
        _s_OnCalculate_Prev_Main = 50.0
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    maxbar = rates_total - min_rates_
    Main = _s_OnCalculate_Prev_Main
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        HH = high[ArrayMaximum(high, bar, InpKPeriod)]
        LL = low[ArrayMinimum(low, bar, InpKPeriod)]
        Range = MathMax(Point() * 1, HH - LL)
        Price = PriceSeries(IPC, bar, open, low, high, close)
        Main = _fdiv(100 * (Price - LL), Range)
        SIGN[bar] = XMA1.XMASeries(maxbar, prev_calculated, rates_total, XMA_Method, XPhase, InpDPeriod, Main, bar, True)
        if Main < 50:
            DnSTOH[bar] = Main
            UpSTOH[bar] = 50.0
        else:
            UpSTOH[bar] = Main
            DnSTOH[bar] = 50.0
        ColorSTOH[bar] = 0.0
        if Main > 50:
            if Main > _s_OnCalculate_Prev_Main:
                ColorSTOH[bar] = 1.0
            if Main < _s_OnCalculate_Prev_Main:
                ColorSTOH[bar] = 2.0
        if Main < 50:
            if Main < _s_OnCalculate_Prev_Main:
                ColorSTOH[bar] = 3.0
            if Main > _s_OnCalculate_Prev_Main:
                ColorSTOH[bar] = 4.0
        ColorSIGN[bar] = 0.0
        if Main > SIGN[bar + 1]:
            ColorSIGN[bar] = 1.0
        if Main < SIGN[bar + 1]:
            ColorSIGN[bar] = 2.0
        if bar:
            _s_OnCalculate_Prev_Main = Main
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()

# ---- static local variables
_s_OnCalculate_Prev_Main = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FastStochastic(_MQL5Indicator):
    name = 'FastStochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpKPeriod': 5,  # K period
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения сигнальной линии
        'InpDPeriod': 3,  # D period
        'XPhase': 15,  # параметр сглаживания сигнальной линии,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

