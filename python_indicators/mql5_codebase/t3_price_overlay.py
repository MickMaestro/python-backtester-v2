"""T3_Price_Overlay — converted from MQL5: MQL5 Indicators/T3_Price_Overlay/T3_Price_Overlay.mq5

Tim Tillson's T3 MA Price Overlay indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 19, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 17}, 'colors': {1: [12632256], 2: [12632256], 3: [2263842, 11193702, 255, 8894686, 11119017]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'T3 High', 2: 'T3 Low', 3: 'Candle'}, 'levels': [], 'description': ["Tim Tillson's T3 MA Price Overlay indicator"], 'name': 'T3_Price_Overlay', 'source': 'MQL5 Indicators/T3_Price_Overlay/T3_Price_Overlay.mq5', 'folder': 'T3_Price_Overlay', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'T3 period', 'sinput': False}, {'mql': 'InpVolumeFactor', 'py': 'InpVolumeFactor', 'param': 'InpVolumeFactor', 'type': 'double', 'default': 0.7, 'label': 'T3 volume factor', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # T3 period
InpVolumeFactor = _input('InpVolumeFactor', 0.7)  # T3 volume factor
BufferT3High = Arr(0, 0.0)
BufferT3Low = Arr(0, 0.0)
BufferCandleO = Arr(0, 0.0)
BufferCandleH = Arr(0, 0.0)
BufferCandleL = Arr(0, 0.0)
BufferCandleC = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferHE1 = Arr(0, 0.0)
BufferHE2 = Arr(0, 0.0)
BufferHE3 = Arr(0, 0.0)
BufferHE4 = Arr(0, 0.0)
BufferHE5 = Arr(0, 0.0)
BufferHE6 = Arr(0, 0.0)
BufferLE1 = Arr(0, 0.0)
BufferLE2 = Arr(0, 0.0)
BufferLE3 = Arr(0, 0.0)
BufferLE4 = Arr(0, 0.0)
BufferLE5 = Arr(0, 0.0)
BufferLE6 = Arr(0, 0.0)
factor = 0.0
period = 0
handle_mah = 0
handle_mal = 0
c1 = 0.0
c2 = 0.0
c3 = 0.0
c4 = 0.0
w1 = 0.0
w2 = 0.0

def OnInit():
    global c1, c2, c3, c4, factor, period, w1, w2
    period = (1 if (InpPeriod < 1) else InpPeriod)
    factor = InpVolumeFactor
    b2 = 0.0
    b3 = 0.0
    b2 = factor * factor
    b3 = b2 * factor
    c1 = -b3
    c2 = 3.0 * (b2 + b3)
    c3 = -3.0 * ((2 * b2) + factor + b3)
    c4 = 1.0 + (3.0 * factor) + b3 + (3 * b2)
    n = 1.0 + (0.5 * (period - 1))
    w1 = _fdiv(2.0, n + 1.0)
    w2 = 1.0 - w1
    SetIndexBuffer(0, BufferT3High, INDICATOR_DATA)
    SetIndexBuffer(1, BufferT3Low, INDICATOR_DATA)
    SetIndexBuffer(2, BufferCandleO, INDICATOR_DATA)
    SetIndexBuffer(3, BufferCandleH, INDICATOR_DATA)
    SetIndexBuffer(4, BufferCandleL, INDICATOR_DATA)
    SetIndexBuffer(5, BufferCandleC, INDICATOR_DATA)
    SetIndexBuffer(6, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, BufferHE1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferHE2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferHE3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferHE4, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, BufferHE5, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, BufferHE6, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, BufferLE1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, BufferLE2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(15, BufferLE3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(16, BufferLE4, INDICATOR_CALCULATIONS)
    SetIndexBuffer(17, BufferLE5, INDICATOR_CALCULATIONS)
    SetIndexBuffer(18, BufferLE6, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'T3 Price Overlay (' + _str(period) + ',' + _str(factor) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(BufferT3High, True)
    ArraySetAsSeries(BufferT3Low, True)
    ArraySetAsSeries(BufferCandleO, True)
    ArraySetAsSeries(BufferCandleH, True)
    ArraySetAsSeries(BufferCandleL, True)
    ArraySetAsSeries(BufferCandleC, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferHE1, True)
    ArraySetAsSeries(BufferHE2, True)
    ArraySetAsSeries(BufferHE3, True)
    ArraySetAsSeries(BufferHE4, True)
    ArraySetAsSeries(BufferHE5, True)
    ArraySetAsSeries(BufferHE6, True)
    ArraySetAsSeries(BufferLE1, True)
    ArraySetAsSeries(BufferLE2, True)
    ArraySetAsSeries(BufferLE3, True)
    ArraySetAsSeries(BufferLE4, True)
    ArraySetAsSeries(BufferLE5, True)
    ArraySetAsSeries(BufferLE6, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferT3High, EMPTY_VALUE)
        ArrayInitialize(BufferT3Low, EMPTY_VALUE)
        ArrayInitialize(BufferCandleO, EMPTY_VALUE)
        ArrayInitialize(BufferCandleH, EMPTY_VALUE)
        ArrayInitialize(BufferCandleL, EMPTY_VALUE)
        ArrayInitialize(BufferCandleC, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 4)
        ArrayInitialize(BufferHE1, 0)
        ArrayInitialize(BufferHE2, 0)
        ArrayInitialize(BufferHE3, 0)
        ArrayInitialize(BufferHE4, 0)
        ArrayInitialize(BufferHE5, 0)
        ArrayInitialize(BufferHE6, 0)
        ArrayInitialize(BufferLE1, 0)
        ArrayInitialize(BufferLE2, 0)
        ArrayInitialize(BufferLE3, 0)
        ArrayInitialize(BufferLE4, 0)
        ArrayInitialize(BufferLE5, 0)
        ArrayInitialize(BufferLE6, 0)
    for i in range(limit, 0 - 1, -1):
        BufferHE1[i] = (w1 * high[i]) + (w2 * BufferHE1[i + 1])
        BufferHE2[i] = (w1 * BufferHE1[i]) + (w2 * BufferHE2[i + 1])
        BufferHE3[i] = (w1 * BufferHE2[i]) + (w2 * BufferHE3[i + 1])
        BufferHE4[i] = (w1 * BufferHE3[i]) + (w2 * BufferHE4[i + 1])
        BufferHE5[i] = (w1 * BufferHE4[i]) + (w2 * BufferHE5[i + 1])
        BufferHE6[i] = (w1 * BufferHE5[i]) + (w2 * BufferHE6[i + 1])
        BufferT3High[i] = (c1 * BufferHE6[i]) + (c2 * BufferHE5[i]) + (c3 * BufferHE4[i]) + (c4 * BufferHE3[i])
        BufferLE1[i] = (w1 * low[i]) + (w2 * BufferLE1[i + 1])
        BufferLE2[i] = (w1 * BufferLE1[i]) + (w2 * BufferLE2[i + 1])
        BufferLE3[i] = (w1 * BufferLE2[i]) + (w2 * BufferLE3[i + 1])
        BufferLE4[i] = (w1 * BufferLE3[i]) + (w2 * BufferLE4[i + 1])
        BufferLE5[i] = (w1 * BufferLE4[i]) + (w2 * BufferLE5[i + 1])
        BufferLE6[i] = (w1 * BufferLE5[i]) + (w2 * BufferLE6[i + 1])
        BufferT3Low[i] = (c1 * BufferLE6[i]) + (c2 * BufferLE5[i]) + (c3 * BufferLE4[i]) + (c4 * BufferLE3[i])
    for i in range(limit, 0 - 1, -1):
        if close[i] > BufferT3High[i]:
            BufferCandleO[i] = open[i]
            BufferCandleH[i] = high[i]
            BufferCandleL[i] = low[i]
            BufferCandleC[i] = close[i]
            BufferColors[i] = (0 if (open[i] < close[i]) else 1 if (open[i] > close[i]) else 4)
        elif close[i] < BufferT3Low[i]:
            BufferCandleO[i] = open[i]
            BufferCandleH[i] = high[i]
            BufferCandleL[i] = low[i]
            BufferCandleC[i] = close[i]
            BufferColors[i] = (2 if (open[i] > close[i]) else 3 if (open[i] < close[i]) else 4)
        else:
            BufferCandleC[i] = EMPTY_VALUE
            BufferCandleL[i] = BufferCandleC[i]
            BufferCandleH[i] = BufferCandleL[i]
            BufferCandleO[i] = BufferCandleH[i]
            BufferColors[i] = 4.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class T3PriceOverlay(_MQL5Indicator):
    name = 'T3_Price_Overlay'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # T3 period
        'InpVolumeFactor': 0.7,  # T3 volume factor
    }

