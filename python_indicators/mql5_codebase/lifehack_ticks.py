"""LifeHack_Ticks — converted from MQL5: MQL5 Indicators/LifeHack Ticks/LifeHack_Ticks.mq5

Tick Indicators
Copyright: Copyright © 2016, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.003

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.003', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Ask', 2: 'Bid'}, 'levels': [], 'description': ['Tick Indicators'], 'name': 'LifeHack_Ticks', 'source': 'MQL5 Indicators/LifeHack Ticks/LifeHack_Ticks.mq5', 'folder': 'LifeHack Ticks', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
AskBuffer = Arr(0, 0.0)
BidBuffer = Arr(0, 0.0)
AskBufferTemp = Arr(0, 0.0)
BidBufferTemp = Arr(0, 0.0)
InpVisible = 300

def OnInit():
    SetIndexBuffer(0, AskBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, BidBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, AskBufferTemp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BidBufferTemp, INDICATOR_CALCULATIONS)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(AskBuffer, True)
    ArraySetAsSeries(BidBuffer, True)
    ArraySetAsSeries(AskBufferTemp, True)
    ArraySetAsSeries(BidBufferTemp, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'LifeHack Ticks ')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if prev_calculated == 0:
        for i in range(0, rates_total):
            AskBuffer[i] = 0.0
            AskBufferTemp[i] = 0.0
            BidBuffer[i] = 0.0
            BidBufferTemp[i] = 0.0
        if not TextCreate(0, 'Text', ChartWindowFind(), time[rates_total - 1], 0.0, 'Text', 'Arial', 10, clrGreen, 0.0, ANCHOR_RIGHT, False, False, True, 0):
            return rates_total
        return rates_total
    last_tick = MqlTick()
    if SymbolInfoTick(Symbol(), last_tick):
        delta = rates_total - prev_calculated
        ArrayCopy(AskBufferTemp, AskBuffer, 1, 0 + delta, InpVisible)
        AskBufferTemp[0] = last_tick.ask
        ArrayCopy(AskBuffer, AskBufferTemp, 0, 0, InpVisible)
        ArrayCopy(BidBufferTemp, BidBuffer, 1, 0 + delta, InpVisible)
        BidBufferTemp[0] = last_tick.bid
        ArrayCopy(BidBuffer, BidBufferTemp, 0, 0, InpVisible)
        for z in range(0, delta):
            AskBuffer[InpVisible - z] = 0.0
            AskBufferTemp[InpVisible - z] = 0.0
            BidBuffer[InpVisible - z] = 0.0
            BidBufferTemp[InpVisible - z] = 0.0
        TextChange(0, 'Text', TimeToString(last_tick.time, (TIME_DATE | TIME_MINUTES) | TIME_SECONDS))
        max_ = ChartGetDouble(0, CHART_PRICE_MAX, ChartWindowFind())
        min_ = ChartGetDouble(0, CHART_PRICE_MIN, ChartWindowFind())
        TextMove(0, 'Text', time[rates_total - 20], (max_ + min_) / 2.0)
    else:
        return 0
    return rates_total

def TextCreate(chart_ID=0, name='Text', sub_window=0, time=0, price=0.0, text='Text', font='Arial', font_size=10, clr=clrRed, angle=0.0, anchor=ANCHOR_LEFT_UPPER, back=False, selection=False, hidden=True, z_order=0):
    time = Box(time)
    price = Box(price)
    ChangeTextEmptyPoint(time, price)
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_TEXT, sub_window, time.v, price.v):
        Print('TextCreate', ': failed to create "Text" object! Error code = ', GetLastError())
        return False
    ObjectSetString(chart_ID, name, OBJPROP_TEXT, text)
    ObjectSetString(chart_ID, name, OBJPROP_FONT, font)
    ObjectSetInteger(chart_ID, name, OBJPROP_FONTSIZE, font_size)
    ObjectSetDouble(chart_ID, name, OBJPROP_ANGLE, angle)
    ObjectSetInteger(chart_ID, name, OBJPROP_ANCHOR, anchor)
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True

def TextMove(chart_ID=0, name='Text', time=0, price=0.0):
    if not time:
        time = TimeCurrent()
    if not price:
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ResetLastError()
    if not ObjectMove(chart_ID, name, 0, time, price):
        Print('TextMove', ': failed to move the anchor point! Error code = ', GetLastError())
        return False
    return True

def TextChange(chart_ID=0, name='Text', text='Text'):
    ResetLastError()
    if not ObjectSetString(chart_ID, name, OBJPROP_TEXT, text):
        Print('TextChange', ': failed to change the text! Error code = ', GetLastError())
        return False
    return True

def TextDelete(chart_ID=0, name='Text'):
    ResetLastError()
    if not ObjectDelete(chart_ID, name):
        Print('TextDelete', ': failed to delete "Text" object! Error code = ', GetLastError())
        return False
    return True

def ChangeTextEmptyPoint(time, price):
    if not time.v:
        time.v = TimeCurrent()
    if not price.v:
        price.v = SymbolInfoDouble(Symbol(), SYMBOL_BID)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LifeHackTicks(_MQL5Indicator):
    name = 'LifeHack_Ticks'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

