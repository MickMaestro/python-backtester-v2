"""WeightOscillator — converted from MQL5: MQL5 Indicators/WeightOscillator/WeightOscillator.mq5

Осциллятор, представляющий взвешенную сглаженную сумму четырёх индикаторов - RSI, MFI, WPR и DeMarker.
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 11}, 'colors': {1: [16748574, 15658671, 8421504, 55295, 42495]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'WeightOscillator'}, 'levels': [0.0], 'description': ['Осциллятор, представляющий взвешенную сглаженную сумму четырёх индикаторов - RSI, MFI, WPR и DeMarker.'], 'name': 'WeightOscillator', 'source': 'MQL5 Indicators/WeightOscillator/WeightOscillator.mq5', 'folder': 'WeightOscillator', 'inputs': [{'mql': 'RSIWeight', 'py': 'RSIWeight', 'param': 'RSIWeight', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MFIWeight', 'py': 'MFIWeight', 'param': 'MFIWeight', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'MFIPeriod', 'py': 'MFIPeriod', 'param': 'MFIPeriod', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'MFIVolumeType', 'py': 'MFIVolumeType', 'param': 'MFIVolumeType', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'WPRWeight', 'py': 'WPRWeight', 'param': 'WPRWeight', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'WPRPeriod', 'py': 'WPRPeriod', 'param': 'WPRPeriod', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'DeMarkerWeight', 'py': 'DeMarkerWeight', 'param': 'DeMarkerWeight', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'DeMarkerPeriod', 'py': 'DeMarkerPeriod', 'param': 'DeMarkerPeriod', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'bMA_Method', 'py': 'bMA_Method', 'param': 'bMA_Method', 'type': 'int', 'default': 4, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'bLength', 'py': 'bLength', 'param': 'bLength', 'type': 'uint', 'default': 5, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'bPhase', 'py': 'bPhase', 'param': 'bPhase', 'type': 'int', 'default': 100, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'uint', 'default': 70, 'label': 'уровень перезакупа', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'uint', 'default': 30, 'label': 'уровень перепроданности', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
RSIWeight = _input('RSIWeight', 1.0)
RSIPeriod = _input('RSIPeriod', 14)
RSIPrice = _input('RSIPrice', PRICE_CLOSE)
MFIWeight = _input('MFIWeight', 1.0)
MFIPeriod = _input('MFIPeriod', 14)
MFIVolumeType = _input('MFIVolumeType', VOLUME_TICK)
WPRWeight = _input('WPRWeight', 1.0)
WPRPeriod = _input('WPRPeriod', 14)
DeMarkerWeight = _input('DeMarkerWeight', 1.0)
DeMarkerPeriod = _input('DeMarkerPeriod', 14)
bMA_Method = _input('bMA_Method', MODE_JJMA)  # метод усреднения
bLength = _input('bLength', 5)  # глубина сглаживания
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
    min_rates_total_1 = _int(MathMax(RSIPeriod, MathMax(MFIPeriod, MathMax(WPRPeriod, DeMarkerPeriod)))) + 1
    min_rates_total = min_rates_total_1 + GetStartBars(bMA_Method, bLength, bPhase)
    SumWeight = RSIWeight + MFIWeight + WPRWeight + DeMarkerWeight
    XMA1.XMALengthCheck('bLength', bLength)
    XMA1.XMAPhaseCheck('bPhase', bPhase, bMA_Method)
    RSI_Handle = iRSI(None, 0, RSIPeriod, RSIPrice)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI')
        return INIT_FAILED
    MFI_Handle = iMFI(None, 0, MFIPeriod, MFIVolumeType)
    if MFI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMFI')
        return INIT_FAILED
    WPR_Handle = iWPR(None, 0, WPRPeriod)
    if WPR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iWPR')
        return INIT_FAILED
    DeMarker_Handle = iDeMarker(None, 0, DeMarkerPeriod)
    if DeMarker_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iDeMarker')
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
    StringConcatenate(shortname, 'WeightOscillator(', bLength, ', ', Smooth1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrLimeGreen)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrRed)
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


class WeightOscillator(_MQL5Indicator):
    name = 'WeightOscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSIWeight': 1.0,
        'RSIPeriod': 14,
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'MFIWeight': 1.0,
        'MFIPeriod': 14,
        'MFIVolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),
        'WPRWeight': 1.0,
        'WPRPeriod': 14,
        'DeMarkerWeight': 1.0,
        'DeMarkerPeriod': 14,
        'bMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения
        'bLength': 5,  # глубина сглаживания
        'bPhase': 100,  # параметр сглаживания,
        'HighLevel': 70,  # уровень перезакупа
        'LowLevel': 30,  # уровень перепроданности
    }

