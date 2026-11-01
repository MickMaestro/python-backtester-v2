"""LRDegrees — converted from MQL5: MQL5 Indicators/LRDegrees MT5/LRDegrees.mq5

MetaTrader 5 Forex Indicator Double Line of LinearRegression with Degrees and Trend Alerts.
Copyright: https://www.mql5.com/en/users/3rjfx. ~ By 3rjfx ~ Created: 2017/01/12; Link: https://www.mql5.com/en/users/3rjfx; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'https://www.mql5.com/en/users/3rjfx. ~ By 3rjfx ~ Created: 2017/01/12', 'link': 'https://www.mql5.com/en/users/3rjfx', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {}, 'levels': [], 'description': ['MetaTrader 5 Forex Indicator Double Line of LinearRegression with Degrees and Trend Alerts.'], 'name': 'LRDegrees', 'source': 'MQL5 Indicators/LRDegrees MT5/LRDegrees.mq5', 'folder': 'LRDegrees MT5', 'inputs': [{'mql': 'degress', 'py': 'degress', 'param': 'degress', 'type': 'int', 'default': 0, 'label': 'Set Linear Degrees Line', 'sinput': False}, {'mql': 'barsCountLine1', 'py': 'barsCountLine1', 'param': 'barsCountLine1', 'type': 'int', 'default': 35, 'label': 'Linear Regression 1 Bars to count', 'sinput': False}, {'mql': 'barsCountLine2', 'py': 'barsCountLine2', 'param': 'barsCountLine2', 'type': 'int', 'default': 5, 'label': 'Linear Regression 2 Bars to count', 'sinput': False}, {'mql': 'LRLineColor1', 'py': 'LRLineColor1', 'param': None, 'type': 'color', 'default': 255, 'label': 'Linear Regression Line1 Color', 'sinput': False}, {'mql': 'LRLineColor2', 'py': 'LRLineColor2', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Linear Regression Line2 Color', 'sinput': False}, {'mql': 'RoundedColor', 'py': 'RoundedColor', 'param': None, 'type': 'color', 'default': 16776960, 'label': 'Rounded Color', 'sinput': False}, {'mql': 'UpsColor', 'py': 'UpsColor', 'param': None, 'type': 'color', 'default': 16776960, 'label': 'Arrow Up Color', 'sinput': False}, {'mql': 'DnsColor', 'py': 'DnsColor', 'param': None, 'type': 'color', 'default': 17919, 'label': 'Arrow Down Color', 'sinput': False}, {'mql': 'PriceColor', 'py': 'PriceColor', 'param': None, 'type': 'color', 'default': 16448255, 'label': 'Arrow Right Price  Color', 'sinput': False}, {'mql': 'LRLineStyle', 'py': 'LRLineStyle', 'param': 'LRLineStyle', 'type': 'int', 'default': 0, 'label': 'Linear Regression Line style', 'sinput': False}, {'mql': 'LRLineWidth', 'py': 'LRLineWidth', 'param': 'LRLineWidth', 'type': 'int', 'default': 2, 'label': 'Linear Regression Line width', 'sinput': False}, {'mql': 'MsgAlerts', 'py': 'MsgAlerts', 'param': 'MsgAlerts', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'SoundAlerts', 'py': 'SoundAlerts', 'param': 'SoundAlerts', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'eMailAlerts', 'py': 'eMailAlerts', 'param': 'eMailAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'SoundAlertFile', 'py': 'SoundAlertFile', 'param': None, 'type': 'string', 'default': 'alert.wav', 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum SetDegree
Line2 = 0
Line1 = 1
_enum('SetDegree', {0: 'Line2', 1: 'Line1'})

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
degress = _input('degress', Line2)  # Set Linear Degrees Line
barsCountLine1 = _input('barsCountLine1', 35)  # Linear Regression 1 Bars to count
barsCountLine2 = _input('barsCountLine2', 5)  # Linear Regression 2 Bars to count
LRLineColor1 = _input('LRLineColor1', clrRed)  # Linear Regression Line1 Color
LRLineColor2 = _input('LRLineColor2', clrBlue)  # Linear Regression Line2 Color
RoundedColor = _input('RoundedColor', clrAqua)  # Rounded Color
UpsColor = _input('UpsColor', clrAqua)  # Arrow Up Color
DnsColor = _input('DnsColor', clrOrangeRed)  # Arrow Down Color
PriceColor = _input('PriceColor', clrSnow)  # Arrow Right Price  Color
LRLineStyle = _input('LRLineStyle', STYLE_SOLID)  # Linear Regression Line style
LRLineWidth = _input('LRLineWidth', 2)  # Linear Regression Line width
MsgAlerts = _input('MsgAlerts', True)
SoundAlerts = _input('SoundAlerts', True)
eMailAlerts = _input('eMailAlerts', False)
SoundAlertFile = _input('SoundAlertFile', 'alert.wav')
DegreesUp = Arr(0, 0.0)
DegreesDn = Arr(0, 0.0)
LRBuffers1 = Arr(0, 0.0)
LRBuffers2 = Arr(0, 0.0)
corner = CORNER_RIGHT_UPPER
dist_x = 144
dist_xt = 104
dist_y = 125
cmal = 0
xmal = 0
posalert = 0
prevalert = 0
bar_count = 0
stgBull = clrBlue
stsBull = clrAqua
stsBear = clrYellow
stgBear = clrRed
txtrbl = clrWhite
txtblk = clrBlack
rndclr = 0
arrclr = 0
txtclr = 0
Chart_Id = 0
name = ""
dtext = ""
Albase = ""
AlSubj = ""
AlMsg = ""

def OnInit():
    global Chart_Id, bar_count, name
    Chart_Id = ChartID()
    bar_count = 120
    name = 'LR Degrees'
    IndicatorSetString(INDICATOR_SHORTNAME, name)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, DegreesUp, INDICATOR_DATA)
    SetIndexBuffer(1, DegreesDn, INDICATOR_DATA)
    SetIndexBuffer(2, LRBuffers1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, LRBuffers2, INDICATOR_CALCULATIONS)
    PlotIndexSetString(0, PLOT_LABEL, 'UpDegrees')
    PlotIndexSetString(1, PLOT_LABEL, 'DnDegrees')
    PlotIndexSetString(2, PLOT_LABEL, 'LR_Line1')
    PlotIndexSetString(3, PLOT_LABEL, 'LR_Line2')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(ChartID(), 0, -1)
    GlobalVariablesDeleteAll()
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global arrclr, dtext, posalert, rndclr, txtclr
    if rates_total < bar_count:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    ResetLastError()
    ChartRedraw(0)
    l = 0
    r = 0
    j = 0
    dtxt = 0
    dgrsUp = False
    dgrsDn = False
    x = 0.0
    y = 0.0
    z = 0.0
    a = 0.0
    b = 0.0
    c = 0.0
    sumy = 0.0
    sumx1 = 0.0
    sumxy = 0.0
    sumx2 = 0.0
    suma = 0.0
    sumb1 = 0.0
    sumab = 0.0
    sumb2 = 0.0
    hmax = 0.0
    lmin = 0.0
    cur_degrees = 0.0
    prev1_degrees = 0.0
    prev2_degrees = 0.0
    div1_degrees = 0.0
    div0_degrees = 0.0
    HL = 100
    Hi = iHighest_u(Symbol(), PERIOD_CURRENT, HL, 0)
    Lo = iLowest_u(Symbol(), PERIOD_CURRENT, HL, 0)
    if Hi != -1:
        hmax = high[Hi]
    if Lo != -1:
        lmin = low[Lo]
    rangetb = hmax - lmin
    toplevel1 = lmin + ((rangetb / 1000) * 838)
    toplevel2 = lmin + ((rangetb / 1000) * 618)
    midlevel = lmin + ((rangetb / 1000) * 500)
    botlevel2 = lmin + ((rangetb / 1000) * 382)
    botlevel1 = lmin + ((rangetb / 1000) * 162)
    r = 0
    for r in range(r, barsCountLine1):
        sumy += iMA_u(Symbol(), PERIOD_CURRENT, 1, 0, MODE_LWMA, PRICE_WEIGHTED, r)
        sumxy += iMA_u(Symbol(), PERIOD_CURRENT, 1, 0, MODE_LWMA, PRICE_WEIGHTED, r) * r
        sumx1 += r
        sumx2 += r * r
    else:
        r = _range_end(r, barsCountLine1, 1)
    x = (sumx2 * barsCountLine1) - (sumx1 * sumx1)
    y = _fdiv((sumxy * barsCountLine1) - (sumx1 * sumy), x)
    z = (sumy - (sumx1 * y)) / barsCountLine1
    l = 0
    for l in range(l, barsCountLine1):
        LRBuffers1[l] = z + (y * l)
    else:
        l = _range_end(l, barsCountLine1, 1)
    j = 0
    for j in range(j, barsCountLine2):
        suma += iMA_u(Symbol(), PERIOD_CURRENT, 1, 0, MODE_LWMA, PRICE_WEIGHTED, j)
        sumab += iMA_u(Symbol(), PERIOD_CURRENT, 1, 0, MODE_LWMA, PRICE_WEIGHTED, j) * j
        sumb1 += j
        sumb2 += j * j
    else:
        j = _range_end(j, barsCountLine2, 1)
    a = (sumb2 * barsCountLine2) - (sumb1 * sumb1)
    b = _fdiv((sumab * barsCountLine2) - (sumb1 * suma), a)
    c = (suma - (sumb1 * b)) / barsCountLine2
    l = 0
    for l in range(l, barsCountLine2):
        LRBuffers2[l] = c + (b * l)
    else:
        l = _range_end(l, barsCountLine2, 1)
    for i in range(bar_count - 1, 0 - 1, -1):
        if i == 0:
            _sw1 = degress
            if _sw1 == 0:
                cur_degrees = NormalizeDouble(270 + (_fdiv(LRBuffers2[0] - lmin, hmax - lmin) * 180), 2)
                prev1_degrees = NormalizeDouble(270 + (_fdiv(LRBuffers2[1] - lmin, hmax - lmin) * 180), 2)
                prev2_degrees = NormalizeDouble(270 + (_fdiv(LRBuffers2[2] - lmin, hmax - lmin) * 180), 2)
                div1_degrees = prev1_degrees - prev2_degrees
                div0_degrees = cur_degrees - prev2_degrees
            elif _sw1 == 1:
                cur_degrees = NormalizeDouble(270 + (_fdiv(LRBuffers1[0] - lmin, hmax - lmin) * 180), 2)
                prev1_degrees = NormalizeDouble(270 + (_fdiv(LRBuffers1[1] - lmin, hmax - lmin) * 180), 2)
                prev2_degrees = NormalizeDouble(270 + (_fdiv(LRBuffers1[2] - lmin, hmax - lmin) * 180), 2)
                div1_degrees = prev1_degrees - prev2_degrees
                div0_degrees = cur_degrees - prev2_degrees
            if cur_degrees > 360.0:
                cur_degrees = NormalizeDouble(cur_degrees - 360.0, 2)
            if cur_degrees == 360.0:
                cur_degrees = NormalizeDouble(0.0, 2)
            if cur_degrees == 90.0:
                cur_degrees = NormalizeDouble(90.0, 2)
            if cur_degrees == 270.0:
                cur_degrees = NormalizeDouble(270.0, 2)
            if div0_degrees > div1_degrees:
                dgrsUp = True
                dgrsDn = False
                DegreesUp[i] = cur_degrees
                DegreesDn[i] = 0.0
            if div0_degrees < div1_degrees:
                dgrsDn = True
                dgrsUp = False
                DegreesDn[i] = cur_degrees
                DegreesUp[i] = 0.0
            if (cur_degrees >= 270.0 and cur_degrees < 315.0) and dgrsDn == True:
                rndclr = stgBear
                arrclr = stgBear
                txtclr = txtrbl
                posalert = 11
            if (cur_degrees >= 270.0 and cur_degrees < 315.0) and dgrsUp == True:
                rndclr = stgBear
                arrclr = stsBear
                txtclr = txtrbl
                posalert = 12
            if (cur_degrees >= 315.0 and cur_degrees < 360.0) and dgrsDn == True:
                rndclr = stsBear
                arrclr = stgBear
                txtclr = txtblk
                posalert = 21
            if (cur_degrees >= 315.0 and cur_degrees < 360.0) and dgrsUp == True:
                rndclr = stsBear
                arrclr = stsBull
                txtclr = txtblk
                posalert = 23
            if (cur_degrees >= 0.0 and cur_degrees < 45.0) and dgrsUp == True:
                rndclr = stsBull
                arrclr = stgBull
                txtclr = txtblk
                posalert = 34
            if (cur_degrees >= 0.0 and cur_degrees < 45.0) and dgrsDn == True:
                rndclr = stsBull
                arrclr = stsBear
                txtclr = txtblk
                posalert = 32
            if (cur_degrees >= 45.0 and cur_degrees <= 90.0) and dgrsUp == True:
                rndclr = stgBull
                arrclr = stgBull
                txtclr = txtrbl
                posalert = 44
            if (cur_degrees >= 45.0 and cur_degrees <= 90.0) and dgrsDn == True:
                rndclr = stgBull
                arrclr = stsBull
                txtclr = txtrbl
                posalert = 43
            dtext = DoubleToString(cur_degrees, 1) + CharToString(176)
            if StringLen(dtext) > 5:
                dtxt = 24
            elif StringLen(dtext) == 5:
                dtxt = 20
            else:
                dtxt = 17
            CreateRoundDegrees(Chart_Id, 'RoundedDegrees', 'Wingdings', CharToString(108), 67, rndclr, corner, dist_x, dist_y, True)
            CreateRoundDegrees(Chart_Id, 'TextDegrees', 'Bodoni MT Black', dtext, 8, txtclr, corner, dist_xt + dtxt, dist_y + 41, True)
            if dgrsUp:
                CreateArrowDegrees(Chart_Id, 'ArrUpDegrees', 'ArrDnDegrees', 'Wingdings', CharToString(217), 23, arrclr, corner, dist_xt + 20, dist_y - 2, True)
            if dgrsDn:
                CreateArrowDegrees(Chart_Id, 'ArrDnDegrees', 'ArrUpDegrees', 'Wingdings', CharToString(218), 23, arrclr, corner, dist_xt + 20, dist_y + 63, True)
            clinear1 = (LRLineColor2 if (LRBuffers1[0] >= LRBuffers1[barsCountLine1 - 1]) else LRLineColor1)
            CreateLRTrendLine(Chart_Id, 'LRTrendLine1', time[0], LRBuffers1[0], time[barsCountLine1 - 1], LRBuffers1[barsCountLine1 - 1], LRLineWidth, LRLineStyle, clinear1, False, True)
            clinear2 = (LRLineColor2 if (LRBuffers2[0] >= LRBuffers2[barsCountLine2 - 1]) else LRLineColor1)
            CreateLRTrendLine(Chart_Id, 'LRTrendLine2', time[0], LRBuffers2[0], time[barsCountLine2 - 1], LRBuffers2[barsCountLine2 - 1], LRLineWidth, LRLineStyle, clinear2, False, True)
            CreateArrowPrice(Chart_Id, 'FiboLabelPrice_t1', time[0], toplevel1, PriceColor, STYLE_SOLID, 1, ANCHOR_LEFT, True)
            CreateArrowPrice(Chart_Id, 'FiboLabelPrice_t2', time[0], toplevel2, PriceColor, STYLE_SOLID, 1, ANCHOR_LEFT, True)
            CreateArrowPrice(Chart_Id, 'FiboLabelPrice_m', time[0], midlevel, PriceColor, STYLE_SOLID, 1, ANCHOR_LEFT, True)
            CreateArrowPrice(Chart_Id, 'FiboLabelPrice_b2', time[0], botlevel2, PriceColor, STYLE_SOLID, 1, ANCHOR_LEFT, True)
            CreateArrowPrice(Chart_Id, 'FiboLabelPrice_b1', time[0], botlevel1, PriceColor, STYLE_SOLID, 1, ANCHOR_LEFT, True)
    ChartRedraw(0)
    Sleep(500)
    PosAlerts(posalert)
    return rates_total

def CreateRoundDegrees(chartid, lable_name, lable_font_model, lable_obj_text, lable_font_size, lable_color, lable_corner, lable_xdist, lable_ydist, lable_hidden):
    if ObjectFind(chartid, lable_name) > 0:
        ObjectDelete(chartid, lable_name)
    ObjectCreate(chartid, lable_name, OBJ_LABEL, 0, 0, 0, 0, 0)
    ObjectSetInteger(chartid, lable_name, OBJPROP_FONTSIZE, lable_font_size)
    ObjectSetString(chartid, lable_name, OBJPROP_FONT, lable_font_model)
    ObjectSetString(chartid, lable_name, OBJPROP_TEXT, lable_obj_text)
    ObjectSetInteger(chartid, lable_name, OBJPROP_COLOR, lable_color)
    ObjectSetInteger(chartid, lable_name, OBJPROP_CORNER, lable_corner)
    ObjectSetInteger(chartid, lable_name, OBJPROP_XDISTANCE, lable_xdist)
    ObjectSetInteger(chartid, lable_name, OBJPROP_YDISTANCE, lable_ydist)
    ObjectSetInteger(chartid, lable_name, OBJPROP_HIDDEN, lable_hidden)

def CreateArrowDegrees(chartid, lable_name1, lable_name2, lable_font_model, lable_obj_text, lable_font_size, lable_color, lable_corner, lable_xdist, lable_ydist, lable_hidden):
    ObjectDelete(chartid, lable_name2)
    if ObjectFind(chartid, lable_name1) > 0:
        ObjectDelete(chartid, lable_name1)
    ObjectCreate(chartid, lable_name1, OBJ_LABEL, 0, 0, 0, 0, 0)
    ObjectSetInteger(chartid, lable_name1, OBJPROP_FONTSIZE, lable_font_size)
    ObjectSetString(chartid, lable_name1, OBJPROP_FONT, lable_font_model)
    ObjectSetString(chartid, lable_name1, OBJPROP_TEXT, lable_obj_text)
    ObjectSetInteger(chartid, lable_name1, OBJPROP_COLOR, lable_color)
    ObjectSetInteger(chartid, lable_name1, OBJPROP_CORNER, lable_corner)
    ObjectSetInteger(chartid, lable_name1, OBJPROP_XDISTANCE, lable_xdist)
    ObjectSetInteger(chartid, lable_name1, OBJPROP_YDISTANCE, lable_ydist)
    ObjectSetInteger(chartid, lable_name1, OBJPROP_HIDDEN, lable_hidden)

def CreateLRTrendLine(chartid, line_name, line_time1, line_price1, line_time2, line_price2, line_width, line_style, line_color, ray_right, line_hidden):
    if ObjectFind(chartid, line_name) > 0:
        ObjectDelete(chartid, line_name)
    ObjectCreate(chartid, line_name, OBJ_TREND, 0, line_time1, line_price1, line_time2, line_price2)
    ObjectSetInteger(chartid, line_name, OBJPROP_WIDTH, line_width)
    ObjectSetInteger(chartid, line_name, OBJPROP_STYLE, line_style)
    ObjectSetInteger(chartid, line_name, OBJPROP_COLOR, line_color)
    ObjectSetInteger(chartid, line_name, OBJPROP_RAY_RIGHT, ray_right)
    ObjectSetInteger(chartid, line_name, OBJPROP_HIDDEN, line_hidden)

def CreateArrowPrice(chart_id, arrow_name, arrow_time, arrow_pos, arrow_color, arrow_style, arrow_width, anchor, hidden):
    if ObjectFind(chart_id, arrow_name) > 0:
        ObjectDelete(chart_id, arrow_name)
    ObjectCreate(chart_id, arrow_name, OBJ_ARROW_RIGHT_PRICE, 0, arrow_time, arrow_pos)
    ObjectSetInteger(chart_id, arrow_name, OBJPROP_COLOR, arrow_color)
    ObjectSetInteger(chart_id, arrow_name, OBJPROP_STYLE, arrow_style)
    ObjectSetInteger(chart_id, arrow_name, OBJPROP_WIDTH, arrow_width)
    ObjectSetInteger(chart_id, arrow_name, OBJPROP_ANCHOR, anchor)
    ObjectSetInteger(chart_id, arrow_name, OBJPROP_HIDDEN, hidden)

def iHighest_u(symbol, tf, countbar, startpos):
    index = startpos
    if startpos < 0:
        return -1
    if countbar <= 0:
        countbar = Bars(symbol, tf)
    high = Arr(0, 0.0)
    ArraySetAsSeries(high, True)
    CopyHigh(symbol, tf, startpos, countbar, high)
    index = ArrayMaximum(high, startpos, countbar - startpos + 1)
    return index

def iLowest_u(symbol, tf, countbar, startpos):
    index = startpos
    if startpos < 0:
        return -1
    if countbar <= 0:
        countbar = Bars(symbol, tf)
    low = Arr(0, 0.0)
    ArraySetAsSeries(low, True)
    CopyLow(symbol, tf, startpos, countbar, low)
    index = ArrayMinimum(low, startpos, countbar - startpos + 1)
    return index

def iMA_u(symbol, tf, period, ma_shift, method, mprice, shift):
    handle = iMA(symbol, tf, period, ma_shift, method, mprice)
    buf = Arr(0, 0.0)
    if handle < 0:
        Print('The iMA object is not created: Error', GetLastError())
        return -1.0
    else:
        CopyBuffer(handle, 0, shift, 1, buf)
    return buf[0]

def MqlReturnDateTime(reqtime, mode):
    mqltm = MqlDateTime()
    TimeToStruct(reqtime, mqltm)
    valdate = 0
    _sw2 = mode
    if _sw2 == 0:
        valdate = mqltm.year
    elif _sw2 == 1:
        valdate = mqltm.mon
    elif _sw2 == 2:
        valdate = mqltm.day
    elif _sw2 == 3:
        valdate = mqltm.hour
    elif _sw2 == 4:
        valdate = mqltm.min
    elif _sw2 == 5:
        valdate = mqltm.sec
    elif _sw2 == 6:
        valdate = mqltm.day_of_week
    elif _sw2 == 7:
        valdate = mqltm.day_of_year
    return valdate

def DoAlerts(msgText, eMailSub):
    if MsgAlerts:
        Alert(msgText)
    if SoundAlerts:
        PlaySound(SoundAlertFile)
    if eMailAlerts:
        SendMail(eMailSub, msgText)

def StrTF(period):
    _sw3 = period
    if _sw3 == PERIOD_M1:
        return 'M1'
    elif _sw3 == PERIOD_M5:
        return 'M5'
    elif _sw3 == PERIOD_M15:
        return 'M15'
    elif _sw3 == PERIOD_M30:
        return 'M30'
    elif _sw3 == PERIOD_H1:
        return 'H1'
    elif _sw3 == PERIOD_H4:
        return 'H4'
    elif _sw3 == PERIOD_D1:
        return 'D1'
    elif _sw3 == PERIOD_W1:
        return 'W1'
    elif _sw3 == PERIOD_MN1:
        return 'MN'
    return _str(period)

def PosAlerts(curalerts):
    global AlMsg, AlSubj, Albase, cmal, prevalert, xmal
    cmal = MqlReturnDateTime(TimeCurrent(), min_)
    if cmal != xmal:
        if curalerts != prevalert and curalerts == 43:
            Albase = name + ' ' + Symbol() + ', TF: ' + StrTF(Period()) + ', Position ' + dtext
            AlSubj = Albase + ' Trend Began to Fall, Bulish Weakened'
            AlMsg = AlSubj + ' @ ' + TimeToString(TimeLocal(), TIME_SECONDS)
            DoAlerts(AlMsg, AlSubj)
            prevalert = curalerts
        if curalerts != prevalert and curalerts == 32:
            Albase = name + ' ' + Symbol() + ', TF: ' + StrTF(Period()) + ', Position ' + dtext
            AlSubj = Albase + ' Trend was Down, Bulish Reversal'
            AlMsg = AlSubj + ' @ ' + TimeToString(TimeCurrent(), TIME_SECONDS)
            DoAlerts(AlMsg, AlSubj)
            prevalert = curalerts
        if curalerts != prevalert and curalerts == 21:
            Albase = name + ' ' + Symbol() + ', TF: ' + StrTF(Period()) + ', Position ' + dtext
            AlSubj = Albase + ' Trend was Down, Bearish Strengthened'
            AlMsg = AlSubj + ' @ ' + TimeToString(TimeCurrent(), TIME_SECONDS)
            DoAlerts(AlMsg, AlSubj)
            prevalert = curalerts
        if curalerts != prevalert and curalerts == 11:
            Albase = name + ' ' + Symbol() + ', TF: ' + StrTF(Period()) + ', Position ' + dtext
            AlSubj = Albase + ' Trend was Down, Strong Bearish'
            AlMsg = AlSubj + ' @ ' + TimeToString(TimeCurrent(), TIME_SECONDS)
            DoAlerts(AlMsg, AlSubj)
            prevalert = curalerts
        if curalerts != prevalert and curalerts == 12:
            Albase = name + ' ' + Symbol() + ', TF: ' + StrTF(Period()) + ', Position ' + dtext
            AlSubj = Albase + ' Trend Began to Rise, Bearish Weakened'
            AlMsg = AlSubj + ' @ ' + TimeToString(TimeCurrent(), TIME_SECONDS)
            DoAlerts(AlMsg, AlSubj)
            prevalert = curalerts
        if curalerts != prevalert and curalerts == 23:
            Albase = name + ' ' + Symbol() + ', TF: ' + StrTF(Period()) + ', Position ' + dtext
            AlSubj = Albase + ' Trend was Up, Bearish Reversal'
            AlMsg = AlSubj + ' @ ' + TimeToString(TimeCurrent(), TIME_SECONDS)
            DoAlerts(AlMsg, AlSubj)
            prevalert = curalerts
        if curalerts != prevalert and curalerts == 34:
            Albase = name + ' ' + Symbol() + ', TF: ' + StrTF(Period()) + ', Position ' + dtext
            AlSubj = Albase + ' Trend was Up, Bulish Strengthened'
            AlMsg = AlSubj + ' @ ' + TimeToString(TimeCurrent(), TIME_SECONDS)
            DoAlerts(AlMsg, AlSubj)
            prevalert = curalerts
        if curalerts != prevalert and curalerts == 44:
            Albase = name + ' ' + Symbol() + ', TF: ' + StrTF(Period()) + ', Position ' + dtext
            AlSubj = Albase + ' Trend was Up, Strong Bulish'
            AlMsg = AlSubj + ' @ ' + TimeToString(TimeCurrent(), TIME_SECONDS)
            DoAlerts(AlMsg, AlSubj)
            prevalert = curalerts
        xmal = cmal
    return


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LRDegrees(_MQL5Indicator):
    name = 'LRDegrees'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'degress': _Choice({0: 'Line2', 1: 'Line1'}, default=0),  # Set Linear Degrees Line
        'barsCountLine1': 35,  # Linear Regression 1 Bars to count
        'barsCountLine2': 5,  # Linear Regression 2 Bars to count
        'LRLineStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Linear Regression Line style
        'LRLineWidth': 2,  # Linear Regression Line width
        'MsgAlerts': True,
        'SoundAlerts': True,
        'eMailAlerts': False,
    }

