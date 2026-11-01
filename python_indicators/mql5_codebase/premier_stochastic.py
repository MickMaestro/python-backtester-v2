"""premier_stochastic — converted from MQL5: MQL5 Indicators/Premier Stochastic Oscillator [v01]/premier_stochastic.mq5

Premier Stochastic Oscillator
Copyright: 2011, traderak20@gmail.com; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2011, traderak20@gmail.com', 'version': '1.0', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 3, 'indicator_maximum': 1.0, 'indicator_minimum': -1.0}, 'types': {1: 8, 2: 12, 3: 10}, 'colors': {1: [65280, 32768, 128, 255, 6908265], 2: [65280, 32768, 128, 255, 16776960], 3: [65280, 32768, 128, 255, 16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {}, 'labels': {1: 'Premier Stochastic Osc', 2: 'PSO signal', 3: 'PSO histogram'}, 'levels': [], 'description': ['Premier Stochastic Oscillator'], 'name': 'premier_stochastic', 'source': 'MQL5 Indicators/Premier Stochastic Oscillator [v01]/premier_stochastic.mq5', 'folder': 'Premier Stochastic Oscillator [v01]', 'inputs': [{'mql': 'InpKPeriod', 'py': 'InpKPeriod', 'param': 'InpKPeriod', 'type': 'int', 'default': 8, 'label': 'K period', 'sinput': False}, {'mql': 'InpDPeriod', 'py': 'InpDPeriod', 'param': 'InpDPeriod', 'type': 'int', 'default': 1, 'label': 'D period', 'sinput': False}, {'mql': 'InpSlowing', 'py': 'InpSlowing', 'param': 'InpSlowing', 'type': 'int', 'default': 1, 'label': 'Slowing', 'sinput': False}, {'mql': 'InpAppliedMA', 'py': 'InpAppliedMA', 'param': 'InpAppliedMA', 'type': 'int', 'default': 0, 'label': 'Applied MA method for stochastic', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 0, 'label': 'Applied price for stochastic', 'sinput': False}, {'mql': 'InpEMAPeriod', 'py': 'InpEMAPeriod', 'param': 'InpEMAPeriod', 'type': 'int', 'default': 5, 'label': 'EMA Period', 'sinput': False}, {'mql': 'InpOuterTreshold', 'py': 'InpOuterTreshold', 'param': 'InpOuterTreshold', 'type': 'double', 'default': 0.9, 'label': 'Outer threshold', 'sinput': False}, {'mql': 'InpInnerTreshold', 'py': 'InpInnerTreshold', 'param': 'InpInnerTreshold', 'type': 'double', 'default': 0.2, 'label': 'Inner threshold', 'sinput': False}, {'mql': 'InpUseMultiColorLine', 'py': 'InpUseMultiColorLine', 'param': 'InpUseMultiColorLine', 'type': 'int', 'default': 0, 'label': 'Use multi-color or single-color line', 'sinput': False}, {'mql': 'InpShowArrows', 'py': 'InpShowArrows', 'param': 'InpShowArrows', 'type': 'bool', 'default': False, 'label': 'Show/hide arrows', 'sinput': False}, {'mql': 'InpArrowCode', 'py': 'InpArrowCode', 'param': 'InpArrowCode', 'type': 'uchar', 'default': 159, 'label': 'Arrow code', 'sinput': False}, {'mql': 'InpUseMultiColorArrows', 'py': 'InpUseMultiColorArrows', 'param': 'InpUseMultiColorArrows', 'type': 'int', 'default': 0, 'label': 'Use multi-color or single-color arrows', 'sinput': False}, {'mql': 'InpShowHistrogram', 'py': 'InpShowHistrogram', 'param': 'InpShowHistrogram', 'type': 'bool', 'default': True, 'label': 'Show/hide histogram', 'sinput': False}, {'mql': 'InpUseMultiColorHistogram', 'py': 'InpUseMultiColorHistogram', 'param': 'InpUseMultiColorHistogram', 'type': 'int', 'default': 0, 'label': 'Use multi-color or single-color histogram', 'sinput': False}, {'mql': 'InpShowLevels', 'py': 'InpShowLevels', 'param': 'InpShowLevels', 'type': 'bool', 'default': True, 'label': 'Show/hide level lines', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum colorswitch
MultiColor = 0
SingleColor = 1
_enum('colorswitch', {0: 'MultiColor', 1: 'SingleColor'})

# ---- inputs and global variables
InpKPeriod = _input('InpKPeriod', 8)  # K period
InpDPeriod = _input('InpDPeriod', 1)  # D period
InpSlowing = _input('InpSlowing', 1)  # Slowing
InpAppliedMA = _input('InpAppliedMA', MODE_SMA)  # Applied MA method for stochastic
InpAppliedPrice = _input('InpAppliedPrice', STO_LOWHIGH)  # Applied price for stochastic
InpEMAPeriod = _input('InpEMAPeriod', 5)  # EMA Period
InpOuterTreshold = _input('InpOuterTreshold', 0.9)  # Outer threshold
InpInnerTreshold = _input('InpInnerTreshold', 0.2)  # Inner threshold
InpUseMultiColorLine = _input('InpUseMultiColorLine', MultiColor)  # Use multi-color or single-color line
InpShowArrows = _input('InpShowArrows', False)  # Show/hide arrows
InpArrowCode = _input('InpArrowCode', 159)  # Arrow code
InpUseMultiColorArrows = _input('InpUseMultiColorArrows', MultiColor)  # Use multi-color or single-color arrows
InpShowHistrogram = _input('InpShowHistrogram', True)  # Show/hide histogram
InpUseMultiColorHistogram = _input('InpUseMultiColorHistogram', MultiColor)  # Use multi-color or single-color histogram
InpShowLevels = _input('InpShowLevels', True)  # Show/hide level lines
ExtMainBuffer = Arr(0, 0.0)
ExtMainColorBuffer = Arr(0, 0.0)
ExtMainArrowBuffer = Arr(0, 0.0)
ExtMainArrowColorBuffer = Arr(0, 0.0)
ExtHistogramBuffer = Arr(0, 0.0)
ExtHistogramColorBuffer = Arr(0, 0.0)
ExtEMA_2Buffer = Arr(0, 0.0)
ExtStochasticHandle = 0  # stochastic handle
ExtEMA_1Handle = 0  # EMA of stochastic
ExtEMA_2Handle = 0  # EMA of EMA on stochastic
ShowErrorMessages = True  # turn on/off error messages for debugging

def OnInit():
    global ExtEMA_1Handle, ExtEMA_2Handle, ExtStochasticHandle
    SetIndexBuffer(0, ExtMainBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtMainColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ExtMainArrowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtMainArrowColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, ExtHistogramBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ExtHistogramColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, ExtEMA_2Buffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(ExtMainBuffer, True)
    ArraySetAsSeries(ExtMainColorBuffer, True)
    ArraySetAsSeries(ExtMainArrowBuffer, True)
    ArraySetAsSeries(ExtMainArrowColorBuffer, True)
    ArraySetAsSeries(ExtHistogramBuffer, True)
    ArraySetAsSeries(ExtHistogramColorBuffer, True)
    ArraySetAsSeries(ExtEMA_2Buffer, True)
    PlotIndexSetInteger(1, PLOT_ARROW, InpArrowCode)
    IndicatorSetInteger(INDICATOR_DIGITS, 4)
    if InpShowLevels:
        IndicatorSetInteger(INDICATOR_LEVELS, 4)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, InpOuterTreshold)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrChocolate)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, InpInnerTreshold)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrChocolate)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, -InpInnerTreshold)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrChocolate)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, -InpOuterTreshold)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, 3, clrChocolate)
    else:
        IndicatorSetInteger(INDICATOR_LEVELS, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'PSO(' + _str(InpKPeriod) + ',' + _str(InpDPeriod) + ',' + _str(InpSlowing) + ',' + _str(InpEMAPeriod) + ')')
    ExtStochasticHandle = iStochastic(None, 0, InpKPeriod, InpDPeriod, InpSlowing, InpAppliedMA, InpAppliedPrice)
    ExtEMA_1Handle = iMA(None, 0, InpEMAPeriod, 0, MODE_EMA, ExtStochasticHandle)
    ExtEMA_2Handle = iMA(None, 0, InpEMAPeriod, 0, MODE_EMA, ExtEMA_1Handle)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    limit = 0
    if (prev_calculated == 0 or prev_calculated < 0) or prev_calculated > rates_total:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    for i in range(limit, 0 - 1, -1):
        if CopyBuffer(ExtEMA_2Handle, 0, i, 1, ExtEMA_2Buffer) <= 0:
            if ShowErrorMessages:
                Print('Getting EMA of EMA on Stochastic failed! Error', GetLastError())
            return 0
        rescale = 0.1 * (ExtEMA_2Buffer[i] - 50)
        exponential = MathExp(rescale)
        ExtMainBuffer[i] = _fdiv(exponential - 1, exponential + 1)
        ExtMainColorBuffer[i] = 4.0
        if InpUseMultiColorLine == MultiColor:
            if ExtMainBuffer[i] >= InpOuterTreshold:
                ExtMainColorBuffer[i] = 0.0
            if ExtMainBuffer[i] >= 0 and ExtMainBuffer[i] < InpOuterTreshold:
                ExtMainColorBuffer[i] = 1.0
            if ExtMainBuffer[i] < 0 and ExtMainBuffer[i] > (-InpOuterTreshold):
                ExtMainColorBuffer[i] = 2.0
            if ExtMainBuffer[i] <= (-InpOuterTreshold):
                ExtMainColorBuffer[i] = 3.0
        if InpShowArrows:
            ExtMainArrowBuffer[i] = EMPTY_VALUE
            if i < limit:
                clrIndex = 4
                ExtMainArrowColorBuffer[i] = clrIndex
                if ExtMainBuffer[i] >= InpOuterTreshold and ExtMainBuffer[i + 1] < InpOuterTreshold:
                    ExtMainArrowBuffer[i] = ExtMainBuffer[i]
                    clrIndex = 0
                if ExtMainBuffer[i] < InpOuterTreshold and ExtMainBuffer[i + 1] >= InpOuterTreshold:
                    ExtMainArrowBuffer[i] = ExtMainBuffer[i]
                    clrIndex = 1
                if ExtMainBuffer[i] > (-InpOuterTreshold) and ExtMainBuffer[i + 1] <= (-InpOuterTreshold):
                    ExtMainArrowBuffer[i] = ExtMainBuffer[i]
                    clrIndex = 2
                if ExtMainBuffer[i] <= (-InpOuterTreshold) and ExtMainBuffer[i + 1] > (-InpOuterTreshold):
                    ExtMainArrowBuffer[i] = ExtMainBuffer[i]
                    clrIndex = 3
                if InpUseMultiColorArrows == MultiColor:
                    ExtMainArrowColorBuffer[i] = clrIndex
        else:
            ExtMainArrowBuffer[i] = EMPTY_VALUE
            ExtMainArrowColorBuffer[i] = EMPTY_VALUE
        if InpShowHistrogram:
            ExtHistogramBuffer[i] = ExtMainBuffer[i]
            ExtHistogramColorBuffer[i] = 4.0
            if InpUseMultiColorHistogram == MultiColor:
                if ExtHistogramBuffer[i] >= InpOuterTreshold:
                    ExtHistogramColorBuffer[i] = 0.0
                if ExtHistogramBuffer[i] >= 0 and ExtHistogramBuffer[i] < InpOuterTreshold:
                    ExtHistogramColorBuffer[i] = 1.0
                if ExtHistogramBuffer[i] < 0 and ExtHistogramBuffer[i] > (-InpOuterTreshold):
                    ExtHistogramColorBuffer[i] = 2.0
                if ExtHistogramBuffer[i] <= (-InpOuterTreshold):
                    ExtHistogramColorBuffer[i] = 3.0
        else:
            ExtHistogramBuffer[i] = EMPTY_VALUE
            ExtHistogramColorBuffer[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PremierStochastic(_MQL5Indicator):
    name = 'premier_stochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpKPeriod': 8,  # K period
        'InpDPeriod': 1,  # D period
        'InpSlowing': 1,  # Slowing
        'InpAppliedMA': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Applied MA method for stochastic
        'InpAppliedPrice': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Applied price for stochastic
        'InpEMAPeriod': 5,  # EMA Period
        'InpOuterTreshold': 0.9,  # Outer threshold
        'InpInnerTreshold': 0.2,  # Inner threshold
        'InpUseMultiColorLine': _Choice({0: 'MultiColor', 1: 'SingleColor'}, default=0),  # Use multi-color or single-color line
        'InpShowArrows': False,  # Show/hide arrows
        'InpArrowCode': 159,  # Arrow code
        'InpUseMultiColorArrows': _Choice({0: 'MultiColor', 1: 'SingleColor'}, default=0),  # Use multi-color or single-color arrows
        'InpShowHistrogram': True,  # Show/hide histogram
        'InpUseMultiColorHistogram': _Choice({0: 'MultiColor', 1: 'SingleColor'}, default=0),  # Use multi-color or single-color histogram
        'InpShowLevels': True,  # Show/hide level lines
    }
    y_range = (-1.0, 1.0)

