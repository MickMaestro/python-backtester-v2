"""jjrsx — converted from MQL5: MQL5 Indicators/ColorZerolagJJRSX/jjrsx.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [14822282]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'JJRSX'}, 'levels': [0.5, -0.5, 0.0], 'description': [], 'name': 'jjrsx', 'source': 'MQL5 Indicators/ColorZerolagJJRSX/jjrsx.mq5', 'folder': 'ColorZerolagJJRSX', 'inputs': [{'mql': 'JLength', 'py': 'JLength', 'param': 'JLength', 'type': 'uint', 'default': 8, 'label': 'Глубина  сглаживания', 'sinput': False}, {'mql': 'Smooth', 'py': 'Smooth', 'param': 'Smooth', 'type': 'uint', 'default': 8, 'label': 'Глубина JJMA усреднения', 'sinput': False}, {'mql': 'JPhase', 'py': 'JPhase', 'param': 'JPhase', 'type': 'int', 'default': 100, 'label': 'Параметр JJMA усреднения', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
JLength = _input('JLength', 8)  # Глубина  сглаживания
Smooth = _input('Smooth', 8)  # Глубина JJMA усреднения
JPhase = _input('JPhase', 100)  # Параметр JJMA усреднения
IPC = _input('IPC', PRICE_CLOSE_)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
JJRSX = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, JJRSX, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 32)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'JJRSX( Length = ', JLength, ', Smooth = ', Smooth, ', Phase = ', JPhase, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    JMA = CJJMA()
    JMA.JJMALengthCheck('Length', JLength)
    JMA.JJMALengthCheck('Smooth', Smooth)
    JMA.JJMAPhaseCheck('Phase', JPhase)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 32:
        return 0
    dprice = 0.0
    udprice = 0.0
    up_jrsx = 0.0
    dn_jrsx = 0.0
    jrsx = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        dprice = PriceSeries(IPC, bar, open, low, high, close) - PriceSeries(IPC, bar - 1, open, low, high, close)
        udprice = MathAbs(dprice)
        up_jrsx = _s_OnCalculate_Jur1.JurXSeries(1, prev_calculated, rates_total, 0, JLength, dprice, bar, False)
        dn_jrsx = _s_OnCalculate_Jur2.JurXSeries(1, prev_calculated, rates_total, 0, JLength, udprice, bar, False)
        if not dn_jrsx:
            jrsx = EMPTY_VALUE
        else:
            jrsx = _fdiv(up_jrsx, dn_jrsx)
            jrsx = MathMax(MathMin(jrsx, 1), -1)
        JJRSX[bar] = _s_OnCalculate_JMA.JJMASeries(1, prev_calculated, rates_total, 0, JPhase, Smooth, jrsx, bar, False)
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


class Jjrsx(_MQL5Indicator):
    name = 'jjrsx'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'JLength': 8,  # Глубина  сглаживания
        'Smooth': 8,  # Глубина JJMA усреднения
        'JPhase': 100,  # Параметр JJMA усреднения
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

