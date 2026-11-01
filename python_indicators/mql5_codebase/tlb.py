"""tlb — converted from MQL5: MQL5 Indicators/Three Line Break/tlb.mq5

Chart of (three)linear breakthrough.
Copyright: Copyright 2012, Rone.; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, Rone.', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [255, 16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Line Break'}, 'levels': [], 'description': ['Chart of (three)linear breakthrough.'], 'name': 'tlb', 'source': 'MQL5 Indicators/Three Line Break/tlb.mq5', 'folder': 'Three Line Break', 'inputs': [{'mql': 'InpLines', 'py': 'InpLines', 'param': 'InpLines', 'type': 'int', 'default': 3, 'label': 'Number of lines', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpLines = _input('InpLines', 3)  # Number of lines
LbBuffer1 = Arr(0, 0.0)
LbBuffer2 = Arr(0, 0.0)
LbBuffer3 = Arr(0, 0.0)
LbBuffer4 = Arr(0, 0.0)
LbColors = Arr(0, 0.0)
LbMax = Arr(0, 0.0)
LbMin = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, LbBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, LbBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, LbBuffer3, INDICATOR_DATA)
    SetIndexBuffer(3, LbBuffer4, INDICATOR_DATA)
    SetIndexBuffer(4, LbColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, LbMax, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, LbMin, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, STYLE_SOLID)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, _str(InpLines) + ' Line Break')
    return 0

def getLinePrice(line, lineShift, up=True):
    price = 0.0
    if up:
        price = LbMax[lineShift.v]
        for i in range(1, line):
            if LbMax[lineShift.v - i] > price:
                price = LbMax[lineShift.v - i]
    else:
        price = LbMin[lineShift.v]
        for i in range(1, line):
            if LbMin[lineShift.v - i] < price:
                price = LbMin[lineShift.v - i]
    return price

def processPrice(price, i, lineShift):
    if price > LbMax[i - 1]:
        LbMax[i] = price
        LbMin[i] = LbMax[i - 1]
        lineShift.v += 1
    elif price < LbMin[i - 1]:
        LbMin[i] = price
        LbMax[i] = LbMin[i - 1]
        lineShift.v += 1

def OnCalculate(rates_total, prev_calculated, begin, price):
    barShift = 1
    lineShift = Box(0)
    while price[0] == price[barShift]:
        pass
        barShift += 1
    if price[0] > price[barShift]:
        LbMax[0] = price[0]
        LbMin[0] = price[barShift]
    else:
        LbMax[0] = price[barShift]
        LbMin[0] = price[0]
    for i in range(1, InpLines):
        while price[barShift] <= getLinePrice(i, lineShift) and price[barShift] >= getLinePrice(i, lineShift, False):
            pass
            barShift += 1
        processPrice(price[barShift], i, lineShift)
    for i in range(InpLines, rates_total):
        while (barShift < rates_total and price[barShift] <= getLinePrice(InpLines, lineShift)) and price[barShift] >= getLinePrice(InpLines, lineShift, False):
            pass
            barShift += 1
        if barShift < rates_total:
            processPrice(price[barShift], i, lineShift)
    for i in range(1, lineShift.v + 1):
        bar = rates_total - lineShift.v - 1 + i
        if LbMax[i] > LbMax[i - 1]:
            LbBuffer2[bar] = LbMax[i]
            LbBuffer4[bar] = LbBuffer2[bar]
            LbBuffer3[bar] = LbMin[i]
            LbBuffer1[bar] = LbBuffer3[bar]
            LbColors[bar] = 1.0
        if LbMax[i] < LbMax[i - 1]:
            LbBuffer2[bar] = LbMin[i]
            LbBuffer4[bar] = LbBuffer2[bar]
            LbBuffer3[bar] = LbMax[i]
            LbBuffer1[bar] = LbBuffer3[bar]
            LbColors[bar] = 0.0
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, price[rates_total - 1])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Tlb(_MQL5Indicator):
    name = 'tlb'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpLines': 3,  # Number of lines
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

