"""silvertrend_crazychart — converted from MQL5: MQL5 Indicators/SilverTrend_CrazyChart/silvertrend_crazychart.mq5

Copyright: Copyright © 2006, CrazyChart; Link: http://viac.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, CrazyChart', 'link': 'http://viac.ru/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16748574, 14053594]}, 'widths': {}, 'styles': {}, 'labels': {1: 'SilverTrend_CrazyChart'}, 'levels': [], 'description': [], 'name': 'silvertrend_crazychart', 'source': 'MQL5 Indicators/SilverTrend_CrazyChart/silvertrend_crazychart.mq5', 'folder': 'SilverTrend_CrazyChart', 'inputs': [{'mql': 'SSP', 'py': 'SSP', 'param': 'SSP', 'type': 'uint', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'Kmin', 'py': 'Kmin', 'param': 'Kmin', 'type': 'double', 'default': 1.6, 'label': '', 'sinput': False}, {'mql': 'Kmax', 'py': 'Kmax', 'param': 'Kmax', 'type': 'double', 'default': 50.6, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SSP = _input('SSP', 7)
Kmin = _input('Kmin', 1.6)
Kmax = _input('Kmax', 50.6)
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(2 * SSP)
    SetIndexBuffer(0, ExtABuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtABuffer, True)
    SetIndexBuffer(1, ExtBBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtBBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SilverTrend_CrazyChart')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    SsMax = 0.0
    SsMin = 0.0
    smin = 0.0
    smax = 0.0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        bar = rates_total - 1
        for bar in range(bar, limit - 1, -1):
            ExtBBuffer[bar] = 0.0
            ExtABuffer[bar] = 0.0
        else:
            bar = _range_end(bar, limit - 1, -1)
    else:
        limit = rates_total - prev_calculated + _int(SSP)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        SsMax = high[ArrayMaximum(high, bar, SSP)]
        SsMin = low[ArrayMinimum(low, bar, SSP)]
        smin = NormalizeDouble(SsMin - (((SsMax - SsMin) * Kmin) / 100), Digits())
        smax = NormalizeDouble(SsMax - (((SsMax - SsMin) * Kmax) / 100), Digits())
        barx = bar - _int(SSP) - 1
        if barx >= 0:
            ExtBBuffer[barx] = smax
        ExtABuffer[bar] = smax
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SilvertrendCrazychart(_MQL5Indicator):
    name = 'silvertrend_crazychart'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SSP': 7,
        'Kmin': 1.6,
        'Kmax': 50.6,
    }

