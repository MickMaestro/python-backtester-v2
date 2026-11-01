"""draw_bars — converted from MQL5: MQL5 Indicators/DRAW_BARS/draw_bars.mq5

This indicator is a demo of DRAW_BARS drawing style
It plots the bars of the specified symbol in the separate window
The bars color, width and symbol changed randomly
after N ticks
Copyright: Copyright 2011, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2011, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 14}, 'colors': {1: [32768]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Bars'}, 'levels': [], 'description': ['This indicator is a demo of DRAW_BARS drawing style', 'It plots the bars of the specified symbol in the separate window', 'The bars color, width and symbol changed randomly', 'after N ticks'], 'name': 'draw_bars', 'source': 'MQL5 Indicators/DRAW_BARS/draw_bars.mq5', 'folder': 'DRAW_BARS', 'inputs': [{'mql': 'N', 'py': 'N', 'param': 'N', 'type': 'int', 'default': 5, 'label': 'Ticks to change properties', 'sinput': False}, {'mql': 'bars', 'py': 'bars', 'param': 'bars', 'type': 'int', 'default': 500, 'label': 'Bars to show', 'sinput': False}, {'mql': 'messages', 'py': 'messages', 'param': 'messages', 'type': 'bool', 'default': False, 'label': 'Log messages to "Experts" tab', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
N = _input('N', 5)  # Ticks to change properties
bars = _input('bars', 500)  # Bars to show
messages = _input('messages', False)  # Log messages to "Experts" tab
BarsBuffer1 = Arr(0, 0.0)
BarsBuffer2 = Arr(0, 0.0)
BarsBuffer3 = Arr(0, 0.0)
BarsBuffer4 = Arr(0, 0.0)
symbol = ""
colors = Arr.of([clrRed, clrBlue, clrGreen, clrPurple, clrBrown, clrIndianRed], fill=0)

def OnInit():
    global symbol
    if bars < 50:
        Comment('Increase the bars input variable to 50!')
        return INIT_PARAMETERS_INCORRECT
    SetIndexBuffer(0, BarsBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, BarsBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, BarsBuffer3, INDICATOR_DATA)
    SetIndexBuffer(3, BarsBuffer4, INDICATOR_DATA)
    symbol = Symbol()
    PlotIndexSetString(0, PLOT_LABEL, symbol + ' Open;' + symbol + ' High;' + symbol + ' Low;' + symbol + ' Close')
    IndicatorSetString(INDICATOR_SHORTNAME, 'DRAW_BARS(' + symbol + ')')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_ticks, symbol
    _s_OnCalculate_ticks += 1
    if _s_OnCalculate_ticks >= N:
        symbol = GetRandomSymbolName()
        ChangeLineAppearance()
        tries = 0
        while (not CopyFromSymbolToBuffers(symbol, rates_total)) and tries < 5:
            tries += 1
        _s_OnCalculate_ticks = 0
    return rates_total

def CopyFromSymbolToBuffers(name, total):
    rates = Arr(0, 0, factory=MqlRates)
    attempts = 0
    copied = 0
    while attempts < 25 and (copied := CopyRates(name, Period(), 0, bars, rates)) < 0:
        Sleep(100)
        attempts += 1
        if messages:
            PrintFormat('%s CopyRates(%s) attempts=%d', 'CopyFromSymbolToBuffers', name, attempts)
    if copied != bars:
        comm = StringFormat('Error: Copied only %d bars of %d needed for the %s symbol ', name, copied, bars)
        Comment(comm)
        if messages:
            Print(comm)
        return False
    else:
        PlotIndexSetString(0, PLOT_LABEL, name + ' Open;' + name + ' High;' + name + ' Low;' + name + ' Close')
        IndicatorSetString(INDICATOR_SHORTNAME, 'DRAW_BARS(' + name + ')')
    ArrayInitialize(BarsBuffer1, 0.0)
    ArrayInitialize(BarsBuffer2, 0.0)
    ArrayInitialize(BarsBuffer3, 0.0)
    ArrayInitialize(BarsBuffer4, 0.0)
    for i in range(0, copied):
        buffer_index = total - copied + i
        BarsBuffer1[buffer_index] = rates[i].open
        BarsBuffer2[buffer_index] = rates[i].high
        BarsBuffer3[buffer_index] = rates[i].low
        BarsBuffer4[buffer_index] = rates[i].close
    return True

def GetRandomSymbolName():
    symbols = SymbolsTotal(True)
    number = _imod(MathRand(), symbols)
    return SymbolName(number, True)

def ChangeLineAppearance():
    comm = ''
    number = MathRand()
    size = ArraySize(colors)
    color_index = _imod(number, size)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, colors[color_index])
    comm = comm + '\r\n' + _str(colors[color_index])
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


class DrawBars(_MQL5Indicator):
    name = 'draw_bars'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'N': 5,  # Ticks to change properties
        'bars': 500,  # Bars to show
        'messages': False,  # Log messages to "Experts" tab
    }

