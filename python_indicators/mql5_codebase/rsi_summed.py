"""RSI summed — converted from MQL5: MQL5 Indicators/RSI Summed/RSI summed.mq5

Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 10, 2: 1}, 'colors': {1: [11119017, 7451452, 17919], 2: [8421504]}, 'widths': {1: 2, 2: 0}, 'styles': {}, 'labels': {1: 'RSI state', 2: 'RSI state line'}, 'levels': [], 'description': [], 'name': 'RSI summed', 'source': 'MQL5 Indicators/RSI Summed/RSI summed.mq5', 'folder': 'RSI Summed', 'inputs': [{'mql': 'inpPeriods', 'py': 'inpPeriods', 'param': None, 'type': 'string', 'default': '14;15;16;17;18;19;20;21', 'label': 'RSI periods', 'sinput': False}, {'mql': 'inpLevelUp', 'py': 'inpLevelUp', 'param': 'inpLevelUp', 'type': 'double', 'default': 55.0, 'label': 'High period', 'sinput': False}, {'mql': 'inpLevelDown', 'py': 'inpLevelDown', 'param': 'inpLevelDown', 'type': 'double', 'default': 45.0, 'label': 'Low period', 'sinput': False}, {'mql': 'inpRsiPrice', 'py': 'inpRsiPrice', 'param': 'inpRsiPrice', 'type': 'int', 'default': 1, 'label': 'RSI price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriods = _input('inpPeriods', '14;15;16;17;18;19;20;21')  # RSI periods
inpLevelUp = _input('inpLevelUp', 55.0)  # High period
inpLevelDown = _input('inpLevelDown', 45.0)  # Low period
inpRsiPrice = _input('inpRsiPrice', PRICE_CLOSE)  # RSI price
val = Arr(0, 0.0)
vall = Arr(0, 0.0)
valc = Arr(0, 0.0)
_rsiHandles = Arr(0, 0)
_rsiHandlesSize = 0
_rsisCalculated = ''

def OnInit():
    global _rsiHandlesSize, _rsisCalculated
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, vall, INDICATOR_DATA)
    _temp = Arr(0, "")
    _sep = StringGetCharacter(';', 0)
    _count = StringSplit(inpPeriods, _sep, _temp)
    for i in range(0, _count):
        period = _int(StringToInteger(_temp[i]))
        if period > 0:
            handle = iRSI(Symbol(), Period(), period, inpRsiPrice)
            if handle != INVALID_HANDLE:
                _rsiHandlesSize += 1
                ArrayResize(_rsiHandles, _rsiHandlesSize)
                _rsiHandles[_rsiHandlesSize - 1] = handle
                _rsisCalculated += (',' if (_rsisCalculated != '') else '') + _str(period)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSI summed (' + _rsisCalculated + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _summ = 0.0
        _tempRsi = Arr(1, 0.0, dyn=False)
        for k in range(0, _rsiHandlesSize):
            if CopyBuffer(_rsiHandles[k], 0, rates_total - i - 1, 1, _tempRsi) == 1:
                _summ += (1 if (_tempRsi[0] > inpLevelUp) else -1 if (_tempRsi[0] < inpLevelDown) else 0)
        vall[i] = (1 if (_summ == _rsiHandlesSize) else -1 if (_summ == (-_rsiHandlesSize)) else 0)
        val[i] = vall[i]
        valc[i] = (1 if (val[i] == 1) else 2 if (val[i] == -1) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSISummed(_MQL5Indicator):
    name = 'RSI summed'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpLevelUp': 55.0,  # High period
        'inpLevelDown': 45.0,  # Low period
        'inpRsiPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # RSI price
    }

