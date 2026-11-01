"""Headley acceleration bands — converted from MQL5: MQL5 Indicators/Headley's acceleration bands/Headley acceleration bands.mq5

Price Headley's acceleration bands
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 1}, 'colors': {1: [14474460], 2: [11119017], 3: [11119017], 4: [11119017]}, 'widths': {2: 2, 3: 2}, 'styles': {4: 2}, 'labels': {1: 'fill', 2: 'Upper band', 3: 'Lower band', 4: 'Average'}, 'levels': [], 'description': ["Price Headley's acceleration bands"], 'name': 'Headley acceleration bands', 'source': "MQL5 Indicators/Headley's acceleration bands/Headley acceleration bands.mq5", 'folder': "Headley's acceleration bands", 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 30, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 30)  # Period
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
valu = Arr(0, 0.0)
vald = Arr(0, 0.0)
valm = Arr(0, 0.0)
workh = Arr(0, 0.0)
workl = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, valu, INDICATOR_DATA)
    SetIndexBuffer(3, vald, INDICATOR_DATA)
    SetIndexBuffer(4, valm, INDICATOR_DATA)
    SetIndexBuffer(5, workh, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, workl, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, "Headley's acceleration bands (" + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        workh[i] = high[i] * (1.0 + (2.0 * (_fdiv(high[i] - low[i], (high[i] + low[i]) / 2.0) * 1000.0) * 0.001))
        workl[i] = low[i] * (1.0 - (2.0 * (_fdiv(high[i] - low[i], (high[i] + low[i]) / 2.0) * 1000.0) * 0.001))
        valm[i] = 0.0
        valu[i] = 0.0
        vald[i] = 0.0
        k = 0
        while k < inpPeriod and (i - k) >= 0:
            valm[i] += close[i - k]
            valu[i] += workh[i - k]
            vald[i] += workl[i - k]
            k += 1
        valm[i] = valm[i] / inpPeriod
        valu[i] = valu[i] / inpPeriod
        vald[i] = vald[i] / inpPeriod
        fillu[i] = valu[i]
        filld[i] = vald[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HeadleyAccelerationBands(_MQL5Indicator):
    name = 'Headley acceleration bands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 30,  # Period
    }

