"""DSL QQE histo — converted from MQL5: MQL5 Indicators/DSL QQE histo/DSL QQE histo.mq5

Discontinued signal line QQE histo
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 6}, 'types': {1: 11, 2: 1, 3: 1, 4: 1, 5: 1, 6: 8}, 'colors': {1: [14474460, 16760576, 8036607], 2: [12632256], 3: [12632256], 4: [11119017], 5: [11119017], 6: [11119017, 16760576, 8036607]}, 'widths': {1: 2, 6: 2}, 'styles': {2: 2, 3: 2, 4: 2}, 'labels': {1: 'QQE histogram', 2: 'Level up', 3: 'Level down', 4: 'QQE fast', 5: 'QQE slow', 6: 'QQE'}, 'levels': [], 'description': ['Discontinued signal line QQE histo'], 'name': 'DSL QQE histo', 'source': 'MQL5 Indicators/DSL QQE histo/DSL QQE histo.mq5', 'folder': 'DSL QQE histo', 'inputs': [{'mql': 'inpRsiPeriod', 'py': 'inpRsiPeriod', 'param': 'inpRsiPeriod', 'type': 'int', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'inpRsiSmoothingFactor', 'py': 'inpRsiSmoothingFactor', 'param': 'inpRsiSmoothingFactor', 'type': 'int', 'default': 5, 'label': 'RSI smoothing factor', 'sinput': False}, {'mql': 'inpWPFast', 'py': 'inpWPFast', 'param': 'inpWPFast', 'type': 'double', 'default': 2.618, 'label': 'Fast period', 'sinput': False}, {'mql': 'inpWPSlow', 'py': 'inpWPSlow', 'param': 'inpWPSlow', 'type': 'double', 'default': 4.236, 'label': 'Slow period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpSignalPeriod', 'py': 'inpSignalPeriod', 'param': 'inpSignalPeriod', 'type': 'double', 'default': 9.0, 'label': 'DSL signal period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRsiPeriod = _input('inpRsiPeriod', 14)  # RSI period
inpRsiSmoothingFactor = _input('inpRsiSmoothingFactor', 5)  # RSI smoothing factor
inpWPFast = _input('inpWPFast', 2.618)  # Fast period
inpWPSlow = _input('inpWPSlow', 4.236)  # Slow period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpSignalPeriod = _input('inpSignalPeriod', 9.0)  # DSL signal period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levup = Arr(0, 0.0)
levdn = Arr(0, 0.0)
levs = Arr(0, 0.0)
levf = Arr(0, 0.0)
histoh = Arr(0, 0.0)
histol = Arr(0, 0.0)
histoc = Arr(0, 0.0)
rsi = Arr(0, 0.0)
_rsiHandle = 0
workEma = Arr(6, 0.0, dyn=False, dims=(5,))

def OnInit():
    global _rsiHandle
    SetIndexBuffer(0, histoh, INDICATOR_DATA)
    SetIndexBuffer(1, histol, INDICATOR_DATA)
    SetIndexBuffer(2, histoc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, levup, INDICATOR_DATA)
    SetIndexBuffer(4, levdn, INDICATOR_DATA)
    SetIndexBuffer(5, levf, INDICATOR_DATA)
    SetIndexBuffer(6, levs, INDICATOR_DATA)
    SetIndexBuffer(7, val, INDICATOR_DATA)
    SetIndexBuffer(8, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(9, rsi, INDICATOR_CALCULATIONS)
    _rsiHandle = iRSI(Symbol(), 0, inpRsiPeriod, inpPrice)
    if not _checkHandle(_rsiHandle):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'DSL QQE histo (' + _str(inpRsiPeriod) + ',' + _str(inpRsiSmoothingFactor) + ',' + _str(inpSignalPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(_rsiHandle) < rates_total:
        return prev_calculated
    _copyCount = MathMin(rates_total - prev_calculated + 1, rates_total)
    if CopyBuffer(_rsiHandle, 0, 0, _copyCount, rsi) != _copyCount:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        histoh[i] = iEma((rsi[i] if (rsi[i] != EMPTY_VALUE) else 0), inpRsiSmoothingFactor, i, 0)
        val[i] = histoh[i]
        _iEma = iEma((MathAbs(val[i - 1] - val[i]) if (i > 0) else 0), inpRsiPeriod, i, 1)
        _iEmm = iEma(_iEma, inpRsiPeriod, i, 2)
        _iEmf = _iEmm * inpWPFast
        _iEms = _iEmm * inpWPSlow
        tr = (levs[i - 1] if (i > 0) else 0)
        dv = tr
        if val[i] < tr:
            tr = val[i] + _iEms
            if (i > 0 and val[i - 1] < dv) and tr > dv:
                tr = dv
        if val[i] > tr:
            tr = val[i] - _iEms
            if (i > 0 and val[i - 1] > dv) and tr < dv:
                tr = dv
        levs[i] = tr
        tr = (levf[i - 1] if (i > 0) else 0)
        dv = tr
        if val[i] < tr:
            tr = val[i] + _iEmf
            if (i > 0 and val[i - 1] < dv) and tr > dv:
                tr = dv
        if val[i] > tr:
            tr = val[i] - _iEmf
            if (i > 0 and val[i - 1] > dv) and tr < dv:
                tr = dv
        levf[i] = tr
        histol[i] = 50.0
        levup[i] = iEma(val[i], inpSignalPeriod, i, 3, val[i] < 50.0)
        levdn[i] = iEma(val[i], inpSignalPeriod, i, 4, val[i] > 50.0)
        valc[i] = (1 if (val[i] > levf[i] and val[i] > levs[i]) else 2 if (val[i] < levf[i] and val[i] < levs[i]) else valc[i - 1] if (i > 0) else 0)
        histoc[i] = (1 if (val[i] > levup[i]) else 2 if (val[i] < levdn[i]) else 0)
        i += 1
    return i

def iEma(price, period, i, _inst=0, copy=False):
    _indC = _imod(i, 6)
    _indP = _imod(i - 1, 6)
    if ((not copy) and i > 0) and period > 1:
        workEma[_indC][_inst] = workEma[_indP][_inst] + (_fdiv(2.0, 1.0 + period) * (price - workEma[_indP][_inst]))
    else:
        workEma[_indC][_inst] = (workEma[_indP][_inst] if (i > 0) else price)
    return workEma[_indC][_inst]

def _checkHandle(_handle):
    _size = ArraySize(_s__checkHandle__handles)
    if _handle != INVALID_HANDLE:
        ArrayResize(_s__checkHandle__handles, _size + 1)
        _s__checkHandle__handles[_size] = _handle
        return True
    for i in range(_size - 1, 0, -1):
        IndicatorRelease(_s__checkHandle__handles[i])
    return False

# ---- static local variables
_s__checkHandle__handles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DSLQQEHisto(_MQL5Indicator):
    name = 'DSL QQE histo'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRsiPeriod': 14,  # RSI period
        'inpRsiSmoothingFactor': 5,  # RSI smoothing factor
        'inpWPFast': 2.618,  # Fast period
        'inpWPSlow': 4.236,  # Slow period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpSignalPeriod': 9.0,  # DSL signal period
    }

