"""igdr_fractal_levels — converted from MQL5: MQL5 Indicators/iGDR_Fractal_Levels/igdr_fractal_levels.mq5

Copyright: Copyright © 2008-2009, GreenDog; Link: krot@inbox.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008-2009, GreenDog', 'link': 'krot@inbox.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'igdr_fractal_levels', 'source': 'MQL5 Indicators/iGDR_Fractal_Levels/igdr_fractal_levels.mq5', 'folder': 'iGDR_Fractal_Levels', 'inputs': [{'mql': 'frNum_', 'py': 'frNum_', 'param': 'frNum_', 'type': 'uint', 'default': 2, 'label': 'Number of fractal bars, 2=5 bar fractal, 3=7 bar etc.', 'sinput': False}, {'mql': 'frType', 'py': 'frType', 'param': 'frType', 'type': 'int', 'default': 1, 'label': 'Fractal specifying type 0=strict, 1=not strict', 'sinput': False}, {'mql': 'frMode', 'py': 'frMode', 'param': 'frMode', 'type': 'int', 'default': 0, 'label': 'Mode', 'sinput': False}, {'mql': 'dlt_', 'py': 'dlt_', 'param': 'dlt_', 'type': 'double', 'default': 0.24, 'label': 'Inaccuracy measure from the bars average height', 'sinput': False}, {'mql': 'sBars_', 'py': 'sBars_', 'param': 'sBars_', 'type': 'uint', 'default': 200, 'label': 'Number of bars (not more than 200)', 'sinput': False}, {'mql': 'BG1_Color', 'py': 'BG1_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'First levels background color', 'sinput': False}, {'mql': 'TL1Color', 'py': 'TL1Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'First levels lines color', 'sinput': False}, {'mql': 'BG2_Color', 'py': 'BG2_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Second levels background color', 'sinput': False}, {'mql': 'TL2Color', 'py': 'TL2Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Second levels lines color', 'sinput': False}, {'mql': 'BG3_Color', 'py': 'BG3_Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Third levels background color', 'sinput': False}, {'mql': 'TL3Color', 'py': 'TL3Color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Third levels lines color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

DarkOrange = 0x008CFF  # MQL4 colour name
Green = 0x008000  # MQL4 colour name
PaleGreen = 0x98FB98  # MQL4 colour name
Pink = 0xCBC0FF  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name
Yellow = 0x00FFFF  # MQL4 colour name

# enum FRACTAL_MODE
MODE_HIGH_LOW = 0
MODE_LOW = 1
MODE_HIGH = 2
_enum('FRACTAL_MODE', {0: 'MODE_HIGH_LOW', 1: 'MODE_LOW', 2: 'MODE_HIGH'})

# enum FRACTAL_TYPE
TYPE1 = 0
TYPE2 = 1
_enum('FRACTAL_TYPE', {0: 'TYPE1', 1: 'TYPE2'})

# ---- inputs and global variables
frNum_ = _input('frNum_', 2)  # Number of fractal bars, 2=5 bar fractal, 3=7 bar etc.
frType = _input('frType', TYPE2)  # Fractal specifying type 0=strict, 1=not strict
frMode = _input('frMode', MODE_HIGH_LOW)  # Mode
dlt_ = _input('dlt_', 0.24)  # Inaccuracy measure from the bars average height
sBars_ = _input('sBars_', 200)  # Number of bars (not more than 200)
lastBars = 0
frNum = 0
sBars = 0
lastTime = 0
BGColor = Arr(3, 0, dyn=False)
TLColor = Arr(3, 0, dyn=False)
aData = Arr(240, 0.0, dyn=False, dims=(2,))
aRes = Arr(3, 0.0, dyn=False, dims=(2,))

def OnInit():
    global frNum, sBars
    frNum = frNum_
    if frNum_ < 2:
        frNum = 2
    sBars = sBars_
    if sBars_ > 200:
        sBars = 200
    if sBars_ < 10:
        sBars = 10
    BGColor[0] = BG1_Color
    BGColor[1] = BG2_Color
    BGColor[2] = BG3_Color
    TLColor[0] = TL1Color
    TLColor[1] = TL2Color
    TLColor[2] = TL3Color

def CreateTextLabel(chart_id, name, nwin, time1, price1, Color, text, font, fontsize):
    ObjectCreate(chart_id, name, OBJ_TEXT, nwin, time1, price1)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(chart_id, name, OBJPROP_ZORDER, True)
    ObjectSetString(chart_id, name, OBJPROP_FONT, font)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, fontsize)

def SetTextLabel(chart_id, name, nwin, time1, price1, Color, style, width, text, font, fontsize):
    if ObjectFind(chart_id, name) == -1:
        CreateTextLabel(chart_id, name, nwin, time1, price1, Color, text, font, fontsize)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)

def CreateChannel(chart_id, name, nwin, time1, price1, time2, price2, time3, price3, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_CHANNEL, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_FILL, True)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, True)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(chart_id, name, OBJPROP_ZORDER, True)

def SetChannel(chart_id, name, nwin, time1, price1, time2, price2, time3, price3, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateChannel(chart_id, name, nwin, time1, price1, time2, price2, time3, price3, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)
        ObjectMove(chart_id, name, 2, time3, price3)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)

def CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_TREND, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, False)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, True)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(chart_id, name, OBJPROP_ZORDER, True)

def SetTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)

def upFrac(cnt, High):
    for i in range(1, _int(frNum) + 1):
        if frType == TYPE1:
            if High[cnt + i] >= High[cnt + i - 1] or High[cnt - i] >= High[cnt - i + 1]:
                return False
        else:
            if High[cnt + i] > High[cnt] or High[cnt - i] > High[cnt]:
                return False
    return True

def dwFrac(cnt, Low):
    for i in range(1, _int(frNum) + 1):
        if frType == TYPE1:
            if Low[cnt + i] <= Low[cnt + i - 1] or Low[cnt - i] <= Low[cnt - i + 1]:
                return False
        else:
            if Low[cnt + i] < Low[cnt] or Low[cnt - i] < Low[cnt]:
                return False
    return True

def OnDeinit(reason):
    Comment('')
    for i in range(0, 3):
        name = 'IPGDR_Lv' + _str(i)
        ObjectDelete(0, name)
        ObjectDelete(0, name + 'Up')
        ObjectDelete(0, name + 'Dw')
        ObjectDelete(0, name + 'Tx')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global lastBars
    if rates_total < _int(sBars):
        return 0
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    lastBars = rates_total
    sh = 0
    ArrayInitialize(aData, 0)
    lastExt = 0.0
    total = _int(sBars - (2 * frNum))
    start = _int(frNum + 1)
    for i in range(start, total):
        if frMode != MODE_LOW and upFrac(i, high):
            if not ((frType != TYPE1 and lastExt > 0) and lastExt == high[i]):
                aData[sh][0] = high[i]
                lastExt = high[i]
                sh += 1
        if sh >= 240:
            break
        if frMode != MODE_HIGH and dwFrac(i, low):
            if ((not frType) != TYPE1 and lastExt > 0) and lastExt == low[i]:
                aData[sh][0] = low[i]
                lastExt = low[i]
                sh += 1
        if sh >= 240:
            break
    dlt = 0.0
    sHL = 0.0
    for i in range(1, _int(sBars) + 1):
        sHL += high[i] - low[i]
    sHL = _fdiv(sHL, sBars)
    dlt = sHL * dlt_
    for i in range(0, sh):
        for j in range(i + 1, sh):
            if aData[j][0] > (aData[i][0] - dlt) and aData[j][0] < (aData[i][0] + dlt):
                aData[i][1] += 1
                aData[j][1] += 1
    cur = Arr(2, 0.0, dyn=False)
    tmp = Arr(2, 0.0, dyn=False)
    aRes[0][0] = aData[0][0]
    aRes[0][1] = aData[0][1]
    for i in range(1, sh):
        cur[0] = aData[i][0]
        cur[1] = aData[i][1]
        if cur[1] > aRes[0][1]:
            tmp[0] = aRes[0][0]
            tmp[1] = aRes[0][1]
            aRes[0][0] = cur[0]
            aRes[0][1] = cur[1]
            cur[0] = tmp[0]
            cur[1] = tmp[1]
        if cur[1] > aRes[1][1] and (cur[0] < (aRes[0][0] - dlt) or cur[0] > (aRes[0][0] + dlt)):
            tmp[0] = aRes[1][0]
            tmp[1] = aRes[1][1]
            aRes[1][0] = cur[0]
            aRes[1][1] = cur[1]
            cur[0] = tmp[0]
            cur[1] = tmp[1]
        if (cur[1] > aRes[2][1] and (cur[0] < (aRes[0][0] - dlt) or cur[0] > (aRes[0][0] + dlt))) and (cur[0] < (aRes[1][0] - dlt) or cur[0] > (aRes[1][0] + dlt)):
            aRes[2][0] = cur[0]
            aRes[2][1] = cur[1]
    for i in range(0, 3):
        dwL = aRes[i][0] - dlt
        upL = aRes[i][0] + dlt
        name = 'IPGDR_Lv' + _str(i)
        SetChannel(0, name, 0, time[24], upL, time[1], upL, time[24], dwL, BGColor[i], STYLE_SOLID, 1, name)
        SetTline(0, name + 'Up', 0, time[24], upL, time[1], upL, TLColor[i], STYLE_SOLID, 1, name + 'Up')
        SetTline(0, name + 'Dw', 0, time[24], dwL, time[1], dwL, TLColor[i], STYLE_SOLID, 1, name + 'Dw')
        SetTextLabel(0, name + 'Tx', 0, time[32], upL + (2 * Point()), TLColor[i], STYLE_SOLID, 1, DoubleToString(aRes[i][0], Digits()), 'tahoma', 14)
    rem1 = ''
    rem2 = Box('')
    if frType == TYPE2:
        rem1 = rem1 + 'Standard '
    else:
        rem1 = rem1 + 'Strict '
    rem1 = rem1 + _str((frNum * 2) + 1) + ' bar fractals'
    if frMode == MODE_LOW:
        rem1 = rem1 + ', bottoms'
    elif frMode == MODE_HIGH:
        rem1 = rem1 + ', tops'
    rem1 = rem1 + '\nFound ' + _str(sh) + ' fractals \nThe strongest levels '
    StringConcatenate(rem2, aRes[0][0], '[', aRes[0][1], '], ', aRes[1][0], '[', aRes[1][1], '], ', aRes[2][0], '[', aRes[2][1], '], inaccuracy measure ±', NormalizeDouble(_fdiv(dlt, Point()), 1), ' points')
    Comment(rem1 + rem2.v)
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
BG1_Color = _input('BG1_Color', _uint(PaleGreen))  # First levels background color
TL1Color = _input('TL1Color', _uint(Green))  # First levels lines color
BG2_Color = _input('BG2_Color', _uint(Yellow))  # Second levels background color
TL2Color = _input('TL2Color', _uint(DarkOrange))  # Second levels lines color
BG3_Color = _input('BG3_Color', _uint(Pink))  # Third levels background color
TL3Color = _input('TL3Color', _uint(Red))  # Third levels lines color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IgdrFractalLevels(_MQL5Indicator):
    name = 'igdr_fractal_levels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'frNum_': 2,  # Number of fractal bars, 2=5 bar fractal, 3=7 bar etc.
        'frType': _Choice({0: 'strict', 1: 'not strict'}, default=1),  # Fractal specifying type 0=strict, 1=not strict
        'frMode': _Choice({0: 'by extremums', 1: 'by tops', 2: 'by bottoms'}, default=0),  # Mode
        'dlt_': 0.24,  # Inaccuracy measure from the bars average height
        'sBars_': 200,  # Number of bars (not more than 200)
    }

