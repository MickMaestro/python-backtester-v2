"""Dtosc — converted from MQL5: MQL5 Indicators/Dynamic Trader Oscillator/Dtosc.mq5

Dynamic Trader Oscillator
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [7451452, 17919], 2: [8421504]}, 'widths': {}, 'styles': {2: 2}, 'labels': {1: 'DTOSC', 2: 'Signal'}, 'levels': [0.0, 100.0], 'description': ['Dynamic Trader Oscillator'], 'name': 'Dtosc', 'source': 'MQL5 Indicators/Dynamic Trader Oscillator/Dtosc.mq5', 'folder': 'Dynamic Trader Oscillator', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpStoPeriod', 'py': 'inpStoPeriod', 'param': 'inpStoPeriod', 'type': 'int', 'default': 32, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'inpStoSlowing', 'py': 'inpStoSlowing', 'param': 'inpStoSlowing', 'type': 'int', 'default': 3, 'label': 'Stochastic slowing', 'sinput': False}, {'mql': 'inpStoSignal', 'py': 'inpStoSignal', 'param': 'inpStoSignal', 'type': 'int', 'default': 3, 'label': 'Stochastic signal period', 'sinput': False}, {'mql': 'inpStoMethod', 'py': 'inpStoMethod', 'param': 'inpStoMethod', 'type': 'int', 'default': 1, 'label': 'Stochastic signal method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpStoPeriod = _input('inpStoPeriod', 32)  # Stochastic period
inpStoSlowing = _input('inpStoSlowing', 3)  # Stochastic slowing
inpStoSignal = _input('inpStoSignal', 3)  # Stochastic signal period
inpStoMethod = _input('inpStoMethod', MODE_EMA)  # Stochastic signal method
sto = Arr(0, 0.0)
stoc = Arr(0, 0.0)
sig = Arr(0, 0.0)
rsi = Arr(0, 0.0)
ª_rsiHandle = 0
ª_rsiPeriod = 0

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
    global ª_rsiHandle, ª_rsiPeriod
    SetIndexBuffer(0, sto, INDICATOR_DATA)
    SetIndexBuffer(1, stoc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, sig, INDICATOR_DATA)
    SetIndexBuffer(3, rsi, INDICATOR_CALCULATIONS)
    ª_rsiPeriod = (inpPeriod if (inpPeriod > 1) else 1)
    ª_rsiHandle = iRSI(Symbol(), 0, ª_rsiPeriod, inpPrice)
    if not _checkHandle(ª_rsiHandle, 'RSI'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, '"DTOSC" (' + _str(inpPeriod) + ',' + _str(inpStoPeriod) + ',' + _str(inpStoSlowing) + ',' + _str(inpStoSignal) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_rsiHandle, 0, 0, _copyCount, rsi) != _copyCount:
        return prev_calculated
    start = prev_calculated - 1
    if start < 0:
        start = 0
    for i in range(start, rates_total):
        if rsi[i] == EMPTY_VALUE:
            rsi[i] = 0.0
        sto[i] = iStoch(rsi[i], rsi[i], rsi[i], inpStoPeriod, inpStoSlowing, i)
    weightsum = Box(0)
    _sw1 = inpStoMethod
    if _sw1 == MODE_SMA:
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, inpStoSignal, sto, sig)
    elif _sw1 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, inpStoSignal, sto, sig)
    elif _sw1 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, inpStoSignal, sto, sig)
    else:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, inpStoSignal, sto, sig, weightsum)
    for i in range(start, rates_total):
        stoc[i] = (0 if (sto[i] > sig[i]) else 1 if (sto[i] < sig[i]) else stoc[i - 1] if (i > 0) else 0)
    return rates_total

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


class Dtosc(_MQL5Indicator):
    name = 'Dtosc'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpStoPeriod': 32,  # Stochastic period
        'inpStoSlowing': 3,  # Stochastic slowing
        'inpStoSignal': 3,  # Stochastic signal period
        'inpStoMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Stochastic signal method
    }

