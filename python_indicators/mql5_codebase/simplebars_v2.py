"""simplebars_v2 — converted from MQL5: MQL5 Indicators/SimpleBars_V2/simplebars_v2.mq5

SimpleBars
Copyright: Copyright © 2012, Ivan Kornilov; Link: excelf@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Ivan Kornilov', 'link': 'excelf@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [5737262, 65535, 16711680, 65535, 255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Upper;lower'}, 'levels': [], 'description': ['SimpleBars'], 'name': 'simplebars_v2', 'source': 'MQL5 Indicators/SimpleBars_V2/simplebars_v2.mq5', 'folder': 'SimpleBars_V2', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'useclose', 'py': 'useclose', 'param': 'useclose', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period = _input('period', 6)
useclose = _input('useclose', True)
ExtopenBuffer = Arr(0, 0.0)
ExthighBuffer = Arr(0, 0.0)
ExtlowBuffer = Arr(0, 0.0)
ExtcloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = period + 1
    SetIndexBuffer(0, ExtopenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExthighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtlowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtcloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'SimpleBars'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_trend
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    trend = 0
    buyPrice = 0.0
    sellPrice = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
        _s_OnCalculate_prev_trend = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if useclose:
            buyPrice = close[bar]
            sellPrice = close[bar]
        else:
            buyPrice = low[bar]
            sellPrice = high[bar]
        if _s_OnCalculate_prev_trend == 0:
            if close[bar] > open[bar]:
                trend = 1
            else:
                trend = -1
        else:
            if _s_OnCalculate_prev_trend == 1:
                if buyPrice > low[bar - 1]:
                    trend = 1
                else:
                    for j in range(2, period + 1):
                        if buyPrice > low[bar - j]:
                            trend = 1
                            break
                        else:
                            trend = -1
            if _s_OnCalculate_prev_trend == -1:
                if sellPrice < high[bar - 1]:
                    trend = -1
                else:
                    for j in range(2, period + 1):
                        if sellPrice < high[bar - j]:
                            trend = -1
                            break
                        else:
                            trend = 1
        clr = 2
        if trend == -1:
            if open[bar] > close[bar]:
                clr = 4
            elif open[bar] < close[bar]:
                clr = 3
        if trend == 1:
            if open[bar] < close[bar]:
                clr = 0
            elif open[bar] > close[bar]:
                clr = 1
        ExtColorBuffer[bar] = clr
        ExtopenBuffer[bar] = open[bar]
        ExtcloseBuffer[bar] = close[bar]
        ExthighBuffer[bar] = high[bar]
        ExtlowBuffer[bar] = low[bar]
        if bar < (rates_total - 1):
            _s_OnCalculate_prev_trend = trend
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_prev_trend = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SimplebarsV2(_MQL5Indicator):
    name = 'simplebars_v2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 6,
        'useclose': True,
    }

