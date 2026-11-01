"""RSX of RSX — converted from MQL5: MQL5 Indicators/RSX of RSX/RSX of RSX.mq5

RSX of RSX
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 9639167, 32768]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Rsx'}, 'levels': [], 'description': ['RSX of RSX'], 'name': 'RSX of RSX', 'source': 'MQL5 Indicators/RSX of RSX/RSX of RSX.mq5', 'folder': 'RSX of RSX', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 32, 'label': 'RSX period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32)  # RSX period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
workRsi = Arr(5, 0.0, dyn=False, dims=(26,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSX of RSX (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        _price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        val[i] = iRsx(iRsx(_price, inpPeriod, i, 0), inpPeriod, i, 1)
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
    return rates_total

def iRsx(price, period, i, instance=0):
    _indP = _int(MathMod(i - 1, 5))
    _indC = _int(MathMod(i, 5))
    _inst = instance * 13
    workRsi[_indC][_inst] = price
    if i < period:
        for k in range(1, 13):
            workRsi[_indC][_inst + k] = 0.0
        return 50.0
    Kg = _fdiv(3.0, 2.0 + period)
    Hg = 1.0 - Kg
    mom = workRsi[_indC][_inst] - workRsi[_indP][_inst]
    moa = MathAbs(mom)
    for k in range(0, 3):
        kk = _inst + (k * 2)
        workRsi[_indC][kk + 1] = (Kg * mom) + (Hg * workRsi[_indP][kk + 1])
        workRsi[_indC][kk + 2] = (Kg * workRsi[_indC][kk + 1]) + (Hg * workRsi[_indP][kk + 2])
        mom = (1.5 * workRsi[_indC][kk + 1]) - (0.5 * workRsi[_indC][kk + 2])
        workRsi[_indC][kk + 7] = (Kg * moa) + (Hg * workRsi[_indP][kk + 7])
        workRsi[_indC][kk + 8] = (Kg * workRsi[_indC][kk + 7]) + (Hg * workRsi[_indP][kk + 8])
        moa = (1.5 * workRsi[_indC][kk + 7]) - (0.5 * workRsi[_indC][kk + 8])
    return MathMax(MathMin((_fdiv(mom, MathMax(moa, DBL_MIN)) + 1.0) * 50.0, 100.0), 0.0)

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


class RSXOfRSX(_MQL5Indicator):
    name = 'RSX of RSX'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 32,  # RSX period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

