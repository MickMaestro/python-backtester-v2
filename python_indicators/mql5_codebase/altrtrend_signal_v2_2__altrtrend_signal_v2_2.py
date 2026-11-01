"""altrtrend_signal_v2_2 — converted from MQL5: MQL5 Indicators/AltrTrend_Signal_v2_2/altrtrend_signal_v2_2.mq5

Copyright: Copyright © 2005, OlegVS, GOODMAN; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, OlegVS, GOODMAN', 'link': '', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [36095], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'Sell', 2: 'Buy'}, 'levels': [], 'description': [], 'name': 'altrtrend_signal_v2_2', 'source': 'MQL5 Indicators/AltrTrend_Signal_v2_2/altrtrend_signal_v2_2.mq5', 'folder': 'AltrTrend_Signal_v2_2', 'inputs': [{'mql': 'K', 'py': 'K', 'param': 'K', 'type': 'uint', 'default': 30, 'label': '', 'sinput': False}, {'mql': 'Kstop', 'py': 'Kstop', 'param': 'Kstop', 'type': 'double', 'default': 0.5, 'label': '', 'sinput': False}, {'mql': 'Kperiod', 'py': 'Kperiod', 'param': 'Kperiod', 'type': 'uint', 'default': 150, 'label': '', 'sinput': False}, {'mql': 'PerADX', 'py': 'PerADX', 'param': 'PerADX', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
K = _input('K', 30)
Kstop = _input('Kstop', 0.5)
Kperiod = _input('Kperiod', 150)
PerADX = _input('PerADX', 14)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
ADX_Handle = 0

def OnInit():
    global ADX_Handle, min_rates_total
    min_rates_total = _int(PerADX) + 1
    ADX_Handle = iADX(None, PERIOD_CURRENT, PerADX)
    if ADX_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of the iADX indicator')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'AltrTrend_Signal_v2_2'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_old_trend
    if BarsCalculated(ADX_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    end = 0
    trend = 0
    ADX = Arr(0, 0.0)
    Res = 0.0
    Range = 0.0
    AvgRange = 0.0
    smin = 0.0
    smax = 0.0
    SsMax = 0.0
    SsMin = 0.0
    SSP = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        _s_OnCalculate_old_trend = 0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(ADX_Handle, 0, 0, to_copy, ADX) <= 0:
        return 0
    ArraySetAsSeries(ADX, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        SSP = MathCeil(_fdiv(Kperiod, ADX[bar + 1]))
        end = _int(MathMin(bar + SSP, rates_total))
        AvgRange = 0.0
        for iii in range(bar, end):
            AvgRange += MathAbs(high[iii] - low[iii])
        Range = _fdiv(AvgRange, SSP + 1)
        SsMax = high[bar]
        SsMin = low[bar]
        for kkk in range(bar, end):
            if SsMax < high[kkk]:
                SsMax = high[kkk]
            if SsMin >= low[kkk]:
                SsMin = low[kkk]
        Res = ((SsMax - SsMin) * K) / 100
        smin = SsMin + Res
        smax = SsMax - Res
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if close[bar] < smin:
            trend = -1
        if close[bar] > smax:
            trend = 1
        if not _s_OnCalculate_old_trend:
            _s_OnCalculate_old_trend = trend
        if trend != _s_OnCalculate_old_trend and close[bar] > smax:
            BuyBuffer[bar] = low[bar] - (Range * Kstop)
        if trend != _s_OnCalculate_old_trend and close[bar] < smin:
            SellBuffer[bar] = high[bar] + (Range * Kstop)
        if bar:
            _s_OnCalculate_old_trend = trend
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_old_trend = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AltrtrendSignalV22(_MQL5Indicator):
    name = 'altrtrend_signal_v2_2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'K': 30,
        'Kstop': 0.5,
        'Kperiod': 150,
        'PerADX': 14,
    }

