"""PY_Signal — converted from MQL5: MQL5 Indicators/PY_Signal/PY_Signal.mq5

Copyright: I Made Purnama Yasa; Link: imade.purnamayasa@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'I Made Purnama Yasa', 'link': 'imade.purnamayasa@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'PY_Signal', 'source': 'MQL5 Indicators/PY_Signal/PY_Signal.mq5', 'folder': 'PY_Signal', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
b = 0
s = 0
n = 0

def OnInit():
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global b, n, s
    b = 0
    s = 0
    n = 0
    x = 0
    y = 0
    x = 190
    y = 12
    GuiHeader(PERIOD_M5, (x := x - 20), y)
    GuiHeader(PERIOD_M15, (x := x - 20), y)
    GuiHeader(PERIOD_M30, (x := x - 20), y)
    GuiHeader(PERIOD_H1, (x := x - 20), y)
    GuiHeader(PERIOD_H4, (x := x - 20), y)
    GuiHeader(PERIOD_D1, (x := x - 20), y)
    GuiHeader(PERIOD_W1, (x := x - 20), y)
    GuiHeader(PERIOD_MN1, (x := x - 20), y)
    x = 190
    y = y + 12
    Price(PERIOD_M5, (x := x - 20), y)
    Price(PERIOD_M15, (x := x - 20), y)
    Price(PERIOD_M30, (x := x - 20), y)
    Price(PERIOD_H1, (x := x - 20), y)
    Price(PERIOD_H4, (x := x - 20), y)
    Price(PERIOD_D1, (x := x - 20), y)
    Price(PERIOD_W1, (x := x - 20), y)
    Price(PERIOD_MN1, (x := x - 20), y)
    x = 190
    y = y + 12
    SMA5(PERIOD_M5, (x := x - 20), y)
    SMA5(PERIOD_M15, (x := x - 20), y)
    SMA5(PERIOD_M30, (x := x - 20), y)
    SMA5(PERIOD_H1, (x := x - 20), y)
    SMA5(PERIOD_H4, (x := x - 20), y)
    SMA5(PERIOD_D1, (x := x - 20), y)
    SMA5(PERIOD_W1, (x := x - 20), y)
    SMA5(PERIOD_MN1, (x := x - 20), y)
    x = 190
    y = y + 12
    SMA10(PERIOD_M5, (x := x - 20), y)
    SMA10(PERIOD_M15, (x := x - 20), y)
    SMA10(PERIOD_M30, (x := x - 20), y)
    SMA10(PERIOD_H1, (x := x - 20), y)
    SMA10(PERIOD_H4, (x := x - 20), y)
    SMA10(PERIOD_D1, (x := x - 20), y)
    SMA10(PERIOD_W1, (x := x - 20), y)
    SMA10(PERIOD_MN1, (x := x - 20), y)
    x = 190
    y = y + 12
    SMA20(PERIOD_M5, (x := x - 20), y)
    SMA20(PERIOD_M15, (x := x - 20), y)
    SMA20(PERIOD_M30, (x := x - 20), y)
    SMA20(PERIOD_H1, (x := x - 20), y)
    SMA20(PERIOD_H4, (x := x - 20), y)
    SMA20(PERIOD_D1, (x := x - 20), y)
    SMA20(PERIOD_W1, (x := x - 20), y)
    SMA20(PERIOD_MN1, (x := x - 20), y)
    x = 190
    y = y + 12
    SMA50(PERIOD_M5, (x := x - 20), y)
    SMA50(PERIOD_M15, (x := x - 20), y)
    SMA50(PERIOD_M30, (x := x - 20), y)
    SMA50(PERIOD_H1, (x := x - 20), y)
    SMA50(PERIOD_H4, (x := x - 20), y)
    SMA50(PERIOD_D1, (x := x - 20), y)
    SMA50(PERIOD_W1, (x := x - 20), y)
    SMA50(PERIOD_MN1, (x := x - 20), y)
    x = 190
    y = y + 12
    SMA100(PERIOD_M5, (x := x - 20), y)
    SMA100(PERIOD_M15, (x := x - 20), y)
    SMA100(PERIOD_M30, (x := x - 20), y)
    SMA100(PERIOD_H1, (x := x - 20), y)
    SMA100(PERIOD_H4, (x := x - 20), y)
    SMA100(PERIOD_D1, (x := x - 20), y)
    SMA100(PERIOD_W1, (x := x - 20), y)
    SMA100(PERIOD_MN1, (x := x - 20), y)
    x = 190
    y = y + 12
    SMA200(PERIOD_M5, (x := x - 20), y)
    SMA200(PERIOD_M15, (x := x - 20), y)
    SMA200(PERIOD_M30, (x := x - 20), y)
    SMA200(PERIOD_H1, (x := x - 20), y)
    SMA200(PERIOD_H4, (x := x - 20), y)
    SMA200(PERIOD_D1, (x := x - 20), y)
    SMA200(PERIOD_W1, (x := x - 20), y)
    SMA200(PERIOD_MN1, (x := x - 20), y)
    x = 190
    y = y + 12
    STO(PERIOD_M5, (x := x - 20), y)
    STO(PERIOD_M15, (x := x - 20), y)
    STO(PERIOD_M30, (x := x - 20), y)
    STO(PERIOD_H1, (x := x - 20), y)
    STO(PERIOD_H4, (x := x - 20), y)
    STO(PERIOD_D1, (x := x - 20), y)
    STO(PERIOD_W1, (x := x - 20), y)
    STO(PERIOD_MN1, (x := x - 20), y)
    x = 190
    y = y + 12
    RSI(PERIOD_M5, (x := x - 20), y)
    RSI(PERIOD_M15, (x := x - 20), y)
    RSI(PERIOD_M30, (x := x - 20), y)
    RSI(PERIOD_H1, (x := x - 20), y)
    RSI(PERIOD_H4, (x := x - 20), y)
    RSI(PERIOD_D1, (x := x - 20), y)
    RSI(PERIOD_W1, (x := x - 20), y)
    RSI(PERIOD_MN1, (x := x - 20), y)
    x = 190
    y = y + 12
    GuiFooter(PERIOD_M5, (x := x - 20), y)
    return rates_total

def GuiHeader(period, x, y):
    basename = 'TIME'
    name = basename + EnumToString(period, 'ENUM_TIMEFRAMES')
    label = Box(EnumToString(period, 'ENUM_TIMEFRAMES'))
    StringReplace(label, 'PERIOD_', '')
    LabelDelete(0, name)
    LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, label.v, 'Arial', 7, clrYellow, 0.0, ANCHOR_LEFT_UPPER)

def GuiFooter(period, x, y):
    basenameb = 'TOTALB'
    nameb = basenameb + EnumToString(period, 'ENUM_TIMEFRAMES')
    y = y + 12
    LabelDelete(0, nameb)
    LabelCreate(0, nameb, 0, x, y, CORNER_RIGHT_UPPER, _str(b), 'Arial', 7, clrBlue, 0.0, ANCHOR_LEFT_UPPER)
    LabelDelete(0, basenameb)
    LabelCreate(0, basenameb, 0, 225, y, CORNER_RIGHT_UPPER, 'TOTAL(B)', 'Arial', 7, clrAqua, 0.0, ANCHOR_LEFT_UPPER)
    basenames = 'TOTALS'
    names = basenames + EnumToString(period, 'ENUM_TIMEFRAMES')
    y = y + 12
    LabelDelete(0, names)
    LabelCreate(0, names, 0, x, y, CORNER_RIGHT_UPPER, _str(s), 'Arial', 7, clrRed, 0.0, ANCHOR_LEFT_UPPER)
    LabelDelete(0, basenames)
    LabelCreate(0, basenames, 0, 225, y, CORNER_RIGHT_UPPER, 'TOTAL(S)', 'Arial', 7, clrAqua, 0.0, ANCHOR_LEFT_UPPER)
    basenamen = 'TOTALN'
    namen = basenamen + EnumToString(period, 'ENUM_TIMEFRAMES')
    y = y + 12
    LabelDelete(0, namen)
    LabelCreate(0, namen, 0, x, y, CORNER_RIGHT_UPPER, _str(n), 'Arial', 7, clrWhite, 0.0, ANCHOR_LEFT_UPPER)
    LabelDelete(0, basenamen)
    LabelCreate(0, basenamen, 0, 225, y, CORNER_RIGHT_UPPER, 'TOTAL(N)', 'Arial', 7, clrAqua, 0.0, ANCHOR_LEFT_UPPER)

def Price(period, x, y):
    global b, n, s
    basename = 'PRICE'
    name = basename + EnumToString(period, 'ENUM_TIMEFRAMES')
    rates = Arr(2, 0, dyn=False, factory=MqlRates)
    CopyRates(Symbol(), period, 0, 2, rates)
    if rates[0].open < rates[0].close:
        b += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'B', 'Arial', 7, clrBlue, 0.0, ANCHOR_LEFT_UPPER)
    elif rates[0].open > rates[0].close:
        LabelDelete(0, name)
        s += 1
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'S', 'Arial', 7, clrRed, 0.0, ANCHOR_LEFT_UPPER)
    else:
        n += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'N', 'Arial', 7, clrWhite, 0.0, ANCHOR_LEFT_UPPER)
    LabelDelete(0, basename)
    LabelCreate(0, basename, 0, 225, y, CORNER_RIGHT_UPPER, 'PRICE', 'Arial', 7, clrAqua, 0.0, ANCHOR_LEFT_UPPER)

def SMA5(period, x, y):
    global b, n, s
    basename = 'SMA5'
    name = basename + EnumToString(period, 'ENUM_TIMEFRAMES')
    rates = Arr(1, 0, dyn=False, factory=MqlRates)
    CopyRates(Symbol(), period, 0, 1, rates)
    handle = 0
    ma = Arr(1, 0.0, dyn=False)
    handle = iMA(Symbol(), period, 5, 0, MODE_SMA, PRICE_CLOSE)
    CopyBuffer(handle, 0, 0, 1, ma)
    if rates[0].close > ma[0]:
        b += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'B', 'Arial', 7, clrBlue, 0.0, ANCHOR_LEFT_UPPER)
    elif rates[0].close < ma[0]:
        s += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'S', 'Arial', 7, clrRed, 0.0, ANCHOR_LEFT_UPPER)
    else:
        n += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'N', 'Arial', 7, clrWhite, 0.0, ANCHOR_LEFT_UPPER)
    LabelDelete(0, basename)
    LabelCreate(0, basename, 0, 225, y, CORNER_RIGHT_UPPER, 'SMA(5)', 'Arial', 7, clrAqua, 0.0, ANCHOR_LEFT_UPPER)

def SMA10(period, x, y):
    global b, n, s
    basename = 'SMA10'
    name = basename + EnumToString(period, 'ENUM_TIMEFRAMES')
    rates = Arr(1, 0, dyn=False, factory=MqlRates)
    CopyRates(Symbol(), period, 0, 1, rates)
    handle = 0
    ma = Arr(1, 0.0, dyn=False)
    handle = iMA(Symbol(), period, 10, 0, MODE_SMA, PRICE_CLOSE)
    CopyBuffer(handle, 0, 0, 1, ma)
    if rates[0].close > ma[0]:
        b += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'B', 'Arial', 7, clrBlue, 0.0, ANCHOR_LEFT_UPPER)
    elif rates[0].close < ma[0]:
        s += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'S', 'Arial', 7, clrRed, 0.0, ANCHOR_LEFT_UPPER)
    else:
        n += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'N', 'Arial', 7, clrWhite, 0.0, ANCHOR_LEFT_UPPER)
    LabelDelete(0, basename)
    LabelCreate(0, basename, 0, 225, y, CORNER_RIGHT_UPPER, 'SMA(10)', 'Arial', 7, clrAqua, 0.0, ANCHOR_LEFT_UPPER)

def SMA20(period, x, y):
    global b, n, s
    basename = 'SMA20'
    name = basename + EnumToString(period, 'ENUM_TIMEFRAMES')
    rates = Arr(1, 0, dyn=False, factory=MqlRates)
    CopyRates(Symbol(), period, 0, 1, rates)
    handle = 0
    ma = Arr(1, 0.0, dyn=False)
    handle = iMA(Symbol(), period, 20, 0, MODE_SMA, PRICE_CLOSE)
    CopyBuffer(handle, 0, 0, 1, ma)
    if rates[0].close > ma[0]:
        b += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'B', 'Arial', 7, clrBlue, 0.0, ANCHOR_LEFT_UPPER)
    elif rates[0].close < ma[0]:
        s += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'S', 'Arial', 7, clrRed, 0.0, ANCHOR_LEFT_UPPER)
    else:
        n += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'N', 'Arial', 7, clrWhite, 0.0, ANCHOR_LEFT_UPPER)
    LabelDelete(0, basename)
    LabelCreate(0, basename, 0, 225, y, CORNER_RIGHT_UPPER, 'SMA(20)', 'Arial', 7, clrAqua, 0.0, ANCHOR_LEFT_UPPER)

def SMA50(period, x, y):
    global b, n, s
    basename = 'SM50'
    name = basename + EnumToString(period, 'ENUM_TIMEFRAMES')
    rates = Arr(1, 0, dyn=False, factory=MqlRates)
    CopyRates(Symbol(), period, 0, 1, rates)
    handle = 0
    ma = Arr(1, 0.0, dyn=False)
    handle = iMA(Symbol(), period, 50, 0, MODE_SMA, PRICE_CLOSE)
    CopyBuffer(handle, 0, 0, 1, ma)
    if rates[0].close > ma[0]:
        b += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'B', 'Arial', 7, clrBlue, 0.0, ANCHOR_LEFT_UPPER)
    elif rates[0].close < ma[0]:
        s += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'S', 'Arial', 7, clrRed, 0.0, ANCHOR_LEFT_UPPER)
    else:
        n += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'N', 'Arial', 7, clrWhite, 0.0, ANCHOR_LEFT_UPPER)
    LabelDelete(0, basename)
    LabelCreate(0, basename, 0, 225, y, CORNER_RIGHT_UPPER, 'SMA(50)', 'Arial', 7, clrAqua, 0.0, ANCHOR_LEFT_UPPER)

def SMA100(period, x, y):
    global b, n, s
    basename = 'SM100'
    name = basename + EnumToString(period, 'ENUM_TIMEFRAMES')
    rates = Arr(1, 0, dyn=False, factory=MqlRates)
    CopyRates(Symbol(), period, 0, 1, rates)
    handle = 0
    ma = Arr(1, 0.0, dyn=False)
    handle = iMA(Symbol(), period, 100, 0, MODE_SMA, PRICE_CLOSE)
    CopyBuffer(handle, 0, 0, 1, ma)
    if rates[0].close > ma[0]:
        b += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'B', 'Arial', 7, clrBlue, 0.0, ANCHOR_LEFT_UPPER)
    elif rates[0].close < ma[0]:
        s += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'S', 'Arial', 7, clrRed, 0.0, ANCHOR_LEFT_UPPER)
    else:
        n += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'N', 'Arial', 7, clrWhite, 0.0, ANCHOR_LEFT_UPPER)
    LabelDelete(0, basename)
    LabelCreate(0, basename, 0, 225, y, CORNER_RIGHT_UPPER, 'SMA(100)', 'Arial', 7, clrAqua, 0.0, ANCHOR_LEFT_UPPER)

def SMA200(period, x, y):
    global b, n, s
    basename = 'SM5200'
    name = basename + EnumToString(period, 'ENUM_TIMEFRAMES')
    rates = Arr(1, 0, dyn=False, factory=MqlRates)
    CopyRates(Symbol(), period, 0, 1, rates)
    handle = 0
    ma = Arr(1, 0.0, dyn=False)
    handle = iMA(Symbol(), period, 200, 0, MODE_SMA, PRICE_CLOSE)
    CopyBuffer(handle, 0, 0, 1, ma)
    if rates[0].close > ma[0]:
        b += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'B', 'Arial', 7, clrBlue, 0.0, ANCHOR_LEFT_UPPER)
    elif rates[0].close < ma[0]:
        s += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'S', 'Arial', 7, clrRed, 0.0, ANCHOR_LEFT_UPPER)
    else:
        n += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'N', 'Arial', 7, clrWhite, 0.0, ANCHOR_LEFT_UPPER)
    LabelDelete(0, basename)
    LabelCreate(0, basename, 0, 225, y, CORNER_RIGHT_UPPER, 'SMA(200)', 'Arial', 7, clrAqua, 0.0, ANCHOR_LEFT_UPPER)

def STO(period, x, y):
    global b, n, s
    basename = 'STO'
    name = basename + EnumToString(period, 'ENUM_TIMEFRAMES')
    handle = 0
    sto = Arr(1, 0.0, dyn=False)
    handle = iStochastic(Symbol(), period, 14, 3, 3, MODE_SMA, STO_LOWHIGH)
    CopyBuffer(handle, SIGNAL_LINE, 0, 1, sto)
    if sto[0] < 20:
        b += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'B', 'Arial', 7, clrBlue, 0.0, ANCHOR_LEFT_UPPER)
    elif sto[0] > 80:
        s += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'S', 'Arial', 7, clrRed, 0.0, ANCHOR_LEFT_UPPER)
    else:
        n += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'N', 'Arial', 7, clrWhite, 0.0, ANCHOR_LEFT_UPPER)
    LabelDelete(0, basename)
    LabelCreate(0, basename, 0, 225, y, CORNER_RIGHT_UPPER, basename, 'Arial', 7, clrAqua, 0.0, ANCHOR_LEFT_UPPER)

def RSI(period, x, y):
    global b, n, s
    basename = 'RSI'
    name = basename + EnumToString(period, 'ENUM_TIMEFRAMES')
    handle = 0
    rsi = Arr(1, 0.0, dyn=False)
    handle = iRSI(Symbol(), period, 14, PRICE_CLOSE)
    CopyBuffer(handle, SIGNAL_LINE, 0, 1, rsi)
    if rsi[0] < 30:
        b += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'B', 'Arial', 7, clrBlue, 0.0, ANCHOR_LEFT_UPPER)
    elif rsi[0] > 70:
        s += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'S', 'Arial', 7, clrRed, 0.0, ANCHOR_LEFT_UPPER)
    else:
        n += 1
        LabelDelete(0, name)
        LabelCreate(0, name, 0, x, y, CORNER_RIGHT_UPPER, 'N', 'Arial', 7, clrWhite, 0.0, ANCHOR_LEFT_UPPER)
    LabelDelete(0, basename)
    LabelCreate(0, basename, 0, 225, y, CORNER_RIGHT_UPPER, basename, 'Arial', 7, clrAqua, 0.0, ANCHOR_LEFT_UPPER)

def LabelCreate(chart_ID=0, name='Label', sub_window=0, x=0, y=0, corner=CORNER_LEFT_UPPER, text='Label', font='Arial', font_size=10, clr=clrRed, angle=0.0, anchor=ANCHOR_LEFT_UPPER, back=False, selection=False, hidden=True, z_order=0):
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_LABEL, sub_window, 0, 0):
        Print('LabelCreate', ': failed to create text label! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_XDISTANCE, x)
    ObjectSetInteger(chart_ID, name, OBJPROP_YDISTANCE, y)
    ObjectSetInteger(chart_ID, name, OBJPROP_CORNER, corner)
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

def LabelDelete(chart_ID=0, name='Label'):
    ResetLastError()
    if not ObjectDelete(chart_ID, name):
        Print('LabelDelete', ': failed to delete a text label! Error code = ', GetLastError())
        return False
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PYSignal(_MQL5Indicator):
    name = 'PY_Signal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

