"""Generalized DEMA — converted from MQL5: MQL5 Indicators/Generalized DEMA/Generalized DEMA.mq5

Generalized DEMA
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [12632256, 7451452, 36095]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Generalized DEMA'}, 'levels': [], 'description': ['Generalized DEMA'], 'name': 'Generalized DEMA', 'source': 'MQL5 Indicators/Generalized DEMA/Generalized DEMA.mq5', 'folder': 'Generalized DEMA', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'DEMA period', 'sinput': False}, {'mql': 'inpVolume', 'py': 'inpVolume', 'param': 'inpVolume', 'type': 'double', 'default': 0.7, 'label': 'DEMA volume factor', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # DEMA period
inpVolume = _input('inpVolume', 0.7)  # DEMA volume factor
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Generalized DEMA (' + _str(inpPeriod) + ')')

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
        val[i] = iGdema(_price, inpPeriod, inpVolume, i)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iGdema(price, period, volumeFactor, i, _instance=0):
    if _s_iGdema__workCoeff[_instance][0] != period or volumeFactor != _s_iGdema__workCoeff[_instance][2]:
        _s_iGdema__workCoeff[_instance][0] = period
        _s_iGdema__workCoeff[_instance][2] = ((1 if (volumeFactor > 1) else volumeFactor) if (volumeFactor > 0) else 0.01)
        _s_iGdema__workCoeff[_instance][3] = _s_iGdema__workCoeff[_instance][2] + 1
        _s_iGdema__workCoeff[_instance][1] = _fdiv(2.0, 1.0 + (period if (period > 1) else 1))
    _indC = _imod(i, 16)
    if i > 0 and period > 1.0:
        _indP = _imod(i - 1, 16)
        _s_iGdema__workArray[_indC][_instance + 1] = _s_iGdema__workArray[_indP][_instance + 1] + (_s_iGdema__workCoeff[_instance][1] * (price - _s_iGdema__workArray[_indP][_instance + 1]))
        _s_iGdema__workArray[_indC][_instance + 2] = _s_iGdema__workArray[_indP][_instance + 2] + (_s_iGdema__workCoeff[_instance][1] * (_s_iGdema__workArray[_indC][_instance + 1] - _s_iGdema__workArray[_indP][_instance + 2]))
        _s_iGdema__workArray[_indC][_instance] = (_s_iGdema__workArray[_indC][_instance + 1] * _s_iGdema__workCoeff[_instance][3]) - (_s_iGdema__workArray[_indC][_instance + 2] * _s_iGdema__workCoeff[_instance][2])
    else:
        for k in range(0, 3):
            _s_iGdema__workArray[_indC][_instance + k] = price
    return _s_iGdema__workArray[_indC][_instance]

# ---- static local variables
_s_iGdema__workArray = Arr(16, 0.0, dyn=False, dims=(3,))
_s_iGdema__workCoeff = Arr(1, 0.0, dyn=False, dims=(4,))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GeneralizedDEMA(_MQL5Indicator):
    name = 'Generalized DEMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # DEMA period
        'inpVolume': 0.7,  # DEMA volume factor
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

