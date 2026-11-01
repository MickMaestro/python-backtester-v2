"""pivot_lines_timezone — converted from MQL5: MQL5 Indicators/Pivot Lines TimeZone/pivot_lines_timezone.mq5

Expert rewritten from MQL4, the author: Alejandro Galindo, published on mql4.com by Scriptor (http://www.mql4.com/ru/users/Scriptor), link - http://codebase.mql4.com/ru/1395
Copyright: Integer; Link: https://login.mql5.com/ru/users/Integer; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Integer', 'link': 'https://login.mql5.com/ru/users/Integer', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 19, 'indicator_plots': 17}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1}, 'colors': {1: [36095], 2: [255], 3: [16760576], 4: [255], 5: [16760576], 6: [255], 7: [16760576], 8: [16711680], 9: [16711680], 10: [16711680], 11: [16711680], 12: [16711680], 13: [16711680], 14: [65535], 15: [65535], 16: [65535], 17: [65535]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0}, 'labels': {1: 'Pivot', 2: 'S1', 3: 'R1', 4: 'S2', 5: 'R2', 6: 'S3', 7: 'R3', 8: 'M0', 9: 'M1', 10: 'M2', 11: 'M3', 12: 'M4', 13: 'M5', 14: 'L3', 15: 'H3', 16: 'L4', 17: 'H4'}, 'levels': [], 'description': ['', 'Expert rewritten from MQL4, the author: Alejandro Galindo, published on mql4.com by Scriptor (http://www.mql4.com/ru/users/Scriptor), link - http://codebase.mql4.com/ru/1395'], 'name': 'pivot_lines_timezone', 'source': 'MQL5 Indicators/Pivot Lines TimeZone/pivot_lines_timezone.mq5', 'folder': 'Pivot Lines TimeZone', 'inputs': [{'mql': 'DayStartHour', 'py': 'DayStartHour', 'param': 'DayStartHour', 'type': 'int', 'default': 0, 'label': 'DayStartHour', 'sinput': False}, {'mql': 'DayStartMinute', 'py': 'DayStartMinute', 'param': 'DayStartMinute', 'type': 'int', 'default': 0, 'label': 'DayStartMinute', 'sinput': False}, {'mql': 'PivotsBufers', 'py': 'PivotsBufers', 'param': 'PivotsBufers', 'type': 'bool', 'default': False, 'label': 'PivotsBufers', 'sinput': False}, {'mql': 'MidpivotsBuffers', 'py': 'MidpivotsBuffers', 'param': 'MidpivotsBuffers', 'type': 'bool', 'default': False, 'label': 'MidpivotsBuffers', 'sinput': False}, {'mql': 'CamarillaBuffers', 'py': 'CamarillaBuffers', 'param': 'CamarillaBuffers', 'type': 'bool', 'default': False, 'label': 'CamarillaBuffers', 'sinput': False}, {'mql': 'PivotsLines', 'py': 'PivotsLines', 'param': 'PivotsLines', 'type': 'bool', 'default': True, 'label': 'PivotsLines', 'sinput': False}, {'mql': 'MidpivotsLines', 'py': 'MidpivotsLines', 'param': 'MidpivotsLines', 'type': 'bool', 'default': False, 'label': 'MidpivotsLines', 'sinput': False}, {'mql': 'CamarillaLines', 'py': 'CamarillaLines', 'param': 'CamarillaLines', 'type': 'bool', 'default': False, 'label': 'CamarillaLines', 'sinput': False}, {'mql': 'ClrPivot', 'py': 'ClrPivot', 'param': None, 'type': 'color', 'default': 42495, 'label': 'ClrPivot', 'sinput': False}, {'mql': 'ClrS', 'py': 'ClrS', 'param': None, 'type': 'color', 'default': 255, 'label': 'ClrS', 'sinput': False}, {'mql': 'ClrR', 'py': 'ClrR', 'param': None, 'type': 'color', 'default': 16760576, 'label': 'ClrR', 'sinput': False}, {'mql': 'ClrM', 'py': 'ClrM', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'ClrM', 'sinput': False}, {'mql': 'ClrCamarilla', 'py': 'ClrCamarilla', 'param': None, 'type': 'color', 'default': 65535, 'label': 'ClrCamarilla', 'sinput': False}, {'mql': 'ClrTxt', 'py': 'ClrTxt', 'param': None, 'type': 'color', 'default': 16777215, 'label': 'ClrTxt', 'sinput': False}, {'mql': 'AttachSundToMond', 'py': 'AttachSundToMond', 'param': 'AttachSundToMond', 'type': 'bool', 'default': True, 'label': 'AttachSundToMond', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

OBJ_ALL_PERIODS = 0  # MQL5 constant unknown to the converter
Red = 0x0000FF  # MQL4 colour name

# ---- inputs and global variables
DayStartHour = _input('DayStartHour', 0)  # DayStartHour
DayStartMinute = _input('DayStartMinute', 0)  # DayStartMinute
PivotsBufers = _input('PivotsBufers', False)  # PivotsBufers
MidpivotsBuffers = _input('MidpivotsBuffers', False)  # MidpivotsBuffers
CamarillaBuffers = _input('CamarillaBuffers', False)  # CamarillaBuffers
PivotsLines = _input('PivotsLines', True)  # PivotsLines
MidpivotsLines = _input('MidpivotsLines', False)  # MidpivotsLines
CamarillaLines = _input('CamarillaLines', False)  # CamarillaLines
ClrPivot = _input('ClrPivot', clrOrange)  # ClrPivot
ClrS = _input('ClrS', clrRed)  # ClrS
ClrR = _input('ClrR', clrDeepSkyBlue)  # ClrR
ClrM = _input('ClrM', clrBlue)  # ClrM
ClrCamarilla = _input('ClrCamarilla', clrYellow)  # ClrCamarilla
ClrTxt = _input('ClrTxt', clrWhite)  # ClrTxt
AttachSundToMond = _input('AttachSundToMond', True)  # AttachSundToMond
PivotBuffer = Arr(0, 0.0)
S1Buffer = Arr(0, 0.0)
R1Buffer = Arr(0, 0.0)
S2Buffer = Arr(0, 0.0)
R2Buffer = Arr(0, 0.0)
S3Buffer = Arr(0, 0.0)
R3Buffer = Arr(0, 0.0)
M0Buffer = Arr(0, 0.0)
M1Buffer = Arr(0, 0.0)
M2Buffer = Arr(0, 0.0)
M3Buffer = Arr(0, 0.0)
M4Buffer = Arr(0, 0.0)
M5Buffer = Arr(0, 0.0)
H3Buffer = Arr(0, 0.0)
L3Buffer = Arr(0, 0.0)
H4Buffer = Arr(0, 0.0)
L4Buffer = Arr(0, 0.0)
BufHigh = Arr(0, 0.0)
BufLow = Arr(0, 0.0)
TimeShift = 0
P = 0.0
R1 = 0.0
S1 = 0.0
R2 = 0.0
S2 = 0.0
R3 = 0.0
S3 = 0.0
Q = 0.0
H4 = 0.0
H3 = 0.0
L3 = 0.0
L4 = 0.0
M5 = 0.0
M4 = 0.0
M3 = 0.0
M2 = 0.0
M1 = 0.0
M0 = 0.0
Redr = False

def OnInit():
    global Redr, TimeShift
    if PivotsLines:
        fObjHLine('Pivot', 0.0, 'Pivot', 0, ClrPivot, 1, STYLE_DOT, 0, True, False, False, _long(OBJ_ALL_PERIODS))
        fObjHLine('S1', 0.0, 'S1', 0, ClrS, 1, STYLE_DASHDOTDOT, 0, True, False, False, _long(OBJ_ALL_PERIODS))
        fObjHLine('R1', 0.0, 'R1', 0, ClrR, 1, STYLE_DASHDOTDOT, 0, True, False, False, _long(OBJ_ALL_PERIODS))
        fObjHLine('S2', 0.0, 'S2', 0, ClrS, 1, STYLE_DASHDOTDOT, 0, True, False, False, _long(OBJ_ALL_PERIODS))
        fObjHLine('R2', 0.0, 'R2', 0, ClrR, 1, STYLE_DASHDOTDOT, 0, True, False, False, _long(OBJ_ALL_PERIODS))
        fObjHLine('S3', 0.0, 'S3', 0, ClrS, 1, STYLE_DASHDOTDOT, 0, True, False, False, _long(OBJ_ALL_PERIODS))
        fObjHLine('R3', 0.0, 'R3', 0, ClrR, 1, STYLE_DASHDOTDOT, 0, True, False, False, _long(OBJ_ALL_PERIODS))
        fObjText('TxtPivot', 0, 0.0, 'P', 0, ANCHOR_LEFT_UPPER, ClrTxt, 8, 'Arial', 0, False, 0.0, False, False, _long(OBJ_ALL_PERIODS))
        fObjText('TxtS1', 0, 0.0, 'S1', 0, ANCHOR_LEFT_UPPER, ClrTxt, 8, 'Arial', 0, False, 0.0, False, False, _long(OBJ_ALL_PERIODS))
        fObjText('TxtR1', 0, 0.0, 'R1', 0, ANCHOR_LEFT_UPPER, ClrTxt, 8, 'Arial', 0, False, 0.0, False, False, _long(OBJ_ALL_PERIODS))
        fObjText('TxtS2', 0, 0.0, 'S2', 0, ANCHOR_LEFT_UPPER, ClrTxt, 8, 'Arial', 0, False, 0.0, False, False, _long(OBJ_ALL_PERIODS))
        fObjText('TxtR2', 0, 0.0, 'R2', 0, ANCHOR_LEFT_UPPER, ClrTxt, 8, 'Arial', 0, False, 0.0, False, False, _long(OBJ_ALL_PERIODS))
        fObjText('TxtS3', 0, 0.0, 'S3', 0, ANCHOR_LEFT_UPPER, ClrTxt, 8, 'Arial', 0, False, 0.0, False, False, _long(OBJ_ALL_PERIODS))
        fObjText('TxtR3', 0, 0.0, 'R3', 0, ANCHOR_LEFT_UPPER, ClrTxt, 8, 'Arial', 0, False, 0.0, False, False, _long(OBJ_ALL_PERIODS))
    if MidpivotsLines:
        fObjHLine('M0', 0.0, 'M0', 0, ClrM, 1, STYLE_DASHDOTDOT, 0, True, False, False, _long(OBJ_ALL_PERIODS))
        fObjHLine('M1', 0.0, 'M1', 0, ClrM, 1, STYLE_DASHDOTDOT, 0, True, False, False, _long(OBJ_ALL_PERIODS))
        fObjHLine('M2', 0.0, 'M2', 0, ClrM, 1, STYLE_DASHDOTDOT, 0, True, False, False, _long(OBJ_ALL_PERIODS))
        fObjHLine('M3', 0.0, 'M3', 0, ClrM, 1, STYLE_DASHDOTDOT, 0, True, False, False, _long(OBJ_ALL_PERIODS))
        fObjHLine('M4', 0.0, 'M4', 0, ClrM, 1, STYLE_DASHDOTDOT, 0, True, False, False, _long(OBJ_ALL_PERIODS))
        fObjHLine('M5', 0.0, 'M5', 0, ClrM, 1, STYLE_DASHDOTDOT, 0, True, False, False, _long(OBJ_ALL_PERIODS))
        fObjText('TxtM0', 0, 0.0, 'M0', 0, ANCHOR_LEFT_UPPER, ClrTxt, 8, 'Arial', 0, False, 0.0, False, False, _long(OBJ_ALL_PERIODS))
        fObjText('TxtM1', 0, 0.0, 'M1', 0, ANCHOR_LEFT_UPPER, ClrTxt, 8, 'Arial', 0, False, 0.0, False, False, _long(OBJ_ALL_PERIODS))
        fObjText('TxtM2', 0, 0.0, 'M2', 0, ANCHOR_LEFT_UPPER, ClrTxt, 8, 'Arial', 0, False, 0.0, False, False, _long(OBJ_ALL_PERIODS))
        fObjText('TxtM3', 0, 0.0, 'M3', 0, ANCHOR_LEFT_UPPER, ClrTxt, 8, 'Arial', 0, False, 0.0, False, False, _long(OBJ_ALL_PERIODS))
        fObjText('TxtM4', 0, 0.0, 'M4', 0, ANCHOR_LEFT_UPPER, ClrTxt, 8, 'Arial', 0, False, 0.0, False, False, _long(OBJ_ALL_PERIODS))
        fObjText('TxtM5', 0, 0.0, 'M5', 0, ANCHOR_LEFT_UPPER, ClrTxt, 8, 'Arial', 0, False, 0.0, False, False, _long(OBJ_ALL_PERIODS))
    if CamarillaLines:
        fObjHLine('L3', 0.0, 'L3', 0, ClrCamarilla, 1, STYLE_DASHDOTDOT, 0, True, False, False, _long(OBJ_ALL_PERIODS))
        fObjHLine('H3', 0.0, 'H3', 0, ClrCamarilla, 1, STYLE_DASHDOTDOT, 0, True, False, False, _long(OBJ_ALL_PERIODS))
        fObjHLine('L4', 0.0, 'L4', 0, ClrCamarilla, 1, STYLE_DASHDOTDOT, 0, True, False, False, _long(OBJ_ALL_PERIODS))
        fObjHLine('H4', 0.0, 'H4', 0, ClrCamarilla, 1, STYLE_DASHDOTDOT, 0, True, False, False, _long(OBJ_ALL_PERIODS))
        fObjText('TxtL3', 0, 0.0, 'L3', 0, ANCHOR_LEFT_UPPER, ClrTxt, 8, 'Arial', 0, False, 0.0, False, False, _long(OBJ_ALL_PERIODS))
        fObjText('TxtH3', 0, 0.0, 'H3', 0, ANCHOR_LEFT_UPPER, ClrTxt, 8, 'Arial', 0, False, 0.0, False, False, _long(OBJ_ALL_PERIODS))
        fObjText('TxtL4', 0, 0.0, 'L4', 0, ANCHOR_LEFT_UPPER, ClrTxt, 8, 'Arial', 0, False, 0.0, False, False, _long(OBJ_ALL_PERIODS))
        fObjText('TxtH4', 0, 0.0, 'H4', 0, ANCHOR_LEFT_UPPER, ClrTxt, 8, 'Arial', 0, False, 0.0, False, False, _long(OBJ_ALL_PERIODS))
    Redr = (PivotsLines or MidpivotsLines) or CamarillaLines
    TimeShift = (DayStartHour * 3600) + (DayStartMinute * 60)
    SetIndexBuffer(0, PivotBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, S1Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, R1Buffer, INDICATOR_DATA)
    SetIndexBuffer(3, S2Buffer, INDICATOR_DATA)
    SetIndexBuffer(4, R2Buffer, INDICATOR_DATA)
    SetIndexBuffer(5, S3Buffer, INDICATOR_DATA)
    SetIndexBuffer(6, R3Buffer, INDICATOR_DATA)
    SetIndexBuffer(7, M0Buffer, INDICATOR_DATA)
    SetIndexBuffer(8, M1Buffer, INDICATOR_DATA)
    SetIndexBuffer(9, M2Buffer, INDICATOR_DATA)
    SetIndexBuffer(10, M3Buffer, INDICATOR_DATA)
    SetIndexBuffer(11, M4Buffer, INDICATOR_DATA)
    SetIndexBuffer(12, M5Buffer, INDICATOR_DATA)
    SetIndexBuffer(13, L3Buffer, INDICATOR_DATA)
    SetIndexBuffer(14, H3Buffer, INDICATOR_DATA)
    SetIndexBuffer(15, L4Buffer, INDICATOR_DATA)
    SetIndexBuffer(16, H4Buffer, INDICATOR_DATA)
    SetIndexBuffer(17, BufHigh, INDICATOR_CALCULATIONS)
    SetIndexBuffer(18, BufLow, INDICATOR_CALCULATIONS)
    return 0

def OnDeinit(Rason):
    if PivotsLines:
        ObjectDelete(0, 'Pivot')
        ObjectDelete(0, 'S1')
        ObjectDelete(0, 'R1')
        ObjectDelete(0, 'S2')
        ObjectDelete(0, 'R2')
        ObjectDelete(0, 'S3')
        ObjectDelete(0, 'R3')
        ObjectDelete(0, 'TxtPivot')
        ObjectDelete(0, 'TxtS1')
        ObjectDelete(0, 'TxtR1')
        ObjectDelete(0, 'TxtS2')
        ObjectDelete(0, 'TxtR2')
        ObjectDelete(0, 'TxtS3')
        ObjectDelete(0, 'TxtR3')
    if MidpivotsLines:
        ObjectDelete(0, 'M0')
        ObjectDelete(0, 'M1')
        ObjectDelete(0, 'M2')
        ObjectDelete(0, 'M3')
        ObjectDelete(0, 'M4')
        ObjectDelete(0, 'M5')
        ObjectDelete(0, 'TxtM0')
        ObjectDelete(0, 'TxtM1')
        ObjectDelete(0, 'TxtM2')
        ObjectDelete(0, 'TxtM3')
        ObjectDelete(0, 'TxtM4')
        ObjectDelete(0, 'TxtM5')
    if CamarillaLines:
        ObjectDelete(0, 'L3')
        ObjectDelete(0, 'H3')
        ObjectDelete(0, 'L4')
        ObjectDelete(0, 'H4')
        ObjectDelete(0, 'TxtL3')
        ObjectDelete(0, 'TxtH3')
        ObjectDelete(0, 'TxtL4')
        ObjectDelete(0, 'TxtH4')
    if Redr:
        ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global H3, H4, L3, L4, M0, M1, M2, M3, M4, M5, P, Q, R1, R2, R3, S1, S2, S3, _s_OnCalculate_error
    start = 0
    if prev_calculated == 0:
        _s_OnCalculate_error = True
    if _s_OnCalculate_error:
        start = 1
        _s_OnCalculate_error = False
    else:
        start = prev_calculated - 1
    for i in range(start, rates_total):
        BufHigh[i] = BufHigh[i - 1]
        BufLow[i] = BufLow[i - 1]
        PivotBuffer[i] = PivotBuffer[i - 1]
        S1Buffer[i] = S1Buffer[i - 1]
        R1Buffer[i] = R1Buffer[i - 1]
        S2Buffer[i] = S2Buffer[i - 1]
        R2Buffer[i] = R2Buffer[i - 1]
        S3Buffer[i] = S3Buffer[i - 1]
        R3Buffer[i] = R3Buffer[i - 1]
        M0Buffer[i] = M0Buffer[i - 1]
        M1Buffer[i] = M1Buffer[i - 1]
        M2Buffer[i] = M2Buffer[i - 1]
        M3Buffer[i] = M3Buffer[i - 1]
        M4Buffer[i] = M4Buffer[i - 1]
        M5Buffer[i] = M5Buffer[i - 1]
        L3Buffer[i] = L3Buffer[i - 1]
        H3Buffer[i] = H3Buffer[i - 1]
        L4Buffer[i] = L4Buffer[i - 1]
        H4Buffer[i] = H4Buffer[i - 1]
        NowTime = time[i] - TimeShift
        PreTime = time[i - 1] - TimeShift
        if NewDay(NowTime, PreTime):
            if BufHigh[i] != 0:
                P = (BufHigh[i] + BufLow[i] + close[i - 1]) / 3
                R1 = (2.0 * P) - BufLow[i]
                S1 = (2.0 * P) - BufHigh[i]
                R2 = P + (BufHigh[i] - BufLow[i])
                S2 = P - (BufHigh[i] - BufLow[i])
                R3 = (2.0 * P) + (BufHigh[i] - (2.0 * BufLow[i]))
                S3 = (2.0 * P) - ((2.0 * BufHigh[i]) - BufLow[i])
                if PivotsBufers:
                    PivotBuffer[i] = P
                    S1Buffer[i] = S1
                    R1Buffer[i] = R1
                    S2Buffer[i] = S2
                    R2Buffer[i] = R2
                    S3Buffer[i] = S3
                    R3Buffer[i] = R3
                Q = BufHigh[i] - BufLow[i]
                H4 = (Q * 0.55) + close[i - 1]
                H3 = (Q * 0.27) + close[i - 1]
                L3 = close[i - 1] - (Q * 0.27)
                L4 = close[i - 1] - (Q * 0.55)
                if CamarillaBuffers:
                    L3Buffer[i] = L3
                    H3Buffer[i] = H3
                    L4Buffer[i] = L4
                    H4Buffer[i] = H4
                M5 = (R2 + R3) / 2
                M4 = (R1 + R2) / 2
                M3 = (P + R1) / 2
                M2 = (P + S1) / 2
                M1 = (S1 + S2) / 2
                M0 = (S2 + S3) / 2
                if MidpivotsBuffers:
                    M0Buffer[i] = M0
                    M1Buffer[i] = M1
                    M2Buffer[i] = M2
                    M3Buffer[i] = M3
                    M4Buffer[i] = M4
                    M5Buffer[i] = M5
            BufHigh[i] = high[i]
            BufLow[i] = low[i]
        else:
            BufHigh[i] = MathMax(BufHigh[i], high[i])
            BufLow[i] = MathMin(BufLow[i], low[i])
    tm = time[rates_total - 20]
    if PivotsLines:
        fObjMove('Pivot', P, tm)
        fObjMove('S1', S1, tm)
        fObjMove('R1', R1, tm)
        fObjMove('S2', S2, tm)
        fObjMove('R2', R2, tm)
        fObjMove('S3', S3, tm)
        fObjMove('R3', R3, tm)
    if MidpivotsLines:
        fObjMove('M0', M0, tm)
        fObjMove('M1', M1, tm)
        fObjMove('M2', M2, tm)
        fObjMove('M3', M3, tm)
        fObjMove('M4', M4, tm)
        fObjMove('M5', M5, tm)
    if CamarillaLines:
        fObjMove('L3', L3, tm)
        fObjMove('H3', H3, tm)
        fObjMove('L4', L4, tm)
        fObjMove('H4', H4, tm)
    if Redr:
        ChartRedraw()
    return rates_total

def fObjMove(aObjName, aPrice, aTime):
    ObjectMove(0, aObjName, 0, 0, aPrice)
    ObjectMove(0, 'Txt' + aObjName, 0, aTime, aPrice)

def fObjHLine(aObjName, aPrice, aText='HLine', aWindow=0, aColor=_uint(Red), aWidth=1, aStyle=0, aChartID=0, aBack=True, aSelectable=True, aSelected=False, aTimeFrames=_long(OBJ_ALL_PERIODS)):
    ObjectCreate(aChartID, aObjName, OBJ_HLINE, aWindow, 0, aPrice)
    ObjectSetInteger(aChartID, aObjName, OBJPROP_BACK, aBack)
    ObjectSetInteger(aChartID, aObjName, OBJPROP_COLOR, aColor)
    ObjectSetInteger(aChartID, aObjName, OBJPROP_SELECTABLE, aSelectable)
    ObjectSetInteger(aChartID, aObjName, OBJPROP_SELECTED, aSelected)
    ObjectSetInteger(aChartID, aObjName, OBJPROP_TIMEFRAMES, aTimeFrames)
    ObjectSetString(aChartID, aObjName, OBJPROP_TEXT, aText)
    ObjectSetInteger(aChartID, aObjName, OBJPROP_WIDTH, aWidth)
    ObjectSetInteger(aChartID, aObjName, OBJPROP_STYLE, aStyle)
    ObjectMove(aChartID, aObjName, 0, 0, aPrice)

def fObjText(aObjName, aTime, aPrice, aText='ObjText', aWindow=0, aAnchor=ANCHOR_LEFT_UPPER, aColor=_uint(Red), aFontSize=8, aFont='Arial', aChartID=0, aBack=False, aAngle=0.0, aSelectable=True, aSelected=False, aTimeFrames=_long(OBJ_ALL_PERIODS)):
    ObjectDelete(aChartID, aObjName)
    ObjectCreate(aChartID, aObjName, OBJ_TEXT, aWindow, aTime, aPrice)
    ObjectSetInteger(aChartID, aObjName, OBJPROP_ANCHOR, aAnchor)
    ObjectSetInteger(aChartID, aObjName, OBJPROP_BACK, aBack)
    ObjectSetInteger(aChartID, aObjName, OBJPROP_COLOR, aColor)
    ObjectSetInteger(aChartID, aObjName, OBJPROP_FONTSIZE, aFontSize)
    ObjectSetInteger(aChartID, aObjName, OBJPROP_SELECTABLE, aSelectable)
    ObjectSetInteger(aChartID, aObjName, OBJPROP_SELECTED, aSelected)
    ObjectSetInteger(aChartID, aObjName, OBJPROP_TIMEFRAMES, aTimeFrames)
    ObjectSetString(aChartID, aObjName, OBJPROP_TEXT, aText)
    ObjectSetString(aChartID, aObjName, OBJPROP_FONT, aFont)
    ObjectSetDouble(aChartID, aObjName, OBJPROP_ANGLE, aAngle)
    ObjectMove(aChartID, aObjName, 0, aTime, aPrice)

def NewDay(aNowTime, aPreTime):
    NowDay = _idiv(aNowTime, 86400)
    PreDay = _idiv(aPreTime, 86400)
    if AttachSundToMond:
        if NowDay != PreDay:
            nts = MqlDateTime()
            pts = MqlDateTime()
            TimeToStruct(aNowTime, nts)
            TimeToStruct(aPreTime, pts)
            if nts.day_of_week == 1 and pts.day_of_week == 0:
                return False
            return True
    else:
        return NowDay != PreDay
    return False

# ---- static local variables
_s_OnCalculate_error = True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PivotLinesTimezone(_MQL5Indicator):
    name = 'pivot_lines_timezone'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'DayStartHour': 0,  # DayStartHour
        'DayStartMinute': 0,  # DayStartMinute
        'PivotsBufers': False,  # PivotsBufers
        'MidpivotsBuffers': False,  # MidpivotsBuffers
        'CamarillaBuffers': False,  # CamarillaBuffers
        'PivotsLines': True,  # PivotsLines
        'MidpivotsLines': False,  # MidpivotsLines
        'CamarillaLines': False,  # CamarillaLines
        'AttachSundToMond': True,  # AttachSundToMond
    }

