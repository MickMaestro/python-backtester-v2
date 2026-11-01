"""dynamix_HTF — converted from MQL5: MQL5 Indicators/dynamix_HTF/dynamix_HTF.mq5

dynamix
Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {1: 1}, 'colors': {}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': ['dynamix'], 'name': 'dynamix_HTF', 'source': 'MQL5 Indicators/dynamix_HTF/dynamix_HTF.mq5', 'folder': 'dynamix_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора', 'sinput': False}, {'mql': 'step', 'py': 'step', 'param': 'step', 'type': 'uint', 'default': 10, 'label': 'шаг построения скользящих средних, оптимальный диапазон значений - от 1 до 10', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'ColorWidth', 'py': 'ColorWidth', 'param': 'ColorWidth', 'type': 'int', 'default': 40, 'label': 'ширина цветовой палитры (изменяется от 0 до 131)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

AliceBlue = 0xFFF8F0  # MQL4 colour name
AntiqueWhite = 0xD7EBFA  # MQL4 colour name
Aqua = 0xFFFF00  # MQL4 colour name
Aquamarine = 0xD4FF7F  # MQL4 colour name
Beige = 0xDCF5F5  # MQL4 colour name
Bisque = 0xC4E4FF  # MQL4 colour name
Black = 0x000000  # MQL4 colour name
BlanchedAlmond = 0xCDEBFF  # MQL4 colour name
Blue = 0xFF0000  # MQL4 colour name
BlueViolet = 0xE22B8A  # MQL4 colour name
Brown = 0x2A2AA5  # MQL4 colour name
BurlyWood = 0x87B8DE  # MQL4 colour name
CadetBlue = 0xA09E5F  # MQL4 colour name
Chartreuse = 0x00FF7F  # MQL4 colour name
Chocolate = 0x1E69D2  # MQL4 colour name
Coral = 0x507FFF  # MQL4 colour name
CornflowerBlue = 0xED9564  # MQL4 colour name
Cornsilk = 0xDCF8FF  # MQL4 colour name
Crimson = 0x3C14DC  # MQL4 colour name
DarkBlue = 0x8B0000  # MQL4 colour name
DarkGoldenrod = 0x0B86B8  # MQL4 colour name
DarkGray = 0xA9A9A9  # MQL4 colour name
DarkGreen = 0x006400  # MQL4 colour name
DarkKhaki = 0x6BB7BD  # MQL4 colour name
DarkOliveGreen = 0x2F6B55  # MQL4 colour name
DarkOrange = 0x008CFF  # MQL4 colour name
DarkOrchid = 0xCC3299  # MQL4 colour name
DarkSalmon = 0x7A96E9  # MQL4 colour name
DarkSeaGreen = 0x8FBC8F  # MQL4 colour name
DarkSlateBlue = 0x8B3D48  # MQL4 colour name
DarkSlateGray = 0x4F4F2F  # MQL4 colour name
DarkTurquoise = 0xD1CE00  # MQL4 colour name
DarkViolet = 0xD30094  # MQL4 colour name
DeepPink = 0x9314FF  # MQL4 colour name
DeepSkyBlue = 0xFFBF00  # MQL4 colour name
DimGray = 0x696969  # MQL4 colour name
DodgerBlue = 0xFF901E  # MQL4 colour name
FireBrick = 0x2222B2  # MQL4 colour name
ForestGreen = 0x228B22  # MQL4 colour name
Gainsboro = 0xDCDCDC  # MQL4 colour name
Gold = 0x00D7FF  # MQL4 colour name
Goldenrod = 0x20A5DA  # MQL4 colour name
Gray = 0x808080  # MQL4 colour name
Green = 0x008000  # MQL4 colour name
GreenYellow = 0x2FFFAD  # MQL4 colour name
Honeydew = 0xF0FFF0  # MQL4 colour name
HotPink = 0xB469FF  # MQL4 colour name
IndianRed = 0x5C5CCD  # MQL4 colour name
Indigo = 0x82004B  # MQL4 colour name
Ivory = 0xF0FFFF  # MQL4 colour name
Khaki = 0x8CE6F0  # MQL4 colour name
Lavender = 0xFAE6E6  # MQL4 colour name
LavenderBlush = 0xF5F0FF  # MQL4 colour name
LawnGreen = 0x00FC7C  # MQL4 colour name
LemonChiffon = 0xCDFAFF  # MQL4 colour name
LightBlue = 0xE6D8AD  # MQL4 colour name
LightCoral = 0x8080F0  # MQL4 colour name
LightCyan = 0xFFFFE0  # MQL4 colour name
LightGoldenrod = 0xD2FAFA  # MQL4 colour name
LightGray = 0xD3D3D3  # MQL4 colour name
LightGreen = 0x90EE90  # MQL4 colour name
LightPink = 0xC1B6FF  # MQL4 colour name
LightSalmon = 0x7AA0FF  # MQL4 colour name
LightSeaGreen = 0xAAB220  # MQL4 colour name
LightSkyBlue = 0xFACE87  # MQL4 colour name
LightSlateGray = 0x998877  # MQL4 colour name
LightSteelBlue = 0xDEC4B0  # MQL4 colour name
LightYellow = 0xE0FFFF  # MQL4 colour name
Lime = 0x00FF00  # MQL4 colour name
LimeGreen = 0x32CD32  # MQL4 colour name
Linen = 0xE6F0FA  # MQL4 colour name
Magenta = 0xFF00FF  # MQL4 colour name
Maroon = 0x000080  # MQL4 colour name
MediumAquamarine = 0xAACD66  # MQL4 colour name
MediumBlue = 0xCD0000  # MQL4 colour name
MediumOrchid = 0xD355BA  # MQL4 colour name
MediumPurple = 0xDB7093  # MQL4 colour name
MediumSeaGreen = 0x71B33C  # MQL4 colour name
MediumSlateBlue = 0xEE687B  # MQL4 colour name
MediumSpringGreen = 0x9AFA00  # MQL4 colour name
MediumTurquoise = 0xCCD148  # MQL4 colour name
MediumVioletRed = 0x8515C7  # MQL4 colour name
MidnightBlue = 0x701919  # MQL4 colour name
MintCream = 0xFAFFF5  # MQL4 colour name
MistyRose = 0xE1E4FF  # MQL4 colour name
Moccasin = 0xB5E4FF  # MQL4 colour name
NavajoWhite = 0xADDEFF  # MQL4 colour name
Navy = 0x800000  # MQL4 colour name
OldLace = 0xE6F5FD  # MQL4 colour name
Olive = 0x008080  # MQL4 colour name
OliveDrab = 0x238E6B  # MQL4 colour name
Orange = 0x00A5FF  # MQL4 colour name
OrangeRed = 0x0045FF  # MQL4 colour name
Orchid = 0xD670DA  # MQL4 colour name
PaleGoldenrod = 0xAAE8EE  # MQL4 colour name
PaleGreen = 0x98FB98  # MQL4 colour name
PaleTurquoise = 0xEEEEAF  # MQL4 colour name
PaleVioletRed = 0x9370DB  # MQL4 colour name
PapayaWhip = 0xD5EFFF  # MQL4 colour name
PeachPuff = 0xB9DAFF  # MQL4 colour name
Peru = 0x3F85CD  # MQL4 colour name
Pink = 0xCBC0FF  # MQL4 colour name
Plum = 0xDDA0DD  # MQL4 colour name
PowderBlue = 0xE6E0B0  # MQL4 colour name
Purple = 0x800080  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name
RosyBrown = 0x8F8FBC  # MQL4 colour name
RoyalBlue = 0xE16941  # MQL4 colour name
SaddleBrown = 0x13458B  # MQL4 colour name
Salmon = 0x7280FA  # MQL4 colour name
SandyBrown = 0x60A4F4  # MQL4 colour name
SeaGreen = 0x578B2E  # MQL4 colour name
Seashell = 0xEEF5FF  # MQL4 colour name
Sienna = 0x2D52A0  # MQL4 colour name
Silver = 0xC0C0C0  # MQL4 colour name
SkyBlue = 0xEBCE87  # MQL4 colour name
SlateBlue = 0xCD5A6A  # MQL4 colour name
SlateGray = 0x908070  # MQL4 colour name
Snow = 0xFAFAFF  # MQL4 colour name
SpringGreen = 0x7FFF00  # MQL4 colour name
SteelBlue = 0xB48246  # MQL4 colour name
Tan = 0x8CB4D2  # MQL4 colour name
Teal = 0x808000  # MQL4 colour name
Thistle = 0xD8BFD8  # MQL4 colour name
Tomato = 0x4763FF  # MQL4 colour name
Turquoise = 0xD0E040  # MQL4 colour name
Violet = 0xEE82EE  # MQL4 colour name
Wheat = 0xB3DEF5  # MQL4 colour name
White = 0xFFFFFF  # MQL4 colour name
WhiteSmoke = 0xF5F5F5  # MQL4 colour name
Yellow = 0x00FFFF  # MQL4 colour name
YellowGreen = 0x32CD9A  # MQL4 colour name

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
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора
step = _input('step', 10)  # шаг построения скользящих средних, оптимальный диапазон значений - от 1 до 10
IPC = _input('IPC', PRICE_CLOSE)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
ColorWidth = _input('ColorWidth', 40)  # ширина цветовой палитры (изменяется от 0 до 131)
Symbol_ = ""
Word = ""
min_rates_total = 0
Ind_Handle = 0

class CIndicatorsBuffers(MqlObject):
    _q_fields = ('IndBuffer',)
    def __init__(self, *args):
        self.IndBuffer = Arr(0, 0.0)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('dynamix', TimeFrame):
        return INIT_FAILED
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'dynamix', step, IPC, 0, 40)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ' + 'dynamix')
        return INIT_FAILED
    min_rates_total = 2
    ArrayColors = Arr.of([_uint(Black), _uint(DarkGreen), _uint(DarkSlateGray), _uint(Olive), _uint(Green), _uint(Teal), _uint(Navy), _uint(Purple), _uint(Maroon), _uint(Indigo), _uint(MidnightBlue), _uint(DarkBlue), _uint(DarkOliveGreen), _uint(SaddleBrown), _uint(ForestGreen), _uint(OliveDrab), _uint(SeaGreen), _uint(DarkGoldenrod), _uint(DarkSlateBlue), _uint(Sienna), _uint(MediumBlue), _uint(Brown), _uint(DarkTurquoise), _uint(DimGray), _uint(LightSeaGreen), _uint(DarkViolet), _uint(FireBrick), _uint(MediumVioletRed), _uint(MediumSeaGreen), _uint(Chocolate), _uint(Crimson), _uint(SteelBlue), _uint(Goldenrod), _uint(MediumSpringGreen), _uint(LawnGreen), _uint(CadetBlue), _uint(DarkOrchid), _uint(YellowGreen), _uint(LimeGreen), _uint(OrangeRed), _uint(DarkOrange), _uint(Orange), _uint(Gold), _uint(Yellow), _uint(Chartreuse), _uint(Lime), _uint(SpringGreen), _uint(Aqua), _uint(DeepSkyBlue), _uint(Blue), _uint(Magenta), _uint(Red), _uint(Gray), _uint(SlateGray), _uint(Peru), _uint(BlueViolet), _uint(LightSlateGray), _uint(DeepPink), _uint(MediumTurquoise), _uint(DodgerBlue), _uint(Turquoise), _uint(RoyalBlue), _uint(SlateBlue), _uint(DarkKhaki), _uint(IndianRed), _uint(MediumOrchid), _uint(GreenYellow), _uint(MediumAquamarine), _uint(DarkSeaGreen), _uint(Tomato), _uint(RosyBrown), _uint(Orchid), _uint(MediumPurple), _uint(PaleVioletRed), _uint(Coral), _uint(CornflowerBlue), _uint(DarkGray), _uint(SandyBrown), _uint(MediumSlateBlue), _uint(Tan), _uint(DarkSalmon), _uint(BurlyWood), _uint(HotPink), _uint(Salmon), _uint(Violet), _uint(LightCoral), _uint(SkyBlue), _uint(LightSalmon), _uint(Plum), _uint(Khaki), _uint(LightGreen), _uint(Aquamarine), _uint(Silver), _uint(LightSkyBlue), _uint(LightSteelBlue), _uint(LightBlue), _uint(PaleGreen), _uint(Thistle), _uint(PowderBlue), _uint(PaleGoldenrod), _uint(PaleTurquoise), _uint(LightGray), _uint(Wheat), _uint(NavajoWhite), _uint(Moccasin), _uint(LightPink), _uint(Gainsboro), _uint(PeachPuff), _uint(Pink), _uint(Bisque), _uint(LightGoldenrod), _uint(BlanchedAlmond), _uint(LemonChiffon), _uint(Beige), _uint(AntiqueWhite), _uint(PapayaWhip), _uint(Cornsilk), _uint(LightYellow), _uint(LightCyan), _uint(Linen), _uint(Lavender), _uint(MistyRose), _uint(OldLace), _uint(WhiteSmoke), _uint(Seashell), _uint(Ivory), _uint(Honeydew), _uint(AliceBlue), _uint(LavenderBlush), _uint(MintCream), _uint(Snow), _uint(White)], fill=0)
    size = ArraySize(ArrayColors)
    size -= 2
    ColorWidth_ = ColorWidth
    if ColorWidth > size:
        ColorWidth_ = size
    if ColorWidth < 1:
        ColorWidth_ = 1
    Colors = Arr(0, 0)
    if ArrayResize(Colors, ColorWidth_) < ColorWidth_:
        Print('Не удалось распределить память под массив Colors')
    ArrayCopy(Colors, ArrayColors, 0, 2, ColorWidth_)
    ArraySetAsSeries(Colors, True)
    K = _fdiv(ColorWidth_, 27 * 1.0)
    for numb in range(0, 27):
        shortname = Box('')
        StringConcatenate(shortname, 'dynamix', numb)
        PlotIndexSetString(numb, PLOT_LABEL, shortname.v)
        PlotIndexSetDouble(numb, PLOT_EMPTY_VALUE, EMPTY_VALUE)
        PlotIndexSetInteger(numb, PLOT_DRAW_BEGIN, min_rates_total)
        SetIndexBuffer(numb, Ind[numb].IndBuffer, INDICATOR_DATA)
        ArraySetAsSeries(Ind[numb].IndBuffer, True)
        PlotIndexSetInteger(numb, PLOT_DRAW_TYPE, PlotIndexGetInteger(0, PLOT_DRAW_TYPE))
        PlotIndexSetInteger(numb, PLOT_LINE_STYLE, PlotIndexGetInteger(0, PLOT_LINE_STYLE))
        PlotIndexSetInteger(numb, PLOT_LINE_WIDTH, PlotIndexGetInteger(0, PLOT_LINE_WIDTH))
        PlotIndexSetInteger(numb, PLOT_LINE_COLOR, Colors[_int(numb * K)])
    shortname = Box("")
    StringConcatenate(shortname, 'dynamix', 27, '(', step, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    for numb in range(0, 27):
        if not CountIndicator(numb, "", TimeFrame, Ind_Handle, numb, Ind[numb].IndBuffer, time, rates_total, prev_calculated, min_rates_total):
            return 0
    return rates_total

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb, IndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        IndBuf[bar] = 0.0
        if CopyTime(Symbol_, TFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            Arr_ = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf[bar] = Arr_[0]
        else:
            IndBuf[bar] = IndBuf[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика!')
        Print('Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- global variables initialised from expressions
Ind = Arr(27, 0, dyn=False, factory=CIndicatorsBuffers)

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(27, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DynamixHTF(_MQL5Indicator):
    name = 'dynamix_HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора
        'step': 10,  # шаг построения скользящих средних, оптимальный диапазон значений - от 1 до 10
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'ColorWidth': 40,  # ширина цветовой палитры (изменяется от 0 до 131)
    }

