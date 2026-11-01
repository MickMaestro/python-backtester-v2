"""WPR + CCI — converted from MQL5: MQL5 Indicators/WPR with CCI/WPR + CCI.mq5

WPR combined with CCI for confirmation
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 7, 2: 8}, 'colors': {1: [14478300, 14474475], 2: [11119017, 7451452, 9639167]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'WPR'}, 'levels': [], 'description': ['WPR combined with CCI for confirmation'], 'name': 'WPR + CCI', 'source': 'MQL5 Indicators/WPR with CCI/WPR + CCI.mq5', 'folder': 'WPR with CCI', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 32, 'label': 'WPR and CCI period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 6, 'label': 'CCI price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32)  # WPR and CCI period
inpPrice = _input('inpPrice', PRICE_TYPICAL)  # CCI price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
cci = Arr(0, 0.0)
ª_wprHandle = 0
ª_cciHandle = 0
ª_wprPeriod = 0

def OnInit():
    global ª_cciHandle, ª_wprHandle, ª_wprPeriod
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, cci, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    ª_wprPeriod = (inpPeriod if (inpPeriod > 1) else 1)
    ª_wprHandle = iWPR(Symbol(), 0, ª_wprPeriod)
    if not _checkHandle(ª_wprHandle, 'WPR'):
        return INIT_FAILED
    ª_cciHandle = iCCI(Symbol(), 0, ª_wprPeriod, inpPrice)
    if not _checkHandle(ª_cciHandle, 'CCI'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'WPR + CCI(' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_wprHandle, 0, 0, _copyCount, val) != _copyCount:
        return prev_calculated
    if CopyBuffer(ª_cciHandle, 0, 0, _copyCount, cci) != _copyCount:
        return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        valc[i] = (1 if (cci[i] > 80) else 2 if (cci[i] < -80) else 0)
        _sw1 = _int(valc[i])
        if _sw1 == 0:
            fillu[i] = -50.0
            filld[i] = -50.0
        elif _sw1 == 1:
            fillu[i] = 0.0
            filld[i] = -100.0
        elif _sw1 == 2:
            filld[i] = 0.0
            fillu[i] = -100.0
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


class WPRCCI(_MQL5Indicator):
    name = 'WPR + CCI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 32,  # WPR and CCI period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # CCI price
    }

