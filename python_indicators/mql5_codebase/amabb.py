"""amabb — converted from MQL5: MQL5 Indicators/Adaptive Moving Average with Bollinger Bands ®/amabb.mq5

2009, MetaQuotes Software Corp.
http://www.mql5.com
Adaptive Moving Average + Bollinger Bands
Copyright: Copyright 2010, ARIES Software Corp.; Link: http://ariess.mp; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2010, ARIES Software Corp.', 'link': 'http://ariess.mp', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [255], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'AMA', 2: 'AMA upper', 3: 'AMA lower'}, 'levels': [], 'description': ['2009, MetaQuotes Software Corp.', 'http://www.mql5.com', 'Adaptive Moving Average + Bollinger Bands'], 'name': 'amabb', 'source': 'MQL5 Indicators/Adaptive Moving Average with Bollinger Bands ®/amabb.mq5', 'folder': 'Adaptive Moving Average with Bollinger Bands ®', 'inputs': [{'mql': 'InpPeriodAMA', 'py': 'InpPeriodAMA', 'param': 'InpPeriodAMA', 'type': 'int', 'default': 10, 'label': 'AMA period', 'sinput': False}, {'mql': 'InpSlowPeriodEMA', 'py': 'InpSlowPeriodEMA', 'param': 'InpSlowPeriodEMA', 'type': 'int', 'default': 30, 'label': 'Slow EMA period', 'sinput': False}, {'mql': 'InpFastPeriodEMA', 'py': 'InpFastPeriodEMA', 'param': 'InpFastPeriodEMA', 'type': 'int', 'default': 2, 'label': 'Fast EMA period', 'sinput': False}, {'mql': 'InpShiftAMA', 'py': 'InpShiftAMA', 'param': 'InpShiftAMA', 'type': 'int', 'default': 0, 'label': 'AMA shift', 'sinput': False}, {'mql': 'InpBandsPeriod', 'py': 'InpBandsPeriod', 'param': 'InpBandsPeriod', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpBandsDeviations', 'py': 'InpBandsDeviations', 'param': 'InpBandsDeviations', 'type': 'double', 'default': 2.0, 'label': 'Deviation', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodAMA = _input('InpPeriodAMA', 10)  # AMA period
InpSlowPeriodEMA = _input('InpSlowPeriodEMA', 30)  # Slow EMA period
InpFastPeriodEMA = _input('InpFastPeriodEMA', 2)  # Fast EMA period
InpShiftAMA = _input('InpShiftAMA', 0)  # AMA shift
InpBandsPeriod = _input('InpBandsPeriod', 20)  # Period
InpBandsDeviations = _input('InpBandsDeviations', 2.0)  # Deviation
ExtAMABuffer = Arr(0, 0.0)
ExtUpBuffer = Arr(0, 0.0)
ExtDwBuffer = Arr(0, 0.0)
ExtStdDevBuffer = Arr(0, 0.0)
ExtFastSC = 0.0
ExtSlowSC = 0.0
ExtPeriodAMA = 0
ExtSlowPeriodEMA = 0
ExtFastPeriodEMA = 0
ExtBandsPeriod = 0
ExtBandsDeviations = 0.0

def OnInit():
    global ExtBandsDeviations, ExtBandsPeriod, ExtFastPeriodEMA, ExtFastSC, ExtPeriodAMA, ExtSlowPeriodEMA, ExtSlowSC
    if InpPeriodAMA <= 0:
        ExtPeriodAMA = 10
        printf('Input parameter InpPeriodAMA has incorrect value (%d). Indicator will use value %d for calculations.', InpPeriodAMA, ExtPeriodAMA)
    else:
        ExtPeriodAMA = InpPeriodAMA
    if InpSlowPeriodEMA <= 0:
        ExtSlowPeriodEMA = 30
        printf('Input parameter InpSlowPeriodEMA has incorrect value (%d). Indicator will use value %d for calculations.', InpSlowPeriodEMA, ExtSlowPeriodEMA)
    else:
        ExtSlowPeriodEMA = InpSlowPeriodEMA
    if InpFastPeriodEMA <= 0:
        ExtFastPeriodEMA = 2
        printf('Input parameter InpFastPeriodEMA has incorrect value (%d). Indicator will use value %d for calculations.', InpFastPeriodEMA, ExtFastPeriodEMA)
    else:
        ExtFastPeriodEMA = InpFastPeriodEMA
    if InpBandsPeriod < 2:
        ExtBandsPeriod = 20
        printf('Incorrect value for input variable InpBandsPeriod=%d. Indicator will use value=%d for calculations.', InpBandsPeriod, ExtBandsPeriod)
    else:
        ExtBandsPeriod = InpBandsPeriod
    if InpBandsDeviations == 0.0:
        ExtBandsDeviations = 2.0
        printf('Incorrect value for input variable InpBandsDeviations=%f. Indicator will use value=%f for calculations.', InpBandsDeviations, ExtBandsDeviations)
    else:
        ExtBandsDeviations = InpBandsDeviations
    SetIndexBuffer(0, ExtAMABuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtUpBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtDwBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtStdDevBuffer, INDICATOR_CALCULATIONS)
    short_name = 'AMA(' + IntegerToString(ExtPeriodAMA) + ',' + IntegerToString(ExtFastPeriodEMA) + ',' + IntegerToString(ExtSlowPeriodEMA) + ',' + IntegerToString(ExtBandsPeriod) + ',' + _str(ExtBandsDeviations) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    PlotIndexSetString(0, PLOT_LABEL, short_name)
    PlotIndexSetString(1, PLOT_LABEL, 'Bands(' + _str(ExtBandsPeriod) + ') Upper')
    PlotIndexSetString(2, PLOT_LABEL, 'Bands(' + _str(ExtBandsPeriod) + ') Lower')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtPeriodAMA)
    PlotIndexSetInteger(0, PLOT_SHIFT, InpShiftAMA)
    ExtFastSC = _fdiv(2.0, ExtFastPeriodEMA + 1.0)
    ExtSlowSC = _fdiv(2.0, ExtSlowPeriodEMA + 1.0)
    return 0

def OnCalculate(rates_total, prev_calculated, begin, price):
    i = 0
    if rates_total < (ExtPeriodAMA + begin):
        return 0
    if begin != 0:
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtPeriodAMA + begin)
    pos = prev_calculated - 1
    if pos < (ExtPeriodAMA + begin):
        pos = ExtPeriodAMA + begin
        i = 0
        for i in range(i, pos - 1):
            ExtAMABuffer[i] = 0.0
        else:
            i = _range_end(i, pos - 1, 1)
        ExtAMABuffer[pos - 1] = price[pos - 1]
    i = pos
    for i in range(i, rates_total):
        dCurrentSSC = (CalculateER(i, price) * (ExtFastSC - ExtSlowSC)) + ExtSlowSC
        dPrevAMA = ExtAMABuffer[i - 1]
        ExtAMABuffer[i] = (pow(dCurrentSSC, 2) * (price[i] - dPrevAMA)) + dPrevAMA
        ExtStdDevBuffer[i] = StdDev_Func(i, price, ExtAMABuffer, ExtBandsPeriod)
        ExtUpBuffer[i] = ExtAMABuffer[i] + (ExtBandsDeviations * ExtStdDevBuffer[i])
        ExtDwBuffer[i] = ExtAMABuffer[i] - (ExtBandsDeviations * ExtStdDevBuffer[i])
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total

def CalculateER(nPosition, PriceData):
    dSignal = fabs(PriceData[nPosition] - PriceData[nPosition - ExtPeriodAMA])
    dNoise = 0.0
    for delta in range(0, ExtPeriodAMA):
        dNoise += fabs(PriceData[nPosition - delta] - PriceData[nPosition - delta - 1])
    if dNoise != 0.0:
        return _fdiv(dSignal, dNoise)
    return 0.0

def StdDev_Func(position, price, MAprice, period):
    StdDev_dTmp = 0.0
    if position < (period - 1):
        return StdDev_dTmp
    for i in range(0, period):
        StdDev_dTmp += MathPow(price[position - i] - MAprice[position], 2)
    StdDev_dTmp = MathSqrt(_fdiv(StdDev_dTmp, period))
    return StdDev_dTmp


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Amabb(_MQL5Indicator):
    name = 'amabb'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodAMA': 10,  # AMA period
        'InpSlowPeriodEMA': 30,  # Slow EMA period
        'InpFastPeriodEMA': 2,  # Fast EMA period
        'InpShiftAMA': 0,  # AMA shift
        'InpBandsPeriod': 20,  # Period
        'InpBandsDeviations': 2.0,  # Deviation
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

