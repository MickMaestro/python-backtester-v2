"""dcc — converted from MQL5: MQL5 Indicators/DCC/dcc.mq5

Copyright: 2012, Karlson.; Link: https://login.mql5.com/en/users/Karlson

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2012, Karlson.', 'link': 'https://login.mql5.com/en/users/Karlson', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'dcc', 'source': 'MQL5 Indicators/DCC/dcc.mq5', 'folder': 'DCC', 'inputs': [{'mql': 'symbol', 'py': 'symbol', 'param': None, 'type': 'string', 'default': 'GBPUSD', 'label': 'Symbol', 'sinput': False}, {'mql': 'type', 'py': 'type_', 'param': 'type_', 'type': 'int', 'default': 17, 'label': 'Type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
bars = 500  # Bars
symbol = _input('symbol', 'GBPUSD')  # Symbol
type_ = _input('type_', DRAW_COLOR_CANDLES)  # Type
ColorCandlesBuffer1 = Arr(0, 0.0)
ColorCandlesBuffer2 = Arr(0, 0.0)
ColorCandlesBuffer3 = Arr(0, 0.0)
ColorCandlesBuffer4 = Arr(0, 0.0)
ColorCandlesColors = Arr(0, 0.0)
col = Arr.of([clrBlack, clrDarkGreen, clrDarkSlateGray, clrOlive, clrGreen, clrTeal, clrNavy, clrPurple, clrMaroon, clrIndigo, clrDarkBlue, clrDarkOliveGreen, clrSaddleBrown, clrForestGreen, clrOliveDrab, clrSeaGreen, clrDarkGoldenrod, clrDarkSlateBlue, clrSienna, clrMediumBlue, clrBrown, clrDarkTurquoise, clrDimGray, clrLightSeaGreen, clrDarkViolet, clrFireBrick, clrMediumVioletRed, clrMediumSeaGreen, clrChocolate, clrCrimson, clrSteelBlue, clrGoldenrod, clrMediumSpringGreen, clrLawnGreen, clrCadetBlue, clrDarkOrchid, clrYellowGreen, clrLimeGreen, clrOrangeRed, clrDarkOrange, clrOrange, clrChartreuse, clrLime, clrDeepSkyBlue, clrBlue, clrMagenta, clrRed, clrSlateGray, clrPeru, clrBlueViolet, clrDeepPink, clrMediumTurquoise, clrDodgerBlue, clrTurquoise, clrRoyalBlue, clrSlateBlue], fill=0, dyn=False, size=56)

def OnInit():
    SetIndexBuffer(0, ColorCandlesBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ColorCandlesBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, ColorCandlesBuffer3, INDICATOR_DATA)
    SetIndexBuffer(3, ColorCandlesBuffer4, INDICATOR_DATA)
    SetIndexBuffer(4, ColorCandlesColors, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 3)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, col[GetNumber()])
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, col[GetNumber() + 28])
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 2, clrBlack)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, type_)
    PlotIndexSetString(0, PLOT_LABEL, symbol + ' Open;' + symbol + ' High;' + symbol + ' Low;' + symbol + ' Close')
    IndicatorSetString(INDICATOR_SHORTNAME, 'DCC(' + symbol + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    tries = 0
    while (not CopyFromSymbolToBuffers(symbol, rates_total, ColorCandlesBuffer1, ColorCandlesBuffer2, ColorCandlesBuffer3, ColorCandlesBuffer4, ColorCandlesColors)) and tries < 5:
        Print('tries=', tries)
        tries += 1
    return rates_total

def CopyFromSymbolToBuffers(name, total, buff1, buff2, buff3, buff4, col_buffer):
    rates = Arr(0, 0, factory=MqlRates)
    attempts = 0
    copied = 0
    while attempts < 25 and (copied := CopyRates(name, Period(), 0, bars, rates)) < bars:
        Sleep(100)
        attempts += 1
    ArrayInitialize(buff1, 0.0)
    ArrayInitialize(buff2, 0.0)
    ArrayInitialize(buff3, 0.0)
    ArrayInitialize(buff4, 0.0)
    for i in range(0, copied):
        buffer_index = total - copied + i
        buff1[buffer_index] = rates[i].open
        buff2[buffer_index] = rates[i].high
        buff3[buffer_index] = rates[i].low
        buff4[buffer_index] = rates[i].close
        if buff1[buffer_index] < buff4[buffer_index]:
            col_buffer[buffer_index] = 0.0
        else:
            col_buffer[buffer_index] = 2.0
        if buff1[buffer_index] > buff4[buffer_index]:
            col_buffer[buffer_index] = 1.0
    return True

def GetNumber():
    MathSrand(GetTickCount())
    col_index = _idiv(MathRand(), 1220)
    if GetLastError() > 0:
        Print('Error(CustomColor)=', GetLastError())
    return col_index


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dcc(_MQL5Indicator):
    name = 'dcc'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'type_': _Choice({0: 'None', 1: 'Line', 2: 'Section', 3: 'Histogram', 4: 'Histogram2', 5: 'Arrow', 6: 'Zigzag', 7: 'Filling', 8: 'Color Line', 9: 'Color Section', 10: 'Color Histogram', 11: 'Color Histogram2', 12: 'Color Arrow', 13: 'Color Zigzag', 14: 'Bars', 15: 'Candles', 16: 'Color Bars', 17: 'Color Candles'}, default=17),  # Type
    }

