"""Heiken Ashi smoothed zone trade — converted from MQL5: MQL5 Indicators/Heiken ashi smoothed - zone trade/Heiken Ashi smoothed zone trade.mq5

Heiken ashi smoothed zone trade
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 15, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16760576, 6333684, 12632256, 12632256]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Heiken ashi open;Heiken ashi high;Heiken ashi low;Heiken ashi close'}, 'levels': [], 'description': ['Heiken ashi smoothed zone trade'], 'name': 'Heiken Ashi smoothed zone trade', 'source': 'MQL5 Indicators/Heiken ashi smoothed - zone trade/Heiken Ashi smoothed zone trade.mq5', 'folder': 'Heiken ashi smoothed - zone trade', 'inputs': [{'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 7, 'label': 'Smoothing period (<= 1 for no smoothing)', 'sinput': False}, {'mql': 'inpMaMetod', 'py': 'inpMaMetod', 'param': 'inpMaMetod', 'type': 'int', 'default': 3, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'inpStep', 'py': 'inpStep', 'param': 'inpStep', 'type': 'double', 'default': 0.0, 'label': 'Step size (in pips)', 'sinput': False}, {'mql': 'inpBetterFormula', 'py': 'inpBetterFormula', 'param': 'inpBetterFormula', 'type': 'bool', 'default': False, 'label': 'Use better formula?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpMaPeriod = _input('inpMaPeriod', 7)  # Smoothing period (<= 1 for no smoothing)
inpMaMetod = _input('inpMaMetod', MODE_LWMA)  # Smoothing method
inpStep = _input('inpStep', 0.0)  # Step size (in pips)
inpBetterFormula = _input('inpBetterFormula', False)  # Use better formula?
canh = Arr(0, 0.0)
canl = Arr(0, 0.0)
cano = Arr(0, 0.0)
canc = Arr(0, 0.0)
cancl = Arr(0, 0.0)
hah = Arr(0, 0.0)
hal = Arr(0, 0.0)
hao = Arr(0, 0.0)
hac = Arr(0, 0.0)
haC = Arr(0, 0.0)
mah = Arr(0, 0.0)
mal = Arr(0, 0.0)
mao = Arr(0, 0.0)
mac = Arr(0, 0.0)
acb = Arr(0, 0.0)
aob = Arr(0, 0.0)
_mao = 0
_mac = 0
_mal = 0
_mah = 0
_ach = 0
_aoh = 0

def OnInit():
    global _ach, _aoh, _mac, _mah, _mal, _mao
    SetIndexBuffer(0, cano, INDICATOR_DATA)
    SetIndexBuffer(1, canh, INDICATOR_DATA)
    SetIndexBuffer(2, canl, INDICATOR_DATA)
    SetIndexBuffer(3, canc, INDICATOR_DATA)
    SetIndexBuffer(4, cancl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, hao, INDICATOR_DATA)
    SetIndexBuffer(6, hah, INDICATOR_DATA)
    SetIndexBuffer(7, hal, INDICATOR_DATA)
    SetIndexBuffer(8, hac, INDICATOR_DATA)
    SetIndexBuffer(9, mac, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, mao, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, mah, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, mal, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, acb, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, aob, INDICATOR_CALCULATIONS)
    _maPeriod = (inpMaPeriod if (inpMaPeriod > 0) else 1)
    _mao = iMA(Symbol(), 0, _maPeriod, 0, inpMaMetod, PRICE_OPEN)
    if not _checkHandle(_mao, 'Moving average of open'):
        return INIT_FAILED
    _mac = iMA(Symbol(), 0, _maPeriod, 0, inpMaMetod, PRICE_CLOSE)
    if not _checkHandle(_mac, 'Moving average of close'):
        return INIT_FAILED
    _mah = iMA(Symbol(), 0, _maPeriod, 0, inpMaMetod, PRICE_HIGH)
    if not _checkHandle(_mah, 'Moving average of high'):
        return INIT_FAILED
    _mal = iMA(Symbol(), 0, _maPeriod, 0, inpMaMetod, PRICE_LOW)
    if not _checkHandle(_mal, 'Moving average of low'):
        return INIT_FAILED
    _ach = iAC(Symbol(), 0)
    if not _checkHandle(_ach, 'Accelerator Oscillator'):
        return INIT_FAILED
    _aoh = iAO(Symbol(), 0)
    if not _checkHandle(_aoh, 'Awesome Oscillator'):
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(_mao) < rates_total:
        return prev_calculated
    if BarsCalculated(_mac) < rates_total:
        return prev_calculated
    if BarsCalculated(_mah) < rates_total:
        return prev_calculated
    if BarsCalculated(_mal) < rates_total:
        return prev_calculated
    if BarsCalculated(_ach) < rates_total:
        return prev_calculated
    if BarsCalculated(_aoh) < rates_total:
        return prev_calculated
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(_mao, 0, 0, _copyCount, mao) != _copyCount:
        return prev_calculated
    if CopyBuffer(_mac, 0, 0, _copyCount, mac) != _copyCount:
        return prev_calculated
    if CopyBuffer(_mah, 0, 0, _copyCount, mah) != _copyCount:
        return prev_calculated
    if CopyBuffer(_mal, 0, 0, _copyCount, mal) != _copyCount:
        return prev_calculated
    if CopyBuffer(_ach, 0, 0, _copyCount, acb) != _copyCount:
        return prev_calculated
    if CopyBuffer(_aoh, 0, 0, _copyCount, aob) != _copyCount:
        return prev_calculated
    _step = ((inpStep * MathPow(10, _imod(Digits(), 2)) * Point()) if (inpStep > 0) else 0)
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        maOpen = (mao[i] if (mao[i] != EMPTY_VALUE) else open[i])
        maClose = (mac[i] if (mac[i] != EMPTY_VALUE) else close[i])
        maLow = (mal[i] if (mal[i] != EMPTY_VALUE) else low[i])
        maHigh = (mah[i] if (mah[i] != EMPTY_VALUE) else high[i])
        haClose = (((maOpen + maHigh + maLow + maClose) * 0.25) if (not inpBetterFormula) else (((maOpen + maClose) * 0.5) + (_fdiv(maClose - maOpen, maHigh - maLow) * (((maClose - maOpen) * 0.5) if (((maClose - maOpen) * 0.5) > 0.0) else (-((maClose - maOpen) * 0.5))))) if (maHigh != maLow) else ((maOpen + maClose) * 0.5))
        haOpen = (((hao[i - 1] + hac[i - 1]) * 0.5) if (i > 0) else ((open[i] + close[i]) * 0.5))
        haHigh = (maHigh if (maHigh > (haOpen if (haOpen > haClose) else haClose)) else haOpen if (haOpen > haClose) else haClose)
        haLow = (maLow if (maLow < (haOpen if (haOpen < haClose) else haClose)) else haOpen if (haOpen < haClose) else haClose)
        canl[i] = haLow
        hal[i] = canl[i]
        canh[i] = haHigh
        hah[i] = canh[i]
        cano[i] = haOpen
        hao[i] = cano[i]
        canc[i] = haClose
        hac[i] = canc[i]
        if i > 0:
            if _step > 0:
                if ((hah[i] - hah[i - 1]) if ((hah[i] - hah[i - 1]) > 0.0) else (-(hah[i] - hah[i - 1]))) < _step:
                    hah[i] = hah[i - 1]
                if ((hal[i] - hal[i - 1]) if ((hal[i] - hal[i - 1]) > 0.0) else (-(hal[i] - hal[i - 1]))) < _step:
                    hal[i] = hal[i - 1]
                if ((hao[i] - hao[i - 1]) if ((hao[i] - hao[i - 1]) > 0.0) else (-(hao[i] - hao[i - 1]))) < _step:
                    hao[i] = hao[i - 1]
                if ((hac[i] - hac[i - 1]) if ((hac[i] - hac[i - 1]) > 0.0) else (-(hac[i] - hac[i - 1]))) < _step:
                    hac[i] = hac[i - 1]
            acD = 0
            if acb[i] > acb[i - 1]:
                acD = 1
            if acb[i] < acb[i - 1]:
                acD = 2
            aoD = 0
            if aob[i] > aob[i - 1]:
                aoD = 1
            if aob[i] < aob[i - 1]:
                aoD = 2
            cancl[i] = (0 if (acD == 1 and aoD == 1) else 1 if (acD == 2 and aoD == 2) else 2 if (acD == 1 and aoD == 2) else 3)
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


class HeikenAshiSmoothedZoneTrade(_MQL5Indicator):
    name = 'Heiken Ashi smoothed zone trade'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpMaPeriod': 7,  # Smoothing period (<= 1 for no smoothing)
        'inpMaMetod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=3),  # Smoothing method
        'inpStep': 0.0,  # Step size (in pips)
        'inpBetterFormula': False,  # Use better formula?
    }

