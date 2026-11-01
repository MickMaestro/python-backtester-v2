"""disparityindex — converted from MQL5: MQL5 Indicators/Disparity Index/disparityindex.mq5

Disparity Index shows the difference between the closing price and the selected moving 
average in percentages. Recommended for use in combination with candlestick 
models.
Copyright: Copyright 2012, Rone.; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2012, Rone.', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 3}, 'types': {1: 10, 2: 1, 3: 1}, 'colors': {1: [255, 16711680, 4678655, 16748574], 2: [6908265], 3: [6908265]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Disparity Index', 2: 'Upper Level', 3: 'Lower Level'}, 'levels': [], 'description': ['Disparity Index shows the difference between the closing price and the selected moving ', 'average in percentages. Recommended for use in combination with candlestick ', 'models.'], 'name': 'disparityindex', 'source': 'MQL5 Indicators/Disparity Index/disparityindex.mq5', 'folder': 'Disparity Index', 'inputs': [{'mql': 'InpMaMethod', 'py': 'InpMaMethod', 'param': 'InpMaMethod', 'type': 'int', 'default': 2, 'label': 'МА method', 'sinput': False}, {'mql': 'InpMaPeriod', 'py': 'InpMaPeriod', 'param': 'InpMaPeriod', 'type': 'int', 'default': 10, 'label': 'МА period', 'sinput': False}, {'mql': 'InpLevelsCoeff', 'py': 'InpLevelsCoeff', 'param': 'InpLevelsCoeff', 'type': 'double', 'default': 3.0, 'label': 'levels coefficients', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum MA_METHOD
MODE_EMA_ = 0
MODE_LWMA_ = 1
MODE_SMA_ = 2
MODE_SMMA_ = 3
_enum('MA_METHOD', {0: 'MODE_EMA_', 1: 'MODE_LWMA_', 2: 'MODE_SMA_', 3: 'MODE_SMMA_'})

# ---- inputs and global variables
InpMaMethod = _input('InpMaMethod', MODE_SMA_)  # МА method
InpMaPeriod = _input('InpMaPeriod', 10)  # МА period
InpLevelsCoeff = _input('InpLevelsCoeff', 3.0)  # levels coefficients
DiBuffer = Arr(0, 0.0)
DiColors = Arr(0, 0.0)
UpperBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
AbsRocBuffer = Arr(0, 0.0)
AbsRocMaBuffer = Arr(0, 0.0)
MaBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, DiBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DiColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, UpperBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, LowerBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, AbsRocBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, AbsRocMaBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, MaBuffer, INDICATOR_CALCULATIONS)
    for i in range(0, 3):
        PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, InpMaPeriod - 1)
    IndicatorSetInteger(INDICATOR_DIGITS, 4)
    shortname = 'Disparity Index (' + _str(InpMaPeriod) + ', ' + DoubleToString(InpLevelsCoeff, 2) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    return 0

def OnCalculate(rates_total, prev_calculated, begin, price):
    global _s_OnCalculate_maWeightSum, _s_OnCalculate_rocWeightSum
    startBar = 0
    minRequiredBars = begin + InpMaPeriod - 1
    if begin > 0:
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, minRequiredBars)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, minRequiredBars)
        PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, minRequiredBars)
    if prev_calculated < minRequiredBars:
        ArrayInitialize(DiBuffer, 0.0)
        ArrayInitialize(DiColors, 0.0)
        ArrayInitialize(UpperBuffer, 0.0)
        ArrayInitialize(LowerBuffer, 0.0)
        ArrayInitialize(AbsRocBuffer, 0.0)
        startBar = minRequiredBars
        _s_OnCalculate_rocWeightSum = 0
        _s_OnCalculate_maWeightSum = _s_OnCalculate_rocWeightSum
    else:
        startBar = prev_calculated - 1
    for bar in range(startBar, rates_total):
        AbsRocBuffer[bar] = _fdiv(MathAbs(price[bar] - price[bar - 1]), price[bar]) * 100
    _sw1 = InpMaMethod
    if _sw1 == MODE_EMA_:
        ExponentialMAOnBuffer(rates_total, prev_calculated, begin, InpMaPeriod, price, MaBuffer)
        ExponentialMAOnBuffer(rates_total, prev_calculated, begin, InpMaPeriod, AbsRocBuffer, AbsRocMaBuffer)
    elif _sw1 == MODE_LWMA_:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, begin, InpMaPeriod, price, MaBuffer, _GlobRef(globals(), '_s_OnCalculate_maWeightSum'))
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, begin, InpMaPeriod, AbsRocBuffer, AbsRocMaBuffer, _GlobRef(globals(), '_s_OnCalculate_rocWeightSum'))
    elif _sw1 == MODE_SMMA_:
        SmoothedMAOnBuffer(rates_total, prev_calculated, begin, InpMaPeriod, price, MaBuffer)
        SmoothedMAOnBuffer(rates_total, prev_calculated, begin, InpMaPeriod, AbsRocBuffer, AbsRocMaBuffer)
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, begin, InpMaPeriod, price, MaBuffer)
        SimpleMAOnBuffer(rates_total, prev_calculated, begin, InpMaPeriod, AbsRocBuffer, AbsRocMaBuffer)
    for bar in range(startBar, rates_total):
        if MaBuffer[bar] != 0.0:
            DiBuffer[bar] = _fdiv(100 * (price[bar] - MaBuffer[bar]), MaBuffer[bar])
            UpperBuffer[bar] = AbsRocMaBuffer[bar] * InpLevelsCoeff
            LowerBuffer[bar] = (-AbsRocMaBuffer[bar]) * InpLevelsCoeff
        if DiBuffer[bar] >= 0.0:
            if DiBuffer[bar] > UpperBuffer[bar]:
                DiColors[bar] = 1.0
            else:
                DiColors[bar] = 3.0
        else:
            if DiBuffer[bar] < LowerBuffer[bar]:
                DiColors[bar] = 0.0
            else:
                DiColors[bar] = 2.0
    return rates_total

# ---- static local variables
_s_OnCalculate_maWeightSum = 0
_s_OnCalculate_rocWeightSum = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Disparityindex(_MQL5Indicator):
    name = 'disparityindex'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMaMethod': _Choice({0: 'Exponential', 1: 'Linear Weighted', 2: 'Simple', 3: 'Smoothed'}, default=2),  # МА method
        'InpMaPeriod': 10,  # МА period
        'InpLevelsCoeff': 3.0,  # levels coefficients
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

