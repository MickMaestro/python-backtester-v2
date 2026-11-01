"""ColorPEMA_Digit_Trend_x10 — converted from MQL5: MQL5 Indicators/ColorPEMA_Digit_Trend_x10/ColorPEMA_Digit_Trend_x10.mq5

Индикатор отображает направление тренда индикатора ColorPEMA_Digit с десяти разных таймфреймов
Copyright: 2011,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.getfontname import *  # #include getfontname.mqh

MQL5_META = {'props': {'copyright': '2011,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Индикатор отображает направление тренда индикатора ColorPEMA_Digit с десяти разных таймфреймов'], 'name': 'ColorPEMA_Digit_Trend_x10', 'source': 'MQL5 Indicators/ColorPEMA_Digit_Trend_x10/ColorPEMA_Digit_Trend_x10.mq5', 'folder': 'ColorPEMA_Digit_Trend_x10', 'inputs': [{'mql': 'TimeFrame0', 'py': 'TimeFrame0', 'param': 'TimeFrame0', 'type': 'int', 'default': 16385, 'label': 'период графика 1', 'sinput': False}, {'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 16386, 'label': 'период графика 2', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 16387, 'label': 'период графика 3', 'sinput': False}, {'mql': 'TimeFrame3', 'py': 'TimeFrame3', 'param': 'TimeFrame3', 'type': 'int', 'default': 16388, 'label': 'период графика 4', 'sinput': False}, {'mql': 'TimeFrame4', 'py': 'TimeFrame4', 'param': 'TimeFrame4', 'type': 'int', 'default': 16390, 'label': 'период графика 5', 'sinput': False}, {'mql': 'TimeFrame5', 'py': 'TimeFrame5', 'param': 'TimeFrame5', 'type': 'int', 'default': 16392, 'label': 'период графика 6', 'sinput': False}, {'mql': 'TimeFrame6', 'py': 'TimeFrame6', 'param': 'TimeFrame6', 'type': 'int', 'default': 16396, 'label': 'период графика 7', 'sinput': False}, {'mql': 'TimeFrame7', 'py': 'TimeFrame7', 'param': 'TimeFrame7', 'type': 'int', 'default': 16408, 'label': 'период графика 8', 'sinput': False}, {'mql': 'TimeFrame8', 'py': 'TimeFrame8', 'param': 'TimeFrame8', 'type': 'int', 'default': 32769, 'label': 'период графика 9', 'sinput': False}, {'mql': 'TimeFrame9', 'py': 'TimeFrame9', 'param': 'TimeFrame9', 'type': 'int', 'default': 49153, 'label': 'период графика 10', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для получения сигнала (0 - текущий бар)', 'sinput': False}, {'mql': 'EmaLength', 'py': 'EmaLength', 'param': 'EmaLength', 'type': 'double', 'default': 50.01, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Digit', 'py': 'Digit', 'param': 'Digit', 'type': 'uint', 'default': 2, 'label': 'количество разрядов округления', 'sinput': False}, {'mql': 'CpColor', 'py': 'CpColor', 'param': None, 'type': 'color', 'default': 14822282, 'label': 'цвет названия индикатора', 'sinput': False}, {'mql': 'BuyColor', 'py': 'BuyColor', 'param': None, 'type': 'color', 'default': 16748574, 'label': 'цвет Buy сигнала', 'sinput': False}, {'mql': 'UpColor', 'py': 'UpColor', 'param': None, 'type': 'color', 'default': 13434880, 'label': 'цвет продолжения растущего тренда', 'sinput': False}, {'mql': 'NnColor', 'py': 'NnColor', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'цвет отсутствия тренда', 'sinput': False}, {'mql': 'DnColor', 'py': 'DnColor', 'param': None, 'type': 'color', 'default': 8388736, 'label': 'цвет продолжения падающего тренда', 'sinput': False}, {'mql': 'SellColor', 'py': 'SellColor', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'цвет Sell сигнала', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 15, 'label': 'размер шрифта', 'sinput': False}, {'mql': 'FontType', 'py': 'FontType', 'param': 'FontType', 'type': 'int', 'default': 14, 'label': 'тип шрифта', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 1, 'label': 'угол расположения', 'sinput': False}, {'mql': 'Y_', 'py': 'Y_', 'param': 'Y_', 'type': 'uint', 'default': 20, 'label': 'расположение по вертикали', 'sinput': False}, {'mql': 'X_', 'py': 'X_', 'param': 'X_', 'type': 'uint', 'default': 5, 'label': 'расположение по горизонтали', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['getfontname.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
TimeFrame0 = _input('TimeFrame0', PERIOD_H1)  # период графика 1
TimeFrame1 = _input('TimeFrame1', PERIOD_H2)  # период графика 2
TimeFrame2 = _input('TimeFrame2', PERIOD_H3)  # период графика 3
TimeFrame3 = _input('TimeFrame3', PERIOD_H4)  # период графика 4
TimeFrame4 = _input('TimeFrame4', PERIOD_H6)  # период графика 5
TimeFrame5 = _input('TimeFrame5', PERIOD_H8)  # период графика 6
TimeFrame6 = _input('TimeFrame6', PERIOD_H12)  # период графика 7
TimeFrame7 = _input('TimeFrame7', PERIOD_D1)  # период графика 8
TimeFrame8 = _input('TimeFrame8', PERIOD_W1)  # период графика 9
TimeFrame9 = _input('TimeFrame9', PERIOD_MN1)  # период графика 10
SignalBar = _input('SignalBar', 1)  # Номер бара для получения сигнала (0 - текущий бар)
EmaLength = _input('EmaLength', 50.01)  # глубина сглаживания
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Digit = _input('Digit', 2)  # количество разрядов округления
CpColor = _input('CpColor', clrBlueViolet)  # цвет названия индикатора
BuyColor = _input('BuyColor', clrDodgerBlue)  # цвет Buy сигнала
UpColor = _input('UpColor', clrMediumBlue)  # цвет продолжения растущего тренда
NnColor = _input('NnColor', clrGray)  # цвет отсутствия тренда
DnColor = _input('DnColor', clrPurple)  # цвет продолжения падающего тренда
SellColor = _input('SellColor', clrMagenta)  # цвет Sell сигнала
FontSize = _input('FontSize', 15)  # размер шрифта
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
    _q_fields = ('m_Ind', 'm_Handle', 'm_TimeFrame')
    def __init__(self, *args):
        self.m_Ind = Arr(2, 0.0, dyn=False)
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
        Ind[poz].m_Handle = iCustom(Symbol(), Ind[poz].m_TimeFrame, 'ColorPEMA_Digit', EmaLength, IPC, 0, 0, Digit, '', False)
        if Ind[poz].m_Handle == INVALID_HANDLE:
            Print('OnInit()(', poz, '): Не удалось получить хендл индикатора ColorPEMA_Digit')
            return False
    FONT = CFontName()
    sFontType = FONT.GetFontName(FontType)
    Deinit()
    min_rates_total = 9 + 1
    min_rates_total += 1
    xshift = _int(X_ + (8.3 * FontSize))
    Cap = 'ColorPEMA_Digit_Trend_x10'
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
            return prev_calculated
    for poz in range(0, 10):
        if CopyBuffer(Ind[poz].m_Handle, 1, SignalBar, 2, Ind[poz].m_Ind) <= 0:
            return prev_calculated
    ColorGain = Arr(10, 0, dyn=False)
    SignalSymbol = Arr(10, "", dyn=False)
    ArrayInitialize(ColorGain, clrNONE)
    for poz in range(0, 10):
        _sw2 = _int(Ind[poz].m_Ind[1])
        if _sw2 == 2:
            _sw3 = _int(Ind[poz].m_Ind[0])
            if _sw3 == 0:
                SignalSymbol[poz] = 'ж'
                ColorGain[poz] = BuyColor
            elif _sw3 == 1:
                SignalSymbol[poz] = 'ж'
                ColorGain[poz] = BuyColor
            elif _sw3 == 2:
                SignalSymbol[poz] = 'в'
                ColorGain[poz] = UpColor
        elif _sw2 == 1:
            _sw4 = _int(Ind[poz].m_Ind[0])
            if _sw4 == 0:
                SignalSymbol[poz] = 'в'
                ColorGain[poz] = DnColor
            elif _sw4 == 1:
                SignalSymbol[poz] = 'в'
                ColorGain[poz] = NnColor
            elif _sw4 == 2:
                SignalSymbol[poz] = 'в'
                ColorGain[poz] = UpColor
        elif _sw2 == 0:
            _sw5 = _int(Ind[poz].m_Ind[0])
            if _sw5 == 0:
                SignalSymbol[poz] = 'в'
                ColorGain[poz] = DnColor
            elif _sw5 == 1:
                SignalSymbol[poz] = 'и'
                ColorGain[poz] = SellColor
            elif _sw5 == 2:
                SignalSymbol[poz] = 'и'
                ColorGain[poz] = SellColor
    for poz in range(0, 10):
        SetTLabel(0, sPerA[poz], 0, WhatCorner, 2 * WhatCorner, X_, shift[poz + 1], sPer[poz] + ': ', ColorGain[poz], sFontType, FontSize)
        SetTLabel(0, sPerB[poz], 0, WhatCorner, 2 * WhatCorner, xshift, shift[poz + 1], SignalSymbol[poz], ColorGain[poz], 'Wingdings 3', FontSize)
    SetTLabel(0, Cap, 0, WhatCorner, 2 * WhatCorner, X_, shift[0], Cap, CpColor, sFontType, FontSize)
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
Ind = Arr(10, 0, dyn=False, factory=CIndArrow)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorPEMADigitTrendX10(_MQL5Indicator):
    name = 'ColorPEMA_Digit_Trend_x10'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame0': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # период графика 1
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16386),  # период графика 2
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16387),  # период графика 3
        'TimeFrame3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # период графика 4
        'TimeFrame4': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16390),  # период графика 5
        'TimeFrame5': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16392),  # период графика 6
        'TimeFrame6': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16396),  # период графика 7
        'TimeFrame7': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # период графика 8
        'TimeFrame8': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=32769),  # период графика 9
        'TimeFrame9': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=49153),  # период графика 10
        'SignalBar': 1,  # Номер бара для получения сигнала (0 - текущий бар)
        'EmaLength': 50.01,  # глубина сглаживания
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Digit': 2,  # количество разрядов округления
        'FontSize': 15,  # размер шрифта
        'FontType': _Choice({0: 'Arial', 1: 'Arial Black', 2: 'Arial Bold', 3: 'Arial Bold Italic', 4: 'Arial Italic', 5: 'Comic Sans MS Bold', 6: 'Courier', 7: 'Courier New', 8: 'Courier New Bold', 9: 'Courier New Bold Italic', 10: 'Courier New Italic', 11: 'Estrangelo Edessa', 12: 'Franklin Gothic Medium', 13: 'Gautami', 14: 'Georgia', 15: 'Georgia Bold', 16: 'Georgia Bold Italic', 17: 'Georgia Italic', 18: 'Georgia Italic Impact', 19: 'Latha', 20: 'Lucida Console', 21: 'Lucida Sans Unicode', 22: 'Modern MS Sans Serif', 23: 'MS Sans Serif', 24: 'Mv Boli', 25: 'Palatino Linotype', 26: 'Palatino Linotype Bold', 27: 'Palatino Linotype Italic', 28: 'Roman', 29: 'Script', 30: 'Small Fonts', 31: 'Symbol', 32: 'Tahoma', 33: 'Tahoma Bold', 34: 'Times New Roman', 35: 'Times New Roman Bold', 36: 'Times New Roman Bold Italic', 37: 'Times New Roman Italic', 38: 'Trebuchet MS', 39: 'Trebuchet MS Bold', 40: 'Trebuchet MS Bold Italic', 41: 'Trebuchet MS Italic', 42: 'Tunga', 43: 'Verdana', 44: 'Verdana Bold', 45: 'Verdana Bold Italic', 46: 'Verdana Italic', 47: 'Webdings', 48: 'Westminster', 49: 'Wingdings', 50: 'WST_Czech', 51: 'WST_Engl', 52: 'WST_Fren', 53: 'WST_Germ', 54: 'WST_Ital', 55: 'WST_Span', 56: 'WST_Swed'}, default=14),  # тип шрифта
        'WhatCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=1),  # угол расположения
        'Y_': 20,  # расположение по вертикали
        'X_': 5,  # расположение по горизонтали
    }

