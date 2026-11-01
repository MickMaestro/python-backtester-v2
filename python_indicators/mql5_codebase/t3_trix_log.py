"""T3 TRIX log — converted from MQL5: MQL5 Indicators/T3 TRIX Log/T3 TRIX log.mq5

T3 Trix
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 16748574, 6333684]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Trix'}, 'levels': [], 'description': ['T3 Trix'], 'name': 'T3 TRIX log', 'source': 'MQL5 Indicators/T3 TRIX Log/T3 TRIX log.mq5', 'folder': 'T3 TRIX Log', 'inputs': [{'mql': 'inpTrixPeriod', 'py': 'inpTrixPeriod', 'param': 'inpTrixPeriod', 'type': 'int', 'default': 14, 'label': 'Trix period', 'sinput': False}, {'mql': 'inpT3Hot', 'py': 'inpT3Hot', 'param': 'inpT3Hot', 'type': 'double', 'default': 0.7, 'label': 'T3 hot', 'sinput': False}, {'mql': 'inpT3Type', 'py': 'inpT3Type', 'param': 'inpT3Type', 'type': 'int', 'default': 1, 'label': 'T3 type', 'sinput': False}, {'mql': 'inpTrixPrice', 'py': 'inpTrixPrice', 'param': 'inpTrixPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enT3Type
t3_tillson = 0
t3_fulksmat = 1
_enum('enT3Type', {0: 't3_tillson', 1: 't3_fulksmat'})

# ---- inputs and global variables
inpTrixPeriod = _input('inpTrixPeriod', 14)  # Trix period
inpT3Hot = _input('inpT3Hot', 0.7)  # T3 hot
inpT3Type = _input('inpT3Type', t3_fulksmat)  # T3 type
inpTrixPrice = _input('inpTrixPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
workTrix = Arr(0, 0.0, dims=(3,))
workT3 = Arr(0, 0.0, dims=(18,))
workT3Coeffs = Arr(0, 0.0, dims=(6,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'T3 TRIX log (' + _str(inpTrixPeriod) + ',' + _str(inpT3Hot) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if ArrayRange(workTrix, 0) != rates_total:
        ArrayResize(workTrix, rates_total)
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        price = MathLog(getPrice(inpTrixPrice, open, close, high, low, i, rates_total))
        workTrix[i][0] = iT3(price, inpTrixPeriod, inpT3Hot, inpT3Type == t3_tillson, i, rates_total, 0)
        workTrix[i][1] = iT3(workTrix[i][0], inpTrixPeriod, inpT3Hot, inpT3Type == t3_tillson, i, rates_total, 1)
        workTrix[i][2] = iT3(workTrix[i][1], inpTrixPeriod, inpT3Hot, inpT3Type == t3_tillson, i, rates_total, 2)
        val[i] = ((_fdiv(workTrix[i][2] - workTrix[i - 1][2], workTrix[i - 1][2]) if (workTrix[i - 1][2] != 0) else 0) if (i > 0) else 0)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
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

def getPrice(tprice, open, close, high, low, i, _bars):
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


class T3TRIXLog(_MQL5Indicator):
    name = 'T3 TRIX log'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTrixPeriod': 14,  # Trix period
        'inpT3Hot': 0.7,  # T3 hot
        'inpT3Type': _Choice({0: 'Tim Tillson way of calculation', 1: 'Fulks/Matulich way of calculation'}, default=1),  # T3 type
        'inpTrixPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

