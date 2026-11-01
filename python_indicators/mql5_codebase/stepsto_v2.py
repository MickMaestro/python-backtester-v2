"""StepSto_v2 — converted from MQL5: MQL5 Indicators/StepSto_v2/StepSto_v2.mq5

Copyright: Copyright © 2005, TrendLaboratory Ltd.; Link: http://finance.groups.yahoo.com/group/TrendLaboratory; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, TrendLaboratory Ltd.', 'link': 'http://finance.groups.yahoo.com/group/TrendLaboratory', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 10, 2: 1}, 'colors': {1: [65280, 32768, 8421504, 128, 255], 2: [15624315]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'StepSto Fast', 2: 'StepSto Slow'}, 'levels': [], 'description': [], 'name': 'StepSto_v2', 'source': 'MQL5 Indicators/StepSto_v2/StepSto_v2.mq5', 'folder': 'StepSto_v2', 'inputs': [{'mql': 'Kfast', 'py': 'Kfast', 'param': 'Kfast', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'Kslow', 'py': 'Kslow', 'param': 'Kslow', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Kfast = _input('Kfast', 1.0)
Kslow = _input('Kslow', 1.0)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
FastBuffer = Arr(0, 0.0)
ColorFastBuffer = Arr(0, 0.0)
SlowBuffer = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0
PeriodATR = 0

def OnInit():
    global ATR_Handle, PeriodATR, min_rates_total
    PeriodATR = 10
    min_rates_total = MathMax(2, PeriodATR)
    ATR_Handle = iATR(None, PERIOD_CURRENT, PeriodATR)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iATR')
    SetIndexBuffer(0, FastBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(FastBuffer, True)
    SetIndexBuffer(1, ColorFastBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorFastBuffer, True)
    SetIndexBuffer(2, SlowBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SlowBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'StepSto(', Kfast, ',', Kslow, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_ATRmax1, _s_OnCalculate_ATRmin1, _s_OnCalculate_SmaxMax1, _s_OnCalculate_SmaxMid1, _s_OnCalculate_SmaxMin1, _s_OnCalculate_SminMax1, _s_OnCalculate_SminMid1, _s_OnCalculate_SminMin1, _s_OnCalculate_TrendMax1, _s_OnCalculate_TrendMid1, _s_OnCalculate_TrendMin1
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    TrendMin0 = 0
    TrendMax0 = 0
    TrendMid0 = 0
    clr = 0
    ATR = Arr(0, 0.0)
    linemin = 0.0
    linemax = 0.0
    linemid = 0.0
    Sto1 = 0.0
    Sto2 = 0.0
    bsmin = 0.0
    bsmax = 0.0
    StepSizeMin = 0.0
    StepSizeMax = 0.0
    SminMid0 = 0.0
    SmaxMid0 = 0.0
    SminMin0 = 0.0
    SmaxMin0 = 0.0
    SminMax0 = 0.0
    SmaxMax0 = 0.0
    ATRmax0 = 0.0
    ATRmin0 = 0.0
    StepSizeMid = 0.0
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(ATR, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_ATRmax1 = 0.0
        _s_OnCalculate_ATRmin1 = 999999999.9
        _s_OnCalculate_SminMin1 = close[limit]
        _s_OnCalculate_SmaxMin1 = close[limit]
        _s_OnCalculate_SminMax1 = close[limit]
        _s_OnCalculate_SmaxMax1 = close[limit]
        _s_OnCalculate_SminMid1 = close[limit]
        _s_OnCalculate_SmaxMid1 = close[limit]
        _s_OnCalculate_TrendMax1 = 1
        _s_OnCalculate_TrendMin1 = -1
        _s_OnCalculate_TrendMid1 = 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    TrendMax0 = _s_OnCalculate_TrendMax1
    TrendMin0 = _s_OnCalculate_TrendMin1
    TrendMid0 = _s_OnCalculate_TrendMid1
    for bar in range(limit, 0 - 1, -1):
        ATRmax0 = MathMax(ATR[bar], _s_OnCalculate_ATRmax1)
        ATRmin0 = MathMin(ATR[bar], _s_OnCalculate_ATRmin1)
        StepSizeMin = Kfast * ATRmin0
        StepSizeMax = Kfast * ATRmax0
        StepSizeMid = Kfast * 0.5 * Kslow * (ATRmax0 + ATRmin0)
        SmaxMin0 = close[bar] + (2 * StepSizeMin)
        SminMin0 = close[bar] - (2 * StepSizeMin)
        SmaxMax0 = close[bar] + (2 * StepSizeMax)
        SminMax0 = close[bar] - (2 * StepSizeMax)
        SmaxMid0 = close[bar] + (2 * StepSizeMid)
        SminMid0 = close[bar] - (2 * StepSizeMid)
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
        if TrendMin0 > 0 and SminMin0 < _s_OnCalculate_SminMin1:
            SminMin0 = _s_OnCalculate_SminMin1
        if TrendMin0 < 0 and SmaxMin0 > _s_OnCalculate_SmaxMin1:
            SmaxMin0 = _s_OnCalculate_SmaxMin1
        if TrendMax0 > 0 and SminMax0 < _s_OnCalculate_SminMax1:
            SminMax0 = _s_OnCalculate_SminMax1
        if TrendMax0 < 0 and SmaxMax0 > _s_OnCalculate_SmaxMax1:
            SmaxMax0 = _s_OnCalculate_SmaxMax1
        if TrendMid0 > 0 and SminMid0 < _s_OnCalculate_SminMid1:
            SminMid0 = _s_OnCalculate_SminMid1
        if TrendMid0 < 0 and SmaxMid0 > _s_OnCalculate_SmaxMid1:
            SmaxMid0 = _s_OnCalculate_SmaxMid1
        if TrendMin0 > 0:
            linemin = SminMin0 + StepSizeMin
        if TrendMin0 < 0:
            linemin = SmaxMin0 - StepSizeMin
        if TrendMax0 > 0:
            linemax = SminMax0 + StepSizeMax
        if TrendMax0 < 0:
            linemax = SmaxMax0 - StepSizeMax
        if TrendMid0 > 0:
            linemid = SminMid0 + StepSizeMid
        if TrendMid0 < 0:
            linemid = SmaxMid0 - StepSizeMid
        bsmin = linemax - StepSizeMax
        bsmax = linemax + StepSizeMax
        Sto1 = _fdiv(100 * (linemin - bsmin), bsmax - bsmin)
        Sto2 = _fdiv(100 * (linemid - bsmin), bsmax - bsmin)
        Sto1 -= 50
        Sto2 -= 50
        FastBuffer[bar] = Sto1
        SlowBuffer[bar] = Sto2
        clr = 2
        if Sto1 > 0:
            if Sto1 >= Sto2:
                clr = 0
            else:
                clr = 1
        else:
            if Sto1 <= Sto2:
                clr = 4
            else:
                clr = 3
        ColorFastBuffer[bar] = clr
        if bar:
            _s_OnCalculate_ATRmax1 = ATRmax0
            _s_OnCalculate_ATRmin1 = ATRmin0
            _s_OnCalculate_SminMin1 = SminMin0
            _s_OnCalculate_SmaxMin1 = SmaxMin0
            _s_OnCalculate_SminMax1 = SminMax0
            _s_OnCalculate_SmaxMax1 = SmaxMax0
            _s_OnCalculate_SminMid1 = SminMid0
            _s_OnCalculate_SmaxMid1 = SmaxMid0
            _s_OnCalculate_TrendMax1 = TrendMax0
            _s_OnCalculate_TrendMin1 = TrendMin0
            _s_OnCalculate_TrendMid1 = TrendMid0
    return rates_total

# ---- static local variables
_s_OnCalculate_SminMin1 = 0.0
_s_OnCalculate_SmaxMin1 = 0.0
_s_OnCalculate_SminMax1 = 0.0
_s_OnCalculate_SmaxMax1 = 0.0
_s_OnCalculate_SminMid1 = 0.0
_s_OnCalculate_SmaxMid1 = 0.0
_s_OnCalculate_ATRmax1 = 0.0
_s_OnCalculate_ATRmin1 = 0.0
_s_OnCalculate_TrendMin1 = 0
_s_OnCalculate_TrendMax1 = 0
_s_OnCalculate_TrendMid1 = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StepStoV2(_MQL5Indicator):
    name = 'StepSto_v2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Kfast': 1.0,
        'Kslow': 1.0,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

