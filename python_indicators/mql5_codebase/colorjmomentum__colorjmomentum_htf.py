"""colorjmomentum — converted from MQL5: MQL5 Indicators/ColorJMomentum_HTF/colorjmomentum.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 5, 3: 5, 4: 5}, 'colors': {1: [8421504], 2: [8388352], 3: [9639167], 4: [8421504]}, 'widths': {1: 1, 2: 3, 3: 3, 4: 3}, 'styles': {1: 0}, 'labels': {1: 'JMomentum', 2: 'Up_Signal', 3: 'Dn_Signal', 4: 'No_Signal'}, 'levels': [], 'description': [], 'name': 'colorjmomentum', 'source': 'MQL5 Indicators/ColorJMomentum_HTF/colorjmomentum.mq5', 'folder': 'ColorJMomentum_HTF', 'inputs': [{'mql': 'MLength', 'py': 'MLength', 'param': 'MLength', 'type': 'int', 'default': 8, 'label': 'Период индикатора Momentum', 'sinput': False}, {'mql': 'JMLength', 'py': 'JMLength', 'param': 'JMLength', 'type': 'int', 'default': 8, 'label': 'Глубина JMA сглаживания индикатора Momentum', 'sinput': False}, {'mql': 'JPhase', 'py': 'JPhase', 'param': 'JPhase', 'type': 'int', 'default': 100, 'label': 'Параметр JMA сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
MLength = _input('MLength', 8)  # Период индикатора Momentum
JMLength = _input('JMLength', 8)  # Глубина JMA сглаживания индикатора Momentum
JPhase = _input('JPhase', 100)  # Параметр JMA сглаживания
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
JMomentum = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
FlBuffer = Arr(0, 0.0)
start = 0

def OnInit():
    global start
    start = MLength + 31
    SetIndexBuffer(0, JMomentum, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, MLength)
    PlotIndexSetString(0, PLOT_LABEL, 'JMomentum')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, start)
    PlotIndexSetString(1, PLOT_LABEL, 'Up Signal')
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    SetIndexBuffer(2, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, start)
    PlotIndexSetString(2, PLOT_LABEL, 'Dn Signal')
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    SetIndexBuffer(3, FlBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, start)
    PlotIndexSetString(3, PLOT_LABEL, 'No Signal')
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    shortname = Box("")
    StringConcatenate(shortname, 'JMomentum( MLength = ', MLength, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    Mom = CMomentum()
    JMA = CJJMA()
    Mom.MALengthCheck_1('MLength', MLength)
    JMA.JJMALengthCheck('JMLength', JMLength)
    JMA.JJMAPhaseCheck('JPhase', JPhase)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < start:
        return 0
    price = 0.0
    momentum = 0.0
    jmomentum = 0.0
    dmomentum = 0.0
    first = 0
    bar = 0
    if prev_calculated == 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        momentum = _s_OnCalculate_Mom.MomentumSeries(0, prev_calculated, rates_total, MLength, price, bar, False)
        jmomentum = _s_OnCalculate_JMA.JJMASeries(MLength + 1, prev_calculated, rates_total, 0, JPhase, JMLength, momentum, bar, False)
        JMomentum[bar] = _fdiv(jmomentum, Point())
        UpBuffer[bar] = EMPTY_VALUE
        DnBuffer[bar] = EMPTY_VALUE
        FlBuffer[bar] = EMPTY_VALUE
        if bar < start:
            continue
        dmomentum = NormalizeDouble(JMomentum[bar] - JMomentum[bar - 1], 0)
        if dmomentum > 0:
            UpBuffer[bar] = JMomentum[bar]
        if dmomentum < 0:
            DnBuffer[bar] = JMomentum[bar]
        if dmomentum == 0:
            FlBuffer[bar] = JMomentum[bar]
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Mom = CMomentum()
_s_OnCalculate_JMA = CJJMA()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorjmomentum(_MQL5Indicator):
    name = 'colorjmomentum'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MLength': 8,  # Период индикатора Momentum
        'JMLength': 8,  # Глубина JMA сглаживания индикатора Momentum
        'JPhase': 100,  # Параметр JMA сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

