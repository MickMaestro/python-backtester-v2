"""Nadaraya-Watson estimator — converted from MQL5: MQL5 Indicators/Nadaraya-Watson estimator/Nadaraya-Watson estimator.mq5

Nadaraya-Watson estimator
Based on work published by luxAlgo
Copyright: © mladen, 2021; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2021', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16760576, 5275647]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Estimator'}, 'levels': [], 'description': ['Nadaraya-Watson estimator', 'Based on work published by luxAlgo'], 'name': 'Nadaraya-Watson estimator', 'source': 'MQL5 Indicators/Nadaraya-Watson estimator/Nadaraya-Watson estimator.mq5', 'folder': 'Nadaraya-Watson estimator', 'inputs': [{'mql': 'inpBandWidth', 'py': 'inpBandWidth', 'param': 'inpBandWidth', 'type': 'double', 'default': 8.0, 'label': 'Band width', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpBarsToCalculate', 'py': 'inpBarsToCalculate', 'param': 'inpBarsToCalculate', 'type': 'int', 'default': 500, 'label': 'Bars to calculate for estimations', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpBandWidth = _input('inpBandWidth', 8.0)  # Band width
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpBarsToCalculate = _input('inpBarsToCalculate', 500)  # Bars to calculate for estimations
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class sWorkStruct(MqlObject):
    _q_fields = ('price',)
    def __init__(self, *args):
        self.price = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_workSize
    _limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    _barsToCaclulate = MathMin(inpBarsToCalculate, rates_total)
    if _s_OnCalculate_m_workSize < rates_total:
        _s_OnCalculate_m_workSize = ArrayResize(_s_OnCalculate_m_work, rates_total + 500, 2000)
    for i in range(_limit, rates_total):
        _s_OnCalculate_m_work[i].price = iGetPrice(inpPrice, open, high, low, close, i)
    for i in range(0, _barsToCaclulate):
        sum_ = 0.0
        sumw = 0.0
        for j in range(0, _barsToCaclulate):
            w = exp(-_fdiv(pow(i - j, 2), inpBandWidth * inpBandWidth * 2.0))
            sum_ += _s_OnCalculate_m_work[rates_total - j - 1].price * w
            sumw += w
        val[rates_total - i - 1] = _fdiv(sum_, sumw)
    for i in range(rates_total - _barsToCaclulate, rates_total):
        valc[i] = ((0 if (val[i] > val[i - 1]) else 1) if (i > 0) else 0)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, rates_total - _barsToCaclulate)
    return rates_total

def iGetPrice(price, open, high, low, close, i):
    _sw1 = price
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

# ---- static local variables
_s_OnCalculate_m_work = Arr(0, 0, factory=sWorkStruct)
_s_OnCalculate_m_workSize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NadarayaWatsonEstimator(_MQL5Indicator):
    name = 'Nadaraya-Watson estimator'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpBandWidth': 8.0,  # Band width
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpBarsToCalculate': 500,  # Bars to calculate for estimations
    }

