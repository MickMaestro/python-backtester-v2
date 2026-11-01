"""3 MAs Market — converted from MQL5: MQL5 Indicators/3 MAs Market/3 MAs Market.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [3329330, 255, 2263842, 36095, 11119017]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Chaos zone'}, 'levels': [], 'description': [], 'name': '3 MAs Market', 'source': 'MQL5 Indicators/3 MAs Market/3 MAs Market.mq5', 'folder': '3 MAs Market', 'inputs': [{'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inMaLength1', 'py': 'inMaLength1', 'param': 'inMaLength1', 'type': 'int', 'default': 3, 'label': 'Fast ma period', 'sinput': False}, {'mql': 'inMaMode1', 'py': 'inMaMode1', 'param': 'inMaMode1', 'type': 'int', 'default': 3, 'label': 'Fast ma method', 'sinput': False}, {'mql': 'inMaLength2', 'py': 'inMaLength2', 'param': 'inMaLength2', 'type': 'int', 'default': 8, 'label': 'Medium ma period', 'sinput': False}, {'mql': 'inMaMode2', 'py': 'inMaMode2', 'param': 'inMaMode2', 'type': 'int', 'default': 3, 'label': 'Medium ma method', 'sinput': False}, {'mql': 'inMaLength3', 'py': 'inMaLength3', 'param': 'inMaLength3', 'type': 'int', 'default': 14, 'label': 'Slow ma period', 'sinput': False}, {'mql': 'inMaMode3', 'py': 'inMaMode3', 'param': 'inMaMode3', 'type': 'int', 'default': 3, 'label': 'Slow ma method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Price = _input('Price', PRICE_CLOSE)  # Price
inMaLength1 = _input('inMaLength1', 3)  # Fast ma period
inMaMode1 = _input('inMaMode1', MODE_LWMA)  # Fast ma method
inMaLength2 = _input('inMaLength2', 8)  # Medium ma period
inMaMode2 = _input('inMaMode2', MODE_LWMA)  # Medium ma method
inMaLength3 = _input('inMaLength3', 14)  # Slow ma period
inMaMode3 = _input('inMaMode3', MODE_LWMA)  # Slow ma method
chigh = Arr(0, 0.0)
clow = Arr(0, 0.0)
copen = Arr(0, 0.0)
cclose = Arr(0, 0.0)
ccolor = Arr(0, 0.0)
_ma1Handle = 0
_ma2Handle = 0
_ma3Handle = 0

def OnInit():
    global _ma1Handle, _ma2Handle, _ma3Handle
    SetIndexBuffer(0, copen, INDICATOR_DATA)
    SetIndexBuffer(1, chigh, INDICATOR_DATA)
    SetIndexBuffer(2, clow, INDICATOR_DATA)
    SetIndexBuffer(3, cclose, INDICATOR_DATA)
    SetIndexBuffer(4, ccolor, INDICATOR_COLOR_INDEX)
    _ma1Handle = iMA(Symbol(), 0, inMaLength1, 0, inMaMode1, Price)
    if _ma1Handle == INVALID_HANDLE:
        return INIT_FAILED
    _ma2Handle = iMA(Symbol(), 0, inMaLength2, 0, inMaMode2, Price)
    if _ma2Handle == INVALID_HANDLE:
        IndicatorRelease(_ma1Handle)
        return INIT_FAILED
    _ma3Handle = iMA(Symbol(), 0, inMaLength3, 0, inMaMode3, Price)
    if _ma3Handle == INVALID_HANDLE:
        IndicatorRelease(_ma1Handle)
        IndicatorRelease(_ma2Handle)
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, '3 MAs Market')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    if BarsCalculated(_ma1Handle) < rates_total:
        return prev_calculated
    if BarsCalculated(_ma2Handle) < rates_total:
        return prev_calculated
    if BarsCalculated(_ma3Handle) < rates_total:
        return prev_calculated
    _ma1Val = Arr(2, 0.0, dyn=False)
    _ma2Val = Arr(2, 0.0, dyn=False)
    _ma3Val = Arr(2, 0.0, dyn=False)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        chigh[i] = high[i]
        clow[i] = low[i]
        copen[i] = open[i]
        cclose[i] = close[i]
        _ma1Copied = CopyBuffer(_ma1Handle, 0, _DT(time[i]), 2, _ma1Val)
        _ma2Copied = CopyBuffer(_ma2Handle, 0, _DT(time[i]), 2, _ma2Val)
        _ma3Copied = CopyBuffer(_ma3Handle, 0, _DT(time[i]), 2, _ma3Val)
        if (_ma1Copied == 2 and _ma2Copied == 2) and _ma3Copied == 2:
            Cond1 = (_ma1Val[1] > _ma2Val[1] and _ma2Val[1] > _ma3Val[1]) and _ma1Val[1] > _ma1Val[0]
            Cond2 = (_ma1Val[1] > _ma2Val[1] and _ma2Val[1] < _ma3Val[1]) and _ma1Val[1] > _ma1Val[0]
            Cond3 = (_ma1Val[1] < _ma2Val[1] and _ma2Val[1] < _ma3Val[1]) and _ma1Val[1] < _ma1Val[0]
            Cond4 = (_ma1Val[1] < _ma2Val[1] and _ma2Val[1] > _ma3Val[1]) and _ma1Val[1] < _ma1Val[0]
            ccolor[i] = (0 if Cond1 else 2 if Cond2 else 1 if Cond3 else 3 if Cond4 else 4)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ind3MAsMarket(_MQL5Indicator):
    name = '3 MAs Market'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inMaLength1': 3,  # Fast ma period
        'inMaMode1': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=3),  # Fast ma method
        'inMaLength2': 8,  # Medium ma period
        'inMaMode2': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=3),  # Medium ma method
        'inMaLength3': 14,  # Slow ma period
        'inMaMode3': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=3),  # Slow ma method
    }

