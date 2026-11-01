"""Stochastic of filtered price — converted from MQL5: MQL5 Indicators/Stochastic of filtered price/Stochastic of filtered price.mq5

Stochastic of filtered price
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Stochastic of filtered price'}, 'levels': [], 'description': ['Stochastic of filtered price'], 'name': 'Stochastic of filtered price', 'source': 'MQL5 Indicators/Stochastic of filtered price/Stochastic of filtered price.mq5', 'folder': 'Stochastic of filtered price', 'inputs': [{'mql': 'inpStoPeriod', 'py': 'inpStoPeriod', 'param': 'inpStoPeriod', 'type': 'int', 'default': 32, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'inpStoSlowing', 'py': 'inpStoSlowing', 'param': 'inpStoSlowing', 'type': 'int', 'default': 3, 'label': 'Stochastic slowing', 'sinput': False}, {'mql': 'inpFilPeriod', 'py': 'inpFilPeriod', 'param': 'inpFilPeriod', 'type': 'int', 'default': 0, 'label': 'Filter period (0 for same as stochastic period)', 'sinput': False}, {'mql': 'inpFilSize', 'py': 'inpFilSize', 'param': 'inpFilSize', 'type': 'double', 'default': 2.0, 'label': 'Filter size', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpStoPeriod = _input('inpStoPeriod', 32)  # Stochastic period
inpStoSlowing = _input('inpStoSlowing', 3)  # Stochastic slowing
inpFilPeriod = _input('inpFilPeriod', 0)  # Filter period (0 for same as stochastic period)
inpFilSize = _input('inpFilSize', 2.0)  # Filter size
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
ª_filPeriod = 0

class cStochasticWork(MqlObject):
    _q_fields = ('originalPeriod', 'period', 'slowing', 'slowingSize', 'maxArray', 'minArray', 'diffh', 'diffl', 'sumh', 'suml')
    def __init__(self):
        self.originalPeriod = 0
        self.period = 0
        self.slowing = 0
        self.slowingSize = 0
        self.maxArray = Arr(0, 0.0)
        self.minArray = Arr(0, 0.0)
        self.diffh = Arr(0, 0.0)
        self.diffl = Arr(0, 0.0)
        self.sumh = Arr(0, 0.0)
        self.suml = Arr(0, 0.0)
        self.originalPeriod = -1
        return
    def _q_dtor(self):
        ArrayFree(self.maxArray)
        ArrayFree(self.minArray)
        ArrayFree(self.diffh)
        ArrayFree(self.diffl)
        ArrayFree(self.sumh)
        ArrayFree(self.suml)
        return

class sFilterArrayStruct(MqlObject):
    _q_fields = ('value', 'change', 'power', 'summc', 'summp')
    def __init__(self, *args):
        self.value = 0.0
        self.change = 0.0
        self.power = 0.0
        self.summc = 0.0
        self.summp = 0.0

def OnInit():
    global ª_filPeriod
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    ª_filPeriod = (inpFilPeriod if (inpFilPeriod > 0) else inpStoPeriod)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 100)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stochastic of filtered price (' + _str(inpStoPeriod) + ',' + _str(inpStoSlowing) + ',' + _str(ª_filPeriod) + ',' + _str(inpFilSize) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
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
        _price = iFilter(_price, inpFilSize, ª_filPeriod, i, rates_total)
        val[i] = iStoch(_price, _price, _price, inpStoPeriod, inpStoSlowing, i)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iStoch(price, priceHigh, priceLow, period, slowing, i, instance=0):
    if _s_iStoch_m_work[instance].originalPeriod != period:
        _s_iStoch_m_work[instance].originalPeriod = period
        _s_iStoch_m_work[instance].period = (period if (period > 0) else 1)
        _s_iStoch_m_work[instance].slowing = (slowing if (slowing > 0) else 1)
        _s_iStoch_m_work[instance].slowingSize = _s_iStoch_m_work[instance].slowing + 32
        ArrayResize(_s_iStoch_m_work[instance].maxArray, _s_iStoch_m_work[instance].period)
        ArrayInitialize(_s_iStoch_m_work[instance].maxArray, priceHigh)
        ArrayResize(_s_iStoch_m_work[instance].minArray, _s_iStoch_m_work[instance].period)
        ArrayInitialize(_s_iStoch_m_work[instance].minArray, priceLow)
        ArrayResize(_s_iStoch_m_work[instance].diffh, _s_iStoch_m_work[instance].slowingSize)
        ArrayInitialize(_s_iStoch_m_work[instance].diffh, 0)
        ArrayResize(_s_iStoch_m_work[instance].diffl, _s_iStoch_m_work[instance].slowingSize)
        ArrayInitialize(_s_iStoch_m_work[instance].diffl, 0)
        ArrayResize(_s_iStoch_m_work[instance].sumh, _s_iStoch_m_work[instance].slowingSize)
        ArrayInitialize(_s_iStoch_m_work[instance].sumh, 0)
        ArrayResize(_s_iStoch_m_work[instance].suml, _s_iStoch_m_work[instance].slowingSize)
        ArrayInitialize(_s_iStoch_m_work[instance].suml, 0)
    _pos = _imod(i, _s_iStoch_m_work[instance].period)
    _s_iStoch_m_work[instance].minArray[_pos] = priceLow
    _s_iStoch_m_work[instance].maxArray[_pos] = priceHigh
    min_ = _s_iStoch_m_work[instance].minArray[ArrayMinimum(_s_iStoch_m_work[instance].minArray)]
    max_ = _s_iStoch_m_work[instance].maxArray[ArrayMaximum(_s_iStoch_m_work[instance].maxArray)]
    _pos = _imod(i, _s_iStoch_m_work[instance].slowingSize)
    _s_iStoch_m_work[instance].diffh[_pos] = max_ - min_
    _s_iStoch_m_work[instance].diffl[_pos] = price - min_
    if i > _s_iStoch_m_work[instance].slowing:
        _posp = _imod(i - 1, _s_iStoch_m_work[instance].slowingSize)
        _posf = _imod(i - _s_iStoch_m_work[instance].slowing, _s_iStoch_m_work[instance].slowingSize)
        _s_iStoch_m_work[instance].sumh[_pos] = _s_iStoch_m_work[instance].sumh[_posp] + _s_iStoch_m_work[instance].diffh[_pos] - _s_iStoch_m_work[instance].diffh[_posf]
        _s_iStoch_m_work[instance].suml[_pos] = _s_iStoch_m_work[instance].suml[_posp] + _s_iStoch_m_work[instance].diffl[_pos] - _s_iStoch_m_work[instance].diffl[_posf]
    else:
        _s_iStoch_m_work[instance].sumh[_pos] = _s_iStoch_m_work[instance].diffh[_pos]
        _s_iStoch_m_work[instance].suml[_pos] = _s_iStoch_m_work[instance].diffl[_pos]
        k = 1
        _posp = _pos - 1
        while k < _s_iStoch_m_work[instance].slowing:
            if _posp < 0:
                _posp += _s_iStoch_m_work[instance].slowingSize
            _s_iStoch_m_work[instance].sumh[_pos] += _s_iStoch_m_work[instance].diffh[_posp]
            _s_iStoch_m_work[instance].suml[_pos] += _s_iStoch_m_work[instance].diffl[_posp]
            k += 1
            _posp -= 1
    return (_fdiv(100.0 * _s_iStoch_m_work[instance].suml[_pos], _s_iStoch_m_work[instance].sumh[_pos]) if (_s_iStoch_m_work[instance].sumh[_pos] != 0.0) else 0)

def iFilter(value, filter_, period, i, bars, instance=0):
    global _s_iFilter_m_arraySize
    if _s_iFilter_m_arraySize < bars:
        _res = ArrayResize(_s_iFilter_m_array, bars + 500)
        if _res < bars:
            return 0.0
        _s_iFilter_m_arraySize = _res
    _s_iFilter_m_array[i][instance].value = value
    _change = ((_s_iFilter_m_array[i][instance].value - _s_iFilter_m_array[i - 1][instance].value) if (i > 0) else 0)
    _s_iFilter_m_array[i][instance].change = (_change if (_change > 0) else (-_change))
    if i > period:
        _s_iFilter_m_array[i][instance].summc = _s_iFilter_m_array[i - 1][instance].summc + _s_iFilter_m_array[i][instance].change - _s_iFilter_m_array[i - period][instance].change
        _s_iFilter_m_array[i][instance].power = (_s_iFilter_m_array[i][instance].change - _fdiv(_s_iFilter_m_array[i][instance].summc, float(period))) * (_s_iFilter_m_array[i][instance].change - _fdiv(_s_iFilter_m_array[i][instance].summc, float(period)))
        _s_iFilter_m_array[i][instance].summp = _s_iFilter_m_array[i - 1][instance].summp + _s_iFilter_m_array[i][instance].power - _s_iFilter_m_array[i - period][instance].power
    else:
        _s_iFilter_m_array[i][instance].summp = 0.0
        _s_iFilter_m_array[i][instance].summc = _s_iFilter_m_array[i][instance].summp
        k = 0
        while k < period and i >= k:
            _s_iFilter_m_array[i][instance].summc += _s_iFilter_m_array[i - k][instance].change
            k += 1
        _s_iFilter_m_array[i][instance].power = (_s_iFilter_m_array[i][instance].change - _fdiv(_s_iFilter_m_array[i][instance].summc, float(period))) * (_s_iFilter_m_array[i][instance].change - _fdiv(_s_iFilter_m_array[i][instance].summc, float(period)))
        k = 0
        while k < period and i >= k:
            _s_iFilter_m_array[i][instance].summp += _s_iFilter_m_array[i - k][instance].power
            k += 1
    if (i > 0 and filter_ > 0) and _s_iFilter_m_array[i][instance].change < (filter_ * MathSqrt(_fdiv(_s_iFilter_m_array[i][instance].summp, float(period)))):
        _s_iFilter_m_array[i][instance].value = _s_iFilter_m_array[i - 1][instance].value
    return _s_iFilter_m_array[i][instance].value

# ---- static local variables
_s_iStoch_m_work = Arr(1, 0, dyn=False, factory=cStochasticWork)
_s_iFilter_m_array = Arr(0, 0, factory=sFilterArrayStruct, dims=(1,))
_s_iFilter_m_arraySize = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticOfFilteredPrice(_MQL5Indicator):
    name = 'Stochastic of filtered price'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpStoPeriod': 32,  # Stochastic period
        'inpStoSlowing': 3,  # Stochastic slowing
        'inpFilPeriod': 0,  # Filter period (0 for same as stochastic period)
        'inpFilSize': 2.0,  # Filter size
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

