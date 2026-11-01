"""stepma_stoch_kv1 — converted from MQL5: MQL5 Indicators/StepMA_Stoch_KV1_HTF/stepma_stoch_kv1.mq5

Copyright: Copyright © 2005, TrendLaboratory Ltd.; Link: E-mail: igorad2004@list.ru; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, TrendLaboratory Ltd.', 'link': 'E-mail: igorad2004@list.ru', 'version': '1.02', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16711935, 8721863, 14524637, 8421504, 16436871, 8421376, 16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'StepMA_Stoch_KV1'}, 'levels': [], 'description': [], 'name': 'stepma_stoch_kv1', 'source': 'MQL5 Indicators/StepMA_Stoch_KV1_HTF/stepma_stoch_kv1.mq5', 'folder': 'StepMA_Stoch_KV1_HTF', 'inputs': [{'mql': 'PeriodWATR', 'py': 'PeriodWATR', 'param': 'PeriodWATR', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'Kwatr', 'py': 'Kwatr', 'param': 'Kwatr', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'HighLow', 'py': 'HighLow', 'param': 'HighLow', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PeriodWATR = _input('PeriodWATR', 10)
Kwatr = _input('Kwatr', 1.0)
HighLow = _input('HighLow', False)
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(PeriodWATR + 1)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'StepMA_Stoch_KV1')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_SmaxMax1, _s_OnCalculate_SmaxMid1, _s_OnCalculate_SmaxMin1, _s_OnCalculate_SminMax1, _s_OnCalculate_SminMid1, _s_OnCalculate_SminMin1, _s_OnCalculate_TrendMax1, _s_OnCalculate_TrendMid1, _s_OnCalculate_TrendMin1, _s_OnCalculate_WATRmax, _s_OnCalculate_WATRmax_, _s_OnCalculate_WATRmin, _s_OnCalculate_WATRmin_
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    TrendMin = 0
    TrendMax = 0
    TrendMid = 0
    SminMin0 = 0.0
    SmaxMin0 = 0.0
    SumRange = 0.0
    dK = 0.0
    WATR0 = 0.0
    SminMax0 = 0.0
    SmaxMax0 = 0.0
    SminMid0 = 0.0
    SmaxMid0 = 0.0
    linemin = 0.0
    linemax = 0.0
    linemid = 0.0
    Stoch1 = 0.0
    Stoch2 = 0.0
    bsmin = 0.0
    bsmax = 0.0
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        bar = limit
        SumRange = 0.0
        for iii in range(0, _int(PeriodWATR)):
            dK = 1 + ((1.0 * (PeriodWATR - iii)) / PeriodWATR)
            kkk = bar + iii
            SumRange += dK * MathAbs(high[kkk] - low[kkk])
        WATR0 = SumRange / PeriodWATR
        _s_OnCalculate_WATRmax_ = WATR0
        _s_OnCalculate_WATRmin_ = WATR0
        StepSizeMin = _int(MathRound(_fdiv(Kwatr * _s_OnCalculate_WATRmin, Point())))
        StepSizeMax = _int(MathRound(_fdiv(Kwatr * _s_OnCalculate_WATRmax, Point())))
        StepSizeMid = _int(MathRound(_fdiv(Kwatr * 0.5 * (_s_OnCalculate_WATRmax + _s_OnCalculate_WATRmin), Point())))
        if HighLow:
            _s_OnCalculate_SmaxMin1 = low[bar] + (2 * StepSizeMin * Point())
            _s_OnCalculate_SminMin1 = high[bar] - (2 * StepSizeMin * Point())
            _s_OnCalculate_SmaxMax1 = low[bar] + (2 * StepSizeMax * Point())
            _s_OnCalculate_SminMax1 = high[bar] - (2 * StepSizeMax * Point())
            _s_OnCalculate_SmaxMid1 = low[bar] + (2 * StepSizeMid * Point())
            _s_OnCalculate_SminMid1 = high[bar] - (2 * StepSizeMid * Point())
        if not HighLow:
            _s_OnCalculate_SmaxMin1 = close[bar] + (2 * StepSizeMin * Point())
            _s_OnCalculate_SminMin1 = close[bar] - (2 * StepSizeMin * Point())
            _s_OnCalculate_SmaxMax1 = close[bar] + (2 * StepSizeMax * Point())
            _s_OnCalculate_SminMax1 = close[bar] - (2 * StepSizeMax * Point())
            _s_OnCalculate_SmaxMid1 = close[bar] + (2 * StepSizeMid * Point())
            _s_OnCalculate_SminMid1 = close[bar] - (2 * StepSizeMid * Point())
        _s_OnCalculate_TrendMin1 = 0
        _s_OnCalculate_TrendMax1 = 0
        _s_OnCalculate_TrendMid1 = 0
    else:
        limit = rates_total - prev_calculated
    TrendMin = _s_OnCalculate_TrendMin1
    TrendMax = _s_OnCalculate_TrendMax1
    TrendMid = _s_OnCalculate_TrendMid1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        SumRange = 0.0
        for iii in range(0, _int(PeriodWATR)):
            dK = 1 + ((1.0 * (PeriodWATR - iii)) / PeriodWATR)
            kkk = bar + iii
            SumRange += dK * MathAbs(high[kkk] - low[kkk])
        WATR0 = SumRange / PeriodWATR
        _s_OnCalculate_WATRmax = MathMax(WATR0, _s_OnCalculate_WATRmax_)
        _s_OnCalculate_WATRmin = MathMin(WATR0, _s_OnCalculate_WATRmin_)
        StepSizeMin = _int(MathRound(_fdiv(Kwatr * _s_OnCalculate_WATRmin, Point())))
        StepSizeMax = _int(MathRound(_fdiv(Kwatr * _s_OnCalculate_WATRmax, Point())))
        StepSizeMid = _int(MathRound(_fdiv(Kwatr * 0.5 * (_s_OnCalculate_WATRmax + _s_OnCalculate_WATRmin), Point())))
        if HighLow:
            SmaxMin0 = low[bar] + (2 * StepSizeMin * Point())
            SminMin0 = high[bar] - (2 * StepSizeMin * Point())
            SmaxMax0 = low[bar] + (2 * StepSizeMax * Point())
            SminMax0 = high[bar] - (2 * StepSizeMax * Point())
            SmaxMid0 = low[bar] + (2 * StepSizeMid * Point())
            SminMid0 = high[bar] - (2 * StepSizeMid * Point())
            if close[bar] > _s_OnCalculate_SmaxMin1:
                TrendMin = 1
            if close[bar] < _s_OnCalculate_SminMin1:
                TrendMin = -1
            if close[bar] > _s_OnCalculate_SmaxMax1:
                TrendMax = 1
            if close[bar] < _s_OnCalculate_SminMax1:
                TrendMax = -1
            if close[bar] > _s_OnCalculate_SmaxMid1:
                TrendMid = 1
            if close[bar] < _s_OnCalculate_SminMid1:
                TrendMid = -1
        if not HighLow:
            SmaxMin0 = close[bar] + (2 * StepSizeMin * Point())
            SminMin0 = close[bar] - (2 * StepSizeMin * Point())
            SmaxMax0 = close[bar] + (2 * StepSizeMax * Point())
            SminMax0 = close[bar] - (2 * StepSizeMax * Point())
            SmaxMid0 = close[bar] + (2 * StepSizeMid * Point())
            SminMid0 = close[bar] - (2 * StepSizeMid * Point())
            if close[bar] > _s_OnCalculate_SmaxMin1:
                TrendMin = 1
            if close[bar] < _s_OnCalculate_SminMin1:
                TrendMin = -1
            if close[bar] > _s_OnCalculate_SmaxMax1:
                TrendMax = 1
            if close[bar] < _s_OnCalculate_SminMax1:
                TrendMax = -1
            if close[bar] > _s_OnCalculate_SmaxMid1:
                TrendMid = 1
            if close[bar] < _s_OnCalculate_SminMid1:
                TrendMid = -1
        if TrendMin > 0 and SminMin0 < _s_OnCalculate_SminMin1:
            SminMin0 = _s_OnCalculate_SminMin1
        if TrendMin < 0 and SmaxMin0 > _s_OnCalculate_SmaxMin1:
            SmaxMin0 = _s_OnCalculate_SmaxMin1
        if TrendMax > 0 and SminMax0 < _s_OnCalculate_SminMax1:
            SminMax0 = _s_OnCalculate_SminMax1
        if TrendMax < 0 and SmaxMax0 > _s_OnCalculate_SmaxMax1:
            SmaxMax0 = _s_OnCalculate_SmaxMax1
        if TrendMid > 0 and SminMid0 < _s_OnCalculate_SminMid1:
            SminMid0 = _s_OnCalculate_SminMid1
        if TrendMid < 0 and SmaxMid0 > _s_OnCalculate_SmaxMid1:
            SmaxMid0 = _s_OnCalculate_SmaxMid1
        if TrendMin > 0:
            linemin = SminMin0 + (StepSizeMin * Point())
        if TrendMin < 0:
            linemin = SmaxMin0 - (StepSizeMin * Point())
        if TrendMax > 0:
            linemax = SminMax0 + (StepSizeMax * Point())
        if TrendMax < 0:
            linemax = SmaxMax0 - (StepSizeMax * Point())
        if TrendMid > 0:
            linemid = SminMid0 + (StepSizeMid * Point())
        if TrendMid < 0:
            linemid = SmaxMid0 - (StepSizeMid * Point())
        bsmin = linemax - (StepSizeMax * Point())
        bsmax = linemin + (StepSizeMax * Point())
        res = bsmax - bsmin
        if not res:
            res = 1e-08
        Stoch1 = NormalizeDouble(_fdiv(linemin - bsmin, res), 6)
        Stoch2 = NormalizeDouble(_fdiv(linemid - bsmin, res), 6)
        IndBuffer[bar] = Stoch1 - Stoch2
        if bar:
            _s_OnCalculate_SminMin1 = SminMin0
            _s_OnCalculate_SmaxMin1 = SmaxMin0
            _s_OnCalculate_SminMax1 = SminMax0
            _s_OnCalculate_SmaxMax1 = SmaxMax0
            _s_OnCalculate_SminMid1 = SminMid0
            _s_OnCalculate_SmaxMid1 = SmaxMid0
            _s_OnCalculate_WATRmax_ = _s_OnCalculate_WATRmax
            _s_OnCalculate_WATRmin_ = _s_OnCalculate_WATRmin
            _s_OnCalculate_TrendMin1 = TrendMin
            _s_OnCalculate_TrendMax1 = TrendMax
            _s_OnCalculate_TrendMid1 = TrendMid
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        clr = 3
        if IndBuffer[bar] > 0:
            if IndBuffer[bar] > IndBuffer[bar + 1]:
                clr = 6
            if IndBuffer[bar] == IndBuffer[bar + 1]:
                clr = 5
            if IndBuffer[bar] < IndBuffer[bar + 1]:
                clr = 4
        if IndBuffer[bar] < 0:
            if IndBuffer[bar] < IndBuffer[bar + 1]:
                clr = 0
            if IndBuffer[bar] == IndBuffer[bar + 1]:
                clr = 1
            if IndBuffer[bar] > IndBuffer[bar + 1]:
                clr = 2
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_SminMin1 = 0.0
_s_OnCalculate_SmaxMin1 = 0.0
_s_OnCalculate_WATRmax = 0.0
_s_OnCalculate_WATRmin = 0.0
_s_OnCalculate_SminMax1 = 0.0
_s_OnCalculate_SmaxMax1 = 0.0
_s_OnCalculate_SminMid1 = 0.0
_s_OnCalculate_SmaxMid1 = 0.0
_s_OnCalculate_WATRmax_ = 0.0
_s_OnCalculate_WATRmin_ = 0.0
_s_OnCalculate_TrendMin1 = 0
_s_OnCalculate_TrendMax1 = 0
_s_OnCalculate_TrendMid1 = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StepmaStochKv1(_MQL5Indicator):
    name = 'stepma_stoch_kv1'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PeriodWATR': 10,
        'Kwatr': 1.0,
        'HighLow': False,
    }

