"""Fractal_WeightOscillator — converted from MQL5: MQL5 Indicators/Fractal_WeightOscillator/Fractal_WeightOscillator.mq5

Осциллятор, представляющий взвешенную сглаженную сумму четырёх индикаторов - Fractal_RSI, Fractal_MFI, Fractal_WPR и Fractal_DeMarker.
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1, 'indicator_maximum': 100.0, 'indicator_minimum': 0.0}, 'types': {1: 11}, 'colors': {1: [8421376, 15658671, 8421504, 15631086, 9639167]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Fractal_WeightOscillator'}, 'levels': [0.0], 'description': ['Осциллятор, представляющий взвешенную сглаженную сумму четырёх индикаторов - Fractal_RSI, Fractal_MFI, Fractal_WPR и Fractal_DeMarker.'], 'name': 'Fractal_WeightOscillator', 'source': 'MQL5 Indicators/Fractal_WeightOscillator/Fractal_WeightOscillator.mq5', 'folder': 'Fractal_WeightOscillator', 'inputs': [{'mql': 'e_period', 'py': 'e_period', 'param': 'e_period', 'type': 'uint', 'default': 30, 'label': 'глубина  усреднения Fractal_WeightOscillator', 'sinput': False}, {'mql': 'normal_speed', 'py': 'normal_speed', 'param': 'normal_speed', 'type': 'uint', 'default': 30, 'label': '', 'sinput': False}, {'mql': 'RSIWeight', 'py': 'RSIWeight', 'param': 'RSIWeight', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MFIWeight', 'py': 'MFIWeight', 'param': 'MFIWeight', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'MFIPrice', 'py': 'MFIPrice', 'param': 'MFIPrice', 'type': 'int', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'MFIVolumeType', 'py': 'MFIVolumeType', 'param': 'MFIVolumeType', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'WPRWeight', 'py': 'WPRWeight', 'param': 'WPRWeight', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'DeMarkerWeight', 'py': 'DeMarkerWeight', 'param': 'DeMarkerWeight', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'bMA_Method', 'py': 'bMA_Method', 'param': 'bMA_Method', 'type': 'int', 'default': 4, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'bLength', 'py': 'bLength', 'param': 'bLength', 'type': 'uint', 'default': 7, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'bPhase', 'py': 'bPhase', 'param': 'bPhase', 'type': 'int', 'default': 100, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'uint', 'default': 70, 'label': 'уровень перезакупа', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'uint', 'default': 30, 'label': 'уровень перепроданности', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum ENUM_APPLIED_PRICE_
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
_enum('ENUM_APPLIED_PRICE_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
e_period = _input('e_period', 30)  # глубина  усреднения Fractal_WeightOscillator
normal_speed = _input('normal_speed', 30)
RSIWeight = _input('RSIWeight', 1.0)
RSIPrice = _input('RSIPrice', PRICE_CLOSE_)
MFIWeight = _input('MFIWeight', 1.0)
MFIPrice = _input('MFIPrice', PRICE_TYPICAL_)
MFIVolumeType = _input('MFIVolumeType', VOLUME_TICK)
WPRWeight = _input('WPRWeight', 1.0)
DeMarkerWeight = _input('DeMarkerWeight', 1.0)
bMA_Method = _input('bMA_Method', MODE_JJMA)  # метод усреднения
bLength = _input('bLength', 7)  # глубина сглаживания
bPhase = _input('bPhase', 100)  # параметр сглаживания,
HighLevel = _input('HighLevel', 70)  # уровень перезакупа
LowLevel = _input('LowLevel', 30)  # уровень перепроданности
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_total_1 = 0
SumWeight = 0.0
RSI_Handle = 0
MFI_Handle = 0
WPR_Handle = 0
DeMarker_Handle = 0

def OnInit():
    global DeMarker_Handle, MFI_Handle, RSI_Handle, SumWeight, WPR_Handle, min_rates_total, min_rates_total_1
    if HighLevel < 50:
        Print(' Значение уровня перекупленности должно быть не меньше 50')
        return INIT_FAILED
    if LowLevel > 50:
        Print(' Значение уровня перепроданности должно быть не больше 50')
        return INIT_FAILED
    min_rates_total_1 = _int(MathMax(e_period, normal_speed)) + 3
    min_rates_total = min_rates_total_1 + GetStartBars(bMA_Method, bLength, bPhase)
    SumWeight = RSIWeight + MFIWeight + WPRWeight + DeMarkerWeight
    XMA1.XMALengthCheck('bLength', bLength)
    XMA1.XMAPhaseCheck('bPhase', bPhase, bMA_Method)
    RSI_Handle = iCustom(None, 0, '::Indicators\\Fractal_RSI', e_period, normal_speed, RSIPrice)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Fractal_RSI')
        return INIT_FAILED
    MFI_Handle = iCustom(None, 0, '::Indicators\\Fractal_MFI', e_period, normal_speed, MFIPrice, MFIVolumeType)
    if MFI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Fractal_MFI')
        return INIT_FAILED
    WPR_Handle = iCustom(None, 0, '::Indicators\\Fractal_WPR', e_period, normal_speed)
    if WPR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Fractal_WPR')
        return INIT_FAILED
    DeMarker_Handle = iCustom(None, 0, '::Indicators\\Fractal_DeMarker', e_period, normal_speed)
    if DeMarker_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Fractal_DeMarker')
        return INIT_FAILED
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnBuffer, True)
    SetIndexBuffer(2, ColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorBuffer, True)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(bMA_Method)
    StringConcatenate(shortname, 'Fractal_WeightOscillator(', bLength, ', ', Smooth1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrPurple)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (((BarsCalculated(RSI_Handle) < rates_total or BarsCalculated(MFI_Handle) < rates_total) or BarsCalculated(WPR_Handle) < rates_total) or BarsCalculated(DeMarker_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = 0
    RSI = Arr(0, 0.0)
    MFI = Arr(0, 0.0)
    WPR = Arr(0, 0.0)
    DeMarker = Arr(0, 0.0)
    WeightOscillator = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(RSI_Handle, 0, 0, to_copy, RSI) <= 0:
        return 0
    if CopyBuffer(MFI_Handle, 0, 0, to_copy, MFI) <= 0:
        return 0
    if CopyBuffer(WPR_Handle, 0, 0, to_copy, WPR) <= 0:
        return 0
    if CopyBuffer(DeMarker_Handle, 0, 0, to_copy, DeMarker) <= 0:
        return 0
    ArraySetAsSeries(RSI, True)
    ArraySetAsSeries(MFI, True)
    ArraySetAsSeries(WPR, True)
    ArraySetAsSeries(DeMarker, True)
    maxbar = rates_total - min_rates_total_1 - 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        WeightOscillator = _fdiv((RSIWeight * RSI[bar]) + (MFIWeight * MFI[bar]) + (WPRWeight * (WPR[bar] + 100)) + (DeMarkerWeight * 100 * DeMarker[bar]), SumWeight)
        UpBuffer[bar] = XMA1.XMASeries(maxbar, prev_calculated, rates_total, bMA_Method, bPhase, bLength, WeightOscillator, bar, True)
        DnBuffer[bar] = 50.0
        clr = _int(2.0)
        if UpBuffer[bar] > HighLevel:
            clr = _int(0.0)
        elif UpBuffer[bar] > 50:
            clr = _int(1.0)
        elif UpBuffer[bar] < LowLevel:
            clr = _int(4.0)
        elif UpBuffer[bar] < 50:
            clr = _int(3.0)
        ColorBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FractalWeightOscillator(_MQL5Indicator):
    name = 'Fractal_WeightOscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'e_period': 30,  # глубина  усреднения Fractal_WeightOscillator
        'normal_speed': 30,
        'RSIWeight': 1.0,
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),
        'MFIWeight': 1.0,
        'MFIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=6),
        'MFIVolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),
        'WPRWeight': 1.0,
        'DeMarkerWeight': 1.0,
        'bMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения
        'bLength': 7,  # глубина сглаживания
        'bPhase': 100,  # параметр сглаживания,
        'HighLevel': 70,  # уровень перезакупа
        'LowLevel': 30,  # уровень перепроданности
    }
    y_range = (0.0, 100.0)

