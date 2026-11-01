"""BreakevenLine — converted from MQL5: MQL5 Indicators/Breakeven Line Indicator for MT5/BreakevenLine.mq5

Displays a breakeven line for the current symbol.
You can hide/show the line by pressing Shift+B.
Copyright: www.Wolfforex.com, 2025; Version: 2.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.Wolfforex.com, 2025', 'version': '2.01', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Displays a breakeven line for the current symbol.', 'You can hide/show the line by pressing Shift+B.'], 'name': 'BreakevenLine', 'source': 'MQL5 Indicators/Breakeven Line Indicator for MT5/BreakevenLine.mq5', 'folder': 'Breakeven Line Indicator for MT5', 'inputs': [{'mql': 'IgnoreLong', 'py': 'IgnoreLong', 'param': 'IgnoreLong', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'IgnoreShort', 'py': 'IgnoreShort', 'param': 'IgnoreShort', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'line_color_buy', 'py': 'line_color_buy', 'param': None, 'type': 'color', 'default': 8421376, 'label': '', 'sinput': False}, {'mql': 'line_color_sell', 'py': 'line_color_sell', 'param': None, 'type': 'color', 'default': 13353215, 'label': '', 'sinput': False}, {'mql': 'line_color_neutral', 'py': 'line_color_neutral', 'param': None, 'type': 'color', 'default': 9470064, 'label': '', 'sinput': False}, {'mql': 'line_style', 'py': 'line_style', 'param': 'line_style', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'line_width', 'py': 'line_width', 'param': 'line_width', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'font_color', 'py': 'font_color', 'param': None, 'type': 'color', 'default': 9470064, 'label': '', 'sinput': False}, {'mql': 'font_size', 'py': 'font_size', 'param': 'font_size', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'font_face', 'py': 'font_face', 'param': None, 'type': 'string', 'default': 'Courier', 'label': '', 'sinput': False}, {'mql': 'ObjectPrefix', 'py': 'ObjectPrefix', 'param': None, 'type': 'string', 'default': 'BEL_', 'label': 'ObjectPrefix: To prevent confusion with other indicators/EAs.', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

OBJ_ALL_PERIODS = 0  # MQL5 constant unknown to the converter
OBJ_NO_PERIODS = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
IgnoreLong = _input('IgnoreLong', False)
IgnoreShort = _input('IgnoreShort', False)
line_color_buy = _input('line_color_buy', clrTeal)
line_color_sell = _input('line_color_sell', clrPink)
line_color_neutral = _input('line_color_neutral', clrSlateGray)
line_style = _input('line_style', STYLE_SOLID)
line_width = _input('line_width', 1)
font_color = _input('font_color', clrSlateGray)
font_size = _input('font_size', 12)
font_face = _input('font_face', 'Courier')
ObjectPrefix = _input('ObjectPrefix', 'BEL_')  # ObjectPrefix: To prevent confusion with other indicators/EAs.
PositionsLong = 0
PositionsShort = 0
PositionsTotal_v = 0
VolumeLong = 0.0
PriceLong = 0.0
ProfitLong = 0.0
VolumeShort = 0.0
PriceShort = 0.0
ProfitShort = 0.0
VolumeTotal = 0.0
ProfitTotal = 0.0
PriceAverage = 0.0
DistancePoints = 0.0
Pip_Value = 0.0
Pip_Size = 0.0
LotStep = 0.0
LotStep_digits = 0
object_line = ""
object_label = ""

def OnInit():
    global object_label, object_line
    object_line = ObjectPrefix + 'Line' + Symbol()
    object_label = ObjectPrefix + 'Label' + Symbol()
    EventSetMillisecondTimer(200)

def OnDeinit(reason):
    ObjectsDeleteAll(0, ObjectPrefix)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if iBars(Symbol(), Period()) <= 0:
        return 0
    if CalculateData():
        DrawData()
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ == CHARTEVENT_CHART_CHANGE:
        DrawData()
    elif id_ == CHARTEVENT_KEYDOWN:
        if lparam == 66 and TerminalInfoInteger(TERMINAL_KEYSTATE_SHIFT) < 0:
            if ObjectGetInteger(0, object_line, OBJPROP_TIMEFRAMES) == OBJ_NO_PERIODS:
                ObjectSetInteger(0, object_line, OBJPROP_TIMEFRAMES, OBJ_ALL_PERIODS)
                ObjectSetInteger(0, object_label, OBJPROP_TIMEFRAMES, OBJ_ALL_PERIODS)
            else:
                ObjectSetInteger(0, object_line, OBJPROP_TIMEFRAMES, OBJ_NO_PERIODS)
                ObjectSetInteger(0, object_label, OBJPROP_TIMEFRAMES, OBJ_NO_PERIODS)
            ChartRedraw()

def OnTrade():
    if CalculateData():
        DrawData()
    ChartRedraw()

def OnTimer():
    DrawData()
    ChartRedraw()

def CalculateData():
    global DistancePoints, Pip_Size, Pip_Value, PositionsLong, PositionsShort, PositionsTotal_v, PriceAverage, PriceLong, PriceShort, ProfitLong, ProfitShort, ProfitTotal, VolumeLong, VolumeShort, VolumeTotal
    PositionsLong = 0
    VolumeLong = 0.0
    PriceLong = 0.0
    ProfitLong = 0.0
    PositionsShort = 0
    VolumeShort = 0.0
    PriceShort = 0.0
    ProfitShort = 0.0
    PositionsTotal_v = 0
    VolumeTotal = 0.0
    ProfitTotal = 0.0
    PriceAverage = 0.0
    DistancePoints = 0.0
    Pip_Value = SymbolInfoDouble(Symbol(), SYMBOL_TRADE_TICK_VALUE)
    Pip_Size = SymbolInfoDouble(Symbol(), SYMBOL_TRADE_TICK_SIZE)
    if Pip_Value == 0 or Pip_Size == 0:
        return False
    total = PositionsTotal()
    for i in range(0, total):
        pos_symbol = _str(PositionGetSymbol(i))
        if pos_symbol != '':
            if pos_symbol != Symbol():
                continue
            if PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY:
                if IgnoreLong:
                    continue
                PositionsLong += 1
                PriceLong += PositionGetDouble(POSITION_PRICE_OPEN) * PositionGetDouble(POSITION_VOLUME)
                VolumeLong += PositionGetDouble(POSITION_VOLUME)
                ticket = PositionGetInteger(POSITION_TICKET)
                HistoryDealGetDouble(ticket, DEAL_COMMISSION)
                ProfitLong += PositionGetDouble(POSITION_PROFIT) + PositionGetDouble(POSITION_SWAP) + HistoryDealGetDouble(ticket, DEAL_COMMISSION)
            elif PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_SELL:
                if IgnoreShort:
                    continue
                PositionsShort += 1
                PriceShort += PositionGetDouble(POSITION_PRICE_OPEN) * PositionGetDouble(POSITION_VOLUME)
                VolumeShort += PositionGetDouble(POSITION_VOLUME)
                ticket = PositionGetInteger(POSITION_TICKET)
                HistoryDealGetDouble(ticket, DEAL_COMMISSION)
                ProfitShort += PositionGetDouble(POSITION_PROFIT) + PositionGetDouble(POSITION_SWAP) + HistoryDealGetDouble(ticket, DEAL_COMMISSION)
        else:
            Print('Error selecting position #', i, ': ', GetLastError())
    if PriceLong > 0:
        PriceLong = _fdiv(PriceLong, VolumeLong)
    if PriceShort > 0:
        PriceShort = _fdiv(PriceShort, VolumeShort)
    PositionsTotal_v = PositionsLong + PositionsShort
    VolumeTotal = VolumeLong - VolumeShort
    ProfitTotal = ProfitLong + ProfitShort
    if PositionsTotal_v > 0:
        Ask = SymbolInfoDouble(Symbol(), SYMBOL_ASK)
        Bid = SymbolInfoDouble(Symbol(), SYMBOL_BID)
        if VolumeTotal != 0:
            DistancePoints = _fdiv(ProfitTotal, MathAbs(VolumeTotal * Pip_Value)) * Pip_Size
            if VolumeTotal > 0:
                PriceAverage = Bid - DistancePoints
            else:
                PriceAverage = Ask + DistancePoints
        else:
            DistancePoints = _fdiv(ProfitTotal, Pip_Value) * Pip_Size
            PriceAverage = ((Ask + Bid) / 2) - DistancePoints
    return True

def DrawData():
    global LotStep, LotStep_digits
    if ObjectFind(0, object_line) < 0:
        ObjectCreate(0, object_line, OBJ_HLINE, 0, 0, PriceAverage)
        ObjectSetInteger(0, object_line, OBJPROP_WIDTH, 0, line_width)
        ObjectSetInteger(0, object_line, OBJPROP_STYLE, 0, line_style)
        ObjectSetInteger(0, object_line, OBJPROP_SELECTABLE, False)
        ObjectSetInteger(0, object_line, OBJPROP_HIDDEN, True)
    else:
        ObjectMove(0, object_line, 0, 0, PriceAverage)
    colour = line_color_buy
    if VolumeTotal < 0:
        colour = line_color_sell
    elif VolumeTotal == 0:
        colour = line_color_neutral
    ObjectSetInteger(0, object_line, OBJPROP_COLOR, colour)
    if ObjectFind(0, object_label) < 0:
        ObjectCreate(0, object_label, OBJ_LABEL, 0, 0, 0)
        ObjectSetInteger(0, object_label, OBJPROP_SELECTABLE, False)
        ObjectSetInteger(0, object_label, OBJPROP_HIDDEN, True)
        ObjectSetInteger(0, object_label, OBJPROP_FONTSIZE, font_size)
        ObjectSetString(0, object_label, OBJPROP_FONT, font_face)
        ObjectSetInteger(0, object_label, OBJPROP_COLOR, font_color)
        LotStep = SymbolInfoDouble(Symbol(), SYMBOL_VOLUME_STEP)
        LotStep_digits = CountDecimalPlaces(LotStep)
    x = Box(0)
    y = Box(0)
    real_x = 0
    w = Box(0)
    h = Box(0)
    text = IntegerToString(_int(MathRound(_fdiv(DistancePoints, Point())))) + ' (' + DoubleToString(ProfitTotal, 2) + ' ' + AccountInfoString(ACCOUNT_CURRENCY) + ') ' + DoubleToString(VolumeTotal, LotStep_digits) + ' lots, N = ' + IntegerToString(PositionsTotal_v)
    ObjectSetString(0, object_label, OBJPROP_TEXT, text)
    real_x = ChartGetInteger(0, CHART_WIDTH_IN_PIXELS) - 2
    ChartTimePriceToXY(0, 0, iTime(Symbol(), Period(), 0), PriceAverage, x, y)
    TextSetFont(font_face, font_size * -10)
    TextGetSize(text, w, h)
    ObjectSetInteger(0, object_label, OBJPROP_XDISTANCE, real_x - w.v)
    y.v -= _int(h.v + 1)
    ObjectSetInteger(0, object_label, OBJPROP_YDISTANCE, y.v)

def CountDecimalPlaces(number):
    for i in range(0, 100):
        pwr = MathPow(10, i)
        if _fdiv(MathRound(number * pwr), pwr) == number:
            return i
    return -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BreakevenLine(_MQL5Indicator):
    name = 'BreakevenLine'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'IgnoreLong': False,
        'IgnoreShort': False,
        'line_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),
        'line_width': 1,
        'font_size': 12,
    }

