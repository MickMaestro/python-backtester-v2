"""kagi — converted from MQL5: MQL5 Indicators/Kagi/kagi.mq5

The Kagi chart.
Copyright: Copyright 2012, Rone.; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, Rone.', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 4}, 'types': {1: 4, 2: 4, 3: 8, 4: 8}, 'colors': {1: [16711680], 2: [255], 3: [255, 16711680], 4: [255, 16711680]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Yang', 2: 'Yin', 3: 'BendTop', 4: 'BendBottom'}, 'levels': [], 'description': ['The Kagi chart.'], 'name': 'kagi', 'source': 'MQL5 Indicators/Kagi/kagi.mq5', 'folder': 'Kagi', 'inputs': [{'mql': 'InpMode', 'py': 'InpMode', 'param': 'InpMode', 'type': 'int', 'default': 0, 'label': 'Reversal', 'sinput': False}, {'mql': 'InpPips', 'py': 'InpPips', 'param': 'InpPips', 'type': 'int', 'default': 100, 'label': 'Reversal in pips', 'sinput': False}, {'mql': 'InpPercent', 'py': 'InpPercent', 'param': 'InpPercent', 'type': 'double', 'default': 0.5, 'label': 'Reversal in %', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum REVERSAL_MODE
PIPS = 0
PERCENT = 1
_enum('REVERSAL_MODE', {0: 'PIPS', 1: 'PERCENT'})

# ---- inputs and global variables
InpMode = _input('InpMode', PIPS)  # Reversal
InpPips = _input('InpPips', 100)  # Reversal in pips
InpPercent = _input('InpPercent', 0.5)  # Reversal in %
YangBuffer1 = Arr(0, 0.0)
YangBuffer2 = Arr(0, 0.0)
YinBuffer1 = Arr(0, 0.0)
YinBuffer2 = Arr(0, 0.0)
BendTopBuffer = Arr(0, 0.0)
BendTopColors = Arr(0, 0.0)
BendBottomBuffer = Arr(0, 0.0)
BendBottomColors = Arr(0, 0.0)
KagiBuffer = Arr(0, 0.0)
kagiShift = 0

def OnInit():
    SetIndexBuffer(0, YangBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, YangBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, YinBuffer1, INDICATOR_DATA)
    SetIndexBuffer(3, YinBuffer2, INDICATOR_DATA)
    SetIndexBuffer(4, BendTopBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, BendTopColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, BendBottomBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, BendBottomColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(8, KagiBuffer, INDICATOR_CALCULATIONS)
    for i in range(0, 4):
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, STYLE_SOLID)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    modeData = ((_str(InpPips) + ' pips') if (InpMode == PIPS) else (DoubleToString(InpPercent, 2) + '%'))
    IndicatorSetString(INDICATOR_SHORTNAME, 'Kagi (' + modeData + ')')
    return 0

def getReversal(price):
    if InpMode == PIPS:
        return InpPips * Point()
    return NormalizeDouble((price / 100) * InpPercent, Digits())

def OnCalculate(rates_total, prev_calculated, begin, price):
    global kagiShift
    shift = 1
    up = False
    yang = False
    localMin = 0.0
    localMax = 0.0
    reversal = getReversal(price[0])
    while MathAbs(price[shift] - price[0]) < reversal:
        pass
        shift += 1
    KagiBuffer[1] = price[0]
    KagiBuffer[0] = KagiBuffer[1]
    KagiBuffer[2] = price[shift]
    kagiShift = 2
    if price[shift] > price[0]:
        up = True
        yang = True
        localMin = price[0]
        localMax = price[shift]
    else:
        up = False
        yang = False
        localMin = price[shift]
        localMax = price[0]
    for bar in range(shift, rates_total):
        curPrice = price[bar]
        reversal = getReversal(KagiBuffer[kagiShift])
        if up:
            if curPrice > KagiBuffer[kagiShift]:
                KagiBuffer[kagiShift] = curPrice
            elif curPrice < (KagiBuffer[kagiShift] - reversal):
                kagiShift += 1
                KagiBuffer[kagiShift] = KagiBuffer[kagiShift - 1]
                kagiShift += 1
                KagiBuffer[kagiShift] = curPrice
                up = False
        else:
            if curPrice < KagiBuffer[kagiShift]:
                KagiBuffer[kagiShift] = curPrice
            elif curPrice > (KagiBuffer[kagiShift] + reversal):
                kagiShift += 1
                KagiBuffer[kagiShift] = KagiBuffer[kagiShift - 1]
                kagiShift += 1
                KagiBuffer[kagiShift] = curPrice
                up = True
    for i in range(1, kagiShift + 1):
        bar = rates_total - kagiShift - 1 + i
        cur = KagiBuffer[i]
        prev = KagiBuffer[i - 1]
        if yang:
            YinBuffer2[bar] = 0.0
            YinBuffer1[bar] = YinBuffer2[bar]
            BendBottomColors[bar] = 1.0
            BendTopColors[bar] = BendBottomColors[bar]
            if cur > prev:
                localMin = prev
                YangBuffer1[bar] = localMin
                localMax = cur
                YangBuffer2[bar] = localMax
                BendTopBuffer[bar] = cur
                BendBottomBuffer[bar] = prev
            elif cur < prev:
                if cur < localMin:
                    localMax = prev
                    YangBuffer1[bar] = localMax
                    YinBuffer1[bar] = localMin
                    YangBuffer2[bar] = YinBuffer1[bar]
                    localMin = cur
                    YinBuffer2[bar] = localMin
                    yang = False
                    BendTopBuffer[bar] = prev
                    BendBottomBuffer[bar] = cur
                else:
                    localMax = prev
                    YangBuffer1[bar] = localMax
                    localMin = cur
                    YangBuffer2[bar] = localMin
                    BendTopBuffer[bar] = prev
                    BendBottomBuffer[bar] = cur
            else:
                YangBuffer2[bar] = 0.0
                YangBuffer1[bar] = YangBuffer2[bar]
                if cur == localMin:
                    BendTopBuffer[bar] = 0.0
                    BendBottomBuffer[bar] = cur
                else:
                    BendTopBuffer[bar] = cur
                    BendBottomBuffer[bar] = 0.0
        else:
            YangBuffer2[bar] = 0.0
            YangBuffer1[bar] = YangBuffer2[bar]
            BendBottomColors[bar] = 0.0
            BendTopColors[bar] = BendBottomColors[bar]
            if cur < prev:
                localMax = prev
                YinBuffer1[bar] = localMax
                localMin = cur
                YinBuffer2[bar] = localMin
                BendTopBuffer[bar] = prev
                BendBottomBuffer[bar] = cur
            elif cur > prev:
                if cur > localMax:
                    localMin = prev
                    YinBuffer1[bar] = localMin
                    YangBuffer1[bar] = localMax
                    YinBuffer2[bar] = YangBuffer1[bar]
                    localMax = cur
                    YangBuffer2[bar] = localMax
                    yang = True
                    BendTopBuffer[bar] = cur
                    BendBottomBuffer[bar] = prev
                else:
                    localMin = prev
                    YinBuffer1[bar] = localMin
                    localMax = cur
                    YinBuffer2[bar] = localMax
                    BendTopBuffer[bar] = cur
                    BendBottomBuffer[bar] = prev
            else:
                YinBuffer2[bar] = 0.0
                YinBuffer1[bar] = YinBuffer2[bar]
                if cur == localMin:
                    BendTopBuffer[bar] = 0.0
                    BendBottomBuffer[bar] = cur
                else:
                    BendTopBuffer[bar] = cur
                    BendBottomBuffer[bar] = 0.0
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, price[rates_total - 1])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Kagi(_MQL5Indicator):
    name = 'kagi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpMode': _Choice({0: 'In pips', 1: 'In percentage'}, default=0),  # Reversal
        'InpPips': 100,  # Reversal in pips
        'InpPercent': 0.5,  # Reversal in %
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

