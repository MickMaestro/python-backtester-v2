"""Rsi candles with Keltner channel — converted from MQL5: MQL5 Indicators/RSI candles with Keltner channel/Rsi candles with Keltner channel.mq5

Rsi candles with \\"Keltner\\" channels
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 12, 'indicator_plots': 4}, 'types': {1: 17, 2: 1, 3: 1, 4: 1}, 'colors': {1: [8421504, 7451452, 17919], 2: [8421504], 3: [8421504], 4: [8421504]}, 'widths': {}, 'styles': {2: 2, 3: 2, 4: 2}, 'labels': {1: 'RSI', 2: 'average', 3: 'channel up', 4: 'channel up'}, 'levels': [], 'description': ['Rsi candles with \\"Keltner\\" channels'], 'name': 'Rsi candles with Keltner channel', 'source': 'MQL5 Indicators/RSI candles with Keltner channel/Rsi candles with Keltner channel.mq5', 'folder': 'RSI candles with Keltner channel', 'inputs': [{'mql': 'inpRsiPeriod', 'py': 'inpRsiPeriod', 'param': 'inpRsiPeriod', 'type': 'int', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'inpAvgPeriod', 'py': 'inpAvgPeriod', 'param': 'inpAvgPeriod', 'type': 'int', 'default': 0, 'label': 'Channel period (<=1 for same as RSI period)', 'sinput': False}, {'mql': 'inpMultiplier', 'py': 'inpMultiplier', 'param': 'inpMultiplier', 'type': 'double', 'default': 1.5, 'label': 'Channels multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRsiPeriod = _input('inpRsiPeriod', 14)  # RSI period
inpAvgPeriod = _input('inpAvgPeriod', 0)  # Channel period (<=1 for same as RSI period)
inpMultiplier = _input('inpMultiplier', 1.5)  # Channels multiplier
rsio = Arr(0, 0.0)
rsih = Arr(0, 0.0)
rsil = Arr(0, 0.0)
rsic = Arr(0, 0.0)
rsicl = Arr(0, 0.0)
kel = Arr(0, 0.0)
kelu = Arr(0, 0.0)
keld = Arr(0, 0.0)
tr = Arr(0, 0.0)
rsi = Arr(0, 0.0)
atr = Arr(0, 0.0)
avg = Arr(0, 0.0)
ª_workRsi = Arr(4, 0.0, dyn=False)
ª_rshHandle = 0
ª_rslHandle = 0
ª_rsoHandle = 0
ª_rscHandle = 0
ª_avgPeriod = 0

def OnInit():
    global ª_avgPeriod, ª_rscHandle, ª_rshHandle, ª_rslHandle, ª_rsoHandle
    SetIndexBuffer(0, rsio, INDICATOR_DATA)
    SetIndexBuffer(1, rsih, INDICATOR_DATA)
    SetIndexBuffer(2, rsil, INDICATOR_DATA)
    SetIndexBuffer(3, rsic, INDICATOR_DATA)
    SetIndexBuffer(4, rsicl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, kel, INDICATOR_DATA)
    SetIndexBuffer(6, kelu, INDICATOR_DATA)
    SetIndexBuffer(7, keld, INDICATOR_DATA)
    SetIndexBuffer(8, tr, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, atr, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, rsi, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, avg, INDICATOR_CALCULATIONS)
    ª_rshHandle = iRSI(Symbol(), 0, inpRsiPeriod, PRICE_HIGH)
    if not _checkHandle(ª_rshHandle, 'RSI of high'):
        return INIT_FAILED
    ª_rslHandle = iRSI(Symbol(), 0, inpRsiPeriod, PRICE_LOW)
    if not _checkHandle(ª_rslHandle, 'RSI of low'):
        return INIT_FAILED
    ª_rsoHandle = iRSI(Symbol(), 0, inpRsiPeriod, PRICE_OPEN)
    if not _checkHandle(ª_rsoHandle, 'RSI of open'):
        return INIT_FAILED
    ª_rscHandle = iRSI(Symbol(), 0, inpRsiPeriod, PRICE_CLOSE)
    if not _checkHandle(ª_rscHandle, 'RSI of close'):
        return INIT_FAILED
    ª_avgPeriod = (inpAvgPeriod if (inpAvgPeriod > 1) else inpRsiPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Rsi candles (' + _str(inpRsiPeriod) + ',' + _str(ª_avgPeriod) + ',' + _str(inpMultiplier) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_rshHandle, 0, 0, _copyCount, rsih) != _copyCount:
        return prev_calculated
    if CopyBuffer(ª_rslHandle, 0, 0, _copyCount, rsil) != _copyCount:
        return prev_calculated
    if CopyBuffer(ª_rsoHandle, 0, 0, _copyCount, rsio) != _copyCount:
        return prev_calculated
    if CopyBuffer(ª_rscHandle, 0, 0, _copyCount, rsic) != _copyCount:
        return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        if rsil[i] == EMPTY_VALUE:
            rsil[i] = 0.0
        if rsih[i] == EMPTY_VALUE:
            rsih[i] = 0.0
        if rsio[i] == EMPTY_VALUE:
            rsio[i] = 0.0
        if rsic[i] == EMPTY_VALUE:
            rsic[i] = 0.0
        ª_workRsi[1] = rsil[i]
        ª_workRsi[0] = rsih[i]
        ª_workRsi[2] = rsio[i]
        ª_workRsi[3] = rsic[i]
        rsih[i] = ª_workRsi[ArrayMaximum(ª_workRsi)]
        rsil[i] = ª_workRsi[ArrayMinimum(ª_workRsi)]
        rsi[i] = (rsih[i] + rsil[i] + rsio[i] + rsic[i]) / 4.0
        tr[i] = ((MathMax(rsih[i], rsic[i - 1]) - MathMin(rsil[i], rsic[i - 1])) if (i > 0) else (rsih[i] - rsil[i]))
        if i > ª_avgPeriod:
            avg[i] = avg[i - 1] + rsi[i] - rsi[i - ª_avgPeriod]
            atr[i] = atr[i - 1] + tr[i] - tr[i - ª_avgPeriod]
        else:
            atr[i] = 0.0
            avg[i] = atr[i]
            k = 0
            while k < ª_avgPeriod and i >= k:
                avg[i] += rsi[i - k]
                atr[i] += tr[i - k]
                k += 1
        kel[i] = _fdiv(avg[i], float(ª_avgPeriod))
        kelu[i] = kel[i] + _fdiv(inpMultiplier * atr[i], float(ª_avgPeriod))
        keld[i] = kel[i] - _fdiv(inpMultiplier * atr[i], float(ª_avgPeriod))
        rsicl[i] = (1 if (rsic[i] > rsio[i]) else 2 if (rsic[i] < rsio[i]) else 0)
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


class RsiCandlesWithKeltnerChannel(_MQL5Indicator):
    name = 'Rsi candles with Keltner channel'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRsiPeriod': 14,  # RSI period
        'inpAvgPeriod': 0,  # Channel period (<=1 for same as RSI period)
        'inpMultiplier': 1.5,  # Channels multiplier
    }

