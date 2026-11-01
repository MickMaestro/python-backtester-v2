"""vinini_cyber_cycle — converted from MQL5: MQL5 Indicators/VininI Cyber Cyсle [v01]/vinini_cyber_cycle.mq5

VininI Cyber Cycle
Copyright: 2011, traderak20@gmail.com; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2011, traderak20@gmail.com', 'version': '1.0', 'window': 'separate', 'indicator_minimum': -1.05, 'indicator_maximum': 1.05, 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 12, 2: 8}, 'colors': {1: [65535, 32768, 255], 2: [65535, 32768, 255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'VininI Cyber Cycle Arrow', 2: 'VininI Cyber Cycle'}, 'levels': [], 'description': ['VininI Cyber Cycle'], 'name': 'vinini_cyber_cycle', 'source': 'MQL5 Indicators/VininI Cyber Cyсle [v01]/vinini_cyber_cycle.mq5', 'folder': 'VininI Cyber Cyсle [v01]', 'inputs': [{'mql': 'InpAlpha', 'py': 'InpAlpha', 'param': 'InpAlpha', 'type': 'double', 'default': 0.01, 'label': 'Alpha', 'sinput': False}, {'mql': 'InpBeta', 'py': 'InpBeta', 'param': 'InpBeta', 'type': 'double', 'default': 1.0, 'label': 'Beta', 'sinput': False}, {'mql': 'InpNormalizeTarget', 'py': 'InpNormalizeTarget', 'param': 'InpNormalizeTarget', 'type': 'double', 'default': 7.5, 'label': 'Normalize target', 'sinput': False}, {'mql': 'InpBarsInWindow', 'py': 'InpBarsInWindow', 'param': 'InpBarsInWindow', 'type': 'int', 'default': 1000, 'label': 'Length of window for calculations', 'sinput': False}, {'mql': 'InpUseMultiColor', 'py': 'InpUseMultiColor', 'param': 'InpUseMultiColor', 'type': 'int', 'default': 0, 'label': 'Use multi-color or single-color line', 'sinput': False}, {'mql': 'InpDrawArrows', 'py': 'InpDrawArrows', 'param': 'InpDrawArrows', 'type': 'bool', 'default': True, 'label': 'Draw arrows on color change', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 5, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum colorswitch
MultiColor = 0
SingleColor = 1
_enum('colorswitch', {0: 'MultiColor', 1: 'SingleColor'})

# ---- inputs and global variables
InpAlpha = _input('InpAlpha', 0.01)  # Alpha
InpBeta = _input('InpBeta', 1.0)  # Beta
InpNormalizeTarget = _input('InpNormalizeTarget', 7.5)  # Normalize target
InpBarsInWindow = _input('InpBarsInWindow', 1000)  # Length of window for calculations
InpUseMultiColor = _input('InpUseMultiColor', MultiColor)  # Use multi-color or single-color line
InpDrawArrows = _input('InpDrawArrows', True)  # Draw arrows on color change
InpAppliedPrice = _input('InpAppliedPrice', PRICE_MEDIAN)  # Applied price
ExtICycleArrowBuffer = Arr(0, 0.0)
ExtICycleArrowColorBuffer = Arr(0, 0.0)
ExtICycleBuffer = Arr(0, 0.0)
ExtICycleColorBuffer = Arr(0, 0.0)
ExtSmoothBuffer = Arr(0, 0.0)
ExtCycleBuffer = Arr(0, 0.0)
CalcPriceArray = Arr(0, 0.0)  # array to hold applied price data

def CreatePriceArray(f_to_copy):
    f_rates = Arr(0, 0, factory=MqlRates)
    ArraySetAsSeries(f_rates, True)
    if CopyRates(None, 0, 0, f_to_copy, f_rates) <= 0:
        return 0
    ArraySetAsSeries(CalcPriceArray, True)
    ArrayInitialize(CalcPriceArray, EMPTY_VALUE)
    ArrayResize(CalcPriceArray, f_to_copy)
    if InpAppliedPrice == PRICE_CLOSE:
        for i in range(0, f_to_copy):
            CalcPriceArray[i] = f_rates[i].close
    elif InpAppliedPrice == PRICE_OPEN:
        for i in range(0, f_to_copy):
            CalcPriceArray[i] = f_rates[i].open
    elif InpAppliedPrice == PRICE_HIGH:
        for i in range(0, f_to_copy):
            CalcPriceArray[i] = f_rates[i].high
    elif InpAppliedPrice == PRICE_LOW:
        for i in range(0, f_to_copy):
            CalcPriceArray[i] = f_rates[i].low
    elif InpAppliedPrice == PRICE_MEDIAN:
        for i in range(0, f_to_copy):
            CalcPriceArray[i] = (f_rates[i].high + f_rates[i].low) / 2
    elif InpAppliedPrice == PRICE_TYPICAL:
        for i in range(0, f_to_copy):
            CalcPriceArray[i] = (f_rates[i].high + f_rates[i].low + f_rates[i].close) / 3
    elif InpAppliedPrice == PRICE_WEIGHTED:
        for i in range(0, f_to_copy):
            CalcPriceArray[i] = (f_rates[i].high + f_rates[i].low + f_rates[i].close + f_rates[i].close) / 4
    return 1

def OnInit():
    SetIndexBuffer(0, ExtICycleArrowBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtICycleArrowColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ExtICycleBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtICycleColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, ExtSmoothBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, ExtCycleBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpBarsInWindow)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, InpBarsInWindow)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, InpBarsInWindow)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, InpBarsInWindow)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    IndicatorSetInteger(INDICATOR_DIGITS, 4)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, -0.5)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, 0.5)
    IndicatorSetString(INDICATOR_SHORTNAME, 'VininI_Cyber_Cycle_Norm_Gom')
    ArraySetAsSeries(ExtICycleArrowBuffer, True)
    ArraySetAsSeries(ExtICycleArrowColorBuffer, True)
    ArraySetAsSeries(ExtICycleBuffer, True)
    ArraySetAsSeries(ExtICycleColorBuffer, True)
    ArraySetAsSeries(ExtSmoothBuffer, True)
    ArraySetAsSeries(ExtCycleBuffer, True)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    window_size = 0
    if InpBarsInWindow <= 0:
        window_size = 1000
    else:
        window_size = InpBarsInWindow
    if rates_total < window_size:
        return 0
    limit = 0
    if (prev_calculated == 0 or prev_calculated < 0) or prev_calculated > rates_total:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    if limit > (rates_total - 1 - 3):
        limit = rates_total - 1 - 3
    to_copy = 0
    if prev_calculated < 0 or prev_calculated > rates_total:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
        to_copy += 3
        if to_copy > rates_total:
            to_copy = rates_total
    if CreatePriceArray(to_copy) <= 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        ExtSmoothBuffer[i] = (CalcPriceArray[i] + (2.0 * CalcPriceArray[i + 1]) + (2.0 * CalcPriceArray[i + 2]) + CalcPriceArray[i + 3]) / 6.0
    for i in range(limit, 0 - 1, -1):
        ExtCycleBuffer[i] = InpBeta * (((1.0 - (0.5 * InpAlpha)) * (1.0 - (0.5 * InpAlpha)) * (ExtSmoothBuffer[i] - (2.0 * ExtSmoothBuffer[i + 1]) + ExtSmoothBuffer[i + 2])) + (2.0 * (1.0 - InpAlpha) * ExtCycleBuffer[i + 1]) - ((1.0 - InpAlpha) * (1.0 - InpAlpha) * ExtCycleBuffer[i + 2]))
    iMax = ArrayMaximum(ExtCycleBuffer, 0, window_size)
    Max = ExtCycleBuffer[iMax]
    iMin = ArrayMinimum(ExtCycleBuffer, 0, window_size)
    Min = ExtCycleBuffer[iMin]
    Gomot = 0.0
    if MathAbs(Max) > MathAbs(Min):
        Gomot = MathAbs(Max)
    else:
        Gomot = MathAbs(Min)
    KGomot = _fdiv(InpNormalizeTarget, Gomot)
    for i in range(limit, 0 - 1, -1):
        NCycle = KGomot * ExtCycleBuffer[i]
        ExtICycleBuffer[i] = _fdiv(MathExp(2.0 * NCycle) - 1.0, MathExp(2.0 * NCycle) + 1.0)
        ExtICycleArrowBuffer[i] = EMPTY_VALUE
    if InpDrawArrows == True:
        for i in range(limit, 0 - 1, -1):
            if ExtICycleBuffer[i] >= 0.5 and ExtICycleBuffer[i + 1] < 0.5:
                ExtICycleArrowBuffer[i] = ExtICycleBuffer[i]
            if ExtICycleBuffer[i] <= -0.5 and ExtICycleBuffer[i + 1] > -0.5:
                ExtICycleArrowBuffer[i] = ExtICycleBuffer[i]
            if (ExtICycleBuffer[i] < 0.5 and ExtICycleBuffer[i + 1] >= 0.5) or (ExtICycleBuffer[i] > -0.5 and ExtICycleBuffer[i + 1] <= -0.5):
                ExtICycleArrowBuffer[i] = ExtICycleBuffer[i]
    if InpUseMultiColor == MultiColor:
        for i in range(limit, 0 - 1, -1):
            if ExtICycleBuffer[i] >= 0.5:
                ExtICycleColorBuffer[i] = 1.0
            if ExtICycleBuffer[i] <= -0.5:
                ExtICycleColorBuffer[i] = 2.0
            if ExtICycleBuffer[i] < 0.5 and ExtICycleBuffer[i] > -0.5:
                ExtICycleColorBuffer[i] = 0.0
            ExtICycleArrowColorBuffer[i] = ExtICycleColorBuffer[i]
    if InpUseMultiColor == SingleColor:
        for i in range(limit, 0 - 1, -1):
            ExtICycleColorBuffer[i] = 0.0
            ExtICycleArrowColorBuffer[i] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VininiCyberCycle(_MQL5Indicator):
    name = 'vinini_cyber_cycle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpAlpha': 0.01,  # Alpha
        'InpBeta': 1.0,  # Beta
        'InpNormalizeTarget': 7.5,  # Normalize target
        'InpBarsInWindow': 1000,  # Length of window for calculations
        'InpUseMultiColor': _Choice({0: 'MultiColor', 1: 'SingleColor'}, default=0),  # Use multi-color or single-color line
        'InpDrawArrows': True,  # Draw arrows on color change
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Applied price
    }
    y_range = (-1.05, 1.05)

