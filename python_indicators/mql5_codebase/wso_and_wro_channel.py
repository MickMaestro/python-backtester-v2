"""Wso and Wro channel — converted from MQL5: MQL5 Indicators/WSO & WRO Channel/Wso and Wro channel.mq5

Wso & Wro channel
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [14474460, 14474460], 2: [255], 3: [16760576]}, 'widths': {2: 1, 3: 1}, 'styles': {}, 'labels': {1: 'Wso & Wro zone', 2: 'Wso', 3: 'Wro'}, 'levels': [], 'description': ['Wso & Wro channel'], 'name': 'Wso and Wro channel', 'source': 'MQL5 Indicators/WSO & WRO Channel/Wso and Wro channel.mq5', 'folder': 'WSO & WRO Channel', 'inputs': [{'mql': 'inpWsoWroPeriod', 'py': 'inpWsoWroPeriod', 'param': 'inpWsoWroPeriod', 'type': 'int', 'default': 9, 'label': 'Wso & Wro period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpWsoWroPeriod = _input('inpWsoWroPeriod', 9)  # Wso & Wro period
wso = Arr(0, 0.0)
wro = Arr(0, 0.0)
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
wrk = Arr(0, 0.0, dims=(12,))

def OnInit():
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, wso, INDICATOR_DATA)
    SetIndexBuffer(3, wro, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Wso & Wro channel(' + _str(inpWsoWroPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if ArrayRange(wrk, 0) != rates_total:
        ArrayResize(wrk, rates_total)
    center = _idiv(inpWsoWroPeriod - 1, 2)
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        if i == 0:
            for k in range(0, 6):
                wrk[i][k] = low[i]
                wrk[i][k + 6] = high[i]
            i += 1
            continue
        _start = MathMax(i - inpWsoWroPeriod + 1, 0)
        lowest = i - ArrayMinimum(low, _start, inpWsoWroPeriod)
        highest = i - ArrayMaximum(high, _start, inpWsoWroPeriod)
        for k in range(0, 12):
            wrk[i][k] = wrk[i - 1][k]
        if lowest == center:
            wrk[i][0] = low[i - center]
            wrk[i][1] = wrk[i - 1][0]
            wrk[i][2] = wrk[i - 1][1]
            wrk[i][3] = wrk[i - 1][2]
            wrk[i][4] = wrk[i - 1][3]
            wrk[i][5] = wrk[i - 1][4]
        if highest == center:
            wrk[i][6] = high[i - center]
            wrk[i][7] = wrk[i - 1][6]
            wrk[i][8] = wrk[i - 1][7]
            wrk[i][9] = wrk[i - 1][8]
            wrk[i][10] = wrk[i - 1][9]
            wrk[i][11] = wrk[i - 1][10]
        wso[i] = wrk[i][0]
        wro[i] = wrk[i][6]
        filld[i] = wso[i]
        fillu[i] = wro[i]
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WsoAndWroChannel(_MQL5Indicator):
    name = 'Wso and Wro channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpWsoWroPeriod': 9,  # Wso & Wro period
    }

