"""SignalTable_Sar_RSI_MA — converted from MQL5: MQL5 Indicators/SignalTable_Sar_RSI_MA/SignalTable_Sar_RSI_MA.mq5

Cигналы на покупку и продажу с нескольких индикаторов и разных таймфреймов в виде таблицы
Copyright: 2011,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.getfontname import *  # #include getfontname.mqh

MQL5_META = {'props': {'copyright': '2011,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Cигналы на покупку и продажу с нескольких индикаторов и разных таймфреймов в виде таблицы'], 'name': 'SignalTable_Sar_RSI_MA', 'source': 'MQL5 Indicators/SignalTable_Sar_RSI_MA/SignalTable_Sar_RSI_MA.mq5', 'folder': 'SignalTable_Sar_RSI_MA', 'inputs': [{'mql': 'Symbol_', 'py': 'Symbol_', 'param': None, 'type': 'string', 'default': '', 'label': 'финансовый актив', 'sinput': False}, {'mql': 'info1', 'py': 'info1', 'param': None, 'type': 'string', 'default': '<<<==============  Параметры iSAR ===============>>>', 'label': '', 'sinput': True}, {'mql': 'SARStep', 'py': 'SARStep', 'param': 'SARStep', 'type': 'double', 'default': 0.02, 'label': 'Шаг iSAR', 'sinput': False}, {'mql': 'SARMaximum', 'py': 'SARMaximum', 'param': 'SARMaximum', 'type': 'double', 'default': 0.2, 'label': 'Максимум iSAR', 'sinput': False}, {'mql': 'SARNumberofBar', 'py': 'SARNumberofBar', 'param': 'SARNumberofBar', 'type': 'uint', 'default': 0, 'label': 'Номер бара для получения сигнала iSAR', 'sinput': False}, {'mql': 'info2', 'py': 'info2', 'param': None, 'type': 'string', 'default': '<<<============  Параметры Мувингов =============>>>', 'label': '', 'sinput': True}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'FastMA', 'py': 'FastMA', 'param': 'FastMA', 'type': 'uint', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'SlowMA', 'py': 'SlowMA', 'param': 'SlowMA', 'type': 'uint', 'default': 24, 'label': '', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MANumberofBar', 'py': 'MANumberofBar', 'param': 'MANumberofBar', 'type': 'uint', 'default': 0, 'label': 'Номер бара для получения сигнала Мувингов', 'sinput': False}, {'mql': 'info3', 'py': 'info3', 'param': None, 'type': 'string', 'default': '<<<==============  Параметры iRSI ===============>>>', 'label': '', 'sinput': True}, {'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'RSIHighLevel', 'py': 'RSIHighLevel', 'param': 'RSIHighLevel', 'type': 'uint', 'default': 60, 'label': 'уровень перезакупа iRSI', 'sinput': False}, {'mql': 'RSILowLevel', 'py': 'RSILowLevel', 'param': 'RSILowLevel', 'type': 'uint', 'default': 40, 'label': 'уровень перепроданности iRSI', 'sinput': False}, {'mql': 'RSIInvert', 'py': 'RSIInvert', 'param': 'RSIInvert', 'type': 'bool', 'default': True, 'label': 'инвертирование сигналов iRSI', 'sinput': False}, {'mql': 'RSINumberofBar', 'py': 'RSINumberofBar', 'param': 'RSINumberofBar', 'type': 'uint', 'default': 0, 'label': 'Номер бара для получения сигнала RSI', 'sinput': False}, {'mql': 'info4', 'py': 'info4', 'param': None, 'type': 'string', 'default': '<<< === Параметры визуального отображения индикатора === >>>', 'label': '', 'sinput': True}, {'mql': 'TextColor', 'py': 'TextColor', 'param': None, 'type': 'color', 'default': 14822282, 'label': 'цвет текста', 'sinput': False}, {'mql': 'UpColor', 'py': 'UpColor', 'param': None, 'type': 'color', 'default': 16748574, 'label': 'цвет растущего тренда', 'sinput': False}, {'mql': 'MdColor', 'py': 'MdColor', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'цвет отсутствия тренда', 'sinput': False}, {'mql': 'DnColor', 'py': 'DnColor', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'цвет падающего тренда', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 13, 'label': 'размер шрифта', 'sinput': False}, {'mql': 'FontType', 'py': 'FontType', 'param': 'FontType', 'type': 'int', 'default': 14, 'label': 'тип шрифта', 'sinput': False}, {'mql': 'WhatCorner', 'py': 'WhatCorner', 'param': 'WhatCorner', 'type': 'int', 'default': 1, 'label': 'угол расположения', 'sinput': False}, {'mql': 'Y_', 'py': 'Y_', 'param': 'Y_', 'type': 'uint', 'default': 20, 'label': 'расположение по вертикали', 'sinput': False}, {'mql': 'X_', 'py': 'X_', 'param': 'X_', 'type': 'uint', 'default': 5, 'label': 'расположение по горизонтали', 'sinput': False}, {'mql': 'LableSirname', 'py': 'LableSirname', 'param': None, 'type': 'string', 'default': 'SignalTable_Sar_RSI_MA 1', 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['getfontname.mqh']}

# ---- inputs and global variables
Symbol_ = _input('Symbol_', '')  # финансовый актив
info1 = _input('info1', '<<<==============  Параметры iSAR ===============>>>')
SARStep = _input('SARStep', 0.02)  # Шаг iSAR
SARMaximum = _input('SARMaximum', 0.2)  # Максимум iSAR
SARNumberofBar = _input('SARNumberofBar', 0)  # Номер бара для получения сигнала iSAR
info2 = _input('info2', '<<<============  Параметры Мувингов =============>>>')
MAType = _input('MAType', MODE_EMA)
FastMA = _input('FastMA', 13)
SlowMA = _input('SlowMA', 24)
MAPrice = _input('MAPrice', PRICE_CLOSE)
MANumberofBar = _input('MANumberofBar', 0)  # Номер бара для получения сигнала Мувингов
info3 = _input('info3', '<<<==============  Параметры iRSI ===============>>>')
RSIPeriod = _input('RSIPeriod', 14)
RSIPrice = _input('RSIPrice', PRICE_CLOSE)
RSIHighLevel = _input('RSIHighLevel', 60)  # уровень перезакупа iRSI
RSILowLevel = _input('RSILowLevel', 40)  # уровень перепроданности iRSI
RSIInvert = _input('RSIInvert', True)  # инвертирование сигналов iRSI
RSINumberofBar = _input('RSINumberofBar', 0)  # Номер бара для получения сигнала RSI
info4 = _input('info4', '<<< === Параметры визуального отображения индикатора === >>>')
TextColor = _input('TextColor', clrBlueViolet)  # цвет текста
UpColor = _input('UpColor', clrDodgerBlue)  # цвет растущего тренда
MdColor = _input('MdColor', clrGray)  # цвет отсутствия тренда
DnColor = _input('DnColor', clrMagenta)  # цвет падающего тренда
FontSize = _input('FontSize', 13)  # размер шрифта
FontType = _input('FontType', Font14)  # тип шрифта
WhatCorner = _input('WhatCorner', CORNER_LEFT_LOWER)  # угол расположения
Y_ = _input('Y_', 20)  # расположение по вертикали
X_ = _input('X_', 5)  # расположение по горизонтали
LableSirname = _input('LableSirname', 'SignalTable_Sar_RSI_MA 1')
min_rates_total = 0
Width = 0.0
SPoint = 0
sFontType = ""
Lable1 = ""
Lable2 = ""
Lable3 = ""
Lable4 = ""
Lable1_ = Arr(9, "", dyn=False)
Lable2_ = Arr(9, "", dyn=False)
Lable3_ = Arr(9, "", dyn=False)
Lable4_ = Arr(9, "", dyn=False)
symbol = ""
shift_1 = 0
shift_2 = 0
shift_3 = 0
shift_4 = 0
X1 = 0
X2 = 0
X2i = Arr(9, 0, dyn=False)
period = Arr.of([PERIOD_M1, PERIOD_M5, PERIOD_M15, PERIOD_M30, PERIOD_H1, PERIOD_H4, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
signalNameString = Arr.of(['MA', 'RSI', 'SAR'], fill="")
FsMA_Handle = Arr(9, 0, dyn=False)
SlMA_Handle = Arr(9, 0, dyn=False)
RSI_Handle = Arr(9, 0, dyn=False)
SAR_Handle = Arr(9, 0, dyn=False)

class CArray(MqlObject):
    _q_fields = ('IndArr',)
    def __init__(self, *args):
        self.IndArr = Arr(0, 0.0)

def OnInit():
    global Lable1, Lable2, Lable3, Lable4, SPoint, Width, X1, X2, min_rates_total, sFontType, shift_1, shift_2, shift_3, shift_4, symbol
    min_rates_total = 1
    if Symbol_ != '':
        symbol = Symbol_
    else:
        symbol = Symbol()
    Width = 3.3
    SPoint = 2 * WhatCorner
    for iii in range(0, 9):
        FsMA_Handle[iii] = iMA(symbol, period[iii], FastMA, 0, MAType, MAPrice)
        if FsMA_Handle[iii] == INVALID_HANDLE:
            Print(' Не удалось получить хендл индикатора iMA')
        SlMA_Handle[iii] = iMA(symbol, period[iii], SlowMA, 0, MAType, MAPrice)
        if SlMA_Handle[iii] == INVALID_HANDLE:
            Print(' Не удалось получить хендл индикатора iMA')
        RSI_Handle[iii] = iRSI(symbol, period[iii], RSIPeriod, RSIPrice)
        if RSI_Handle[iii] == INVALID_HANDLE:
            Print(' Не удалось получить хендл индикатора iRSI')
        SAR_Handle[iii] = iSAR(symbol, period[iii], SARStep, SARMaximum)
        if SAR_Handle[iii] == INVALID_HANDLE:
            Print(' Не удалось получить хендл индикатора iSAR')
    FONT = CFontName()
    sFontType = FONT.GetFontName(FontType)
    Deinit()
    Lable1 = LableSirname + '_' + 'String_0'
    Lable2 = LableSirname + '_' + 'String_1'
    Lable3 = LableSirname + '_' + 'String_2'
    Lable4 = LableSirname + '_' + 'String_3'
    for iii in range(0, 9):
        Lable1_[iii] = LableSirname + '_' + 'String_0_' + _str(iii)
        Lable2_[iii] = LableSirname + '_' + 'String_1_' + _str(iii)
        Lable3_[iii] = LableSirname + '_' + 'String_2_' + _str(iii)
        Lable4_[iii] = LableSirname + '_' + 'String_3_' + _str(iii)
    _sw1 = WhatCorner
    if _sw1 == CORNER_RIGHT_LOWER:
        shift_1 = _int(Y_ + (FontSize * 6))
        shift_2 = _int(Y_ + (FontSize * 4))
        shift_3 = _int(Y_ + (FontSize * 2))
        shift_4 = _int(Y_ + 0)
        X1 = _int(X_ + (FontSize * 3))
        X2 = _int(X_)
    elif _sw1 == CORNER_LEFT_LOWER:
        shift_1 = _int(Y_ + (FontSize * 6))
        shift_2 = _int(Y_ + (FontSize * 4))
        shift_3 = _int(Y_ + (FontSize * 2))
        shift_4 = _int(Y_ + 0)
        X1 = _int(X_)
        X2 = X_ + (FontSize * 5)
    elif _sw1 == CORNER_RIGHT_UPPER:
        shift_1 = _int(Y_ + 0)
        shift_2 = _int(Y_ + (FontSize * 2))
        shift_3 = _int(Y_ + (FontSize * 4))
        shift_4 = _int(Y_ + (FontSize * 6))
        X1 = _int(X_ + (FontSize * 3))
        X2 = _int(X_)
    elif _sw1 == CORNER_LEFT_UPPER:
        shift_1 = _int(Y_ + 0)
        shift_2 = _int(Y_ + (FontSize * 2))
        shift_3 = _int(Y_ + (FontSize * 4))
        shift_4 = _int(Y_ + (FontSize * 6))
        X1 = _int(X_)
        X2 = _int(X_ + (FontSize * 5))
    SetTLabel(0, Lable1, 0, WhatCorner, SPoint, X1, shift_1, 'Sar: ', TextColor, sFontType, FontSize)
    SetTLabel(0, Lable2, 0, WhatCorner, SPoint, X1, shift_2, 'RSI: ', TextColor, sFontType, FontSize)
    SetTLabel(0, Lable3, 0, WhatCorner, SPoint, X1, shift_3, 'MA: ', TextColor, sFontType, FontSize)
    for iii in range(0, 9):
        X2i[iii] = X2 + _int(Width * iii * FontSize)
    for iii in range(0, 9):
        SetTLabel(0, Lable4_[iii], 0, WhatCorner, SPoint, X2i[iii], shift_4, GetStringTimeframe(period[iii]), TextColor, sFontType, FontSize)

def OnDeinit(reason):
    Deinit()
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for iii in range(0, 9):
        if ((BarsCalculated(FsMA_Handle[iii]) < min_rates_total or BarsCalculated(SlMA_Handle[iii]) < min_rates_total) or BarsCalculated(RSI_Handle[iii]) < min_rates_total) or BarsCalculated(SAR_Handle[iii]) < min_rates_total:
            return 0
    FsMA = Arr(9, 0, dyn=False, factory=CArray)
    SlMA = Arr(9, 0, dyn=False, factory=CArray)
    RSI = Arr(9, 0, dyn=False, factory=CArray)
    SAR = Arr(9, 0, dyn=False, factory=CArray)
    Symb = ""
    Color = 0
    for iii in range(0, 9):
        if CopyBuffer(RSI_Handle[iii], 0, RSINumberofBar, 1, RSI[iii].IndArr) <= 0:
            return 0
        if CopyBuffer(SAR_Handle[iii], 0, SARNumberofBar, 1, SAR[iii].IndArr) <= 0:
            return 0
        if CopyBuffer(FsMA_Handle[iii], 0, MANumberofBar, 1, FsMA[iii].IndArr) <= 0:
            return 0
        if CopyBuffer(SlMA_Handle[iii], 0, MANumberofBar, 1, SlMA[iii].IndArr) <= 0:
            return 0
    for iii in range(0, 9):
        if SAR[iii].IndArr[0] < close[rates_total - 1]:
            Symb = 'г'
            Color = UpColor
        elif SAR[iii].IndArr[0] > close[rates_total - 1]:
            Symb = 'д'
            Color = DnColor
        else:
            Symb = 'в'
            Color = MdColor
        SetTLabel(0, Lable1_[iii], 0, WhatCorner, SPoint, X2i[iii], shift_1, Symb, Color, 'Wingdings 3', FontSize)
    for iii in range(0, 9):
        if RSI[iii].IndArr[0] < RSILowLevel:
            if RSIInvert:
                Symb = 'г'
                Color = UpColor
            else:
                Symb = 'д'
                Color = DnColor
        elif RSI[iii].IndArr[0] > RSIHighLevel:
            if RSIInvert:
                Symb = 'д'
                Color = DnColor
            else:
                Symb = 'г'
                Color = UpColor
        else:
            Symb = 'в'
            Color = MdColor
        SetTLabel(0, Lable2_[iii], 0, WhatCorner, SPoint, X2i[iii], shift_2, Symb, Color, 'Wingdings 3', FontSize)
    for iii in range(0, 9):
        if FsMA[iii].IndArr[0] > SlMA[iii].IndArr[0]:
            Symb = 'г'
            Color = UpColor
        elif FsMA[iii].IndArr[0] < SlMA[iii].IndArr[0]:
            Symb = 'д'
            Color = DnColor
        else:
            Symb = 'в'
            Color = MdColor
        SetTLabel(0, Lable3_[iii], 0, WhatCorner, SPoint, X2i[iii], shift_3, Symb, Color, 'Wingdings 3', FontSize)
    ChartRedraw(0)
    return rates_total

def Deinit():
    ObjectDelete(0, Lable1)
    ObjectDelete(0, Lable2)
    ObjectDelete(0, Lable3)
    ObjectDelete(0, Lable4)
    for iii in range(0, 9):
        ObjectDelete(0, Lable1_[iii])
        ObjectDelete(0, Lable2_[iii])
        ObjectDelete(0, Lable3_[iii])
        ObjectDelete(0, Lable4_[iii])

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

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
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetTLabel(chart_id, name, nwin, corner, point, X, Y, text, Color, Font, Size):
    if ObjectFind(chart_id, name) == -1:
        CreateTLabel(chart_id, name, nwin, corner, point, X, Y, text, Color, Font, Size)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectSetInteger(chart_id, name, OBJPROP_XDISTANCE, X)
        ObjectSetInteger(chart_id, name, OBJPROP_YDISTANCE, Y)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
        ObjectSetString(chart_id, name, OBJPROP_FONT, Font)
        ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, Size)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SignalTableSarRSIMA(_MQL5Indicator):
    name = 'SignalTable_Sar_RSI_MA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SARStep': 0.02,  # Шаг iSAR
        'SARMaximum': 0.2,  # Максимум iSAR
        'SARNumberofBar': 0,  # Номер бара для получения сигнала iSAR
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'FastMA': 13,
        'SlowMA': 24,
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'MANumberofBar': 0,  # Номер бара для получения сигнала Мувингов
        'RSIPeriod': 14,
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'RSIHighLevel': 60,  # уровень перезакупа iRSI
        'RSILowLevel': 40,  # уровень перепроданности iRSI
        'RSIInvert': True,  # инвертирование сигналов iRSI
        'RSINumberofBar': 0,  # Номер бара для получения сигнала RSI
        'FontSize': 13,  # размер шрифта
        'FontType': _Choice({0: 'Arial', 1: 'Arial Black', 2: 'Arial Bold', 3: 'Arial Bold Italic', 4: 'Arial Italic', 5: 'Comic Sans MS Bold', 6: 'Courier', 7: 'Courier New', 8: 'Courier New Bold', 9: 'Courier New Bold Italic', 10: 'Courier New Italic', 11: 'Estrangelo Edessa', 12: 'Franklin Gothic Medium', 13: 'Gautami', 14: 'Georgia', 15: 'Georgia Bold', 16: 'Georgia Bold Italic', 17: 'Georgia Italic', 18: 'Georgia Italic Impact', 19: 'Latha', 20: 'Lucida Console', 21: 'Lucida Sans Unicode', 22: 'Modern MS Sans Serif', 23: 'MS Sans Serif', 24: 'Mv Boli', 25: 'Palatino Linotype', 26: 'Palatino Linotype Bold', 27: 'Palatino Linotype Italic', 28: 'Roman', 29: 'Script', 30: 'Small Fonts', 31: 'Symbol', 32: 'Tahoma', 33: 'Tahoma Bold', 34: 'Times New Roman', 35: 'Times New Roman Bold', 36: 'Times New Roman Bold Italic', 37: 'Times New Roman Italic', 38: 'Trebuchet MS', 39: 'Trebuchet MS Bold', 40: 'Trebuchet MS Bold Italic', 41: 'Trebuchet MS Italic', 42: 'Tunga', 43: 'Verdana', 44: 'Verdana Bold', 45: 'Verdana Bold Italic', 46: 'Verdana Italic', 47: 'Webdings', 48: 'Westminster', 49: 'Wingdings', 50: 'WST_Czech', 51: 'WST_Engl', 52: 'WST_Fren', 53: 'WST_Germ', 54: 'WST_Ital', 55: 'WST_Span', 56: 'WST_Swed'}, default=14),  # тип шрифта
        'WhatCorner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=1),  # угол расположения
        'Y_': 20,  # расположение по вертикали
        'X_': 5,  # расположение по горизонтали
    }

