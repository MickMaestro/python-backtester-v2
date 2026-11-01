"""Trend scalp — converted from MQL5: MQL5 Indicators/Trend Scalp/Trend scalp.mq5

Trend scalp
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 8}, 'colors': {1: [16760576, 6333684], 2: [11119017], 3: [11119017, 16748574, 17919]}, 'widths': {2: 0, 3: 2}, 'styles': {}, 'labels': {1: 'Filling', 2: 'Trend scalp levels'}, 'levels': [], 'description': ['Trend scalp'], 'name': 'Trend scalp', 'source': 'MQL5 Indicators/Trend Scalp/Trend scalp.mq5', 'folder': 'Trend Scalp', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 15, 'label': 'Period', 'sinput': False}, {'mql': 'inpT3Period', 'py': 'inpT3Period', 'param': 'inpT3Period', 'type': 'int', 'default': 5, 'label': 'T3 period', 'sinput': False}, {'mql': 'inpT3Hot', 'py': 'inpT3Hot', 'param': 'inpT3Hot', 'type': 'double', 'default': 0.7, 'label': 'T3 hot', 'sinput': False}, {'mql': 'inpT3Type', 'py': 'inpT3Type', 'param': 'inpT3Type', 'type': 'int', 'default': 1, 'label': 'T3 type', 'sinput': False}, {'mql': 'inpLevels', 'py': 'inpLevels', 'param': 'inpLevels', 'type': 'double', 'default': 100.0, 'label': 'Levels at +- (nnn)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enT3Type
t3_tillson = 0
t3_fulksmat = 1
_enum('enT3Type', {0: 't3_tillson', 1: 't3_fulksmat'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 15)  # Period
inpT3Period = _input('inpT3Period', 5)  # T3 period
inpT3Hot = _input('inpT3Hot', 0.7)  # T3 hot
inpT3Type = _input('inpT3Type', t3_fulksmat)  # T3 type
inpLevels = _input('inpLevels', 100.0)  # Levels at +- (nnn)
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
lev = Arr(0, 0.0)
fup = Arr(0, 0.0)
fdn = Arr(0, 0.0)
workT3 = Arr(0, 0.0, dims=(6,))
workT3Coeffs = Arr(0, 0.0, dims=(6,))

def OnInit():
    SetIndexBuffer(0, fup, INDICATOR_DATA)
    SetIndexBuffer(1, fdn, INDICATOR_DATA)
    SetIndexBuffer(2, lev, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend scalp (' + _str(inpPeriod) + ',' + _str(inpT3Period) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _start = MathMax(i - inpPeriod, 0)
        HighestHighRecent = high[i]
        HighestHighOlder = high[ArrayMaximum(high, _start, inpPeriod)]
        LowestLowRecent = low[i]
        LowestLowOlder = low[ArrayMinimum(low, _start, inpPeriod)]
        BuyPower = HighestHighRecent - LowestLowOlder
        SellPower = HighestHighOlder - LowestLowRecent
        ttf = (_fdiv(100 * (BuyPower - SellPower), 0.5 * (BuyPower + SellPower)) if ((BuyPower + SellPower) != 0) else 0)
        val[i] = iT3(ttf, inpT3Period, inpT3Hot, inpT3Type == t3_tillson, i, rates_total)
        valc[i] = (1 if (val[i] > inpLevels) else 2 if (val[i] < (-inpLevels)) else 0)
        lev[i] = (inpLevels if (val[i] > 0) else (-inpLevels) if (val[i] < 0) else 0)
        fup[i] = val[i]
        fdn[i] = (MathMin(val[i], inpLevels) if (val[i] > 0) else MathMax(val[i], -inpLevels))
        i += 1
    return i

def iT3(price, period, hot, original, r, bars, instanceNo=0):
    if ArrayRange(workT3, 0) != bars:
        ArrayResize(workT3, bars)
    if ArrayRange(workT3Coeffs, 0) < (instanceNo + 1):
        ArrayResize(workT3Coeffs, instanceNo + 1)
    if workT3Coeffs[instanceNo][0] != period:
        workT3Coeffs[instanceNo][0] = period
        workT3Coeffs[instanceNo][1] = (-hot) * hot * hot
        workT3Coeffs[instanceNo][2] = (3 * hot * hot) + (3 * hot * hot * hot)
        workT3Coeffs[instanceNo][3] = (-6 * hot * hot) - (3 * hot) - (3 * hot * hot * hot)
        workT3Coeffs[instanceNo][4] = 1 + (3 * hot) + (hot * hot * hot) + (3 * hot * hot)
        if original:
            workT3Coeffs[instanceNo][5] = _fdiv(2.0, 1.0 + period)
        else:
            workT3Coeffs[instanceNo][5] = _fdiv(2.0, 2.0 + ((period - 1.0) / 2.0))
    buffer = instanceNo * 6
    for k in range(0, 6):
        workT3[r][k + buffer] = (workT3[r - 1][k + buffer] if (r > 0) else price)
    if r > 0 and period > 1:
        workT3[r][0 + buffer] = workT3[r - 1][0 + buffer] + (workT3Coeffs[instanceNo][5] * (price - workT3[r - 1][0 + buffer]))
        workT3[r][1 + buffer] = workT3[r - 1][1 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][0 + buffer] - workT3[r - 1][1 + buffer]))
        workT3[r][2 + buffer] = workT3[r - 1][2 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][1 + buffer] - workT3[r - 1][2 + buffer]))
        workT3[r][3 + buffer] = workT3[r - 1][3 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][2 + buffer] - workT3[r - 1][3 + buffer]))
        workT3[r][4 + buffer] = workT3[r - 1][4 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][3 + buffer] - workT3[r - 1][4 + buffer]))
        workT3[r][5 + buffer] = workT3[r - 1][5 + buffer] + (workT3Coeffs[instanceNo][5] * (workT3[r][4 + buffer] - workT3[r - 1][5 + buffer]))
    return (workT3Coeffs[instanceNo][1] * workT3[r][5 + buffer]) + (workT3Coeffs[instanceNo][2] * workT3[r][4 + buffer]) + (workT3Coeffs[instanceNo][3] * workT3[r][3 + buffer]) + (workT3Coeffs[instanceNo][4] * workT3[r][2 + buffer])


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendScalp(_MQL5Indicator):
    name = 'Trend scalp'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 15,  # Period
        'inpT3Period': 5,  # T3 period
        'inpT3Hot': 0.7,  # T3 hot
        'inpT3Type': _Choice({0: 'Tim Tillson way of calculation', 1: 'Fulks/Matulich way of calculation'}, default=1),  # T3 type
        'inpLevels': 100.0,  # Levels at +- (nnn)
    }

