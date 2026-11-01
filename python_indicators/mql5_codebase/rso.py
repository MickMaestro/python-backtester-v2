"""RSO — converted from MQL5: MQL5 Indicators/RSO, Relative Strength Oscillator/RSO.mq5

Relative Strength Oscillator
Convertion of RS Index to Oscillator by Reza Anvari, Tehran
Copyright: 2009-2017, MetaQuotes Software Corp, Modification by Paran (2017); Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009-2017, MetaQuotes Software Corp, Modification by Paran (2017)', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2, 'indicator_minimum': -50.0, 'indicator_maximum': 50.0}, 'types': {1: 1, 2: 10}, 'colors': {1: [13434880], 2: [9498256, 255]}, 'widths': {1: 1, 2: 2}, 'styles': {}, 'labels': {}, 'levels': [-20.0, 0.0, 20.0], 'description': ['Relative Strength Oscillator', 'Convertion of RS Index to Oscillator by Reza Anvari, Tehran'], 'name': 'RSO', 'source': 'MQL5 Indicators/RSO, Relative Strength Oscillator/RSO.mq5', 'folder': 'RSO, Relative Strength Oscillator', 'inputs': [{'mql': 'InpPeriodRSO', 'py': 'InpPeriodRSO', 'param': 'InpPeriodRSO', 'type': 'int', 'default': 14, 'label': 'RSO Period', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodRSO = _input('InpPeriodRSO', 14)  # RSO Period
ExtRSOBuffer = Arr(0, 0.0)
ExtPosBuffer = Arr(0, 0.0)
ExtNegBuffer = Arr(0, 0.0)
ExtBufferBars = Arr(0, 0.0)
ExtBufferColors = Arr(0, 0.0)
ExtPeriodRSO = 0

def OnInit():
    global ExtPeriodRSO
    if InpPeriodRSO < 1:
        ExtPeriodRSO = 12
        Print('Incorrect value for input variable InpPeriodRSO = ', InpPeriodRSO, 'Indicator will use value = ', ExtPeriodRSO, 'for calculations.')
    else:
        ExtPeriodRSO = InpPeriodRSO
    SetIndexBuffer(0, ExtRSOBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtBufferBars, INDICATOR_DATA)
    SetIndexBuffer(2, ExtBufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, ExtPosBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ExtNegBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtPeriodRSO)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, ExtPeriodRSO)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSO(' + _str(ExtPeriodRSO) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'RSO(' + _str(ExtPeriodRSO) + ')')
    PlotIndexSetString(1, PLOT_LABEL, 'RSO Bars')

def OnCalculate(rates_total, prev_calculated, begin, price):
    i = 0
    diff = 0.0
    if rates_total <= ExtPeriodRSO:
        return 0
    pos = prev_calculated - 1
    if pos <= ExtPeriodRSO:
        ExtRSOBuffer[0] = 0.0
        ExtPosBuffer[0] = 0.0
        ExtNegBuffer[0] = 0.0
        SumP = 0.0
        SumN = 0.0
        i = 1
        for i in range(i, ExtPeriodRSO + 1):
            ExtRSOBuffer[i] = 0.0
            ExtPosBuffer[i] = 0.0
            ExtNegBuffer[i] = 0.0
            diff = price[i] - price[i - 1]
            SumP += (diff if (diff > 0) else 0)
            SumN += ((-diff) if (diff < 0) else 0)
        else:
            i = _range_end(i, ExtPeriodRSO + 1, 1)
        ExtPosBuffer[ExtPeriodRSO] = _fdiv(SumP, ExtPeriodRSO)
        ExtNegBuffer[ExtPeriodRSO] = _fdiv(SumN, ExtPeriodRSO)
        if ExtNegBuffer[ExtPeriodRSO] != 0.0:
            ExtRSOBuffer[ExtPeriodRSO] = 100.0 - _fdiv(100.0, 1.0 + _fdiv(ExtPosBuffer[ExtPeriodRSO], ExtNegBuffer[ExtPeriodRSO]))
        else:
            if ExtPosBuffer[ExtPeriodRSO] != 0.0:
                ExtRSOBuffer[ExtPeriodRSO] = 100.0
            else:
                ExtRSOBuffer[ExtPeriodRSO] = 50.0
        pos = ExtPeriodRSO + 1
    i = pos
    for i in range(i, rates_total):
        diff = price[i] - price[i - 1]
        ExtPosBuffer[i] = _fdiv((ExtPosBuffer[i - 1] * (ExtPeriodRSO - 1)) + (diff if (diff > 0.0) else 0.0), ExtPeriodRSO)
        ExtNegBuffer[i] = _fdiv((ExtNegBuffer[i - 1] * (ExtPeriodRSO - 1)) + ((-diff) if (diff < 0.0) else 0.0), ExtPeriodRSO)
        if ExtNegBuffer[i] != 0.0:
            ExtRSOBuffer[i] = 50.0 - _fdiv(100.0, 1 + _fdiv(ExtPosBuffer[i], ExtNegBuffer[i]))
        else:
            if ExtPosBuffer[i] != 0.0:
                ExtRSOBuffer[i] = 50.0
            else:
                ExtRSOBuffer[i] = 0.0
        ExtBufferBars[i] = 0.9 * ExtRSOBuffer[i]
        ExtBufferColors[i] = (0.0 if ((ExtRSOBuffer[i] - ExtRSOBuffer[i - 1]) >= 0) else 1.0)
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSO(_MQL5Indicator):
    name = 'RSO'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodRSO': 14,  # RSO Period
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }
    y_range = (-50.0, 50.0)

