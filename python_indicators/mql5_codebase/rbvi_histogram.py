"""RBVI_Histogram — converted from MQL5: MQL5 Indicators/RBVI_Histogram/RBVI_Histogram.mq5

Copyright: Copyright © 2004, BECEMAL; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2004, BECEMAL', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [55295, 16711680, 8421504]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'RBVI_Histogram'}, 'levels': [], 'description': [], 'name': 'RBVI_Histogram', 'source': 'MQL5 Indicators/RBVI_Histogram/RBVI_Histogram.mq5', 'folder': 'RBVI_Histogram', 'inputs': [{'mql': 'RBVIPeriod', 'py': 'RBVIPeriod', 'param': 'RBVIPeriod', 'type': 'int', 'default': 10, 'label': 'период индикатора', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'объём', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'uint', 'default': 60, 'label': 'уровень перезакупа', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'uint', 'default': 40, 'label': 'уровень перепроданности', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RBVIPeriod = _input('RBVIPeriod', 10)  # период индикатора
VolumeType = _input('VolumeType', VOLUME_TICK)  # объём
HighLevel = _input('HighLevel', 60)  # уровень перезакупа
LowLevel = _input('LowLevel', 40)  # уровень перепроданности
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    min_rates_total = 2 + RBVIPeriod
    ATR_Handle = iATR(None, 0, RBVIPeriod)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'RBVI_Histogram(', _str(RBVIPeriod), ',', EnumToString(VolumeType, 'ENUM_APPLIED_VOLUME'), ',', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 1)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrTeal)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrPurple)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_negative_, _s_OnCalculate_positive_, _s_OnCalculate_sumn_, _s_OnCalculate_sump_
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    Range = Arr(0, 0.0)
    vol0 = 0.0
    vol1 = 0.0
    sumn = 0.0
    sump = 0.0
    rel = 0.0
    positive = 0.0
    negative = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_sumn_ = 0.0
        _s_OnCalculate_sump_ = 0.0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, Range) <= 0:
        return 0
    ArraySetAsSeries(Range, True)
    if VolumeType == VOLUME_TICK:
        ArraySetAsSeries(tick_volume, True)
    else:
        ArraySetAsSeries(volume, True)
    positive = _s_OnCalculate_positive_
    negative = _s_OnCalculate_negative_
    sumn = _s_OnCalculate_sumn_
    sump = _s_OnCalculate_sump_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            _s_OnCalculate_positive_ = positive
            _s_OnCalculate_negative_ = negative
            _s_OnCalculate_sumn_ = sumn
            _s_OnCalculate_sump_ = sump
        if VolumeType == VOLUME_TICK:
            vol0 = float(tick_volume[bar])
            vol1 = float(tick_volume[bar + 1])
        else:
            vol0 = float(volume[bar])
            vol1 = float(volume[bar + 1])
        rel = (Range[bar] * vol0) - (Range[bar + 1] * vol1)
        if rel > 0:
            sump = rel
        else:
            sumn = -rel
        positive = ((positive * (RBVIPeriod - 1)) + sump) / RBVIPeriod
        negative = ((negative * (RBVIPeriod - 1)) + sumn) / RBVIPeriod
        if not negative:
            IndBuffer[bar] = 100.0
        else:
            IndBuffer[bar] = 100.0 * (1.0 - _fdiv(1.0, 1.0 + _fdiv(positive, negative)))
        clr = _int(1.0)
        if IndBuffer[bar] > HighLevel:
            clr = _int(0.0)
        elif IndBuffer[bar] < LowLevel:
            clr = _int(2.0)
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_positive_ = 0.0
_s_OnCalculate_negative_ = 0.0
_s_OnCalculate_sumn_ = 0.0
_s_OnCalculate_sump_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RBVIHistogram(_MQL5Indicator):
    name = 'RBVI_Histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RBVIPeriod': 10,  # период индикатора
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём
        'HighLevel': 60,  # уровень перезакупа
        'LowLevel': 40,  # уровень перепроданности
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

