"""Choppiness index — converted from MQL5: MQL5 Indicators/Choppiness Index/Choppiness index.mq5

Choppiness index
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [3937500]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Choppiness index'}, 'levels': [], 'description': ['Choppiness index'], 'name': 'Choppiness index', 'source': 'MQL5 Indicators/Choppiness Index/Choppiness index.mq5', 'folder': 'Choppiness Index', 'inputs': [{'mql': 'inpChoPeriod', 'py': 'inpChoPeriod', 'param': 'inpChoPeriod', 'type': 'int', 'default': 14, 'label': 'Choppiness index period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpChoPeriod = _input('inpChoPeriod', 14)  # Choppiness index period
csi = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, csi, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Choppiness index (' + _str(inpChoPeriod) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _log = MathLog(inpChoPeriod) / 100.0
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        atrSum = 0.0
        maxHig = high[i]
        minLow = low[i]
        k = 0
        while k < inpChoPeriod and (i - k - 1) >= 0:
            atrSum += MathMax(high[i - k], close[i - k - 1]) - MathMin(low[i - k], close[i - k - 1])
            maxHig = MathMax(maxHig, MathMax(high[i - k], close[i - k - 1]))
            minLow = MathMin(minLow, MathMin(low[i - k], close[i - k - 1]))
            k += 1
        csi[i] = (_fdiv(MathLog(_fdiv(atrSum, maxHig - minLow)), _log) if (maxHig != minLow) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ChoppinessIndex(_MQL5Indicator):
    name = 'Choppiness index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpChoPeriod': 14,  # Choppiness index period
    }

