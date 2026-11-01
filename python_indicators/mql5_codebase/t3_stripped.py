"""T3 stripped — converted from MQL5: MQL5 Indicators/T3 stripped/T3 stripped.mq5

T3 stripped
Copyright: © mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 16, 'indicator_plots': 11}, 'types': {1: 7, 2: 7, 3: 7, 4: 7, 5: 7, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1}, 'colors': {1: [8310016, 8257691], 2: [8303616, 8257716], 3: [8297216, 8257741], 4: [8297216, 8257741], 5: [8297216, 8257741], 6: [8421504], 7: [8421504], 8: [8421504], 9: [8421504], 10: [8421504], 11: [8421504]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Fill 1', 2: 'Fill 2', 3: 'Fill 3', 4: 'Fill 5', 6: 'T3 step 1', 7: 'T3 step 2', 8: 'T3 step 3', 9: 'T3 step 4', 10: 'T3 step 5', 11: 'T3 step 6'}, 'levels': [], 'description': ['T3 stripped'], 'name': 'T3 stripped', 'source': 'MQL5 Indicators/T3 stripped/T3 stripped.mq5', 'folder': 'T3 stripped', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'double', 'default': 14.0, 'label': 'Period', 'sinput': False}, {'mql': 'inpHot', 'py': 'inpHot', 'param': 'inpHot', 'type': 'double', 'default': 0.7, 'label': 'Hot', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpT3Type', 'py': 'inpT3Type', 'param': 'inpT3Type', 'type': 'int', 'default': 1, 'label': 'T3 type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enT3Type
t3_tillson = 0
t3_fulksmat = 1
_enum('enT3Type', {0: 't3_tillson', 1: 't3_fulksmat'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14.0)  # Period
inpHot = _input('inpHot', 0.7)  # Hot
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpT3Type = _input('inpT3Type', t3_fulksmat)  # T3 type
t3_1u = Arr(0, 0.0)
t3_1d = Arr(0, 0.0)
t3_2u = Arr(0, 0.0)
t3_2d = Arr(0, 0.0)
t3_3u = Arr(0, 0.0)
t3_3d = Arr(0, 0.0)
t3_4u = Arr(0, 0.0)
t3_4d = Arr(0, 0.0)
t3_5u = Arr(0, 0.0)
t3_5d = Arr(0, 0.0)
t3_1 = Arr(0, 0.0)
t3_2 = Arr(0, 0.0)
t3_3 = Arr(0, 0.0)
t3_4 = Arr(0, 0.0)
t3_5 = Arr(0, 0.0)
t3_6 = Arr(0, 0.0)
workT3 = Arr(5, 0.0, dyn=False, dims=(6,))
workT3Coeffs = Arr(0, 0.0, dims=(6,))

def OnInit():
    SetIndexBuffer(0, t3_1u, INDICATOR_DATA)
    SetIndexBuffer(1, t3_1d, INDICATOR_DATA)
    SetIndexBuffer(2, t3_2u, INDICATOR_DATA)
    SetIndexBuffer(3, t3_2d, INDICATOR_DATA)
    SetIndexBuffer(4, t3_3u, INDICATOR_DATA)
    SetIndexBuffer(5, t3_3d, INDICATOR_DATA)
    SetIndexBuffer(6, t3_4u, INDICATOR_DATA)
    SetIndexBuffer(7, t3_4d, INDICATOR_DATA)
    SetIndexBuffer(8, t3_5u, INDICATOR_DATA)
    SetIndexBuffer(9, t3_5d, INDICATOR_DATA)
    SetIndexBuffer(10, t3_1, INDICATOR_DATA)
    SetIndexBuffer(11, t3_2, INDICATOR_DATA)
    SetIndexBuffer(12, t3_3, INDICATOR_DATA)
    SetIndexBuffer(13, t3_4, INDICATOR_DATA)
    SetIndexBuffer(14, t3_5, INDICATOR_DATA)
    SetIndexBuffer(15, t3_6, INDICATOR_DATA)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        laga = Box(0.0)
        lagb = Box(0.0)
        lagc = Box(0.0)
        lagd = Box(0.0)
        lage = Box(0.0)
        lagf = Box(0.0)
        iT3(getPrice(inpPrice, open, close, high, low, i, rates_total), inpPeriod, inpHot, inpT3Type == t3_tillson, laga, lagb, lagc, lagd, lage, lagf, i)
        t3_1[i] = laga.v
        t3_2[i] = lagb.v
        t3_3[i] = lagc.v
        t3_4[i] = lagd.v
        t3_5[i] = lage.v
        t3_6[i] = lagf.v
        t3_1u[i] = laga.v
        t3_1d[i] = lagb.v
        t3_2u[i] = lagb.v
        t3_2d[i] = lagc.v
        t3_3u[i] = lagc.v
        t3_3d[i] = lagd.v
        t3_4u[i] = lagd.v
        t3_4d[i] = lage.v
        t3_5u[i] = lage.v
        t3_5d[i] = lagf.v
        i += 1
    return i

def iT3(price, period, hot, original, lev0, lev1, lev2, lev3, lev4, lev5, i, instance=0):
    _indP = _imod(i - 1, 5)
    _indC = _imod(i, 5)
    _inst = instance * 6
    if ArrayRange(workT3Coeffs, 0) < (instance + 1):
        ArrayResize(workT3Coeffs, instance + 1)
        workT3Coeffs[instance][0] = -99.0
    if workT3Coeffs[instance][0] != period:
        workT3Coeffs[instance][0] = period
        workT3Coeffs[instance][1] = (-hot) * hot * hot
        workT3Coeffs[instance][2] = (3 * hot * hot) + (3 * hot * hot * hot)
        workT3Coeffs[instance][3] = (-6 * hot * hot) - (3 * hot) - (3 * hot * hot * hot)
        workT3Coeffs[instance][4] = 1 + (3 * hot) + (hot * hot * hot) + (3 * hot * hot)
        workT3Coeffs[instance][5] = (_fdiv(2.0, 1.0 + period) if original else _fdiv(2.0, 2.0 + ((period - 1.0) / 2.0)))
    for k in range(0, 6):
        workT3[_indC][k + _inst] = (workT3[_indP][k + _inst] if (i > 0) else price)
    if i > 0 and period > 1:
        workT3[_indC][_inst] = workT3[_indP][_inst] + (workT3Coeffs[instance][5] * (price - workT3[_indP][_inst]))
        workT3[_indC][1 + _inst] = workT3[_indP][1 + _inst] + (workT3Coeffs[instance][5] * (workT3[_indC][0 + _inst] - workT3[_indP][1 + _inst]))
        workT3[_indC][2 + _inst] = workT3[_indP][2 + _inst] + (workT3Coeffs[instance][5] * (workT3[_indC][1 + _inst] - workT3[_indP][2 + _inst]))
        workT3[_indC][3 + _inst] = workT3[_indP][3 + _inst] + (workT3Coeffs[instance][5] * (workT3[_indC][2 + _inst] - workT3[_indP][3 + _inst]))
        workT3[_indC][4 + _inst] = workT3[_indP][4 + _inst] + (workT3Coeffs[instance][5] * (workT3[_indC][3 + _inst] - workT3[_indP][4 + _inst]))
        workT3[_indC][5 + _inst] = workT3[_indP][5 + _inst] + (workT3Coeffs[instance][5] * (workT3[_indC][4 + _inst] - workT3[_indP][5 + _inst]))
    lev0.v = workT3[_indC][_inst]
    lev1.v = workT3[_indC][_inst + 1]
    lev2.v = workT3[_indC][_inst + 2]
    lev3.v = workT3[_indC][_inst + 3]
    lev4.v = workT3[_indC][_inst + 4]
    lev5.v = workT3[_indC][_inst + 5]

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


class T3Stripped(_MQL5Indicator):
    name = 'T3 stripped'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14.0,  # Period
        'inpHot': 0.7,  # Hot
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpT3Type': _Choice({0: 'Tim Tillson way of calculation', 1: 'Fulks / Matulich way of calculation'}, default=1),  # T3 type
    }

