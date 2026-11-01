"""PricePercentRange — converted from MQL5: MQL5 Indicators/PricePercentRange/PricePercentRange.mq5

Price(%)Range is the indicator for the MT5, which calculates the Price movement
based on percentage High (Highest) and Low (Lowest) Price on 100 bars.
Copyright: https://www.mql5.com/en/users/3rjfx. ~ By 3rjfx ~ Created: 2016/01/16; Link: https://www.mql5.com/en/users/3rjfx; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'https://www.mql5.com/en/users/3rjfx. ~ By 3rjfx ~ Created: 2016/01/16', 'link': 'https://www.mql5.com/en/users/3rjfx', 'version': '2.00', 'window': 'separate', 'indicator_buffers': 17, 'indicator_plots': 9}, 'types': {1: 0, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0}, 'colors': {}, 'widths': {}, 'styles': {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'labels': {}, 'levels': [], 'description': ['Price(%)Range is the indicator for the MT5, which calculates the Price movement', 'based on percentage High (Highest) and Low (Lowest) Price on 100 bars.'], 'name': 'PricePercentRange', 'source': 'MQL5 Indicators/PricePercentRange/PricePercentRange.mq5', 'folder': 'PricePercentRange', 'inputs': [{'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 6, 'label': 'AppliedPrice', 'sinput': False}, {'mql': 'SoundAlerts', 'py': 'SoundAlerts', 'param': 'SoundAlerts', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'MsgAlerts', 'py': 'MsgAlerts', 'param': 'MsgAlerts', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'eMailAlerts', 'py': 'eMailAlerts', 'param': 'eMailAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'SoundAlertFile', 'py': 'SoundAlertFile', 'param': None, 'type': 'string', 'default': 'alert.wav', 'label': '', 'sinput': False}, {'mql': 'MoveUpColor', 'py': 'MoveUpColor', 'param': None, 'type': 'color', 'default': 16711680, 'label': '', 'sinput': False}, {'mql': 'MoveDownColor', 'py': 'MoveDownColor', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'WaitDirectionColor', 'py': 'WaitDirectionColor', 'param': None, 'type': 'color', 'default': 65535, 'label': '', 'sinput': False}, {'mql': 'MoveLinkColor', 'py': 'MoveLinkColor', 'param': None, 'type': 'color', 'default': 16776960, 'label': '', 'sinput': False}, {'mql': 'TextColor', 'py': 'TextColor', 'param': None, 'type': 'color', 'default': 16448255, 'label': '', 'sinput': False}, {'mql': 'RoundedColor', 'py': 'RoundedColor', 'param': None, 'type': 'color', 'default': 65535, 'label': '', 'sinput': False}, {'mql': 'BorderlineAppPricesRise', 'py': 'BorderlineAppPricesRise', 'param': None, 'type': 'color', 'default': 16711680, 'label': '', 'sinput': False}, {'mql': 'BorderlineAppPricesDown', 'py': 'BorderlineAppPricesDown', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'LineWidthSize', 'py': 'LineWidthSize', 'param': 'LineWidthSize', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'TrendLineDowntoUpColor', 'py': 'TrendLineDowntoUpColor', 'param': None, 'type': 'color', 'default': 16711680, 'label': '', 'sinput': False}, {'mql': 'TrendLineUptoDownColor', 'py': 'TrendLineUptoDownColor', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'VerticalLineColor', 'py': 'VerticalLineColor', 'param': None, 'type': 'color', 'default': 55295, 'label': '', 'sinput': False}, {'mql': 'LineStyle', 'py': 'LineStyle', 'param': 'LineStyle', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'TextPosition', 'py': 'TextPosition', 'param': 'TextPosition', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'TextFontSize', 'py': 'TextFontSize', 'param': 'TextFontSize', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'TextFontName', 'py': 'TextFontName', 'param': None, 'type': 'string', 'default': 'Arial Black', 'label': '"Courier" //"Calibri" //"Cambria" //"Bodoni MT Black"', 'sinput': False}, {'mql': 'TopBottomDotSize', 'py': 'TopBottomDotSize', 'param': 'TopBottomDotSize', 'type': 'int', 'default': 15, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

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
AppliedPrice = _input('AppliedPrice', PRICE_TYPICAL)  # AppliedPrice
SoundAlerts = _input('SoundAlerts', True)
MsgAlerts = _input('MsgAlerts', True)
eMailAlerts = _input('eMailAlerts', False)
SoundAlertFile = _input('SoundAlertFile', 'alert.wav')
MoveUpColor = _input('MoveUpColor', clrBlue)
MoveDownColor = _input('MoveDownColor', clrRed)
WaitDirectionColor = _input('WaitDirectionColor', clrYellow)
MoveLinkColor = _input('MoveLinkColor', clrAqua)
TextColor = _input('TextColor', clrSnow)
RoundedColor = _input('RoundedColor', clrYellow)
BorderlineAppPricesRise = _input('BorderlineAppPricesRise', clrBlue)
BorderlineAppPricesDown = _input('BorderlineAppPricesDown', clrRed)
LineWidthSize = _input('LineWidthSize', 1)
TrendLineDowntoUpColor = _input('TrendLineDowntoUpColor', clrBlue)
TrendLineUptoDownColor = _input('TrendLineUptoDownColor', clrRed)
VerticalLineColor = _input('VerticalLineColor', clrGold)
LineStyle = _input('LineStyle', STYLE_SOLID)
TextPosition = _input('TextPosition', ANCHOR_RIGHT)
TextFontSize = _input('TextFontSize', 8)
TextFontName = _input('TextFontName', 'Arial Black')  # "Courier" //"Calibri" //"Cambria" //"Bodoni MT Black"
TopBottomDotSize = _input('TopBottomDotSize', 15)
ExtCPRBuffer = Arr(0, 0.0)
ExtHPRBuffer = Arr(0, 0.0)
ExtMHPRBuffer = Arr(0, 0.0)
ExtMDPBuffer = Arr(0, 0.0)
ExtMLPRBuffer = Arr(0, 0.0)
ExtLPRBuffer = Arr(0, 0.0)
ExtEMABuffer = Arr(0, 0.0)
ExtEMABuffUp = Arr(0, 0.0)
ExtEMABuffDn = Arr(0, 0.0)
ExtEMABuffWd = Arr(0, 0.0)
ema04 = Arr(0, 0.0)
ema24 = Arr(0, 0.0)
ema39 = Arr(0, 0.0)
cpr0 = 0.0
cpr1 = 0.0
cph = 0.0
cpl = 0.0
tpb0p1 = 0.0
tpt0p1 = 0.0
tpb0p2 = 0.0
tpt0p2 = 0.0
fb0p1 = 0
ft0p1 = 0
fb0p2 = 0
ft0p2 = 0
barUp = False
barDn = False
scaleYt = 18
offsetX = 150
offsetY = 3
fontSize = 9
corner = 3
arrow = 0
DATA_barcnt = 0
bigema = 39
medema = 24
smlema = 4
hilo = 0
pos = 0
prvup = 0
prvdn = 0
cal = 0
pal = 0
cmnt = 0
pmnt = 0
chart_ID = 0
short_name = ""
alBase = ""
alSubj = ""
alMsg = ""
ExtMa04Handle = 0
open = Arr(0, 0.0)
high = Arr(0, 0.0)
low = Arr(0, 0.0)
close = Arr(0, 0.0)
time = Arr(0, 0)

def OnInit():
    global DATA_barcnt, ExtMa04Handle, chart_ID, hilo, pos, short_name
    chart_ID = ChartID()
    DATA_barcnt = 135
    hilo = 100
    pos = 0
    short_name = 'Price(%R,' + Symbol() + ',' + 'TF:' + strTF(Period()) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_LEVELS, 4)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 23.6)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 38.2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, 61.8)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, 76.4)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrLightSlateGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrLightSlateGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrLightSlateGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 3, clrLightSlateGray)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 3, STYLE_DOT)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 100)
    SetIndexBuffer(0, ExtEMABuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(1, ExtCPRBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtHPRBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtMHPRBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ExtMDPBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, ExtMLPRBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, ExtLPRBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, ExtEMABuffUp, INDICATOR_DATA)
    SetIndexBuffer(8, ExtEMABuffDn, INDICATOR_DATA)
    SetIndexBuffer(9, ExtEMABuffWd, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, ema04, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, ema24, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, ema39, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, open, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, high, INDICATOR_CALCULATIONS)
    SetIndexBuffer(15, low, INDICATOR_CALCULATIONS)
    SetIndexBuffer(16, close, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, MoveLinkColor)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, MoveUpColor)
    PlotIndexSetInteger(3, PLOT_LINE_COLOR, MoveUpColor)
    PlotIndexSetInteger(4, PLOT_LINE_COLOR, WaitDirectionColor)
    PlotIndexSetInteger(5, PLOT_LINE_COLOR, MoveDownColor)
    PlotIndexSetInteger(6, PLOT_LINE_COLOR, MoveDownColor)
    PlotIndexSetInteger(7, PLOT_LINE_COLOR, MoveUpColor)
    PlotIndexSetInteger(8, PLOT_LINE_COLOR, MoveDownColor)
    PlotIndexSetInteger(1, PLOT_LINE_WIDTH, LineWidthSize)
    PlotIndexSetInteger(2, PLOT_LINE_WIDTH, LineWidthSize)
    PlotIndexSetInteger(3, PLOT_LINE_WIDTH, LineWidthSize)
    PlotIndexSetInteger(4, PLOT_LINE_WIDTH, LineWidthSize)
    PlotIndexSetInteger(5, PLOT_LINE_WIDTH, LineWidthSize)
    PlotIndexSetInteger(6, PLOT_LINE_WIDTH, LineWidthSize)
    PlotIndexSetInteger(7, PLOT_LINE_WIDTH, 2)
    PlotIndexSetInteger(8, PLOT_LINE_WIDTH, 2)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, smlema)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, smlema)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, smlema)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, smlema)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, smlema)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, smlema)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, smlema)
    PlotIndexSetInteger(8, PLOT_DRAW_BEGIN, smlema)
    PlotIndexSetString(0, PLOT_LABEL, None)
    PlotIndexSetString(1, PLOT_LABEL, 'Price(%)R')
    PlotIndexSetString(2, PLOT_LABEL, None)
    PlotIndexSetString(3, PLOT_LABEL, None)
    PlotIndexSetString(4, PLOT_LABEL, None)
    PlotIndexSetString(5, PLOT_LABEL, None)
    PlotIndexSetString(6, PLOT_LABEL, None)
    PlotIndexSetString(7, PLOT_LABEL, '(%R)Ups')
    PlotIndexSetString(8, PLOT_LABEL, '(%R)Down')
    PlotIndexSetString(9, PLOT_LABEL, None)
    PlotIndexSetString(10, PLOT_LABEL, None)
    PlotIndexSetString(11, PLOT_LABEL, None)
    PlotIndexSetString(12, PLOT_LABEL, None)
    PlotIndexSetString(13, PLOT_LABEL, None)
    PlotIndexSetString(14, PLOT_LABEL, None)
    PlotIndexSetString(15, PLOT_LABEL, None)
    PlotIndexSetString(16, PLOT_LABEL, None)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(ExtCPRBuffer, True)
    ArraySetAsSeries(ExtHPRBuffer, True)
    ArraySetAsSeries(ExtMHPRBuffer, True)
    ArraySetAsSeries(ExtMDPBuffer, True)
    ArraySetAsSeries(ExtMLPRBuffer, True)
    ArraySetAsSeries(ExtLPRBuffer, True)
    ArraySetAsSeries(ExtEMABuffer, True)
    ArraySetAsSeries(ExtEMABuffUp, True)
    ArraySetAsSeries(ExtEMABuffDn, True)
    ArraySetAsSeries(ExtEMABuffWd, True)
    ArraySetAsSeries(ema04, True)
    ArraySetAsSeries(ema24, True)
    ArraySetAsSeries(ema39, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    ExtMa04Handle = iMA(Symbol(), PERIOD_CURRENT, smlema, 0, MODE_EMA, PRICE_TYPICAL)
    if ExtMa04Handle == INVALID_HANDLE:
        printf('Error creating EMA indicator for ', Symbol())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(chart_ID, 0, -1)
    GlobalVariablesDeleteAll()
    return

def iHighest_u(array, timeframe, depth, startPos):
    index = startPos
    if startPos < 0:
        Print('Invalid parameter in the function iHighest, startPos =', startPos)
        return 0
    size = ArraySize(array)
    max_ = array[startPos]
    for i in range(depth, startPos, -1):
        if array[i] > max_:
            index = i
            max_ = array[i]
    return index

def iLowest_u(array, timeframe, depth, startPos):
    index = startPos
    if startPos < 0:
        Print('Invalid parameter in the function iLowest, startPos =', startPos)
        return 0
    size = ArraySize(array)
    min__ = array[startPos]
    for i in range(depth, startPos, -1):
        if array[i] < min__:
            index = i
            min__ = array[i]
    return index

def OnCalculate(rates_total, prev_calculated, begin, price):
    global arrow, barDn, barUp, cal, cph, cpl, cpr0, cpr1, fb0p1, fb0p2, ft0p1, ft0p2, prvdn, prvup, tpb0p1, tpb0p2, tpt0p1, tpt0p2
    ResetLastError()
    bar = 0
    if rates_total < DATA_barcnt:
        return 0
    bar = rates_total
    if prev_calculated == 0:
        bar = DATA_barcnt
    if prev_calculated > 0:
        bar += 1
    cal = 0
    z = 0
    i = 0
    x = 1
    ft0 = -1
    fb0 = -1
    scan = 7
    stbar = 0
    xbars = 26
    xhilo = 26
    tunebar = 5
    tunstep = 12
    xlimit = 100
    cph = 0.0
    cpl = 0.0
    tpt0 = 0.0
    tpb0 = 0.0
    tpttest = 0.0
    tpbtest = 0.0
    ArrayResize(ExtCPRBuffer, bar)
    ArrayResize(ExtHPRBuffer, bar)
    ArrayResize(ExtMHPRBuffer, bar)
    ArrayResize(ExtMDPBuffer, bar)
    ArrayResize(ExtMLPRBuffer, bar)
    ArrayResize(ExtLPRBuffer, bar)
    ArrayResize(ExtEMABuffer, bar)
    ArrayResize(ExtEMABuffUp, bar)
    ArrayResize(ExtEMABuffDn, bar)
    ArrayResize(ExtEMABuffWd, bar)
    ArrayResize(ema04, bar)
    ArrayResize(ema24, bar)
    ArrayResize(ema39, bar)
    ArrayResize(open, bar)
    ArrayResize(high, bar)
    ArrayResize(low, bar)
    ArrayResize(close, bar)
    ArrayResize(time, bar)
    calculated = BarsCalculated(ExtMa04Handle)
    if BarsCalculated(ExtMa04Handle) < rates_total:
        Print('Not all data of EMA 4 is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if False:
        return 0
    if CopyBuffer(ExtMa04Handle, 0, 0, to_copy, ema04) <= 0:
        Print('Getting EMA 4 buffers is failed! Error:', GetLastError())
        return 0
    copyOpen = CopyOpen(Symbol(), PERIOD_CURRENT, 0, calculated, open)
    copyHigh = CopyHigh(Symbol(), PERIOD_CURRENT, 0, calculated, high)
    copyLow = CopyLow(Symbol(), PERIOD_CURRENT, 0, calculated, low)
    copyClose = CopyClose(Symbol(), PERIOD_CURRENT, 0, calculated, close)
    copyTime = CopyTime(Symbol(), PERIOD_CURRENT, 0, calculated, time)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, medema, ema04, ema24)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, bigema, ema24, ema39)
    inH = iHighest_u(high, PERIOD_CURRENT, hilo, pos)
    inL = iLowest_u(low, PERIOD_CURRENT, hilo, pos)
    if inH != -1:
        cph = high[inH]
    if inL != -1:
        cpl = low[inL]
    ma24d = Arr(0, 0.0)
    ma04d = Arr(0, 0.0)
    ArrayResize(ma24d, calculated)
    ArrayResize(ma04d, calculated)
    ArraySetAsSeries(ma24d, True)
    ArraySetAsSeries(ma04d, True)
    if True:
        z = 0
        while z < tunstep and xhilo < xlimit:
            ft0 = iHighest_u(high, PERIOD_CURRENT, xhilo, stbar)
            fb0 = iLowest_u(low, PERIOD_CURRENT, xhilo, stbar)
            if ft0 != -1:
                tpttest = high[ft0]
            if fb0 != -1:
                tpbtest = low[fb0]
            if tpttest >= high[iHighest_u(high, PERIOD_CURRENT, scan, ft0 + 1)] and tpbtest <= low[iLowest_u(low, PERIOD_CURRENT, scan, fb0 + 1)]:
                tpt0 = high[ft0]
                tpb0 = low[fb0]
                break
            else:
                xhilo = xbars + (tunebar * z)
            z += 1
    if ft0 < fb0:
        barDn = True
        barUp = False
        fb0p1 = time[fb0]
        tpb0p1 = tpb0
        ft0p1 = time[ft0]
        tpt0p1 = tpt0
        prvdn = 1
        objnameDn10_ = short_name + ': VerticalLineSwingBarsUp1_'
        objnameDn20_ = short_name + ': VerticalLineSwingBarsUp2_'
        objname10 = short_name + ': TrendSwingBarsUp'
        objname20 = short_name + ': SwingBarsPosTop0'
        objname30 = short_name + ': SwingBarsPosBottom0'
        ObjectDelete(chart_ID, objname10)
        ObjectDelete(chart_ID, objname20)
        ObjectDelete(chart_ID, objname30)
        ObjectDelete(chart_ID, objnameDn10_)
        ObjectDelete(chart_ID, objnameDn20_)
        CreateObjectVLine(chart_ID, objnameDn10_, time[fb0], VerticalLineColor, LineStyle, LineWidthSize, True)
        CreateObjectVLine(chart_ID, objnameDn20_, time[ft0], VerticalLineColor, LineStyle, LineWidthSize, True)
        CreateObjectTrend(chart_ID, objname10, time[fb0], tpb0, time[ft0], tpt0, TrendLineDowntoUpColor, LineStyle, LineWidthSize, False, True)
        CreateObjectText(chart_ID, objname20, time[ft0], tpt0, CharToString(119), 'Wingdings', TopBottomDotSize, TrendLineUptoDownColor, ANCHOR_CENTER, True)
        CreateObjectText(chart_ID, objname30, time[fb0], tpb0, CharToString(119), 'Wingdings', TopBottomDotSize, TrendLineDowntoUpColor, ANCHOR_CENTER, True)
        if barDn and prvup == 1:
            prvup = 0
            objnameUp10p = short_name + ': VerticalLineSwingBarsDn1-' + TimeToString(fb0p2, TIME_DATE | TIME_MINUTES)
            objnameUp20p = short_name + ': VerticalLineSwingBarsDn2-' + TimeToString(ft0p2, TIME_DATE | TIME_MINUTES)
            objname10p = short_name + ': TrendSwingBarsDown2' + TimeToString(ft0p2, TIME_DATE | TIME_MINUTES)
            objname20p = short_name + ': SwingBarsPosTop0p' + TimeToString(ft0p2, TIME_DATE | TIME_MINUTES)
            objname30p = short_name + ': SwingBarsPosBottom0p' + TimeToString(fb0p2, TIME_DATE | TIME_MINUTES)
            CreateObjectVLine(chart_ID, objnameUp10p, fb0p2, VerticalLineColor, LineStyle, LineWidthSize, True)
            CreateObjectVLine(chart_ID, objnameUp20p, ft0p2, VerticalLineColor, LineStyle, LineWidthSize, True)
            CreateObjectTrend(chart_ID, objname10p, ft0p2, tpt0p2, fb0p2, tpb0p2, TrendLineUptoDownColor, LineStyle, LineWidthSize, False, True)
            CreateObjectText(chart_ID, objname20p, ft0p2, tpt0p2, CharToString(119), 'Wingdings', TopBottomDotSize, TrendLineUptoDownColor, ANCHOR_CENTER, True)
            CreateObjectText(chart_ID, objname30p, fb0p2, tpb0p2, CharToString(119), 'Wingdings', TopBottomDotSize, TrendLineDowntoUpColor, ANCHOR_CENTER, True)
    if ft0 > fb0:
        barUp = True
        barDn = False
        fb0p2 = time[fb0]
        tpb0p2 = tpb0
        ft0p2 = time[ft0]
        tpt0p2 = tpt0
        prvup = 1
        objnameUp10_ = short_name + ': VerticalLineSwingBarsDn1_'
        objnameUp20_ = short_name + ': VerticalLineSwingBarsDn2_'
        objname11 = short_name + ': TrendSwingBarsDown'
        objname21 = short_name + ': SwingBarsPosTop1'
        objname31 = short_name + ': SwingBarsPosBottom1'
        ObjectDelete(chart_ID, objname11)
        ObjectDelete(chart_ID, objname21)
        ObjectDelete(chart_ID, objname31)
        ObjectDelete(chart_ID, objnameUp10_)
        ObjectDelete(chart_ID, objnameUp20_)
        CreateObjectVLine(chart_ID, objnameUp10_, time[ft0], VerticalLineColor, LineStyle, LineWidthSize, True)
        CreateObjectVLine(chart_ID, objnameUp20_, time[fb0], VerticalLineColor, LineStyle, LineWidthSize, True)
        CreateObjectTrend(chart_ID, objname11, time[ft0], tpt0, time[fb0], tpb0, TrendLineUptoDownColor, LineStyle, LineWidthSize, False, True)
        CreateObjectText(chart_ID, objname21, time[ft0], tpt0, CharToString(119), 'Wingdings', TopBottomDotSize, TrendLineUptoDownColor, ANCHOR_CENTER, True)
        CreateObjectText(chart_ID, objname31, time[fb0], tpb0, CharToString(119), 'Wingdings', TopBottomDotSize, TrendLineDowntoUpColor, ANCHOR_CENTER, True)
        if barUp and prvdn == 1:
            prvdn = 0
            objnameDn1p = short_name + ': VerticalLineSwingBarsUp1-' + TimeToString(fb0p1, TIME_DATE | TIME_MINUTES)
            objnameDn2p = short_name + ': VerticalLineSwingBarsUp2-' + TimeToString(ft0p1, TIME_DATE | TIME_MINUTES)
            objname11p = short_name + ': TrendSwingBarsUp1' + TimeToString(fb0p1, TIME_DATE | TIME_MINUTES)
            objname21p = short_name + ': SwingBarsPosTop1p' + TimeToString(ft0p1, TIME_DATE | TIME_MINUTES)
            objname31p = short_name + ': SwingBarsPosBottom1p' + TimeToString(fb0p1, TIME_DATE | TIME_MINUTES)
            CreateObjectVLine(chart_ID, objnameDn1p, fb0p1, VerticalLineColor, LineStyle, LineWidthSize, True)
            CreateObjectVLine(chart_ID, objnameDn2p, ft0p1, VerticalLineColor, LineStyle, LineWidthSize, True)
            CreateObjectTrend(chart_ID, objname11p, fb0p1, tpb0p1, ft0p1, tpt0p1, TrendLineDowntoUpColor, LineStyle, LineWidthSize, False, True)
            CreateObjectText(chart_ID, objname21p, ft0p1, tpt0p1, CharToString(119), 'Wingdings', TopBottomDotSize, TrendLineUptoDownColor, ANCHOR_CENTER, True)
            CreateObjectText(chart_ID, objname31p, fb0p1, tpb0p1, CharToString(119), 'Wingdings', TopBottomDotSize, TrendLineDowntoUpColor, ANCHOR_CENTER, True)
    i = calculated - 2
    while i >= pos:
        _sw1 = AppliedPrice
        if _sw1 == PRICE_CLOSE:
            cpr0 = close[i]
            cpr1 = close[i + 1]
        elif _sw1 == PRICE_OPEN:
            cpr0 = open[i]
            cpr1 = open[i + 1]
        elif _sw1 == PRICE_HIGH:
            cpr0 = high[i]
            cpr1 = high[i + 1]
        elif _sw1 == PRICE_LOW:
            cpr0 = low[i]
            cpr1 = low[i + 1]
        elif _sw1 == PRICE_MEDIAN:
            cpr0 = (high[i] + low[i]) / 2
            cpr1 = (high[i + 1] + low[i + 1]) / 2
        elif _sw1 == PRICE_TYPICAL:
            cpr0 = (high[i] + low[i] + close[i]) / 3
            cpr1 = (high[i + 1] + low[i + 1] + close[i + 1]) / 3
        elif _sw1 == PRICE_WEIGHTED:
            cpr0 = (high[i] + low[i] + close[i] + close[i]) / 4
            cpr1 = (high[i + 1] + low[i + 1] + close[i + 1] + close[i + 1]) / 4
        ExtCPRBuffer[i] = _fdiv(cpr0 - cpl, cph - cpl) * 100
        ExtEMABuffer[i] = _fdiv(ema39[i] - cpl, cph - cpl) * 100
        ma24d[i] = _fdiv(ema24[i] - cpl, cph - cpl) * 100
        ma04d[i] = _fdiv(ema04[i] - cpl, cph - cpl) * 100
        if ma24d[i] > ExtEMABuffer[i]:
            ExtEMABuffUp[i] = ExtEMABuffer[i]
            ExtEMABuffDn[i] = EMPTY_VALUE
            ExtEMABuffWd[i] = EMPTY_VALUE
            arrow = MoveUpColor
        if ma24d[i] < ExtEMABuffer[i]:
            ExtEMABuffDn[i] = ExtEMABuffer[i]
            ExtEMABuffUp[i] = EMPTY_VALUE
            ExtEMABuffWd[i] = EMPTY_VALUE
            arrow = MoveDownColor
        if ma24d[i] > ExtEMABuffer[i] and ma04d[i] > ma04d[i + 1]:
            ExtEMABuffUp[i] = ExtEMABuffer[i]
            ExtEMABuffDn[i] = EMPTY_VALUE
            ExtEMABuffWd[i] = EMPTY_VALUE
            arrow = MoveUpColor
        if ma24d[i] < ExtEMABuffer[i] and ma04d[i] < ma04d[i + 1]:
            ExtEMABuffDn[i] = ExtEMABuffer[i]
            ExtEMABuffUp[i] = EMPTY_VALUE
            ExtEMABuffWd[i] = EMPTY_VALUE
            arrow = MoveDownColor
        if ma24d[i] >= ExtEMABuffer[i] and ExtCPRBuffer[i] > ExtEMABuffer[i]:
            ExtEMABuffUp[i] = ExtEMABuffer[i]
            ExtEMABuffDn[i] = EMPTY_VALUE
            ExtEMABuffWd[i] = ExtEMABuffer[i]
            arrow = WaitDirectionColor
        if ma24d[i] <= ExtEMABuffer[i] and ExtCPRBuffer[i] < ExtEMABuffer[i]:
            ExtEMABuffDn[i] = ExtEMABuffer[i]
            ExtEMABuffUp[i] = EMPTY_VALUE
            ExtEMABuffWd[i] = ExtEMABuffer[i]
            arrow = WaitDirectionColor
        if ExtCPRBuffer[i] >= 76.4 and ExtCPRBuffer[i] < 100.0:
            ExtHPRBuffer[i] = ExtCPRBuffer[i]
            ExtMHPRBuffer[i] = EMPTY_VALUE
            ExtMDPBuffer[i] = EMPTY_VALUE
            ExtMLPRBuffer[i] = EMPTY_VALUE
            ExtLPRBuffer[i] = EMPTY_VALUE
        elif ExtCPRBuffer[i] >= 61.8 and ExtCPRBuffer[i] < 76.4:
            ExtHPRBuffer[i] = EMPTY_VALUE
            ExtMHPRBuffer[i] = ExtCPRBuffer[i]
            ExtMDPBuffer[i] = EMPTY_VALUE
            ExtMLPRBuffer[i] = EMPTY_VALUE
            ExtLPRBuffer[i] = EMPTY_VALUE
        elif ExtCPRBuffer[i] >= 38.2 and ExtCPRBuffer[i] < 61.8:
            ExtHPRBuffer[i] = EMPTY_VALUE
            ExtMHPRBuffer[i] = EMPTY_VALUE
            ExtMDPBuffer[i] = ExtCPRBuffer[i]
            ExtMLPRBuffer[i] = EMPTY_VALUE
            ExtLPRBuffer[i] = EMPTY_VALUE
        elif ExtCPRBuffer[i] >= 23.6 and ExtCPRBuffer[i] < 38.2:
            ExtHPRBuffer[i] = EMPTY_VALUE
            ExtMHPRBuffer[i] = EMPTY_VALUE
            ExtMDPBuffer[i] = EMPTY_VALUE
            ExtMLPRBuffer[i] = ExtCPRBuffer[i]
            ExtLPRBuffer[i] = EMPTY_VALUE
        elif ExtCPRBuffer[i] >= 0.0 and ExtCPRBuffer[i] < 23.6:
            ExtHPRBuffer[i] = EMPTY_VALUE
            ExtMHPRBuffer[i] = EMPTY_VALUE
            ExtMDPBuffer[i] = EMPTY_VALUE
            ExtMLPRBuffer[i] = EMPTY_VALUE
            ExtLPRBuffer[i] = ExtCPRBuffer[i]
        if i == 0:
            if ExtCPRBuffer[i] > ExtCPRBuffer[i + 1]:
                name1 = 'txCons' + _str(x)
                name2 = 'txCons' + _str(x) + 'a'
                name3 = 'txCons' + _str(x) + 'a' + '1'
                ObjectDelete(chart_ID, name1)
                ObjectDelete(chart_ID, name2)
                ObjectDelete(chart_ID, name3)
                CreateObjectLable(chart_ID, name1, 'Wingdings', CharToString(164), 27, RoundedColor, corner, offsetX - 6, scaleYt + offsetY + 29, True)
                CreateObjectLable(chart_ID, name2, 'Wingdings', CharToString(217), 20, arrow, corner, offsetX - 10, scaleYt + offsetY + 15, True)
                if cpr0 > cpr1:
                    CreateObjectLable(chart_ID, name3, 'Bodoni MT Black', 'UP', 7, TextColor, corner, offsetX - 15, scaleYt + offsetY + 62, True)
                else:
                    CreateObjectLable(chart_ID, name3, 'Bodoni MT Black', 'WAIT', 7, TextColor, corner, offsetX - 7, scaleYt + offsetY + 62, True)
            elif ExtCPRBuffer[i] < ExtCPRBuffer[i + 1]:
                name1 = 'txCons' + _str(x)
                name2 = 'txCons' + _str(x) + 'a'
                name3 = 'txCons' + _str(x) + 'a' + '1'
                ObjectDelete(chart_ID, name1)
                ObjectDelete(chart_ID, name2)
                ObjectDelete(chart_ID, name3)
                CreateObjectLable(chart_ID, name1, 'Wingdings', CharToString(164), 27, RoundedColor, corner, offsetX - 6, scaleYt + offsetY + 29, True)
                CreateObjectLable(chart_ID, name2, 'Wingdings', CharToString(218), 20, arrow, corner, offsetX - 10, (3 * scaleYt) + offsetY + 16, True)
                if cpr0 < cpr1:
                    CreateObjectLable(chart_ID, name3, 'Bodoni MT Black', 'DOWN', 7, TextColor, corner, offsetX - 6, scaleYt + offsetY + 21, True)
                else:
                    CreateObjectLable(chart_ID, name3, 'Bodoni MT Black', 'WAIT', 7, TextColor, corner, offsetX - 8, scaleYt + offsetY + 21, True)
            if ((ma04d[i + 1] <= ExtEMABuffer[i + 1] and ma04d[i] > ExtEMABuffer[i]) and cpr0 > cpr1) and ExtEMABuffUp[i] != EMPTY_VALUE:
                cal = 391
            if ((ma04d[i + 1] >= ExtEMABuffer[i + 1] and ma04d[i] < ExtEMABuffer[i]) and cpr0 < cpr1) and ExtEMABuffDn[i] != EMPTY_VALUE:
                cal = 390
            if (((ma04d[i] > ExtEMABuffer[i] and ExtCPRBuffer[i] < 80.0) and cpr0 > cpr1) and ma04d[i] > ma04d[i + 1]) and ExtEMABuffUp[i] != EMPTY_VALUE:
                cal = 393
            if (((ma04d[i] < ExtEMABuffer[i] and ExtCPRBuffer[i] > 20.0) and cpr0 < cpr1) and ma04d[i] < ma04d[i + 1]) and ExtEMABuffDn[i] != EMPTY_VALUE:
                cal = 392
            if ((ExtCPRBuffer[i + 1] < 23.6 and ExtCPRBuffer[i] > 23.6) and ExtEMABuffer[i] > 38.2) and cpr0 > cpr1:
                cal = 395
            if ((ExtCPRBuffer[i + 1] > 76.4 and ExtCPRBuffer[i] < 76.4) and ExtEMABuffer[i] < 61.8) and cpr0 < cpr1:
                cal = 394
            if (((ExtCPRBuffer[i] < 23.6 and inL < inH) and ExtEMABuffer[i] > 61.8) and ma04d[i] > ma04d[i + 1]) and cpr0 > cpr1:
                cal = 397
            if (((ExtCPRBuffer[i] > 76.4 and inH < inL) and ExtEMABuffer[i] < 38.2) and ma04d[i] < ma04d[i + 1]) and cpr0 < cpr1:
                cal = 396
        i -= 1
    ChartRedraw(chart_ID)
    p_alerts(cal)
    return rates_total

def CreateObjectVLine(chart_id, vline_name, vline_time, vline_color, vline_style, vline_width, vline_hidden):
    if ObjectCreate(chart_id, vline_name, OBJ_VLINE, 0, vline_time, 0):
        ObjectSetInteger(chart_id, vline_name, OBJPROP_COLOR, vline_color)
        ObjectSetInteger(chart_id, vline_name, OBJPROP_STYLE, vline_style)
        ObjectSetInteger(chart_id, vline_name, OBJPROP_WIDTH, vline_width)
        ObjectSetInteger(chart_id, vline_name, OBJPROP_HIDDEN, vline_hidden)
    else:
        Print('Failed to create the object OBJ_VLINE ', vline_name, ', Error code = ', GetLastError())

def CreateObjectTrend(chart_id, trend_name, trend_time1, trend_price1, trend_time2, trend_price2, trend_color, trend_style, trend_width, trend_ray_r, trend_hidden):
    if ObjectCreate(chart_id, trend_name, OBJ_TREND, 0, trend_time1, trend_price1, trend_time2, trend_price2):
        ObjectSetInteger(chart_id, trend_name, OBJPROP_COLOR, trend_color)
        ObjectSetInteger(chart_id, trend_name, OBJPROP_STYLE, trend_style)
        ObjectSetInteger(chart_id, trend_name, OBJPROP_WIDTH, trend_width)
        ObjectSetInteger(chart_id, trend_name, OBJPROP_RAY_RIGHT, trend_ray_r)
        ObjectSetInteger(chart_id, trend_name, OBJPROP_HIDDEN, trend_hidden)
    else:
        Print('Failed to create the object OBJ_TREND ', trend_name, ', Error code = ', GetLastError())

def CreateObjectText(chart_id, text_name, text_time1, text_price1, text_obj_text, text_font_model, text_font_size, text_color, text_anchor, text_hidden):
    if ObjectCreate(chart_ID, text_name, OBJ_TEXT, 0, text_time1, text_price1):
        ObjectSetString(chart_id, text_name, OBJPROP_TEXT, text_obj_text)
        ObjectSetString(chart_id, text_name, OBJPROP_FONT, text_font_model)
        ObjectSetInteger(chart_id, text_name, OBJPROP_FONTSIZE, text_font_size)
        ObjectSetInteger(chart_id, text_name, OBJPROP_COLOR, text_color)
        ObjectSetInteger(chart_id, text_name, OBJPROP_ANCHOR, text_anchor)
        ObjectSetInteger(chart_id, text_name, OBJPROP_HIDDEN, text_hidden)
    else:
        Print('Failed to create the object OBJ_TEXT ', text_name, ', Error code = ', GetLastError())

def CreateObjectLable(chart_id, lable_name, lable_font_model, lable_obj_text, lable_font_size, lable_color, lable_corner, lable_xdist, lable_ydist, lable_hidden):
    if ObjectCreate(chart_id, lable_name, OBJ_LABEL, 1, 0, 0):
        ObjectSetString(chart_id, lable_name, OBJPROP_FONT, lable_font_model)
        ObjectSetString(chart_id, lable_name, OBJPROP_TEXT, lable_obj_text)
        ObjectSetInteger(chart_id, lable_name, OBJPROP_FONTSIZE, lable_font_size)
        ObjectSetInteger(chart_id, lable_name, OBJPROP_COLOR, lable_color)
        ObjectSetInteger(chart_id, lable_name, OBJPROP_CORNER, lable_corner)
        ObjectSetInteger(chart_id, lable_name, OBJPROP_XDISTANCE, lable_xdist)
        ObjectSetInteger(chart_id, lable_name, OBJPROP_YDISTANCE, lable_ydist)
        ObjectSetInteger(chart_id, lable_name, OBJPROP_HIDDEN, lable_hidden)
    else:
        Print('Failed to create the object OBJ_LABEL ', lable_name, ', Error code = ', GetLastError())

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

def Do_Alerts(msgText, eMailSub):
    if MsgAlerts:
        Alert(msgText)
    if SoundAlerts:
        PlaySound(SoundAlertFile)
    if eMailAlerts:
        SendMail(eMailSub, msgText)

def strTF(tf):
    _sw3 = tf
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
        return 'MN1'
    return 'Unknown TF'

def p_alerts(alert):
    global alBase, alMsg, alSubj, cmnt, pal, pmnt
    cmnt = MqlReturnDateTime(TimeCurrent(), min_)
    if cmnt != pmnt:
        if cal != pal and alert == 391:
            alBase = short_name + ' @ ' + TimeToString(TimeCurrent(), TIME_MINUTES | TIME_SECONDS)
            alSubj = alBase + '. The Price Goes Up,'
            alMsg = alSubj + ' Action: Open BUY.!!'
            pmnt = cmnt
            pal = cal
            Do_Alerts(alMsg, alSubj)
        if cal != pal and alert == 390:
            alBase = short_name + ' @ ' + TimeToString(TimeCurrent(), TIME_MINUTES | TIME_SECONDS)
            alSubj = alBase + '. The Price Goes Down,'
            alMsg = alSubj + ' Action: Open SELL.!!'
            pmnt = cmnt
            pal = cal
            Do_Alerts(alMsg, alSubj)
        if cal != pal and alert == 393:
            alBase = short_name + ' @ ' + TimeToString(TimeCurrent(), TIME_MINUTES | TIME_SECONDS)
            alSubj = alBase + '. The Price Goes Up,'
            alMsg = alSubj + ' Action: Open BUY.!!'
            pmnt = cmnt
            pal = cal
            Do_Alerts(alMsg, alSubj)
        if cal != pal and alert == 392:
            alBase = short_name + ' @ ' + TimeToString(TimeCurrent(), TIME_MINUTES | TIME_SECONDS)
            alSubj = alBase + '. The Price Goes Down,'
            alMsg = alSubj + ' Action: Open SELL.!!'
            pmnt = cmnt
            pal = cal
            Do_Alerts(alMsg, alSubj)
        if cal != pal and alert == 395:
            alBase = short_name + ' @ ' + TimeToString(TimeCurrent(), TIME_MINUTES | TIME_SECONDS)
            alSubj = alBase + '. The Price Goes Up,'
            alMsg = alSubj + ' Action: Open BUY.!!'
            pmnt = cmnt
            pal = cal
            Do_Alerts(alMsg, alSubj)
        if cal != pal and alert == 394:
            alBase = short_name + ' @ ' + TimeToString(TimeCurrent(), TIME_MINUTES | TIME_SECONDS)
            alSubj = alBase + '. The Price Goes Down,'
            alMsg = alSubj + ' Action: Open SELL.!!'
            pmnt = cmnt
            pal = cal
            Do_Alerts(alMsg, alSubj)
        if cal != pal and alert == 397:
            alBase = short_name + ' @ ' + TimeToString(TimeCurrent(), TIME_MINUTES | TIME_SECONDS)
            alSubj = alBase + '. The Price Goes Up,'
            alMsg = alSubj + ' Action: Open BUY.!!'
            pmnt = cmnt
            pal = cal
            Do_Alerts(alMsg, alSubj)
        if cal != pal and alert == 396:
            alBase = short_name + ' @ ' + TimeToString(TimeCurrent(), TIME_MINUTES | TIME_SECONDS)
            alSubj = alBase + '. The Price Goes Down,'
            alMsg = alSubj + ' Action: Open SELL.!!'
            pmnt = cmnt
            pal = cal
            Do_Alerts(alMsg, alSubj)
    return


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PricePercentRange(_MQL5Indicator):
    name = 'PricePercentRange'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # AppliedPrice
        'SoundAlerts': True,
        'MsgAlerts': True,
        'eMailAlerts': False,
        'LineWidthSize': 1,
        'LineStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),
        'TextPosition': _Choice({0: 'ANCHOR_LEFT_UPPER', 1: 'ANCHOR_LEFT', 2: 'ANCHOR_LEFT_LOWER', 3: 'ANCHOR_LOWER', 4: 'ANCHOR_RIGHT_LOWER', 5: 'ANCHOR_RIGHT', 6: 'ANCHOR_RIGHT_UPPER', 7: 'ANCHOR_UPPER', 8: 'ANCHOR_CENTER'}, default=5),
        'TextFontSize': 8,
        'TopBottomDotSize': 15,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

