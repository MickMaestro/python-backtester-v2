"""Trend_Risk_Indicator — converted from MQL5: MQL5 Indicators/Trend_Risk_Indicator/Trend_Risk_Indicator.mq5

Trend Risk indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 17, 4: 5}, 'colors': {1: [10526303], 2: [10526303], 3: [32768, 255, 3329434, 17919, 11119017], 4: [4294967295]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Top', 2: 'Bottom', 3: 'Open;High;Low;Close', 4: 'Signal'}, 'levels': [], 'description': ['Trend Risk indicator'], 'name': 'Trend_Risk_Indicator', 'source': 'MQL5 Indicators/Trend_Risk_Indicator/Trend_Risk_Indicator.mq5', 'folder': 'Trend_Risk_Indicator', 'inputs': [{'mql': 'InpPeriodBands', 'py': 'InpPeriodBands', 'param': 'InpPeriodBands', 'type': 'uint', 'default': 28, 'label': 'Bands range', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 3.5, 'label': 'Deviation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodBands = _input('InpPeriodBands', 28)  # Bands range
InpDeviation = _input('InpDeviation', 3.5)  # Deviation
BufferTop = Arr(0, 0.0)
BufferBottom = Arr(0, 0.0)
BufferCandleOpen = Arr(0, 0.0)
BufferCandleHigh = Arr(0, 0.0)
BufferCandleLow = Arr(0, 0.0)
BufferCandleClose = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferSmoothPrice = Arr(0, 0.0)
BufferSmoothRange = Arr(0, 0.0)
BufferNoTrade = Arr(0, 0.0)
period_bands = 0
deviation = 0.0

def OnInit():
    global deviation, period_bands
    period_bands = (1 if (InpPeriodBands < 1) else InpPeriodBands)
    deviation = InpDeviation
    SetIndexBuffer(0, BufferTop, INDICATOR_DATA)
    SetIndexBuffer(1, BufferBottom, INDICATOR_DATA)
    SetIndexBuffer(2, BufferCandleOpen, INDICATOR_DATA)
    SetIndexBuffer(3, BufferCandleHigh, INDICATOR_DATA)
    SetIndexBuffer(4, BufferCandleLow, INDICATOR_DATA)
    SetIndexBuffer(5, BufferCandleClose, INDICATOR_DATA)
    SetIndexBuffer(6, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, BufferNoTrade, INDICATOR_DATA)
    SetIndexBuffer(8, BufferSmoothPrice, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferSmoothRange, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend Risk Indicator (' + _str(period_bands) + ',' + DoubleToString(deviation, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(BufferTop, True)
    ArraySetAsSeries(BufferBottom, True)
    ArraySetAsSeries(BufferCandleOpen, True)
    ArraySetAsSeries(BufferCandleHigh, True)
    ArraySetAsSeries(BufferCandleLow, True)
    ArraySetAsSeries(BufferCandleClose, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferNoTrade, True)
    ArraySetAsSeries(BufferSmoothPrice, True)
    ArraySetAsSeries(BufferSmoothRange, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferTop, EMPTY_VALUE)
        ArrayInitialize(BufferBottom, EMPTY_VALUE)
        ArrayInitialize(BufferCandleOpen, EMPTY_VALUE)
        ArrayInitialize(BufferCandleHigh, EMPTY_VALUE)
        ArrayInitialize(BufferCandleLow, EMPTY_VALUE)
        ArrayInitialize(BufferCandleClose, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 4)
        ArrayInitialize(BufferNoTrade, EMPTY_VALUE)
        ArrayInitialize(BufferSmoothPrice, 0)
        ArrayInitialize(BufferSmoothRange, 0)
    for i in range(limit, 0 - 1, -1):
        if i == (rates_total - 1):
            BufferSmoothPrice[i] = close[i]
            BufferSmoothRange[i] = high[i] - low[i]
        else:
            BufferSmoothPrice[i] = _fdiv((BufferSmoothPrice[i + 1] * (period_bands - 1)) + close[i], period_bands)
            BufferSmoothRange[i] = _fdiv((BufferSmoothRange[i + 1] * (period_bands - 1)) + high[i] - low[i], period_bands)
        BufferTop[i] = BufferSmoothPrice[i] + (BufferSmoothRange[i] * deviation)
        BufferBottom[i] = BufferSmoothPrice[i] - (BufferSmoothRange[i] * deviation)
        BufferCandleOpen[i] = open[i]
        BufferCandleHigh[i] = high[i]
        BufferCandleLow[i] = low[i]
        BufferCandleClose[i] = close[i]
        BufferNoTrade[i] = EMPTY_VALUE
        BufferColors[i] = (0 if (BufferCandleClose[i] > BufferCandleOpen[i]) else 1 if (BufferCandleClose[i] < BufferCandleOpen[i]) else 4)
        if close[i] > BufferTop[i]:
            BufferColors[i] = 4.0
            BufferNoTrade[i] = BufferTop[i]
            PlotIndexSetString(3, PLOT_LABEL, 'Do not trade')
        elif close[i] < BufferBottom[i]:
            BufferColors[i] = 4.0
            BufferNoTrade[i] = BufferBottom[i]
            PlotIndexSetString(3, PLOT_LABEL, 'Do not trade')
        else:
            PlotIndexSetString(3, PLOT_LABEL, 'Trade allowed')
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendRiskIndicator(_MQL5Indicator):
    name = 'Trend_Risk_Indicator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodBands': 28,  # Bands range
        'InpDeviation': 3.5,  # Deviation
    }

