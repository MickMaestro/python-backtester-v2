"""DeMarkerTrend_x10Full — converted from MQL5: MQL5 Indicators/DeMarkerTrend_x10Full/DeMarkerTrend_x10Full.mq5

Индикатор отображает положение осциллятора DeMarker с разных таймфреймов
Copyright: 2011,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.getfontname import *  # #include getfontname.mqh

MQL5_META = {'props': {'copyright': '2011,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Индикатор отображает положение осциллятора DeMarker с разных таймфреймов'], 'name': 'DeMarkerTrend_x10Full', 'source': 'MQL5 Indicators/DeMarkerTrend_x10Full/DeMarkerTrend_x10Full.mq5', 'folder': 'DeMarkerTrend_x10Full', 'inputs': [{'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 16385, 'label': 'период графика 1', 'sinput': False}, {'mql': 'DeMarkerPeriod1', 'py': 'DeMarkerPeriod1', 'param': 'DeMarkerPeriod1', 'type': 'uint', 'default': 7, 'label': 'период DeMarker 1', 'sinput': False}, {'mql': 'UpLevel1', 'py': 'UpLevel1', 'param': 'UpLevel1', 'type': 'double', 'default': 0.7, 'label': 'уровень перезакупа 1', 'sinput': False}, {'mql': 'DnLevel1', 'py': 'DnLevel1', 'param': 'DnLevel1', 'type': 'double', 'default': 0.3, 'label': 'уровень перепроданности 1', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 16385, 'label': 'период графика 2', 'sinput': False}, {'mql': 'DeMarkerPeriod2', 'py': 'DeMarkerPeriod2', 'param': 'DeMarkerPeriod2', 'type': 'uint', 'default': 11, 'label': 'период DeMarker 2', 'sinput': False}, {'mql': 'UpLevel2', 'py': 'UpLevel2', 'param': 'UpLevel2', 'type': 'double', 'default': 0.7, 'label': 'уровень перезакупа 2', 'sinput': False}, {'mql': 'DnLevel2', 'py': 'DnLevel2', 'param': 'DnLevel2', 'type': 'double', 'default': 0.3, 'label': 'уровень перепроданности 2', 'sinput': False}, {'mql': 'TimeFrame3', 'py': 'TimeFrame3', 'param': 'TimeFrame3', 'type': 'int', 'default': 16385, 'label': 'период графика 3', 'sinput': False}, {'mql': 'DeMarkerPeriod3', 'py': 'DeMarkerPeriod3', 'param': 'DeMarkerPeriod3', 'type': 'uint', 'default': 15, 'label': 'период DeMarker 3', 'sinput': False}, {'mql': 'UpLevel3', 'py': 'UpLevel3', 'param': 'UpLevel3', 'type': 'double', 'default': 0.7, 'label': 'уровень перезакупа 3', 'sinput': False}, {'mql': 'DnLevel3', 'py': 'DnLevel3', 'param': 'DnLevel3', 'type': 'double', 'default': 0.3, 'label': 'уровень перепроданности 3', 'sinput': False}, {'mql': 'TimeFrame4', 'py': 'TimeFrame4', 'param': 'TimeFrame4', 'type': 'int', 'default': 16385, 'label': 'период графика 4', 'sinput': False}, {'mql': 'DeMarkerPeriod4', 'py': 'DeMarkerPeriod4', 'param': 'DeMarkerPeriod4', 'type': 'uint', 'default': 19, 'label': 'период DeMarker 4', 'sinput': False}, {'mql': 'UpLevel4', 'py': 'UpLevel4', 'param': 'UpLevel4', 'type': 'double', 'default': 0.7, 'label': 'уровень перезакупа 4', 'sinput': False}, {'mql': 'DnLevel4', 'py': 'DnLevel4', 'param': 'DnLevel4', 'type': 'double', 'default': 0.3, 'label': 'уровень перепроданности 4', 'sinput': False}, {'mql': 'TimeFrame5', 'py': 'TimeFrame5', 'param': 'TimeFrame5', 'type': 'int', 'default': 16385, 'label': 'период графика 5', 'sinput': False}, {'mql': 'DeMarkerPeriod5', 'py': 'DeMarkerPeriod5', 'param': 'DeMarkerPeriod5', 'type': 'uint', 'default': 23, 'label': 'период DeMarker 5', 'sinput': False}, {'mql': 'UpLevel5', 'py': 'UpLevel5', 'param': 'UpLevel5', 'type': 'double', 'default': 0.7, 'label': 'уровень перезакупа 5', 'sinput': False}, {'mql': 'DnLevel5', 'py': 'DnLevel5', 'param': 'DnLevel5', 'type': 'double', 'default': 0.3, 'label': 'уровень перепроданности 5', 'sinput': False}, {'mql': 'TimeFrame6', 'py': 'TimeFrame6', 'param': 'TimeFrame6', 'type': 'int', 'default': 16385, 'label': 'период графика 6', 'sinput': False}, {'mql': 'DeMarkerPeriod6', 'py': 'DeMarkerPeriod6', 'param': 'DeMarkerPeriod6', 'type': 'uint', 'default': 27, 'label': 'период DeMarker 6', 'sinput': False}, {'mql': 'UpLevel6', 'py': 'UpLevel6', 'param': 'UpLevel6', 'type': 'double', 'default': 0.7, 'label': 'уровень перезакупа 6', 'sinput': False}, {'mql': 'DnLevel6', 'py': 'DnLevel6', 'param': 'DnLevel6', 'type': 'double', 'default': 0.3, 'label': 'уровень перепроданности 6', 'sinput': False}, {'mql': 'TimeFrame7', 'py': 'TimeFrame7', 'param': 'TimeFrame7', 'type': 'int', 'default': 16385, 'label': 'период графика 7', 'sinput': False}, {'mql': 'DeMarkerPeriod7', 'py': 'DeMarkerPeriod7', 'param': 'DeMarkerPeriod7', 'type': 'uint', 'default': 31, 'label': 'период DeMarker 7', 'sinput': False}, {'mql': 'UpLevel7', 'py': 'UpLevel7', 'param': 'UpLevel7', 'type': 'double', 'default': 0.7, 'label': 'уровень перезакупа 7', 'sinput': False}, {'mql': 'DnLevel7', 'py': 'DnLevel7', 'param': 'DnLevel7', 'type': 'double', 'default': 0.3, 'label': 'уровень перепроданности 7', 'sinput': False}, {'mql': 'TimeFrame8', 'py': 'TimeFrame8', 'param': 'TimeFrame8', 'type': 'int', 'default': 16385, 'label': 'период графика 8', 'sinput': False}, {'mql': 'DeMarkerPeriod8', 'py': 'DeMarkerPeriod8', 'param': 'DeMarkerPeriod8', 'type': 'uint', 'default': 35, 'label': 'период DeMarker 8', 'sinput': False}, {'mql': 'UpLevel8', 'py': 'UpLevel8', 'param': 'UpLevel8', 'type': 'double', 'default': 0.7, 'label': 'уровень перезакупа 8', 'sinput': False}, {'mql': 'DnLevel8', 'py': 'DnLevel8', 'param': 'DnLevel8', 'type': 'double', 'default': 0.3, 'label': 'уровень перепроданности 8', 'sinput': False}, {'mql': 'TimeFrame9', 'py': 'TimeFrame9', 'param': 'TimeFrame9', 'type': 'int', 'default': 16385, 'label': 'период графика 9', 'sinput': False}, {'mql': 'DeMarkerPeriod9', 'py': 'DeMarkerPeriod9', 'param': 'DeMarkerPeriod9', 'type': 'uint', 'default': 39, 'label': 'период DeMarker 9', 'sinput': False}, {'mql': 'UpLevel9', 'py': 'UpLevel9', 'param': 'UpLevel9', 'type': 'double', 'default': 0.7, 'label': 'уровень перезакупа 9', 'sinput': False}, {'mql': 'DnLevel9', 'py': 'DnLevel9', 'param': 'DnLevel9', 'type': 'double', 'default': 0.3, 'label': 'уровень перепроданности 9', 'sinput': False}, {'mql': 'TimeFrame10', 'py': 'TimeFrame10', 'param': 'TimeFrame10', 'type': 'int', 'default': 16385, 'label': 'период графика 10', 'sinput': False}, {'mql': 'DeMarkerPeriod10', 'py': 'DeMarkerPeriod10', 'param': 'DeMarkerPeriod10', 'type': 'uint', 'default': 43, 'label': 'период DeMarker 10', 'sinput': False}, {'mql': 'UpLevel10', 'py': 'UpLevel10', 'param': 'UpLevel10', 'type': 'double', 'default': 70.0, 'label': 'уровень перезакупа 10', 'sinput': False}, {'mql': 'DnLevel10', 'py': 'DnLevel10', 'param': 'DnLevel10', 'type': 'double', 'default': 30.0, 'label': 'уровень перепроданности 10', 'sinput': False}, {'mql': 'CpColor', 'py': 'CpColor', 'param': None, 'type': 'color', 'default': 13382297, 'label': 'цвет названия индикатора', 'sinput': False}, {'mql': 'UpColor', 'py': 'UpColor', 'param': None, 'type': 'color', 'default': 16748574, 'label': 'цвет перекупленности индикатора', 'sinput': False}, {'mql': 'DnColor', 'py': 'DnColor', 'param': None, 'type': 'color', 'default': 255, 'label': 'цвет перепроданности индикатора', 'sinput': False}, {'mql': 'ZrColor', 'py': 'ZrColor', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'цвет без изменения', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 11, 'label': 'размер шрифта', 'sinput': False}, {'mql': 'FontType', 'py': 'FontType', 'param': 'FontType', 'type': 'int', 'default': 14, 'label': 'тип шрифта', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 1, 'label': 'угол расположения', 'sinput': False}, {'mql': 'Y_', 'py': 'Y_', 'param': 'Y_', 'type': 'uint', 'default': 20, 'label': 'расположение по вертикали', 'sinput': False}, {'mql': 'X_', 'py': 'X_', 'param': 'X_', 'type': 'uint', 'default': 5, 'label': 'расположение по горизонтали', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['getfontname.mqh']}

# ---- inputs and global variables
TimeFrame1 = _input('TimeFrame1', PERIOD_H1)  # период графика 1
DeMarkerPeriod1 = _input('DeMarkerPeriod1', 7)  # период DeMarker 1
UpLevel1 = _input('UpLevel1', 0.7)  # уровень перезакупа 1
DnLevel1 = _input('DnLevel1', 0.3)  # уровень перепроданности 1
TimeFrame2 = _input('TimeFrame2', PERIOD_H1)  # период графика 2
DeMarkerPeriod2 = _input('DeMarkerPeriod2', 11)  # период DeMarker 2
UpLevel2 = _input('UpLevel2', 0.7)  # уровень перезакупа 2
DnLevel2 = _input('DnLevel2', 0.3)  # уровень перепроданности 2
TimeFrame3 = _input('TimeFrame3', PERIOD_H1)  # период графика 3
DeMarkerPeriod3 = _input('DeMarkerPeriod3', 15)  # период DeMarker 3
UpLevel3 = _input('UpLevel3', 0.7)  # уровень перезакупа 3
DnLevel3 = _input('DnLevel3', 0.3)  # уровень перепроданности 3
TimeFrame4 = _input('TimeFrame4', PERIOD_H1)  # период графика 4
DeMarkerPeriod4 = _input('DeMarkerPeriod4', 19)  # период DeMarker 4
UpLevel4 = _input('UpLevel4', 0.7)  # уровень перезакупа 4
DnLevel4 = _input('DnLevel4', 0.3)  # уровень перепроданности 4
TimeFrame5 = _input('TimeFrame5', PERIOD_H1)  # период графика 5
DeMarkerPeriod5 = _input('DeMarkerPeriod5', 23)  # период DeMarker 5
UpLevel5 = _input('UpLevel5', 0.7)  # уровень перезакупа 5
DnLevel5 = _input('DnLevel5', 0.3)  # уровень перепроданности 5
TimeFrame6 = _input('TimeFrame6', PERIOD_H1)  # период графика 6
DeMarkerPeriod6 = _input('DeMarkerPeriod6', 27)  # период DeMarker 6
UpLevel6 = _input('UpLevel6', 0.7)  # уровень перезакупа 6
DnLevel6 = _input('DnLevel6', 0.3)  # уровень перепроданности 6
TimeFrame7 = _input('TimeFrame7', PERIOD_H1)  # период графика 7
DeMarkerPeriod7 = _input('DeMarkerPeriod7', 31)  # период DeMarker 7
UpLevel7 = _input('UpLevel7', 0.7)  # уровень перезакупа 7
DnLevel7 = _input('DnLevel7', 0.3)  # уровень перепроданности 7
TimeFrame8 = _input('TimeFrame8', PERIOD_H1)  # период графика 8
DeMarkerPeriod8 = _input('DeMarkerPeriod8', 35)  # период DeMarker 8
UpLevel8 = _input('UpLevel8', 0.7)  # уровень перезакупа 8
DnLevel8 = _input('DnLevel8', 0.3)  # уровень перепроданности 8
TimeFrame9 = _input('TimeFrame9', PERIOD_H1)  # период графика 9
DeMarkerPeriod9 = _input('DeMarkerPeriod9', 39)  # период DeMarker 9
UpLevel9 = _input('UpLevel9', 0.7)  # уровень перезакупа 9
DnLevel9 = _input('DnLevel9', 0.3)  # уровень перепроданности 9
TimeFrame10 = _input('TimeFrame10', PERIOD_H1)  # период графика 10
DeMarkerPeriod10 = _input('DeMarkerPeriod10', 43)  # период DeMarker 10
UpLevel10 = _input('UpLevel10', 70.0)  # уровень перезакупа 10
DnLevel10 = _input('DnLevel10', 30.0)  # уровень перепроданности 10
CpColor = _input('CpColor', clrDarkOrchid)  # цвет названия индикатора
UpColor = _input('UpColor', clrDodgerBlue)  # цвет перекупленности индикатора
DnColor = _input('DnColor', clrRed)  # цвет перепроданности индикатора
ZrColor = _input('ZrColor', clrGray)  # цвет без изменения
FontSize = _input('FontSize', 11)  # размер шрифта
FontType = _input('FontType', Font14)  # тип шрифта
WhatCorner = _input('WhatCorner', CORNER_LEFT_LOWER)  # угол расположения
Y_ = _input('Y_', 20)  # расположение по вертикали
X_ = _input('X_', 5)  # расположение по горизонтали
sFontType = ""
min_rates_total = 0
xshift = 0
shift = Arr(11, 0, dyn=False)
sPer = Arr(10, "", dyn=False)
sPerA = Arr(10, "", dyn=False)
sPerB = Arr(10, "", dyn=False)
Cap = ""
ePer = Arr(10, 0, dyn=False)

class CIndArrow(MqlObject):
    _q_fields = ('m_Ind', 'm_Handle', 'm_TimeFrame', 'm_Period', 'm_UpLevel', 'm_DnLevel')
    def __init__(self, *args):
        self.m_Ind = Arr(1, 0.0, dyn=False)
        self.m_Handle = 0
        self.m_TimeFrame = 0
        self.m_Period = 0
        self.m_UpLevel = 0.0
        self.m_DnLevel = 0.0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Cap, min_rates_total, sFontType, xshift
    ePer[0] = TimeFrame1
    ePer[1] = TimeFrame2
    ePer[2] = TimeFrame3
    ePer[3] = TimeFrame4
    ePer[4] = TimeFrame5
    ePer[5] = TimeFrame6
    ePer[6] = TimeFrame7
    ePer[7] = TimeFrame8
    ePer[8] = TimeFrame9
    ePer[9] = TimeFrame10
    for poz in range(0, 10):
        Ind[poz].m_TimeFrame = ePer[poz]
    Ind[0].m_Period = DeMarkerPeriod1
    Ind[1].m_Period = DeMarkerPeriod2
    Ind[2].m_Period = DeMarkerPeriod3
    Ind[3].m_Period = DeMarkerPeriod4
    Ind[4].m_Period = DeMarkerPeriod5
    Ind[5].m_Period = DeMarkerPeriod6
    Ind[6].m_Period = DeMarkerPeriod7
    Ind[7].m_Period = DeMarkerPeriod8
    Ind[8].m_Period = DeMarkerPeriod9
    Ind[9].m_Period = DeMarkerPeriod10
    Ind[0].m_UpLevel = UpLevel1
    Ind[1].m_UpLevel = UpLevel2
    Ind[2].m_UpLevel = UpLevel3
    Ind[3].m_UpLevel = UpLevel4
    Ind[4].m_UpLevel = UpLevel5
    Ind[5].m_UpLevel = UpLevel6
    Ind[6].m_UpLevel = UpLevel7
    Ind[7].m_UpLevel = UpLevel8
    Ind[8].m_UpLevel = UpLevel9
    Ind[9].m_UpLevel = UpLevel10
    Ind[0].m_DnLevel = DnLevel1
    Ind[1].m_DnLevel = DnLevel2
    Ind[2].m_DnLevel = DnLevel3
    Ind[3].m_DnLevel = DnLevel4
    Ind[4].m_DnLevel = DnLevel5
    Ind[5].m_DnLevel = DnLevel6
    Ind[6].m_DnLevel = DnLevel7
    Ind[7].m_DnLevel = DnLevel8
    Ind[8].m_DnLevel = DnLevel9
    Ind[9].m_DnLevel = DnLevel10
    for poz in range(0, 10):
        Ind[poz].m_Handle = iDeMarker(Symbol(), Ind[poz].m_TimeFrame, Ind[poz].m_Period)
        if Ind[poz].m_Handle == INVALID_HANDLE:
            Print('OnInit()(', poz, '): Не удалось получить хендл индикатора DeMarker', poz)
            return False
    FONT = CFontName()
    sFontType = FONT.GetFontName(FontType)
    Deinit()
    max_ = 0
    for poz in range(0, 10):
        if Ind[poz].m_Period > max_:
            max_ = Ind[poz].m_Period
    min_rates_total = _int(max_ + 1)
    xshift = _int(X_ + (8.3 * FontSize))
    Cap = 'DeMarkerTrend_x10Full'
    _sw1 = WhatCorner
    if _sw1 == CORNER_RIGHT_LOWER:
        for poz in range(0, 10 + 1):
            shift[10 - poz] = Y_ + (22 * poz)
    elif _sw1 == CORNER_LEFT_LOWER:
        for poz in range(0, 10 + 1):
            shift[10 - poz] = Y_ + (22 * poz)
    else:
        for poz in range(0, 10 + 1):
            shift[poz] = Y_ + (22 * poz)
    for poz in range(0, 10):
        sPer[poz] = _str(poz + 1) + ' ' + GetStringTimeframe(ePer[poz])
        sPerA[poz] = sPer[poz] + 'Stat+'
        sPerB[poz] = sPer[poz] + 'Stat_'
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Deinit()
    ChartRedraw(0)

def Deinit():
    for poz in range(0, 10):
        ObjectDelete(0, sPerA[poz])
        ObjectDelete(0, sPerB[poz])
    ObjectDelete(0, Cap)

def CreateTLabel(chart_id, name, nwin, corner, point, X, Y, text, Color, Font, Size):
    ObjectCreate(chart_id, name, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(chart_id, name, OBJPROP_CORNER, corner)
    ObjectSetInteger(chart_id, name, OBJPROP_ANCHOR, point)
    ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, X)
    ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, Y)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetString(chart_id, name, OBJPROP_FONT, Font)
    ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, Size)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, False)

def SetTLabel(chart_id, name, nwin, corner, point, X, Y, text, Color, Font, Size):
    if ObjectFind(chart_id, name) == -1:
        CreateTLabel(chart_id, name, nwin, corner, point, X, Y, text, Color, Font, Size)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, X)
        ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, Y)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for poz in range(0, 10):
        if Bars(Symbol(), ePer[poz]) < min_rates_total:
            return 0
    for poz in range(0, 10):
        if CopyBuffer(Ind[poz].m_Handle, MAIN_LINE, 1, 1, Ind[poz].m_Ind) <= 0:
            return 0
    ColorGain = Arr(10, 0, dyn=False)
    ArrayInitialize(ColorGain, ZrColor)
    for poz in range(0, 10):
        if Ind[poz].m_Ind[0] > Ind[poz].m_UpLevel:
            ColorGain[poz] = UpColor
        if Ind[poz].m_Ind[0] < Ind[poz].m_DnLevel:
            ColorGain[poz] = DnColor
    for poz in range(0, 10):
        SetTLabel(0, sPerA[poz], 0, WhatCorner, 2 * WhatCorner, X_, shift[poz + 1], sPer[poz] + ': ', ColorGain[poz], sFontType, FontSize)
        SetTLabel(0, sPerB[poz], 0, WhatCorner, 2 * WhatCorner, xshift, shift[poz + 1], 'n', ColorGain[poz], 'Wingdings', FontSize)
    SetTLabel(0, Cap, 0, WhatCorner, 2 * WhatCorner, X_, shift[0], Cap, CpColor, sFontType, FontSize)
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
Ind = Arr(10, 0, dyn=False, factory=CIndArrow)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DeMarkerTrendX10Full(_MQL5Indicator):
    name = 'DeMarkerTrend_x10Full'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 1
        'DeMarkerPeriod1': 7,  # период DeMarker 1
        'UpLevel1': 0.7,  # уровень перезакупа 1
        'DnLevel1': 0.3,  # уровень перепроданности 1
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 2
        'DeMarkerPeriod2': 11,  # период DeMarker 2
        'UpLevel2': 0.7,  # уровень перезакупа 2
        'DnLevel2': 0.3,  # уровень перепроданности 2
        'TimeFrame3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 3
        'DeMarkerPeriod3': 15,  # период DeMarker 3
        'UpLevel3': 0.7,  # уровень перезакупа 3
        'DnLevel3': 0.3,  # уровень перепроданности 3
        'TimeFrame4': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 4
        'DeMarkerPeriod4': 19,  # период DeMarker 4
        'UpLevel4': 0.7,  # уровень перезакупа 4
        'DnLevel4': 0.3,  # уровень перепроданности 4
        'TimeFrame5': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 5
        'DeMarkerPeriod5': 23,  # период DeMarker 5
        'UpLevel5': 0.7,  # уровень перезакупа 5
        'DnLevel5': 0.3,  # уровень перепроданности 5
        'TimeFrame6': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 6
        'DeMarkerPeriod6': 27,  # период DeMarker 6
        'UpLevel6': 0.7,  # уровень перезакупа 6
        'DnLevel6': 0.3,  # уровень перепроданности 6
        'TimeFrame7': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 7
        'DeMarkerPeriod7': 31,  # период DeMarker 7
        'UpLevel7': 0.7,  # уровень перезакупа 7
        'DnLevel7': 0.3,  # уровень перепроданности 7
        'TimeFrame8': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 8
        'DeMarkerPeriod8': 35,  # период DeMarker 8
        'UpLevel8': 0.7,  # уровень перезакупа 8
        'DnLevel8': 0.3,  # уровень перепроданности 8
        'TimeFrame9': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 9
        'DeMarkerPeriod9': 39,  # период DeMarker 9
        'UpLevel9': 0.7,  # уровень перезакупа 9
        'DnLevel9': 0.3,  # уровень перепроданности 9
        'TimeFrame10': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 10
        'DeMarkerPeriod10': 43,  # период DeMarker 10
        'UpLevel10': 70.0,  # уровень перезакупа 10
        'DnLevel10': 30.0,  # уровень перепроданности 10
        'FontSize': 11,  # размер шрифта
        'FontType': _Choice({0: 'Arial', 1: 'Arial Black', 2: 'Arial Bold', 3: 'Arial Bold Italic', 4: 'Arial Italic', 5: 'Comic Sans MS Bold', 6: 'Courier', 7: 'Courier New', 8: 'Courier New Bold', 9: 'Courier New Bold Italic', 10: 'Courier New Italic', 11: 'Estrangelo Edessa', 12: 'Franklin Gothic Medium', 13: 'Gautami', 14: 'Georgia', 15: 'Georgia Bold', 16: 'Georgia Bold Italic', 17: 'Georgia Italic', 18: 'Georgia Italic Impact', 19: 'Latha', 20: 'Lucida Console', 21: 'Lucida Sans Unicode', 22: 'Modern MS Sans Serif', 23: 'MS Sans Serif', 24: 'Mv Boli', 25: 'Palatino Linotype', 26: 'Palatino Linotype Bold', 27: 'Palatino Linotype Italic', 28: 'Roman', 29: 'Script', 30: 'Small Fonts', 31: 'Symbol', 32: 'Tahoma', 33: 'Tahoma Bold', 34: 'Times New Roman', 35: 'Times New Roman Bold', 36: 'Times New Roman Bold Italic', 37: 'Times New Roman Italic', 38: 'Trebuchet MS', 39: 'Trebuchet MS Bold', 40: 'Trebuchet MS Bold Italic', 41: 'Trebuchet MS Italic', 42: 'Tunga', 43: 'Verdana', 44: 'Verdana Bold', 45: 'Verdana Bold Italic', 46: 'Verdana Italic', 47: 'Webdings', 48: 'Westminster', 49: 'Wingdings', 50: 'WST_Czech', 51: 'WST_Engl', 52: 'WST_Fren', 53: 'WST_Germ', 54: 'WST_Ital', 55: 'WST_Span', 56: 'WST_Swed'}, default=14),  # тип шрифта
        'WhatCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=1),  # угол расположения
        'Y_': 20,  # расположение по вертикали
        'X_': 5,  # расположение по горизонтали
    }

