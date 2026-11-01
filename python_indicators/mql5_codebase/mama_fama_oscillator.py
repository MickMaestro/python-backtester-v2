"""Mama + fama oscillator — converted from MQL5: MQL5 Indicators/MAMA + FAMA Oscillator/Mama + fama oscillator.mq5

Mama - fama oscillator
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 10, 2: 8}, 'colors': {1: [11119017, 6333684, 16748574], 2: [11119017, 6333684, 16748574]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Mama - fama histogram', 2: 'Mama - fama line'}, 'levels': [], 'description': ['Mama - fama oscillator'], 'name': 'Mama + fama oscillator', 'source': 'MQL5 Indicators/MAMA + FAMA Oscillator/Mama + fama oscillator.mq5', 'folder': 'MAMA + FAMA Oscillator', 'inputs': [{'mql': 'inpFastLimit', 'py': 'inpFastLimit', 'param': 'inpFastLimit', 'type': 'double', 'default': 0.5, 'label': 'Fast limit', 'sinput': False}, {'mql': 'inpSlowLimit', 'py': 'inpSlowLimit', 'param': 'inpSlowLimit', 'type': 'double', 'default': 0.05, 'label': 'Slow limit', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpFastLimit = _input('inpFastLimit', 0.5)  # Fast limit
inpSlowLimit = _input('inpSlowLimit', 0.05)  # Slow limit
inpPrice = _input('inpPrice', PRICE_MEDIAN)  # Price
valf = Arr(0, 0.0)
valfc = Arr(0, 0.0)
valm = Arr(0, 0.0)
valmc = Arr(0, 0.0)
workMama = Arr(0, 0.0, dims=(16,))

def OnInit():
    SetIndexBuffer(0, valf, INDICATOR_DATA)
    SetIndexBuffer(1, valfc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, valm, INDICATOR_DATA)
    SetIndexBuffer(3, valmc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Mama - fama oscillator (' + _str(inpFastLimit) + ',' + _str(inpSlowLimit) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _fama = Box(0.0)
        _mama = iMama(getPrice(inpPrice, open, close, high, low, i, rates_total), inpFastLimit, inpSlowLimit, _fama, i, rates_total)
        valm[i] = _mama - _fama.v
        valf[i] = valm[i]
        valfc[i] = (1 if (valm[i] < 0) else 2 if (valm[i] > 0) else valfc[i - 1] if (i > 0) else 0)
        valmc[i] = valfc[i]
        i += 1
    return i

def iMama(price, fastLimit, slowLimit, retFama, r, bars):
    if ArrayRange(workMama, 0) != bars:
        ArrayResize(workMama, bars)
    workMama[r][0] = price
    workMama[r][1] = ((((4.0 * workMama[r][0]) + (3.0 * workMama[r - 1][0]) + (2.0 * workMama[r - 2][0]) + workMama[r - 3][0]) / 10.0) if (r > 3) else price)
    workMama[r][2] = ((((0.0962 * workMama[r][1]) + (0.5769 * workMama[r - 2][1]) - (0.5769 * workMama[r - 4][1]) - (0.0962 * workMama[r - 6][1])) * ((0.075 * workMama[r - 1][3]) + 0.54)) if (r > 5) else workMama[r][1])
    workMama[r][5] = ((((0.0962 * workMama[r][2]) + (0.5769 * workMama[r - 2][2]) - (0.5769 * workMama[r - 4][2]) - (0.0962 * workMama[r - 6][2])) * ((0.075 * workMama[r - 1][3]) + 0.54)) if (r > 5) else workMama[r][2])
    workMama[r][6] = (workMama[r - 3][2] if (r > 2) else workMama[r][2])
    workMama[r][7] = ((((0.0962 * workMama[r][6]) + (0.5769 * workMama[r - 2][6]) - (0.5769 * workMama[r - 4][6]) - (0.0962 * workMama[r - 6][6])) * ((0.075 * workMama[r - 1][3]) + 0.54)) if (r > 5) else workMama[r][6])
    workMama[r][8] = ((((0.0962 * workMama[r][5]) + (0.5769 * workMama[r - 2][5]) - (0.5769 * workMama[r - 4][5]) - (0.0962 * workMama[r - 6][5])) * ((0.075 * workMama[r - 1][3]) + 0.54)) if (r > 5) else workMama[r][5])
    workMama[r][10] = (workMama[r][6] if (r == 0) else ((0.2 * (workMama[r][6] - workMama[r][8])) + (0.8 * workMama[r - 1][10])))
    workMama[r][9] = (workMama[r][5] if (r == 0) else ((0.2 * (workMama[r][5] + workMama[r][7])) + (0.8 * workMama[r - 1][9])))
    workMama[r][11] = (workMama[r][10] if (r == 0) else ((0.2 * ((workMama[r][10] * workMama[r - 1][10]) + (workMama[r][9] * workMama[r - 1][9]))) + (0.8 * workMama[r - 1][11])))
    workMama[r][12] = (workMama[r][10] if (r == 0) else ((0.2 * ((workMama[r][10] * workMama[r - 1][9]) - (workMama[r][9] * workMama[r - 1][10]))) + (0.8 * workMama[r - 1][12])))
    if workMama[r][11] != 0 and workMama[r][12] != 0:
        workMama[r][3] = _fdiv(360.0, MathArctan(_fdiv(workMama[r][12], workMama[r][11])) * (180.0 / M_PI))
    workMama[r][3] = (workMama[r][3] if (r == 0) else MathMin(workMama[r][3], 1.5 * workMama[r - 1][3]))
    workMama[r][3] = (workMama[r][3] if (r == 0) else MathMax(workMama[r][3], 0.67 * workMama[r - 1][3]))
    workMama[r][3] = MathMin(MathMax(workMama[r][3], 6), 50)
    workMama[r][3] = (workMama[r][3] if (r == 0) else ((0.2 * workMama[r][3]) + (0.8 * workMama[r - 1][3])))
    if workMama[r][6] != 0:
        workMama[r][4] = MathArctan(_fdiv(workMama[r][5], workMama[r][6])) * (180.0 / M_PI)
    DeltaPhase = (0 if (r == 0) else MathMax(workMama[r - 1][4] - workMama[r][4], 1))
    Alpha = (MathMax(MathMin(_fdiv(fastLimit, DeltaPhase), fastLimit), slowLimit) if (DeltaPhase != 0) else 1)
    workMama[r][13] = Alpha
    workMama[r][14] = (price if (r == 0) else ((workMama[r][13] * workMama[r][0]) + ((1.0 - workMama[r][13]) * workMama[r - 1][14])))
    workMama[r][15] = (price if (r == 0) else ((0.5 * workMama[r][13] * workMama[r][14]) + ((1.0 - (0.5 * workMama[r][13])) * workMama[r - 1][15])))
    retFama.v = workMama[r][15]
    return workMama[r][14]

def getPrice(tprice, open, close, high, low, i, _bars):
    if i >= 0:
        _sw1 = tprice
        if _sw1 == PRICE_CLOSE:
            return close[i]
        elif _sw1 == PRICE_OPEN:
            return open[i]
        elif _sw1 == PRICE_HIGH:
            return high[i]
        elif _sw1 == PRICE_LOW:
            return low[i]
        elif _sw1 == PRICE_MEDIAN:
            return (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            return (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MamaFamaOscillator(_MQL5Indicator):
    name = 'Mama + fama oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFastLimit': 0.5,  # Fast limit
        'inpSlowLimit': 0.05,  # Slow limit
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
    }

