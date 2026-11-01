"""Trend trigger factor (of averages)(dsl) — converted from MQL5: MQL5 Indicators/Trend trigger factor - discontinued signal line(s)/Trend trigger factor (of averages)(dsl).mq5

DSL Trend trigger factor
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 8}, 'colors': {1: [16760576, 6333684], 2: [11119017], 3: [11119017], 4: [11119017, 16748574, 17919]}, 'widths': {2: 0, 3: 0, 4: 2}, 'styles': {}, 'labels': {1: 'Filling', 2: 'Trend trigger factor level up', 3: 'Trend trigger factor level down'}, 'levels': [], 'description': ['DSL Trend trigger factor'], 'name': 'Trend trigger factor (of averages)(dsl)', 'source': 'MQL5 Indicators/Trend trigger factor - discontinued signal line(s)/Trend trigger factor (of averages)(dsl).mq5', 'folder': 'Trend trigger factor - discontinued signal line(s)', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 15, 'label': 'Period', 'sinput': False}, {'mql': 'inpAvgPeriod', 'py': 'inpAvgPeriod', 'param': 'inpAvgPeriod', 'type': 'int', 'default': 5, 'label': 'Pre-smoothing period', 'sinput': False}, {'mql': 'inpAvgMethod', 'py': 'inpAvgMethod', 'param': 'inpAvgMethod', 'type': 'int', 'default': 1, 'label': 'Pre-smoothing method', 'sinput': False}, {'mql': 'inpSignal', 'py': 'inpSignal', 'param': 'inpSignal', 'type': 'int', 'default': 10, 'label': 'DSL signal period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 15)  # Period
inpAvgPeriod = _input('inpAvgPeriod', 5)  # Pre-smoothing period
inpAvgMethod = _input('inpAvgMethod', MODE_EMA)  # Pre-smoothing method
inpSignal = _input('inpSignal', 10)  # DSL signal period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levu = Arr(0, 0.0)
levd = Arr(0, 0.0)
fup = Arr(0, 0.0)
fdn = Arr(0, 0.0)
mah = Arr(0, 0.0)
mal = Arr(0, 0.0)
ª_maNames = Arr.of(['SMA', 'EMA', 'SMMA', 'LWMA'], fill="")
ª_mahHandle = 0
ª_malHandle = 0
ª_maPeriod = 0
ª_dslAlpha = 0.0

def OnInit():
    global ª_dslAlpha, ª_maPeriod, ª_mahHandle, ª_malHandle
    SetIndexBuffer(0, fup, INDICATOR_DATA)
    SetIndexBuffer(1, fdn, INDICATOR_DATA)
    SetIndexBuffer(2, levu, INDICATOR_DATA)
    SetIndexBuffer(3, levd, INDICATOR_DATA)
    SetIndexBuffer(4, val, INDICATOR_DATA)
    SetIndexBuffer(5, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, mah, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, mal, INDICATOR_CALCULATIONS)
    ª_maPeriod = (inpAvgPeriod if (inpAvgPeriod > 1) else 1)
    ª_mahHandle = iMA(Symbol(), 0, ª_maPeriod, 0, inpAvgMethod, PRICE_HIGH)
    if not _checkHandle(ª_mahHandle, 'Average of high'):
        return INIT_FAILED
    ª_malHandle = iMA(Symbol(), 0, ª_maPeriod, 0, inpAvgMethod, PRICE_LOW)
    if not _checkHandle(ª_malHandle, 'Average of low'):
        return INIT_FAILED
    ª_dslAlpha = _fdiv(2.0, 1.0 + (inpSignal if (inpSignal > 1) else 1))
    IndicatorSetString(INDICATOR_SHORTNAME, 'DSL Trend trigger factor ' + ª_maNames[inpAvgMethod] + ' (' + _str(inpPeriod) + ',' + _str(ª_maPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_HighestHighOlder, _s_OnCalculate_HighestHighRecent, _s_OnCalculate_LowestLowOlder, _s_OnCalculate_LowestLowRecent, _s_OnCalculate_prev_i
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_mahHandle, 0, 0, _copyCount, mah) != _copyCount:
        return prev_calculated
    if CopyBuffer(ª_malHandle, 0, 0, _copyCount, mal) != _copyCount:
        return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        if _s_OnCalculate_prev_i != i:
            if mah[i] == EMPTY_VALUE:
                mah[i] = high[i]
            if mal[i] == EMPTY_VALUE:
                mal[i] = low[i]
            _s_OnCalculate_prev_i = i
            start = i - (inpPeriod * 2) + 1
            if start < 0:
                start = 0
            _s_OnCalculate_HighestHighOlder = mah[ArrayMaximum(mah, start, inpPeriod)]
            _s_OnCalculate_LowestLowOlder = mal[ArrayMinimum(mal, start, inpPeriod)]
            start = i - inpPeriod + 1
            if start < 0:
                start = 0
            _s_OnCalculate_HighestHighRecent = mah[ArrayMaximum(mah, start, inpPeriod - 1)]
            _s_OnCalculate_LowestLowRecent = mal[ArrayMinimum(mal, start, inpPeriod - 1)]
        BuyPower = (mah[i] if (mah[i] > _s_OnCalculate_HighestHighRecent) else _s_OnCalculate_HighestHighRecent) - _s_OnCalculate_LowestLowOlder
        SellPower = _s_OnCalculate_HighestHighOlder - (mal[i] if (mal[i] < _s_OnCalculate_LowestLowRecent) else _s_OnCalculate_LowestLowRecent)
        fdn[i] = (_fdiv(100.0 * (BuyPower - SellPower), 0.5 * (BuyPower + SellPower)) if ((BuyPower + SellPower) != 0) else 0)
        fup[i] = fdn[i]
        val[i] = fup[i]
        if i > 0:
            levu[i] = ((levu[i - 1] + (ª_dslAlpha * (val[i] - levu[i - 1]))) if (val[i] > 0) else levu[i - 1])
            levd[i] = ((levd[i - 1] + (ª_dslAlpha * (val[i] - levd[i - 1]))) if (val[i] < 0) else levd[i - 1])
        else:
            levd[i] = 0.0
            levu[i] = levd[i]
        valc[i] = (1 if (val[i] > levu[i]) else 2 if (val[i] < levd[i]) else 0)
        if valc[i] == 1:
            fdn[i] = levu[i]
        if valc[i] == 2:
            fdn[i] = levd[i]
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
_s_OnCalculate_HighestHighRecent = 0.0
_s_OnCalculate_LowestLowRecent = 0.0
_s_OnCalculate_HighestHighOlder = 0.0
_s_OnCalculate_LowestLowOlder = 0.0
_s_OnCalculate_prev_i = -1
_s__checkHandle__chandles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendTriggerFactorOfAveragesDsl(_MQL5Indicator):
    name = 'Trend trigger factor (of averages)(dsl)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 15,  # Period
        'inpAvgPeriod': 5,  # Pre-smoothing period
        'inpAvgMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Pre-smoothing method
        'inpSignal': 10,  # DSL signal period
    }

