"""Crosses of averages — converted from MQL5: MQL5 Indicators/Averages crosses/Crosses of averages.mq5

Average crosses signals
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1, 'indicator_minimum': 0.0, 'indicator_maximum': 1.0}, 'types': {1: 7}, 'colors': {1: [7451452, 17919]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Signals'}, 'levels': [], 'description': ['Average crosses signals'], 'name': 'Crosses of averages', 'source': 'MQL5 Indicators/Averages crosses/Crosses of averages.mq5', 'folder': 'Averages crosses', 'inputs': [{'mql': 'inpFastMaPeriod', 'py': 'inpFastMaPeriod', 'param': 'inpFastMaPeriod', 'type': 'int', 'default': 12, 'label': 'Fast average period', 'sinput': False}, {'mql': 'inpSlowMaPeriod', 'py': 'inpSlowMaPeriod', 'param': 'inpSlowMaPeriod', 'type': 'int', 'default': 26, 'label': 'Slow average period', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 1, 'label': 'Average method', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpFastMaPeriod = _input('inpFastMaPeriod', 12)  # Fast average period
inpSlowMaPeriod = _input('inpSlowMaPeriod', 26)  # Slow average period
inpMaMethod = _input('inpMaMethod', MODE_EMA)  # Average method
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
sigup = Arr(0, 0.0)
sigdn = Arr(0, 0.0)
cross = Arr(0, 0.0)
mafast = Arr(0, 0.0)
maslow = Arr(0, 0.0)
ª_maFastHandle = 0
ª_maSlowHandle = 0

def OnInit():
    global ª_maFastHandle, ª_maSlowHandle
    SetIndexBuffer(0, sigup, INDICATOR_DATA)
    SetIndexBuffer(1, sigdn, INDICATOR_DATA)
    SetIndexBuffer(2, cross, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, mafast, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, maslow, INDICATOR_CALCULATIONS)
    ª_maFastHandle = iMA(Symbol(), 0, inpFastMaPeriod, 0, inpMaMethod, inpPrice)
    if not _checkHandle(ª_maFastHandle, 'Fast average'):
        return INIT_FAILED
    ª_maSlowHandle = iMA(Symbol(), 0, inpSlowMaPeriod, 0, inpMaMethod, inpPrice)
    if not _checkHandle(ª_maSlowHandle, 'Slow average'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, StringSubstr(EnumToString(inpMaMethod, 'ENUM_MA_METHOD'), 5, -1) + ' crosses signals (' + _str(inpFastMaPeriod) + ',' + _str(inpSlowMaPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_maFastHandle, 0, 0, _copyCount, mafast) != _copyCount:
        return prev_calculated
    if CopyBuffer(ª_maSlowHandle, 0, 0, _copyCount, maslow) != _copyCount:
        return prev_calculated
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        cross[i] = (1 if (mafast[i] > maslow[i]) else -1 if (mafast[i] < maslow[i]) else cross[i - 1] if (i > 0) else 0)
        sigdn[i] = 0.0
        sigup[i] = sigdn[i]
        if i > 0:
            if cross[i] != cross[i - 1]:
                if cross[i] == 1:
                    sigup[i] = 1.0
                if cross[i] == -1:
                    sigdn[i] = 1.0
            else:
                if cross[i] == 1:
                    sigup[i] = 0.02
                if cross[i] == -1:
                    sigdn[i] = 0.02
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


class CrossesOfAverages(_MQL5Indicator):
    name = 'Crosses of averages'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFastMaPeriod': 12,  # Fast average period
        'inpSlowMaPeriod': 26,  # Slow average period
        'inpMaMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Average method
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }
    y_range = (0.0, 1.0)

