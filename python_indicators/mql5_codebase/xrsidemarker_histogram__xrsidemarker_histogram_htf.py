"""XRSIDeMarker_Histogram — converted from MQL5: MQL5 Indicators/XRSIDeMarker_Histogram_HTF/XRSIDeMarker_Histogram.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 11}, 'colors': {1: [65280, 7451452, 25600, 8388736, 255, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'XRSIDeMarker'}, 'levels': [], 'description': [], 'name': 'XRSIDeMarker_Histogram', 'source': 'MQL5 Indicators/XRSIDeMarker_Histogram_HTF/XRSIDeMarker_Histogram.mq5', 'folder': 'XRSIDeMarker_Histogram_HTF', 'inputs': [{'mql': 'IndPeriod', 'py': 'IndPeriod', 'param': 'IndPeriod', 'type': 'uint', 'default': 14, 'label': 'период индикатора', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': 'цена', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'uint', 'default': 60, 'label': 'уровень перезакупа', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'uint', 'default': 40, 'label': 'уровень перепроданности', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 5, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
IndPeriod = _input('IndPeriod', 14)  # период индикатора
RSIPrice = _input('RSIPrice', PRICE_CLOSE)  # цена
HighLevel = _input('HighLevel', 60)  # уровень перезакупа
LowLevel = _input('LowLevel', 40)  # уровень перепроданности
XMA_Method = _input('XMA_Method', MODE_SMA_)  # метод усреднения
XLength = _input('XLength', 5)  # глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр сглаживания,
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
min_rates_total = 0
min_rates_1 = 0
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
DeMarker_Handle = 0
RSI_Handle = 0

def OnInit():
    global DeMarker_Handle, RSI_Handle, min_rates_1, min_rates_total
    min_rates_1 = _int(IndPeriod)
    min_rates_total = min_rates_1 + GetStartBars(XMA_Method, XLength, XPhase)
    RSI_Handle = iRSI(None, 0, IndPeriod, RSIPrice)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI')
        return INIT_FAILED
    DeMarker_Handle = iDeMarker(None, 0, IndPeriod)
    if DeMarker_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iDeMarker')
        return INIT_FAILED
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnBuffer, True)
    SetIndexBuffer(2, ColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'XRSIDeMarker_Histogram(' + _str(IndPeriod) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if (BarsCalculated(RSI_Handle) < rates_total or BarsCalculated(DeMarker_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = 0
    RSI = Arr(0, 0.0)
    DeMarker = Arr(0, 0.0)
    rsidemarker = 0.0
    maxbar = rates_total - min_rates_1 - 1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(RSI_Handle, 0, 0, to_copy, RSI) <= 0:
        return 0
    if CopyBuffer(DeMarker_Handle, 0, 0, to_copy, DeMarker) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        rsidemarker = (RSI[bar] + (100 * DeMarker[bar])) / 2
        UpBuffer[bar] = XMA1.XMASeries(maxbar, prev_calculated, rates_total, XMA_Method, XPhase, XLength, rsidemarker, bar, True)
        DnBuffer[bar] = 50.0
        clr = _int(3.0)
        if UpBuffer[bar] > HighLevel:
            if UpBuffer[bar + 1] <= UpBuffer[bar]:
                clr = _int(0.0)
            else:
                clr = _int(1.0)
        elif UpBuffer[bar] < LowLevel:
            if UpBuffer[bar + 1] >= UpBuffer[bar]:
                clr = _int(5.0)
            else:
                clr = _int(4.0)
        if UpBuffer[bar] <= HighLevel and UpBuffer[bar] >= LowLevel:
            if UpBuffer[bar + 1] <= UpBuffer[bar]:
                clr = _int(2.0)
            else:
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


class XRSIDeMarkerHistogram(_MQL5Indicator):
    name = 'XRSIDeMarker_Histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'IndPeriod': 14,  # период индикатора
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # цена
        'HighLevel': 60,  # уровень перезакупа
        'LowLevel': 40,  # уровень перепроданности
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения
        'XLength': 5,  # глубина сглаживания
        'XPhase': 15,  # параметр сглаживания,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

