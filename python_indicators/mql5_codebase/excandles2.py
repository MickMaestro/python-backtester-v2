"""excandles2 — converted from MQL5: MQL5 Indicators/ExCandles2/excandles2.mq5

Copyright: Copyright © 2006, Alex Sidd (Executer); Link: mailto:work_st@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Alex Sidd (Executer)', 'link': 'mailto:work_st@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'excandles2', 'source': 'MQL5 Indicators/ExCandles2/excandles2.mq5', 'folder': 'ExCandles2', 'inputs': [{'mql': 'ExPeriod', 'py': 'ExPeriod', 'param': 'ExPeriod', 'type': 'int', 'default': 24, 'label': '', 'sinput': False}, {'mql': 'TrendFilter', 'py': 'TrendFilter', 'param': 'TrendFilter', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'how_bars', 'py': 'how_bars', 'param': 'how_bars', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'UpSymbol', 'py': 'UpSymbol', 'param': 'UpSymbol', 'type': 'int', 'default': 233, 'label': '', 'sinput': False}, {'mql': 'DnSymbol', 'py': 'DnSymbol', 'param': 'DnSymbol', 'type': 'int', 'default': 234, 'label': '', 'sinput': False}, {'mql': 'VertShift', 'py': 'VertShift', 'param': 'VertShift', 'type': 'int', 'default': 100, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Blue = 0xFF0000  # MQL4 colour name
DeepPink = 0x9314FF  # MQL4 colour name
DodgerBlue = 0xFF901E  # MQL4 colour name
Maroon = 0x000080  # MQL4 colour name
OrangeRed = 0x0045FF  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name
RoyalBlue = 0xE16941  # MQL4 colour name
SlateBlue = 0xCD5A6A  # MQL4 colour name

# ---- inputs and global variables
ExPeriod = _input('ExPeriod', 24)
TrendFilter = _input('TrendFilter', True)
how_bars = _input('how_bars', 0)
UpSymbol = _input('UpSymbol', 233)
DnSymbol = _input('DnSymbol', 234)
VertShift = _input('VertShift', 100)
CCodeBuffer = Arr(0, 0.0)
dVertShift = 0.0
min_rates_total = 0

def CreateSymbol(chart_id, name, nwin, time, price, Color, style, width, symbol, text):
    ObjectCreate(chart_id, name, OBJ_ARROW, nwin, time, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chart_id, name, OBJPROP_ARROWCODE, symbol)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetSymbol(chart_id, name, nwin, time, price, Color, style, width, symbol, text):
    if ObjectFind(chart_id, name) == -1:
        CreateSymbol(chart_id, name, nwin, time, price, Color, style, width, symbol, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time, price)

def Trend(rates_total, Open, Close, i):
    negative = 0.0
    positive = 0.0
    if i < (rates_total - ExPeriod - 1):
        k = i + ExPeriod
        while k > i:
            if Open[k] < Close[k]:
                positive += Close[k] - Open[k]
            if Open[k] > Close[k]:
                negative += Open[k] - Close[k]
            k -= 1
    else:
        return 0
    if (positive - negative) > 0:
        return 1
    if (positive - negative) < 0:
        return -1
    if positive == negative:
        return 0
    return 0

def IsHangingMan(rates_total, Open, High, Low, Close, i1):
    buf = Open[i1] - Close[i1]
    if buf == 0:
        buf = 1.0
    if (((TrendFilter == True and Trend(rates_total, Open, Close, i1) > 0) and _fdiv((High[i1] - Open[i1]) * 100, buf) < 20) and _fdiv((Close[i1] - Low[i1]) * 100, buf) > 180) or ((TrendFilter == False and _fdiv((High[i1] - Open[i1]) * 100, buf) < 20) and _fdiv((Close[i1] - Low[i1]) * 100, buf) > 180):
        return True
    else:
        return False
    return False

def IsHammer(rates_total, Open, High, Low, Close, i1):
    buf = Close[i1] - Open[i1]
    if buf == 0:
        buf = 1.0
    if (((TrendFilter == True and Trend(rates_total, Open, Close, i1) < 0) and _fdiv((High[i1] - Close[i1]) * 100, buf) > 180) and _fdiv((Open[i1] - Low[i1]) * 100, buf) < 20) or ((TrendFilter == False and _fdiv((High[i1] - Close[i1]) * 100, buf) > 180) and _fdiv((Open[i1] - Low[i1]) * 100, buf) < 20):
        return True
    else:
        return False
    return False

def IsBearishEngulfing(rates_total, Open, Close, i1, i2):
    if (((((TrendFilter == True and Trend(rates_total, Open, Close, i1) > 0) and (Open[i1] - Close[i1]) > 0) and Open[i1] > Close[i2]) and Close[i1] < Open[i2]) and (Open[i2] - Close[i2]) < 0) or ((((TrendFilter == (False > 0) and (Open[i1] - Close[i1]) > 0) and Open[i1] > Close[i2]) and Close[i1] < Open[i2]) and (Open[i2] - Close[i2]) < 0):
        return True
    else:
        return False
    return False

def IsBullishEngulfing(rates_total, Open, Close, i1, i2):
    if (((((TrendFilter == True and Trend(rates_total, Open, Close, i1) < 0) and (Open[i1] - Close[i1]) < 0) and (Open[i2] - Close[i2]) > 0) and Close[i1] > Open[i2]) and Open[i1] < Close[i2]) or ((((TrendFilter == False and (Open[i1] - Close[i1]) < 0) and (Open[i2] - Close[i2]) > 0) and Close[i1] > Open[i2]) and Open[i1] < Close[i2]):
        return True
    else:
        return False
    return False

def DarkCloud_Cover(rates_total, Open, High, Low, Close, i1, i2):
    x = High[i2] - Low[i2]
    if x == 0:
        x = 0.0001
    if ((((((TrendFilter == True and Trend(rates_total, Open, Close, i1) > 0) and (Open[i1] - Close[i1]) > 0) and (Open[i2] - Close[i2]) < 0) and _fdiv(Close[i2] - Open[i2], x) > 0.6) and Open[i1] > High[i2]) and Close[i1] < (Open[i2] + ((Close[i2] - Open[i2]) / 2))) or (((((TrendFilter == False and (Open[i1] - Close[i1]) > 0) and (Open[i2] - Close[i2]) < 0) and _fdiv(Close[i2] - Open[i2], x) > 0.6) and Open[i1] > High[i2]) and Close[i1] < (Open[i2] + ((Close[i2] - Open[i2]) / 2))):
        return True
    else:
        return False
    return False

def PiercingLine(rates_total, Open, High, Low, Close, i1, i2):
    x = High[i2] - Low[i2]
    if x == 0:
        x = 0.0001
    if ((((((TrendFilter == True and Trend(rates_total, Open, Close, i1) < 0) and (Open[i1] - Close[i1]) < 0) and (Open[i2] - Close[i2]) > 0) and _fdiv(Open[i2] - Close[i2], x) > 0.6) and Open[i1] < Low[i2]) and Close[i1] > (Close[i2] + ((Open[i2] - Close[i2]) / 2))) or (((((TrendFilter == False and (Open[i1] - Close[i1]) < 0) and (Open[i2] - Close[i2]) > 0) and _fdiv(Open[i2] - Close[i2], x) > 0.6) and Open[i1] < Low[i2]) and Close[i1] > (Close[i2] + ((Open[i2] - Close[i2]) / 2))):
        return True
    else:
        return False
    return False

def Morning_Star(rates_total, Open, Close, i1, i2, i3):
    if (((((((((((TrendFilter == True and Trend(rates_total, Open, Close, i1) < 0) and (Open[i3] - Close[i3]) > 0) and (Open[i1] - Close[i1]) < 0) and Close[i2] < Open[i3]) and Close[i2] < Open[i1]) and Close[i2] < Close[i1]) and Close[i2] < Close[i3]) and Open[i2] < Open[i1]) and Open[i2] < Open[i3]) and Open[i2] < Close[i3]) and Open[i2] < Close[i1]) or ((((((((((TrendFilter == False and (Open[i3] - Close[i3]) > 0) and (Open[i1] - Close[i1]) < 0) and Close[i2] < Open[i3]) and Close[i2] < Open[i1]) and Close[i2] < Close[i1]) and Close[i2] < Close[i3]) and Open[i2] < Open[i1]) and Open[i2] < Open[i3]) and Open[i2] < Close[i3]) and Open[i2] < Close[i1]):
        return True
    else:
        return False
    return False

def Evening_Star(rates_total, Open, Close, i1, i2, i3):
    if (((((((((((TrendFilter == True and Trend(rates_total, Open, Close, i1) > 0) and (Open[i3] - Close[i3]) < 0) and (Open[i1] - Close[i1]) > 0) and Close[i2] > Open[i3]) and Close[i2] > Open[i1]) and Close[i2] > Close[i1]) and Close[i2] > Close[i3]) and Open[i2] > Open[i1]) and Open[i2] > Open[i3]) and Open[i2] > Close[i3]) and Open[i2] > Close[i1]) or ((((((((((TrendFilter == False and (Open[i3] - Close[i3]) < 0) and (Open[i1] - Close[i1]) > 0) and Close[i2] > Open[i3]) and Close[i2] > Open[i1]) and Close[i2] > Close[i1]) and Close[i2] > Close[i3]) and Open[i2] > Open[i1]) and Open[i2] > Open[i3]) and Open[i2] > Close[i3]) and Open[i2] > Close[i1]):
        return True
    else:
        return False
    return False

def IsEveningDojiStar(rates_total, Open, Close, i1, i2, i3):
    if ((((((((((((TrendFilter == True and Trend(rates_total, Open, Close, i1) > 0) and Open[i2] == Close[i2]) and (Open[i3] - Close[i3]) < 0) and (Open[i1] - Close[i1]) > 0) and Close[i2] > Open[i3]) and Close[i2] > Open[i1]) and Close[i2] > Close[i1]) and Close[i2] > Close[i3]) and Open[i2] > Open[i1]) and Open[i2] > Open[i3]) and Open[i2] > Close[i3]) and Open[i2] > Close[i1]) or (((((((((((TrendFilter == False and Open[i2] == Close[i2]) and (Open[i3] - Close[i3]) < 0) and (Open[i1] - Close[i1]) > 0) and Close[i2] > Open[i3]) and Close[i2] > Open[i1]) and Close[i2] > Close[i1]) and Close[i2] > Close[i3]) and Open[i2] > Open[i1]) and Open[i2] > Open[i3]) and Open[i2] > Close[i3]) and Open[i2] > Close[i1]):
        return True
    else:
        return False
    return False

def IsMorningDojiStar(rates_total, Open, Close, i1, i2, i3):
    if ((((((((((((TrendFilter == True and Trend(rates_total, Open, Close, i1) < 0) and Open[i2] == Close[i2]) and (Open[i3] - Close[i3]) > 0) and (Open[i1] - Close[i1]) < 0) and Close[i2] < Open[i3]) and Close[i2] < Open[i1]) and Close[i2] < Close[i1]) and Close[i2] < Close[i3]) and Open[i2] < Open[i1]) and Open[i2] < Open[i3]) and Open[i2] < Close[i3]) and Open[i2] < Close[i1]) or (((((((((((TrendFilter == False and Open[i2] == Close[i2]) and (Open[i3] - Close[i3]) > 0) and (Open[i1] - Close[i1]) < 0) and Close[i2] < Open[i3]) and Close[i2] < Open[i1]) and Close[i2] < Close[i1]) and Close[i2] < Close[i3]) and Open[i2] < Open[i1]) and Open[i2] < Open[i3]) and Open[i2] < Close[i3]) and Open[i2] < Close[i1]):
        return True
    else:
        return False
    return False

def IsShootingStar(rates_total, Open, High, Low, Close, i1):
    buf = Open[i1] - Close[i1]
    if buf == 0:
        buf = 1.0
    if (((TrendFilter == True and Trend(rates_total, Open, Close, i1) > 0) and _fdiv((High[i1] - Open[i1]) * 100, buf) > 180) and _fdiv((Close[i1] - Low[i1]) * 100, buf) < 20) or ((TrendFilter == False and _fdiv((High[i1] - Open[i1]) * 100, buf) > 180) and _fdiv((Close[i1] - Low[i1]) * 100, buf) < 20):
        return True
    else:
        return False
    return False

def IsInvertedHammer(rates_total, Open, High, Low, Close, i1):
    buf = Close[i1] - Open[i1]
    if buf == 0:
        buf = 1.0
    if (((TrendFilter == True and Trend(rates_total, Open, Close, i1) < 0) and _fdiv((High[i1] - Close[i1]) * 100, buf) < 20) and _fdiv((Open[i1] - Low[i1]) * 100, buf) > 180) or ((TrendFilter == False and _fdiv((High[i1] - Close[i1]) * 100, buf) < 20) and _fdiv((Open[i1] - Low[i1]) * 100, buf) > 180):
        return True
    else:
        return False
    return False

def OnDeinit(reason):
    ObjectsDeleteAll(0, 0, OBJ_ARROW)

def OnInit():
    global dVertShift, min_rates_total
    min_rates_total = ExPeriod
    dVertShift = VertShift * Point()
    SetIndexBuffer(0, CCodeBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(CCodeBuffer, True)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    name = ""
    negative = 0.0
    positive = 0.0
    i = 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        if how_bars <= 0 or how_bars > rates_total:
            limit = rates_total - min_rates_total - 1
        else:
            limit = how_bars
    else:
        limit = rates_total - prev_calculated
    i = limit
    for i in range(i, 0 - 1, -1):
        if IsShootingStar(rates_total, open, high, low, close, i + 1):
            name = 'Shooting star ' + _str(i)
            SetSymbol(0, name, 0, time[i + 1], high[i + 1] + dVertShift, _uint(Red), STYLE_SOLID, 3, DnSymbol, name)
            CCodeBuffer[i] = 1.0
        if IsInvertedHammer(rates_total, open, high, low, close, i + 1):
            name = 'Inverted hammer ' + _str(i)
            SetSymbol(0, name, 0, time[i + 1], low[i + 1] - dVertShift, _uint(Blue), STYLE_SOLID, 3, UpSymbol, name)
            CCodeBuffer[i] = 2.0
        if IsHangingMan(rates_total, open, high, low, close, i + 1):
            name = 'Hangman ' + _str(i)
            SetSymbol(0, name, 0, time[i + 1], high[i + 1] + dVertShift, _uint(Red), STYLE_SOLID, 3, DnSymbol, name)
            CCodeBuffer[i] = 3.0
        if IsHammer(rates_total, open, high, low, close, i + 1):
            name = 'Hammer ' + _str(i)
            SetSymbol(0, name, 0, time[i + 1], low[i + 1] - dVertShift, _uint(Blue), STYLE_SOLID, 3, UpSymbol, name)
            CCodeBuffer[i] = 4.0
        if IsBearishEngulfing(rates_total, open, close, i + 1, i + 2):
            name = 'Bearish engulfing ' + _str(i)
            SetSymbol(0, name, 0, time[i + 1], high[i + 1] + dVertShift, _uint(Maroon), STYLE_SOLID, 3, DnSymbol, name)
            CCodeBuffer[i] = 5.0
        if IsBullishEngulfing(rates_total, open, close, i + 1, i + 2):
            name = 'Bullish engulfing ' + _str(i)
            SetSymbol(0, name, 0, time[i + 1], low[i + 1] - dVertShift, _uint(RoyalBlue), STYLE_SOLID, 3, UpSymbol, name)
            CCodeBuffer[i] = 6.0
        if DarkCloud_Cover(rates_total, open, high, low, close, i + 1, i + 2):
            name = 'Dark cloud cover ' + _str(i)
            SetSymbol(0, name, 0, time[i], high[i] + dVertShift, _uint(OrangeRed), STYLE_SOLID, 3, DnSymbol, name)
            CCodeBuffer[i] = 7.0
        if PiercingLine(rates_total, open, high, low, close, i + 1, i + 2):
            name = 'Piercing line pattern ' + _str(i)
            SetSymbol(0, name, 0, time[i], low[i] - dVertShift, _uint(SlateBlue), STYLE_SOLID, 3, UpSymbol, name)
            CCodeBuffer[i] = 8.0
        if Evening_Star(rates_total, open, close, i + 1, i + 2, i + 3):
            name = 'Evening star ' + _str(i)
            SetSymbol(0, name, 0, time[i + 2], high[i + 2] + dVertShift, _uint(Red), STYLE_SOLID, 3, DnSymbol, name)
            CCodeBuffer[i] = 9.0
        if Morning_Star(rates_total, open, close, i + 1, i + 2, i + 3):
            name = 'Morning star ' + _str(i)
            SetSymbol(0, name, 0, time[i + 2], low[i + 2] - dVertShift, _uint(DodgerBlue), STYLE_SOLID, 3, UpSymbol, name)
            CCodeBuffer[i] = 10.0
        if IsEveningDojiStar(rates_total, open, close, i + 1, i + 2, i + 3):
            name = 'Evening doji star ' + _str(i)
            SetSymbol(0, name, 0, time[i + 2], high[i + 2] + dVertShift, _uint(DeepPink), STYLE_SOLID, 3, DnSymbol, name)
            CCodeBuffer[i] = 11.0
        if IsMorningDojiStar(rates_total, open, close, i + 1, i + 2, i + 3):
            name = 'Morning doji star ' + _str(i)
            SetSymbol(0, name, 0, time[i + 2], low[i + 2] - dVertShift, _uint(Blue), STYLE_SOLID, 3, UpSymbol, name)
            CCodeBuffer[i] = 12.0
    else:
        i = _range_end(i, 0 - 1, -1)
    ChartRedraw(0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Excandles2(_MQL5Indicator):
    name = 'excandles2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ExPeriod': 24,
        'TrendFilter': True,
        'how_bars': 0,
        'UpSymbol': 233,
        'DnSymbol': 234,
        'VertShift': 100,
    }

