"""Linear_Regression_Slope — converted from MQL5: MQL5 Indicators/Linear_Regression_Slope/Linear_Regression_Slope.mq5

Linear regression slope oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11829830]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'LReg Slope'}, 'levels': [], 'description': ['Linear regression slope oscillator'], 'name': 'Linear_Regression_Slope', 'source': 'MQL5 Indicators/Linear_Regression_Slope/Linear_Regression_Slope.mq5', 'folder': 'Linear_Regression_Slope', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
BufferLRS = Arr(0, 0.0)
period = 0

def OnInit():
    global period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferLRS, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Linear regression slope (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferLRS, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferLRS, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        ii = 0.0
        y = 0.0
        xy = 0.0
        x = 0.0
        x2 = 0.0
        for j in range(i + period, i - 1, -1):
            ii += 1
            y += close[j]
            xy += close[j] * ii
            x += ii
            x2 += ii * ii
        c = (x2 * ii) - (x * x)
        BufferLRS[i] = (_fdiv((xy * ii) - (x * y), c) if (c != 0) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LinearRegressionSlope(_MQL5Indicator):
    name = 'Linear_Regression_Slope'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
    }

