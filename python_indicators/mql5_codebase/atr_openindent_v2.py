"""atr_openindent_v2 — converted from MQL5: MQL5 Indicators/ATR_OpenIndent_v2/atr_openindent_v2.mq5

The indicator shows the opening price of the senior time frame (e.g., 1-day time frame) 
and draws line indents to the opening price, thus forming a range. 
Depending on the parameters the indicator can be used in the trading system to trade range breakouts 
or vice versa - to trade within the range.
Copyright: Copyright 2012, Rone; Link: rone.sergey@gmail.com; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, Rone', 'link': 'rone.sergey@gmail.com', 'version': '2.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [42495], 2: [16711680], 3: [255]}, 'widths': {1: 2, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Frame Open', 2: 'Upper Indent', 3: 'Lower Indent'}, 'levels': [], 'description': ['The indicator shows the opening price of the senior time frame (e.g., 1-day time frame) ', 'and draws line indents to the opening price, thus forming a range. ', 'Depending on the parameters the indicator can be used in the trading system to trade range breakouts ', 'or vice versa - to trade within the range.'], 'name': 'atr_openindent_v2', 'source': 'MQL5 Indicators/ATR_OpenIndent_v2/atr_openindent_v2.mq5', 'folder': 'ATR_OpenIndent_v2', 'inputs': [{'mql': 'InpTimeFrame', 'py': 'InpTimeFrame', 'param': 'InpTimeFrame', 'type': 'int', 'default': 16408, 'label': 'Base time frame for calculation', 'sinput': False}, {'mql': 'InpFrameAtrPeriod', 'py': 'InpFrameAtrPeriod', 'param': 'InpFrameAtrPeriod', 'type': 'int', 'default': 5, 'label': 'Base time frame ATR period', 'sinput': False}, {'mql': 'InpAtrCoef', 'py': 'InpAtrCoef', 'param': 'InpAtrCoef', 'type': 'double', 'default': 0.25, 'label': 'Indent ATR coefficient', 'sinput': False}, {'mql': 'InpUsePipsIndent', 'py': 'InpUsePipsIndent', 'param': 'InpUsePipsIndent', 'type': 'bool', 'default': False, 'label': 'Use indent in pips (instead of ATR)', 'sinput': False}, {'mql': 'InpPipsIndent', 'py': 'InpPipsIndent', 'param': 'InpPipsIndent', 'type': 'int', 'default': 30, 'label': 'Indent in pips (for 4 or 2 digits)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpTimeFrame = _input('InpTimeFrame', PERIOD_D1)  # Base time frame for calculation
InpFrameAtrPeriod = _input('InpFrameAtrPeriod', 5)  # Base time frame ATR period
InpAtrCoef = _input('InpAtrCoef', 0.25)  # Indent ATR coefficient
InpUsePipsIndent = _input('InpUsePipsIndent', False)  # Use indent in pips (instead of ATR)
InpPipsIndent = _input('InpPipsIndent', 30)  # Indent in pips (for 4 or 2 digits)
FrameOpenBuffer = Arr(0, 0.0)
UpperIndentBuffer = Arr(0, 0.0)
LowerIndentBuffer = Arr(0, 0.0)
ExtAtrFrameHandle = 0  # ATR indicator handle
ExtPipsIndent = 0  # Variable to control the indent in pips
minRequiredBars = 0  # Minimum required number of bars for calculation

def OnInit():
    global ExtAtrFrameHandle, ExtPipsIndent, minRequiredBars
    if InpTimeFrame < Period():
        Print('Base time frame must be longer than the current time frame!')
        return -1
    minRequiredBars = InpFrameAtrPeriod * _idiv(PeriodSeconds(InpTimeFrame), PeriodSeconds(Period()))
    if Digits() == 5 or Digits() == 3:
        ExtPipsIndent *= 10
    SetIndexBuffer(0, FrameOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, UpperIndentBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, LowerIndentBuffer, INDICATOR_DATA)
    for i in range(0, 3):
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, 0.0)
        PlotIndexSetInteger(i, PLOT_SHIFT, 0)
    ExtAtrFrameHandle = iATR(Symbol(), InpTimeFrame, InpFrameAtrPeriod)
    if ExtAtrFrameHandle < 0:
        Print('Error when creating the ATR indicator #', GetLastError())
        return -1
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    frameBars = 0
    startBar = 0
    calculated = 0
    mod = 0.0
    indent = 0.0
    frameBars = Bars(Symbol(), InpTimeFrame)
    if frameBars < InpFrameAtrPeriod or rates_total < minRequiredBars:
        return 0
    calculated = BarsCalculated(ExtAtrFrameHandle)
    if calculated < frameBars:
        Print('Not all ATR data calculated. Error #', GetLastError())
        return 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        startBar = minRequiredBars
        for bar in range(0, minRequiredBars):
            FrameOpenBuffer[bar] = 0.0
            UpperIndentBuffer[bar] = 0.0
            LowerIndentBuffer[bar] = 0.0
    else:
        startBar = prev_calculated - 1
    for bar in range(startBar, rates_total):
        mod = MathMod(time[bar], PeriodSeconds(InpTimeFrame))
        if mod == 0:
            FrameOpenBuffer[bar] = open[bar]
            indent = 0.0
            if not InpUsePipsIndent:
                FrameAtrArray = Arr(1, 0.0, dyn=False)
                if CopyBuffer(ExtAtrFrameHandle, 0, _DT(time[bar]), 1, FrameAtrArray) <= 0:
                    Print('Getting ATR data failed. Error #', GetLastError())
                    return 0
                else:
                    indent = NormalizeDouble(FrameAtrArray[0] * InpAtrCoef, Digits())
            else:
                indent = ExtPipsIndent * Point()
            UpperIndentBuffer[bar] = FrameOpenBuffer[bar] + indent
            LowerIndentBuffer[bar] = FrameOpenBuffer[bar] - indent
        else:
            prevBar = bar - 1
            FrameOpenBuffer[bar] = FrameOpenBuffer[prevBar]
            UpperIndentBuffer[bar] = UpperIndentBuffer[prevBar]
            LowerIndentBuffer[bar] = LowerIndentBuffer[prevBar]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AtrOpenindentV2(_MQL5Indicator):
    name = 'atr_openindent_v2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpTimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Base time frame for calculation
        'InpFrameAtrPeriod': 5,  # Base time frame ATR period
        'InpAtrCoef': 0.25,  # Indent ATR coefficient
        'InpUsePipsIndent': False,  # Use indent in pips (instead of ATR)
        'InpPipsIndent': 30,  # Indent in pips (for 4 or 2 digits)
    }

