"""draw_color_bars — converted from MQL5: MQL5 Indicators/DRAW_COLOR_BARS/draw_color_bars.mq5

DRAW_COLOR_BARS Indicator Demo
Draws colored bars for the specified symbol in a separate window
Symbol, and bars color and thickness are changing 
at random every N ticks
Copyright: Copyright 2011, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2011, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 16}, 'colors': {1: [255, 16711680, 32768, 65535, 16711935, 16776960, 65280, 42495]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'ColorBars'}, 'levels': [], 'description': ['DRAW_COLOR_BARS Indicator Demo', 'Draws colored bars for the specified symbol in a separate window', 'Symbol, and bars color and thickness are changing ', 'at random every N ticks'], 'name': 'draw_color_bars', 'source': 'MQL5 Indicators/DRAW_COLOR_BARS/draw_color_bars.mq5', 'folder': 'DRAW_COLOR_BARS', 'inputs': [{'mql': 'N', 'py': 'N', 'param': 'N', 'type': 'int', 'default': 5, 'label': 'Number of ticks to change view', 'sinput': False}, {'mql': 'bars', 'py': 'bars', 'param': 'bars', 'type': 'int', 'default': 500, 'label': 'Bars to display', 'sinput': False}, {'mql': 'messages', 'py': 'messages', 'param': 'messages', 'type': 'bool', 'default': False, 'label': 'Print messages into "Experts" log', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
N = _input('N', 5)  # Number of ticks to change view
bars = _input('bars', 500)  # Bars to display
messages = _input('messages', False)  # Print messages into "Experts" log
ColorBarsBuffer1 = Arr(0, 0.0)
ColorBarsBuffer2 = Arr(0, 0.0)
ColorBarsBuffer3 = Arr(0, 0.0)
ColorBarsBuffer4 = Arr(0, 0.0)
ColorBarsColors = Arr(0, 0.0)
symbol = ""
bars_colors = 0
colors = Arr.of([clrRed, clrBlue, clrGreen, clrChocolate, clrMagenta, clrDodgerBlue, clrGoldenrod, clrIndigo, clrLightBlue, clrAliceBlue, clrMoccasin, clrMagenta, clrCyan, clrMediumPurple], fill=0)

def OnInit():
    global bars_colors
    SetIndexBuffer(0, ColorBarsBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ColorBarsBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, ColorBarsBuffer3, INDICATOR_DATA)
    SetIndexBuffer(3, ColorBarsBuffer4, INDICATOR_DATA)
    SetIndexBuffer(4, ColorBarsColors, INDICATOR_COLOR_INDEX)
    bars_colors = 8
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_ticks, symbol
    _s_OnCalculate_ticks += 1
    if _s_OnCalculate_ticks >= N:
        symbol = GetRandomSymbolName()
        ChangeLineAppearance()
        ChangeColors(colors, bars_colors)
        tries = 0
        while (not CopyFromSymbolToBuffers(symbol, rates_total, bars_colors)) and tries < 5:
            tries += 1
        _s_OnCalculate_ticks = 0
    return rates_total

def CopyFromSymbolToBuffers(name, total, bar_colors):
    rates = Arr(0, 0, factory=MqlRates)
    attempts = 0
    copied = 0
    while attempts < 25 and (copied := CopyRates(name, Period(), 0, bars, rates)) < 0:
        Sleep(100)
        attempts += 1
        if messages:
            PrintFormat('%s CopyRates(%s) attempts=%d', 'CopyFromSymbolToBuffers', name, attempts)
    if copied != bars:
        comm = StringFormat('Для символа %s удалось получить только %d баров из %d затребованных', name, copied, bars)
        Comment(comm)
        if messages:
            Print(comm)
        return False
    else:
        PlotIndexSetString(0, PLOT_LABEL, name + ' Open;' + name + ' High;' + name + ' Low;' + name + ' Close')
        IndicatorSetString(INDICATOR_SHORTNAME, 'DRAW_BARS(' + name + ')')
    ArrayInitialize(ColorBarsBuffer1, 0.0)
    ArrayInitialize(ColorBarsBuffer2, 0.0)
    ArrayInitialize(ColorBarsBuffer3, 0.0)
    ArrayInitialize(ColorBarsBuffer4, 0.0)
    for i in range(0, copied):
        buffer_index = total - copied + i
        ColorBarsBuffer1[buffer_index] = rates[i].open
        ColorBarsBuffer2[buffer_index] = rates[i].high
        ColorBarsBuffer3[buffer_index] = rates[i].low
        ColorBarsBuffer4[buffer_index] = rates[i].close
        ColorBarsColors[buffer_index] = _imod(i, bar_colors)
    return True

def GetRandomSymbolName():
    symbols = SymbolsTotal(True)
    number = _imod(MathRand(), symbols)
    return SymbolName(number, True)

def ChangeColors(cols, plot_colors):
    size = ArraySize(cols)
    comm = ChartGetString(0, CHART_COMMENT) + '\r\n\r\n'
    for plot_color_ind in range(0, plot_colors):
        number = MathRand()
        i = _imod(number, size)
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, plot_color_ind, cols[i])
        comm = comm + StringFormat('SectionColorIndex[%d]=%s \r\n', plot_color_ind, ColorToString(cols[i], True))
        ChartSetString(0, CHART_COMMENT, comm)

def ChangeLineAppearance():
    comm = ''
    number = MathRand()
    width = _imod(number, 5)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, width)
    comm = comm + '\r\nWidth=' + IntegerToString(width)
    comm = '\r\n' + symbol + comm
    Comment(comm)

# ---- static local variables
_s_OnCalculate_ticks = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DrawColorBars(_MQL5Indicator):
    name = 'draw_color_bars'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'N': 5,  # Number of ticks to change view
        'bars': 500,  # Bars to display
        'messages': False,  # Print messages into "Experts" log
    }

