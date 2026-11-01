"""ccibands — converted from MQL5: MQL5 Indicators/CCIBands/ccibands.mq5

Commodity Channel Index High-Low Band
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [65280], 2: [14822282], 3: [255]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'UpCCI', 2: 'MediumCCI', 3: 'LowCCI'}, 'levels': [100.0, 0.0, -100.0], 'description': ['Commodity Channel Index High-Low Band'], 'name': 'ccibands', 'source': 'MQL5 Indicators/CCIBands/ccibands.mq5', 'folder': 'CCIBands', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'CCIPeriod', 'py': 'CCIPeriod', 'param': 'CCIPeriod', 'type': 'uint', 'default': 14, 'label': 'Период CCI индикатора', 'sinput': False}, {'mql': 'koeff', 'py': 'koeff', 'param': 'koeff', 'type': 'double', 'default': 0.015, 'label': '', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_SMA)  # Метод усреднения
CCIPeriod = _input('CCIPeriod', 14)  # Период CCI индикатора
koeff = _input('koeff', 0.015)
XPhase = _input('XPhase', 15)  # Параметр сглаживания
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
ExtBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(GetStartBars(XMA_Method, CCIPeriod, XPhase) + CCIPeriod)
    SetIndexBuffer(0, ExtABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ExtBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, ExtBBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CCIBands')
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    ExtPrice_C = 0.0
    ExtPrice_H = 0.0
    ExtPrice_L = 0.0
    ExtMov_C = 0.0
    ExtMov_H = 0.0
    ExtMov_L = 0.0
    dSum_C = 0.0
    dSum_H = 0.0
    dSum_L = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        ExtPrice_C = (high[bar] + low[bar] + close[bar]) / 3
        ExtPrice_H = (high[bar] + low[bar] + high[bar]) / 3
        ExtPrice_L = (high[bar] + low[bar] + low[bar]) / 3
        ExtMov_C = C1XMA.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, CCIPeriod, ExtPrice_C, bar, False)
        ExtMov_H = H1XMA.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, CCIPeriod, ExtPrice_H, bar, False)
        ExtMov_L = L1XMA.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, CCIPeriod, ExtPrice_L, bar, False)
        dSum_C = koeff * C2XMA.XMASeries(CCIPeriod, prev_calculated, rates_total, MODE_SMA_, XPhase, CCIPeriod, MathAbs(ExtPrice_C - ExtMov_C), bar, False)
        dSum_H = koeff * H2XMA.XMASeries(CCIPeriod, prev_calculated, rates_total, MODE_SMA_, XPhase, CCIPeriod, MathAbs(ExtPrice_H - ExtMov_C), bar, False)
        dSum_L = koeff * L2XMA.XMASeries(CCIPeriod, prev_calculated, rates_total, MODE_SMA_, XPhase, CCIPeriod, MathAbs(ExtPrice_L - ExtMov_C), bar, False)
        ExtABuffer[bar] = 0.0
        ExtBBuffer[bar] = 0.0
        ExtBuffer[bar] = 0.0
        if dSum_C:
            ExtBuffer[bar] = _fdiv(ExtPrice_C - ExtMov_C, dSum_C)
        if dSum_H:
            ExtABuffer[bar] = _fdiv(ExtPrice_H - ExtMov_C, dSum_H)
        if dSum_L:
            ExtBBuffer[bar] = _fdiv(ExtPrice_L - ExtMov_C, dSum_L)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
H1XMA = _alloc(CXMA)
H1XMA.__init__()
H2XMA = _alloc(CXMA)
H2XMA.__init__()
C1XMA = _alloc(CXMA)
C1XMA.__init__()
C2XMA = _alloc(CXMA)
C2XMA.__init__()
L1XMA = _alloc(CXMA)
L1XMA.__init__()
L2XMA = _alloc(CXMA)
L2XMA.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ccibands(_MQL5Indicator):
    name = 'ccibands'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения
        'CCIPeriod': 14,  # Период CCI индикатора
        'koeff': 0.015,
        'XPhase': 15,  # Параметр сглаживания
    }

