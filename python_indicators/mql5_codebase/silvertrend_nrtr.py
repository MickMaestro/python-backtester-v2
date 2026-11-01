"""SilverTrend_NRTR — converted from MQL5: MQL5 Indicators/SilverTrend_NRTR/SilverTrend_NRTR.mq5

Copyright: SilverTrend  rewritten by CrazyChart; Link: http://viac.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'SilverTrend  rewritten by CrazyChart', 'link': 'http://viac.ru/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [7451452], 2: [9639167], 3: [65280], 4: [255]}, 'widths': {1: 1, 2: 1, 3: 4, 4: 4}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'SilverTrend NRTR Up', 2: 'SilverTrend NRTR Down', 3: 'SilverTrend Buy signal', 4: 'SilverTrend Sell signal'}, 'levels': [], 'description': [], 'name': 'SilverTrend_NRTR', 'source': 'MQL5 Indicators/SilverTrend_NRTR/SilverTrend_NRTR.mq5', 'folder': 'SilverTrend_NRTR', 'inputs': [{'mql': 'SSP', 'py': 'SSP', 'param': 'SSP', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'RISK', 'py': 'RISK', 'param': 'RISK', 'type': 'int', 'default': 3, 'label': 'степень риска', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SSP = _input('SSP', 9)
RISK = _input('RISK', 3)  # степень риска
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
TrendUp = Arr(0, 0.0)
TrendDown = Arr(0, 0.0)
SignUp = Arr(0, 0.0)
SignDown = Arr(0, 0.0)
K = 0
counter = 0
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = SSP + 1
    SetIndexBuffer(0, TrendUp, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(TrendUp, True)
    SetIndexBuffer(1, TrendDown, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(TrendDown, True)
    SetIndexBuffer(2, SignUp, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SignUp, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(2, PLOT_ARROW, 108)
    SetIndexBuffer(3, SignDown, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SignDown, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(3, PLOT_ARROW, 108)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'SilverTrend_NRTR'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global K, _s_OnCalculate_trend_prev
    if rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    trend = 0
    Range = 0.0
    AvgRange = 0.0
    smin = 0.0
    smax = 0.0
    SsMax = 0.0
    SsMin = 0.0
    price = 0.0
    newstop = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        K = 33 - RISK
        limit = rates_total - min_rates_total
        _s_OnCalculate_trend_prev = 0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    trend = _s_OnCalculate_trend_prev
    for bar in range(limit, 0 - 1, -1):
        trend = _s_OnCalculate_trend_prev
        Range = 0.0
        AvgRange = 0.0
        for iii in range(bar, bar + SSP + 1):
            AvgRange += MathAbs(high[iii] - low[iii])
        Range = AvgRange / (SSP + 1)
        SsMax = low[bar]
        SsMin = close[bar]
        for kkk in range(bar, bar + SSP - 1 + 1):
            price = high[kkk]
            if SsMax < price:
                SsMax = price
            price = low[kkk]
            if SsMin >= price:
                SsMin = price
        smin = SsMin + (((SsMax - SsMin) * K) / 100)
        smax = SsMax - (((SsMax - SsMin) * K) / 100)
        SignDown[bar] = 0.0
        SignUp[bar] = 0.0
        if close[bar] < smin:
            trend = -1
        if close[bar] > smax:
            trend = 1
        if _s_OnCalculate_trend_prev <= 0 and trend > 0:
            SignUp[bar] = low[bar] - (Range * 0.5)
        if _s_OnCalculate_trend_prev >= 0 and trend < 0:
            SignDown[bar] = high[bar] + (Range * 0.5)
        TrendUp[bar] = 0.0
        TrendDown[bar] = 0.0
        if trend > 0:
            newstop = low[bar] - (Range * 0.5)
            if _s_OnCalculate_trend_prev > 0:
                if newstop > TrendUp[bar + 1]:
                    TrendUp[bar] = newstop
                else:
                    TrendUp[bar] = TrendUp[bar + 1]
            else:
                TrendUp[bar] = newstop
        if trend < 0:
            newstop = high[bar] + (Range * 0.5)
            if _s_OnCalculate_trend_prev < 0:
                if newstop < TrendDown[bar + 1]:
                    TrendDown[bar] = newstop
                else:
                    TrendDown[bar] = TrendDown[bar + 1]
            else:
                TrendDown[bar] = newstop
        if bar:
            _s_OnCalculate_trend_prev = trend
    return rates_total

# ---- static local variables
_s_OnCalculate_trend_prev = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SilverTrendNRTR(_MQL5Indicator):
    name = 'SilverTrend_NRTR'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SSP': 9,
        'RISK': 3,  # степень риска
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

