"""StdDev_sep_win — converted from MQL5: MQL5 Indicators/Brooky Trend Strength for MT5/StdDev_sep_win.mq5

Copyright: © 2023, Ryan Lawrence Johnson; Link: https://www.mql5.com/en/users/rjo/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '© 2023, Ryan Lawrence Johnson', 'link': 'https://www.mql5.com/en/users/rjo/seller', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [7451452]}, 'widths': {}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': [], 'name': 'StdDev_sep_win', 'source': 'MQL5 Indicators/Brooky Trend Strength for MT5/StdDev_sep_win.mq5', 'folder': 'Brooky Trend Strength for MT5', 'inputs': [{'mql': 'InpStdDevPeriod', 'py': 'InpStdDevPeriod', 'param': 'InpStdDevPeriod', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpStdDevShift', 'py': 'InpStdDevShift', 'param': 'InpStdDevShift', 'type': 'int', 'default': 0, 'label': 'Shift', 'sinput': False}, {'mql': 'InpMAMethod', 'py': 'InpMAMethod', 'param': 'InpMAMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpStdDevPeriod = _input('InpStdDevPeriod', 20)  # Period
InpStdDevShift = _input('InpStdDevShift', 0)  # Shift
InpMAMethod = _input('InpMAMethod', MODE_SMA)  # Method
ExtStdDevBuffer = Arr(0, 0.0)
ExtMABuffer = Arr(0, 0.0)
ExtStdDevPeriod = 0
ExtStdDevShift = 0

def OnInit():
    global ExtStdDevPeriod, ExtStdDevShift
    if InpStdDevPeriod <= 1:
        ExtStdDevPeriod = 20
        PrintFormat('Incorrect value for input variable InpStdDevPeriod=%d. Indicator will use value %d for calculations.', InpStdDevPeriod, ExtStdDevPeriod)
    else:
        ExtStdDevPeriod = InpStdDevPeriod
    if InpStdDevShift < 0:
        ExtStdDevShift = 0
        PrintFormat('Incorrect value for input variable InpStdDevShift=%d. Indicator will use value %d for calculations.', InpStdDevShift, ExtStdDevShift)
    else:
        ExtStdDevShift = InpStdDevShift
    SetIndexBuffer(0, ExtStdDevBuffer)
    SetIndexBuffer(1, ExtMABuffer, INDICATOR_CALCULATIONS)
    short_name = StringFormat('StdDev(%d)', ExtStdDevPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    PlotIndexSetString(0, PLOT_LABEL, short_name)
    PlotIndexSetInteger(0, PLOT_SHIFT, ExtStdDevShift)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < ExtStdDevPeriod:
        return 0
    start = prev_calculated - 1
    if start < ExtStdDevPeriod:
        start = ExtStdDevPeriod - 1
        ArrayInitialize(ExtStdDevBuffer, 0.0)
        ArrayInitialize(ExtMABuffer, 0.0)
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtStdDevPeriod - 1 + begin)
    _sw1 = InpMAMethod
    if _sw1 == MODE_EMA:
        for i in range(start, rates_total):
            if i == (InpStdDevPeriod - 1):
                ExtMABuffer[i] = SimpleMA(i, InpStdDevPeriod, price)
            else:
                ExtMABuffer[i] = ExponentialMA(i, InpStdDevPeriod, ExtMABuffer[i - 1], price)
            ExtStdDevBuffer[i] = StdDevFunc(price, ExtMABuffer, i)
    elif _sw1 == MODE_SMMA:
        for i in range(start, rates_total):
            if i == (InpStdDevPeriod - 1):
                ExtMABuffer[i] = SimpleMA(i, InpStdDevPeriod, price)
            else:
                ExtMABuffer[i] = SmoothedMA(i, InpStdDevPeriod, ExtMABuffer[i - 1], price)
            ExtStdDevBuffer[i] = StdDevFunc(price, ExtMABuffer, i)
    elif _sw1 == MODE_LWMA:
        for i in range(start, rates_total):
            ExtMABuffer[i] = LinearWeightedMA(i, InpStdDevPeriod, price)
            ExtStdDevBuffer[i] = StdDevFunc(price, ExtMABuffer, i)
    else:
        for i in range(start, rates_total):
            ExtMABuffer[i] = SimpleMA(i, InpStdDevPeriod, price)
            ExtStdDevBuffer[i] = StdDevFunc(price, ExtMABuffer, i)
    return rates_total

def StdDevFunc(price, ma_price, position):
    dev = 0.0
    for i in range(0, ExtStdDevPeriod):
        dev += MathPow(price[position - i] - ma_price[position], 2.0)
    dev = MathSqrt(_fdiv(dev, ExtStdDevPeriod))
    return dev


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StdDevSepWin(_MQL5Indicator):
    name = 'StdDev_sep_win'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpStdDevPeriod': 20,  # Period
        'InpStdDevShift': 0,  # Shift
        'InpMAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

