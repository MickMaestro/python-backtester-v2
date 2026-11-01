"""SimpleZZ — converted from MQL5: MQL5 Indicators/SimpleZZ/SimpleZZ.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 6}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'ZZ'}, 'levels': [], 'description': [], 'name': 'SimpleZZ', 'source': 'MQL5 Indicators/SimpleZZ/SimpleZZ.mq5', 'folder': 'SimpleZZ', 'inputs': [{'mql': 'InpMethodStep', 'py': 'InpMethodStep', 'param': 'InpMethodStep', 'type': 'int', 'default': 0, 'label': 'Step calculation method', 'sinput': False}, {'mql': 'InpStep', 'py': 'InpStep', 'param': 'InpStep', 'type': 'double', 'default': 100.0, 'label': 'Step size', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_METHOD_STEP
METHOD_STEP_POINTS = 0
METHOD_STEP_PERCENT = 1
_enum('ENUM_METHOD_STEP', {0: 'METHOD_STEP_POINTS', 1: 'METHOD_STEP_PERCENT'})

# ---- inputs and global variables
InpMethodStep = _input('InpMethodStep', METHOD_STEP_POINTS)  # Step calculation method
InpStep = _input('InpStep', 100.0)  # Step size
BufferMinPriceZZ = Arr(0, 0.0)
BufferMaxPriceZZ = Arr(0, 0.0)
BufferDirection = Arr(0, 0.0)
BufferMinBar = Arr(0, 0.0)
BufferMaxBar = Arr(0, 0.0)
step_pt = 0.0
step_pc = 0.0

def OnInit():
    global step_pc, step_pt
    if Point() == 0:
        Print('Error ', GetLastError(), '. The Point() of the symbol ', Symbol(), ' is zero.')
        return INIT_FAILED
    step_pt = (0 if (InpStep < 0) else (InpStep * Point()))
    step_pc = (0 if (InpStep < 0) else InpStep) / 100
    SetIndexBuffer(0, BufferMaxPriceZZ, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMinPriceZZ, INDICATOR_DATA)
    SetIndexBuffer(2, BufferDirection, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMinBar, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMaxBar, INDICATOR_CALCULATIONS)
    PlotIndexSetString(0, PLOT_LABEL, 'ZZ Upper;' + 'ZZ Lower;')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Simple ZigZag')
    ArraySetAsSeries(BufferMinPriceZZ, True)
    ArraySetAsSeries(BufferMaxPriceZZ, True)
    ArraySetAsSeries(BufferDirection, True)
    ArraySetAsSeries(BufferMinBar, True)
    ArraySetAsSeries(BufferMaxBar, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 3:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    total = rates_total - 2
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = total
        ArrayInitialize(BufferMinPriceZZ, EMPTY_VALUE)
        ArrayInitialize(BufferMaxPriceZZ, EMPTY_VALUE)
        ArrayInitialize(BufferDirection, EMPTY_VALUE)
        ArrayInitialize(BufferMinBar, EMPTY_VALUE)
        ArrayInitialize(BufferMaxBar, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        if i == total:
            BufferDirection[i] = 1.0
            BufferMinBar[i] = i
            BufferMaxBar[i] = i
            if close[i] > open[i]:
                BufferMinPriceZZ[i] = high[i]
                BufferMaxPriceZZ[i] = BufferMinPriceZZ[i]
            else:
                BufferMinPriceZZ[i] = low[i]
                BufferMaxPriceZZ[i] = BufferMinPriceZZ[i]
        else:
            BufferMinBar[i] = BufferMinBar[i + 1]
            BufferMaxBar[i] = BufferMaxBar[i + 1]
            BufferDirection[i] = BufferDirection[i + 1]
            BufferMinPriceZZ[i] = EMPTY_VALUE
            BufferMaxPriceZZ[i] = EMPTY_VALUE
            if close[i] < open[i]:
                Calculate(i, high[i], high, low)
                Calculate(i, low[i], high, low)
            else:
                Calculate(i, low[i], high, low)
                Calculate(i, high[i], high, low)
    return rates_total

def CalculateUp(index, price, high):
    last_bar = _int(BufferMaxBar[index])
    if BufferMaxPriceZZ[last_bar] == EMPTY_VALUE:
        BufferMaxPriceZZ[last_bar] = high[last_bar]
    if price > BufferMaxPriceZZ[last_bar]:
        BufferMaxPriceZZ[last_bar] = EMPTY_VALUE
        BufferMaxPriceZZ[index] = price
        BufferMaxBar[index] = index
        last_bar = index
    if ((price + step_pt) < BufferMaxPriceZZ[last_bar] and InpMethodStep == METHOD_STEP_POINTS) or ((price * (1 + (step_pc / 100))) < BufferMaxPriceZZ[last_bar] and InpMethodStep == METHOD_STEP_PERCENT):
        BufferDirection[index] = -1.0
        BufferMinPriceZZ[index] = price
        BufferMinBar[index] = index
    return

def CalculateDn(index, price, low):
    last_bar = _int(BufferMinBar[index])
    if BufferMinPriceZZ[last_bar] == EMPTY_VALUE:
        BufferMinPriceZZ[last_bar] = low[last_bar]
    if price < BufferMinPriceZZ[last_bar]:
        BufferMinPriceZZ[last_bar] = EMPTY_VALUE
        BufferMinPriceZZ[index] = price
        BufferMinBar[index] = index
        last_bar = index
    if ((price - step_pt) > BufferMinPriceZZ[last_bar] and InpMethodStep == METHOD_STEP_POINTS) or ((price * (1 - (step_pc / 100))) > BufferMinPriceZZ[last_bar] and InpMethodStep == METHOD_STEP_PERCENT):
        BufferDirection[index] = 1.0
        BufferMaxPriceZZ[index] = price
        BufferMaxBar[index] = index
    return

def Calculate(index, price, high, low):
    if BufferDirection[index] == 1:
        CalculateUp(index, price, high)
    else:
        CalculateDn(index, price, low)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SimpleZZ(_MQL5Indicator):
    name = 'SimpleZZ'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpMethodStep': _Choice({0: 'Step in pips', 1: 'Step in percent'}, default=0),  # Step calculation method
        'InpStep': 100.0,  # Step size
    }

