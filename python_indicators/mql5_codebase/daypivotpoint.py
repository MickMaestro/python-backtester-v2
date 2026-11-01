"""DayPivotPoint — converted from MQL5: MQL5 Indicators/DayPivotPoint MT5/DayPivotPoint.mq5

version: 1.0 ~ Last update: 2020/10/11 @ 01:35 AM WIT (Western Indonesian Time)
Indicator DayPivotPoint System with Signal and Alert for MetaTrader 5
with options to display signal on the chart.
This Indicator can use only on TF_M1 to H4, and will visually appealing
only on TF-M5 to TF-H1. Recommendation for Day Trading use on TF-M15.
Copyright: Copyright 2020, Roberto Jacobs (3rjfx) ~ By 3rjfx ~ Created: 2020/10/11; Link: https://www.mql5.com/en/users/3rjfx; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Roberto Jacobs (3rjfx) ~ By 3rjfx ~ Created: 2020/10/11', 'link': 'https://www.mql5.com/en/users/3rjfx', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['version: 1.0 ~ Last update: 2020/10/11 @ 01:35 AM WIT (Western Indonesian Time)', 'Indicator DayPivotPoint System with Signal and Alert for MetaTrader 5', 'with options to display signal on the chart.', 'This Indicator can use only on TF_M1 to H4, and will visually appealing', 'only on TF-M5 to TF-H1. Recommendation for Day Trading use on TF-M15.'], 'name': 'DayPivotPoint', 'source': 'MQL5 Indicators/DayPivotPoint MT5/DayPivotPoint.mq5', 'folder': 'DayPivotPoint MT5', 'inputs': [{'mql': 'alerts', 'py': 'alerts', 'param': 'alerts', 'type': 'int', 'default': 1, 'label': 'Display Alerts / Messages (Yes) or (No)', 'sinput': False}, {'mql': 'EmailAlert', 'py': 'EmailAlert', 'param': 'EmailAlert', 'type': 'int', 'default': 0, 'label': 'Email Alert (Yes) or (No)', 'sinput': False}, {'mql': 'sendnotify', 'py': 'sendnotify', 'param': 'sendnotify', 'type': 'int', 'default': 0, 'label': 'Send Notification (Yes) or (No)', 'sinput': False}, {'mql': 'displayinfo', 'py': 'displayinfo', 'param': 'displayinfo', 'type': 'int', 'default': 1, 'label': 'Display Trade Info', 'sinput': False}, {'mql': 'textcolor', 'py': 'textcolor', 'param': None, 'type': 'color', 'default': 16448255, 'label': 'Text Color', 'sinput': False}, {'mql': 'Fonts_Model', 'py': 'Fonts_Model', 'param': 'Fonts_Model', 'type': 'int', 'default': 0, 'label': 'Choose Fonts Model', 'sinput': False}, {'mql': 'WindColors', 'py': 'WindColors', 'param': None, 'type': 'color', 'default': 255, 'label': 'Colors for Wingdings', 'sinput': False}, {'mql': 'PvtLColors', 'py': 'PvtLColors', 'param': None, 'type': 'color', 'default': 55295, 'label': 'Colors for Pivot Lines', 'sinput': False}, {'mql': 'PvtLineStyle', 'py': 'PvtLineStyle', 'param': 'PvtLineStyle', 'type': 'int', 'default': 0, 'label': 'Pivot Line style', 'sinput': False}, {'mql': 'PvtLineWidth', 'py': 'PvtLineWidth', 'param': 'PvtLineWidth', 'type': 'int', 'default': 1, 'label': 'Pivot Line width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

OBJ_PERIOD_H1 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_H4 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_M1 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_M15 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_M30 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_M5 = 0  # MQL5 constant unknown to the converter

# enum YN
No = 0
Yes = 1
_enum('YN', {0: 'No', 1: 'Yes'})

# enum fonts
Arial_Black = 0
Bodoni_MT_Black = 1
_enum('fonts', {0: 'Arial_Black', 1: 'Bodoni_MT_Black'})

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
alerts = _input('alerts', Yes)  # Display Alerts / Messages (Yes) or (No)
EmailAlert = _input('EmailAlert', No)  # Email Alert (Yes) or (No)
sendnotify = _input('sendnotify', No)  # Send Notification (Yes) or (No)
displayinfo = _input('displayinfo', Yes)  # Display Trade Info
textcolor = _input('textcolor', clrSnow)  # Text Color
Fonts_Model = _input('Fonts_Model', Arial_Black)  # Choose Fonts Model
WindColors = _input('WindColors', clrRed)  # Colors for Wingdings
PvtLColors = _input('PvtLColors', clrGold)  # Colors for Pivot Lines
PvtLineStyle = _input('PvtLineStyle', STYLE_SOLID)  # Pivot Line style
PvtLineWidth = _input('PvtLineWidth', 1)  # Pivot Line width
arrpvt = 20
font_siz_ = 7
wind_color = 0
font_ohlc = ""
Pvt = 0.0
PvtO = 0.0
PvtL = 0.0
PvtH = 0.0
PvtO1 = 0.0
PvtL1 = 0.0
PvtH1 = 0.0
PvtC1 = 0.0
pivot = Arr(20, 0.0, dyn=False)
label = Arr.of(['S7', 'S6', 'S5', 'S4', 'S3', 'S2', 'SS1', 'S1', 'P20', 'P40', 'P60', 'P80', 'R1', 'SR1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7'], fill="")
prsi = PERIOD_M15
prdp = PERIOD_D1
chart_Id = 0
TIME = Arr(0, 0)
thistm = 0
prvtmp = 0
prvtmo = 0
cur = 0
prv = 0
imnn = 0
imnp = 0
cmnt = 0
pmnt = 0
lpvt = 77
limit = 0
HandleEMA2 = 0
EMA2 = Arr(0, 0.0)
posisi = ""
sigpos = ""
iname = ""
msgText = ""
_model = ""
frtext = 'PivotLine_'
drawpivot = False
drawpohl = False

def OnInit():
    global HandleEMA2, _model, chart_Id, drawpivot, drawpohl, font_ohlc, iname, prvtmo, prvtmp, wind_color
    chart_Id = ChartID()
    font_ohlc = FontsModel(Fonts_Model)
    wind_color = WindColors
    iname = 'DayPivotPoint (' + TF2Str(Period()) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, iname + '_(' + Symbol() + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    _model = FontsModel(Fonts_Model)
    drawpivot = False
    drawpohl = False
    prvtmp = iTime(Symbol(), 0, 1)
    prvtmo = iTime(Symbol(), 0, 1)
    HandleEMA2 = iMA(Symbol(), 0, 2, 0, MODE_EMA, PRICE_MEDIAN)
    if HandleEMA2 == INVALID_HANDLE:
        printf('Error creating EMA2 indicator for ', Symbol())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Comment('')
    if HandleEMA2 != INVALID_HANDLE:
        IndicatorRelease(HandleEMA2)
    PrintFormat('%s: Deinitialization reason code=%d', 'OnDeinit', reason)
    Print(getUninitReasonText(reason))
    ObjectsDeleteAll(chart_Id, 0, OBJ_TREND)
    ObjectsDeleteAll(chart_Id, 0, OBJ_TEXT)
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global cur, imnn, limit, thistm
    ResetLastError()
    if rates_total < 100:
        return 0
    limit = rates_total - prev_calculated
    if prev_calculated > 0:
        limit += 1
    if limit >= 100:
        limit = 100
    else:
        limit = lpvt + 2
    ArrayResize(EMA2, 2)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(TIME, True)
    ArraySetAsSeries(EMA2, True)
    thistm = time[0]
    imnn = Minutes()
    BarTimeInit(limit)
    if (not drawpivot) or thistm != prvtmp:
        DrawPivotPoint()
    if ((not drawpohl) or (close[0] > PvtH or close[0] < PvtL)) or thistm != prvtmo:
        DrawPOHL()
    if imnn != imnp:
        cur = SignalIndi()
    if (alerts == Yes or EmailAlert == Yes) or sendnotify == Yes:
        Do_Alerts(cur)
    if displayinfo == Yes:
        ChartComm()
    ChartRedraw(chart_Id)
    return rates_total

def DrawPivotPoint():
    global Pvt, PvtC1, PvtH1, PvtL1, PvtO1, drawpivot, prvtmp
    pb = 1
    dtcb = iTime(Symbol(), prdp, 0)
    pb = (2 if (DayOfWeek(dtcb) == 1) else 1)
    PvtL1 = iLow(Symbol(), prdp, pb)
    PvtH1 = iHigh(Symbol(), prdp, pb)
    PvtC1 = iClose(Symbol(), prdp, pb)
    PvtO1 = iOpen(Symbol(), prdp, pb)
    Pvt = (PvtH1 + PvtL1 + PvtC1) / 3
    sup1 = (Pvt * 2) - PvtH1
    res1 = (Pvt * 2) - PvtL1
    disr = res1 - sup1
    disl = disr * 0.2
    pivot[19] = (Pvt * 6) + PvtH1 - (PvtL1 * 6)
    pivot[18] = (Pvt * 5) + PvtH1 - (PvtL1 * 5)
    pivot[17] = (Pvt * 4) + PvtH1 - (PvtL1 * 4)
    pivot[16] = (Pvt * 3) + PvtH1 - (PvtL1 * 3)
    pivot[15] = (Pvt * 2) + PvtH1 - (PvtL1 * 2)
    pivot[14] = Pvt + PvtH1 - PvtL1
    pivot[13] = res1 + (disl * 0.618)
    pivot[12] = res1
    pivot[11] = sup1 + (disr * 0.8)
    pivot[10] = sup1 + (disr * 0.6)
    pivot[9] = sup1 + (disr * 0.4)
    pivot[8] = sup1 + (disr * 0.2)
    pivot[7] = sup1
    pivot[6] = sup1 - (disl * 0.618)
    pivot[5] = Pvt - PvtH1 + PvtL1
    pivot[4] = (Pvt * 2) - ((PvtH1 * 2) - PvtL1)
    pivot[3] = (Pvt * 3) - ((PvtH1 * 3) - PvtL1)
    pivot[2] = (Pvt * 4) - ((PvtH1 * 4) - PvtL1)
    pivot[1] = (Pvt * 5) - ((PvtH1 * 5) - PvtL1)
    pivot[0] = (Pvt * 6) - ((PvtH1 * 6) - PvtL1)
    x = 0
    while x < arrpvt:
        CreateTrendLine(chart_Id, frtext + label[x], TIME[lpvt], pivot[x], TIME[0], pivot[x], PvtLineWidth, PvtLineStyle, PvtLColors, False, True)
        CreateText(chart_Id, frtext + 'PDW' + _str(x), TIME[0], pivot[x], CharToString(108), 'Wingdings', font_siz_, wind_color, ANCHOR_LEFT)
        CreateText(chart_Id, frtext + 'PPP' + _str(x), TIME[0], pivot[x], '   ' + label[x] + ' - ' + DoubleToString(pivot[x], Digits()), _model, font_siz_, textcolor, ANCHOR_LEFT)
        prvtmp = thistm
        drawpivot = True
        DrawPOHL()
        x += 1
    return drawpivot

def DrawPOHL():
    global PvtH, PvtL, drawpohl, prvtmo
    POHL = Arr(4, 0.0, dyn=False)
    labelpric = Arr.of(['Pivot', 'Low', 'Open', 'High'], fill="")
    clrPOHL = Arr.of([clrAqua, clrDeepPink, clrMediumOrchid, clrBlue], fill=0)
    POHL[0] = Pvt
    POHL[1] = iLow(Symbol(), prdp, 0)
    POHL[2] = iOpen(Symbol(), prdp, 0)
    POHL[3] = iHigh(Symbol(), prdp, 0)
    PvtH = POHL[3]
    PvtL = POHL[1]
    x = 0
    while x < ArraySize(POHL):
        CreateTrendLine(chart_Id, frtext + labelpric[x], TIME[lpvt], POHL[x], TIME[0], POHL[x], PvtLineWidth, PvtLineStyle, clrPOHL[x], False, True)
        CreateText(chart_Id, frtext + 'PWDOHLC' + _str(x), TIME[0], POHL[x], CharToString(108), 'Wingdings', font_siz_, wind_color, ANCHOR_LEFT)
        CreateText(chart_Id, frtext + 'PPDOHLC' + _str(x), TIME[0], POHL[x], '   ' + labelpric[x] + ' - ' + DoubleToString(POHL[x], Digits()), FontsModel(0), font_siz_, textcolor, ANCHOR_LEFT)
        prvtmo = thistm
        drawpohl = True
        x += 1
    return drawpohl

def BarTimeInit(bars):
    ArrayResize(TIME, bars)
    for i in range(bars - 1, 0 - 1, -1):
        TIME[i] = iTime(Symbol(), 0, i)
    return

def SignalIndi():
    global imnp
    res = 0
    OPEN = iOpen(Symbol(), 0, 0)
    CopyBuffer(HandleEMA2, 0, 0, 2, EMA2)
    if OPEN < EMA2[0]:
        res = 1
    if OPEN > EMA2[0]:
        res = -1
    imnp = imnn
    return res

def FontsModel(mode):
    str_font = ""
    _sw1 = mode
    if _sw1 == 0:
        str_font = 'Arial Black'
    elif _sw1 == 1:
        str_font = 'Bodoni MT Black'
    return str_font

def CreateTrendLine(chartid, line_name, line_time1, line_price1, line_time2, line_price2, line_width, line_style, line_color, ray_right, line_hidden):
    ObjectDelete(chartid, line_name)
    if ObjectCreate(chartid, line_name, OBJ_TREND, 0, line_time1, line_price1, line_time2, line_price2):
        ObjectSetInteger(chartid, line_name, OBJPROP_WIDTH, line_width)
        ObjectSetInteger(chartid, line_name, OBJPROP_STYLE, line_style)
        ObjectSetInteger(chartid, line_name, OBJPROP_COLOR, line_color)
        ObjectSetInteger(chartid, line_name, OBJPROP_RAY_RIGHT, ray_right)
        ObjectSetInteger(chartid, line_name, OBJPROP_HIDDEN, line_hidden)
        ObjectSetInteger(chartid, line_name, OBJPROP_TIMEFRAMES, ((((OBJ_PERIOD_M1 | OBJ_PERIOD_M5) | OBJ_PERIOD_M15) | OBJ_PERIOD_M30) | OBJ_PERIOD_H1) | OBJ_PERIOD_H4)
    else:
        Print('Failed to create the object OBJ_TREND ', line_name, ', Error code = ', GetLastError())
        return False
    return True

def CreateText(chart_id, text_name, txt_time, txt_price, label_text, font_model, font_size, text_color, anchor):
    ObjectDelete(chart_id, text_name)
    if ObjectCreate(chart_id, text_name, OBJ_TEXT, 0, txt_time, txt_price):
        ObjectSetString(chart_id, text_name, OBJPROP_TEXT, label_text)
        ObjectSetString(chart_id, text_name, OBJPROP_FONT, font_model)
        ObjectSetInteger(chart_id, text_name, OBJPROP_FONTSIZE, font_size)
        ObjectSetInteger(chart_id, text_name, OBJPROP_COLOR, text_color)
        ObjectSetInteger(chart_id, text_name, OBJPROP_ANCHOR, anchor)
        ObjectSetInteger(chart_id, text_name, OBJPROP_TIMEFRAMES, ((((OBJ_PERIOD_M1 | OBJ_PERIOD_M5) | OBJ_PERIOD_M15) | OBJ_PERIOD_M30) | OBJ_PERIOD_H1) | OBJ_PERIOD_H4)
    else:
        Print('Failed to create the object OBJ_TEXT ', text_name, ', Error code = ', GetLastError())
        return False
    return True

def Do_Alerts(fcur):
    global cmnt, msgText, pmnt, posisi, prv, sigpos
    cmnt = Minutes()
    if cmnt != pmnt:
        if fcur == 1:
            msgText = 'The price will be rise'
            posisi = 'Bullish'
            sigpos = 'Open BUY Order!'
        elif fcur == -1:
            msgText = 'The price will be down'
            posisi = 'Bearish'
            sigpos = 'Open SELL Order!'
        else:
            msgText = 'Trend Not Found!'
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
    _sw2 = period
    if _sw2 == PERIOD_M1:
        return 'M1'
    elif _sw2 == PERIOD_M5:
        return 'M5'
    elif _sw2 == PERIOD_M15:
        return 'M15'
    elif _sw2 == PERIOD_M30:
        return 'M30'
    elif _sw2 == PERIOD_H1:
        return 'H1'
    elif _sw2 == PERIOD_H4:
        return 'H4'
    elif _sw2 == PERIOD_D1:
        return 'D1'
    elif _sw2 == PERIOD_W1:
        return 'W1'
    elif _sw2 == PERIOD_MN1:
        return 'MN'
    return _str(period)

def AccountMode():
    account_type = AccountInfoInteger(ACCOUNT_TRADE_MODE)
    trade_mode = ""
    _sw3 = account_type
    if _sw3 == ACCOUNT_TRADE_MODE_DEMO:
        trade_mode = 'Demo'
    elif _sw3 == ACCOUNT_TRADE_MODE_CONTEST:
        trade_mode = 'Contest'
    else:
        trade_mode = 'Real'
    return trade_mode

def ChartComm():
    Comment('\n     :: Server Date Time : ', _str(Year()), '.', _str(Month()), '.', _str(Day()), '   ', TimeToString(TimeCurrent(), TIME_SECONDS), '\n     ------------------------------------------------------------', '\n      :: Broker             :  ', TerminalInfoString(TERMINAL_COMPANY), '\n      :: Acc. Name       :  ', AccountInfoString(ACCOUNT_NAME), '\n      :: Acc, Number    :  ', _str(AccountInfoInteger(ACCOUNT_LOGIN)), '\n      :: Acc,TradeMode :  ', AccountMode(), '\n      :: Acc. Leverage   :  1 : ', _str(AccountInfoInteger(ACCOUNT_LEVERAGE)), '\n      :: Acc. Balance     :  ', DoubleToString(AccountInfoDouble(ACCOUNT_BALANCE), 2), '\n      :: Acc. Equity       :  ', DoubleToString(AccountInfoDouble(ACCOUNT_EQUITY), 2), '\n      --------------------------------------------', '\n      :: Indicator Name  :  ', iname, '\n      :: Currency Pair    :  ', Symbol(), '\n      :: Current Spread  :  ', IntegerToString(SymbolInfoInteger(Symbol(), SYMBOL_SPREAD), 0), '\n      :: Indicator Signal :  ', posisi, '\n      :: Suggested        :  ', sigpos)
    ChartRedraw()
    return

def Year():
    return MqlReturnDateTime(TimeCurrent(), year)

def Month():
    return MqlReturnDateTime(TimeCurrent(), mon)

def DayOfWeek(dow):
    return MqlReturnDateTime(dow, day_of_week)

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
    _sw4 = mode
    if _sw4 == 0:
        valdate = mqltm.year
    elif _sw4 == 1:
        valdate = mqltm.mon
    elif _sw4 == 2:
        valdate = mqltm.day
    elif _sw4 == 3:
        valdate = mqltm.hour
    elif _sw4 == 4:
        valdate = mqltm.min
    elif _sw4 == 5:
        valdate = mqltm.sec
    elif _sw4 == 6:
        valdate = mqltm.day_of_week
    elif _sw4 == 7:
        valdate = mqltm.day_of_year
    return valdate

def getUninitReasonText(reasonCode):
    text = ''
    _sw5 = reasonCode
    if _sw5 == REASON_PROGRAM:
        text = 'The EA has stopped working calling by remove function.'
    elif _sw5 == REASON_REMOVE:
        text = 'Program ' + 'DayPivotPoint.mq5' + ' was removed from chart'
    elif _sw5 == REASON_RECOMPILE:
        text = 'Program recompiled.'
    elif _sw5 == REASON_CHARTCHANGE:
        text = 'Symbol or timeframe was changed'
    elif _sw5 == REASON_CHARTCLOSE:
        text = 'Chart was closed'
    elif _sw5 == REASON_PARAMETERS:
        text = 'Input-parameter was changed'
    elif _sw5 == REASON_ACCOUNT:
        text = 'Account was changed'
    elif _sw5 == REASON_TEMPLATE:
        text = 'New template was applied to chart'
    elif _sw5 == REASON_INITFAILED:
        text = 'The OnInit() handler returned a non-zero value.'
    elif _sw5 == REASON_CLOSE:
        text = 'Terminal closed.'
    else:
        text = 'Another reason'
    return text


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DayPivotPoint(_MQL5Indicator):
    name = 'DayPivotPoint'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'alerts': _Choice({0: 'No', 1: 'Yes'}, default=1),  # Display Alerts / Messages (Yes) or (No)
        'EmailAlert': _Choice({0: 'No', 1: 'Yes'}, default=0),  # Email Alert (Yes) or (No)
        'sendnotify': _Choice({0: 'No', 1: 'Yes'}, default=0),  # Send Notification (Yes) or (No)
        'displayinfo': _Choice({0: 'No', 1: 'Yes'}, default=1),  # Display Trade Info
        'Fonts_Model': _Choice({0: 'Arial Black', 1: 'Bodoni MT Black'}, default=0),  # Choose Fonts Model
        'PvtLineStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Pivot Line style
        'PvtLineWidth': 1,  # Pivot Line width
    }

