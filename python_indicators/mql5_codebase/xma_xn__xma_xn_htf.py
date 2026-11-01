"""XMA-XN — converted from MQL5: MQL5 Indicators/XMA-XN_HTF/XMA-XN.mq5

XMA-X
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {1: 1}, 'colors': {}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': ['XMA-X'], 'name': 'XMA-XN', 'source': 'MQL5 Indicators/XMA-XN_HTF/XMA-XN.mq5', 'folder': 'XMA-XN_HTF', 'inputs': [{'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'int', 'default': 10, 'label': 'шаг периода', 'sinput': False}, {'mql': 'xMA_Method', 'py': 'xMA_Method', 'param': 'xMA_Method', 'type': 'int', 'default': 4, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'xLength', 'py': 'xLength', 'param': 'xLength', 'type': 'int', 'default': 3, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'xPhase', 'py': 'xPhase', 'param': 'xPhase', 'type': 'int', 'default': 100, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}, {'mql': 'ColorWidth', 'py': 'ColorWidth', 'param': 'ColorWidth', 'type': 'int', 'default': 40, 'label': 'ширина цветовой палитры (изменяется от 0 до 131)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
Step = _input('Step', 10)  # шаг периода
xMA_Method = _input('xMA_Method', MODE_JJMA)  # метод усреднения
xLength = _input('xLength', 3)  # глубина сглаживания
xPhase = _input('xPhase', 100)  # параметр сглаживания,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
ColorWidth = _input('ColorWidth', 40)  # ширина цветовой палитры (изменяется от 0 до 131)
period = Arr(100, 0, dyn=False)
dPriceShift = 0.0
min_rates_total = 0

class CIndicatorsBuffers(MqlObject):
    _q_fields = ('IndBuffer',)
    def __init__(self, *args):
        self.IndBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = GetStartBars(xMA_Method, xLength + (Step * 100), xPhase)
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
    Smooth1 = XMA[0].GetString_MA_Method(xMA_Method)
    StringConcatenate(shortname, 'XMA-X', 100, '(', Step, ',', xLength, ', ', Smooth1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    bar = 0
    limit = 0
    maxbar = 0
    price_ = 0.0
    maxbar = rates_total - 1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        for numb in range(0, 100):
            Ind[numb].IndBuffer[bar] = XMA[numb].XMASeries(maxbar, prev_calculated, rates_total, xMA_Method, xPhase, period[numb], price_, bar, True)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA = Arr(100, 0, dyn=False, factory=CXMA)
Ind = Arr(100, 0, dyn=False, factory=CIndicatorsBuffers)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XMAXN(_MQL5Indicator):
    name = 'XMA-XN'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Step': 10,  # шаг периода
        'xMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения
        'xLength': 3,  # глубина сглаживания
        'xPhase': 100,  # параметр сглаживания,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # cдвиг индикатора по вертикали в пунктах
        'ColorWidth': 40,  # ширина цветовой палитры (изменяется от 0 до 131)
    }

