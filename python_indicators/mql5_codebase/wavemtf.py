"""WaveMTF — converted from MQL5: MQL5 Indicators/WaveMTF MT5/WaveMTF.mq5

Indicator WaveMTF Bull and Bear System with Signal and Alert
for MetaTrader 5 with options to display signal on the chart.
version: 2.00 ~ Last update 27/08/2020
Copyright: Copyright 2020, Roberto Jacobs (3rjfx) ~ By 3rjfx ~ Created: 2020/06/10; Link: https://www.mql5.com/en/users/3rjfx; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Roberto Jacobs (3rjfx) ~ By 3rjfx ~ Created: 2020/06/10', 'link': 'https://www.mql5.com/en/users/3rjfx', 'version': '2.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 0, 2: 0}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Indicator WaveMTF Bull and Bear System with Signal and Alert', 'for MetaTrader 5 with options to display signal on the chart.', 'version: 2.00 ~ Last update 27/08/2020'], 'name': 'WaveMTF', 'source': 'MQL5 Indicators/WaveMTF MT5/WaveMTF.mq5', 'folder': 'WaveMTF MT5', 'inputs': [{'mql': 'stf', 'py': 'stf', 'param': 'stf', 'type': 'int', 'default': 1, 'label': 'Time Frames Calculation Signal Starts', 'sinput': False}, {'mql': 'etf', 'py': 'etf', 'param': 'etf', 'type': 'int', 'default': 6, 'label': 'Last Time Frames Calculation Signal', 'sinput': False}, {'mql': 'cor', 'py': 'cor', 'param': 'cor', 'type': 'int', 'default': 0, 'label': 'Arrow Move Position', 'sinput': False}, {'mql': 'alerts', 'py': 'alerts', 'param': 'alerts', 'type': 'int', 'default': 1, 'label': 'Display Alerts / Messages (Yes) or (No)', 'sinput': False}, {'mql': 'EmailAlert', 'py': 'EmailAlert', 'param': 'EmailAlert', 'type': 'int', 'default': 0, 'label': 'Email Alert (Yes) or (No)', 'sinput': False}, {'mql': 'sendnotify', 'py': 'sendnotify', 'param': 'sendnotify', 'type': 'int', 'default': 0, 'label': 'Send Notification (Yes) or (No)', 'sinput': False}, {'mql': 'displayinfo', 'py': 'displayinfo', 'param': 'displayinfo', 'type': 'int', 'default': 1, 'label': 'Display Trade Info', 'sinput': False}, {'mql': 'textcolor', 'py': 'textcolor', 'param': None, 'type': 'color', 'default': 16448255, 'label': 'Text Color', 'sinput': False}, {'mql': 'ArrowUp', 'py': 'ArrowUp', 'param': None, 'type': 'color', 'default': 65280, 'label': 'Arrow Up Color', 'sinput': False}, {'mql': 'ArrowDn', 'py': 'ArrowDn', 'param': None, 'type': 'color', 'default': 255, 'label': 'Arrow Down Color', 'sinput': False}, {'mql': 'NTArrow', 'py': 'NTArrow', 'param': None, 'type': 'color', 'default': 65535, 'label': 'Arrow No Signal', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum YN
No = 0
Yes = 1
_enum('YN', {0: 'No', 1: 'Yes'})

# enum corner
NotShow = -1
topchart = 0
bottomchart = 1
_enum('corner', {-1: 'NotShow', 0: 'topchart', 1: 'bottomchart'})

# enum StrTF
M1 = 0
M5 = 1
M15 = 2
M30 = 3
H1 = 4
H4 = 5
D1 = 6
W1 = 7
MN = 8
_enum('StrTF', {0: 'M1', 1: 'M5', 2: 'M15', 3: 'M30', 4: 'H1', 5: 'H4', 6: 'D1', 7: 'W1', 8: 'MN'})

# enum TimeReturn
year = 0
mon = 1
day = 2
hour = 3
min_ = 4
sec = 5
day_of_week = 6
day_of_year = 7
_enum('TimeReturn', {0: 'year', 1: 'mon', 2: 'day', 3: 'hour', 4: 'min', 5: 'sec', 6: 'day_of_week', 7: 'day_of_year'})

# ---- inputs and global variables
stf = _input('stf', M5)  # Time Frames Calculation Signal Starts
etf = _input('etf', D1)  # Last Time Frames Calculation Signal
cor = _input('cor', topchart)  # Arrow Move Position
alerts = _input('alerts', Yes)  # Display Alerts / Messages (Yes) or (No)
EmailAlert = _input('EmailAlert', No)  # Email Alert (Yes) or (No)
sendnotify = _input('sendnotify', No)  # Send Notification (Yes) or (No)
displayinfo = _input('displayinfo', Yes)  # Display Trade Info
textcolor = _input('textcolor', clrSnow)  # Text Color
ArrowUp = _input('ArrowUp', clrLime)  # Arrow Up Color
ArrowDn = _input('ArrowDn', clrRed)  # Arrow Down Color
NTArrow = _input('NTArrow', clrYellow)  # Arrow No Signal
BufferUp = Arr(0, 0.0)
BufferDn = Arr(0, 0.0)
scaleX = 35  # coordinate
scaleY = 40  # coordinate
scaleYt = 18  # coordinate
offsetX = 250  # coordinate
offsetY = 3  # coordinate
fontSize = 7  # coordinate
txttf = 0
arrtf = 0
arclr = 0
bcor = 0
BBTF = Arr.of([PERIOD_M1, PERIOD_M5, PERIOD_M15, PERIOD_M30, PERIOD_H1, PERIOD_H4, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
XBB = Arr(10, 0, dyn=False)
periodStr = Arr.of(['M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D1', 'W1', 'MN', 'MOVE'], fill="")  # Text Timeframes
pricepos = 0.0
cbartime = 0
cur = 0
prv = 0
imnn = 0
imnp = 0
cmnt = 0
pmnt = 0
arr = 0
CI = 0
fbar = 0
posisi = ""
sigpos = ""
iname = ""
msgText = ""
frtext = 'wave'

def OnInit():
    global CI, arr, arrtf, bcor, iname, txttf
    SetIndexBuffer(0, BufferUp, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, 'Bullish')
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, True)
    SetIndexBuffer(1, BufferDn, INDICATOR_DATA)
    PlotIndexSetString(1, PLOT_LABEL, 'Bearish')
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    iname = 'WaveMTF'
    IndicatorSetString(INDICATOR_SHORTNAME, iname + '_(' + Symbol() + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    CI = ChartID()
    arr = ArraySize(XBB)
    if cor >= 0:
        if cor == topchart:
            bcor = CORNER_LEFT_UPPER
            txttf = 45
            arrtf = -20
        if cor == bottomchart:
            bcor = CORNER_LEFT_LOWER
            txttf = 45
            arrtf = -12
    else:
        name = ""
        for i in range(ObjectsTotal(CI, 0, -1) - 1, 0 - 1, -1):
            name = ObjectName(CI, i, 0, -1)
            if StringFind(name, frtext, 0) > -1:
                ObjectDelete(CI, name)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Comment('')
    name = ""
    for i in range(ObjectsTotal(CI, 0, -1) - 1, 0 - 1, -1):
        name = ObjectName(CI, i, 0, -1)
        if StringFind(name, frtext, 0) > -1:
            ObjectDelete(CI, name)
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global arclr, cbartime, cur, fbar, imnn, imnp, pricepos
    ResetLastError()
    limit = 0
    barc = 0
    if rates_total > 120:
        limit = 120
    barc = limit - 1
    ArrayResize(BufferUp, limit)
    ArrayResize(BufferDn, limit)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(BufferUp, True)
    ArraySetAsSeries(BufferDn, True)
    tfcnt = etf - stf
    arclr = NTArrow
    imnn = Seconds()
    if imnn != imnp:
        for w in range(barc, 0 - 1, -1):
            tr = 0
            xbup = 0
            xbdn = 0
            i = 0
            cbartime = time[w]
            if cor >= 0:
                x = 0
                while x < arr:
                    CreateArrowLabel(CI, frtext + '_tfx_arrow_' + _str(x), periodStr[x], 'Bodoni MT Black', fontSize, textcolor, bcor, txttf + (x * scaleX) + offsetX, scaleY + offsetY + 7, True)
                    x += 1
            i = 0
            while i < (arr - 1):
                XBB[i] = GetDirection(BBTF[i], w)
                if cor >= 0:
                    if XBB[i] > 0:
                        arclr = ArrowUp
                    if XBB[i] < 0:
                        arclr = ArrowDn
                    CreateArrowLabel(CI, frtext + '_win_arrow_' + _str(i), CharToString(108), 'Wingdings', 14, arclr, bcor, txttf + (i * scaleX) + offsetX, arrtf + scaleY + offsetY + 7, True)
                if i >= stf and i <= etf:
                    if XBB[i] > 0:
                        xbup += 1
                    if XBB[i] < 0:
                        xbdn += 1
                i += 1
            if i == 9:
                if xbup >= tfcnt:
                    tr = 1
                    XBB[i] = xbup
                    arclr = ArrowUp
                    BufferUp[w] = GetPrice(Period(), tr, w)
                    pricepos = BufferUp[w]
                    BufferDn[w] = 0.0
                    cur = 1
                    fbar = iBarShift(Symbol(), Period(), cbartime, False)
                elif xbdn >= tfcnt:
                    tr = -1
                    XBB[i] = xbdn
                    arclr = ArrowDn
                    BufferDn[w] = GetPrice(Period(), tr, w)
                    pricepos = BufferDn[w]
                    BufferUp[w] = 0.0
                    cur = -1
                    fbar = iBarShift(Symbol(), Period(), cbartime, False)
                else:
                    XBB[i] = 0
                    arclr = NTArrow
                    BufferDn[w] = 0.0
                    BufferUp[w] = 0.0
                    pricepos = close[w]
                    cur = 0
                    fbar = iBarShift(Symbol(), Period(), cbartime, False)
                if cor >= 0:
                    CreateArrowLabel(CI, frtext + '_win_arrow_' + _str(i), CharToString(108), 'Wingdings', 14, arclr, bcor, txttf + (i * scaleX) + offsetX + 8, arrtf + scaleY + offsetY + 7, True)
        imnp = imnn
    if (alerts == Yes or EmailAlert == Yes) or sendnotify == Yes:
        Do_Alerts(cur, fbar)
    if displayinfo == Yes:
        ChartComm()
    return rates_total

def GetDirection(xtf, bar):
    ret = 0
    ptpc1 = (iHigh(Symbol(), xtf, bar + 1) + iLow(Symbol(), xtf, bar + 1) + iClose(Symbol(), xtf, bar + 1)) / 3
    ptpc0 = (iHigh(Symbol(), xtf, bar) + iLow(Symbol(), xtf, bar) + iClose(Symbol(), xtf, bar)) / 3
    mapw1 = IMA(Symbol(), xtf, 13, 0, MODE_SMMA, PRICE_WEIGHTED, bar + 1)
    mapw0 = IMA(Symbol(), xtf, 13, 0, MODE_SMMA, PRICE_WEIGHTED, bar)
    bb1 = ptpc1 - mapw1
    bb0 = ptpc0 - mapw0
    if bb0 > bb1:
        ret = 1
    if bb0 < bb1:
        ret = -1
    return ret

def GetPrice(xtf, bb, bx):
    global cbartime
    bar = 30
    ppos = 0.0
    HH = iHighest(Symbol(), xtf, MODE_HIGH, bar, bx)
    LL = iLowest(Symbol(), xtf, MODE_LOW, bar, bx)
    if bb > 0:
        ppos = iLow(Symbol(), xtf, LL)
        cbartime = iTime(Symbol(), xtf, LL)
    if bb < 0:
        ppos = iHigh(Symbol(), xtf, HH)
        cbartime = iTime(Symbol(), xtf, HH)
    return ppos

def IMA(symbol, tf, period, ma_shift, method, mprice, shift):
    handle = iMA(symbol, tf, period, ma_shift, method, mprice)
    buf = Arr(0, 0.0)
    if handle < 0:
        Print('The iMA object is not created: Error', GetLastError())
        return -1.0
    else:
        CopyBuffer(handle, 0, shift, 1, buf)
    return buf[0]

def Do_Alerts(fcur, fb):
    global cmnt, msgText, pmnt, posisi, prv, sigpos
    cmnt = Minutes()
    if cmnt != pmnt:
        if fcur == 1:
            msgText = 'Wave Price Up Start' + ' at bars: ' + _str(fb)
            posisi = 'Bullish'
            sigpos = 'Open BUY Order'
        elif fcur == -1:
            msgText = 'Wave Price Down Start' + ' at bars: ' + _str(fb)
            posisi = 'Bearish'
            sigpos = 'Open SELL Order'
        else:
            msgText = 'Wave Price Not Found!'
            posisi = 'Not Found!'
            sigpos = 'Wait for Confirmation!'
        if fcur != prv:
            Print(iname, '--- ' + Symbol() + ' ' + TF2Str(Period()) + ': ' + msgText + '\n--- at: ', TimeToString(iTime(Symbol(), 0, 0), TIME_DATE | TIME_MINUTES) + ' - ' + sigpos)
            if alerts == Yes:
                Alert(iname, '--- ' + Symbol() + ' ' + TF2Str(Period()) + ': ' + msgText + '--- at: ', TimeToString(iTime(Symbol(), 0, 0), TIME_DATE | TIME_MINUTES) + ' - ' + sigpos)
            if EmailAlert == Yes:
                SendMail(iname, '--- ' + Symbol() + ' ' + TF2Str(Period()) + ': ' + msgText + '\n--- at: ' + TimeToString(iTime(Symbol(), 0, 0), TIME_DATE | TIME_MINUTES) + ' - ' + sigpos)
            if sendnotify == Yes:
                SendNotification(iname + '--- ' + Symbol() + ' ' + TF2Str(Period()) + ': ' + msgText + '\n--- at: ' + TimeToString(iTime(Symbol(), 0, 0), TIME_DATE | TIME_MINUTES) + ' - ' + sigpos)
            prv = fcur
        pmnt = cmnt
    return

def TF2Str(period):
    _sw1 = period
    if _sw1 == PERIOD_M1:
        return 'M1'
    elif _sw1 == PERIOD_M5:
        return 'M5'
    elif _sw1 == PERIOD_M15:
        return 'M15'
    elif _sw1 == PERIOD_M30:
        return 'M30'
    elif _sw1 == PERIOD_H1:
        return 'H1'
    elif _sw1 == PERIOD_H4:
        return 'H4'
    elif _sw1 == PERIOD_D1:
        return 'D1'
    elif _sw1 == PERIOD_W1:
        return 'W1'
    elif _sw1 == PERIOD_MN1:
        return 'MN'
    return _str(period)

def AccountMode():
    account_type = AccountInfoInteger(ACCOUNT_TRADE_MODE)
    trade_mode = ""
    _sw2 = account_type
    if _sw2 == ACCOUNT_TRADE_MODE_DEMO:
        trade_mode = 'Demo'
    elif _sw2 == ACCOUNT_TRADE_MODE_CONTEST:
        trade_mode = 'Contest'
    else:
        trade_mode = 'Real'
    return trade_mode

def ChartComm():
    Comment('\n     :: Server Date Time : ', _str(Year()), '.', _str(Month()), '.', _str(Day()), '   ', TimeToString(TimeCurrent(), TIME_SECONDS), '\n     ------------------------------------------------------------', '\n      :: Broker             :  ', TerminalInfoString(TERMINAL_COMPANY), '\n      :: Acc. Name       :  ', AccountInfoString(ACCOUNT_NAME), '\n      :: Acc, Number    :  ', _str(AccountInfoInteger(ACCOUNT_LOGIN)), '\n      :: Acc,TradeMode :  ', AccountMode(), '\n      :: Acc. Leverage   :  1 : ', _str(AccountInfoInteger(ACCOUNT_LEVERAGE)), '\n      :: Acc. Balance     :  ', DoubleToString(AccountInfoDouble(ACCOUNT_BALANCE), 2), '\n      :: Acc. Equity       :  ', DoubleToString(AccountInfoDouble(ACCOUNT_EQUITY), 2), '\n      --------------------------------------------', '\n      :: Indicator Name  :  ', iname, '\n      :: Currency Pair    :  ', Symbol(), '\n      :: Current Spread  :  ', IntegerToString(SymbolInfoInteger(Symbol(), SYMBOL_SPREAD), 0), '\n      :: Signal Start       : at bar ', _str(iBarShift(Symbol(), 0, cbartime, False)), '\n      :: Wave Start       :  ', DoubleToString(pricepos, Digits()), '\n      :: Indicator Signal :  ', posisi, '\n      :: Suggested        :  ', sigpos)
    ChartRedraw()
    return

def CreateArrowLabel(chart_id, lable_name, label_text, font_model, font_size, label_color, chart_corner, x_cor, y_cor, price_hidden):
    ObjectDelete(chart_id, lable_name)
    if not ObjectCreate(chart_id, lable_name, OBJ_LABEL, 0, 0, 0, 0, 0):
        return False
    ObjectSetString(chart_id, lable_name, OBJPROP_TEXT, label_text)
    ObjectSetString(chart_id, lable_name, OBJPROP_FONT, font_model)
    ObjectSetInteger(chart_id, lable_name, OBJPROP_FONTSIZE, font_size)
    ObjectSetInteger(chart_id, lable_name, OBJPROP_COLOR, label_color)
    ObjectSetInteger(chart_id, lable_name, OBJPROP_CORNER, chart_corner)
    ObjectSetInteger(chart_id, lable_name, OBJPROP_XDISTANCE, x_cor)
    ObjectSetInteger(chart_id, lable_name, OBJPROP_YDISTANCE, y_cor)
    ObjectSetInteger(chart_id, lable_name, OBJPROP_HIDDEN, price_hidden)
    return True

def Year():
    return MqlReturnDateTime(TimeCurrent(), year)

def Month():
    return MqlReturnDateTime(TimeCurrent(), mon)

def Day():
    return MqlReturnDateTime(TimeCurrent(), day)

def Hours():
    return MqlReturnDateTime(TimeCurrent(), hour)

def Minutes():
    return MqlReturnDateTime(TimeCurrent(), min_)

def Seconds():
    return MqlReturnDateTime(TimeCurrent(), sec)

def MqlReturnDateTime(reqtime, mode):
    mqltm = MqlDateTime()
    TimeToStruct(reqtime, mqltm)
    valdate = 0
    _sw3 = mode
    if _sw3 == 0:
        valdate = mqltm.year
    elif _sw3 == 1:
        valdate = mqltm.mon
    elif _sw3 == 2:
        valdate = mqltm.day
    elif _sw3 == 3:
        valdate = mqltm.hour
    elif _sw3 == 4:
        valdate = mqltm.min
    elif _sw3 == 5:
        valdate = mqltm.sec
    elif _sw3 == 6:
        valdate = mqltm.day_of_week
    elif _sw3 == 7:
        valdate = mqltm.day_of_year
    return valdate


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WaveMTF(_MQL5Indicator):
    name = 'WaveMTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'stf': _Choice({0: 'TF-M1', 1: 'TF-M5', 2: 'TF-M15', 3: 'TF-M30', 4: 'TF-H1', 5: 'TF-H4', 6: 'TF-D1', 7: 'TF-W1', 8: 'TF-MN'}, default=1),  # Time Frames Calculation Signal Starts
        'etf': _Choice({0: 'TF-M1', 1: 'TF-M5', 2: 'TF-M15', 3: 'TF-M30', 4: 'TF-H1', 5: 'TF-H4', 6: 'TF-D1', 7: 'TF-W1', 8: 'TF-MN'}, default=6),  # Last Time Frames Calculation Signal
        'cor': _Choice({-1: 'Not Show Arrow', 0: 'On Top Chart', 1: 'On Bottom Chart'}, default=0),  # Arrow Move Position
        'alerts': _Choice({0: 'No', 1: 'Yes'}, default=1),  # Display Alerts / Messages (Yes) or (No)
        'EmailAlert': _Choice({0: 'No', 1: 'Yes'}, default=0),  # Email Alert (Yes) or (No)
        'sendnotify': _Choice({0: 'No', 1: 'Yes'}, default=0),  # Send Notification (Yes) or (No)
        'displayinfo': _Choice({0: 'No', 1: 'Yes'}, default=1),  # Display Trade Info
    }

