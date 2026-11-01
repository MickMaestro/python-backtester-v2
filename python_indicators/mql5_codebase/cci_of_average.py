"""CCI of average — converted from MQL5: MQL5 Indicators/CCI of average/CCI of average.mq5

CCI of average
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 16760576, 8036607]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'CCI of average'}, 'levels': [], 'description': ['CCI of average'], 'name': 'CCI of average', 'source': 'MQL5 Indicators/CCI of average/CCI of average.mq5', 'folder': 'CCI of average', 'inputs': [{'mql': 'inpCciPeriod', 'py': 'inpCciPeriod', 'param': 'inpCciPeriod', 'type': 'int', 'default': 32, 'label': 'CCI period', 'sinput': False}, {'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 14, 'label': 'Average period (<= 1 for no average)', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 1, 'label': 'Average method', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpLevel', 'py': 'inpLevel', 'param': 'inpLevel', 'type': 'double', 'default': 100.0, 'label': 'Level(s) (+ and - will be the same)', 'sinput': False}, {'mql': 'inpColorChange', 'py': 'inpColorChange', 'param': 'inpColorChange', 'type': 'int', 'default': 1, 'label': 'Color change type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorChangeOn
cchange_onSlope = 0
cchange_onLevels = 1
cchange_onZero = 2
_enum('enColorChangeOn', {0: 'cchange_onSlope', 1: 'cchange_onLevels', 2: 'cchange_onZero'})

# ---- inputs and global variables
inpCciPeriod = _input('inpCciPeriod', 32)  # CCI period
inpMaPeriod = _input('inpMaPeriod', 14)  # Average period (<= 1 for no average)
inpMaMethod = _input('inpMaMethod', MODE_EMA)  # Average method
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpLevel = _input('inpLevel', 100.0)  # Level(s) (+ and - will be the same)
inpColorChange = _input('inpColorChange', cchange_onLevels)  # Color change type
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
ª_maHandle = 0
ª_maPeriod = 0
ª_cciHandle = 0

def OnInit():
    global ª_cciHandle, ª_maHandle, ª_maPeriod
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, inpLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, -inpLevel)
    ª_maPeriod = (inpMaPeriod if (inpMaPeriod > 0) else 1)
    ª_maHandle = iMA(Symbol(), 0, ª_maPeriod, 0, inpMaMethod, inpPrice)
    if not _checkHandle(ª_maHandle, 'average'):
        return INIT_FAILED
    ª_cciHandle = iCCI(Symbol(), 0, inpCciPeriod, ª_maHandle)
    if not _checkHandle(ª_cciHandle, 'CCI'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'CCI of ' + StringSubstr(EnumToString(inpMaMethod, 'ENUM_MA_METHOD'), 5, -1) + ' (' + _str(inpCciPeriod) + ',' + _str(inpMaPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_cciHandle, 0, 0, _copyCount, val) != _copyCount:
        return prev_calculated
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        _sw1 = inpColorChange
        if _sw1 == cchange_onLevels:
            valc[i] = (1 if (val[i] > inpLevel) else 2 if (val[i] < (-inpLevel)) else 0)
        elif _sw1 == cchange_onSlope:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        elif _sw1 == cchange_onZero:
            valc[i] = (1 if (val[i] > 0) else 2 if (val[i] < 0) else 0)
        i += 1
    return i

def _checkHandle(_handle, _description):
    _size = ArraySize(_s__checkHandle__handles)
    _answer = _handle != INVALID_HANDLE
    if _answer:
        ArrayResize(_s__checkHandle__handles, _size + 1)
        _s__checkHandle__handles[_size] = _handle
    else:
        for i in range(_size - 1, 0 - 1, -1):
            IndicatorRelease(_s__checkHandle__handles[i])
        ArrayResize(_s__checkHandle__handles, 0)
        Alert(_description + ' initialization failed')
    return _answer

# ---- static local variables
_s__checkHandle__handles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CCIOfAverage(_MQL5Indicator):
    name = 'CCI of average'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpCciPeriod': 32,  # CCI period
        'inpMaPeriod': 14,  # Average period (<= 1 for no average)
        'inpMaMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Average method
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpLevel': 100.0,  # Level(s) (+ and - will be the same)
        'inpColorChange': _Choice({0: 'Change color on slope change', 1: 'Change color on levels crossing', 2: 'Change color on zero crossing'}, default=1),  # Color change type
    }

