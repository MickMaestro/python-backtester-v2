"""fx5_selfadjustingcci — converted from MQL5: MQL5 Indicators/FX5_SelfAdjustingCCI/fx5_selfadjustingcci.mq5

Copyright: Copyright © 2008, FX5; Link: hazem@uk2.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, FX5', 'link': 'hazem@uk2.net', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16711680], 2: [32768], 3: [255]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'CCI', 2: 'OverBought', 3: 'OverSold'}, 'levels': [100.0, 0.0, -100.0], 'description': [''], 'name': 'fx5_selfadjustingcci', 'source': 'MQL5 Indicators/FX5_SelfAdjustingCCI/fx5_selfadjustingcci.mq5', 'folder': 'FX5_SelfAdjustingCCI', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 12, 'label': 'Период CCI', 'sinput': False}, {'mql': 'CCIPrice', 'py': 'CCIPrice', 'param': 'CCIPrice', 'type': 'int', 'default': 5, 'label': 'Цена CCI индикатора', 'sinput': False}, {'mql': 'BandsDeviation', 'py': 'BandsDeviation', 'param': 'BandsDeviation', 'type': 'double', 'default': 2.0, 'label': 'Девиация', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'bool', 'default': True, 'label': 'Использовать сглаживание для Боллинджера', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 12)  # Период CCI
CCIPrice = _input('CCIPrice', PRICE_MEDIAN)  # Цена CCI индикатора
BandsDeviation = _input('BandsDeviation', 2.0)  # Девиация
MA_Method = _input('MA_Method', True)  # Использовать сглаживание для Боллинджера
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtLineBuffer = Arr(0, 0.0)
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtCalcBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_ = 0
CCI_Handle = 0
STD_Handle = 0

def OnInit():
    global CCI_Handle, STD_Handle, min_rates_, min_rates_total
    min_rates_ = _int(Length)
    min_rates_total = _int(min_rates_ + (2 * Length))
    CCI_Handle = iCCI(None, PERIOD_CURRENT, Length, CCIPrice)
    if CCI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iCCI')
    if not MA_Method:
        STD_Handle = iStdDev(None, PERIOD_CURRENT, Length, 0, MODE_SMA, CCI_Handle)
        if STD_Handle == INVALID_HANDLE:
            Print(' Не удалось получить хендл индикатора iStdDev')
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer, True)
    SetIndexBuffer(1, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLineBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer1, True)
    ArraySetAsSeries(ExtLineBuffer2, True)
    SetIndexBuffer(3, ExtCalcBuffer, INDICATOR_CALCULATIONS)
    shortname = Box("")
    StringConcatenate(shortname, 'FX5_SelfAdjustingCCI(', Length, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(CCI_Handle) < rates_total or ((not MA_Method) and BarsCalculated(STD_Handle) < rates_total)) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    STD = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_ - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(CCI_Handle, 0, 0, to_copy, ExtLineBuffer) <= 0:
        return 0
    if not MA_Method:
        if CopyBuffer(STD_Handle, 0, 0, to_copy, STD) <= 0:
            return 0
    ArraySetAsSeries(STD, True)
    if MA_Method == True:
        bar = limit
        for bar in range(bar, 0 - 1, -1):
            smoothedCCI = GetSmoothedCCI(bar)
            ExtCalcBuffer[bar] = MathAbs(ExtLineBuffer[bar] - smoothedCCI)
            kDiviation = BandsDeviation * GetAbsDiviationAverage(bar)
            ExtLineBuffer1[bar] = 50 + kDiviation
            ExtLineBuffer2[bar] = 50 - kDiviation
        else:
            bar = _range_end(bar, 0 - 1, -1)
    else:
        bar = limit
        for bar in range(bar, 0 - 1, -1):
            kDiviation = BandsDeviation * STD[bar]
            ExtLineBuffer1[bar] = 50 + kDiviation
            ExtLineBuffer2[bar] = 50 - kDiviation
        else:
            bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def GetSmoothedCCI(shift):
    sum_ = 0.0
    for iii in range(_int(shift + Length - 1), shift - 1, -1):
        sum_ += ExtLineBuffer[iii]
    return sum_ / Length

def GetAbsDiviationAverage(shift):
    sum_ = 0.0
    for iii in range(_int(shift + Length - 1), shift - 1, -1):
        sum_ += ExtCalcBuffer[iii]
    return sum_ / Length


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Fx5Selfadjustingcci(_MQL5Indicator):
    name = 'fx5_selfadjustingcci'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 12,  # Период CCI
        'CCIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Цена CCI индикатора
        'BandsDeviation': 2.0,  # Девиация
        'MA_Method': True,  # Использовать сглаживание для Боллинджера
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

