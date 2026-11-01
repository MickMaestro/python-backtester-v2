"""SRsi — converted from MQL5: MQL5 Indicators/Sell Relative Strengt Index/SRsi.mq5

Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [65535, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'SRsi'}, 'levels': [], 'description': [], 'name': 'SRsi', 'source': 'MQL5 Indicators/Sell Relative Strengt Index/SRsi.mq5', 'folder': 'Sell Relative Strengt Index', 'inputs': [{'mql': 'inpRsiPeriod', 'py': 'inpRsiPeriod', 'param': 'inpRsiPeriod', 'type': 'int', 'default': 20, 'label': 'RSI period', 'sinput': False}, {'mql': 'inpLevels', 'py': 'inpLevels', 'param': 'inpLevels', 'type': 'double', 'default': 0.38, 'label': 'Levels', 'sinput': False}, {'mql': 'inpNLevels', 'py': 'inpNLevels', 'param': 'inpNLevels', 'type': 'double', 'default': 0.05, 'label': 'Neutral zone', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRsiPeriod = _input('inpRsiPeriod', 20)  # RSI period
inpLevels = _input('inpLevels', 0.38)  # Levels
inpNLevels = _input('inpNLevels', 0.05)  # Neutral zone
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
srsiv = Arr(0, 0.0)
srsis = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, srsiv, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, srsis, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_LEVELS, 4)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, inpLevels)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, -inpLevels)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, inpNLevels)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, -inpNLevels)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SRsi (' + _str(inpRsiPeriod) + ',' + _str(inpNLevels) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        srsiv[i] = (_fdiv(close[i] - open[i], high[i] - low[i]) if (high[i] != low[i]) else 0)
        if i > inpRsiPeriod:
            srsis[i] = srsis[i - 1] - srsiv[i - inpRsiPeriod] + srsiv[i]
        else:
            srsis[i] = srsiv[i]
            k = 1
            while k < inpRsiPeriod and i >= k:
                srsis[i] += srsiv[i - k]
                k += 1
        val[i] = srsis[i] / inpRsiPeriod
        valc[i] = (1 if (val[i] > inpNLevels) else 2 if (val[i] < (-inpNLevels)) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SRsi(_MQL5Indicator):
    name = 'SRsi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRsiPeriod': 20,  # RSI period
        'inpLevels': 0.38,  # Levels
        'inpNLevels': 0.05,  # Neutral zone
    }

