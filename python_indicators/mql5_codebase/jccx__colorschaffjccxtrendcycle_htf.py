"""jccx — converted from MQL5: MQL5 Indicators/ColorSchaffJCCXTrendCycle_HTF/jccx.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'JCCX'}, 'levels': [0.5, -0.5, 0.0], 'description': [], 'name': 'jccx', 'source': 'MQL5 Indicators/ColorSchaffJCCXTrendCycle_HTF/jccx.mq5', 'folder': 'ColorSchaffJCCXTrendCycle_HTF', 'inputs': [{'mql': 'JMALength', 'py': 'JMALength', 'param': 'JMALength', 'type': 'uint', 'default': 8, 'label': 'Глубина  JJMA сглаживания входной цены', 'sinput': False}, {'mql': 'JMAPhase', 'py': 'JMAPhase', 'param': 'JMAPhase', 'type': 'int', 'default': 100, 'label': 'Параметр JJMA усреднения', 'sinput': False}, {'mql': 'JurXLength', 'py': 'JurXLength', 'param': 'JurXLength', 'type': 'uint', 'default': 8, 'label': 'Глубина JurX усреднения индикатора', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
JMALength = _input('JMALength', 8)  # Глубина  JJMA сглаживания входной цены
JMAPhase = _input('JMAPhase', 100)  # Параметр JJMA усреднения
JurXLength = _input('JurXLength', 8)  # Глубина JurX усреднения индикатора
IPC = _input('IPC', PRICE_CLOSE_)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
JCCX = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, JCCX, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 30)
    PlotIndexSetString(0, PLOT_LABEL, 'JCCX')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'JCCX( JMALength = ', JMALength, ', JMAPhase = ', JMAPhase, ', JurXLength = ', JurXLength, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    JMA = CJJMA()
    JMA.JJMALengthCheck('JMALength', JMALength)
    JMA.JJMALengthCheck('JurXLength', JurXLength)
    JMA.JJMAPhaseCheck('JMAPhase', JMAPhase)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 0:
        return 0
    price_ = 0.0
    jma = 0.0
    up_cci = 0.0
    dn_cci = 0.0
    up_jccx = 0.0
    dn_jccx = 0.0
    jccx = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        jma = _s_OnCalculate_JMA.JJMASeries(0, prev_calculated, rates_total, 0, JMAPhase, JMALength, price_, bar, False)
        up_cci = price_ - jma
        dn_cci = MathAbs(up_cci)
        up_jccx = _s_OnCalculate_Jur1.JurXSeries(30, prev_calculated, rates_total, 0, JurXLength, up_cci, bar, False)
        dn_jccx = _s_OnCalculate_Jur2.JurXSeries(30, prev_calculated, rates_total, 0, JurXLength, dn_cci, bar, False)
        if dn_jccx == 0:
            jccx = EMPTY_VALUE
        else:
            jccx = _fdiv(up_jccx, dn_jccx)
            if jccx > 1:
                jccx = 1.0
            if jccx < -1:
                jccx = -1.0
        JCCX[bar] = jccx
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Jur1 = CJurX()
_s_OnCalculate_Jur2 = CJurX()
_s_OnCalculate_JMA = CJJMA()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Jccx(_MQL5Indicator):
    name = 'jccx'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'JMALength': 8,  # Глубина  JJMA сглаживания входной цены
        'JMAPhase': 100,  # Параметр JJMA усреднения
        'JurXLength': 8,  # Глубина JurX усреднения индикатора
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

