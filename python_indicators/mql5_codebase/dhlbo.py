"""DHLBO — converted from MQL5: MQL5 Indicators/DHLBO/DHLBO.mq5

Dynamic High/Low Band Overlay indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'DHLBO Top', 2: 'DHLBO Bottom'}, 'levels': [], 'description': ['Dynamic High/Low Band Overlay indicator'], 'name': 'DHLBO', 'source': 'MQL5 Indicators/DHLBO/DHLBO.mq5', 'folder': 'DHLBO', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpStep', 'py': 'InpStep', 'param': 'InpStep', 'type': 'double', 'default': 0.7071, 'label': 'Expansion', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpStep = _input('InpStep', 0.7071)  # Expansion
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
step = 0.0
period = 0

def OnInit():
    global period, step
    period = (1 if (InpPeriod < 1) else InpPeriod)
    step = InpStep
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'DHLBO (' + _str(period) + ',' + DoubleToString(step, 4) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        bh = Highest(period, i)
        bl = Lowest(period, i)
        if bh == WRONG_VALUE or bl == WRONG_VALUE:
            continue
        max_ = high[bh]
        min_ = low[bl]
        BufferUP[i] = min_ + ((max_ - min_) * step)
        BufferDN[i] = max_ - ((max_ - min_) * step)
    return rates_total

def Highest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return ((ArrayMaximum(array) + start) if (CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)

def Lowest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return ((ArrayMinimum(array) + start) if (CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)
    return WRONG_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DHLBO(_MQL5Indicator):
    name = 'DHLBO'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpStep': 0.7071,  # Expansion
    }

