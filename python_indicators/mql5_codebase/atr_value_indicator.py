"""ATR Value Indicator — converted from MQL5: MQL5 Indicators/ATR Value Indicator/ATR Value Indicator.mq5

Fully Coded By Hossein Nouri
Email : hsn.nouri@gmail.com
Skype : hsn.nouri
Telegram : @hypernova1990
Website : http://www.metatraderprogrammer.ir
MQL5 Profile : https://www.mql5.com/en/users/hsnnouri
 
Feel free to contact me for MQL4/MQL5 coding.
Copyright: Copyright 2018-2024, Hossein Nouri; Link: https://www.mql5.com/en/users/hsnnouri; Version: 1.12

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018-2024, Hossein Nouri', 'link': 'https://www.mql5.com/en/users/hsnnouri', 'version': '1.12', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Fully Coded By Hossein Nouri', 'Email : hsn.nouri@gmail.com', 'Skype : hsn.nouri', 'Telegram : @hypernova1990', 'Website : http://www.metatraderprogrammer.ir', 'MQL5 Profile : https://www.mql5.com/en/users/hsnnouri', ' ', 'Feel free to contact me for MQL4/MQL5 coding.'], 'name': 'ATR Value Indicator', 'source': 'MQL5 Indicators/ATR Value Indicator/ATR Value Indicator.mq5', 'folder': 'ATR Value Indicator', 'inputs': [{'mql': 'InpATRTimeframe', 'py': 'InpATRTimeframe', 'param': 'InpATRTimeframe', 'type': 'int', 'default': 0, 'label': 'ATR Timeframe', 'sinput': False}, {'mql': 'InpATRPeriod', 'py': 'InpATRPeriod', 'param': 'InpATRPeriod', 'type': 'int', 'default': 14, 'label': 'ATR Period', 'sinput': False}, {'mql': 'InpMultiplier', 'py': 'InpMultiplier', 'param': 'InpMultiplier', 'type': 'double', 'default': 2.0, 'label': 'Multiplier', 'sinput': False}, {'mql': 'DescStyle', 'py': 'DescStyle', 'param': None, 'type': 'string', 'default': '======== Style ========', 'label': 'Description', 'sinput': False}, {'mql': 'InpPosition', 'py': 'InpPosition', 'param': 'InpPosition', 'type': 'int', 'default': 2, 'label': 'Position', 'sinput': False}, {'mql': 'InpOffsetX', 'py': 'InpOffsetX', 'param': 'InpOffsetX', 'type': 'int', 'default': 0, 'label': 'Offset X', 'sinput': False}, {'mql': 'InpOffsetY', 'py': 'InpOffsetY', 'param': 'InpOffsetY', 'type': 'int', 'default': 30, 'label': 'Offset Y', 'sinput': False}, {'mql': 'InpDisplay', 'py': 'InpDisplay', 'param': 'InpDisplay', 'type': 'int', 'default': 0, 'label': 'Display Mode', 'sinput': False}, {'mql': 'InpLabelColor', 'py': 'InpLabelColor', 'param': None, 'type': 'color', 'default': 255, 'label': 'Color', 'sinput': False}, {'mql': 'InpFontSize', 'py': 'InpFontSize', 'param': 'InpFontSize', 'type': 'int', 'default': 10, 'label': 'Font Size', 'sinput': False}, {'mql': 'DescVisulizations', 'py': 'DescVisulizations', 'param': None, 'type': 'string', 'default': '===== Visulizations =====', 'label': 'Description', 'sinput': False}, {'mql': 'InpTimeframeAll', 'py': 'InpTimeframeAll', 'param': 'InpTimeframeAll', 'type': 'bool', 'default': True, 'label': 'All Timeframes', 'sinput': False}, {'mql': 'InpTimeframeM1', 'py': 'InpTimeframeM1', 'param': 'InpTimeframeM1', 'type': 'bool', 'default': False, 'label': 'M1', 'sinput': False}, {'mql': 'InpTimeframeM2', 'py': 'InpTimeframeM2', 'param': 'InpTimeframeM2', 'type': 'bool', 'default': False, 'label': 'M2', 'sinput': False}, {'mql': 'InpTimeframeM3', 'py': 'InpTimeframeM3', 'param': 'InpTimeframeM3', 'type': 'bool', 'default': False, 'label': 'M3', 'sinput': False}, {'mql': 'InpTimeframeM4', 'py': 'InpTimeframeM4', 'param': 'InpTimeframeM4', 'type': 'bool', 'default': False, 'label': 'M4', 'sinput': False}, {'mql': 'InpTimeframeM5', 'py': 'InpTimeframeM5', 'param': 'InpTimeframeM5', 'type': 'bool', 'default': False, 'label': 'M5', 'sinput': False}, {'mql': 'InpTimeframeM6', 'py': 'InpTimeframeM6', 'param': 'InpTimeframeM6', 'type': 'bool', 'default': False, 'label': 'M6', 'sinput': False}, {'mql': 'InpTimeframeM10', 'py': 'InpTimeframeM10', 'param': 'InpTimeframeM10', 'type': 'bool', 'default': False, 'label': 'M10', 'sinput': False}, {'mql': 'InpTimeframeM12', 'py': 'InpTimeframeM12', 'param': 'InpTimeframeM12', 'type': 'bool', 'default': False, 'label': 'M12', 'sinput': False}, {'mql': 'InpTimeframeM15', 'py': 'InpTimeframeM15', 'param': 'InpTimeframeM15', 'type': 'bool', 'default': False, 'label': 'M15', 'sinput': False}, {'mql': 'InpTimeframeM20', 'py': 'InpTimeframeM20', 'param': 'InpTimeframeM20', 'type': 'bool', 'default': False, 'label': 'M20', 'sinput': False}, {'mql': 'InpTimeframeM30', 'py': 'InpTimeframeM30', 'param': 'InpTimeframeM30', 'type': 'bool', 'default': False, 'label': 'M30', 'sinput': False}, {'mql': 'InpTimeframeH1', 'py': 'InpTimeframeH1', 'param': 'InpTimeframeH1', 'type': 'bool', 'default': False, 'label': 'H1', 'sinput': False}, {'mql': 'InpTimeframeH2', 'py': 'InpTimeframeH2', 'param': 'InpTimeframeH2', 'type': 'bool', 'default': False, 'label': 'H2', 'sinput': False}, {'mql': 'InpTimeframeH3', 'py': 'InpTimeframeH3', 'param': 'InpTimeframeH3', 'type': 'bool', 'default': False, 'label': 'H3', 'sinput': False}, {'mql': 'InpTimeframeH4', 'py': 'InpTimeframeH4', 'param': 'InpTimeframeH4', 'type': 'bool', 'default': False, 'label': 'H4', 'sinput': False}, {'mql': 'InpTimeframeH6', 'py': 'InpTimeframeH6', 'param': 'InpTimeframeH6', 'type': 'bool', 'default': False, 'label': 'H6', 'sinput': False}, {'mql': 'InpTimeframeH8', 'py': 'InpTimeframeH8', 'param': 'InpTimeframeH8', 'type': 'bool', 'default': False, 'label': 'H8', 'sinput': False}, {'mql': 'InpTimeframeH12', 'py': 'InpTimeframeH12', 'param': 'InpTimeframeH12', 'type': 'bool', 'default': False, 'label': 'H12', 'sinput': False}, {'mql': 'InpTimeframeD1', 'py': 'InpTimeframeD1', 'param': 'InpTimeframeD1', 'type': 'bool', 'default': False, 'label': 'D1', 'sinput': False}, {'mql': 'InpTimeframeW1', 'py': 'InpTimeframeW1', 'param': 'InpTimeframeW1', 'type': 'bool', 'default': False, 'label': 'W1', 'sinput': False}, {'mql': 'InpTimeframeMN1', 'py': 'InpTimeframeMN1', 'param': 'InpTimeframeMN1', 'type': 'bool', 'default': False, 'label': 'MN1', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

OBJ_ALL_PERIODS = 0  # MQL5 constant unknown to the converter
OBJ_NO_PERIODS = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_D1 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_H1 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_H12 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_H2 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_H3 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_H4 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_H6 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_H8 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_M1 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_M10 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_M12 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_M15 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_M2 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_M20 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_M3 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_M30 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_M4 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_M5 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_M6 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_MN1 = 0  # MQL5 constant unknown to the converter
OBJ_PERIOD_W1 = 0  # MQL5 constant unknown to the converter

# enum ENUM_VALUE_TYPE
Points = 0
Pips = 1
_enum('ENUM_VALUE_TYPE', {0: 'Points', 1: 'Pips'})

# enum ENUM_CORNER
LEFT_UPPER = 0
LEFT_LOWER = 1
RIGHT_UPPER = 2
RIGHT_LOWER = 3
_enum('ENUM_CORNER', {0: 'LEFT_UPPER', 1: 'LEFT_LOWER', 2: 'RIGHT_UPPER', 3: 'RIGHT_LOWER'})

# ---- inputs and global variables
InpATRTimeframe = _input('InpATRTimeframe', PERIOD_CURRENT)  # ATR Timeframe
InpATRPeriod = _input('InpATRPeriod', 14)  # ATR Period
InpMultiplier = _input('InpMultiplier', 2.0)  # Multiplier
DescStyle = _input('DescStyle', '======== Style ========')  # Description
InpPosition = _input('InpPosition', RIGHT_UPPER)  # Position
InpOffsetX = _input('InpOffsetX', 0)  # Offset X
InpOffsetY = _input('InpOffsetY', 30)  # Offset Y
InpDisplay = _input('InpDisplay', 0)  # Display Mode
InpLabelColor = _input('InpLabelColor', clrRed)  # Color
InpFontSize = _input('InpFontSize', 10)  # Font Size
DescVisulizations = _input('DescVisulizations', '===== Visulizations =====')  # Description
InpTimeframeAll = _input('InpTimeframeAll', True)  # All Timeframes
InpTimeframeM1 = _input('InpTimeframeM1', False)  # M1
InpTimeframeM2 = _input('InpTimeframeM2', False)  # M2
InpTimeframeM3 = _input('InpTimeframeM3', False)  # M3
InpTimeframeM4 = _input('InpTimeframeM4', False)  # M4
InpTimeframeM5 = _input('InpTimeframeM5', False)  # M5
InpTimeframeM6 = _input('InpTimeframeM6', False)  # M6
InpTimeframeM10 = _input('InpTimeframeM10', False)  # M10
InpTimeframeM12 = _input('InpTimeframeM12', False)  # M12
InpTimeframeM15 = _input('InpTimeframeM15', False)  # M15
InpTimeframeM20 = _input('InpTimeframeM20', False)  # M20
InpTimeframeM30 = _input('InpTimeframeM30', False)  # M30
InpTimeframeH1 = _input('InpTimeframeH1', False)  # H1
InpTimeframeH2 = _input('InpTimeframeH2', False)  # H2
InpTimeframeH3 = _input('InpTimeframeH3', False)  # H3
InpTimeframeH4 = _input('InpTimeframeH4', False)  # H4
InpTimeframeH6 = _input('InpTimeframeH6', False)  # H6
InpTimeframeH8 = _input('InpTimeframeH8', False)  # H8
InpTimeframeH12 = _input('InpTimeframeH12', False)  # H12
InpTimeframeD1 = _input('InpTimeframeD1', False)  # D1
InpTimeframeW1 = _input('InpTimeframeW1', False)  # W1
InpTimeframeMN1 = _input('InpTimeframeMN1', False)  # MN1
OBJ_NAME = ""
OBJ_PATTERN = ""
Visibility = 0
ATRHandle = 0
ATRBuffer = Arr(0, 0.0)
TextCorner = 0
TextAnchor = 0

def SetVisibility():
    global Visibility
    Visibility = 0
    if InpTimeframeAll:
        Visibility += OBJ_ALL_PERIODS
        return
    if InpTimeframeM1:
        Visibility += OBJ_PERIOD_M1
    if InpTimeframeM2:
        Visibility += OBJ_PERIOD_M2
    if InpTimeframeM3:
        Visibility += OBJ_PERIOD_M3
    if InpTimeframeM4:
        Visibility += OBJ_PERIOD_M4
    if InpTimeframeM5:
        Visibility += OBJ_PERIOD_M5
    if InpTimeframeM6:
        Visibility += OBJ_PERIOD_M6
    if InpTimeframeM10:
        Visibility += OBJ_PERIOD_M10
    if InpTimeframeM12:
        Visibility += OBJ_PERIOD_M12
    if InpTimeframeM15:
        Visibility += OBJ_PERIOD_M15
    if InpTimeframeM20:
        Visibility += OBJ_PERIOD_M20
    if InpTimeframeM30:
        Visibility += OBJ_PERIOD_M30
    if InpTimeframeH1:
        Visibility += OBJ_PERIOD_H1
    if InpTimeframeH2:
        Visibility += OBJ_PERIOD_H2
    if InpTimeframeH3:
        Visibility += OBJ_PERIOD_H3
    if InpTimeframeH4:
        Visibility += OBJ_PERIOD_H4
    if InpTimeframeH6:
        Visibility += OBJ_PERIOD_H6
    if InpTimeframeH8:
        Visibility += OBJ_PERIOD_H8
    if InpTimeframeH12:
        Visibility += OBJ_PERIOD_H12
    if InpTimeframeD1:
        Visibility += OBJ_PERIOD_D1
    if InpTimeframeW1:
        Visibility += OBJ_PERIOD_W1
    if InpTimeframeMN1:
        Visibility += OBJ_PERIOD_MN1
    if Visibility == 0:
        Visibility = _int(OBJ_NO_PERIODS)

def OnInit():
    global ATRHandle, OBJ_NAME, OBJ_PATTERN
    ATRHandle = iATR(Symbol(), InpATRTimeframe, InpATRPeriod)
    ArraySetAsSeries(ATRBuffer, True)
    SetVisibility()
    SetTextPosition()
    OBJ_PATTERN = 'ATRInd_' + _str(ChartID())
    CleanUpChart()
    OBJ_NAME = OBJ_PATTERN + '_' + GetTFName() + '_' + IntegerToString(InpATRPeriod) + '_' + GetTFName(InpATRTimeframe) + '_' + DoubleToString(InpMultiplier, 2) + '_'
    ShowATR()
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, OBJ_NAME)
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ShowATR()
    return rates_total

def ShowATR():
    global _s_ShowATR_ATR
    if CopyBuffer(ATRHandle, 0, 0, 2, ATRBuffer) <= 0:
        Print('Getting ATR failed! Error', GetLastError())
        return
    _s_ShowATR_ATR = ATRBuffer[0]
    _s_ShowATR_ATR = _s_ShowATR_ATR * InpMultiplier * MathPow(10, Digits() - InpDisplay)
    DrawATROnChart(_s_ShowATR_ATR)

def DrawATROnChart(ATR):
    Dis = ""
    if InpDisplay == 0:
        Dis = ' Points'
    if InpDisplay == 1:
        Dis = ' Pips'
    Output = StringFormat('%s%s of ATR(%s,%s): %s %s  ', DoubleToString(InpMultiplier * 100, 0), '%', IntegerToString(InpATRPeriod), GetTFName(InpATRTimeframe), DoubleToString(ATR, 0), Dis)
    if ObjectFind(0, OBJ_NAME) < 0:
        ObjectCreate(0, OBJ_NAME, OBJ_LABEL, 0, 0, 0)
        ObjectSetInteger(0, OBJ_NAME, OBJPROP_YDISTANCE, InpOffsetY)
        ObjectSetInteger(0, OBJ_NAME, OBJPROP_XDISTANCE, InpOffsetX)
        ObjectSetInteger(0, OBJ_NAME, OBJPROP_CORNER, TextCorner)
        ObjectSetString(0, OBJ_NAME, OBJPROP_TEXT, Output)
        ObjectSetString(0, OBJ_NAME, OBJPROP_FONT, 'Arial')
        ObjectSetInteger(0, OBJ_NAME, OBJPROP_FONTSIZE, InpFontSize)
        ObjectSetDouble(0, OBJ_NAME, OBJPROP_ANGLE, 0)
        ObjectSetInteger(0, OBJ_NAME, OBJPROP_ANCHOR, TextAnchor)
        ObjectSetInteger(0, OBJ_NAME, OBJPROP_COLOR, InpLabelColor)
        ObjectSetInteger(0, OBJ_NAME, OBJPROP_BACK, False)
        ObjectSetInteger(0, OBJ_NAME, OBJPROP_SELECTABLE, False)
        ObjectSetInteger(0, OBJ_NAME, OBJPROP_SELECTED, False)
        ObjectSetInteger(0, OBJ_NAME, OBJPROP_HIDDEN, True)
        ObjectSetInteger(0, OBJ_NAME, OBJPROP_ZORDER, 0)
        ObjectSetInteger(0, OBJ_NAME, OBJPROP_TIMEFRAMES, Visibility)
    ObjectSetString(0, OBJ_NAME, OBJPROP_TEXT, Output)
    ChartRedraw()

def GetTFName(_TF=-1):
    if _TF == PERIOD_CURRENT:
        _TF = Period()
    if _TF == 1:
        return 'M1'
    if _TF == 2:
        return 'M2'
    if _TF == 3:
        return 'M3'
    if _TF == 4:
        return 'M4'
    if _TF == 5:
        return 'M5'
    if _TF == 6:
        return 'M6'
    if _TF == 10:
        return 'M10'
    if _TF == 12:
        return 'M12'
    if _TF == 15:
        return 'M15'
    if _TF == 20:
        return 'M20'
    if _TF == 30:
        return 'M30'
    if _TF == 16385:
        return 'H1'
    if _TF == 16386:
        return 'H2'
    if _TF == 16387:
        return 'H3'
    if _TF == 16388:
        return 'H4'
    if _TF == 16390:
        return 'H6'
    if _TF == 16392:
        return 'H8'
    if _TF == 16396:
        return 'H12'
    if _TF == 16408:
        return 'D1'
    if _TF == 32769:
        return 'W1'
    if _TF == 49153:
        return 'MN1'
    return _str(_TF)

def SetTextPosition():
    global TextAnchor, TextCorner
    if InpPosition == LEFT_UPPER:
        TextCorner = CORNER_LEFT_UPPER
        TextAnchor = ANCHOR_LEFT_UPPER
    elif InpPosition == LEFT_LOWER:
        TextCorner = CORNER_LEFT_LOWER
        TextAnchor = ANCHOR_LEFT_LOWER
    elif InpPosition == RIGHT_UPPER:
        TextCorner = CORNER_RIGHT_UPPER
        TextAnchor = ANCHOR_RIGHT_UPPER
    elif InpPosition == RIGHT_LOWER:
        TextCorner = CORNER_RIGHT_LOWER
        TextAnchor = ANCHOR_RIGHT_LOWER

def CleanUpChart():
    TotalObjects = ObjectsTotal(0, 0, OBJ_LABEL)
    ObjName = ''
    for i in range(TotalObjects - 1, 0 - 1, -1):
        ObjName = ObjectName(0, i, 0, OBJ_LABEL)
        if StringFind(ObjName, 'ATRInd_') != -1:
            if StringFind(ObjName, OBJ_PATTERN) == -1:
                ObjectDelete(0, ObjName)

# ---- static local variables
_s_ShowATR_ATR = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ATRValueIndicator(_MQL5Indicator):
    name = 'ATR Value Indicator'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpATRTimeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # ATR Timeframe
        'InpATRPeriod': 14,  # ATR Period
        'InpMultiplier': 2.0,  # Multiplier
        'InpPosition': _Choice({0: 'Left Upper', 1: 'Left Lower', 2: 'Right Upper', 3: 'Right Lower'}, default=2),  # Position
        'InpOffsetX': 0,  # Offset X
        'InpOffsetY': 30,  # Offset Y
        'InpDisplay': _Choice({0: 'Points', 1: 'Pips'}, default=0),  # Display Mode
        'InpFontSize': 10,  # Font Size
        'InpTimeframeAll': True,  # All Timeframes
        'InpTimeframeM1': False,  # M1
        'InpTimeframeM2': False,  # M2
        'InpTimeframeM3': False,  # M3
        'InpTimeframeM4': False,  # M4
        'InpTimeframeM5': False,  # M5
        'InpTimeframeM6': False,  # M6
        'InpTimeframeM10': False,  # M10
        'InpTimeframeM12': False,  # M12
        'InpTimeframeM15': False,  # M15
        'InpTimeframeM20': False,  # M20
        'InpTimeframeM30': False,  # M30
        'InpTimeframeH1': False,  # H1
        'InpTimeframeH2': False,  # H2
        'InpTimeframeH3': False,  # H3
        'InpTimeframeH4': False,  # H4
        'InpTimeframeH6': False,  # H6
        'InpTimeframeH8': False,  # H8
        'InpTimeframeH12': False,  # H12
        'InpTimeframeD1': False,  # D1
        'InpTimeframeW1': False,  # W1
        'InpTimeframeMN1': False,  # MN1
    }

