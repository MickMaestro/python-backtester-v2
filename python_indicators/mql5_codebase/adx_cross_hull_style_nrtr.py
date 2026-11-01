"""ADX_Cross_Hull_Style_NRTR — converted from MQL5: MQL5 Indicators/ADX_Cross_Hull_Style_NRTR/ADX_Cross_Hull_Style_NRTR.mq5

Copyright: Copyright © 2005, .; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, .', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [65280], 2: [255], 3: [8421376], 4: [16711935]}, 'widths': {1: 1, 2: 1, 3: 2, 4: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'NRTR Up', 2: 'NRTR Down', 3: 'Buy NRTR signal', 4: 'Sell NRTR signal'}, 'levels': [], 'description': [''], 'name': 'ADX_Cross_Hull_Style_NRTR', 'source': 'MQL5 Indicators/ADX_Cross_Hull_Style_NRTR/ADX_Cross_Hull_Style_NRTR.mq5', 'folder': 'ADX_Cross_Hull_Style_NRTR', 'inputs': [{'mql': 'ADXPeriod', 'py': 'ADXPeriod', 'param': 'ADXPeriod', 'type': 'uint', 'default': 14, 'label': 'период индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ADXPeriod = _input('ADXPeriod', 14)  # период индикатора
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
TrendUp = Arr(0, 0.0)
TrendDown = Arr(0, 0.0)
SignUp = Arr(0, 0.0)
SignDown = Arr(0, 0.0)
ADX1_Handle = 0
ADX2_Handle = 0
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ADX1_Handle, ADX2_Handle, ATR_Handle, min_rates_total
    AtrPeriod = 10
    min_rates_total = _int(MathMax(ADXPeriod + 1, AtrPeriod))
    ADX1_Handle = iADX(None, 0, ADXPeriod)
    if ADX1_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ADX1')
    ADX2_Handle = iADX(None, 0, _int(MathFloor(ADXPeriod / 2.0)))
    if ADX2_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ADX2')
    ATR_Handle = iATR(None, 0, AtrPeriod)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
    SetIndexBuffer(0, TrendUp, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(TrendUp, True)
    SetIndexBuffer(1, TrendDown, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(TrendDown, True)
    SetIndexBuffer(2, SignUp, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SignUp, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(2, PLOT_ARROW, 171)
    SetIndexBuffer(3, SignDown, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SignDown, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(3, PLOT_ARROW, 171)
    shortname = Box("")
    StringConcatenate(shortname, 'ADX_Cross_Hull_Style_NRTR(', ADXPeriod, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_trend_prev
    if ((BarsCalculated(ADX1_Handle) < rates_total or BarsCalculated(ADX2_Handle) < rates_total) or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    trend = 0
    pADX1 = Arr(0, 0.0)
    pADX2 = Arr(0, 0.0)
    mADX1 = Arr(0, 0.0)
    mADX2 = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    b4plusdi = 0.0
    nowplusdi = 0.0
    b4minusdi = 0.0
    nowminusdi = 0.0
    newstop = 0.0
    ArraySetAsSeries(pADX1, True)
    ArraySetAsSeries(pADX2, True)
    ArraySetAsSeries(mADX1, True)
    ArraySetAsSeries(mADX2, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
        _s_OnCalculate_trend_prev = 0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(ADX1_Handle, PLUSDI_LINE, 0, to_copy, pADX1) <= 0:
        return 0
    if CopyBuffer(ADX2_Handle, PLUSDI_LINE, 0, to_copy, pADX2) <= 0:
        return 0
    if CopyBuffer(ADX1_Handle, MINUSDI_LINE, 0, to_copy, mADX1) <= 0:
        return 0
    if CopyBuffer(ADX2_Handle, MINUSDI_LINE, 0, to_copy, mADX2) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy - 1, ATR) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        TrendUp[bar] = 0.0
        TrendDown[bar] = 0.0
        SignUp[bar] = 0.0
        SignDown[bar] = 0.0
        trend = _s_OnCalculate_trend_prev
        b4plusdi = (pADX2[bar + 1] * 2) - pADX1[bar + 1]
        nowplusdi = (pADX2[bar] * 2) - pADX1[bar]
        b4minusdi = (mADX2[bar + 1] * 2) - mADX1[bar + 1]
        nowminusdi = (mADX2[bar] * 2) - mADX1[bar]
        if b4plusdi < b4minusdi and nowplusdi > nowminusdi:
            trend = 1
        if b4plusdi > b4minusdi and nowplusdi < nowminusdi:
            trend = -1
        if trend > 0:
            newstop = low[bar] - (0.25 * ATR[bar])
            if _s_OnCalculate_trend_prev > 0:
                if newstop > TrendUp[bar + 1]:
                    TrendUp[bar] = newstop
                else:
                    TrendUp[bar] = TrendUp[bar + 1]
            else:
                TrendUp[bar] = newstop
                SignUp[bar] = TrendUp[bar]
        if trend < 0:
            newstop = high[bar] + (0.25 * ATR[bar])
            if _s_OnCalculate_trend_prev < 0:
                if newstop < TrendDown[bar + 1]:
                    TrendDown[bar] = newstop
                else:
                    TrendDown[bar] = TrendDown[bar + 1]
            else:
                TrendDown[bar] = newstop
                SignDown[bar] = TrendDown[bar]
        if bar:
            _s_OnCalculate_trend_prev = trend
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_trend_prev = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ADXCrossHullStyleNRTR(_MQL5Indicator):
    name = 'ADX_Cross_Hull_Style_NRTR'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ADXPeriod': 14,  # период индикатора
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

