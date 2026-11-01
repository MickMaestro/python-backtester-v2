"""iheikenashism — converted from MQL5: MQL5 Indicators/iHeikenAshiSm/iheikenashism.mq5

Copyright: Integer; Link: http://dmffx.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Integer', 'link': 'http://dmffx.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 17, 'indicator_plots': 1}, 'types': {}, 'colors': {1: [16748574, 255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'HeikenAshi'}, 'levels': [], 'description': [], 'name': 'iheikenashism', 'source': 'MQL5 Indicators/iHeikenAshiSm/iheikenashism.mq5', 'folder': 'iHeikenAshiSm', 'inputs': [{'mql': 'Variant', 'py': 'Variant', 'param': 'Variant', 'type': 'int', 'default': 0, 'label': 'Variant', 'sinput': False}, {'mql': 'Type', 'py': 'Type', 'param': 'Type', 'type': 'int', 'default': 17, 'label': 'Type', 'sinput': False}, {'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'int', 'default': 1, 'label': 'MAPeriod', 'sinput': False}, {'mql': 'MAMethod', 'py': 'MAMethod', 'param': 'MAMethod', 'type': 'int', 'default': 0, 'label': 'MAMethod', 'sinput': False}, {'mql': 'SmPeriod', 'py': 'SmPeriod', 'param': 'SmPeriod', 'type': 'int', 'default': 1, 'label': 'SmPeriod', 'sinput': False}, {'mql': 'SmMethod', 'py': 'SmMethod', 'param': 'SmMethod', 'type': 'int', 'default': 0, 'label': 'SmMethod', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum eType
CANDLES = 17
BARS = 16
_enum('eType', {17: 'CANDLES', 16: 'BARS'})

# enum eVar
HeikenAshi = 0
Price = 1
_enum('eVar', {0: 'HeikenAshi', 1: 'Price'})

# ---- inputs and global variables
Variant = _input('Variant', HeikenAshi)  # Variant
Type = _input('Type', CANDLES)  # Type
MAPeriod = _input('MAPeriod', 1)  # MAPeriod
MAMethod = _input('MAMethod', MODE_SMA)  # MAMethod
SmPeriod = _input('SmPeriod', 1)  # SmPeriod
SmMethod = _input('SmMethod', MODE_SMA)  # SmMethod
HeikenAshiBuffer1 = Arr(0, 0.0)
HeikenAshiBuffer2 = Arr(0, 0.0)
HeikenAshiBuffer3 = Arr(0, 0.0)
HeikenAshiBuffer4 = Arr(0, 0.0)
HeikenAshiColors = Arr(0, 0.0)
OpenMABuffer = Arr(0, 0.0)
HighMABuffer = Arr(0, 0.0)
LowMABuffer = Arr(0, 0.0)
CloseMABuffer = Arr(0, 0.0)
_open = Arr(0, 0.0)
_high = Arr(0, 0.0)
_low = Arr(0, 0.0)
_close = Arr(0, 0.0)
_openSm = Arr(0, 0.0)
_highSm = Arr(0, 0.0)
_lowSm = Arr(0, 0.0)
_closeSm = Arr(0, 0.0)
OpenMAHandle = 0
HighMAHandle = 0
LowMAHandle = 0
CloseMAHandle = 0

def OnInit():
    global CloseMAHandle, HighMAHandle, LowMAHandle, OpenMAHandle
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, Type)
    SetIndexBuffer(0, HeikenAshiBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, HeikenAshiBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, HeikenAshiBuffer3, INDICATOR_DATA)
    SetIndexBuffer(3, HeikenAshiBuffer4, INDICATOR_DATA)
    SetIndexBuffer(4, HeikenAshiColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, OpenMABuffer, INDICATOR_DATA)
    SetIndexBuffer(6, HighMABuffer, INDICATOR_DATA)
    SetIndexBuffer(7, LowMABuffer, INDICATOR_DATA)
    SetIndexBuffer(8, CloseMABuffer, INDICATOR_DATA)
    SetIndexBuffer(9, _open, INDICATOR_DATA)
    SetIndexBuffer(10, _high, INDICATOR_DATA)
    SetIndexBuffer(11, _low, INDICATOR_DATA)
    SetIndexBuffer(12, _close, INDICATOR_DATA)
    SetIndexBuffer(13, _openSm, INDICATOR_DATA)
    SetIndexBuffer(14, _highSm, INDICATOR_DATA)
    SetIndexBuffer(15, _lowSm, INDICATOR_DATA)
    SetIndexBuffer(16, _closeSm, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(3, PLOT_SHOW_DATA, False)
    OpenMAHandle = iMA(Symbol(), PERIOD_CURRENT, MAPeriod, 0, MAMethod, PRICE_OPEN)
    HighMAHandle = iMA(Symbol(), PERIOD_CURRENT, MAPeriod, 0, MAMethod, PRICE_HIGH)
    LowMAHandle = iMA(Symbol(), PERIOD_CURRENT, MAPeriod, 0, MAMethod, PRICE_LOW)
    CloseMAHandle = iMA(Symbol(), PERIOD_CURRENT, MAPeriod, 0, MAMethod, PRICE_CLOSE)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_error
    start = 0
    start2 = 0
    start3 = 0
    begin2 = 0
    beginX = 0
    if prev_calculated == 0:
        _s_OnCalculate_error = True
    if _s_OnCalculate_error:
        start = MAPeriod
        begin2 = start
        start2 = begin2
        start3 = start2
        beginX = start3
        _s_OnCalculate_error = False
        ArrayInitialize(HeikenAshiBuffer1, EMPTY_VALUE)
        ArrayInitialize(HeikenAshiBuffer2, EMPTY_VALUE)
        ArrayInitialize(HeikenAshiBuffer3, EMPTY_VALUE)
        ArrayInitialize(HeikenAshiBuffer4, EMPTY_VALUE)
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, MAPeriod + SmPeriod)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, MAPeriod + SmPeriod)
        PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, MAPeriod + SmPeriod)
        PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, MAPeriod + SmPeriod)
    else:
        start = prev_calculated - 1
        start2 = start
        start3 = start
    if CopyBuffer(OpenMAHandle, 0, 0, rates_total - start, OpenMABuffer) == -1:
        _s_OnCalculate_error = True
        return 0
    if CopyBuffer(HighMAHandle, 0, 0, rates_total - start, HighMABuffer) == -1:
        _s_OnCalculate_error = True
        return 0
    if CopyBuffer(LowMAHandle, 0, 0, rates_total - start, LowMABuffer) == -1:
        _s_OnCalculate_error = True
        return 0
    if CopyBuffer(CloseMAHandle, 0, 0, rates_total - start, CloseMABuffer) == -1:
        _s_OnCalculate_error = True
        return 0
    if start2 == begin2:
        _open[start2] = OpenMABuffer[start2]
        _high[start2] = HighMABuffer[start2]
        _low[start2] = LowMABuffer[start2]
        _close[start2] = CloseMABuffer[start2]
        start2 += 1
    for i in range(start2, rates_total):
        _close[i] = (OpenMABuffer[i] + HighMABuffer[i] + LowMABuffer[i] + CloseMABuffer[i]) / 4
        _open[i] = (_open[i - 1] + _close[i - 1]) / 2
        _high[i] = MathMax(HighMABuffer[i], MathMax(_open[i], _close[i]))
        _low[i] = MathMin(LowMABuffer[i], MathMin(_open[i], _close[i]))
    fMAOnArray2(_open, _openSm, SmPeriod, SmMethod, beginX, start3, rates_total)
    fMAOnArray2(_high, _highSm, SmPeriod, SmMethod, beginX, start3, rates_total)
    fMAOnArray2(_low, _lowSm, SmPeriod, SmMethod, beginX, start3, rates_total)
    fMAOnArray2(_close, _closeSm, SmPeriod, SmMethod, beginX, start3, rates_total)
    if Variant == HeikenAshi:
        for i in range(start3, rates_total):
            HeikenAshiColors[i] = HeikenAshiColors[i - 1]
            HeikenAshiBuffer1[i] = _openSm[i]
            HeikenAshiBuffer2[i] = MathMax(_highSm[i], MathMax(_openSm[i], _closeSm[i]))
            HeikenAshiBuffer3[i] = MathMin(_lowSm[i], MathMin(_openSm[i], _closeSm[i]))
            HeikenAshiBuffer4[i] = _closeSm[i]
            if _closeSm[i] < _openSm[i]:
                HeikenAshiColors[i] = 1.0
            if _closeSm[i] > _openSm[i]:
                HeikenAshiColors[i] = 0.0
    else:
        for i in range(start3, rates_total):
            HeikenAshiColors[i] = HeikenAshiColors[i - 1]
            HeikenAshiBuffer1[i] = open[i]
            HeikenAshiBuffer2[i] = high[i]
            HeikenAshiBuffer3[i] = low[i]
            HeikenAshiBuffer4[i] = close[i]
            if _closeSm[i] < _openSm[i]:
                HeikenAshiColors[i] = 1.0
            if _closeSm[i] > _openSm[i]:
                HeikenAshiColors[i] = 0.0
    return rates_total

def fMAOnArray2(aData, aMA, aPeriod, aMethod, aBegin, aStart, aRatesTotal):
    p1 = 0.0
    p2 = 0.0
    tWS = 0.0
    _sw1 = aMethod
    if _sw1 == MODE_SMA:
        aStart = MathMax(aStart, aBegin + aPeriod)
        for i in range(aStart, aRatesTotal):
            if i == (aBegin + aPeriod):
                aMA[i] = 0.0
                for j in range(0, aPeriod):
                    aMA[i] += aData[i - j]
                aMA[i] = _fdiv(aMA[i], aPeriod)
            else:
                aMA[i] = aMA[i - 1] - _fdiv(aData[i - aPeriod] - aData[i], aPeriod)
    elif _sw1 == MODE_EMA:
        if aStart == aBegin:
            aMA[aBegin] = aData[aBegin]
            aStart += 1
        p1 = _fdiv(2.0, 1.0 + aPeriod)
        p2 = 1.0 - p1
        for i in range(aStart, aRatesTotal):
            aMA[i] = (p1 * aData[i]) + (p2 * aMA[i - 1])
    elif _sw1 == MODE_LWMA:
        aStart = MathMax(aStart, aBegin + aPeriod)
        tWS = ((1.0 + aPeriod) / 2.0) * aPeriod
        for i in range(aStart, aRatesTotal):
            aMA[i] = 0.0
            for j in range(0, aPeriod):
                aMA[i] += aData[i - j] * (aPeriod - j)
            aMA[i] = _fdiv(aMA[i], tWS)
    elif _sw1 == MODE_SMMA:
        if aStart == aBegin:
            aMA[aBegin] = aData[aBegin]
            aStart += 1
        p1 = _fdiv(1.0, aPeriod)
        p2 = 1.0 - p1
        for i in range(aStart, aRatesTotal):
            aMA[i] = (p1 * aData[i]) + (p2 * aMA[i - 1])

def fMADrawBegin(aPeriod, aMethod):
    _sw2 = aMethod
    if _sw2 == 1:
        return 10 * aPeriod
    elif _sw2 == 2:
        return 20 * aPeriod
    return aPeriod

# ---- static local variables
_s_OnCalculate_error = True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Iheikenashism(_MQL5Indicator):
    name = 'iheikenashism'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Variant': _Choice({0: 'HeikenAshi', 1: 'Price'}, default=0),  # Variant
        'Type': _Choice({17: 'CANDLES', 16: 'BARS'}, default=17),  # Type
        'MAPeriod': 1,  # MAPeriod
        'MAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MAMethod
        'SmPeriod': 1,  # SmPeriod
        'SmMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # SmMethod
    }

