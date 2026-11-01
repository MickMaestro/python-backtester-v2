"""XMA-XN_HTF — converted from MQL5: MQL5 Indicators/XMA-XN_HTF/XMA-XN_HTF.mq5

XMA-XN с фиксированным во входных параметрах таймфреймом
Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {1: 1}, 'colors': {}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': ['XMA-XN с фиксированным во входных параметрах таймфреймом'], 'name': 'XMA-XN_HTF', 'source': 'MQL5 Indicators/XMA-XN_HTF/XMA-XN_HTF.mq5', 'folder': 'XMA-XN_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора', 'sinput': False}, {'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'int', 'default': 10, 'label': 'шаг периода', 'sinput': False}, {'mql': 'xMA_Method', 'py': 'xMA_Method', 'param': 'xMA_Method', 'type': 'int', 'default': 4, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'xLength', 'py': 'xLength', 'param': 'xLength', 'type': 'int', 'default': 3, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'xPhase', 'py': 'xPhase', 'param': 'xPhase', 'type': 'int', 'default': 100, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}, {'mql': 'ColorWidth', 'py': 'ColorWidth', 'param': 'ColorWidth', 'type': 'int', 'default': 40, 'label': 'ширина цветовой палитры (изменяется от 0 до 131)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum Smooth_Method
MODE_SMA_ = 0
MODE_EMA_ = 1
MODE_SMMA_ = 2
MODE_LWMA_ = 3
MODE_JJMA = 4
MODE_JurX = 5
MODE_ParMA = 6
MODE_T3 = 7
MODE_VIDYA = 8
MODE_AMA = 9
_enum('Smooth_Method', {0: 'MODE_SMA_', 1: 'MODE_EMA_', 2: 'MODE_SMMA_', 3: 'MODE_LWMA_', 4: 'MODE_JJMA', 5: 'MODE_JurX', 6: 'MODE_ParMA', 7: 'MODE_T3', 8: 'MODE_VIDYA', 9: 'MODE_AMA'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора
Step = _input('Step', 10)  # шаг периода
xMA_Method = _input('xMA_Method', MODE_JJMA)  # метод усреднения
xLength = _input('xLength', 3)  # глубина сглаживания
xPhase = _input('xPhase', 100)  # параметр сглаживания,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
ColorWidth = _input('ColorWidth', 40)  # ширина цветовой палитры (изменяется от 0 до 131)
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
    if not TimeFramesCheck('XMA-XN', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, '::Indicators\\XMA-XN', Step, xMA_Method, xLength, xPhase, IPC, 0, PriceShift, ColorWidth)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора XMA-XN')
        return INIT_FAILED
    ArrayColors = Arr.of([clrBlack, clrDarkGreen, clrDarkSlateGray, clrOlive, clrGreen, clrTeal, clrNavy, clrPurple, clrMaroon, clrIndigo, clrMidnightBlue, clrDarkBlue, clrDarkOliveGreen, clrSaddleBrown, clrForestGreen, clrOliveDrab, clrSeaGreen, clrDarkGoldenrod, clrDarkSlateBlue, clrSienna, clrMediumBlue, clrBrown, clrDarkTurquoise, clrDimGray, clrLightSeaGreen, clrDarkViolet, clrFireBrick, clrMediumVioletRed, clrMediumSeaGreen, clrChocolate, clrCrimson, clrSteelBlue, clrGoldenrod, clrMediumSpringGreen, clrLawnGreen, clrCadetBlue, clrDarkOrchid, clrYellowGreen, clrLimeGreen, clrOrangeRed, clrDarkOrange, clrOrange, clrGold, clrYellow, clrChartreuse, clrLime, clrSpringGreen, clrAqua, clrDeepSkyBlue, clrBlue, clrMagenta, clrRed, clrGray, clrSlateGray, clrPeru, clrBlueViolet, clrLightSlateGray, clrDeepPink, clrMediumTurquoise, clrDodgerBlue, clrTurquoise, clrRoyalBlue, clrSlateBlue, clrDarkKhaki, clrIndianRed, clrMediumOrchid, clrGreenYellow, clrMediumAquamarine, clrDarkSeaGreen, clrTomato, clrRosyBrown, clrOrchid, clrMediumPurple, clrPaleVioletRed, clrCoral, clrCornflowerBlue, clrDarkGray, clrSandyBrown, clrMediumSlateBlue, clrTan, clrDarkSalmon, clrBurlyWood, clrHotPink, clrSalmon, clrViolet, clrLightCoral, clrSkyBlue, clrLightSalmon, clrPlum, clrKhaki, clrLightGreen, clrAquamarine, clrSilver, clrLightSkyBlue, clrLightSteelBlue, clrLightBlue, clrPaleGreen, clrThistle, clrPowderBlue, clrPaleGoldenrod, clrPaleTurquoise, clrLightGray, clrWheat, clrNavajoWhite, clrMoccasin, clrLightPink, clrGainsboro, clrPeachPuff, clrPink, clrBisque, clrLightGoldenrod, clrBlanchedAlmond, clrLemonChiffon, clrBeige, clrAntiqueWhite, clrPapayaWhip, clrCornsilk, clrLightYellow, clrLightCyan, clrLinen, clrLavender, clrMistyRose, clrOldLace, clrWhiteSmoke, clrSeashell, clrIvory, clrHoneydew, clrAliceBlue, clrLavenderBlush, clrMintCream, clrSnow, clrWhite], fill=0)
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
    K = _fdiv(ColorWidth_, 100 * 1.0)
    period = Arr(100, 0, dyn=False)
    for numb in range(0, 100):
        period[numb] = xLength + (Step * numb)
        shortname = Box('')
        StringConcatenate(shortname, 'XMA-X', numb, '(', period[numb], ')')
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
    StringConcatenate(shortname, 'XMA-XN', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    for numb in range(0, 100):
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
        if CopyTime(Symbol(), TFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return False
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            Arr_ = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return False
            IndBuf[bar] = Arr_[0]
        else:
            IndBuf[bar] = IndBuf[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика!')
        Print('Следует изменить входные параметры индикатора!')
        return False
    return True

# ---- global variables initialised from expressions
Ind = Arr(100, 0, dyn=False, factory=CIndicatorsBuffers)

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(100, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XMAXNHTF(_MQL5Indicator):
    name = 'XMA-XN_HTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора
        'Step': 10,  # шаг периода
        'xMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения
        'xLength': 3,  # глубина сглаживания
        'xPhase': 100,  # параметр сглаживания,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # cдвиг индикатора по вертикали в пунктах
        'ColorWidth': 40,  # ширина цветовой палитры (изменяется от 0 до 131)
    }

