"""AsymmetricFractals — converted from MQL5: MQL5 Indicators/AsymmetricFractals/AsymmetricFractals.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Fractal Up', 2: 'Fractal Down'}, 'levels': [], 'description': [], 'name': 'AsymmetricFractals', 'source': 'MQL5 Indicators/AsymmetricFractals/AsymmetricFractals.mq5', 'folder': 'AsymmetricFractals', 'inputs': [{'mql': 'InpNumBefore', 'py': 'InpNumBefore', 'param': 'InpNumBefore', 'type': 'uint', 'default': 4, 'label': 'Number of bars on the left', 'sinput': False}, {'mql': 'InpNumAfter', 'py': 'InpNumAfter', 'param': 'InpNumAfter', 'type': 'uint', 'default': 2, 'label': 'Number of bars on the right', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpNumBefore = _input('InpNumBefore', 4)  # Number of bars on the left
InpNumAfter = _input('InpNumAfter', 2)  # Number of bars on the right
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
num_before = 0
num_after = 0

def OnInit():
    global num_after, num_before
    num_before = (1 if (InpNumBefore < 1) else InpNumBefore)
    num_after = (1 if (InpNumAfter < 1) else InpNumAfter)
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 119)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    IndicatorSetString(INDICATOR_SHORTNAME, 'AsymmetricFractals(' + _str(num_before) + ',' + _str(num_after) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    max_ = num_before + num_after
    if rates_total < max_:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - max_ - 2
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    for i in range(limit, 0 - 1, -1):
        fractal_up = True
        fractal_dn = True
        for n in range(1, num_before + 1):
            if high[i + num_after + n] >= high[i + num_after]:
                fractal_up = False
            if low[i + num_after + n] <= low[i + num_after]:
                fractal_dn = False
        for n in range(1, num_after + 1):
            if high[i + num_after - n] >= high[i + num_after]:
                fractal_up = False
            if low[i + num_after - n] <= low[i + num_after]:
                fractal_dn = False
        if fractal_up:
            BufferUP[i + num_after] = high[i + num_after]
        else:
            BufferUP[i + num_after] = EMPTY_VALUE
        if fractal_dn:
            BufferDN[i + num_after] = low[i + num_after]
        else:
            BufferDN[i + num_after] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AsymmetricFractals(_MQL5Indicator):
    name = 'AsymmetricFractals'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpNumBefore': 4,  # Number of bars on the left
        'InpNumAfter': 2,  # Number of bars on the right
    }

