"""Point-and-Figure — converted from MQL5: MQL5 Indicators/Point and Figure Indicator for MetaTrader 5/Point-and-Figure.mq5

Point-and-Figure is a basic point-and-figure charting indicator based on real ticks data.
It supports full customization and all types of alerts.
Copyright: Copyright © 2025; Link: https://t.me/ForexEaPremium; Version: 2.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2025', 'link': 'https://t.me/ForexEaPremium', 'version': '2.01', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Point-and-Figure is a basic point-and-figure charting indicator based on real ticks data.', 'It supports full customization and all types of alerts.'], 'name': 'Point-and-Figure', 'source': 'MQL5 Indicators/Point and Figure Indicator for MetaTrader 5/Point-and-Figure.mq5', 'folder': 'Point and Figure Indicator for MetaTrader 5', 'inputs': [{'mql': 'BoxSize', 'py': 'BoxSize', 'param': 'BoxSize', 'type': 'int', 'default': 60, 'label': 'Box size, points', 'sinput': False}, {'mql': 'Reversal', 'py': 'Reversal', 'param': 'Reversal', 'type': 'int', 'default': 3, 'label': 'Number of boxes for reversal', 'sinput': False}, {'mql': 'Days', 'py': 'Days', 'param': 'Days', 'type': 'int', 'default': 1, 'label': 'Days to look back.', 'sinput': False}, {'mql': 'PriceToUse', 'py': 'PriceToUse', 'param': 'PriceToUse', 'type': 'int', 'default': 0, 'label': 'Price to use', 'sinput': False}, {'mql': 'AlertOnXO', 'py': 'AlertOnXO', 'param': 'AlertOnXO', 'type': 'bool', 'default': False, 'label': 'Alert on new X/O', 'sinput': False}, {'mql': 'AlertOnReversal', 'py': 'AlertOnReversal', 'param': 'AlertOnReversal', 'type': 'bool', 'default': False, 'label': 'Alert on reversal', 'sinput': False}, {'mql': 'EnableNativeAlerts', 'py': 'EnableNativeAlerts', 'param': 'EnableNativeAlerts', 'type': 'bool', 'default': False, 'label': 'Enable native alerts', 'sinput': False}, {'mql': 'EnableEmailAlerts', 'py': 'EnableEmailAlerts', 'param': 'EnableEmailAlerts', 'type': 'bool', 'default': False, 'label': 'Enable email alerts', 'sinput': False}, {'mql': 'EnablePushAlerts', 'py': 'EnablePushAlerts', 'param': 'EnablePushAlerts', 'type': 'bool', 'default': False, 'label': 'Enable push-notification alerts', 'sinput': False}, {'mql': 'ColorUp', 'py': 'ColorUp', 'param': None, 'type': 'color', 'default': 32768, 'label': 'X Color', 'sinput': False}, {'mql': 'ColorDown', 'py': 'ColorDown', 'param': None, 'type': 'color', 'default': 255, 'label': 'O Color', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 15, 'label': 'Font size', 'sinput': False}, {'mql': 'Font', 'py': 'Font', 'param': None, 'type': 'string', 'default': 'Arial', 'label': 'Font', 'sinput': False}, {'mql': 'X', 'py': 'X', 'param': None, 'type': 'string', 'default': 'x', 'label': 'Up Symbol', 'sinput': False}, {'mql': 'O', 'py': 'O', 'param': None, 'type': 'string', 'default': 'o', 'label': 'Down Symbol', 'sinput': False}, {'mql': 'SilentMode', 'py': 'SilentMode', 'param': 'SilentMode', 'type': 'bool', 'default': True, 'label': "Don't print information about each X/O", 'sinput': False}, {'mql': 'MaxObjects', 'py': 'MaxObjects', 'param': 'MaxObjects', 'type': 'int', 'default': 10000, 'label': 'Maximum allowed number of X/O chart objects', 'sinput': False}, {'mql': 'ObjectPrefix', 'py': 'ObjectPrefix', 'param': None, 'type': 'string', 'default': 'PNF-', 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

COPY_TICKS_ALL = 0  # MQL5 constant unknown to the converter

# enum enum_price
Bid = 0
Ask = 1
Midprice = 2
BidAsk = 3
_enum('enum_price', {0: 'Bid', 1: 'Ask', 2: 'Midprice', 3: 'BidAsk'})

# ---- inputs and global variables
BoxSize = _input('BoxSize', 60)  # Box size, points
Reversal = _input('Reversal', 3)  # Number of boxes for reversal
Days = _input('Days', 1)  # Days to look back.
PriceToUse = _input('PriceToUse', Bid)  # Price to use
AlertOnXO = _input('AlertOnXO', False)  # Alert on new X/O
AlertOnReversal = _input('AlertOnReversal', False)  # Alert on reversal
EnableNativeAlerts = _input('EnableNativeAlerts', False)  # Enable native alerts
EnableEmailAlerts = _input('EnableEmailAlerts', False)  # Enable email alerts
EnablePushAlerts = _input('EnablePushAlerts', False)  # Enable push-notification alerts
ColorUp = _input('ColorUp', clrGreen)  # X Color
ColorDown = _input('ColorDown', clrRed)  # O Color
FontSize = _input('FontSize', 15)  # Font size
Font = _input('Font', 'Arial')  # Font
X = _input('X', 'x')  # Up Symbol
O = _input('O', 'o')  # Down Symbol
SilentMode = _input('SilentMode', True)  # Don't print information about each X/O
MaxObjects = _input('MaxObjects', 10000)  # Maximum allowed number of X/O chart objects
ObjectPrefix = _input('ObjectPrefix', 'PNF-')
cBoxSize = 0.0
cReversal = 0.0
LastPrice = 0.0  # Stores last price where a box was drawn.
CurrentDirection = 0.0
FirstBoxUp = 0.0
FirstBoxDown = 0.0
LastEndTime_msc = 0
Number = 0  # Number of objects.
LastBars = 0  # Number of bars.
LastBarTime = 0  # To check if it were some old bars downloading or new ones.

def OnInit():
    global CurrentDirection, FirstBoxDown, FirstBoxUp, LastBarTime, LastBars, LastEndTime_msc, LastPrice, Number, cBoxSize, cReversal
    Number = 0
    LastBars = 0
    LastPrice = 0.0
    CurrentDirection = 0.0
    FirstBoxUp = 0.0
    FirstBoxDown = 0.0
    LastEndTime_msc = 0
    LastBarTime = 0
    cBoxSize = BoxSize * Point()
    cReversal = Reversal * cBoxSize
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(ChartID(), ObjectPrefix)
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, tick_volume, volume, spread):
    global FirstBoxDown, FirstBoxUp, LastEndTime_msc, LastPrice
    if iBarShift(Symbol(), Period(), iTime(Symbol(), Period(), 0), True) < 0:
        Print('Syncing...')
        return prev_calculated
    if Number > 0:
        if Number > MaxObjects:
            Print('Warning: Too many X/O objects!')
        pt = _int(ObjectGetInteger(ChartID(), ObjectPrefix + IntegerToString(Number - 1), OBJPROP_TIME, 0))
        bar = iBarShift(Symbol(), Period(), pt, True)
        if bar < 0:
            Print('Syncing...')
            return prev_calculated
        if bar > 0:
            Print('Moving all objects ', bar, ' times.')
            while bar > 0:
                if not MoveAllRight():
                    return prev_calculated
                bar -= 1
    ticks_array = Arr(0, 0, factory=MqlTick)
    end_time_seconds = _int(TimeCurrent())
    begin_time_msc = 0
    if LastEndTime_msc == 0:
        begin_time_msc = _ulong(end_time_seconds - (Days * 24 * 3600)) * 1000
        if _idiv(begin_time_msc, 1000) < _ulong(Time[0]):
            Print('Requested Days go beyond the available chart data. Either reduce Days or load more bars.')
            return prev_calculated
    else:
        begin_time_msc = LastEndTime_msc + 1
    n = _int(CopyTicksRange(Symbol(), ticks_array, COPY_TICKS_ALL, begin_time_msc, _ulong(end_time_seconds) * 1000))
    if n < 0:
        Print('Waiting for ticks... ')
        return prev_calculated
    elif n == 0:
        return rates_total
    else:
        LastEndTime_msc = ticks_array[n - 1].time_msc
    for i in range(0, n):
        Price = 0.0
        B = 0.0
        A = 0.0
        _sw1 = PriceToUse
        if _sw1 == Bid:
            Price = ticks_array[i].bid
        elif _sw1 == Ask:
            Price = ticks_array[i].ask
        elif _sw1 == Midprice:
            Price = (ticks_array[i].bid + ticks_array[i].ask) / 2
        elif _sw1 == BidAsk:
            B = ticks_array[i].bid
            A = ticks_array[i].ask
        else:
            Price = 0.0
            A = 0.0
            B = 0.0
        if CurrentDirection == 0:
            if PriceToUse == BidAsk:
                Price = B
            if Price >= FirstBoxUp and FirstBoxUp != 0:
                LastPrice = FirstBoxUp
                while LastPrice <= Price:
                    DrawX(LastPrice)
                    if AlertOnXO and (TimeCurrent() - ticks_array[i].time) <= 5:
                        DoAlerts('X')
                    LastPrice = NormalizeDouble(LastPrice + cBoxSize, Digits())
            else:
                if PriceToUse == BidAsk:
                    Price = A
                if Price <= FirstBoxDown and FirstBoxDown != 0:
                    LastPrice = FirstBoxDown
                    while LastPrice >= Price:
                        DrawO(LastPrice)
                        if AlertOnXO and (TimeCurrent() - ticks_array[i].time) <= 5:
                            DoAlerts('O')
                        LastPrice = NormalizeDouble(LastPrice - cBoxSize, Digits())
            if FirstBoxUp == 0:
                if PriceToUse == BidAsk:
                    Price = B
                FirstBoxUp = NormalizeDouble(MathCeil(_fdiv(Price, cBoxSize)) * cBoxSize, Digits())
            if FirstBoxDown == 0:
                if PriceToUse == BidAsk:
                    Price = A
                FirstBoxDown = NormalizeDouble(MathFloor(_fdiv(Price, cBoxSize)) * cBoxSize, Digits())
        elif CurrentDirection == 1:
            if PriceToUse == BidAsk:
                Price = B
            while Price >= LastPrice:
                DrawX(LastPrice)
                if AlertOnXO and (TimeCurrent() - ticks_array[i].time) <= 5:
                    DoAlerts('X')
                LastPrice = NormalizeDouble(LastPrice + cBoxSize, Digits())
            if Price <= (LastPrice - cBoxSize - cReversal):
                if AlertOnReversal and (TimeCurrent() - ticks_array[i].time) <= 5:
                    DoAlerts('X->O Reversal')
                LastPrice = NormalizeDouble(LastPrice - (2 * cBoxSize), Digits())
                while Price <= LastPrice:
                    DrawO(LastPrice)
                    LastPrice = NormalizeDouble(LastPrice - cBoxSize, Digits())
        elif CurrentDirection == -1:
            if PriceToUse == BidAsk:
                Price = A
            while Price <= LastPrice:
                DrawO(LastPrice)
                if AlertOnXO and (TimeCurrent() - ticks_array[i].time) <= 5:
                    DoAlerts('O')
                LastPrice = NormalizeDouble(LastPrice - cBoxSize, Digits())
            if Price >= (LastPrice + cBoxSize + cReversal):
                if AlertOnReversal and (TimeCurrent() - ticks_array[i].time) <= 5:
                    DoAlerts('O->X Reversal')
                LastPrice = NormalizeDouble(LastPrice + (cBoxSize * 2), Digits())
                while Price >= LastPrice:
                    DrawX(LastPrice)
                    LastPrice = NormalizeDouble(LastPrice + cBoxSize, Digits())
        if Number > MaxObjects:
            break
    return rates_total

def DrawX(price):
    global CurrentDirection, Number
    if CurrentDirection == -1:
        MoveAllLeft()
    ObjectCreate(ChartID(), ObjectPrefix + IntegerToString(Number), OBJ_TEXT, 0, iTime(Symbol(), Period(), 0), price)
    ObjectSetString(ChartID(), ObjectPrefix + IntegerToString(Number), OBJPROP_TEXT, X)
    ObjectSetInteger(ChartID(), ObjectPrefix + IntegerToString(Number), OBJPROP_FONTSIZE, FontSize)
    ObjectSetString(ChartID(), ObjectPrefix + IntegerToString(Number), OBJPROP_FONT, Font)
    ObjectSetInteger(ChartID(), ObjectPrefix + IntegerToString(Number), OBJPROP_COLOR, ColorUp)
    Number += 1
    CurrentDirection = 1.0
    if not SilentMode:
        Print('X: ', price)

def DrawO(price):
    global CurrentDirection, Number
    if CurrentDirection == 1:
        MoveAllLeft()
    ObjectCreate(ChartID(), ObjectPrefix + IntegerToString(Number), OBJ_TEXT, 0, iTime(Symbol(), Period(), 0), price)
    ObjectSetString(ChartID(), ObjectPrefix + IntegerToString(Number), OBJPROP_TEXT, O)
    ObjectSetInteger(ChartID(), ObjectPrefix + IntegerToString(Number), OBJPROP_FONTSIZE, FontSize)
    ObjectSetString(ChartID(), ObjectPrefix + IntegerToString(Number), OBJPROP_FONT, Font)
    ObjectSetInteger(ChartID(), ObjectPrefix + IntegerToString(Number), OBJPROP_COLOR, ColorDown)
    Number += 1
    CurrentDirection = -1.0
    if not SilentMode:
        Print('O: ', price)

def MoveAllRight():
    if not SilentMode:
        Print('Moving all X/O to the right...')
    for i in range(0, Number):
        pt = _int(ObjectGetInteger(ChartID(), ObjectPrefix + IntegerToString(i), OBJPROP_TIME, 0))
        bar = iBarShift(Symbol(), Period(), pt, True)
        if bar > 0:
            bar -= 1
        elif bar == 0:
            Print("Can't move right!")
        elif bar < 0:
            Print('iBarShift error! ', 'MoveAllRight', ' ', pt)
            return False
        pt = iTime(Symbol(), Period(), bar)
        ObjectSetInteger(ChartID(), ObjectPrefix + IntegerToString(i), OBJPROP_TIME, 0, _int(pt))
    return True

def MoveAllLeft():
    if not SilentMode:
        Print('Moving all X/O to the left...')
    max_bar = iBars(Symbol(), Period()) - 1
    for i in range(0, Number):
        pt = ObjectGetInteger(ChartID(), ObjectPrefix + IntegerToString(i), OBJPROP_TIME, 0)
        bar = iBarShift(Symbol(), Period(), pt, True)
        if bar == -1:
            Print('iBarShift error! ', 'MoveAllLeft', ' ', pt)
            return
        elif bar < max_bar:
            bar += 1
        else:
            Print('Failed to increment the bar value: bar ', bar, ' >= ', max_bar)
            return
        pt = iTime(Symbol(), Period(), bar)
        if pt == 0:
            Print(bar)
        ObjectSetInteger(ChartID(), ObjectPrefix + IntegerToString(i), OBJPROP_TIME, 0, _int(pt))

def DoAlerts(text):
    Text = ""
    TextNative = ""
    Text = 'Point-and-Figure: ' + Symbol() + ' - ' + text + ' @ ' + DoubleToString(LastPrice, Digits())
    TextNative = text + ' @ ' + DoubleToString(LastPrice, Digits())
    if EnableNativeAlerts:
        Alert(TextNative)
    if EnableEmailAlerts:
        SendMail('Point-and-Figure Alert', Text)
    if EnablePushAlerts:
        SendNotification(Text)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PointAndFigure(_MQL5Indicator):
    name = 'Point-and-Figure'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BoxSize': 60,  # Box size, points
        'Reversal': 3,  # Number of boxes for reversal
        'Days': 1,  # Days to look back.
        'PriceToUse': _Choice({0: 'Bid', 1: 'Ask', 2: 'Midprice', 3: 'Bid/Ask'}, default=0),  # Price to use
        'AlertOnXO': False,  # Alert on new X/O
        'AlertOnReversal': False,  # Alert on reversal
        'EnableNativeAlerts': False,  # Enable native alerts
        'EnableEmailAlerts': False,  # Enable email alerts
        'EnablePushAlerts': False,  # Enable push-notification alerts
        'FontSize': 15,  # Font size
        'SilentMode': True,  # Don't print information about each X/O
        'MaxObjects': 10000,  # Maximum allowed number of X/O chart objects
    }

