"""CCI variation — converted from MQL5: MQL5 Indicators/CCI variation/CCI variation.mq5

CCI  - atr or std based
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'CCI'}, 'levels': [], 'description': ['CCI  - atr or std based'], 'name': 'CCI variation', 'source': 'MQL5 Indicators/CCI variation/CCI variation.mq5', 'folder': 'CCI variation', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 50, 'label': 'Period', 'sinput': False}, {'mql': 'inpSmoothing', 'py': 'inpSmoothing', 'param': 'inpSmoothing', 'type': 'int', 'default': 0, 'label': 'Smoothing period (<=1 for no smoothing)', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 6, 'label': 'Price', 'sinput': False}, {'mql': 'inpUseWhat', 'py': 'inpUseWhat', 'param': 'inpUseWhat', 'type': 'int', 'default': 1, 'label': 'Calculation method', 'sinput': False}, {'mql': 'inpColorMode', 'py': 'inpColorMode', 'param': 'inpColorMode', 'type': 'int', 'default': 1, 'label': 'Color changing method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enUseWhat
use_atr = 0
use_dev = 1
_enum('enUseWhat', {0: 'use_atr', 1: 'use_dev'})

# enum enColorMode
clr_onSlope = 0
clr_onZero = 1
_enum('enColorMode', {0: 'clr_onSlope', 1: 'clr_onZero'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 50)  # Period
inpSmoothing = _input('inpSmoothing', 0)  # Smoothing period (<=1 for no smoothing)
inpPrice = _input('inpPrice', PRICE_TYPICAL)  # Price
inpUseWhat = _input('inpUseWhat', use_dev)  # Calculation method
inpColorMode = _input('inpColorMode', clr_onZero)  # Color changing method
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
ade = Arr(0, 0.0)
ma = Arr(0, 0.0)
price = Arr(0, 0.0)
ª_adHandle = 0
ª_maHandle = 0
ª_prHandle = 0
ª_prPeriod = 0
ª_cciTypes = Arr.of(['ATR based', 'STD based'], fill="")

def OnInit():
    global ª_adHandle, ª_maHandle, ª_prHandle, ª_prPeriod
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ade, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ma, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, price, INDICATOR_CALCULATIONS)
    ª_prPeriod = (inpSmoothing if (inpSmoothing > 1) else 1)
    if inpUseWhat == use_atr:
        ª_adHandle = iATR(Symbol(), 0, inpPeriod)
        if not _checkHandle(ª_adHandle, 'ATR'):
            return INIT_FAILED
    else:
        ª_adHandle = iStdDev(Symbol(), 0, inpPeriod, 0, MODE_SMA, inpPrice)
        if not _checkHandle(ª_adHandle, 'Standard deviation'):
            return INIT_FAILED
    ª_maHandle = iMA(Symbol(), 0, inpPeriod, 0, MODE_SMA, inpPrice)
    if not _checkHandle(ª_maHandle, 'Average'):
        return INIT_FAILED
    ª_prHandle = iMA(Symbol(), 0, ª_prPeriod, 0, MODE_SMA, inpPrice)
    if not _checkHandle(ª_prHandle, 'Prices'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, ª_cciTypes[inpUseWhat] + ' CCI (' + _str(inpPeriod) + ((',' + _str(ª_prPeriod)) if (ª_prPeriod > 1) else '') + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_adHandle, 0, 0, _copyCount, ade) != _copyCount:
        return prev_calculated
    if CopyBuffer(ª_maHandle, 0, 0, _copyCount, ma) != _copyCount:
        return prev_calculated
    if CopyBuffer(ª_prHandle, 0, 0, _copyCount, price) != _copyCount:
        return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        val[i] = (_fdiv(price[i] - ma[i], 0.015 * ade[i]) if (ade[i] != 0) else 0)
        if inpColorMode == clr_onSlope:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        else:
            valc[i] = (1 if (val[i] > 0) else 2 if (val[i] < 0) else 0)
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

# ---- static local variables
_s__checkHandle__chandles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CCIVariation(_MQL5Indicator):
    name = 'CCI variation'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 50,  # Period
        'inpSmoothing': 0,  # Smoothing period (<=1 for no smoothing)
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Price
        'inpUseWhat': _Choice({0: 'Use ATR for calculation', 1: 'Use standard deviation for calculation'}, default=1),  # Calculation method
        'inpColorMode': _Choice({0: 'Change color on slope change', 1: 'Change color on zero cross'}, default=1),  # Color changing method
    }

