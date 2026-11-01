"""Heiken Ashi zone trade - separate — converted from MQL5: MQL5 Indicators/Heiken Ashi Zone Trade - Separate/Heiken Ashi zone trade - separate.mq5

Heiken Ashi zone trade separate
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16760576, 6333684, 12632256, 12632256]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Heiken Ashi zone trade separate'], 'name': 'Heiken Ashi zone trade - separate', 'source': 'MQL5 Indicators/Heiken Ashi Zone Trade - Separate/Heiken Ashi zone trade - separate.mq5', 'folder': 'Heiken Ashi Zone Trade - Separate', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
canh = Arr(0, 0.0)
canl = Arr(0, 0.0)
cano = Arr(0, 0.0)
canc = Arr(0, 0.0)
cancl = Arr(0, 0.0)
hah = Arr(0, 0.0)
hal = Arr(0, 0.0)
hao = Arr(0, 0.0)
hac = Arr(0, 0.0)
_acHandle = 0
_aoHandle = 0

def OnInit():
    global _acHandle, _aoHandle
    SetIndexBuffer(0, cano, INDICATOR_DATA)
    SetIndexBuffer(1, canh, INDICATOR_DATA)
    SetIndexBuffer(2, canl, INDICATOR_DATA)
    SetIndexBuffer(3, canc, INDICATOR_DATA)
    SetIndexBuffer(4, cancl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, hao, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, hah, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, hal, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, hac, INDICATOR_CALCULATIONS)
    _acHandle = iAC(Symbol(), 0)
    if _acHandle == INVALID_HANDLE:
        return INIT_FAILED
    _aoHandle = iAO(Symbol(), 0)
    if _aoHandle == INVALID_HANDLE:
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Heiken Ashi zone trade')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if BarsCalculated(_acHandle) < rates_total:
        return prev_calculated
    if BarsCalculated(_aoHandle) < rates_total:
        return prev_calculated
    _acValues = Arr(2, 0.0, dyn=False)
    _aoValues = Arr(2, 0.0, dyn=False)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        haOpen = (((hao[i - 1] + hac[i - 1]) / 2) if (i > 0) else ((open[i] + close[i]) / 2))
        haClose = (open[i] + high[i] + low[i] + close[i]) / 4
        haHigh = MathMax(high[i], MathMax(haOpen, haClose))
        haLow = MathMin(low[i], MathMin(haOpen, haClose))
        hal[i] = haLow
        hah[i] = haHigh
        hao[i] = haOpen
        hac[i] = haClose
        if i == 0:
            i += 1
            continue
        _acValuesCopied = CopyBuffer(_acHandle, 0, _DT(time[i]), 2, _acValues)
        if _acValuesCopied != 2:
            break
        _aoValuesCopied = CopyBuffer(_aoHandle, 0, _DT(time[i]), 2, _aoValues)
        if _aoValuesCopied != 2:
            break
        acD = 0
        if _acValues[1] > _acValues[0]:
            acD = 1
        if _acValues[1] < _acValues[0]:
            acD = 2
        aoD = 0
        if _aoValues[1] > _aoValues[0]:
            aoD = 1
        if _aoValues[1] < _aoValues[0]:
            aoD = 2
        cancl[i] = (0 if (acD == 1 and aoD == 1) else 1 if (acD == 2 and aoD == 2) else 2 if (acD == 1 and aoD == 2) else 3)
        canh[i] = hah[i]
        canl[i] = hal[i]
        canc[i] = hac[i]
        cano[i] = hao[i]
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HeikenAshiZoneTradeSeparate(_MQL5Indicator):
    name = 'Heiken Ashi zone trade - separate'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

