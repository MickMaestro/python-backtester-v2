"""flat-trend — converted from MQL5: MQL5 Indicators/Flat-Trend_HTF/flat-trend.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 14822282, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Flat-Trend'}, 'levels': [], 'description': [], 'name': 'flat-trend', 'source': 'MQL5 Indicators/Flat-Trend_HTF/flat-trend.mq5', 'folder': 'Flat-Trend_HTF', 'inputs': [{'mql': 'StDevPeriod', 'py': 'StDevPeriod', 'param': 'StDevPeriod', 'type': 'uint', 'default': 20, 'label': 'Период StDev', 'sinput': False}, {'mql': 'StDev_Method', 'py': 'StDev_Method', 'param': 'StDev_Method', 'type': 'int', 'default': 3, 'label': 'Метод усреднения StDev', 'sinput': False}, {'mql': 'StDevLength', 'py': 'StDevLength', 'param': 'StDevLength', 'type': 'uint', 'default': 5, 'label': 'Глубина сглаживания StDev', 'sinput': False}, {'mql': 'StDevPhase', 'py': 'StDevPhase', 'param': 'StDevPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания StDev', 'sinput': False}, {'mql': 'ATRPeriod', 'py': 'ATRPeriod', 'param': 'ATRPeriod', 'type': 'uint', 'default': 20, 'label': 'Период StDev', 'sinput': False}, {'mql': 'ATR_Method', 'py': 'ATR_Method', 'param': 'ATR_Method', 'type': 'int', 'default': 3, 'label': 'Метод усреднения ATR', 'sinput': False}, {'mql': 'ATRLength', 'py': 'ATRLength', 'param': 'ATRLength', 'type': 'uint', 'default': 5, 'label': 'Глубина сглаживания ATR', 'sinput': False}, {'mql': 'ATRPhase', 'py': 'ATRPhase', 'param': 'ATRPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания ATR', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
StDevPeriod = _input('StDevPeriod', 20)  # Период StDev
StDev_Method = _input('StDev_Method', MODE_LWMA)  # Метод усреднения StDev
StDevLength = _input('StDevLength', 5)  # Глубина сглаживания StDev
StDevPhase = _input('StDevPhase', 15)  # Параметр сглаживания StDev
ATRPeriod = _input('ATRPeriod', 20)  # Период StDev
ATR_Method = _input('ATR_Method', MODE_LWMA)  # Метод усреднения ATR
ATRLength = _input('ATRLength', 5)  # Глубина сглаживания ATR
ATRPhase = _input('ATRPhase', 15)  # Параметр сглаживания ATR
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
ATR_Handle = 0
StDev_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, StDev_Handle, min_rates_total
    min_rate_1 = _int(StDevPeriod) + XMA1.GetStartBars(StDev_Method, StDevLength, StDevPhase)
    min_rate_2 = _int(ATRPeriod) + XMA2.GetStartBars(ATR_Method, ATRLength, ATRPhase)
    min_rates_total = MathMax(min_rate_1, min_rate_2) + 1
    XMA1.XMALengthCheck('StDevLength', StDevLength)
    XMA2.XMALengthCheck('ATRLength', ATRLength)
    XMA1.XMAPhaseCheck('StDevPhase', StDevPhase, StDev_Method)
    XMA2.XMAPhaseCheck('ATRPhase', ATRPhase, ATR_Method)
    ATR_Handle = iATR(None, PERIOD_CURRENT, ATRPeriod)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
    StDev_Handle = iStdDev(None, PERIOD_CURRENT, ATRPeriod, 0, MODE_SMA, PRICE_CLOSE)
    if StDev_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора StdDev')
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Flat-Trend')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_xatr, _s_OnCalculate_prev_xstdev
    if (BarsCalculated(ATR_Handle) < rates_total or BarsCalculated(StDev_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    StDev = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    xatr = 0.0
    xstdev = 0.0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar1 = 0
    maxbar2 = 0
    res = 0
    ArraySetAsSeries(StDev, True)
    ArraySetAsSeries(ATR, True)
    maxbar1 = _int(rates_total - ATRPeriod - 1)
    maxbar2 = _int(rates_total - StDevPeriod - 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
        _s_OnCalculate_prev_xatr = 0.0
        _s_OnCalculate_prev_xstdev = 0.0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    if CopyBuffer(StDev_Handle, 0, 0, to_copy, StDev) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        xatr = XMA1.XMASeries(maxbar1, prev_calculated, rates_total, ATR_Method, ATRPhase, ATRLength, ATR[bar], bar, True)
        xstdev = XMA2.XMASeries(maxbar2, prev_calculated, rates_total, StDev_Method, StDevPhase, StDevLength, StDev[bar], bar, True)
        res = 0
        if _s_OnCalculate_prev_xatr > xatr and _s_OnCalculate_prev_xstdev > xstdev:
            res = 1
        if _s_OnCalculate_prev_xatr < xatr and _s_OnCalculate_prev_xstdev < xstdev:
            res = 2
        IndBuffer[bar] = res + 1
        ColorIndBuffer[bar] = res
        if bar:
            _s_OnCalculate_prev_xatr = xatr
            _s_OnCalculate_prev_xstdev = xstdev
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()

# ---- static local variables
_s_OnCalculate_prev_xatr = 0.0
_s_OnCalculate_prev_xstdev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FlatTrend(_MQL5Indicator):
    name = 'flat-trend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'StDevPeriod': 20,  # Период StDev
        'StDev_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # Метод усреднения StDev
        'StDevLength': 5,  # Глубина сглаживания StDev
        'StDevPhase': 15,  # Параметр сглаживания StDev
        'ATRPeriod': 20,  # Период StDev
        'ATR_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # Метод усреднения ATR
        'ATRLength': 5,  # Глубина сглаживания ATR
        'ATRPhase': 15,  # Параметр сглаживания ATR
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

