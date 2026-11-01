"""Stochastic of average — converted from MQL5: MQL5 Indicators/Stochastic of average(s)/Stochastic of average.mq5

Stochastic of one of 4 types of averages
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Stochastic of average'}, 'levels': [], 'description': ['Stochastic of one of 4 types of averages'], 'name': 'Stochastic of average', 'source': 'MQL5 Indicators/Stochastic of average(s)/Stochastic of average.mq5', 'folder': 'Stochastic of average(s)', 'inputs': [{'mql': 'inpStoPeriod', 'py': 'inpStoPeriod', 'param': 'inpStoPeriod', 'type': 'int', 'default': 32, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'inpStoSlowing', 'py': 'inpStoSlowing', 'param': 'inpStoSlowing', 'type': 'int', 'default': 3, 'label': 'Stochastic slowing', 'sinput': False}, {'mql': 'inpAvgPeriod', 'py': 'inpAvgPeriod', 'param': 'inpAvgPeriod', 'type': 'int', 'default': 14, 'label': 'Average period', 'sinput': False}, {'mql': 'inpAvgMethod', 'py': 'inpAvgMethod', 'param': 'inpAvgMethod', 'type': 'int', 'default': 1, 'label': 'Average method', 'sinput': False}, {'mql': 'inpAvgPrice', 'py': 'inpAvgPrice', 'param': 'inpAvgPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpStoPeriod = _input('inpStoPeriod', 32)  # Stochastic period
inpStoSlowing = _input('inpStoSlowing', 3)  # Stochastic slowing
inpAvgPeriod = _input('inpAvgPeriod', 14)  # Average period
inpAvgMethod = _input('inpAvgMethod', MODE_EMA)  # Average method
inpAvgPrice = _input('inpAvgPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
avg = Arr(0, 0.0)
ª_maNames = Arr.of(['SMA', 'EMA', 'SMMA', 'LWMA'], fill="")
ª_maHandle = 0
ª_maPeriod = 0

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

def OnInit():
    global ª_maHandle, ª_maPeriod
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, avg, INDICATOR_CALCULATIONS)
    ª_maPeriod = (inpAvgPeriod if (inpAvgPeriod > 1) else 1)
    ª_maHandle = iMA(Symbol(), 0, ª_maPeriod, 0, inpAvgMethod, inpAvgPrice)
    if not _checkHandle(ª_maHandle, 'Average'):
        return INIT_FAILED
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 100)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stochastic of ' + ª_maNames[inpAvgMethod] + ' (' + _str(inpStoPeriod) + ',' + _str(inpStoSlowing) + ',' + _str(ª_maPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_maHandle, 0, 0, _copyCount, avg) != _copyCount:
        return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        if avg[i] == EMPTY_VALUE:
            avg[i] = close[i]
        val[i] = iStoch(avg[i], avg[i], avg[i], inpStoPeriod, inpStoSlowing, i)
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

def _checkHandle(_handle, _description):
    _size = ArraySize(_s__checkHandle__chandles)
    _answer = _handle != INVALID_HANDLE
    if _answer:
        ArrayResize(_s__checkHandle__chandles, _size + 1)
        _s__checkHandle__chandles[_size] = _handle
    else:
        for i in range(_size - 1, 0 - 1, -1):
            IndicatorRelease(_s__checkHandle__chandles[i])
        ArrayResize(_s__checkHandle__chandles, 0)
        Alert(_description + ' initialization failed')
    return _answer

# ---- static local variables
_s_iStoch_m_work = Arr(1, 0, dyn=False, factory=cStochasticWork)
_s__checkHandle__chandles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticOfAverage(_MQL5Indicator):
    name = 'Stochastic of average'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpStoPeriod': 32,  # Stochastic period
        'inpStoSlowing': 3,  # Stochastic slowing
        'inpAvgPeriod': 14,  # Average period
        'inpAvgMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Average method
        'inpAvgPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

