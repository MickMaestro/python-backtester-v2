"""Price Momentum Oscillator — converted from MQL5: MQL5 Indicators/Price momentum oscillator/Price Momentum Oscillator.mq5

Copyright: copyright© mladen 2020; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'copyright© mladen 2020', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [16748574, 5275647], 2: [255]}, 'widths': {1: 2}, 'styles': {2: 2}, 'labels': {1: 'PMO', 2: 'Signal'}, 'levels': [], 'description': [], 'name': 'Price Momentum Oscillator', 'source': 'MQL5 Indicators/Price momentum oscillator/Price Momentum Oscillator.mq5', 'folder': 'Price momentum oscillator', 'inputs': [{'mql': 'inpPeriod1', 'py': 'inpPeriod1', 'param': 'inpPeriod1', 'type': 'int', 'default': 35, 'label': 'Period', 'sinput': False}, {'mql': 'inpPeriod2', 'py': 'inpPeriod2', 'param': 'inpPeriod2', 'type': 'int', 'default': 20, 'label': 'Period 2', 'sinput': False}, {'mql': 'inpPeriodSignal', 'py': 'inpPeriodSignal', 'param': 'inpPeriodSignal', 'type': 'int', 'default': 10, 'label': 'Signal period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpColorMode', 'py': 'inpColorMode', 'param': 'inpColorMode', 'type': 'int', 'default': 1, 'label': 'Color mode :', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorMode
col_slope = 0
col_signal = 1
col_zero = 2
_enum('enColorMode', {0: 'col_slope', 1: 'col_signal', 2: 'col_zero'})

# ---- inputs and global variables
inpPeriod1 = _input('inpPeriod1', 35)  # Period
inpPeriod2 = _input('inpPeriod2', 20)  # Period 2
inpPeriodSignal = _input('inpPeriodSignal', 10)  # Signal period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpColorMode = _input('inpColorMode', col_signal)  # Color mode :
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
vals = Arr(0, 0.0)
_alpha1 = 0.0
_alpha2 = 0.0
_alphas = 0.0

class sWorkStruc(MqlObject):
    _q_fields = ('price', 'roc', 'EmaOfRoc', 'PmoOsc')
    def __init__(self, *args):
        self.price = 0.0
        self.roc = 0.0
        self.EmaOfRoc = 0.0
        self.PmoOsc = 0.0

def OnInit():
    global _alpha1, _alpha2, _alphas
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, vals, INDICATOR_DATA)
    _alpha1 = _fdiv(2.0, MathMax(inpPeriod1, 1))
    _alpha2 = _fdiv(2.0, MathMax(inpPeriod2, 1))
    _alphas = _fdiv(2.0, 1 + MathMax(inpPeriodSignal, 1))
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('Price momentum oscillator (%i,%i,%i)', inpPeriod1, inpPeriod2, inpPeriodSignal))
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_workSize
    limit = prev_calculated - 1
    if limit < 0:
        limit = 0
    if _s_OnCalculate_m_workSize < rates_total:
        _s_OnCalculate_m_workSize = ArrayResize(_s_OnCalculate_m_work, rates_total + 500, 2000)
    for i in range(limit, rates_total):
        _s_OnCalculate_m_work[i].price = getPrice(inpPrice, open, high, low, close, i)
        if i > 0:
            _s_OnCalculate_m_work[i].roc = (_fdiv(_s_OnCalculate_m_work[i].price, _s_OnCalculate_m_work[i - 1].price) - 1) * 100
            _s_OnCalculate_m_work[i].EmaOfRoc = _s_OnCalculate_m_work[i - 1].EmaOfRoc + (_alpha1 * (_s_OnCalculate_m_work[i].roc - _s_OnCalculate_m_work[i - 1].EmaOfRoc))
            _s_OnCalculate_m_work[i].PmoOsc = _s_OnCalculate_m_work[i - 1].PmoOsc + (_alpha2 * (_s_OnCalculate_m_work[i].EmaOfRoc - _s_OnCalculate_m_work[i - 1].PmoOsc))
            val[i] = _s_OnCalculate_m_work[i].PmoOsc
            vals[i] = vals[i - 1] + (_alphas * (val[i] - vals[i - 1]))
            _sw1 = inpColorMode
            if _sw1 == col_signal:
                valc[i] = (0 if (val[i] > vals[i]) else 1)
            elif _sw1 == col_slope:
                valc[i] = (0 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1])
            else:
                valc[i] = (0 if (val[i] > 0) else 1)
        else:
            valc[i] = 0.0
            vals[i] = valc[i]
            val[i] = vals[i]
            _s_OnCalculate_m_work[i].PmoOsc = val[i]
            _s_OnCalculate_m_work[i].EmaOfRoc = _s_OnCalculate_m_work[i].PmoOsc
            _s_OnCalculate_m_work[i].roc = _s_OnCalculate_m_work[i].EmaOfRoc
    return rates_total

def getPrice(price, open, high, low, close, i):
    _sw2 = price
    if _sw2 == PRICE_CLOSE:
        return close[i]
    elif _sw2 == PRICE_HIGH:
        return high[i]
    elif _sw2 == PRICE_LOW:
        return low[i]
    elif _sw2 == PRICE_OPEN:
        return open[i]
    elif _sw2 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw2 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw2 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0

# ---- static local variables
_s_OnCalculate_m_work = Arr(0, 0, factory=sWorkStruc)
_s_OnCalculate_m_workSize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PriceMomentumOscillator(_MQL5Indicator):
    name = 'Price Momentum Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod1': 35,  # Period
        'inpPeriod2': 20,  # Period 2
        'inpPeriodSignal': 10,  # Signal period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpColorMode': _Choice({0: 'change color on slope change', 1: 'change color on signal cross', 2: 'change color on 0 cross'}, default=1),  # Color mode :
    }

