"""Blau - tsi trade — converted from MQL5: MQL5 Indicators/True Strength Index trade/Blau - tsi trade.mq5

True Strength Index Trade (William Blau)
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 7, 2: 8}, 'colors': {1: [15656678, 15132398], 2: [12632256, 16760576, 6333684]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'filling', 2: 'TSI - trade'}, 'levels': [], 'description': ['True Strength Index Trade (William Blau)'], 'name': 'Blau - tsi trade', 'source': 'MQL5 Indicators/True Strength Index trade/Blau - tsi trade.mq5', 'folder': 'True Strength Index trade', 'inputs': [{'mql': 'inpPeriod1', 'py': 'inpPeriod1', 'param': 'inpPeriod1', 'type': 'int', 'default': 25, 'label': 'True strength index momentum smoothing period', 'sinput': False}, {'mql': 'inpPeriod2', 'py': 'inpPeriod2', 'param': 'inpPeriod2', 'type': 'int', 'default': 13, 'label': 'True strength index smoothing period 2', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod1 = _input('inpPeriod1', 25)  # True strength index momentum smoothing period
inpPeriod2 = _input('inpPeriod2', 13)  # True strength index smoothing period 2
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
valr = Arr(0, 0.0)
valfu = Arr(0, 0.0)
valfd = Arr(0, 0.0)
prices = Arr(0, 0.0)
workEma = Arr(6, 0.0, dyn=False, dims=(4,))

def OnInit():
    SetIndexBuffer(0, valfu, INDICATOR_DATA)
    SetIndexBuffer(1, valfd, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, prices, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, valr, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'True strength index trade (' + _str(inpPeriod1) + ',' + _str(inpPeriod2) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            prices[i] = close[i]
        elif _sw1 == PRICE_OPEN:
            prices[i] = open[i]
        elif _sw1 == PRICE_HIGH:
            prices[i] = high[i]
        elif _sw1 == PRICE_LOW:
            prices[i] = low[i]
        elif _sw1 == PRICE_MEDIAN:
            prices[i] = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            prices[i] = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            prices[i] = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            prices[i] = 0.0
        _momentum = ((prices[i] - prices[i - 1]) if (i > 0) else 0)
        _momentua = (_momentum if (_momentum > 0) else (-_momentum))
        avg = iEma(iEma(_momentum, inpPeriod1, i, 0), inpPeriod2, i, 1)
        ava = iEma(iEma(_momentua, inpPeriod1, i, 2), inpPeriod2, i, 3)
        valr[i] = (_fdiv(100.0 * avg, ava) if (ava != 0) else 0)
        valc[i] = ((1 if (valr[i] > valr[i - 1] and valr[i] > 0) else 2 if (valr[i] < valr[i - 1] and valr[i] < 0) else 0) if (i > 0) else 0)
        val[i] = (valr[i] if (valc[i] == 1) else valr[i] if (valc[i] == 2) else 0)
        valfu[i] = val[i]
        valfd[i] = 0.0
        i += 1
    return i

def iEma(price, period, i, _inst=0):
    _indC = _imod(i, 6)
    _indP = _imod(i - 1, 6)
    if i > 0 and period > 1:
        workEma[_indC][_inst] = workEma[_indP][_inst] + (_fdiv(2.0, 1.0 + period) * (price - workEma[_indP][_inst]))
    else:
        workEma[_indC][_inst] = price
    return workEma[_indC][_inst]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BlauTsiTrade(_MQL5Indicator):
    name = 'Blau - tsi trade'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod1': 25,  # True strength index momentum smoothing period
        'inpPeriod2': 13,  # True strength index smoothing period 2
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

