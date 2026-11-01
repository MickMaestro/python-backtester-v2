"""Volume weighted awesome oscillator — converted from MQL5: MQL5 Indicators/Volume weighted awesome oscillator/Volume weighted awesome oscillator.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [3329330, 7451452, 42495, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Volume weighted awesome oscillator'}, 'levels': [], 'description': [], 'name': 'Volume weighted awesome oscillator', 'source': 'MQL5 Indicators/Volume weighted awesome oscillator/Volume weighted awesome oscillator.mq5', 'folder': 'Volume weighted awesome oscillator', 'inputs': [{'mql': 'inpVolume', 'py': 'inpVolume', 'param': 'inpVolume', 'type': 'int', 'default': 0, 'label': 'Volume to use', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpVolume = _input('inpVolume', VOLUME_TICK)  # Volume to use
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class sVwmaArrayStruct(MqlObject):
    _q_fields = ('price', 'volume', 'sump', 'sumv')
    def __init__(self, *args):
        self.price = 0.0
        self.volume = 0.0
        self.sump = 0.0
        self.sumv = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volume weighted AO')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        _price = (high[i] + low[i]) / 2.0
        _volume = (float(tick_volume[i]) if (inpVolume == VOLUME_TICK) else float(volume[i]))
        val[i] = iVwma(_price, _volume, 5, i, rates_total, 0) - iVwma(_price, _volume, 34, i, rates_total, 1)
        valc[i] = (((0 if (val[i] > val[i - 1]) else 1) if (val[i] > 0) else 2 if (val[i] < val[i - 1]) else 3) if (i > 0) else 0)
        i += 1
    return i

def iVwma(price, volume, period, i, bars, instance=0):
    global _s_iVwma_m_arraySize
    if _s_iVwma_m_arraySize < bars:
        _res = ArrayResize(_s_iVwma_m_array, bars + 500)
        if _res <= bars:
            return 0.0
        _s_iVwma_m_arraySize = _res
    if volume == 0:
        volume = 1.0
    _s_iVwma_m_array[i][instance].price = volume * price
    _s_iVwma_m_array[i][instance].volume = volume
    if i > period:
        _s_iVwma_m_array[i][instance].sump = _s_iVwma_m_array[i - 1][instance].sump + _s_iVwma_m_array[i][instance].price - _s_iVwma_m_array[i - period][instance].price
        _s_iVwma_m_array[i][instance].sumv = _s_iVwma_m_array[i - 1][instance].sumv + volume - _s_iVwma_m_array[i - period][instance].volume
    else:
        _s_iVwma_m_array[i][instance].sump = _s_iVwma_m_array[i][instance].price
        _s_iVwma_m_array[i][instance].sumv = _s_iVwma_m_array[i][instance].volume
        k = 1
        while k < period and i >= k:
            _s_iVwma_m_array[i][instance].sump += _s_iVwma_m_array[i - k][instance].price
            _s_iVwma_m_array[i][instance].sumv += _s_iVwma_m_array[i - k][instance].volume
            k += 1
    return _fdiv(_s_iVwma_m_array[i][instance].sump, _s_iVwma_m_array[i][instance].sumv)

# ---- static local variables
_s_iVwma_m_array = Arr(0, 0, factory=sVwmaArrayStruct, dims=(2,))
_s_iVwma_m_arraySize = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolumeWeightedAwesomeOscillator(_MQL5Indicator):
    name = 'Volume weighted awesome oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpVolume': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volume to use
    }

