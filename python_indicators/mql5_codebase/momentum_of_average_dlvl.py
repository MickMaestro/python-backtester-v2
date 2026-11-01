"""Momentum of average (dlvl) — converted from MQL5: MQL5 Indicators/Momentum of average/Momentum of average (dlvl).mq5

Momentum of average
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 8}, 'colors': {1: [11119017], 2: [11119017], 3: [11119017, 16760576, 8036607]}, 'widths': {3: 2}, 'styles': {1: 2, 2: 2}, 'labels': {1: 'Level up', 2: 'Level down', 3: 'Momentum of average'}, 'levels': [], 'description': ['Momentum of average'], 'name': 'Momentum of average (dlvl)', 'source': 'MQL5 Indicators/Momentum of average/Momentum of average (dlvl).mq5', 'folder': 'Momentum of average', 'inputs': [{'mql': 'inpMomPeriod', 'py': 'inpMomPeriod', 'param': 'inpMomPeriod', 'type': 'int', 'default': 32, 'label': 'Momentum period', 'sinput': False}, {'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 14, 'label': 'Average period (<= 1 for no average)', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 1, 'label': 'Average method', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpLevelPeriod', 'py': 'inpLevelPeriod', 'param': 'inpLevelPeriod', 'type': 'double', 'default': 14.0, 'label': 'Levels period', 'sinput': False}, {'mql': 'inpColorChange', 'py': 'inpColorChange', 'param': 'inpColorChange', 'type': 'int', 'default': 1, 'label': 'Color change type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorChangeOn
cchange_onSlope = 0
cchange_onLevels = 1
cchange_on100 = 2
_enum('enColorChangeOn', {0: 'cchange_onSlope', 1: 'cchange_onLevels', 2: 'cchange_on100'})

# ---- inputs and global variables
inpMomPeriod = _input('inpMomPeriod', 32)  # Momentum period
inpMaPeriod = _input('inpMaPeriod', 14)  # Average period (<= 1 for no average)
inpMaMethod = _input('inpMaMethod', MODE_EMA)  # Average method
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpLevelPeriod = _input('inpLevelPeriod', 14.0)  # Levels period
inpColorChange = _input('inpColorChange', cchange_onLevels)  # Color change type
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
lup = Arr(0, 0.0)
ldn = Arr(0, 0.0)
ª_maHandle = 0
ª_maPeriod = 0
ª_momHandle = 0
ª_alphal = 0.0
ª_lvlPeriod = 0.0

def OnInit():
    global ª_alphal, ª_lvlPeriod, ª_maHandle, ª_maPeriod, ª_momHandle
    SetIndexBuffer(0, lup, INDICATOR_DATA)
    SetIndexBuffer(1, ldn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    if inpColorChange == cchange_on100:
        IndicatorSetInteger(INDICATOR_LEVELS, 1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 100)
    else:
        IndicatorSetInteger(INDICATOR_LEVELS, 1)
    ª_lvlPeriod = (inpLevelPeriod if (inpLevelPeriod > 1) else 1)
    ª_alphal = _fdiv(2.0, 1.0 + ª_lvlPeriod)
    ª_maPeriod = (inpMaPeriod if (inpMaPeriod > 0) else 1)
    ª_maHandle = iMA(Symbol(), 0, ª_maPeriod, 0, inpMaMethod, inpPrice)
    if not _checkHandle(ª_maHandle, 'average'):
        return INIT_FAILED
    ª_momHandle = iMomentum(Symbol(), 0, inpMomPeriod, ª_maHandle)
    if not _checkHandle(ª_momHandle, 'Momentum'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Momentum of ' + StringSubstr(EnumToString(inpMaMethod, 'ENUM_MA_METHOD'), 5, -1) + ' (' + _str(inpMomPeriod) + ',' + _str(ª_maPeriod) + ',' + _str(ª_lvlPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_momHandle, 0, 0, _copyCount, val) != _copyCount:
        return prev_calculated
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        if val[i] == EMPTY_VALUE:
            val[i] = 0.0
        _sw1 = inpColorChange
        if _sw1 == cchange_onLevels:
            lup[i] = ((lup[i - 1] if (val[i] < ldn[i - 1]) else (lup[i - 1] + (ª_alphal * (val[i] - lup[i - 1])))) if (i > 0) else val[i])
            ldn[i] = ((ldn[i - 1] if (val[i] > lup[i - 1]) else (ldn[i - 1] + (ª_alphal * (val[i] - ldn[i - 1])))) if (i > 0) else val[i])
            valc[i] = (1 if (val[i] > lup[i]) else 2 if (val[i] < ldn[i]) else 0)
        elif _sw1 == cchange_onSlope:
            ldn[i] = EMPTY_VALUE
            lup[i] = ldn[i]
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        elif _sw1 == cchange_on100:
            ldn[i] = EMPTY_VALUE
            lup[i] = ldn[i]
            valc[i] = (1 if (val[i] > 100) else 2 if (val[i] < 100) else 0)
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


class MomentumOfAverageDlvl(_MQL5Indicator):
    name = 'Momentum of average (dlvl)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpMomPeriod': 32,  # Momentum period
        'inpMaPeriod': 14,  # Average period (<= 1 for no average)
        'inpMaMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Average method
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpLevelPeriod': 14.0,  # Levels period
        'inpColorChange': _Choice({0: 'Change color on slope change', 1: 'Change color on levels crossing', 2: 'Change color on 100 crossing'}, default=1),  # Color change type
    }

