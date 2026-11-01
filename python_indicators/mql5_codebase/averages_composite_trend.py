"""Averages composite trend — converted from MQL5: MQL5 Indicators/Averages composite trend/Averages composite trend.mq5

Averages composite trend
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 232, 'indicator_plots': 3}, 'types': {1: 10, 2: 10, 3: 8}, 'colors': {1: [11119017, 7451452, 11823615], 2: [11119017, 7451452, 11823615], 3: [11119017, 32768, 9639167]}, 'widths': {1: 2, 2: 0, 3: 2}, 'styles': {}, 'labels': {1: 'CT trending', 2: 'CT reverting', 3: 'CT'}, 'levels': [30.0, -30.0], 'description': ['Averages composite trend'], 'name': 'Averages composite trend', 'source': 'MQL5 Indicators/Averages composite trend/Averages composite trend.mq5', 'folder': 'Averages composite trend', 'inputs': [{'mql': 'inpMaPeriods', 'py': 'inpMaPeriods', 'param': None, 'type': 'string', 'default': '10;15;20;25;30;40;50;60', 'label': 'Averages periods (separated by ";")', 'sinput': False}, {'mql': 'inpMethod', 'py': 'inpMethod', 'param': 'inpMethod', 'type': 'int', 'default': 1, 'label': 'Averages method', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Averages price', 'sinput': False}, {'mql': 'inpSmooth', 'py': 'inpSmooth', 'param': 'inpSmooth', 'type': 'double', 'default': 3.0, 'label': 'Smoothing/slowing period (<= 1 for no smoothing)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpMaPeriods = _input('inpMaPeriods', '10;15;20;25;30;40;50;60')  # Averages periods (separated by ";")
inpMethod = _input('inpMethod', MODE_EMA)  # Averages method
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Averages price
inpSmooth = _input('inpSmooth', 3.0)  # Smoothing/slowing period (<= 1 for no smoothing)
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
valht = Arr(0, 0.0)
valhtc = Arr(0, 0.0)
valhr = Arr(0, 0.0)
valhrc = Arr(0, 0.0)
ª_alpha = 0.0
_handles = Arr(0, 0)
_handlesSize = 0
_maxPeriod = 0

class simpleBuff(MqlObject):
    _q_fields = ('buffer',)
    def __init__(self, *args):
        self.buffer = Arr(0, 0.0)

def OnInit():
    global _handlesSize, _maxPeriod, ª_alpha
    SetIndexBuffer(0, valht, INDICATOR_DATA)
    SetIndexBuffer(1, valhtc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, valhr, INDICATOR_DATA)
    SetIndexBuffer(3, valhrc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, val, INDICATOR_DATA)
    SetIndexBuffer(5, valc, INDICATOR_COLOR_INDEX)
    _sep = StringGetCharacter(';', 0)
    _handlesSize = 0
    _periods = Arr(0, "")
    _periodsSize = StringSplit(inpMaPeriods, _sep, _periods)
    _periodi = Arr(0, 0)
    for i in range(0, _periodsSize):
        period = _int(StringToInteger(_periods[i]))
        if period > 0:
            _size = ArraySize(_periodi)
            ArrayResize(_periodi, _size + 1)
            _periodi[_size] = period
    ArraySort(_periodi)
    _periodsSize = ArraySize(_periodi)
    for i in range(0, _periodsSize):
        period = _periodi[i]
        handle = iMA(None, 0, period, 0, inpMethod, inpPrice)
        if not _checkHandle(handle, 'Average : ' + _str(period)):
            return INIT_FAILED
        ArrayResize(_handles, _handlesSize + 1)
        _handles[_handlesSize] = handle
        _handlesSize += 1
    if _handlesSize < 2:
        Alert('Error : at least 2 averages must be specified')
        _checkHandle(INVALID_HANDLE, 'cleanig handles,')
        return INIT_FAILED
    if _handlesSize > 256:
        Alert('Error : maximum 256 averages exceeded')
        _checkHandle(INVALID_HANDLE, 'cleanig handles,')
        return INIT_FAILED
    for i in range(0, _handlesSize):
        SetIndexBuffer(i + 6, _buffers[i].buffer, INDICATOR_CALCULATIONS)
    _maxPeriod = _periodi[_periodsSize - 1]
    ª_alpha = _fdiv(2.0, 1.0 + MathSqrt((inpSmooth if (inpSmooth > 1) else 1)))
    IndicatorSetString(INDICATOR_SHORTNAME, StringSubstr(EnumToString(inpMethod, 'ENUM_MA_METHOD'), 5) + ' composite trend (' + _str((inpSmooth if (inpSmooth > 1) else 1)) + ')(' + inpMaPeriods + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    for i in range(0, _handlesSize):
        if CopyBuffer(_handles[i], 0, 0, _copyCount, _buffers[i].buffer) != _copyCount:
            return prev_calculated
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        first = _buffers[0].buffer[i]
        sum_ = 0.0
        for k in range(1, _handlesSize):
            sum_ += first - _buffers[k].buffer[i]
        sum_ = _fdiv(sum_, float(_handlesSize - 1))
        val[i] = ((val[i - 1] + (ª_alpha * (sum_ - val[i - 1]))) if (i > _maxPeriod) else 0)
        slope = (((1 if (val[i] > val[i - 1]) else 0) if (val[i] > 0) else 1 if (val[i] < val[i - 1]) else 0) if (i > 0) else 0)
        valht[i] = (val[i] if (slope == 1) else EMPTY_VALUE)
        valhr[i] = (val[i] if (slope == 0) else EMPTY_VALUE)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        valhtc[i] = (1 if (val[i] > 0) else 2)
        valhrc[i] = (1 if (val[i] > 0) else 2)
        i += 1
    return i

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

# ---- global variables initialised from expressions
_buffers = Arr(256, 0, dyn=False, factory=simpleBuff)

# ---- static local variables
_s__checkHandle__chandles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AveragesCompositeTrend(_MQL5Indicator):
    name = 'Averages composite trend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Averages method
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Averages price
        'inpSmooth': 3.0,  # Smoothing/slowing period (<= 1 for no smoothing)
    }

