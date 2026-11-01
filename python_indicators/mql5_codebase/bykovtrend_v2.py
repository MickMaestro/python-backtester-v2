"""BykovTrend_V2 — converted from MQL5: MQL5 Indicators/BykovTrend_V2/BykovTrend_V2.mq5

Copyright: Ramdass - Conversion only; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Ramdass - Conversion only', 'link': '', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [3329330, 8421376, 8421504, 1993170, 55295]}, 'widths': {}, 'styles': {}, 'labels': {1: 'BykovTrendOpen;BykovTrendHigh;BykovTrendLow;BykovTrendClose'}, 'levels': [], 'description': [], 'name': 'BykovTrend_V2', 'source': 'MQL5 Indicators/BykovTrend_V2/BykovTrend_V2.mq5', 'folder': 'BykovTrend_V2', 'inputs': [{'mql': 'RISK', 'py': 'RISK', 'param': 'RISK', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'SSP', 'py': 'SSP', 'param': 'SSP', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RISK = _input('RISK', 3)
SSP = _input('SSP', 9)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorsBuffer = Arr(0, 0.0)
K = 0
WPR_Handle = 0
min_rates_total = 0

def OnInit():
    global K, WPR_Handle, min_rates_total
    K = 33 - RISK
    min_rates_total = SSP + 1
    WPR_Handle = iWPR(None, 0, SSP)
    if WPR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iWPR')
        return INIT_FAILED
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorsBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorsBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'BykovTrend_V2'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_oldtrend
    if BarsCalculated(WPR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    trend = 0
    WPR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        _s_OnCalculate_oldtrend = 0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(WPR_Handle, 0, 0, to_copy, WPR) <= 0:
        return 0
    ArraySetAsSeries(WPR, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtOpenBuffer[bar] = open[bar]
        ExtHighBuffer[bar] = high[bar]
        ExtLowBuffer[bar] = low[bar]
        ExtCloseBuffer[bar] = close[bar]
        ExtColorsBuffer[bar] = 2.0
        trend = _s_OnCalculate_oldtrend
        if WPR[bar] < (-100 + K):
            trend = -1
        if WPR[bar] > (-K):
            trend = 1
        if trend > 0:
            if open[bar] <= close[bar]:
                ExtColorsBuffer[bar] = 0.0
            else:
                ExtColorsBuffer[bar] = 1.0
        if trend < 0:
            if open[bar] >= close[bar]:
                ExtColorsBuffer[bar] = 4.0
            else:
                ExtColorsBuffer[bar] = 3.0
        if bar:
            _s_OnCalculate_oldtrend = trend
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_oldtrend = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BykovTrendV2(_MQL5Indicator):
    name = 'BykovTrend_V2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RISK': 3,
        'SSP': 9,
    }

