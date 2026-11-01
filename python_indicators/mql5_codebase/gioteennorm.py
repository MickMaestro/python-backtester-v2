"""GioteenNorm — converted from MQL5: MQL5 Indicators/Normalized Price Indicator/GioteenNorm.mq5

Gioteen Norm
Copyright: Copyright 2020, Legendary Forex Experts; Link: https://www.mql5.com/en/users/gioteen

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2020, Legendary Forex Experts', 'link': 'https://www.mql5.com/en/users/gioteen', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': ['Gioteen Norm'], 'name': 'GioteenNorm', 'source': 'MQL5 Indicators/Normalized Price Indicator/GioteenNorm.mq5', 'folder': 'Normalized Price Indicator', 'inputs': [{'mql': 'InpStdDevPeriod', 'py': 'InpStdDevPeriod', 'param': 'InpStdDevPeriod', 'type': 'int', 'default': 100, 'label': 'Period', 'sinput': False}, {'mql': 'InpMAMethod', 'py': 'InpMAMethod', 'param': 'InpMAMethod', 'type': 'int', 'default': 1, 'label': 'Method', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpStdDevPeriod = _input('InpStdDevPeriod', 100)  # Period
InpStdDevShift = 0  # Shift
InpMAMethod = _input('InpMAMethod', MODE_EMA)  # Method
ExtStdDevBuffer = Arr(0, 0.0)
ExtMABuffer = Arr(0, 0.0)
ExtStdDevPeriod = 0
ExtStdDevShift = 0

def OnInit():
    global ExtStdDevPeriod, ExtStdDevShift
    if InpStdDevPeriod <= 1:
        ExtStdDevPeriod = 20
        printf('Incorrect value for input variable InpStdDevPeriod=%d. Indicator will use value=%d for calculations.', InpStdDevPeriod, ExtStdDevPeriod)
    else:
        ExtStdDevPeriod = InpStdDevPeriod
    if InpStdDevShift < 0:
        ExtStdDevShift = 0
        printf('Incorrect value for input variable InpStdDevShift=%d. Indicator will use value=%d for calculations.', InpStdDevShift, ExtStdDevShift)
    else:
        ExtStdDevShift = InpStdDevShift
    IndicatorSetString(INDICATOR_SHORTNAME, 'Gioteen-Norm(' + _str(ExtStdDevPeriod) + ')')
    SetIndexBuffer(0, ExtStdDevBuffer)
    SetIndexBuffer(1, ExtMABuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetString(0, PLOT_LABEL, 'Gioteen-Norm(' + _str(ExtStdDevPeriod) + ')')
    PlotIndexSetInteger(0, PLOT_SHIFT, ExtStdDevShift)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, 2)

def OnCalculate(rates_total, prev_calculated, begin, price):
    pos = 0
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtStdDevPeriod - 1 + begin)
    if rates_total < ExtStdDevPeriod:
        return 0
    pos = prev_calculated - 1
    if pos < ExtStdDevPeriod:
        pos = ExtStdDevPeriod - 1
        ArrayInitialize(ExtStdDevBuffer, 0.0)
        ArrayInitialize(ExtMABuffer, 0.0)
    _sw1 = InpMAMethod
    if _sw1 == MODE_EMA:
        for i in range(pos, rates_total):
            if i == (InpStdDevPeriod - 1):
                ExtMABuffer[i] = SimpleMA(i, InpStdDevPeriod, price)
            else:
                ExtMABuffer[i] = ExponentialMA(i, InpStdDevPeriod, ExtMABuffer[i - 1], price)
            ExtStdDevBuffer[i] = StdDevFunc(price, ExtMABuffer, i)
    elif _sw1 == MODE_SMMA:
        for i in range(pos, rates_total):
            if i == (InpStdDevPeriod - 1):
                ExtMABuffer[i] = SimpleMA(i, InpStdDevPeriod, price)
            else:
                ExtMABuffer[i] = SmoothedMA(i, InpStdDevPeriod, ExtMABuffer[i - 1], price)
            ExtStdDevBuffer[i] = StdDevFunc(price, ExtMABuffer, i)
    elif _sw1 == MODE_LWMA:
        for i in range(pos, rates_total):
            ExtMABuffer[i] = LinearWeightedMA(i, InpStdDevPeriod, price)
            ExtStdDevBuffer[i] = StdDevFunc(price, ExtMABuffer, i)
    else:
        for i in range(pos, rates_total):
            ExtMABuffer[i] = SimpleMA(i, InpStdDevPeriod, price)
            ExtStdDevBuffer[i] = StdDevFunc(price, ExtMABuffer, i)
    return rates_total

def StdDevFunc(price, MAprice, position):
    dTmp = 0.0
    for i in range(0, ExtStdDevPeriod):
        dTmp += MathPow(price[position - i] - MAprice[position], 2)
    dTmp = MathSqrt(_fdiv(dTmp, ExtStdDevPeriod))
    return _fdiv(price[position] - MAprice[position], dTmp)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GioteenNorm(_MQL5Indicator):
    name = 'GioteenNorm'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpStdDevPeriod': 100,  # Period
        'InpMAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Method
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

