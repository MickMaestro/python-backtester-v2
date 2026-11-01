"""Normalized smoothed MACD — converted from MQL5: MQL5 Indicators/Normalizied MACD - self adjusting signal/Normalized smoothed MACD.mq5

Normalized MACD
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 2}, 'types': {1: 8, 2: 8}, 'colors': {1: [12632256, 16748574, 6333684], 2: [12632256, 16748574, 6333684]}, 'widths': {1: 2}, 'styles': {2: 2}, 'labels': {1: 'Normalized MACD', 2: 'Normalized MACD signal line'}, 'levels': [], 'description': ['Normalized MACD'], 'name': 'Normalized smoothed MACD', 'source': 'MQL5 Indicators/Normalizied MACD - self adjusting signal/Normalized smoothed MACD.mq5', 'folder': 'Normalizied MACD - self adjusting signal', 'inputs': [{'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 12, 'label': 'MACD fast period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 26, 'label': 'MACD slow period', 'sinput': False}, {'mql': 'inpMacdSignal', 'py': 'inpMacdSignal', 'param': 'inpMacdSignal', 'type': 'int', 'default': 9, 'label': 'Signal period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpSmoothPeriod', 'py': 'inpSmoothPeriod', 'param': 'inpSmoothPeriod', 'type': 'int', 'default': 5, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'inpNormPeriod', 'py': 'inpNormPeriod', 'param': 'inpNormPeriod', 'type': 'int', 'default': 20, 'label': 'Normalization period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpFastPeriod = _input('inpFastPeriod', 12)  # MACD fast period
inpSlowPeriod = _input('inpSlowPeriod', 26)  # MACD slow period
inpMacdSignal = _input('inpMacdSignal', 9)  # Signal period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpSmoothPeriod = _input('inpSmoothPeriod', 5)  # Smoothing period
inpNormPeriod = _input('inpNormPeriod', 20)  # Normalization period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
sig = Arr(0, 0.0)
sigc = Arr(0, 0.0)
macd = Arr(0, 0.0)
emaf = Arr(0, 0.0)
emas = Arr(0, 0.0)
sigu = Arr(0, 0.0)
sigd = Arr(0, 0.0)
ª_alphaf = 0.0
ª_alphas = 0.0
ª_alphasig = 0.0
ª_alphasm = 0.0
ª_normPeriodm1 = 0

def OnInit():
    global ª_alphaf, ª_alphas, ª_alphasig, ª_alphasm, ª_normPeriodm1
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, sig, INDICATOR_DATA)
    SetIndexBuffer(3, sigc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, macd, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, emaf, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, emas, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, sigu, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, sigd, INDICATOR_CALCULATIONS)
    ª_alphaf = _fdiv(2.0, 1.0 + MathMax(inpFastPeriod, 1))
    ª_alphas = _fdiv(2.0, 1.0 + MathMax(inpSlowPeriod, 1))
    ª_alphasig = _fdiv(2.0, 1.0 + MathMax(inpMacdSignal, 1))
    ª_alphasm = _fdiv(2.0, 1.0 + MathMax(inpSmoothPeriod, 1))
    ª_normPeriodm1 = ((inpNormPeriod - 1) if (inpNormPeriod > 1) else 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Normalized MACD (' + _str(inpFastPeriod) + ',' + _str(inpSlowPeriod) + ',' + _str(inpMacdSignal) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_i, _s_OnCalculate_prev_max, _s_OnCalculate_prev_min
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _price = 0.0
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            _price = close[i]
        elif _sw1 == PRICE_OPEN:
            _price = open[i]
        elif _sw1 == PRICE_HIGH:
            _price = high[i]
        elif _sw1 == PRICE_LOW:
            _price = low[i]
        elif _sw1 == PRICE_MEDIAN:
            _price = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            _price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            _price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            _price = 0.0
        if i > 0:
            emaf[i] = emaf[i - 1] + (ª_alphaf * (_price - emaf[i - 1]))
            emas[i] = emas[i - 1] + (ª_alphas * (_price - emas[i - 1]))
        else:
            emas[i] = _price
            emaf[i] = emas[i]
        macd[i] = emaf[i] - emas[i]
        if _s_OnCalculate_prev_i != i:
            _start = i - inpNormPeriod + 1
            if _start < 0:
                _start = 0
            _s_OnCalculate_prev_max = macd[ArrayMaximum(macd, _start, ª_normPeriodm1)]
            _s_OnCalculate_prev_min = macd[ArrayMinimum(macd, _start, ª_normPeriodm1)]
            _s_OnCalculate_prev_i = i
        max_ = (macd[i] if (macd[i] > _s_OnCalculate_prev_max) else _s_OnCalculate_prev_max)
        min_ = (macd[i] if (macd[i] < _s_OnCalculate_prev_min) else _s_OnCalculate_prev_min)
        nval = ((_fdiv(2.0 * (macd[i] - min_), max_ - min_) - 1.0) if (min_ != max_) else 0)
        if i > 0:
            val[i] = val[i - 1] + (ª_alphasm * (nval - val[i - 1]))
            sigu[i] = ((sigu[i - 1] + (ª_alphasig * (val[i] - sigu[i - 1]))) if (val[i] > 0) else sigu[i - 1])
            sigd[i] = ((sigd[i - 1] + (ª_alphasig * (val[i] - sigd[i - 1]))) if (val[i] < 0) else sigd[i - 1])
            sig[i] = (sigu[i - 1] if (val[i] > 0) else sigd[i])
        else:
            val[i] = 0.0
            sig[i] = val[i]
            sigd[i] = sig[i]
            sigu[i] = sigd[i]
        valc[i] = (1 if (val[i] > sigu[i]) else 2 if (val[i] < sigd[i]) else 0)
        sigc[i] = valc[i]
        i += 1
    return i

# ---- static local variables
_s_OnCalculate_prev_i = -1
_s_OnCalculate_prev_max = 0.0
_s_OnCalculate_prev_min = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NormalizedSmoothedMACD(_MQL5Indicator):
    name = 'Normalized smoothed MACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFastPeriod': 12,  # MACD fast period
        'inpSlowPeriod': 26,  # MACD slow period
        'inpMacdSignal': 9,  # Signal period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpSmoothPeriod': 5,  # Smoothing period
        'inpNormPeriod': 20,  # Normalization period
    }

