"""renko — converted from MQL5: MQL5 Indicators/Renko/renko.mq5

The Renko chart. Regardless of whether what a time frame is used for the chart on which the indicator is attached, 
the Renko is calculated by the closing prices of М1 time frame.
Copyright: Copyright 2012, Rone.; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, Rone.', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [255, 16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Renko Open;Renko High;Renko Low;Renko Close'}, 'levels': [], 'description': ['The Renko chart. Regardless of whether what a time frame is used for the chart on which the indicator is attached, ', 'the Renko is calculated by the closing prices of М1 time frame.'], 'name': 'renko', 'source': 'MQL5 Indicators/Renko/renko.mq5', 'folder': 'Renko', 'inputs': [{'mql': 'InpBoxSize', 'py': 'InpBoxSize', 'param': 'InpBoxSize', 'type': 'int', 'default': 100, 'label': 'Box size (in pips)', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpBoxSize = _input('InpBoxSize', 100)  # Box size (in pips)
BoxOpenBuffer = Arr(0, 0.0)
BoxHighBuffer = Arr(0, 0.0)
BoxLowBuffer = Arr(0, 0.0)
BoxCloseBuffer = Arr(0, 0.0)
BoxColors = Arr(0, 0.0)
boxSize = 0.0

def OnInit():
    global boxSize
    if InpBoxSize < 50:
        boxSize = 50 * Point()
        Print('Incorrect parameter InpBoxSize = ', InpBoxSize, '. Value equal to 50 will be used.')
    else:
        boxSize = InpBoxSize * Point()
    SetIndexBuffer(0, BoxOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, BoxHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, BoxLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, BoxCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, BoxColors, INDICATOR_COLOR_INDEX)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, STYLE_SOLID)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Renko (' + _str(boxSize) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, begin, price):
    RenkoBuffer = Arr(0, 0.0)
    BackupBuffer = Arr(0, 0.0)
    Close = Arr(0, 0.0)
    m1RatesTotal = Bars(Symbol(), PERIOD_M1)
    renkoShift = 0
    barShift = 0
    while (ArrayResize(RenkoBuffer, m1RatesTotal) == -1 and ArrayResize(BackupBuffer, m1RatesTotal) == -1) and ArrayResize(Close, m1RatesTotal) == -1:
        pass
        m1RatesTotal = _idiv(m1RatesTotal, 2)
    if CopyClose(Symbol(), PERIOD_M1, 0, m1RatesTotal, Close) != m1RatesTotal:
        Print('Failed to copy history data for the М1 time frame. Error #', GetLastError())
        return 0
    RenkoBuffer[renkoShift] = Close[0]
    renkoShift += 1
    barShift = 1
    while MathAbs(Close[barShift] - Close[0]) <= boxSize:
        pass
        barShift += 1
    while Close[barShift] > (RenkoBuffer[renkoShift] + boxSize):
        renkoShift += 1
        RenkoBuffer[renkoShift] = RenkoBuffer[renkoShift - 1] + boxSize
    while Close[barShift] < (RenkoBuffer[renkoShift] - boxSize):
        renkoShift += 1
        RenkoBuffer[renkoShift] = RenkoBuffer[renkoShift - 1] - boxSize
    while barShift < m1RatesTotal:
        if renkoShift > (ArraySize(RenkoBuffer) - 100):
            ArrayCopy(BackupBuffer, RenkoBuffer)
            ArrayResize(RenkoBuffer, ArraySize(RenkoBuffer) + m1RatesTotal)
            ArrayCopy(RenkoBuffer, BackupBuffer, 0, 0, renkoShift + 1)
            ArrayResize(BackupBuffer, ArraySize(BackupBuffer) + m1RatesTotal)
        lastClose = Close[barShift]
        if RenkoBuffer[renkoShift] > RenkoBuffer[renkoShift - 1]:
            if lastClose > (RenkoBuffer[renkoShift] + boxSize):
                while lastClose > (RenkoBuffer[renkoShift] + boxSize):
                    renkoShift += 1
                    RenkoBuffer[renkoShift] = RenkoBuffer[renkoShift - 1] + boxSize
            elif lastClose < (RenkoBuffer[renkoShift] - (2 * boxSize)):
                renkoShift += 1
                RenkoBuffer[renkoShift] = RenkoBuffer[renkoShift - 1] - (2 * boxSize)
                while lastClose < (RenkoBuffer[renkoShift - 1] - boxSize):
                    renkoShift += 1
                    RenkoBuffer[renkoShift] = RenkoBuffer[renkoShift - 1] - boxSize
        if RenkoBuffer[renkoShift] < RenkoBuffer[renkoShift - 1]:
            if lastClose < (RenkoBuffer[renkoShift] - boxSize):
                while lastClose < (RenkoBuffer[renkoShift] - boxSize):
                    renkoShift += 1
                    RenkoBuffer[renkoShift] = RenkoBuffer[renkoShift - 1] - boxSize
            elif lastClose > (RenkoBuffer[renkoShift] + (2 * boxSize)):
                renkoShift += 1
                RenkoBuffer[renkoShift] = RenkoBuffer[renkoShift - 1] + (2 * boxSize)
                while lastClose > (RenkoBuffer[renkoShift] + boxSize):
                    renkoShift += 1
                    RenkoBuffer[renkoShift] = RenkoBuffer[renkoShift - 1] + boxSize
        barShift += 1
    ArrayInitialize(BoxOpenBuffer, 0.0)
    ArrayInitialize(BoxHighBuffer, 0.0)
    ArrayInitialize(BoxLowBuffer, 0.0)
    ArrayInitialize(BoxCloseBuffer, 0.0)
    if renkoShift > (rates_total - 100):
        for i in range(0, rates_total - 100 + 1):
            RenkoBuffer[i] = RenkoBuffer[i + renkoShift - (rates_total - 100)]
        renkoShift = rates_total - 100
    for i in range(2, renkoShift + 1):
        bar = rates_total - renkoShift - 1 + i
        current = RenkoBuffer[i]
        previous = RenkoBuffer[i - 1]
        penult = RenkoBuffer[i - 2]
        if current > previous:
            BoxColors[bar] = 1.0
            BoxHighBuffer[bar] = current
            BoxCloseBuffer[bar] = BoxHighBuffer[bar]
            if previous > penult:
                BoxLowBuffer[bar] = previous
                BoxOpenBuffer[bar] = BoxLowBuffer[bar]
            elif previous < penult:
                BoxLowBuffer[bar] = current - boxSize
                BoxOpenBuffer[bar] = BoxLowBuffer[bar]
        elif current < previous:
            BoxColors[bar] = 0.0
            BoxLowBuffer[bar] = current
            BoxCloseBuffer[bar] = BoxLowBuffer[bar]
            if previous < penult:
                BoxHighBuffer[bar] = previous
                BoxOpenBuffer[bar] = BoxHighBuffer[bar]
            elif previous > penult:
                BoxHighBuffer[bar] = current + boxSize
                BoxOpenBuffer[bar] = BoxHighBuffer[bar]
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, price[rates_total - 1])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Renko(_MQL5Indicator):
    name = 'renko'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpBoxSize': 100,  # Box size (in pips)
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

