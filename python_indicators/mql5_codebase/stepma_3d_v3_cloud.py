"""StepMA_3D_v3_Cloud — converted from MQL5: MQL5 Indicators/StepMA_3D_v3_Cloud/StepMA_3D_v3_Cloud.mq5

Copyright: Copyright © 2006, TrendLaboratory; Link: http://finance.groups.yahoo.com/group/TrendLaboratory; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, TrendLaboratory', 'link': 'http://finance.groups.yahoo.com/group/TrendLaboratory', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 8, 2: 7, 3: 1, 4: 1}, 'colors': {1: [3329330, 16711935], 2: [16436871, 13353215], 3: [16711680], 4: [255]}, 'widths': {1: 4, 3: 2, 4: 2}, 'styles': {1: 0, 3: 0, 4: 0}, 'labels': {1: 'Upper StepMA_3D_v3', 2: 'Upper StepMA_3D_v3 Cloud', 3: 'Middle StepMA_3D_v3', 4: 'Lower StepMA_3D_v3'}, 'levels': [], 'description': [], 'name': 'StepMA_3D_v3_Cloud', 'source': 'MQL5 Indicators/StepMA_3D_v3_Cloud/StepMA_3D_v3_Cloud.mq5', 'folder': 'StepMA_3D_v3_Cloud', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 10, 'label': 'Период ATR', 'sinput': False}, {'mql': 'Kv', 'py': 'Kv', 'param': 'Kv', 'type': 'double', 'default': 1.000001, 'label': 'Фактор чувствительности на изменения цены', 'sinput': False}, {'mql': 'MA_Mode', 'py': 'MA_Mode', 'param': 'MA_Mode', 'type': 'int', 'default': 0, 'label': 'Метод усреднения ATR', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_MA_MODE
MODE_SMA_ = 0
MODE_LWMA_ = 1
_enum('ENUM_MA_MODE', {0: 'MODE_SMA_', 1: 'MODE_LWMA_'})

# ---- inputs and global variables
Length = _input('Length', 10)  # Период ATR
Kv = _input('Kv', 1.000001)  # Фактор чувствительности на изменения цены
MA_Mode = _input('MA_Mode', MODE_SMA_)  # Метод усреднения ATR
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
UpBuffer = Arr(0, 0.0)
UpColorBuffer = Arr(0, 0.0)
MiddleBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
UpCldBuffer = Arr(0, 0.0)
DnCldBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(Length) + 1
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(1, UpColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(UpColorBuffer, True)
    SetIndexBuffer(2, UpCldBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpCldBuffer, True)
    SetIndexBuffer(3, DnCldBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnCldBuffer, True)
    SetIndexBuffer(4, MiddleBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(MiddleBuffer, True)
    SetIndexBuffer(5, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(DnBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'StepMA_3D_v3_Cloud(', Length, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_ATRmax, _s_OnCalculate_ATRmin, _s_OnCalculate_SmaxMax1, _s_OnCalculate_SmaxMid1, _s_OnCalculate_SmaxMin1, _s_OnCalculate_SminMax1, _s_OnCalculate_SminMid1, _s_OnCalculate_SminMin1, _s_OnCalculate_TrendMax1, _s_OnCalculate_TrendMid1, _s_OnCalculate_TrendMin1
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    TrendMin0 = 0
    TrendMax0 = 0
    TrendMid0 = 0
    StepSizeMin = 0.0
    StepSizeMax = 0.0
    StepSizeMid = 0.0
    AvgRange = 0.0
    Weight = 0.0
    SminMin0 = 0.0
    SmaxMin0 = 0.0
    SminMax0 = 0.0
    SmaxMax0 = 0.0
    SminMid0 = 0.0
    SmaxMid0 = 0.0
    alfa = 0.0
    ATR0 = 0.0
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        _s_OnCalculate_ATRmax = 0.0
        _s_OnCalculate_ATRmin = 999999999.0
        _s_OnCalculate_TrendMid1 = 0
        _s_OnCalculate_TrendMax1 = _s_OnCalculate_TrendMid1
        _s_OnCalculate_TrendMin1 = _s_OnCalculate_TrendMax1
        _s_OnCalculate_SmaxMid1 = close[limit + 1]
        _s_OnCalculate_SminMid1 = _s_OnCalculate_SmaxMid1
        _s_OnCalculate_SmaxMax1 = _s_OnCalculate_SminMid1
        _s_OnCalculate_SminMax1 = _s_OnCalculate_SmaxMax1
        _s_OnCalculate_SmaxMin1 = _s_OnCalculate_SminMax1
        _s_OnCalculate_SminMin1 = _s_OnCalculate_SmaxMin1
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        AvgRange = 0.0
        Weight = 0.0
        for iii in range(_int(Length) - 1, 0 - 1, -1):
            if MA_Mode == MODE_SMA_:
                alfa = 1.0
            else:
                alfa = (1.0 * (Length - iii)) / Length
            AvgRange += alfa * (high[bar + iii] - low[bar + iii])
            Weight += alfa
        ATR0 = _fdiv(AvgRange, Weight)
        if ATR0 > _s_OnCalculate_ATRmax:
            _s_OnCalculate_ATRmax = ATR0
        if ATR0 < _s_OnCalculate_ATRmin:
            _s_OnCalculate_ATRmin = ATR0
        StepSizeMin = MathRound(_fdiv(Kv * _s_OnCalculate_ATRmin, Point())) * Point()
        StepSizeMax = MathRound(_fdiv(Kv * _s_OnCalculate_ATRmax, Point())) * Point()
        StepSizeMid = MathRound(_fdiv(Kv * 0.5 * (_s_OnCalculate_ATRmax + _s_OnCalculate_ATRmin), Point())) * Point()
        SmaxMin0 = close[bar] + (2.0 * StepSizeMin)
        SminMin0 = close[bar] - (2.0 * StepSizeMin)
        SmaxMax0 = close[bar] + (2.0 * StepSizeMax)
        SminMax0 = close[bar] - (2.0 * StepSizeMax)
        SmaxMid0 = close[bar] + (2.0 * StepSizeMid)
        SminMid0 = close[bar] - (2.0 * StepSizeMid)
        TrendMin0 = _s_OnCalculate_TrendMin1
        TrendMax0 = _s_OnCalculate_TrendMax1
        TrendMid0 = _s_OnCalculate_TrendMid1
        if close[bar] > _s_OnCalculate_SmaxMin1:
            TrendMin0 = 1
        if close[bar] < _s_OnCalculate_SminMin1:
            TrendMin0 = -1
        if close[bar] > _s_OnCalculate_SmaxMax1:
            TrendMax0 = 1
        if close[bar] < _s_OnCalculate_SminMax1:
            TrendMax0 = -1
        if close[bar] > _s_OnCalculate_SmaxMid1:
            TrendMid0 = 1
        if close[bar] < _s_OnCalculate_SminMid1:
            TrendMid0 = -1
        if TrendMin0 > 0:
            if SminMin0 < _s_OnCalculate_SminMin1:
                SminMin0 = _s_OnCalculate_SminMin1
            UpBuffer[bar] = SminMin0 + StepSizeMin
        if TrendMin0 < 0:
            if SmaxMin0 > _s_OnCalculate_SmaxMin1:
                SmaxMin0 = _s_OnCalculate_SmaxMin1
            UpBuffer[bar] = SmaxMin0 - StepSizeMin
        if TrendMax0 > 0:
            if SminMax0 < _s_OnCalculate_SminMax1:
                SminMax0 = _s_OnCalculate_SminMax1
            DnCldBuffer[bar] = SminMax0 + StepSizeMax
            DnBuffer[bar] = DnCldBuffer[bar]
        if TrendMax0 < 0:
            if SmaxMax0 > _s_OnCalculate_SmaxMax1:
                SmaxMax0 = _s_OnCalculate_SmaxMax1
            DnCldBuffer[bar] = SmaxMax0 - StepSizeMax
            DnBuffer[bar] = DnCldBuffer[bar]
        if TrendMid0 > 0:
            if SminMid0 < _s_OnCalculate_SminMid1:
                SminMid0 = _s_OnCalculate_SminMid1
            UpCldBuffer[bar] = SminMid0 + StepSizeMid
            MiddleBuffer[bar] = UpCldBuffer[bar]
        if TrendMid0 < 0:
            if SmaxMid0 > _s_OnCalculate_SmaxMid1:
                SmaxMid0 = _s_OnCalculate_SmaxMid1
            UpCldBuffer[bar] = SmaxMid0 - StepSizeMid
            MiddleBuffer[bar] = UpCldBuffer[bar]
        if UpBuffer[bar] > DnBuffer[bar] and UpBuffer[bar] > MiddleBuffer[bar]:
            UpColorBuffer[bar] = 0.0
        elif UpBuffer[bar] < DnBuffer[bar] and UpBuffer[bar] < MiddleBuffer[bar]:
            UpColorBuffer[bar] = 1.0
        else:
            UpColorBuffer[bar] = UpColorBuffer[bar + 1]
        if bar:
            _s_OnCalculate_SmaxMin1 = SmaxMin0
            _s_OnCalculate_SminMin1 = SminMin0
            _s_OnCalculate_SmaxMax1 = SmaxMax0
            _s_OnCalculate_SminMax1 = SminMax0
            _s_OnCalculate_SmaxMid1 = SmaxMid0
            _s_OnCalculate_SminMid1 = SminMid0
            _s_OnCalculate_TrendMin1 = TrendMin0
            _s_OnCalculate_TrendMax1 = TrendMax0
            _s_OnCalculate_TrendMid1 = TrendMid0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_SminMin1 = 0.0
_s_OnCalculate_SmaxMin1 = 0.0
_s_OnCalculate_SminMax1 = 0.0
_s_OnCalculate_SmaxMax1 = 0.0
_s_OnCalculate_SminMid1 = 0.0
_s_OnCalculate_SmaxMid1 = 0.0
_s_OnCalculate_ATRmax = 0.0
_s_OnCalculate_ATRmin = 0.0
_s_OnCalculate_TrendMin1 = 0
_s_OnCalculate_TrendMax1 = 0
_s_OnCalculate_TrendMid1 = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StepMA3DV3Cloud(_MQL5Indicator):
    name = 'StepMA_3D_v3_Cloud'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 10,  # Период ATR
        'Kv': 1.000001,  # Фактор чувствительности на изменения цены
        'MA_Mode': _Choice({0: 'SMA', 1: 'LWMA'}, default=0),  # Метод усреднения ATR
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

