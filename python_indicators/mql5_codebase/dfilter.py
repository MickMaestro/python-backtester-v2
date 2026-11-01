"""dfilter — converted from MQL5: MQL5 Indicators/Universal digital filter/dfilter.mq5

Copyright: 2005, Sergey Ilyukhin, Moscow; Link: http://fx.qrz.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Imports DLL/library functions: DF.dll (not available).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2005, Sergey Ilyukhin, Moscow', 'link': 'http://fx.qrz.ru/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [13828244]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'DFilter'}, 'levels': [], 'description': [], 'name': 'dfilter', 'source': 'MQL5 Indicators/Universal digital filter/dfilter.mq5', 'folder': 'Universal digital filter', 'inputs': [{'mql': 'FType', 'py': 'FType', 'param': 'FType', 'type': 'int', 'default': 0, 'label': 'Filter type', 'sinput': False}, {'mql': 'P1', 'py': 'P1', 'param': 'P1', 'type': 'int', 'default': 28, 'label': 'Cut-off period 1, bars', 'sinput': False}, {'mql': 'D1', 'py': 'D1', 'param': 'D1', 'type': 'int', 'default': 19, 'label': 'Transient process cut-off period 1, bars', 'sinput': False}, {'mql': 'A1', 'py': 'A1', 'param': 'A1', 'type': 'int', 'default': 40, 'label': 'Attenuation in a rejection band 1, dB', 'sinput': False}, {'mql': 'P2', 'py': 'P2', 'param': 'P2', 'type': 'int', 'default': 0, 'label': 'Cut-off period 2, bars', 'sinput': False}, {'mql': 'D2', 'py': 'D2', 'param': 'D2', 'type': 'int', 'default': 0, 'label': 'Transient process cut-off period 2, bars', 'sinput': False}, {'mql': 'A2', 'py': 'A2', 'param': 'A2', 'type': 'int', 'default': 0, 'label': 'Attenuation in a rejection band 2, dB', 'sinput': False}, {'mql': 'Delay', 'py': 'Delay', 'param': 'Delay', 'type': 'int', 'default': 0, 'label': 'Delay, bars', 'sinput': False}, {'mql': 'Ripple', 'py': 'Ripple', 'param': 'Ripple', 'type': 'double', 'default': 0.08, 'label': 'Pulsations in a pass band, dB', 'sinput': False}, {'mql': 'FILTERShift', 'py': 'FILTERShift', 'param': 'FILTERShift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of moving average in bars', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': ['DF.dll'], 'libraries': []}

# enum FType_
LPF = 0
HPE = 1
BPF = 2
SPF = 3
_enum('FType_', {0: 'LPF', 1: 'HPE', 2: 'BPF', 3: 'SPF'})

# ---- inputs and global variables
FType = _input('FType', LPF)  # Filter type
P1 = _input('P1', 28)  # Cut-off period 1, bars
D1 = _input('D1', 19)  # Transient process cut-off period 1, bars
A1 = _input('A1', 40)  # Attenuation in a rejection band 1, dB
P2 = _input('P2', 0)  # Cut-off period 2, bars
D2 = _input('D2', 0)  # Transient process cut-off period 2, bars
A2 = _input('A2', 0)  # Attenuation in a rejection band 2, dB
Delay = _input('Delay', 0)  # Delay, bars
Ripple = _input('Ripple', 0.08)  # Pulsations in a pass band, dB
FILTERShift = _input('FILTERShift', 0)  # Horizontal shift of moving average in bars
FILTERPeriod = 0
ExtLineBuffer = Arr(0, 0.0)
FILTERTable = Arr(0, 0.0)

def DigitalFilter(*args):
    raise NotImplementedError('DLL/library function DigitalFilter from DF.dll')

def OnInit():
    global FILTERPeriod
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, FILTERShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, FILTERPeriod)
    shortname = Box("")
    StringConcatenate(shortname, 'FILTER(', FILTERShift, ')')
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    Array = Arr(1500, 0.0, dyn=False)
    FILTERPeriod = DigitalFilter(FType, P1, D1, A1, P2, D2, A2, Ripple, Delay, Array)
    if FILTERPeriod <= 0:
        Print('Input parameters are incorrect. Indicator cannot be launched!')
        return
    ArrayCopy(FILTERTable, Array, 0, 0, FILTERPeriod)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (FILTERPeriod - 1 + begin):
        return 0
    first = 0
    bar = 0
    iii = 0
    FILTER = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = FILTERPeriod - 1 + begin
        if begin > 0:
            PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, begin + FILTERPeriod)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        FILTER = 0.0
        iii = 0
        for iii in range(iii, FILTERPeriod):
            FILTER += FILTERTable[iii] * price[bar - iii]
        else:
            iii = _range_end(iii, FILTERPeriod, 1)
        ExtLineBuffer[bar] = FILTER
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dfilter(_MQL5Indicator):
    name = 'dfilter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FType': _Choice({0: 'LPF (FATL/SATL/KGLP)', 1: 'HPF (KGHP)', 2: 'band-pass (RBCI/KGBP)', 3: 'rejection (KGBS)'}, default=0),  # Filter type
        'P1': 28,  # Cut-off period 1, bars
        'D1': 19,  # Transient process cut-off period 1, bars
        'A1': 40,  # Attenuation in a rejection band 1, dB
        'P2': 0,  # Cut-off period 2, bars
        'D2': 0,  # Transient process cut-off period 2, bars
        'A2': 0,  # Attenuation in a rejection band 2, dB
        'Delay': 0,  # Delay, bars
        'Ripple': 0.08,  # Pulsations in a pass band, dB
        'FILTERShift': 0,  # Horizontal shift of moving average in bars
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

