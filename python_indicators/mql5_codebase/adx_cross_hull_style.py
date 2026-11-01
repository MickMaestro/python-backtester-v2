"""adx_cross_hull_style — converted from MQL5: MQL5 Indicators/ADX Cross Hull Style/adx_cross_hull_style.mq5

METRO
Copyright: Copyright © 2005, .; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, .', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [11186720], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Lower ADX_Cross_Hull_Style', 2: 'Upper ADX_Cross_Hull_Style'}, 'levels': [], 'description': ['METRO'], 'name': 'adx_cross_hull_style', 'source': 'MQL5 Indicators/ADX Cross Hull Style/adx_cross_hull_style.mq5', 'folder': 'ADX Cross Hull Style', 'inputs': [{'mql': 'ADXPeriod', 'py': 'ADXPeriod', 'param': 'ADXPeriod', 'type': 'uint', 'default': 14, 'label': 'indicator period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ADXPeriod = _input('ADXPeriod', 14)  # indicator period
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
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
        Print(' Failed to get handle of the ADX1 indicator')
    ADX2_Handle = iADX(None, 0, _int(MathFloor(ADXPeriod / 2.0)))
    if ADX2_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ADX2 indicator')
    ATR_Handle = iATR(None, 0, AtrPeriod)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(DnBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'ADX_Cross_Hull_Style(', ADXPeriod, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((BarsCalculated(ADX1_Handle) < rates_total or BarsCalculated(ADX2_Handle) < rates_total) or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    pADX1 = Arr(0, 0.0)
    pADX2 = Arr(0, 0.0)
    mADX1 = Arr(0, 0.0)
    mADX2 = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    b4plusdi = 0.0
    nowplusdi = 0.0
    b4minusdi = 0.0
    nowminusdi = 0.0
    ArraySetAsSeries(pADX1, True)
    ArraySetAsSeries(pADX2, True)
    ArraySetAsSeries(mADX1, True)
    ArraySetAsSeries(mADX2, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
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
        UpBuffer[bar] = 0.0
        DnBuffer[bar] = 0.0
        b4plusdi = (pADX2[bar + 1] * 2) - pADX1[bar + 1]
        nowplusdi = (pADX2[bar] * 2) - pADX1[bar]
        b4minusdi = (mADX2[bar + 1] * 2) - mADX1[bar + 1]
        nowminusdi = (mADX2[bar] * 2) - mADX1[bar]
        if b4plusdi < b4minusdi and nowplusdi > nowminusdi:
            UpBuffer[bar] = low[bar] - (0.25 * ATR[bar])
        if b4plusdi > b4minusdi and nowplusdi < nowminusdi:
            DnBuffer[bar] = high[bar] + (0.25 * ATR[bar])
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AdxCrossHullStyle(_MQL5Indicator):
    name = 'adx_cross_hull_style'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ADXPeriod': 14,  # indicator period
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

