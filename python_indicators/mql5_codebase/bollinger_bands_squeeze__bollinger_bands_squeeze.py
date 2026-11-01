"""Bollinger bands squeeze — converted from MQL5: MQL5 Indicators/Bollinger bands squeeze/Bollinger bands squeeze.mq5

BB squeeze on chart
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 11, 'indicator_plots': 6}, 'types': {1: 7, 2: 8, 3: 1, 4: 8, 5: 1, 6: 8}, 'colors': {1: [14474460, 14474460], 2: [14474460, 3329330], 3: [12632256], 4: [12632256, 3329330, 42495], 5: [12632256], 6: [14474460, 42495]}, 'widths': {4: 2}, 'styles': {3: 2, 5: 2}, 'labels': {1: 'squeeze area', 2: 'BB upper band', 3: 'Keltner channel upper band', 4: 'BB and Keltner channel middle value', 5: 'Keltner channel lower band', 6: 'BB lower band'}, 'levels': [], 'description': ['BB squeeze on chart'], 'name': 'Bollinger bands squeeze', 'source': 'MQL5 Indicators/Bollinger bands squeeze/Bollinger bands squeeze.mq5', 'folder': 'Bollinger bands squeeze', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 20, 'label': 'BB and Keltner period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpBbMultiplier', 'py': 'inpBbMultiplier', 'param': 'inpBbMultiplier', 'type': 'double', 'default': 2.0, 'label': 'BB width', 'sinput': False}, {'mql': 'inpKcMultiplier', 'py': 'inpKcMultiplier', 'param': 'inpKcMultiplier', 'type': 'double', 'default': 1.5, 'label': 'Keltner channel width, <=0 same as BB width)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 20)  # BB and Keltner period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpBbMultiplier = _input('inpBbMultiplier', 2.0)  # BB width
inpKcMultiplier = _input('inpKcMultiplier', 1.5)  # Keltner channel width, <=0 same as BB width)
mid = Arr(0, 0.0)
midc = Arr(0, 0.0)
bbup = Arr(0, 0.0)
bbupc = Arr(0, 0.0)
bbdn = Arr(0, 0.0)
bbdnc = Arr(0, 0.0)
kelu = Arr(0, 0.0)
keld = Arr(0, 0.0)
sqzu = Arr(0, 0.0)
sqzd = Arr(0, 0.0)
atr = Arr(0, 0.0)
_kcMultiplier = 0.0
_bbHandle = 0
_atrHandle = 0

def OnInit():
    global _atrHandle, _bbHandle, _kcMultiplier
    SetIndexBuffer(0, sqzu, INDICATOR_DATA)
    SetIndexBuffer(1, sqzd, INDICATOR_DATA)
    SetIndexBuffer(2, bbup, INDICATOR_DATA)
    SetIndexBuffer(3, bbupc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, kelu, INDICATOR_DATA)
    SetIndexBuffer(5, mid, INDICATOR_DATA)
    SetIndexBuffer(6, midc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, keld, INDICATOR_DATA)
    SetIndexBuffer(8, bbdn, INDICATOR_DATA)
    SetIndexBuffer(9, bbdnc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(10, atr, INDICATOR_CALCULATIONS)
    _kcMultiplier = (inpBbMultiplier if (inpKcMultiplier <= 0) else inpKcMultiplier)
    _bbHandle = iBands(Symbol(), 0, inpPeriod, 0, inpBbMultiplier, inpPrice)
    if not _checkHandle(_bbHandle, 'Bollinger bands'):
        return INIT_FAILED
    _atrHandle = iATR(Symbol(), 0, inpPeriod)
    if not _checkHandle(_atrHandle, 'ATR'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'BB squeeze (' + _str(inpPeriod) + ',' + _str(inpBbMultiplier) + ',' + _str(_kcMultiplier) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(_bbHandle) < rates_total:
        return prev_calculated
    if BarsCalculated(_atrHandle) < rates_total:
        return prev_calculated
    _copyCount = MathMin(rates_total - prev_calculated + 1, rates_total)
    if CopyBuffer(_bbHandle, BASE_LINE, 0, _copyCount, mid) != _copyCount:
        return prev_calculated
    if CopyBuffer(_bbHandle, LOWER_BAND, 0, _copyCount, bbdn) != _copyCount:
        return prev_calculated
    if CopyBuffer(_bbHandle, UPPER_BAND, 0, _copyCount, bbup) != _copyCount:
        return prev_calculated
    if CopyBuffer(_atrHandle, BASE_LINE, 0, _copyCount, atr) != _copyCount:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        keld[i] = mid[i] - (atr[i] * _kcMultiplier)
        kelu[i] = mid[i] + (atr[i] * _kcMultiplier)
        _squeeze = kelu[i] > bbup[i]
        sqzu[i] = (bbup[i] if _squeeze else mid[i])
        sqzd[i] = (bbdn[i] if _squeeze else mid[i])
        bbupc[i] = (0 if _squeeze else 1 if (close[i] > bbup[i]) else 0)
        bbdnc[i] = (0 if _squeeze else 1 if (close[i] < bbdn[i]) else 0)
        midc[i] = (0 if _squeeze else 1 if (close[i] > mid[i]) else 2)
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


class BollingerBandsSqueeze(_MQL5Indicator):
    name = 'Bollinger bands squeeze'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 20,  # BB and Keltner period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpBbMultiplier': 2.0,  # BB width
        'inpKcMultiplier': 1.5,  # Keltner channel width, <=0 same as BB width)
    }

