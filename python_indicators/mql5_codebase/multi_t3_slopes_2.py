"""Multi T3 slopes 2 — converted from MQL5: MQL5 Indicators/Multi T3 Slopes/Multi T3 slopes 2.mq5

Multi T3 slopes
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 3, 2: 3}, 'colors': {1: [3329330], 2: [3937500]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Multi T3 slopes up', 2: 'Multi T3 slopes down'}, 'levels': [], 'description': ['Multi T3 slopes'], 'name': 'Multi T3 slopes 2', 'source': 'MQL5 Indicators/Multi T3 Slopes/Multi T3 slopes 2.mq5', 'folder': 'Multi T3 Slopes', 'inputs': [{'mql': 'inpT3Type', 'py': 'inpT3Type', 'param': 'inpT3Type', 'type': 'int', 'default': 1, 'label': 'T3 type', 'sinput': False}, {'mql': 'inpT3Hot', 'py': 'inpT3Hot', 'param': 'inpT3Hot', 'type': 'double', 'default': 0.7, 'label': 'T3 hot', 'sinput': False}, {'mql': 'inpPeriod1', 'py': 'inpPeriod1', 'param': 'inpPeriod1', 'type': 'int', 'default': 8, 'label': 'Period 1', 'sinput': False}, {'mql': 'inpPeriod2', 'py': 'inpPeriod2', 'param': 'inpPeriod2', 'type': 'int', 'default': 11, 'label': 'Period 2', 'sinput': False}, {'mql': 'inpPeriod3', 'py': 'inpPeriod3', 'param': 'inpPeriod3', 'type': 'int', 'default': 14, 'label': 'Period 3', 'sinput': False}, {'mql': 'inpPeriod4', 'py': 'inpPeriod4', 'param': 'inpPeriod4', 'type': 'int', 'default': 17, 'label': 'Period 4', 'sinput': False}, {'mql': 'inpPeriod5', 'py': 'inpPeriod5', 'param': 'inpPeriod5', 'type': 'int', 'default': 20, 'label': 'Period 5', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enT3Type
t3_tillson = 0
t3_fulksmat = 1
_enum('enT3Type', {0: 't3_tillson', 1: 't3_fulksmat'})

# ---- inputs and global variables
inpT3Type = _input('inpT3Type', t3_fulksmat)  # T3 type
inpT3Hot = _input('inpT3Hot', 0.7)  # T3 hot
inpPeriod1 = _input('inpPeriod1', 8)  # Period 1
inpPeriod2 = _input('inpPeriod2', 11)  # Period 2
inpPeriod3 = _input('inpPeriod3', 14)  # Period 3
inpPeriod4 = _input('inpPeriod4', 17)  # Period 4
inpPeriod5 = _input('inpPeriod5', 20)  # Period 5
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
histou = Arr(0, 0.0)
histod = Arr(0, 0.0)
averages = Arr(0, 0.0, dims=(5,))
workT3 = Arr(5, 0.0, dyn=False, dims=(30,))
workT3Coeffs = Arr(0, 0.0, dims=(6,))

def OnInit():
    SetIndexBuffer(0, histou, INDICATOR_DATA)
    SetIndexBuffer(1, histod, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Multi T3 slopes (' + _str(inpT3Hot) + ',' + _str(inpPeriod1) + ',' + _str(inpPeriod2) + ',' + _str(inpPeriod3) + ',' + _str(inpPeriod4) + ',' + _str(inpPeriod5) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    if ArrayRange(averages, 0) != rates_total:
        ArrayResize(averages, rates_total)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        _price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        averages[i][0] = iT3(_price, inpPeriod1, inpT3Hot, inpT3Type == t3_fulksmat, i, 0)
        averages[i][1] = iT3(_price, inpPeriod2, inpT3Hot, inpT3Type == t3_fulksmat, i, 1)
        averages[i][2] = iT3(_price, inpPeriod3, inpT3Hot, inpT3Type == t3_fulksmat, i, 2)
        averages[i][3] = iT3(_price, inpPeriod4, inpT3Hot, inpT3Type == t3_fulksmat, i, 3)
        averages[i][4] = iT3(_price, inpPeriod5, inpT3Hot, inpT3Type == t3_fulksmat, i, 4)
        histod[i] = 0.0
        histou[i] = histod[i]
        if i > 0:
            if averages[i][0] > averages[i - 1][0]:
                histou[i] += 1
            if averages[i][0] < averages[i - 1][0]:
                histod[i] -= 1
            if averages[i][1] > averages[i - 1][1]:
                histou[i] += 1
            if averages[i][1] < averages[i - 1][1]:
                histod[i] -= 1
            if averages[i][2] > averages[i - 1][2]:
                histou[i] += 1
            if averages[i][2] < averages[i - 1][2]:
                histod[i] -= 1
            if averages[i][3] > averages[i - 1][3]:
                histou[i] += 1
            if averages[i][3] < averages[i - 1][3]:
                histod[i] -= 1
            if averages[i][4] > averages[i - 1][4]:
                histou[i] += 1
            if averages[i][4] < averages[i - 1][4]:
                histod[i] -= 1
    return rates_total

def iT3(price, period, hot, original, i, instance=0):
    if ArrayRange(workT3Coeffs, 0) < (instance + 1):
        ArrayResize(workT3Coeffs, instance + 1)
    if workT3Coeffs[instance][0] != period:
        workT3Coeffs[instance][0] = period
        workT3Coeffs[instance][1] = (-hot) * hot * hot
        workT3Coeffs[instance][2] = (3 * hot * hot) + (3 * hot * hot * hot)
        workT3Coeffs[instance][3] = (-6 * hot * hot) - (3 * hot) - (3 * hot * hot * hot)
        workT3Coeffs[instance][4] = 1 + (3 * hot) + (hot * hot * hot) + (3 * hot * hot)
        workT3Coeffs[instance][5] = (_fdiv(2.0, 1.0 + period) if original else _fdiv(2.0, 2.0 + ((period - 1.0) / 2.0)))
    _indP = _int(MathMod(i - 1, 5))
    _indC = _int(MathMod(i, 5))
    _inst = instance * 6
    for k in range(0, 6):
        workT3[_indC][k + _inst] = (workT3[_indP][k + _inst] if (i > 0) else price)
    if i > 0 and period > 1:
        workT3[_indC][_inst] = workT3[_indP][_inst] + (workT3Coeffs[instance][5] * (price - workT3[_indP][_inst]))
        workT3[_indC][_inst + 1] = workT3[_indP][_inst + 1] + (workT3Coeffs[instance][5] * (workT3[_indC][_inst] - workT3[_indP][_inst + 1]))
        workT3[_indC][_inst + 2] = workT3[_indP][_inst + 2] + (workT3Coeffs[instance][5] * (workT3[_indC][_inst + 1] - workT3[_indP][_inst + 2]))
        workT3[_indC][_inst + 3] = workT3[_indP][_inst + 3] + (workT3Coeffs[instance][5] * (workT3[_indC][_inst + 2] - workT3[_indP][_inst + 3]))
        workT3[_indC][_inst + 4] = workT3[_indP][_inst + 4] + (workT3Coeffs[instance][5] * (workT3[_indC][_inst + 3] - workT3[_indP][_inst + 4]))
        workT3[_indC][_inst + 5] = workT3[_indP][_inst + 5] + (workT3Coeffs[instance][5] * (workT3[_indC][_inst + 4] - workT3[_indP][_inst + 5]))
    return (workT3Coeffs[instance][1] * workT3[_indC][_inst + 5]) + (workT3Coeffs[instance][2] * workT3[_indC][_inst + 4]) + (workT3Coeffs[instance][3] * workT3[_indC][_inst + 3]) + (workT3Coeffs[instance][4] * workT3[_indC][_inst + 2])

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


class MultiT3Slopes2(_MQL5Indicator):
    name = 'Multi T3 slopes 2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpT3Type': _Choice({0: 'Tim Tillson way of calculation', 1: 'Fulks/Matulich way of calculation'}, default=1),  # T3 type
        'inpT3Hot': 0.7,  # T3 hot
        'inpPeriod1': 8,  # Period 1
        'inpPeriod2': 11,  # Period 2
        'inpPeriod3': 14,  # Period 3
        'inpPeriod4': 17,  # Period 4
        'inpPeriod5': 20,  # Period 5
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

