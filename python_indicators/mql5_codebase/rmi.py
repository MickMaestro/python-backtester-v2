"""rmi — converted from MQL5: MQL5 Indicators/MA on RMI/rmi.mq5

Relative Momentum Index
Copyright: Copyright 2013, Rone.; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2013, Rone.', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1, 'indicator_minimum': 0.0, 'indicator_maximum': 100.0}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'RMI'}, 'levels': [30.0, 50.0, 70.0], 'description': ['Relative Momentum Index'], 'name': 'rmi', 'source': 'MQL5 Indicators/MA on RMI/rmi.mq5', 'folder': 'MA on RMI', 'inputs': [{'mql': 'InpRmiPeriod', 'py': 'InpRmiPeriod', 'param': 'InpRmiPeriod', 'type': 'ushort', 'default': 14, 'label': 'RMI Period', 'sinput': False}, {'mql': 'InpMomPeriod', 'py': 'InpMomPeriod', 'param': 'InpMomPeriod', 'type': 'ushort', 'default': 10, 'label': 'Momentum Period', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpRmiPeriod = _input('InpRmiPeriod', 14)  # RMI Period
InpMomPeriod = _input('InpMomPeriod', 10)  # Momentum Period
RMIBuffer = Arr(0, 0.0)
PosBuffer = Arr(0, 0.0)
NegBuffer = Arr(0, 0.0)
rmi_period = 0
mom_period = 0
min_required_bars = 0

def OnInit():
    global min_required_bars, mom_period, rmi_period
    if InpRmiPeriod < 1:
        rmi_period = 14
        printf('Incorrected input variable RMI Period = %d. Indicator will use value %d.', InpRmiPeriod, rmi_period)
    else:
        rmi_period = InpRmiPeriod
    if InpMomPeriod < 1:
        mom_period = 10
        printf('Incorrected input variable Momentum Period = %d. Indicator will use value %d.', InpMomPeriod, mom_period)
    else:
        mom_period = InpMomPeriod
    min_required_bars = rmi_period + mom_period + 1
    SetIndexBuffer(0, RMIBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, PosBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, NegBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_required_bars)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RMI(' + _str(rmi_period) + ', ' + _str(mom_period) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < min_required_bars:
        Print('Not enough bars for calculation')
        return 0
    start_bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        start_bar = min_required_bars
        ArrayInitialize(RMIBuffer, 0.0)
        ArrayInitialize(PosBuffer, 0.0)
        ArrayInitialize(NegBuffer, 0.0)
    else:
        start_bar = prev_calculated - 1
    for bar in range(start_bar, rates_total):
        diff = price[bar] - price[bar - mom_period]
        PosBuffer[bar] = _fdiv((PosBuffer[bar - 1] * (rmi_period - 1)) + (diff if (diff > 0.0) else 0.0), rmi_period)
        NegBuffer[bar] = _fdiv((NegBuffer[bar - 1] * (rmi_period - 1)) + ((-diff) if (diff < 0.0) else 0.0), rmi_period)
        if NegBuffer[bar] != 0.0:
            RMIBuffer[bar] = 100.0 - _fdiv(100.0, 1 + _fdiv(PosBuffer[bar], NegBuffer[bar]))
        else:
            RMIBuffer[bar] = 50.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Rmi(_MQL5Indicator):
    name = 'rmi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpRmiPeriod': 14,  # RMI Period
        'InpMomPeriod': 10,  # Momentum Period
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }
    y_range = (0.0, 100.0)

