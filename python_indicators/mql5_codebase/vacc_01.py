"""vacc_01 — converted from MQL5: MQL5 Indicators/Smoothed Accelerator/vacc_01.mq5

VAcc

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {}, 'styles': {}, 'labels': {1: 'VAcc'}, 'levels': [0.0], 'description': ['VAcc'], 'name': 'vacc_01', 'source': 'MQL5 Indicators/Smoothed Accelerator/vacc_01.mq5', 'folder': 'Smoothed Accelerator', 'inputs': [{'mql': 'InpAccPeriod', 'py': 'InpAccPeriod', 'param': 'InpAccPeriod', 'type': 'int', 'default': 3, 'label': 'Acc period (1...100)', 'sinput': False}, {'mql': 'InpMAPeriod', 'py': 'InpMAPeriod', 'param': 'InpMAPeriod', 'type': 'int', 'default': 5, 'label': 'MA period  (2...100)', 'sinput': False}, {'mql': 'InpNHistory', 'py': 'InpNHistory', 'param': 'InpNHistory', 'type': 'int', 'default': 255, 'label': 'N History  (32...1024)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpAccPeriod = _input('InpAccPeriod', 3)  # Acc period (1...100)
InpMAPeriod = _input('InpMAPeriod', 5)  # MA period  (2...100)
InpNHistory = _input('InpNHistory', 255)  # N History  (32...1024)
ExtOutBuffer = Arr(0, 0.0)
ExtPeriodAcc = 0
ExtPeriodMA = 0
ExtNHistory = 0
P1 = 0.0
P2 = 0.0

def OnInit():
    global ExtNHistory, ExtPeriodAcc, ExtPeriodMA, P1, P2
    if InpAccPeriod < 1 or InpAccPeriod > 100:
        ExtPeriodAcc = 3
        printf('Incorrect input parameter InpAccPeriod = %d. Indicator will use value %d for calculations.', InpAccPeriod, ExtPeriodAcc)
    else:
        ExtPeriodAcc = InpAccPeriod
    if InpMAPeriod < 2 or InpMAPeriod > 100:
        ExtPeriodMA = 3
        printf('Incorrect input parameter InpMAPeriod = %d. Indicator will use value %d for calculations.', InpMAPeriod, ExtPeriodMA)
    else:
        ExtPeriodMA = InpMAPeriod
    P1 = _fdiv(2.0, ExtPeriodMA + 1)
    P2 = 1.0 - P1
    if InpNHistory < 32 or InpNHistory > 1024:
        ExtNHistory = 255
        printf('Incorrect input parameter InpNHistory = %d. Indicator will use value %d for calculations.', InpNHistory, ExtNHistory)
    else:
        ExtNHistory = InpNHistory
    SetIndexBuffer(0, ExtOutBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtOutBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'VAcc(' + _str(ExtPeriodAcc) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    PlotIndexSetString(0, PLOT_LABEL, short_name)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    ArraySetAsSeries(Close, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Bars(Symbol(), 0) - ExtNHistory)
    ExtOutBuffer[ExtNHistory + 1] = 0.0
    i = ExtNHistory
    for i in range(i, 0 - 1, -1):
        ExtOutBuffer[i] = (MathLog(_fdiv(Close[i], Close[i + ExtPeriodAcc])) * P1) + (ExtOutBuffer[i + 1] * P2)
    else:
        i = _range_end(i, 0 - 1, -1)
    i = 1
    for i in range(i, ExtNHistory):
        ExtOutBuffer[i] = (ExtOutBuffer[i] * P1) + (ExtOutBuffer[i - 1] * P2)
    else:
        i = _range_end(i, ExtNHistory, 1)
    i = ExtNHistory - 1
    for i in range(i, 0 - 1, -1):
        ExtOutBuffer[i] = (ExtOutBuffer[i] * P1) + (ExtOutBuffer[i + 1] * P2)
    else:
        i = _range_end(i, 0 - 1, -1)
    i = 1
    for i in range(i, ExtNHistory):
        ExtOutBuffer[i] = (ExtOutBuffer[i] * P1) + (ExtOutBuffer[i - 1] * P2)
    else:
        i = _range_end(i, ExtNHistory, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Vacc01(_MQL5Indicator):
    name = 'vacc_01'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpAccPeriod': 3,  # Acc period (1...100)
        'InpMAPeriod': 5,  # MA period  (2...100)
        'InpNHistory': 255,  # N History  (32...1024)
    }

