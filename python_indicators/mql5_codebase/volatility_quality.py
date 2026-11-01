"""Volatility quality — converted from MQL5: MQL5 Indicators/Volatility quality/Volatility quality.mq5

Volatility quality
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [12632256, 3329330, 42495]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Volatility quality'}, 'levels': [], 'description': ['Volatility quality'], 'name': 'Volatility quality', 'source': 'MQL5 Indicators/Volatility quality/Volatility quality.mq5', 'folder': 'Volatility quality', 'inputs': [{'mql': 'inpPriceSmoothing', 'py': 'inpPriceSmoothing', 'param': 'inpPriceSmoothing', 'type': 'int', 'default': 5, 'label': 'Price smoothing period', 'sinput': False}, {'mql': 'inpPriceSmoothingMethod', 'py': 'inpPriceSmoothingMethod', 'param': 'inpPriceSmoothingMethod', 'type': 'int', 'default': 3, 'label': 'Price smoothing method', 'sinput': False}, {'mql': 'inpFilter', 'py': 'inpFilter', 'param': 'inpFilter', 'type': 'double', 'default': 20.0, 'label': 'Filter (% of ATR)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPriceSmoothing = _input('inpPriceSmoothing', 5)  # Price smoothing period
inpPriceSmoothingMethod = _input('inpPriceSmoothingMethod', MODE_LWMA)  # Price smoothing method
inpFilter = _input('inpFilter', 20.0)  # Filter (% of ATR)
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
mah = Arr(0, 0.0)
mal = Arr(0, 0.0)
mao = Arr(0, 0.0)
mac = Arr(0, 0.0)
atr = Arr(0, 0.0)
ª_filter = 0.0
ª_maHandleh = 0
ª_maHandlel = 0
ª_maHandleo = 0
ª_maHandlec = 0
ª_atrHandle = 0

def OnInit():
    global ª_atrHandle, ª_filter, ª_maHandlec, ª_maHandleh, ª_maHandlel, ª_maHandleo
    ª_maHandleh = iMA(Symbol(), 0, inpPriceSmoothing, 0, inpPriceSmoothingMethod, PRICE_HIGH)
    if not _checkHandle(ª_maHandleh, 'average of high'):
        return INIT_FAILED
    ª_maHandlel = iMA(Symbol(), 0, inpPriceSmoothing, 0, inpPriceSmoothingMethod, PRICE_LOW)
    if not _checkHandle(ª_maHandlel, 'average of low'):
        return INIT_FAILED
    ª_maHandleo = iMA(Symbol(), 0, inpPriceSmoothing, 0, inpPriceSmoothingMethod, PRICE_OPEN)
    if not _checkHandle(ª_maHandleo, 'average of open'):
        return INIT_FAILED
    ª_maHandlec = iMA(Symbol(), 0, inpPriceSmoothing, 0, inpPriceSmoothingMethod, PRICE_CLOSE)
    if not _checkHandle(ª_maHandlec, 'average of close'):
        return INIT_FAILED
    ª_atrHandle = iATR(Symbol(), 0, inpPriceSmoothing)
    if not _checkHandle(ª_atrHandle, 'ATR'):
        return INIT_FAILED
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, mah, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, mal, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, mao, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, mac, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, atr, INDICATOR_CALCULATIONS)
    ª_filter = inpFilter / 100.0
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volatility quality (' + _str(inpPriceSmoothing) + ', filter ' + _str(inpFilter) + '% of ATR)')
    return 0

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_maHandleh, 0, 0, _copyCount, mah) != _copyCount:
        return prev_calculated
    if CopyBuffer(ª_maHandlel, 0, 0, _copyCount, mal) != _copyCount:
        return prev_calculated
    if CopyBuffer(ª_maHandleo, 0, 0, _copyCount, mao) != _copyCount:
        return prev_calculated
    if CopyBuffer(ª_maHandlec, 0, 0, _copyCount, mac) != _copyCount:
        return prev_calculated
    if CopyBuffer(ª_atrHandle, 0, 0, _copyCount, atr) != _copyCount:
        return prev_calculated
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        if mah[i] == EMPTY_VALUE:
            mah[i] = high[i]
        if mal[i] == EMPTY_VALUE:
            mal[i] = low[i]
        if mao[i] == EMPTY_VALUE:
            mao[i] = open[i]
        if mac[i] == EMPTY_VALUE:
            mac[i] = close[i]
        if atr[i] == EMPTY_VALUE:
            atr[i] = 0.0
        trueRange = (mah[i] if (mah[i] > (mac[i - 1] if (i > 0) else mac[i])) else mac[i - 1] if (i > 0) else mac[i]) - (mal[i] if (mal[i] < (mac[i - 1] if (i > 0) else mac[i])) else mac[i - 1] if (i > 0) else mac[i])
        range_ = mah[i] - mal[i]
        vqi = (((_fdiv(mac[i] - (mac[i - 1] if (i > 0) else mac[i]), trueRange) + _fdiv(mac[i] - mao[i], range_)) * 0.5) if (range_ > 0 and trueRange > 0) else val[i - 1] if (i > 0) else 0)
        val[i] = ((val[i - 1] + ((vqi if (vqi > 0) else (-vqi)) * (mac[i] - (mac[i - 1] if (i > 0) else mac[i]) + mac[i] - mao[i]) * 0.5)) if (i > 0) else 0)
        if ª_filter > 0 and i > 0:
            if ((val[i] - val[i - 1]) if (val[i] > val[i - 1]) else (val[i - 1] - val[i])) < (ª_filter * atr[i]):
                val[i] = val[i - 1]
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return rates_total

def _checkHandle(_handle, _description):
    _size = ArraySize(_s__checkHandle__chkHandles)
    _answer = _handle != INVALID_HANDLE
    if _answer:
        ArrayResize(_s__checkHandle__chkHandles, _size + 1)
        _s__checkHandle__chkHandles[_size] = _handle
    else:
        for i in range(_size - 1, 0 - 1, -1):
            IndicatorRelease(_s__checkHandle__chkHandles[i])
        ArrayResize(_s__checkHandle__chkHandles, 0)
        Alert(_description + ' initialization failed')
    return _answer

# ---- static local variables
_s__checkHandle__chkHandles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolatilityQuality(_MQL5Indicator):
    name = 'Volatility quality'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPriceSmoothing': 5,  # Price smoothing period
        'inpPriceSmoothingMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=3),  # Price smoothing method
        'inpFilter': 20.0,  # Filter (% of ATR)
    }

