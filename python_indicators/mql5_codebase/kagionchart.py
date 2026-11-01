"""kagionchart — converted from MQL5: MQL5 Indicators/Kagi On Chart/kagionchart.mq5

The Kagi chart in the main chart window considering the time scale.
Copyright: Copyright 2012, Rone.; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, Rone.', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 5}, 'types': {1: 4, 2: 4, 3: 8, 4: 8, 5: 8}, 'colors': {1: [16711680], 2: [255], 3: [255, 16711680], 4: [255, 16711680], 5: [255, 16711680]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2, 5: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'Yang', 2: 'Yin', 3: 'Bend1', 4: 'Bend2', 5: 'Bend3'}, 'levels': [], 'description': ['The Kagi chart in the main chart window considering the time scale.'], 'name': 'kagionchart', 'source': 'MQL5 Indicators/Kagi On Chart/kagionchart.mq5', 'folder': 'Kagi On Chart', 'inputs': [{'mql': 'InpMode', 'py': 'InpMode', 'param': 'InpMode', 'type': 'int', 'default': 0, 'label': 'Reversal', 'sinput': False}, {'mql': 'InpPips', 'py': 'InpPips', 'param': 'InpPips', 'type': 'int', 'default': 100, 'label': 'Reversal in pips', 'sinput': False}, {'mql': 'InpPercent', 'py': 'InpPercent', 'param': 'InpPercent', 'type': 'double', 'default': 0.5, 'label': 'Reversal in %-х', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum REVERSAL_MODE
PIPS = 0
PERCENT = 1
_enum('REVERSAL_MODE', {0: 'PIPS', 1: 'PERCENT'})

# ---- inputs and global variables
InpMode = _input('InpMode', PIPS)  # Reversal
InpPips = _input('InpPips', 100)  # Reversal in pips
InpPercent = _input('InpPercent', 0.5)  # Reversal in %-х
YangBuffer1 = Arr(0, 0.0)
YangBuffer2 = Arr(0, 0.0)
YinBuffer1 = Arr(0, 0.0)
YinBuffer2 = Arr(0, 0.0)
Bend1Buffer = Arr(0, 0.0)
Bend1Colors = Arr(0, 0.0)
Bend2Buffer = Arr(0, 0.0)
Bend2Colors = Arr(0, 0.0)
Bend3Buffer = Arr(0, 0.0)
Bend3Colors = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, YangBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, YangBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, YinBuffer1, INDICATOR_DATA)
    SetIndexBuffer(3, YinBuffer2, INDICATOR_DATA)
    SetIndexBuffer(4, Bend1Buffer, INDICATOR_DATA)
    SetIndexBuffer(5, Bend1Colors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, Bend2Buffer, INDICATOR_DATA)
    SetIndexBuffer(7, Bend2Colors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(8, Bend3Buffer, INDICATOR_DATA)
    SetIndexBuffer(9, Bend3Colors, INDICATOR_COLOR_INDEX)
    for i in range(0, 5):
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, 0.0)
        PlotIndexSetInteger(i, PLOT_SHIFT, 0)
    for i in range(2, 5):
        PlotIndexSetInteger(i, PLOT_SHOW_DATA, False)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    modeData = ((_str(InpPips) + ' pips') if (InpMode == PIPS) else (DoubleToString(InpPercent, 2) + '%'))
    IndicatorSetString(INDICATOR_SHORTNAME, 'Kagi (' + modeData + ')')
    return 0

def getReversal(price):
    if InpMode == PIPS:
        return InpPips * Point()
    return NormalizeDouble((price / 100) * InpPercent, Digits())

def setBendContinue(bar, price, clr):
    if Bend1Buffer[bar - 1] == price:
        Bend1Buffer[bar] = price
        Bend1Colors[bar] = clr
    elif Bend2Buffer[bar - 1] == price:
        Bend2Buffer[bar] = price
        Bend2Colors[bar] = clr
    elif Bend3Buffer[bar - 1] == price:
        Bend3Buffer[bar] = price
        Bend3Colors[bar] = clr

def setBendNew(bar, price, clr):
    if Bend1Buffer[bar - 1] == 0.0:
        Bend1Buffer[bar] = price
        Bend1Colors[bar] = clr
    elif Bend2Buffer[bar - 1] == 0.0:
        Bend2Buffer[bar] = price
        Bend2Colors[bar] = clr
    elif Bend3Buffer[bar - 1] == 0.0:
        Bend3Buffer[bar] = price
        Bend3Colors[bar] = clr

def setBends(bar, contPrice, contClr, newPrice, newClr):
    setBendContinue(bar, contPrice, contClr)
    setBendNew(bar, newPrice, newClr)

def OnCalculate(rates_total, prev_calculated, begin, price):
    global _s_OnCalculate__localMax, _s_OnCalculate__localMin, _s_OnCalculate__reversalMax, _s_OnCalculate__reversalMin, _s_OnCalculate__up, _s_OnCalculate__yang
    startBar = 0
    up = False
    yang = False
    localMin = 0.0
    localMax = 0.0
    reversalMin = 0.0
    reversalMax = 0.0
    reversal = getReversal(price[0])
    if prev_calculated > rates_total or prev_calculated <= 0:
        ArrayInitialize(YangBuffer1, 0.0)
        ArrayInitialize(YangBuffer2, 0.0)
        ArrayInitialize(YinBuffer1, 0.0)
        ArrayInitialize(YinBuffer2, 0.0)
        ArrayInitialize(Bend1Buffer, 0.0)
        ArrayInitialize(Bend2Buffer, 0.0)
        ArrayInitialize(Bend3Buffer, 0.0)
        startBar = 1
        while (MathAbs(price[startBar] - price[0]) - reversal) <= 1e-05:
            pass
            startBar += 1
        if price[startBar] > price[0]:
            _s_OnCalculate__reversalMin = price[0]
            _s_OnCalculate__localMin = _s_OnCalculate__reversalMin
            _s_OnCalculate__reversalMax = price[startBar]
            _s_OnCalculate__localMax = _s_OnCalculate__reversalMax
            _s_OnCalculate__up = True
            _s_OnCalculate__yang = _s_OnCalculate__up
        else:
            _s_OnCalculate__reversalMin = price[startBar]
            _s_OnCalculate__localMin = _s_OnCalculate__reversalMin
            _s_OnCalculate__reversalMax = price[0]
            _s_OnCalculate__localMax = _s_OnCalculate__reversalMax
            _s_OnCalculate__up = False
            _s_OnCalculate__yang = _s_OnCalculate__up
    else:
        startBar = prev_calculated - 1
    up = _s_OnCalculate__up
    yang = _s_OnCalculate__yang
    localMin = _s_OnCalculate__localMin
    localMax = _s_OnCalculate__localMax
    reversalMin = _s_OnCalculate__reversalMin
    reversalMax = _s_OnCalculate__reversalMax
    for bar in range(startBar, rates_total):
        current = price[bar]
        if rates_total != prev_calculated and bar == (rates_total - 1):
            _s_OnCalculate__up = up
            _s_OnCalculate__yang = yang
            _s_OnCalculate__localMin = localMin
            _s_OnCalculate__localMax = localMax
            _s_OnCalculate__reversalMin = reversalMin
            _s_OnCalculate__reversalMax = reversalMax
        if yang:
            if up:
                reversal = getReversal(localMax)
                YangBuffer1[bar] = localMax
                if current > localMax:
                    setBends(bar, localMax, 1, current, 1)
                    YangBuffer2[bar] = current
                    localMax = current
                elif current < (localMax - reversal):
                    if current < reversalMin:
                        setBends(bar, localMax, 1, current, 0)
                        YinBuffer1[bar] = reversalMin
                        YangBuffer2[bar] = YinBuffer1[bar]
                        YinBuffer2[bar] = current
                        localMin = current
                        reversalMax = localMax
                        yang = False
                    else:
                        setBends(bar, localMax, 1, current, 1)
                        YangBuffer2[bar] = current
                        localMin = current
                        reversalMax = localMax
                    up = False
                else:
                    setBendContinue(bar, localMax, 1)
                    YangBuffer2[bar] = localMax
            else:
                reversal = getReversal(localMin)
                YangBuffer1[bar] = localMin
                if current < localMin:
                    if current < reversalMin:
                        setBends(bar, localMin, 1, current, 0)
                        YinBuffer1[bar] = reversalMin
                        YangBuffer2[bar] = YinBuffer1[bar]
                        YinBuffer2[bar] = current
                        localMin = current
                        reversalMax = localMax
                        yang = False
                    else:
                        setBends(bar, localMin, 1, current, 1)
                        YangBuffer2[bar] = current
                        localMin = current
                elif current > (localMin + reversal):
                    setBends(bar, localMin, 1, current, 1)
                    YangBuffer2[bar] = current
                    localMax = current
                    reversalMin = localMin
                    up = True
                else:
                    setBendContinue(bar, localMin, 1)
                    YangBuffer2[bar] = localMin
        else:
            if up:
                reversal = getReversal(localMax)
                YinBuffer1[bar] = localMax
                if current > localMax:
                    if current > reversalMax:
                        setBends(bar, localMax, 0, current, 1)
                        YangBuffer1[bar] = reversalMax
                        YinBuffer2[bar] = YangBuffer1[bar]
                        YangBuffer2[bar] = current
                        localMax = current
                        reversalMin = localMin
                        yang = True
                    else:
                        setBends(bar, localMax, 0, current, 0)
                        YinBuffer2[bar] = current
                        localMax = current
                elif current < (localMax - reversal):
                    setBends(bar, localMax, 0, current, 0)
                    YinBuffer2[bar] = current
                    localMin = current
                    reversalMax = localMax
                    up = False
                else:
                    setBendContinue(bar, localMax, 0)
                    YinBuffer2[bar] = localMax
            else:
                reversal = getReversal(localMin)
                YinBuffer1[bar] = localMin
                if current < localMin:
                    setBends(bar, localMin, 0, current, 0)
                    YinBuffer2[bar] = current
                    localMin = current
                elif current > (localMin + reversal):
                    if current > reversalMax:
                        setBends(bar, localMin, 0, current, 1)
                        YangBuffer1[bar] = reversalMax
                        YinBuffer2[bar] = YangBuffer1[bar]
                        YangBuffer2[bar] = current
                        localMax = current
                        reversalMin = localMin
                        yang = True
                    else:
                        setBends(bar, localMin, 0, current, 0)
                        YinBuffer2[bar] = current
                        localMax = current
                        reversalMin = localMin
                    up = True
                else:
                    setBendContinue(bar, localMin, 0)
                    YinBuffer2[bar] = localMin
    return rates_total

# ---- static local variables
_s_OnCalculate__up = False
_s_OnCalculate__yang = False
_s_OnCalculate__localMin = 0.0
_s_OnCalculate__localMax = 0.0
_s_OnCalculate__reversalMin = 0.0
_s_OnCalculate__reversalMax = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Kagionchart(_MQL5Indicator):
    name = 'kagionchart'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMode': _Choice({0: 'In pips', 1: 'In percentage'}, default=0),  # Reversal
        'InpPips': 100,  # Reversal in pips
        'InpPercent': 0.5,  # Reversal in %-х
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

