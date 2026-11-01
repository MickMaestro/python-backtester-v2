"""QQE of Rsi(oma)(on chart) — converted from MQL5: MQL5 Indicators/QQE of Rsi(oma) - on chart/QQE of Rsi(oma)(on chart).mq5

On-chart QQE
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 17, 'indicator_plots': 8}, 'types': {1: 7, 2: 7, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 8}, 'colors': {1: [15790335], 2: [15794160], 3: [8421504], 4: [8421504], 5: [8421504], 6: [11119017], 7: [11119017], 8: [11119017, 7451452, 17919]}, 'widths': {8: 2}, 'styles': {3: 2, 4: 2, 5: 2, 6: 2}, 'labels': {1: 'Upper filling', 2: 'Lower filling', 3: 'Upper level', 4: 'Middle level', 5: 'Lower level', 6: 'QQE fast', 7: 'QQE slow', 8: 'QQE'}, 'levels': [], 'description': ['On-chart QQE'], 'name': 'QQE of Rsi(oma)(on chart)', 'source': 'MQL5 Indicators/QQE of Rsi(oma) - on chart/QQE of Rsi(oma)(on chart).mq5', 'folder': 'QQE of Rsi(oma) - on chart', 'inputs': [{'mql': 'inpRsiPeriod', 'py': 'inpRsiPeriod', 'param': 'inpRsiPeriod', 'type': 'int', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 32, 'label': 'Average period', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 1, 'label': 'Average method', 'sinput': False}, {'mql': 'inpRsiSmoothingFactor', 'py': 'inpRsiSmoothingFactor', 'param': 'inpRsiSmoothingFactor', 'type': 'int', 'default': 5, 'label': 'RSI smoothing factor', 'sinput': False}, {'mql': 'inpWPFast', 'py': 'inpWPFast', 'param': 'inpWPFast', 'type': 'double', 'default': 2.618, 'label': 'Fast period', 'sinput': False}, {'mql': 'inpWPSlow', 'py': 'inpWPSlow', 'param': 'inpWPSlow', 'type': 'double', 'default': 4.236, 'label': 'Slow period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpHlPeriod', 'py': 'inpHlPeriod', 'param': 'inpHlPeriod', 'type': 'int', 'default': 25, 'label': 'Highest high/lowest low period', 'sinput': False}, {'mql': 'inpHlLevelUp', 'py': 'inpHlLevelUp', 'param': 'inpHlLevelUp', 'type': 'double', 'default': 70.0, 'label': 'OB level', 'sinput': False}, {'mql': 'inpHlLevelDn', 'py': 'inpHlLevelDn', 'param': 'inpHlLevelDn', 'type': 'double', 'default': 30.0, 'label': 'OS level', 'sinput': False}, {'mql': 'inpColorChange', 'py': 'inpColorChange', 'param': 'inpColorChange', 'type': 'int', 'default': 0, 'label': 'Color changing mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorChangeOn
cchange_onOriginal = 0
cchange_onSlope = 1
cchange_onLevels = 2
cchange_onZero = 3
_enum('enColorChangeOn', {0: 'cchange_onOriginal', 1: 'cchange_onSlope', 2: 'cchange_onLevels', 3: 'cchange_onZero'})

# ---- inputs and global variables
inpRsiPeriod = _input('inpRsiPeriod', 14)  # RSI period
inpMaPeriod = _input('inpMaPeriod', 32)  # Average period
inpMaMethod = _input('inpMaMethod', MODE_EMA)  # Average method
inpRsiSmoothingFactor = _input('inpRsiSmoothingFactor', 5)  # RSI smoothing factor
inpWPFast = _input('inpWPFast', 2.618)  # Fast period
inpWPSlow = _input('inpWPSlow', 4.236)  # Slow period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpHlPeriod = _input('inpHlPeriod', 25)  # Highest high/lowest low period
inpHlLevelUp = _input('inpHlLevelUp', 70.0)  # OB level
inpHlLevelDn = _input('inpHlLevelDn', 30.0)  # OS level
inpColorChange = _input('inpColorChange', cchange_onOriginal)  # Color changing mode
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levs = Arr(0, 0.0)
levf = Arr(0, 0.0)
filluu = Arr(0, 0.0)
fillud = Arr(0, 0.0)
filldd = Arr(0, 0.0)
filldu = Arr(0, 0.0)
levu = Arr(0, 0.0)
levd = Arr(0, 0.0)
levm = Arr(0, 0.0)
rsi = Arr(0, 0.0)
work = Arr(0, 0.0)
wlevf = Arr(0, 0.0)
wlevs = Arr(0, 0.0)
ema = Arr(0, 0.0)
emm = Arr(0, 0.0)
_alphaS = 0.0
_alphaR = 0.0
ª_rsiHandle = 0
ª_maHandle = 0
ª_rsiPeriod = 0

def OnInit():
    global _alphaR, _alphaS, ª_maHandle, ª_rsiHandle, ª_rsiPeriod
    SetIndexBuffer(0, filluu, INDICATOR_DATA)
    SetIndexBuffer(1, fillud, INDICATOR_DATA)
    SetIndexBuffer(2, filldu, INDICATOR_DATA)
    SetIndexBuffer(3, filldd, INDICATOR_DATA)
    SetIndexBuffer(4, levm, INDICATOR_DATA)
    SetIndexBuffer(5, levu, INDICATOR_DATA)
    SetIndexBuffer(6, levd, INDICATOR_DATA)
    SetIndexBuffer(7, levf, INDICATOR_DATA)
    SetIndexBuffer(8, levs, INDICATOR_DATA)
    SetIndexBuffer(9, val, INDICATOR_DATA)
    SetIndexBuffer(10, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(11, rsi, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, ema, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, emm, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, work, INDICATOR_CALCULATIONS)
    SetIndexBuffer(15, wlevf, INDICATOR_CALCULATIONS)
    SetIndexBuffer(16, wlevs, INDICATOR_CALCULATIONS)
    ª_rsiPeriod = (inpRsiPeriod if (inpRsiPeriod > 1) else 1)
    ª_maHandle = iMA(Symbol(), 0, inpMaPeriod, 0, inpMaMethod, inpPrice)
    if not _checkHandle(ª_maHandle, 'average'):
        return INIT_FAILED
    ª_rsiHandle = iRSI(Symbol(), 0, ª_rsiPeriod, ª_maHandle)
    if not _checkHandle(ª_rsiHandle, 'RSI'):
        return INIT_FAILED
    _alphaS = _fdiv(2.0, 1.0 + (inpRsiSmoothingFactor if (inpRsiSmoothingFactor > 1) else 1))
    _alphaR = _fdiv(2.0, 1.0 + ª_rsiPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'QQE on chart (' + _str(inpRsiPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_i, _s_OnCalculate_prev_max, _s_OnCalculate_prev_min
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_rsiHandle, 0, 0, _copyCount, rsi) != _copyCount:
        return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        if rsi[i] == EMPTY_VALUE:
            rsi[i] = 0.0
        if i > 0:
            work[i] = work[i - 1] + (_alphaS * (rsi[i] - work[i - 1]))
            _diff = work[i - 1] - work[i]
            if _diff < 0:
                _diff = -_diff
            ema[i] = ema[i - 1] + (_alphaR * (_diff - ema[i - 1]))
            emm[i] = emm[i - 1] + (_alphaR * (ema[i] - emm[i - 1]))
            _iEmf = emm[i] * inpWPFast
            _iEms = emm[i] * inpWPSlow
            tr = wlevs[i - 1]
            dv = tr
            if work[i] < tr:
                tr = work[i] + _iEms
                if (i > 0 and work[i - 1] < dv) and tr > dv:
                    tr = dv
            if work[i] > tr:
                tr = work[i] - _iEms
                if (i > 0 and work[i - 1] > dv) and tr < dv:
                    tr = dv
            wlevs[i] = tr
            tr = wlevf[i - 1]
            dv = tr
            if work[i] < tr:
                tr = work[i] + _iEmf
                if (i > 0 and work[i - 1] < dv) and tr > dv:
                    tr = dv
            if work[i] > tr:
                tr = work[i] - _iEmf
                if (i > 0 and work[i - 1] > dv) and tr < dv:
                    tr = dv
            wlevf[i] = tr
        else:
            wlevs[i] = 0.0
            wlevf[i] = wlevs[i]
            work[i] = wlevf[i]
        if _s_OnCalculate_prev_i != i:
            _s_OnCalculate_prev_i = i
            start = i - inpHlPeriod + 1
            if start < 0:
                start = 0
            _s_OnCalculate_prev_max = high[ArrayMaximum(high, start, inpHlPeriod - 1)]
            _s_OnCalculate_prev_min = low[ArrayMinimum(low, start, inpHlPeriod - 1)]
        max_ = (high[i] if (high[i] > _s_OnCalculate_prev_max) else _s_OnCalculate_prev_max)
        min_ = (low[i] if (low[i] < _s_OnCalculate_prev_min) else _s_OnCalculate_prev_min)
        range_ = (max_ - min_) / 100.0
        levu[i] = min_ + (inpHlLevelUp * range_)
        levd[i] = min_ + (inpHlLevelDn * range_)
        levm[i] = min_ + (50 * range_)
        filldu[i] = min_ + (work[i] * range_)
        fillud[i] = filldu[i]
        val[i] = fillud[i]
        levf[i] = min_ + (wlevf[i] * range_)
        levs[i] = min_ + (wlevs[i] * range_)
        filluu[i] = max_
        filldd[i] = min_
        _sw1 = inpColorChange
        if _sw1 == cchange_onLevels:
            valc[i] = (1 if (val[i] > levu[i]) else 2 if (val[i] < levd[i]) else 0)
        elif _sw1 == cchange_onSlope:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        elif _sw1 == cchange_onZero:
            valc[i] = (1 if (val[i] > levm[i]) else 2 if (val[i] < levm[i]) else 0)
        elif _sw1 == cchange_onOriginal:
            valc[i] = (1 if (work[i] > wlevf[i] and work[i] > wlevs[i]) else 2 if (work[i] < wlevf[i] and work[i] < wlevs[i]) else valc[i - 1] if (i > 0) else 0)
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
_s_OnCalculate_prev_i = -1
_s_OnCalculate_prev_max = 0.0
_s_OnCalculate_prev_min = 0.0
_s__checkHandle__chandles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class QQEOfRsiOmaOnChart(_MQL5Indicator):
    name = 'QQE of Rsi(oma)(on chart)'
    pane = _Pane.PRICE
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
        'inpHlPeriod': 25,  # Highest high/lowest low period
        'inpHlLevelUp': 70.0,  # OB level
        'inpHlLevelDn': 30.0,  # OS level
        'inpColorChange': _Choice({0: 'Change color on original qqe', 1: 'Change color on slope change', 2: 'Change color on OB/OS level', 3: 'Change color on level 50 cross'}, default=0),  # Color changing mode
    }

