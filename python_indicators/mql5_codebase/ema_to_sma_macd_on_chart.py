"""EMA to SMA MACD (on chart) — converted from MQL5: MQL5 Indicators/EMA to SMA MACD - on chart/EMA to SMA MACD (on chart).mq5

EMA to SMA MACD - on chart
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [7451452, 42495], 2: [11119017], 3: [11119017]}, 'widths': {3: 2}, 'styles': {}, 'labels': {1: 'Fill area', 2: 'EMA', 3: 'SMA'}, 'levels': [], 'description': ['EMA to SMA MACD - on chart'], 'name': 'EMA to SMA MACD (on chart)', 'source': 'MQL5 Indicators/EMA to SMA MACD - on chart/EMA to SMA MACD (on chart).mq5', 'folder': 'EMA to SMA MACD - on chart', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 26, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 26)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
ema = Arr(0, 0.0)
sma = Arr(0, 0.0)
ª_emaHandle = 0
ª_smaHandle = 0
ª_maPeriod = 0

def OnInit():
    global ª_emaHandle, ª_maPeriod, ª_smaHandle
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, ema, INDICATOR_DATA)
    SetIndexBuffer(3, sma, INDICATOR_DATA)
    ª_maPeriod = (inpPeriod if (inpPeriod > 0) else 1)
    ª_emaHandle = iMA(Symbol(), 0, ª_maPeriod, 0, MODE_EMA, inpPrice)
    if not _checkHandle(ª_emaHandle, 'EMA'):
        return INIT_FAILED
    ª_smaHandle = iMA(Symbol(), 0, ª_maPeriod, 0, MODE_SMA, inpPrice)
    if not _checkHandle(ª_smaHandle, 'SMA'):
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'EMA to SMA MACD (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_emaHandle, 0, 0, _copyCount, ema) != _copyCount:
        return prev_calculated
    if CopyBuffer(ª_smaHandle, 0, 0, _copyCount, sma) != _copyCount:
        return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        if ema[i] == EMPTY_VALUE:
            ema[i] = 0.0
        if sma[i] == EMPTY_VALUE:
            sma[i] = 0.0
        fillu[i] = ema[i]
        filld[i] = sma[i]
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


class EMAToSMAMACDOnChart(_MQL5Indicator):
    name = 'EMA to SMA MACD (on chart)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 26,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

