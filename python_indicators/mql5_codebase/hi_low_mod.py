"""Hi-low mod — converted from MQL5: MQL5 Indicators/Hi_lo mod/Hi-low mod.mq5

Hi/lo mod (variation of hi/low indicator)
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [3329330]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Hi/lo mod (variation of hi/low indicator)'], 'name': 'Hi-low mod', 'source': 'MQL5 Indicators/Hi_lo mod/Hi-low mod.mq5', 'folder': 'Hi_lo mod', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 2, 'label': 'Calculating period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 2)  # Calculating period
up = Arr(0, 0.0)
down = Arr(0, 0.0)
state = Arr(0, 0.0)
_handleH = 0
_handleL = 0

def OnInit():
    global _handleH, _handleL
    SetIndexBuffer(0, up, INDICATOR_DATA)
    SetIndexBuffer(1, down, INDICATOR_DATA)
    SetIndexBuffer(2, state, INDICATOR_CALCULATIONS)
    _handleH = iMA(Symbol(), Period(), inpPeriod, 1, MODE_SMA, PRICE_HIGH)
    if _handleH == INVALID_HANDLE:
        return INIT_FAILED
    _handleL = iMA(Symbol(), Period(), inpPeriod, 1, MODE_SMA, PRICE_LOW)
    if _handleL == INVALID_HANDLE:
        IndicatorRelease(_handleH)
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Hi/lo mod (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    if _handleH != INVALID_HANDLE:
        IndicatorRelease(_handleH)
    if _handleL != INVALID_HANDLE:
        IndicatorRelease(_handleL)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    _valh = Arr(1, 0.0, dyn=False)
    _vall = Arr(1, 0.0, dyn=False)
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _valhCopied = CopyBuffer(_handleH, 0, rates_total - i - 1, 1, _valh)
        if _valhCopied != 1:
            i += 1
            continue
        _vallCopied = CopyBuffer(_handleL, 0, rates_total - i - 1, 1, _vall)
        if _vallCopied != 1:
            i += 1
            continue
        state[i] = (state[i - 1] if (i > 0) else 0)
        if close[i] < _valh[0]:
            state[i] = -1.0
        if close[i] > _vall[0]:
            state[i] = 1.0
        up[i] = ((_valh[0] + (2 * Point())) if (state[i] == -1) else EMPTY_VALUE)
        down[i] = ((_vall[0] - (2 * Point())) if (state[i] == 1) else EMPTY_VALUE)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HiLowMod(_MQL5Indicator):
    name = 'Hi-low mod'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 2,  # Calculating period
    }

