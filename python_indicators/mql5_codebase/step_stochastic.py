"""step_stochastic — converted from MQL5: MQL5 Indicators/Step Stochastic/step_stochastic.mq5

Copyright: mladen; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3, 'indicator_minimum': 0.0, 'indicator_maximum': 100.0}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [16760576, 9662683], 2: [6908265], 3: [6908265]}, 'widths': {2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'Step stochastic filling', 2: 'Step stochastic', 3: 'Step stochastic signal'}, 'levels': [], 'description': [], 'name': 'step_stochastic', 'source': 'MQL5 Indicators/Step Stochastic/step_stochastic.mq5', 'folder': 'Step Stochastic', 'inputs': [{'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 5, 'label': 'Price to use in calculations', 'sinput': False}, {'mql': 'AtrPeriod', 'py': 'AtrPeriod', 'param': 'AtrPeriod', 'type': 'int', 'default': 10, 'label': 'ATR calculation period', 'sinput': False}, {'mql': 'K_Slow', 'py': 'K_Slow', 'param': 'K_Slow', 'type': 'double', 'default': 1.0, 'label': 'K slow', 'sinput': False}, {'mql': 'K_Fast', 'py': 'K_Fast', 'param': 'K_Fast', 'type': 'double', 'default': 1.0, 'label': 'K fast', 'sinput': False}, {'mql': 'Window', 'py': 'Window', 'param': 'Window', 'type': 'int', 'default': 256, 'label': 'ATR minimum maximum window size', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Price = _input('Price', PRICE_MEDIAN)  # Price to use in calculations
AtrPeriod = _input('AtrPeriod', 10)  # ATR calculation period
K_Slow = _input('K_Slow', 1.0)  # K slow
K_Fast = _input('K_Fast', 1.0)  # K fast
Window = _input('Window', 256)  # ATR minimum maximum window size
stoch1 = Arr(0, 0.0)
stoch2 = Arr(0, 0.0)
fill1 = Arr(0, 0.0)
fill2 = Arr(0, 0.0)
work = Arr(0, 0.0, dims=(13,))

def OnInit():
    SetIndexBuffer(0, fill1, INDICATOR_DATA)
    SetIndexBuffer(1, fill2, INDICATOR_DATA)
    SetIndexBuffer(2, stoch1, INDICATOR_DATA)
    SetIndexBuffer(3, stoch2, INDICATOR_DATA)
    return 0

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if ArrayRange(work, 0) != rates_total:
        ArrayResize(work, rates_total)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        nPrice = 0.0
        _sw1 = Price
        if _sw1 == PRICE_CLOSE:
            nPrice = Close[i]
        elif _sw1 == PRICE_OPEN:
            nPrice = Open[i]
        elif _sw1 == PRICE_HIGH:
            nPrice = High[i]
        elif _sw1 == PRICE_LOW:
            nPrice = Low[i]
        elif _sw1 == PRICE_MEDIAN:
            nPrice = (High[i] + Low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            nPrice = (High[i] + Low[i] + Close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            nPrice = (High[i] + Low[i] + Close[i] + Close[i]) / 4.0
        else:
            nPrice = 0.0
        atr = 0.0
        k = 0
        while k < AtrPeriod and (i - k - 1) >= 0:
            atr += MathMax(High[i - k], Low[i - k - 1]) - MathMin(Low[i - k], High[i - k - 1])
            k += 1
        work[i][12] = atr / AtrPeriod
        if i < Window:
            work[i][6] = 0.0
            work[i][7] = 0.0
            work[i][8] = 0.0
            work[i][9] = 0.0
            work[i][10] = 0.0
            work[i][11] = 0.0
            work[i][0] = 99999999.0
            work[i][1] = 99999999.0
            work[i][4] = 0.0
            work[i][5] = 0.0
            work[i][2] = 0.0
            work[i][3] = 0.0
            stoch1[i] = EMPTY_VALUE
            stoch2[i] = EMPTY_VALUE
            fill1[i] = EMPTY_VALUE
            fill2[i] = EMPTY_VALUE
            continue
        nATRmax = work[i][12]
        nATRmin = work[i][12]
        k = 1
        while k < Window and (i - k) >= 0:
            nATRmax = MathMax(nATRmax, work[i - k][12])
            nATRmin = MathMin(nATRmin, work[i - k][12])
            k += 1
        StepSizeMin = K_Fast * nATRmin
        StepSizeMax = K_Fast * nATRmax
        StepSizeMid = K_Fast * 0.5 * K_Slow * (nATRmax + nATRmin)
        work[i][1] = nPrice + (2.0 * StepSizeMin)
        work[i][0] = nPrice - (2.0 * StepSizeMin)
        work[i][5] = nPrice + (2.0 * StepSizeMax)
        work[i][4] = nPrice - (2.0 * StepSizeMax)
        work[i][3] = nPrice + (2.0 * StepSizeMid)
        work[i][2] = nPrice - (2.0 * StepSizeMid)
        TrendMin = work[i - 1][6]
        TrendMid = work[i - 1][7]
        TrendMax = work[i - 1][8]
        linemin = work[i - 1][9]
        linemid = work[i - 1][10]
        linemax = work[i - 1][11]
        if nPrice > work[i - 1][1]:
            TrendMin = 1.0
        if nPrice < work[i - 1][0]:
            TrendMin = -1.0
        if nPrice > work[i - 1][5]:
            TrendMax = 1.0
        if nPrice < work[i - 1][4]:
            TrendMax = -1.0
        if nPrice > work[i - 1][3]:
            TrendMid = 1.0
        if nPrice < work[i - 1][2]:
            TrendMid = -1.0
        if TrendMin > 0 and work[i][0] < work[i - 1][0]:
            work[i][0] = work[i - 1][0]
        if TrendMin < 0 and work[i][1] > work[i - 1][1]:
            work[i][1] = work[i - 1][1]
        if TrendMax > 0 and work[i][4] < work[i - 1][4]:
            work[i][4] = work[i - 1][4]
        if TrendMax < 0 and work[i][5] > work[i - 1][5]:
            work[i][5] = work[i - 1][5]
        if TrendMid > 0 and work[i][2] < work[i - 1][2]:
            work[i][2] = work[i - 1][2]
        if TrendMid < 0 and work[i][3] > work[i - 1][3]:
            work[i][3] = work[i - 1][3]
        if TrendMin > 0:
            linemin = work[i][0] + StepSizeMin
        if TrendMin < 0:
            linemin = work[i][1] - StepSizeMin
        if TrendMax > 0:
            linemax = work[i][4] + StepSizeMax
        if TrendMax < 0:
            linemax = work[i][5] - StepSizeMax
        if TrendMid > 0:
            linemid = work[i][2] + StepSizeMid
        if TrendMid < 0:
            linemid = work[i][3] - StepSizeMid
        work[i][6] = TrendMin
        work[i][7] = TrendMid
        work[i][8] = TrendMax
        work[i][9] = linemin
        work[i][10] = linemid
        work[i][11] = linemax
        bsmin = linemax - StepSizeMax
        bsmax = linemax + StepSizeMax
        if bsmax != bsmin:
            stoch1[i] = _fdiv(linemin - bsmin, bsmax - bsmin) * 100.0
            stoch2[i] = _fdiv(linemid - bsmin, bsmax - bsmin) * 100.0
        else:
            stoch1[i] = 0.0
            stoch2[i] = 0.0
        fill1[i] = stoch1[i]
        fill2[i] = stoch2[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StepStochastic(_MQL5Indicator):
    name = 'step_stochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price to use in calculations
        'AtrPeriod': 10,  # ATR calculation period
        'K_Slow': 1.0,  # K slow
        'K_Fast': 1.0,  # K fast
        'Window': 256,  # ATR minimum maximum window size
    }
    y_range = (0.0, 100.0)

