"""QQE of rsi(oma) — converted from MQL5: MQL5 Indicators/QQE of Rsi(oma)/QQE of rsi(oma).mq5

QQE of Rsi(oma)
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 8}, 'colors': {1: [11119017], 2: [11119017], 3: [11119017, 16760576, 8036607]}, 'widths': {3: 2}, 'styles': {1: 2}, 'labels': {1: 'QQE fast', 2: 'QQE slow', 3: 'QQE'}, 'levels': [], 'description': ['QQE of Rsi(oma)'], 'name': 'QQE of rsi(oma)', 'source': 'MQL5 Indicators/QQE of Rsi(oma)/QQE of rsi(oma).mq5', 'folder': 'QQE of Rsi(oma)', 'inputs': [{'mql': 'inpRsiPeriod', 'py': 'inpRsiPeriod', 'param': 'inpRsiPeriod', 'type': 'int', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 32, 'label': 'Average period', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 1, 'label': 'Average method', 'sinput': False}, {'mql': 'inpRsiSmoothingFactor', 'py': 'inpRsiSmoothingFactor', 'param': 'inpRsiSmoothingFactor', 'type': 'int', 'default': 5, 'label': 'RSI smoothing factor', 'sinput': False}, {'mql': 'inpWPFast', 'py': 'inpWPFast', 'param': 'inpWPFast', 'type': 'double', 'default': 2.618, 'label': 'Fast period', 'sinput': False}, {'mql': 'inpWPSlow', 'py': 'inpWPSlow', 'param': 'inpWPSlow', 'type': 'double', 'default': 4.236, 'label': 'Slow period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRsiPeriod = _input('inpRsiPeriod', 14)  # RSI period
inpMaPeriod = _input('inpMaPeriod', 32)  # Average period
inpMaMethod = _input('inpMaMethod', MODE_EMA)  # Average method
inpRsiSmoothingFactor = _input('inpRsiSmoothingFactor', 5)  # RSI smoothing factor
inpWPFast = _input('inpWPFast', 2.618)  # Fast period
inpWPSlow = _input('inpWPSlow', 4.236)  # Slow period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levs = Arr(0, 0.0)
levf = Arr(0, 0.0)
ema = Arr(0, 0.0)
emm = Arr(0, 0.0)
rsi = Arr(0, 0.0)
_alphaS = 0.0
_alphaR = 0.0
_rsiHandle = 0
_maHandle = 0
_rsiPeriod = 0

def OnInit():
    global _alphaR, _alphaS, _maHandle, _rsiHandle, _rsiPeriod
    SetIndexBuffer(0, levf, INDICATOR_DATA)
    SetIndexBuffer(1, levs, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, ema, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, emm, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, rsi, INDICATOR_CALCULATIONS)
    _rsiPeriod = (inpRsiPeriod if (inpRsiPeriod > 1) else 1)
    _maHandle = iMA(Symbol(), 0, inpMaPeriod, 0, inpMaMethod, inpPrice)
    if not _checkHandle(_maHandle, 'average'):
        return INIT_FAILED
    _rsiHandle = iRSI(Symbol(), 0, _rsiPeriod, _maHandle)
    if not _checkHandle(_rsiHandle, 'RSI'):
        return INIT_FAILED
    _alphaS = _fdiv(2.0, 1.0 + (inpRsiSmoothingFactor if (inpRsiSmoothingFactor > 1) else 1))
    _alphaR = _fdiv(2.0, 1.0 + _rsiPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'QQE (' + _str(inpRsiPeriod) + ',' + _str(inpRsiSmoothingFactor) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(_rsiHandle, 0, 0, _copyCount, rsi) != _copyCount:
        return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        if rsi[i] == EMPTY_VALUE:
            rsi[i] = 0.0
        if i > 0:
            val[i] = val[i - 1] + (_alphaS * (rsi[i] - val[i - 1]))
            _diff = val[i - 1] - val[i]
            if _diff < 0:
                _diff = -_diff
            ema[i] = ema[i - 1] + (_alphaR * (_diff - ema[i - 1]))
            emm[i] = emm[i - 1] + (_alphaR * (ema[i] - emm[i - 1]))
            _iEmf = emm[i] * inpWPFast
            _iEms = emm[i] * inpWPSlow
            tr = levs[i - 1]
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
            tr = levf[i - 1]
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
        else:
            levs[i] = 0.0
            levf[i] = levs[i]
            val[i] = levf[i]
        valc[i] = (1 if (val[i] > levf[i] and val[i] > levs[i]) else 2 if (val[i] < levf[i] and val[i] < levs[i]) else valc[i - 1] if (i > 0) else 0)
        i += 1
    return i

def _checkHandle(_handle, _description):
    _size = ArraySize(_s__checkHandle__chandles)
    _answer = _handle != INVALID_HANDLE
    if _answer:
        ArrayResize(_s__checkHandle__chandles, _size + 1)
        _s__checkHandle__chandles[_size] = _handle
    else:
        for i in range(_size - 1, 0 - 1, -1):
            IndicatorRelease(_s__checkHandle__chandles[i])
        ArrayResize(_s__checkHandle__chandles, 0)
        Alert(_description + ' initialization failed')
    return _answer

# ---- static local variables
_s__checkHandle__chandles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class QQEOfRsiOma(_MQL5Indicator):
    name = 'QQE of rsi(oma)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRsiPeriod': 14,  # RSI period
        'inpMaPeriod': 32,  # Average period
        'inpMaMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Average method
        'inpRsiSmoothingFactor': 5,  # RSI smoothing factor
        'inpWPFast': 2.618,  # Fast period
        'inpWPSlow': 4.236,  # Slow period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

