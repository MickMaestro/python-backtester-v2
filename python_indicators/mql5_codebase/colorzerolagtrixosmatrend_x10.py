"""colorzerolagtrixosmatrend_x10 — converted from MQL5: MQL5 Indicators/ColorZerolagTriXOSMATrend_x10/colorzerolagtrixosmatrend_x10.mq5

Индикатор отображает направление движения осциллятора ColorZerolagTriXOSMA с разных таймфреймов
Copyright: 2011,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.getfontname import *  # #include getfontname.mqh

MQL5_META = {'props': {'copyright': '2011,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Индикатор отображает направление движения осциллятора ColorZerolagTriXOSMA с разных таймфреймов'], 'name': 'colorzerolagtrixosmatrend_x10', 'source': 'MQL5 Indicators/ColorZerolagTriXOSMATrend_x10/colorzerolagtrixosmatrend_x10.mq5', 'folder': 'ColorZerolagTriXOSMATrend_x10', 'inputs': [{'mql': 'TimeFrame0', 'py': 'TimeFrame0', 'param': 'TimeFrame0', 'type': 'int', 'default': 16385, 'label': 'Период графика 1', 'sinput': False}, {'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 16386, 'label': 'Период графика 2', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 16387, 'label': 'Период графика 3', 'sinput': False}, {'mql': 'TimeFrame3', 'py': 'TimeFrame3', 'param': 'TimeFrame3', 'type': 'int', 'default': 16388, 'label': 'Период графика 4', 'sinput': False}, {'mql': 'TimeFrame4', 'py': 'TimeFrame4', 'param': 'TimeFrame4', 'type': 'int', 'default': 16390, 'label': 'Период графика 5', 'sinput': False}, {'mql': 'TimeFrame5', 'py': 'TimeFrame5', 'param': 'TimeFrame5', 'type': 'int', 'default': 16392, 'label': 'Период графика 6', 'sinput': False}, {'mql': 'TimeFrame6', 'py': 'TimeFrame6', 'param': 'TimeFrame6', 'type': 'int', 'default': 16396, 'label': 'Период графика 7', 'sinput': False}, {'mql': 'TimeFrame7', 'py': 'TimeFrame7', 'param': 'TimeFrame7', 'type': 'int', 'default': 16408, 'label': 'Период графика 8', 'sinput': False}, {'mql': 'TimeFrame8', 'py': 'TimeFrame8', 'param': 'TimeFrame8', 'type': 'int', 'default': 32769, 'label': 'Период графика 9', 'sinput': False}, {'mql': 'TimeFrame9', 'py': 'TimeFrame9', 'param': 'TimeFrame9', 'type': 'int', 'default': 49153, 'label': 'Период графика 10', 'sinput': False}, {'mql': 'smoothing1', 'py': 'smoothing1', 'param': 'smoothing1', 'type': 'uint', 'default': 15, 'label': '', 'sinput': False}, {'mql': 'smoothing2', 'py': 'smoothing2', 'param': 'smoothing2', 'type': 'uint', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Factor1', 'py': 'Factor1', 'param': 'Factor1', 'type': 'double', 'default': 0.05, 'label': '', 'sinput': False}, {'mql': 'TriX_period1', 'py': 'TriX_period1', 'param': 'TriX_period1', 'type': 'uint', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'Factor2', 'py': 'Factor2', 'param': 'Factor2', 'type': 'double', 'default': 0.1, 'label': '', 'sinput': False}, {'mql': 'TriX_period2', 'py': 'TriX_period2', 'param': 'TriX_period2', 'type': 'uint', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'Factor3', 'py': 'Factor3', 'param': 'Factor3', 'type': 'double', 'default': 0.16, 'label': '', 'sinput': False}, {'mql': 'TriX_period3', 'py': 'TriX_period3', 'param': 'TriX_period3', 'type': 'uint', 'default': 34, 'label': '', 'sinput': False}, {'mql': 'Factor4', 'py': 'Factor4', 'param': 'Factor4', 'type': 'double', 'default': 0.26, 'label': '', 'sinput': False}, {'mql': 'TriX_period4', 'py': 'TriX_period4', 'param': 'TriX_period4', 'type': 'int', 'default': 55, 'label': '', 'sinput': False}, {'mql': 'Factor5', 'py': 'Factor5', 'param': 'Factor5', 'type': 'double', 'default': 0.43, 'label': '', 'sinput': False}, {'mql': 'TriX_period5', 'py': 'TriX_period5', 'param': 'TriX_period5', 'type': 'uint', 'default': 89, 'label': '', 'sinput': False}, {'mql': 'CpColor', 'py': 'CpColor', 'param': None, 'type': 'color', 'default': 13382297, 'label': 'Цвет названия индикатора', 'sinput': False}, {'mql': 'UpColor', 'py': 'UpColor', 'param': None, 'type': 'color', 'default': 16748574, 'label': 'Цвет перекупленности индикатора', 'sinput': False}, {'mql': 'DnColor', 'py': 'DnColor', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Цвет перепроданности индикатора', 'sinput': False}, {'mql': 'ZrColor', 'py': 'ZrColor', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'Цвет без изменения', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 11, 'label': 'Размер шрифта', 'sinput': False}, {'mql': 'FontType', 'py': 'FontType', 'param': 'FontType', 'type': 'int', 'default': 14, 'label': 'Тип шрифта', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 1, 'label': 'Угол расположения', 'sinput': False}, {'mql': 'Y_', 'py': 'Y_', 'param': 'Y_', 'type': 'uint', 'default': 20, 'label': 'Расположение по вертикали', 'sinput': False}, {'mql': 'X_', 'py': 'X_', 'param': 'X_', 'type': 'uint', 'default': 5, 'label': 'Расположение по горизонтали', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['getfontname.mqh']}

# ---- inputs and global variables
TimeFrame0 = _input('TimeFrame0', PERIOD_H1)  # Период графика 1
TimeFrame1 = _input('TimeFrame1', PERIOD_H2)  # Период графика 2
TimeFrame2 = _input('TimeFrame2', PERIOD_H3)  # Период графика 3
TimeFrame3 = _input('TimeFrame3', PERIOD_H4)  # Период графика 4
TimeFrame4 = _input('TimeFrame4', PERIOD_H6)  # Период графика 5
TimeFrame5 = _input('TimeFrame5', PERIOD_H8)  # Период графика 6
TimeFrame6 = _input('TimeFrame6', PERIOD_H12)  # Период графика 7
TimeFrame7 = _input('TimeFrame7', PERIOD_D1)  # Период графика 8
TimeFrame8 = _input('TimeFrame8', PERIOD_W1)  # Период графика 9
TimeFrame9 = _input('TimeFrame9', PERIOD_MN1)  # Период графика 10
smoothing1 = _input('smoothing1', 15)
smoothing2 = _input('smoothing2', 7)
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
Factor1 = _input('Factor1', 0.05)
TriX_period1 = _input('TriX_period1', 8)
Factor2 = _input('Factor2', 0.1)
TriX_period2 = _input('TriX_period2', 21)
Factor3 = _input('Factor3', 0.16)
TriX_period3 = _input('TriX_period3', 34)
Factor4 = _input('Factor4', 0.26)
TriX_period4 = _input('TriX_period4', 55)
Factor5 = _input('Factor5', 0.43)
TriX_period5 = _input('TriX_period5', 89)
CpColor = _input('CpColor', clrDarkOrchid)  # Цвет названия индикатора
UpColor = _input('UpColor', clrDodgerBlue)  # Цвет перекупленности индикатора
DnColor = _input('DnColor', clrMagenta)  # Цвет перепроданности индикатора
ZrColor = _input('ZrColor', clrGray)  # Цвет без изменения
FontSize = _input('FontSize', 11)  # Размер шрифта
FontType = _input('FontType', Font14)  # Тип шрифта
WhatCorner = _input('WhatCorner', CORNER_LEFT_LOWER)  # Угол расположения
Y_ = _input('Y_', 20)  # Расположение по вертикали
X_ = _input('X_', 5)  # Расположение по горизонтали
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
    _q_fields = ('m_ClrInd', 'm_Handle', 'm_TimeFrame')
    def __init__(self, *args):
        self.m_ClrInd = Arr(1, 0.0, dyn=False)
        self.m_Handle = 0
        self.m_TimeFrame = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Cap, min_rates_total, sFontType, xshift
    ePer[0] = TimeFrame0
    ePer[1] = TimeFrame1
    ePer[2] = TimeFrame2
    ePer[3] = TimeFrame3
    ePer[4] = TimeFrame4
    ePer[5] = TimeFrame5
    ePer[6] = TimeFrame6
    ePer[7] = TimeFrame7
    ePer[8] = TimeFrame8
    ePer[9] = TimeFrame9
    for poz in range(0, 10):
        Ind[poz].m_TimeFrame = ePer[poz]
    for poz in range(0, 10):
        Ind[poz].m_Handle = iCustom(Symbol(), Ind[poz].m_TimeFrame, 'ColorZerolagTriXOSMA', smoothing1, smoothing2, IPC, Factor1, TriX_period1, Factor2, TriX_period2, Factor3, TriX_period3, Factor4, TriX_period4, Factor5, TriX_period5)
        if Ind[poz].m_Handle == INVALID_HANDLE:
            Print('OnInit()(', poz, '): Не удалось получить хендл индикатора ColorZerolagTriXOSMA')
            return False
    FONT = CFontName()
    sFontType = FONT.GetFontName(FontType)
    Deinit()
    PeriodBuffer = Arr(5, 0, dyn=False)
    PeriodBuffer[0] = TriX_period1
    PeriodBuffer[1] = TriX_period2
    PeriodBuffer[2] = TriX_period3
    PeriodBuffer[3] = TriX_period4
    PeriodBuffer[4] = TriX_period5
    min_rates_total = _int(3 * PeriodBuffer[ArrayMaximum(PeriodBuffer, 0, WHOLE_ARRAY)])
    xshift = _int(X_ + (8.3 * FontSize))
    Cap = 'ColorZerolagTriXOSMATrend_x10'
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
        sPer[poz] = GetStringTimeframe(ePer[poz])
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
        if CopyBuffer(Ind[poz].m_Handle, 1, 1, 1, Ind[poz].m_ClrInd) <= 0:
            return 0
    ColorGain = Arr(10, 0, dyn=False)
    ArrayInitialize(ColorGain, ZrColor)
    for poz in range(0, 10):
        if Ind[poz].m_ClrInd[0] == 1 or Ind[poz].m_ClrInd[0] == 4:
            ColorGain[poz] = UpColor
        if Ind[poz].m_ClrInd[0] == 0 or Ind[poz].m_ClrInd[0] == 3:
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


class ColorzerolagtrixosmatrendX10(_MQL5Indicator):
    name = 'colorzerolagtrixosmatrend_x10'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame0': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # Период графика 1
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16386),  # Период графика 2
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16387),  # Период графика 3
        'TimeFrame3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика 4
        'TimeFrame4': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16390),  # Период графика 5
        'TimeFrame5': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16392),  # Период графика 6
        'TimeFrame6': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16396),  # Период графика 7
        'TimeFrame7': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Период графика 8
        'TimeFrame8': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=32769),  # Период графика 9
        'TimeFrame9': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=49153),  # Период графика 10
        'smoothing1': 15,
        'smoothing2': 7,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Ценовая константа
        'Factor1': 0.05,
        'TriX_period1': 8,
        'Factor2': 0.1,
        'TriX_period2': 21,
        'Factor3': 0.16,
        'TriX_period3': 34,
        'Factor4': 0.26,
        'TriX_period4': 55,
        'Factor5': 0.43,
        'TriX_period5': 89,
        'FontSize': 11,  # Размер шрифта
        'FontType': _Choice({0: 'Arial', 1: 'Arial Black', 2: 'Arial Bold', 3: 'Arial Bold Italic', 4: 'Arial Italic', 5: 'Comic Sans MS Bold', 6: 'Courier', 7: 'Courier New', 8: 'Courier New Bold', 9: 'Courier New Bold Italic', 10: 'Courier New Italic', 11: 'Estrangelo Edessa', 12: 'Franklin Gothic Medium', 13: 'Gautami', 14: 'Georgia', 15: 'Georgia Bold', 16: 'Georgia Bold Italic', 17: 'Georgia Italic', 18: 'Georgia Italic Impact', 19: 'Latha', 20: 'Lucida Console', 21: 'Lucida Sans Unicode', 22: 'Modern MS Sans Serif', 23: 'MS Sans Serif', 24: 'Mv Boli', 25: 'Palatino Linotype', 26: 'Palatino Linotype Bold', 27: 'Palatino Linotype Italic', 28: 'Roman', 29: 'Script', 30: 'Small Fonts', 31: 'Symbol', 32: 'Tahoma', 33: 'Tahoma Bold', 34: 'Times New Roman', 35: 'Times New Roman Bold', 36: 'Times New Roman Bold Italic', 37: 'Times New Roman Italic', 38: 'Trebuchet MS', 39: 'Trebuchet MS Bold', 40: 'Trebuchet MS Bold Italic', 41: 'Trebuchet MS Italic', 42: 'Tunga', 43: 'Verdana', 44: 'Verdana Bold', 45: 'Verdana Bold Italic', 46: 'Verdana Italic', 47: 'Webdings', 48: 'Westminster', 49: 'Wingdings', 50: 'WST_Czech', 51: 'WST_Engl', 52: 'WST_Fren', 53: 'WST_Germ', 54: 'WST_Ital', 55: 'WST_Span', 56: 'WST_Swed'}, default=14),  # Тип шрифта
        'WhatCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=1),  # Угол расположения
        'Y_': 20,  # Расположение по вертикали
        'X_': 5,  # Расположение по горизонтали
    }

