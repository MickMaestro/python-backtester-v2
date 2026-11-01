"""Sets_the_chart_scale — converted from MQL5: MQL5 Indicators/Sets Chart Scale/Sets_the_chart_scale.mq5

Copyright: Alexey Viktorov; Link: https://www.mql5.com/ru/users/alexeyvik/news; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Alexey Viktorov', 'link': 'https://www.mql5.com/ru/users/alexeyvik/news', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Sets_the_chart_scale', 'source': 'MQL5 Indicators/Sets Chart Scale/Sets_the_chart_scale.mq5', 'folder': 'Sets Chart Scale', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
half = 0.0
chartScale = 0

def OnInit():
    global chartScale, half
    chartScale = _int(ChartGetInteger(0, CHART_SCALE))
    half = NormalizeDouble(ChartGetDouble(0, CHART_PRICE_MAX) - ((ChartGetDouble(0, CHART_PRICE_MAX) + ChartGetDouble(0, CHART_PRICE_MIN)) / 2), Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    chartMax = ChartGetDouble(0, CHART_PRICE_MAX)
    chartMin = ChartGetDouble(0, CHART_PRICE_MIN)
    chartMid = NormalizeDouble((chartMax + chartMin) / 2, Digits())
    firstVisibleBar = _int(ChartGetInteger(0, CHART_FIRST_VISIBLE_BAR))
    visibleBars = _int(ChartGetInteger(0, CHART_VISIBLE_BARS))
    ratesBar = rates_total - firstVisibleBar - 3 + visibleBars
    ChartSetInteger(0, CHART_SCALEFIX, True)
    ChartSetDouble(0, CHART_FIXED_MAX, ((open[ratesBar] + close[ratesBar]) / 2) + half)
    ChartSetDouble(0, CHART_FIXED_MIN, ((open[ratesBar] + close[ratesBar]) / 2) - half)
    return rates_total

def OnDeinit(reason):
    ChartSetInteger(0, CHART_SCALEFIX, False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SetsTheChartScale(_MQL5Indicator):
    name = 'Sets_the_chart_scale'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

