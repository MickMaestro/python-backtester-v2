"""draw_candles — converted from MQL5: MQL5 Indicators/DRAW_CANDLES/draw_candles.mq5

This indicator is a demo of DRAW_CANDLES drawing style.
It plots the candles of two different symbols in the separate window
 
The candles color and symbol
changed randomly each N ticks.
Copyright: Copyright 2011, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2011, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 15}, 'colors': {1: [32768]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'DRAW_CANDLES1'}, 'levels': [], 'description': ['This indicator is a demo of DRAW_CANDLES drawing style.', 'It plots the candles of two different symbols in the separate window', ' ', 'The candles color and symbol', 'changed randomly each N ticks.'], 'name': 'draw_candles', 'source': 'MQL5 Indicators/DRAW_CANDLES/draw_candles.mq5', 'folder': 'DRAW_CANDLES', 'inputs': [{'mql': 'N', 'py': 'N', 'param': 'N', 'type': 'int', 'default': 5, 'label': 'Ticks to change properties', 'sinput': False}, {'mql': 'bars', 'py': 'bars', 'param': 'bars', 'type': 'int', 'default': 500, 'label': 'Bars to show', 'sinput': False}, {'mql': 'messages', 'py': 'messages', 'param': 'messages', 'type': 'bool', 'default': False, 'label': 'Log messages', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
N = _input('N', 5)  # Ticks to change properties
bars = _input('bars', 500)  # Bars to show
messages = _input('messages', False)  # Log messages
Candle1Buffer1 = Arr(0, 0.0)
Candle1Buffer2 = Arr(0, 0.0)
Candle1Buffer3 = Arr(0, 0.0)
Candle1Buffer4 = Arr(0, 0.0)
symbol = ""
colors = Arr.of([clrRed, clrBlue, clrGreen, clrPurple, clrBrown, clrIndianRed], fill=0)

def OnInit():
    global symbol
    if bars < 50:
        Comment('Error: The bars must be > 50!')
        return INIT_PARAMETERS_INCORRECT
    SetIndexBuffer(0, Candle1Buffer1, INDICATOR_DATA)
    SetIndexBuffer(1, Candle1Buffer2, INDICATOR_DATA)
    SetIndexBuffer(2, Candle1Buffer3, INDICATOR_DATA)
    SetIndexBuffer(3, Candle1Buffer4, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    symbol = Symbol()
    PlotIndexSetString(0, PLOT_LABEL, symbol + ' Open;' + symbol + ' High;' + symbol + ' Low;' + symbol + ' Close')
    IndicatorSetString(INDICATOR_SHORTNAME, 'DRAW_CANDLES(' + symbol + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_ticks, symbol
    _s_OnCalculate_ticks += 1
    if _s_OnCalculate_ticks >= N:
        ChangeLineAppearance()
        symbol = GetRandomSymbolName()
        tries = 0
        while (not CopyFromSymbolToBuffers(symbol, rates_total, 0, Candle1Buffer1, Candle1Buffer2, Candle1Buffer3, Candle1Buffer4)) and tries < 5:
            tries += 1
        _s_OnCalculate_ticks = 0
    return rates_total

def CopyFromSymbolToBuffers(name, total, plot_index, buff1, buff2, buff3, buff4):
    rates = Arr(0, 0, factory=MqlRates)
    attempts = 0
    copied = 0
    while attempts < 25 and (copied := CopyRates(name, Period(), 0, bars, rates)) < 0:
        Sleep(100)
        attempts += 1
        if messages:
            PrintFormat('%s CopyRates(%s) attempts=%d', 'CopyFromSymbolToBuffers', name, attempts)
    if copied != bars:
        comm = StringFormat('Copied only %d bars for the symbol %s from %d needed', name, copied, bars)
        Comment(comm)
        if messages:
            Print(comm)
        return False
    else:
        PlotIndexSetString(plot_index, PLOT_LABEL, name + ' Open;' + name + ' High;' + name + ' Low;' + name + ' Close')
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
    comm = '\r\n' + symbol + comm
    Comment(comm)

# ---- static local variables
_s_OnCalculate_ticks = INT_MAX - 100


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DrawCandles(_MQL5Indicator):
    name = 'draw_candles'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'N': 5,  # Ticks to change properties
        'bars': 500,  # Bars to show
        'messages': False,  # Log messages
    }

