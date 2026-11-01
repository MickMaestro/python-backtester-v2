"""M-oscillator (extended) — converted from MQL5: MQL5 Indicators/M-oscillator - extended/M-oscillator (extended).mq5

m_oscillator
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [12632256, 7451452, 17919], 2: [12632256]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['m_oscillator'], 'name': 'M-oscillator (extended)', 'source': 'MQL5 Indicators/M-oscillator - extended/M-oscillator (extended).mq5', 'folder': 'M-oscillator - extended', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpPeriod1', 'py': 'inpPeriod1', 'param': 'inpPeriod1', 'type': 'int', 'default': 5, 'label': 'Smoothing period 1', 'sinput': False}, {'mql': 'inpPeriod2', 'py': 'inpPeriod2', 'param': 'inpPeriod2', 'type': 'int', 'default': 3, 'label': 'Smoothing period 2', 'sinput': False}, {'mql': 'inpPeriod3', 'py': 'inpPeriod3', 'param': 'inpPeriod3', 'type': 'int', 'default': 3, 'label': 'Signal period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpLevelUp', 'py': 'inpLevelUp', 'param': 'inpLevelUp', 'type': 'double', 'default': 10.0, 'label': 'Upper level', 'sinput': False}, {'mql': 'inpLevelDn', 'py': 'inpLevelDn', 'param': 'inpLevelDn', 'type': 'double', 'default': -10.0, 'label': 'Lower level', 'sinput': False}, {'mql': 'inpColorOn', 'py': 'inpColorOn', 'param': 'inpColorOn', 'type': 'int', 'default': 2, 'label': 'Color change mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorOn
coloron_slopeChange = 0
coloron_levelsCross = 1
coloron_signalCross = 2
coloron_zeroCross = 3
_enum('enColorOn', {0: 'coloron_slopeChange', 1: 'coloron_levelsCross', 2: 'coloron_signalCross', 3: 'coloron_zeroCross'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpPeriod1 = _input('inpPeriod1', 5)  # Smoothing period 1
inpPeriod2 = _input('inpPeriod2', 3)  # Smoothing period 2
inpPeriod3 = _input('inpPeriod3', 3)  # Signal period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpLevelUp = _input('inpLevelUp', 10.0)  # Upper level
inpLevelDn = _input('inpLevelDn', -10.0)  # Lower level
inpColorOn = _input('inpColorOn', coloron_signalCross)  # Color change mode
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
signal = Arr(0, 0.0)
_alpha1 = 0.0
_alpha2 = 0.0
_alpha3 = 0.0
_step = 0.0

class sMoscStruct(MqlObject):
    _q_fields = ('price', 'summ', 'ema')
    def __init__(self, *args):
        self.price = 0.0
        self.summ = 0.0
        self.ema = 0.0

def OnInit():
    global _alpha1, _alpha2, _alpha3, _step
    SetIndexBuffer(0, val)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, signal)
    _alpha1 = _fdiv(2.0, 1.0 + (inpPeriod1 if (inpPeriod1 > 1) else 1))
    _alpha2 = _fdiv(2.0, 1.0 + (inpPeriod2 if (inpPeriod2 > 1) else 1))
    _alpha3 = _fdiv(2.0, 1.0 + (inpPeriod3 if (inpPeriod3 > 1) else 1))
    _step = 14 / float((inpPeriod if (inpPeriod > 1) else 1))
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, inpLevelUp)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, inpLevelDn)
    IndicatorSetString(INDICATOR_SHORTNAME, 'M-Oscillator (extended)(' + _str(inpPeriod) + ')(' + _str(inpPeriod1) + ',' + _str(inpPeriod2) + ',' + _str(inpPeriod3) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_arraySize
    if _s_OnCalculate_m_arraySize < rates_total:
        _s_OnCalculate_m_arraySize = ArrayResize(_s_OnCalculate_m_array, rates_total + 500)
        if _s_OnCalculate_m_arraySize < rates_total:
            return 0
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            _s_OnCalculate_m_array[i].price = close[i]
        elif _sw1 == PRICE_OPEN:
            _s_OnCalculate_m_array[i].price = open[i]
        elif _sw1 == PRICE_HIGH:
            _s_OnCalculate_m_array[i].price = high[i]
        elif _sw1 == PRICE_LOW:
            _s_OnCalculate_m_array[i].price = low[i]
        elif _sw1 == PRICE_MEDIAN:
            _s_OnCalculate_m_array[i].price = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            _s_OnCalculate_m_array[i].price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            _s_OnCalculate_m_array[i].price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            _s_OnCalculate_m_array[i].price = 0.0
        _s_OnCalculate_m_array[i].summ = 0.0
        k = 0
        while k < inpPeriod and i >= k:
            _s_OnCalculate_m_array[i].summ += (_step if (_s_OnCalculate_m_array[i].price > _s_OnCalculate_m_array[i - k].price) else (-_step) if (_s_OnCalculate_m_array[i].price < _s_OnCalculate_m_array[i - k].price) else 0)
            k += 1
        if i > 0:
            _s_OnCalculate_m_array[i].ema = _s_OnCalculate_m_array[i - 1].ema + (_alpha1 * (_s_OnCalculate_m_array[i].summ - _s_OnCalculate_m_array[i - 1].ema))
            val[i] = val[i - 1] + (_alpha2 * (_s_OnCalculate_m_array[i].ema - val[i - 1]))
            signal[i] = signal[i - 1] + (_alpha3 * (val[i] - signal[i - 1]))
            _sw2 = inpColorOn
            if _sw2 == coloron_slopeChange:
                valc[i] = (1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else 0)
            elif _sw2 == coloron_levelsCross:
                valc[i] = (1 if (val[i] > inpLevelUp) else 2 if (val[i] < inpLevelDn) else 0)
            elif _sw2 == coloron_signalCross:
                valc[i] = (1 if (val[i] > signal[i]) else 2 if (val[i] < signal[i]) else 0)
            elif _sw2 == coloron_zeroCross:
                valc[i] = (1 if (val[i] > 0) else 2 if (val[i] < 0) else 0)
        else:
            valc[i] = 0.0
            signal[i] = valc[i]
            val[i] = signal[i]
        i += 1
    return i

# ---- static local variables
_s_OnCalculate_m_array = Arr(0, 0, factory=sMoscStruct)
_s_OnCalculate_m_arraySize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MOscillatorExtended(_MQL5Indicator):
    name = 'M-oscillator (extended)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpPeriod1': 5,  # Smoothing period 1
        'inpPeriod2': 3,  # Smoothing period 2
        'inpPeriod3': 3,  # Signal period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpLevelUp': 10.0,  # Upper level
        'inpLevelDn': -10.0,  # Lower level
        'inpColorOn': _Choice({0: 'Change color on slope change', 1: 'Change color on levels cross', 2: 'Change color on signal line cross', 3: 'Change color on zero line cross'}, default=2),  # Color change mode
    }

