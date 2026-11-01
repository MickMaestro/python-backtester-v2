"""Convert iExposure.mq4 From MetaQuotes — converted from MQL5: MQL5 Indicators/Convert iExposure.mq4 From MetaQuotes/Convert iExposure.mq4 From MetaQuotes.mq5

Copyright: Dwi Sudarsono; Link: https://t.me/DwiSudarsono; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Dwi Sudarsono', 'link': 'https://t.me/DwiSudarsono', 'version': '1.00', 'window': 'separate', 'indicator_plots': 0, 'indicator_buffers': 1, 'indicator_minimum': 0.0, 'indicator_maximum': 0.1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Convert iExposure.mq4 From MetaQuotes', 'source': 'MQL5 Indicators/Convert iExposure.mq4 From MetaQuotes/Convert iExposure.mq4 From MetaQuotes.mq5', 'folder': 'Convert iExposure.mq4 From MetaQuotes', 'inputs': [{'mql': 'InpColor', 'py': 'InpColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Text color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

LightSeaGreen = 0xAAB220  # MQL4 colour name

# ---- inputs and global variables
ExtName = 'Exposure'
ExtSymbols = Arr(1024, "", dyn=False)
ExtSymbolsTotal = 0
ExtSymbolsSummaries = Arr(1024, 0.0, dyn=False, dims=(7,))
ExtLines = -1
ExtCols = Arr.of(['Symbol', 'Deals', 'Buy lots', 'Buy price', 'Sell lots', 'Sell price', 'Net lots', 'Profit'], fill="", dyn=False, size=8)
ExtShifts = Arr.of([10, 80, 130, 180, 260, 310, 390, 460], fill=0, dyn=False, size=8)
ExtVertShift = 14
ExtMapBuffer = Arr(0, 0.0)
chartid = 0

def OnInit():
    IndicatorSetString(INDICATOR_SHORTNAME, ExtName)
    SetIndexBuffer(0, ExtMapBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_NONE)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)

def OnDeinit(reason):
    windex = ChartWindowFind(chartid, ExtName)
    if windex > 0:
        ObjectsDeleteAll(windex)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global ExtLines
    name = ""
    i = 0
    col = 0
    line = 0
    windex = ChartWindowFind(chartid, ExtName)
    if windex < 0:
        return rates_total
    if ExtLines < 0:
        col = 0
        for col in range(col, 8):
            name = 'Head_' + _str(col)
            if ObjectCreate(chartid, name, OBJ_LABEL, windex, 0, 0):
                ObjectSetInteger(chartid, name, OBJPROP_XDISTANCE, ExtShifts[col])
                ObjectSetInteger(chartid, name, OBJPROP_YDISTANCE, ExtVertShift)
                ObjectSetString(chartid, name, OBJPROP_TEXT, ExtCols[col])
                ObjectSetString(chartid, name, OBJPROP_FONT, 'Arial')
                ObjectSetInteger(chartid, name, OBJPROP_FONTSIZE, 9)
                ObjectSetInteger(chartid, name, OBJPROP_COLOR, InpColor)
        else:
            col = _range_end(col, 8, 1)
        ExtLines = 0
    ArrayInitialize(ExtSymbolsSummaries, 0.0)
    total = Analyze()
    if total > 0:
        line = 0
        i = 0
        for i in range(i, ExtSymbolsTotal):
            if ExtSymbolsSummaries[i][0] <= 0:
                continue
            line += 1
            if line > ExtLines:
                y_dist = (ExtVertShift * (line + 1)) + 1
                col = 0
                for col in range(col, 8):
                    name = 'Line_' + _str(line) + '_' + _str(col)
                    if ObjectCreate(chartid, name, OBJ_LABEL, windex, 0, 0):
                        ObjectSetInteger(chartid, name, OBJPROP_XDISTANCE, ExtShifts[col])
                        ObjectSetInteger(chartid, name, OBJPROP_YDISTANCE, y_dist)
                else:
                    col = _range_end(col, 8, 1)
                ExtLines += 1
            digits = _int(SymbolInfoInteger(ExtSymbols[i], SYMBOL_DIGITS))
            buy_lots = ExtSymbolsSummaries[i][1]
            sell_lots = ExtSymbolsSummaries[i][3]
            buy_price = 0.0
            sell_price = 0.0
            if buy_lots != 0:
                buy_price = _fdiv(ExtSymbolsSummaries[i][2], buy_lots)
            if sell_lots != 0:
                sell_price = _fdiv(ExtSymbolsSummaries[i][4], sell_lots)
            name = 'Line_' + _str(line) + '_0'
            ObjectSetString(chartid, name, OBJPROP_TEXT, ExtSymbols[i])
            ObjectSetString(chartid, name, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(chartid, name, OBJPROP_FONTSIZE, 9)
            ObjectSetInteger(chartid, name, OBJPROP_COLOR, InpColor)
            name = 'Line_' + _str(line) + '_1'
            ObjectSetString(chartid, name, OBJPROP_TEXT, DoubleToString(ExtSymbolsSummaries[i][0], 0))
            ObjectSetString(chartid, name, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(chartid, name, OBJPROP_FONTSIZE, 9)
            ObjectSetInteger(chartid, name, OBJPROP_COLOR, InpColor)
            name = 'Line_' + _str(line) + '_2'
            ObjectSetString(chartid, name, OBJPROP_TEXT, DoubleToString(buy_lots, 2))
            ObjectSetString(chartid, name, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(chartid, name, OBJPROP_FONTSIZE, 9)
            ObjectSetInteger(chartid, name, OBJPROP_COLOR, InpColor)
            name = 'Line_' + _str(line) + '_3'
            ObjectSetString(chartid, name, OBJPROP_TEXT, DoubleToString(buy_price, digits))
            ObjectSetString(chartid, name, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(chartid, name, OBJPROP_FONTSIZE, 9)
            ObjectSetInteger(chartid, name, OBJPROP_COLOR, InpColor)
            name = 'Line_' + _str(line) + '_4'
            ObjectSetString(chartid, name, OBJPROP_TEXT, DoubleToString(sell_lots, 2))
            ObjectSetString(chartid, name, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(chartid, name, OBJPROP_FONTSIZE, 9)
            ObjectSetInteger(chartid, name, OBJPROP_COLOR, InpColor)
            name = 'Line_' + _str(line) + '_5'
            ObjectSetString(chartid, name, OBJPROP_TEXT, DoubleToString(sell_price, digits))
            ObjectSetString(chartid, name, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(chartid, name, OBJPROP_FONTSIZE, 9)
            ObjectSetInteger(chartid, name, OBJPROP_COLOR, InpColor)
            name = 'Line_' + _str(line) + '_6'
            ObjectSetString(chartid, name, OBJPROP_TEXT, DoubleToString(buy_lots - sell_lots, 2))
            ObjectSetString(chartid, name, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(chartid, name, OBJPROP_FONTSIZE, 9)
            ObjectSetInteger(chartid, name, OBJPROP_COLOR, InpColor)
            name = 'Line_' + _str(line) + '_7'
            ObjectSetString(chartid, name, OBJPROP_TEXT, DoubleToString(ExtSymbolsSummaries[i][6], 2))
            ObjectSetString(chartid, name, OBJPROP_FONT, 'Arial')
            ObjectSetInteger(chartid, name, OBJPROP_FONTSIZE, 9)
            ObjectSetInteger(chartid, name, OBJPROP_COLOR, InpColor)
        else:
            i = _range_end(i, ExtSymbolsTotal, 1)
    if total < ExtLines:
        line = ExtLines
        for line in range(line, total, -1):
            name = 'Line_' + _str(line) + '_0'
            ObjectSetString(chartid, name, OBJPROP_TEXT, ' ')
            name = 'Line_' + _str(line) + '_1'
            ObjectSetString(chartid, name, OBJPROP_TEXT, ' ')
            name = 'Line_' + _str(line) + '_2'
            ObjectSetString(chartid, name, OBJPROP_TEXT, ' ')
            name = 'Line_' + _str(line) + '_3'
            ObjectSetString(chartid, name, OBJPROP_TEXT, ' ')
            name = 'Line_' + _str(line) + '_4'
            ObjectSetString(chartid, name, OBJPROP_TEXT, ' ')
            name = 'Line_' + _str(line) + '_5'
            ObjectSetString(chartid, name, OBJPROP_TEXT, ' ')
            name = 'Line_' + _str(line) + '_6'
            ObjectSetString(chartid, name, OBJPROP_TEXT, ' ')
            name = 'Line_' + _str(line) + '_7'
            ObjectSetString(chartid, name, OBJPROP_TEXT, ' ')
        else:
            line = _range_end(line, total, -1)
    bars = iBars(Symbol(), Period())
    ExtMapBuffer[bars - 1] = -1.0
    return rates_total

def Analyze():
    profit = 0.0
    i = 0
    index = 0
    total = PositionsTotal()
    i = 0
    for i in range(i, total):
        if not PositionGetTicket(i):
            continue
        if PositionGetInteger(POSITION_TYPE) != POSITION_TYPE_BUY and PositionGetInteger(POSITION_TYPE) != POSITION_TYPE_SELL:
            continue
        index = SymbolsIndex(PositionGetString(POSITION_SYMBOL))
        if index < 0 or index >= 1024:
            continue
        ExtSymbolsSummaries[index][0] += 1
        profit = PositionGetDouble(POSITION_PROFIT) + PositionGetDouble(POSITION_SWAP) + AccountInfoDouble(ACCOUNT_COMMISSION_BLOCKED)
        ExtSymbolsSummaries[index][6] += profit
        if PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY:
            ExtSymbolsSummaries[index][1] += PositionGetDouble(POSITION_VOLUME)
            ExtSymbolsSummaries[index][2] += PositionGetDouble(POSITION_PRICE_OPEN) * PositionGetDouble(POSITION_VOLUME)
        else:
            ExtSymbolsSummaries[index][3] += PositionGetDouble(POSITION_VOLUME)
            ExtSymbolsSummaries[index][4] += PositionGetDouble(POSITION_PRICE_OPEN) * PositionGetDouble(POSITION_VOLUME)
    else:
        i = _range_end(i, total, 1)
    total = 0
    i = 0
    for i in range(i, ExtSymbolsTotal):
        if ExtSymbolsSummaries[i][0] > 0:
            total += 1
    else:
        i = _range_end(i, ExtSymbolsTotal, 1)
    return total

def SymbolsIndex(SymbolName_):
    global ExtSymbolsTotal
    found = False
    i = 0
    i = 0
    for i in range(i, ExtSymbolsTotal):
        if SymbolName_ == ExtSymbols[i]:
            found = True
            break
    else:
        i = _range_end(i, ExtSymbolsTotal, 1)
    if found:
        return i
    if ExtSymbolsTotal >= 1024:
        return -1
    i = ExtSymbolsTotal
    ExtSymbolsTotal += 1
    ExtSymbols[i] = SymbolName_
    ExtSymbolsSummaries[i][0] = 0.0
    ExtSymbolsSummaries[i][1] = 0.0
    ExtSymbolsSummaries[i][2] = 0.0
    ExtSymbolsSummaries[i][3] = 0.0
    ExtSymbolsSummaries[i][4] = 0.0
    ExtSymbolsSummaries[i][5] = 0.0
    ExtSymbolsSummaries[i][6] = 0.0
    return i

# ---- global variables initialised from expressions
InpColor = _input('InpColor', _uint(LightSeaGreen))  # Text color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ConvertIExposureMq4FromMetaQuotes(_MQL5Indicator):
    name = 'Convert iExposure.mq4 From MetaQuotes'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }
    y_range = (0.0, 0.1)

