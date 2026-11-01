"""AlterTrend — converted from MQL5: MQL5 Indicators/AlterTrend/AlterTrend.mq5

Copyright: Copyright © 2005, OlegVS; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, OlegVS', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [65280, 32768, 2763429, 36095]}, 'widths': {}, 'styles': {}, 'labels': {1: 'AlterTrend_Open;AlterTrend_High;AlterTrend_Low;AlterTrend_Close'}, 'levels': [], 'description': [], 'name': 'AlterTrend', 'source': 'MQL5 Indicators/AlterTrend/AlterTrend.mq5', 'folder': 'AlterTrend', 'inputs': [{'mql': 'K', 'py': 'K', 'param': 'K', 'type': 'int', 'default': 30, 'label': '', 'sinput': False}, {'mql': 'Kperiod', 'py': 'Kperiod', 'param': 'Kperiod', 'type': 'uint', 'default': 150, 'label': '', 'sinput': False}, {'mql': 'PerADX', 'py': 'PerADX', 'param': 'PerADX', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
K = _input('K', 30)
Kperiod = _input('Kperiod', 150)
PerADX = _input('PerADX', 14)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
ADX_Handle = 0

def OnInit():
    global ADX_Handle, min_rates_total
    min_rates_total = 1 + _int(Kperiod + PerADX)
    ADX_Handle = iADX(None, 0, PerADX)
    if ADX_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ADX')
        return INIT_FAILED
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'AlterTrend'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ADX_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    ADX = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(ADX, True)
    if CopyBuffer(ADX_Handle, 0, 0, to_copy, ADX) <= 0:
        return 0
    for bar in range(limit, 0 - 1, -1):
        ExtCloseBuffer[bar] = 0.0
        ExtHighBuffer[bar] = ExtCloseBuffer[bar]
        ExtLowBuffer[bar] = ExtHighBuffer[bar]
        ExtOpenBuffer[bar] = ExtLowBuffer[bar]
        ExtColorBuffer[bar] = 4.0
        SSP = _int(MathCeil(_fdiv(Kperiod, ADX[bar])))
        AvgRange = 0.0
        for kkk in range(MathMin(bar + SSP, rates_total - 1), bar - 1, -1):
            AvgRange += MathAbs(high[kkk] - low[kkk])
        Range = _fdiv(AvgRange, SSP + 1)
        SsMax = high[bar]
        SsMin = low[bar]
        for iii in range(MathMin(bar + SSP - 1, rates_total - 1), bar, -1):
            price = high[iii]
            if SsMax < price:
                SsMax = price
            price = low[iii]
            if SsMin >= price:
                SsMin = price
        smin = SsMin + (((SsMax - SsMin) * K) / 100)
        smax = SsMax - (((SsMax - SsMin) * K) / 100)
        if close[bar] < smin:
            ExtOpenBuffer[bar] = open[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
            ExtCloseBuffer[bar] = close[bar]
            if close[bar] <= open[bar]:
                ExtColorBuffer[bar] = 3.0
            else:
                ExtColorBuffer[bar] = 2.0
        if close[bar] > smax:
            ExtOpenBuffer[bar] = open[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
            ExtCloseBuffer[bar] = close[bar]
            if close[bar] >= open[bar]:
                ExtColorBuffer[bar] = 0.0
            else:
                ExtColorBuffer[bar] = 1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AlterTrend(_MQL5Indicator):
    name = 'AlterTrend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'K': 30,
        'Kperiod': 150,
        'PerADX': 14,
    }

