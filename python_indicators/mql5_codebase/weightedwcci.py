"""weightedwcci — converted from MQL5: MQL5 Indicators/WeightedWCCI/weightedwcci.mq5

The indicator draws the slow and fast ССI and colors bars for determining patterns and trends
Copyright: Copyright © 2005, Luis Guilherme Damiani; Link: http://www.damianifx.com.br; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Luis Guilherme Damiani', 'link': 'http://www.damianifx.com.br', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 10}, 'colors': {1: [65280, 255], 2: [16711935, 15631086, 8421504, 16760576, 16711680]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'WeightedWCCI Signal', 2: 'WeightedWCCI Stochastic'}, 'levels': [], 'description': ['The indicator draws the slow and fast ССI and colors bars for determining patterns and trends'], 'name': 'weightedwcci', 'source': 'MQL5 Indicators/WeightedWCCI/weightedwcci.mq5', 'folder': 'WeightedWCCI', 'inputs': [{'mql': 'FastCCI_Period', 'py': 'FastCCI_Period', 'param': 'FastCCI_Period', 'type': 'uint', 'default': 7, 'label': 'Fast CCI period', 'sinput': False}, {'mql': 'SlowCCI_Period', 'py': 'SlowCCI_Period', 'param': 'SlowCCI_Period', 'type': 'uint', 'default': 13, 'label': 'Slow CCI period', 'sinput': False}, {'mql': 'CCIPrice', 'py': 'CCIPrice', 'param': 'CCIPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}, {'mql': 'weight', 'py': 'weight', 'param': 'weight', 'type': 'double', 'default': 1.0, 'label': 'Weight', 'sinput': False}, {'mql': 'overbslevel', 'py': 'overbslevel', 'param': 'overbslevel', 'type': 'uint', 'default': 200, 'label': 'Extreme level', 'sinput': False}, {'mql': 'triglevel', 'py': 'triglevel', 'param': 'triglevel', 'type': 'uint', 'default': 50, 'label': 'Trigger level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FastCCI_Period = _input('FastCCI_Period', 7)  # Fast CCI period
SlowCCI_Period = _input('SlowCCI_Period', 13)  # Slow CCI period
CCIPrice = _input('CCIPrice', PRICE_MEDIAN)  # Price
weight = _input('weight', 1.0)  # Weight
overbslevel = _input('overbslevel', _uint(200.0))  # Extreme level
triglevel = _input('triglevel', _uint(50.0))  # Trigger level
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
min_rates_total = 0
overbslevel50 = 0
FsCCI_Handle = 0
SlCCI_Handle = 0
FsATR_Handle = 0
SlATR_Handle = 0

def OnInit():
    global FsATR_Handle, FsCCI_Handle, SlATR_Handle, SlCCI_Handle, min_rates_total, overbslevel50
    if weight:
        FsATRPeriod = 7
        SlATRPeriod = 49
        min_rates_total = MathMax(FsATRPeriod, SlATRPeriod)
        FsATR_Handle = iATR(Symbol(), PERIOD_CURRENT, FsATRPeriod)
        if FsATR_Handle == INVALID_HANDLE:
            Print(' Failed to get handle of the ATR indicator')
            return INIT_FAILED
        SlATR_Handle = iATR(Symbol(), PERIOD_CURRENT, SlATRPeriod)
        if SlATR_Handle == INVALID_HANDLE:
            Print(' Failed to get handle of the ATR indicator')
            return INIT_FAILED
    else:
        min_rates_total = 0
    min_rates_total = _int(MathMax(min_rates_total, MathMax(FastCCI_Period, SlowCCI_Period)))
    overbslevel50 = _int(overbslevel + 50)
    FsCCI_Handle = iCCI(Symbol(), PERIOD_CURRENT, FastCCI_Period, CCIPrice)
    if FsCCI_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of the Fast iCCI indicator')
        return INIT_FAILED
    SlCCI_Handle = iCCI(Symbol(), PERIOD_CURRENT, SlowCCI_Period, CCIPrice)
    if SlCCI_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of the Slow iCCI indicator')
        return INIT_FAILED
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(UpBuffer, True)
    ArraySetAsSeries(DnBuffer, True)
    ArraySetAsSeries(IndBuffer, True)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'WeightedWCCI')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 5)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbslevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, triglevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, 0.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, -triglevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 4, -overbslevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrLime)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 3, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 4, clrRed)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_SOLID)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASH)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 3, STYLE_DASH)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 4, STYLE_SOLID)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 0, 4)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 1, 1)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 2, 1)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 3, 1)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 4, 4)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((((BarsCalculated(FsATR_Handle) < rates_total and weight) or (BarsCalculated(SlATR_Handle) < rates_total and weight)) or BarsCalculated(FsCCI_Handle) < rates_total) or BarsCalculated(SlCCI_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    Kw = 0.0
    FsCCI = Arr(0, 0.0)
    SlCCI = Arr(0, 0.0)
    FsATR = Arr(0, 0.0)
    SlATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(FsATR_Handle, 0, 0, to_copy, FsATR) <= 0:
        return 0
    if CopyBuffer(SlATR_Handle, 0, 0, to_copy, SlATR) <= 0:
        return 0
    if CopyBuffer(FsCCI_Handle, 0, 0, to_copy, FsCCI) <= 0:
        return 0
    if CopyBuffer(SlCCI_Handle, 0, 0, to_copy, SlCCI) <= 0:
        return 0
    ArraySetAsSeries(FsATR, True)
    ArraySetAsSeries(SlATR, True)
    ArraySetAsSeries(FsCCI, True)
    ArraySetAsSeries(SlCCI, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if weight:
            if not SlATR[bar]:
                continue
            Kw = _fdiv(weight * FsATR[bar], SlATR[bar])
            FsCCI[bar] *= Kw
            SlCCI[bar] *= Kw
        FsCCI[bar] = MathMin(FsCCI[bar], overbslevel50)
        SlCCI[bar] = MathMin(SlCCI[bar], overbslevel50)
        FsCCI[bar] = MathMax(FsCCI[bar], -overbslevel50)
        SlCCI[bar] = MathMax(SlCCI[bar], -overbslevel50)
        IndBuffer[bar] = FsCCI[bar]
        UpBuffer[bar] = IndBuffer[bar]
        DnBuffer[bar] = SlCCI[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        clr = 2
        if IndBuffer[bar] > 0:
            if IndBuffer[bar] > IndBuffer[bar + 1]:
                clr = 4
            if IndBuffer[bar] < IndBuffer[bar + 1]:
                clr = 3
        if IndBuffer[bar] < 0:
            if IndBuffer[bar] < IndBuffer[bar + 1]:
                clr = 0
            if IndBuffer[bar] > IndBuffer[bar + 1]:
                clr = 1
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Weightedwcci(_MQL5Indicator):
    name = 'weightedwcci'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastCCI_Period': 7,  # Fast CCI period
        'SlowCCI_Period': 13,  # Slow CCI period
        'CCIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
        'weight': 1.0,  # Weight
        'overbslevel': 200,  # Extreme level
        'triglevel': 50,  # Trigger level
    }

