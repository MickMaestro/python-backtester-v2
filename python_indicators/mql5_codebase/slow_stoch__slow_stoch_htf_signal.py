"""slow-stoch — converted from MQL5: MQL5 Indicators/Slow-Stoch_HTF_Signal/slow-stoch.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_minimum': 0.0, 'indicator_maximum': 100.0}, 'types': {1: 7}, 'colors': {1: [8421376, 16711935]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Stochastic; Signal'}, 'levels': [75.0, 50.0, 25.0], 'description': [], 'name': 'slow-stoch', 'source': 'MQL5 Indicators/Slow-Stoch_HTF_Signal/slow-stoch.mq5', 'folder': 'Slow-Stoch_HTF_Signal', 'inputs': [{'mql': 'KPeriod', 'py': 'KPeriod', 'param': 'KPeriod', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'STO_Method', 'py': 'STO_Method', 'param': 'STO_Method', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field', 'py': 'Price_field', 'param': 'Price_field', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 4, 'label': 'Method of averaging', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 5, 'label': 'Type of smoothing', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
KPeriod = _input('KPeriod', 5)
DPeriod = _input('DPeriod', 3)
Slowing = _input('Slowing', 3)
STO_Method = _input('STO_Method', MODE_SMA)
Price_field = _input('Price_field', STO_LOWHIGH)
XMA_Method = _input('XMA_Method', MODE_JJMA)  # Method of averaging
XLength = _input('XLength', 5)  # Type of smoothing
XPhase = _input('XPhase', 15)  # Smoothing parameter
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
StoBuffer = Arr(0, 0.0)
SignBuffer = Arr(0, 0.0)
STO_Handle = 0
min_rates_total = 0
min_rates_Sto = 0

def OnInit():
    global STO_Handle, min_rates_Sto, min_rates_total
    min_rates_Sto = _int(KPeriod + DPeriod + Slowing)
    min_rates_total = GetStartBars(XMA_Method, XLength, XPhase)
    STO_Handle = iStochastic(None, 0, KPeriod, DPeriod, Slowing, STO_Method, Price_field)
    if STO_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of the iStochastic indicator')
        return INIT_FAILED
    SetIndexBuffer(0, StoBuffer, INDICATOR_DATA)
    ArraySetAsSeries(StoBuffer, True)
    SetIndexBuffer(1, SignBuffer, INDICATOR_DATA)
    ArraySetAsSeries(SignBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Slow-Stoch')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(STO_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    maxbar = 0
    bar = 0
    STO = Arr(0, 0.0)
    SIG = Arr(0, 0.0)
    ArraySetAsSeries(STO, True)
    ArraySetAsSeries(SIG, True)
    maxbar = rates_total - 1 - min_rates_Sto
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(STO_Handle, MAIN_LINE, 0, to_copy, STO) <= 0:
        return 0
    if CopyBuffer(STO_Handle, SIGNAL_LINE, 0, to_copy, SIG) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        StoBuffer[bar] = _s_OnCalculate_XMA1.XMASeries(maxbar, prev_calculated, rates_total, XMA_Method, XPhase, XLength, STO[bar], bar, True)
        SignBuffer[bar] = _s_OnCalculate_XMA2.XMASeries(maxbar, prev_calculated, rates_total, XMA_Method, XPhase, XLength, SIG[bar], bar, True)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_XMA1 = CXMA()
_s_OnCalculate_XMA2 = CXMA()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SlowStoch(_MQL5Indicator):
    name = 'slow-stoch'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'KPeriod': 5,
        'DPeriod': 3,
        'Slowing': 3,
        'STO_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Method of averaging
        'XLength': 5,  # Type of smoothing
        'XPhase': 15,  # Smoothing parameter
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }
    y_range = (0.0, 100.0)

