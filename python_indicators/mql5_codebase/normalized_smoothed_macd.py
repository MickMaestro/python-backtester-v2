"""Normalized smoothed MACD — converted from MQL5: MQL5 Indicators/Normalized smoothed MACD/Normalized smoothed MACD.mq5

Normalized MACD
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 2}, 'types': {1: 8, 2: 8}, 'colors': {1: [16748574, 6333684], 2: [16748574, 6333684]}, 'widths': {1: 2}, 'styles': {2: 2}, 'labels': {1: 'Normalized MACD', 2: 'Normalized MACD signal line'}, 'levels': [], 'description': ['Normalized MACD'], 'name': 'Normalized smoothed MACD', 'source': 'MQL5 Indicators/Normalized smoothed MACD/Normalized smoothed MACD.mq5', 'folder': 'Normalized smoothed MACD', 'inputs': [{'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 12, 'label': 'MACD fast period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 26, 'label': 'MACD slow period', 'sinput': False}, {'mql': 'inpMacdSignal', 'py': 'inpMacdSignal', 'param': 'inpMacdSignal', 'type': 'int', 'default': 9, 'label': 'Signal period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpSmoothPeriod', 'py': 'inpSmoothPeriod', 'param': 'inpSmoothPeriod', 'type': 'int', 'default': 5, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'inpNormPeriod', 'py': 'inpNormPeriod', 'param': 'inpNormPeriod', 'type': 'int', 'default': 20, 'label': 'Normalization period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
ª_alphaf = 0.0
ª_alphas = 0.0
ª_alphasig = 0.0
ª_alphasm = 0.0

def OnInit():
    global ª_alphaf, ª_alphas, ª_alphasig, ª_alphasm
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, sig, INDICATOR_DATA)
    SetIndexBuffer(3, sigc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, macd, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, emaf, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, emas, INDICATOR_CALCULATIONS)
    ª_alphaf = _fdiv(2.0, 1.0 + MathMax(inpFastPeriod, 1))
    ª_alphas = _fdiv(2.0, 1.0 + MathMax(inpSlowPeriod, 1))
    ª_alphasig = _fdiv(2.0, 1.0 + MathMax(inpMacdSignal, 1))
    ª_alphasm = _fdiv(2.0, 1.0 + MathMax(inpSmoothPeriod, 1))
    IndicatorSetString(INDICATOR_SHORTNAME, 'Normalized MACD (' + _str(inpFastPeriod) + ',' + _str(inpSlowPeriod) + ',' + _str(inpMacdSignal) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
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
        emaf[i] = ((emaf[i - 1] + (ª_alphaf * (_price - emaf[i - 1]))) if (i > 0) else _price)
        emas[i] = ((emas[i - 1] + (ª_alphas * (_price - emas[i - 1]))) if (i > 0) else _price)
        macd[i] = emaf[i] - emas[i]
        _start = ((i - inpNormPeriod + 1) if (i > inpNormPeriod) else 0)
        _max = macd[ArrayMaximum(macd, _start, inpNormPeriod)]
        _min = macd[ArrayMinimum(macd, _start, inpNormPeriod)]
        _nval = ((_fdiv(2.0 * (macd[i] - _min), _max - _min) - 1.0) if (_min != _max) else 0)
        val[i] = ((val[i - 1] + (ª_alphasm * (_nval - val[i - 1]))) if (i > 0) else 0)
        valc[i] = ((0 if (val[i] > val[i - 1]) else 1) if (i > 0) else 0)
        sig[i] = ((sig[i - 1] + (ª_alphasig * (val[i] - sig[i - 1]))) if (i > 0) else 0)
        sigc[i] = (0 if (val[i] > sig[i]) else 1)
        i += 1
    return rates_total


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

