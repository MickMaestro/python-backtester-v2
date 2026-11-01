"""jmomentum — converted from MQL5: MQL5 Indicators/JMomentum_HTF/jmomentum.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [128]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'JMomentum'}, 'levels': [0.5, -0.5, 0.0], 'description': [], 'name': 'jmomentum', 'source': 'MQL5 Indicators/JMomentum_HTF/jmomentum.mq5', 'folder': 'JMomentum_HTF', 'inputs': [{'mql': 'MLength', 'py': 'MLength', 'param': 'MLength', 'type': 'int', 'default': 8, 'label': 'Глубина  сглаживания', 'sinput': False}, {'mql': 'JLength', 'py': 'JLength', 'param': 'JLength', 'type': 'int', 'default': 8, 'label': 'Глубина JMA сглаживания индикатора Momentum', 'sinput': False}, {'mql': 'JPhase', 'py': 'JPhase', 'param': 'JPhase', 'type': 'int', 'default': 100, 'label': 'Параметр JMA сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
MLength = _input('MLength', 8)  # Глубина  сглаживания
JLength = _input('JLength', 8)  # Глубина JMA сглаживания индикатора Momentum
JPhase = _input('JPhase', 100)  # Параметр JMA сглаживания
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
JMomentum = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, JMomentum, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 0)
    PlotIndexSetString(0, PLOT_LABEL, 'JMomentum')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'JMomentum( MLengthh = ', MLength, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    Mom = CMomentum()
    JMA = CJJMA()
    Mom.MALengthCheck_1('MLength', MLength)
    JMA.JJMALengthCheck('JLength', JLength)
    JMA.JJMAPhaseCheck('JPhase', JPhase)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (MLength + 31):
        return 0
    price = 0.0
    momentum = 0.0
    jmomentum = 0.0
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
        jmomentum = _s_OnCalculate_JMA.JJMASeries(MLength + 1, prev_calculated, rates_total, 0, JPhase, JLength, momentum, bar, False)
        JMomentum[bar] = jmomentum
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Mom = CMomentum()
_s_OnCalculate_JMA = CJJMA()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Jmomentum(_MQL5Indicator):
    name = 'jmomentum'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MLength': 8,  # Глубина  сглаживания
        'JLength': 8,  # Глубина JMA сглаживания индикатора Momentum
        'JPhase': 100,  # Параметр JMA сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

