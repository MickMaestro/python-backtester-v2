"""ultimate_oscillator — converted from MQL5: MQL5 Indicators/Ultimate_Oscillator/ultimate_oscillator.mq5

Ultimate Oscillator
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Ultimate Oscillator'}, 'levels': [70.0, 50.0, 30.0], 'description': ['Ultimate Oscillator'], 'name': 'ultimate_oscillator', 'source': 'MQL5 Indicators/Ultimate_Oscillator/ultimate_oscillator.mq5', 'folder': 'Ultimate_Oscillator', 'inputs': [{'mql': 'fastperiod', 'py': 'fastperiod', 'param': 'fastperiod', 'type': 'uint', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'middleperiod', 'py': 'middleperiod', 'param': 'middleperiod', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'slowperiod', 'py': 'slowperiod', 'param': 'slowperiod', 'type': 'uint', 'default': 28, 'label': '', 'sinput': False}, {'mql': 'fastK', 'py': 'fastK', 'param': 'fastK', 'type': 'uint', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'middleK', 'py': 'middleK', 'param': 'middleK', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'slowK', 'py': 'slowK', 'param': 'slowK', 'type': 'uint', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift (in bars)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
fastperiod = _input('fastperiod', 7)
middleperiod = _input('middleperiod', 14)
slowperiod = _input('slowperiod', 28)
fastK = _input('fastK', 4)
middleK = _input('middleK', 2)
slowK = _input('slowK', 1)
Shift = _input('Shift', 0)  # Horizontal shift (in bars)
IndBuffer = Arr(0, 0.0)
min_rates_total = 0
divider = 0
FATR_Handle = 0
MATR_Handle = 0
SATR_Handle = 0

def OnInit():
    global FATR_Handle, MATR_Handle, SATR_Handle, divider, min_rates_total
    min_rates_total = _int(MathMax(MathMax(fastperiod, middleperiod), slowperiod) + fastK + middleK + slowK)
    divider = _int(fastK + middleK + slowK)
    FATR_Handle = iATR(None, 0, fastperiod)
    if FATR_Handle == INVALID_HANDLE:
        Print(' Error in creation of ATR indicator')
    MATR_Handle = iATR(None, 0, middleperiod)
    if MATR_Handle == INVALID_HANDLE:
        Print(' Error in creation of ATR indicator')
    SATR_Handle = iATR(None, 0, slowperiod)
    if SATR_Handle == INVALID_HANDLE:
        Print(' Error in creation of ATR indicator')
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Ultimate Oscillator')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((BarsCalculated(FATR_Handle) < rates_total or BarsCalculated(MATR_Handle) < rates_total) or BarsCalculated(SATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    FATR = Arr(0, 0.0)
    MATR = Arr(0, 0.0)
    SATR = Arr(0, 0.0)
    value = 0.0
    fast = 0.0
    middle = 0.0
    slow = 0.0
    RawUO = 0.0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar1 = 0
    maxbar2 = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 2
    else:
        limit = rates_total - prev_calculated
    maxbar1 = rates_total - 2
    maxbar2 = maxbar1 - min_rates_total
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(FATR, True)
    ArraySetAsSeries(MATR, True)
    ArraySetAsSeries(SATR, True)
    to_copy = limit + 1
    if CopyBuffer(FATR_Handle, 0, 0, to_copy, FATR) <= 0:
        return 0
    if CopyBuffer(MATR_Handle, 0, 0, to_copy, MATR) <= 0:
        return 0
    if CopyBuffer(SATR_Handle, 0, 0, to_copy, SATR) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        value = close[bar] - MathMin(low[bar], close[bar + 1])
        fast = FXMA.XMASeries(maxbar1, prev_calculated, rates_total, 0, 1, fastperiod, value, bar, True)
        middle = MXMA.XMASeries(maxbar1, prev_calculated, rates_total, 0, 1, middleperiod, value, bar, True)
        slow = SXMA.XMASeries(maxbar1, prev_calculated, rates_total, 0, 1, slowperiod, value, bar, True)
        if bar > maxbar2:
            continue
        RawUO = _fdiv(fastK * fast, FATR[bar]) + _fdiv(middleK * middle, MATR[bar]) + _fdiv(slowK * slow, SATR[bar])
        IndBuffer[bar] = _fdiv(RawUO, divider) * 100
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
FXMA = _alloc(CXMA)
FXMA.__init__()
MXMA = _alloc(CXMA)
MXMA.__init__()
SXMA = _alloc(CXMA)
SXMA.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class UltimateOscillator(_MQL5Indicator):
    name = 'ultimate_oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'fastperiod': 7,
        'middleperiod': 14,
        'slowperiod': 28,
        'fastK': 4,
        'middleK': 2,
        'slowK': 1,
        'Shift': 0,  # Horizontal shift (in bars)
    }

