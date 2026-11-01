"""Pearson coeficcient — converted from MQL5: MQL5 Indicators/Pearson coefficient/Pearson coeficcient.mq5

Pearson coeficcient
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 8}, 'colors': {1: [2263842], 2: [11119017], 3: [3937500], 4: [11119017, 3937500, 2263842]}, 'widths': {4: 2}, 'styles': {1: 2, 2: 2, 3: 2}, 'labels': {1: 'Level up', 2: 'Middle level', 3: 'Level down', 4: 'Pearson coeficcient'}, 'levels': [], 'description': ['Pearson coeficcient'], 'name': 'Pearson coeficcient', 'source': 'MQL5 Indicators/Pearson coefficient/Pearson coeficcient.mq5', 'folder': 'Pearson coefficient', 'inputs': [{'mql': 'inpSymbol', 'py': 'inpSymbol', 'param': None, 'type': 'string', 'default': '', 'label': 'Second symbol', 'sinput': False}, {'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 30, 'label': 'Period', 'sinput': False}, {'mql': 'inpLag', 'py': 'inpLag', 'param': 'inpLag', 'type': 'int', 'default': 1, 'label': 'Lag of the second symbol', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpColorMode', 'py': 'inpColorMode', 'param': 'inpColorMode', 'type': 'int', 'default': 1, 'label': 'Change color mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorMode
col_onZero = 0
col_onOuter = 1
_enum('enColorMode', {0: 'col_onZero', 1: 'col_onOuter'})

# ---- inputs and global variables
inpSymbol = _input('inpSymbol', '')  # Second symbol
inpPeriod = _input('inpPeriod', 30)  # Period
inpLag = _input('inpLag', 1)  # Lag of the second symbol
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpColorMode = _input('inpColorMode', col_onOuter)  # Change color mode
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
flup = Arr(0, 0.0)
flmi = Arr(0, 0.0)
fldn = Arr(0, 0.0)
diff = Arr(0, 0.0)
difl = Arr(0, 0.0)
_forSymbol = ""

def OnInit():
    global _forSymbol
    SetIndexBuffer(0, flup, INDICATOR_DATA)
    SetIndexBuffer(1, flmi, INDICATOR_DATA)
    SetIndexBuffer(2, fldn, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, diff, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, difl, INDICATOR_CALCULATIONS)
    _forSymbol = (Symbol() if (inpSymbol == '') else inpSymbol)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Pearson ' + Symbol() + ' to ' + _forSymbol + ' coeficcient (' + _str(inpPeriod) + ',' + _str(inpLag) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    pers = MathSqrt(inpPeriod)
    _ratesf = Arr(1, 0, dyn=False, factory=MqlRates)
    _ratesl = Arr(1, 0, dyn=False, factory=MqlRates)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        _ratesfCopied = CopyRates(Symbol(), 0, _DT(time[i]), 1, _ratesf)
        _rateslCopied = (CopyRates(_forSymbol, 0, _DT(time[i - inpLag]), 1, _ratesl) if (i >= inpLag) else CopyRates(_forSymbol, 0, _DT(time[i]), 1, _ratesl))
        diff[i] = (getPrice(inpPrice, _ratesf) if (_ratesfCopied == 1) else 0)
        difl[i] = (getPrice(inpPrice, _ratesl) if (_rateslCopied == 1) else 0)
        dev1 = iDeviation(diff, inpPeriod, i)
        dev2 = iDeviation(difl, inpPeriod, i)
        val[i] = (_fdiv(iCovariance(diff, difl, inpPeriod, i), dev1 * dev2) if (dev1 != 0 and dev2 != 0) else 0)
        pe = _fdiv(0.6745 * (1.0 - (val[i] * val[i])), pers)
        flup[i] = 6.0 * pe
        fldn[i] = -6.0 * pe
        flmi[i] = 0.0
        _sw1 = inpColorMode
        if _sw1 == col_onOuter:
            valc[i] = (2 if (val[i] > flup[i]) else 1 if (val[i] < fldn[i]) else 0)
        elif _sw1 == col_onZero:
            valc[i] = (2 if (val[i] > flmi[i]) else 1 if (val[i] < flmi[i]) else valc[i - 1] if (i > 0) else 0)
    return rates_total

def iDeviation(array, size, i, isSample=False):
    avg = array[i]
    k = 1
    while k < size and (i - k) >= 0:
        avg += array[i - k]
        k += 1
    avg = _fdiv(avg, float(size))
    sum_ = 0.0
    k = 0
    while k < size and (i - k) >= 0:
        sum_ += (array[i - k] - avg) * (array[i - k] - avg)
        k += 1
    if isSample:
        return MathSqrt(_fdiv(sum_, float(size - 1)))
    else:
        return MathSqrt(_fdiv(sum_, float(size)))

def iCovariance(indep, depen, size, i, isSample=False):
    avgi = indep[i]
    k = 1
    while k < size and (i - k) >= 0:
        avgi += indep[i - k]
        k += 1
    avgi = _fdiv(avgi, size)
    avgd = depen[i]
    k = 1
    while k < size and (i - k) >= 0:
        avgd += depen[i - k]
        k += 1
    avgd = _fdiv(avgd, size)
    sum_ = 0.0
    k = 0
    while k < size and (i - k) >= 0:
        sum_ += (indep[i - k] - avgi) * (depen[i - k] - avgd)
        k += 1
    if isSample:
        return _fdiv(sum_, size - 1)
    else:
        return _fdiv(sum_, size)

def getPrice(tprice, _rates):
    _sw2 = tprice
    if _sw2 == PRICE_CLOSE:
        return _rates[0].close
    elif _sw2 == PRICE_OPEN:
        return _rates[0].open
    elif _sw2 == PRICE_HIGH:
        return _rates[0].high
    elif _sw2 == PRICE_LOW:
        return _rates[0].low
    elif _sw2 == PRICE_MEDIAN:
        return (_rates[0].high + _rates[0].low) / 2.0
    elif _sw2 == PRICE_TYPICAL:
        return (_rates[0].high + _rates[0].low + _rates[0].close) / 3.0
    elif _sw2 == PRICE_WEIGHTED:
        return (_rates[0].high + _rates[0].low + _rates[0].close + _rates[0].close) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PearsonCoeficcient(_MQL5Indicator):
    name = 'Pearson coeficcient'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 30,  # Period
        'inpLag': 1,  # Lag of the second symbol
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpColorMode': _Choice({0: 'Change color on middle line cross', 1: 'Change color on outer levels cross'}, default=1),  # Change color mode
    }

