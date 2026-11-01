"""bb — converted from MQL5: MQL5 Indicators/Bollinger Bands ®/bb.mq5

Bollinger Bands
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [11186720], 2: [11186720], 3: [11186720]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Bands middle', 2: 'Bands upper', 3: 'Bands lower'}, 'levels': [], 'description': ['Bollinger Bands'], 'name': 'bb', 'source': 'MQL5 Indicators/Bollinger Bands ®/bb.mq5', 'folder': 'Bollinger Bands ®', 'inputs': [{'mql': 'InpBandsPeriod', 'py': 'InpBandsPeriod', 'param': 'InpBandsPeriod', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpBandsShift', 'py': 'InpBandsShift', 'param': 'InpBandsShift', 'type': 'int', 'default': 0, 'label': 'Shift', 'sinput': False}, {'mql': 'InpBandsDeviations', 'py': 'InpBandsDeviations', 'param': 'InpBandsDeviations', 'type': 'double', 'default': 2.0, 'label': 'Deviation', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpBandsPeriod = _input('InpBandsPeriod', 20)  # Period
InpBandsShift = _input('InpBandsShift', 0)  # Shift
InpBandsDeviations = _input('InpBandsDeviations', 2.0)  # Deviation
ExtBandsPeriod = 0
ExtBandsShift = 0
ExtBandsDeviations = 0.0
ExtPlotBegin = 0
ExtMLBuffer = Arr(0, 0.0)
ExtTLBuffer = Arr(0, 0.0)
ExtBLBuffer = Arr(0, 0.0)
ExtStdDevBuffer = Arr(0, 0.0)

def OnInit():
    global ExtBandsDeviations, ExtBandsPeriod, ExtBandsShift, ExtPlotBegin
    if InpBandsPeriod < 2:
        ExtBandsPeriod = 20
        printf('Incorrect value for input variable InpBandsPeriod=%d. Indicator will use value=%d for calculations.', InpBandsPeriod, ExtBandsPeriod)
    else:
        ExtBandsPeriod = InpBandsPeriod
    if InpBandsShift < 0:
        ExtBandsShift = 0
        printf('Incorrect value for input variable InpBandsShift=%d. Indicator will use value=%d for calculations.', InpBandsShift, ExtBandsShift)
    else:
        ExtBandsShift = InpBandsShift
    if InpBandsDeviations == 0.0:
        ExtBandsDeviations = 2.0
        printf('Incorrect value for input variable InpBandsDeviations=%f. Indicator will use value=%f for calculations.', InpBandsDeviations, ExtBandsDeviations)
    else:
        ExtBandsDeviations = InpBandsDeviations
    SetIndexBuffer(0, ExtMLBuffer)
    SetIndexBuffer(1, ExtTLBuffer)
    SetIndexBuffer(2, ExtBLBuffer)
    SetIndexBuffer(3, ExtStdDevBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetString(0, PLOT_LABEL, 'Bands(' + _str(ExtBandsPeriod) + ') Middle')
    PlotIndexSetString(1, PLOT_LABEL, 'Bands(' + _str(ExtBandsPeriod) + ') Upper')
    PlotIndexSetString(2, PLOT_LABEL, 'Bands(' + _str(ExtBandsPeriod) + ') Lower')
    IndicatorSetString(INDICATOR_SHORTNAME, 'Bollinger Bands')
    ExtPlotBegin = ExtBandsPeriod - 1
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtBandsPeriod)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, ExtBandsPeriod)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, ExtBandsPeriod)
    PlotIndexSetInteger(0, PLOT_SHIFT, ExtBandsShift)
    PlotIndexSetInteger(1, PLOT_SHIFT, ExtBandsShift)
    PlotIndexSetInteger(2, PLOT_SHIFT, ExtBandsShift)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, begin, price):
    global ExtPlotBegin
    pos = 0
    if ExtPlotBegin != (ExtBandsPeriod + begin):
        ExtPlotBegin = ExtBandsPeriod + begin
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtPlotBegin)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, ExtPlotBegin)
        PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, ExtPlotBegin)
    if rates_total < ExtPlotBegin:
        return 0
    if prev_calculated > 1:
        pos = prev_calculated - 1
    else:
        pos = 0
    for i in range(pos, rates_total):
        ExtMLBuffer[i] = SimpleMA(i, ExtBandsPeriod, price)
        ExtStdDevBuffer[i] = StdDev_Func(i, price, ExtMLBuffer, ExtBandsPeriod)
        ExtTLBuffer[i] = ExtMLBuffer[i] + (ExtBandsDeviations * ExtStdDevBuffer[i])
        ExtBLBuffer[i] = ExtMLBuffer[i] - (ExtBandsDeviations * ExtStdDevBuffer[i])
    return rates_total

def StdDev_Func(position, price, MAprice, period):
    StdDev_dTmp = 0.0
    if position < period:
        return StdDev_dTmp
    for i in range(0, period):
        StdDev_dTmp += MathPow(price[position - i] - MAprice[position], 2)
    StdDev_dTmp = MathSqrt(_fdiv(StdDev_dTmp, period))
    return StdDev_dTmp


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Bb(_MQL5Indicator):
    name = 'bb'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpBandsPeriod': 20,  # Period
        'InpBandsShift': 0,  # Shift
        'InpBandsDeviations': 2.0,  # Deviation
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

