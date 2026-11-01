"""sdrsi — converted from MQL5: MQL5 Indicators/Relative Strength Index of Volatility/sdrsi.mq5

Relative Strength Index of Volatility
Copyright: 2010, KTS Group; Link: http://www.koss.su; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2010, KTS Group', 'link': 'http://www.koss.su', 'version': '1.00', 'window': 'separate', 'indicator_minimum': 0.0, 'indicator_maximum': 100.0, 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0], 'description': ['Relative Strength Index of Volatility'], 'name': 'sdrsi', 'source': 'MQL5 Indicators/Relative Strength Index of Volatility/sdrsi.mq5', 'folder': 'Relative Strength Index of Volatility', 'inputs': [{'mql': 'FastPeriodRSI', 'py': 'FastPeriodRSI', 'param': 'FastPeriodRSI', 'type': 'int', 'default': 24, 'label': 'Fast period', 'sinput': False}, {'mql': 'SlowPeriodRSI', 'py': 'SlowPeriodRSI', 'param': 'SlowPeriodRSI', 'type': 'int', 'default': 120, 'label': 'Slow period', 'sinput': False}, {'mql': 'InpMAMethod', 'py': 'InpMAMethod', 'param': 'InpMAMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppPrice', 'py': 'InpAppPrice', 'param': 'InpAppPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FastPeriodRSI = _input('FastPeriodRSI', 24)  # Fast period
SlowPeriodRSI = _input('SlowPeriodRSI', 120)  # Slow period
InpMAMethod = _input('InpMAMethod', MODE_SMA)  # Method
InpAppPrice = _input('InpAppPrice', PRICE_CLOSE)
FastRSIBuffer = Arr(0, 0.0)
SlowRSIBuffer = Arr(0, 0.0)
ExtFastRSI = 0
ExtSlowRSI = 0
hFastStdDev = 0
hFastRSI = 0
hSlowStdDev = 0
hSlowRSI = 0

def OnInit():
    global ExtFastRSI, ExtSlowRSI
    if FastPeriodRSI <= 1:
        ExtFastRSI = 24
    else:
        ExtFastRSI = FastPeriodRSI
    if SlowPeriodRSI <= 1:
        ExtSlowRSI = 120
    else:
        ExtSlowRSI = SlowPeriodRSI
    SetIndexBuffer(0, FastRSIBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtFastRSI)
    SetIndexBuffer(1, SlowRSIBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, ExtSlowRSI)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SDRSI(' + _str(ExtFastRSI) + '/' + _str(ExtSlowRSI) + ')')
    SetHandles()

def OnCalculate(rates_total, prev_calculated, begin, price):
    ToCopy = 0
    if rates_total < prev_calculated or prev_calculated == 0:
        ToCopy = rates_total
        if CopyBuffer(hFastRSI, 0, 0, ToCopy, FastRSIBuffer) <= 0:
            return 0
        if CopyBuffer(hSlowRSI, 0, 0, ToCopy, SlowRSIBuffer) <= 0:
            return 0
    else:
        if rates_total > prev_calculated:
            ToCopy = rates_total - prev_calculated + 1
            if CopyBuffer(hFastRSI, 0, 0, ToCopy, FastRSIBuffer) <= 0:
                return 0
            if CopyBuffer(hSlowRSI, 0, 0, ToCopy, SlowRSIBuffer) <= 0:
                return 0
    return rates_total

def SetHandles():
    global hFastRSI, hFastStdDev, hSlowRSI, hSlowStdDev
    hSlowStdDev = iStdDev(None, 0, ExtSlowRSI, 0, InpMAMethod, InpAppPrice)
    hFastStdDev = iStdDev(None, 0, ExtFastRSI, 0, InpMAMethod, InpAppPrice)
    hFastRSI = iRSI(None, 0, ExtFastRSI, hFastStdDev)
    hSlowRSI = iRSI(None, 0, ExtSlowRSI, hSlowStdDev)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Sdrsi(_MQL5Indicator):
    name = 'sdrsi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastPeriodRSI': 24,  # Fast period
        'SlowPeriodRSI': 120,  # Slow period
        'InpMAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpAppPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }
    y_range = (0.0, 100.0)

