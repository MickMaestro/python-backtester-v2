"""Projection_Bands — converted from MQL5: MQL5 Indicators/Projection_Bands/Projection_Bands.mq5

Projection Bands indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Band Up', 2: 'Band Down'}, 'levels': [], 'description': ['Projection Bands indicator'], 'name': 'Projection_Bands', 'source': 'MQL5 Indicators/Projection_Bands/Projection_Bands.mq5', 'folder': 'Projection_Bands', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
BufferBandUP = Arr(0, 0.0)
BufferBandDN = Arr(0, 0.0)
BufferH = Arr(0, 0.0)
BufferL = Arr(0, 0.0)
period = 0

def OnInit():
    global period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferBandUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferBandDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferH, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferL, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Projection Bands (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, (2 * period) - 1)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, (2 * period) - 1)
    ArraySetAsSeries(BufferBandUP, True)
    ArraySetAsSeries(BufferBandDN, True)
    ArraySetAsSeries(BufferH, True)
    ArraySetAsSeries(BufferL, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferBandUP, EMPTY_VALUE)
        ArrayInitialize(BufferBandDN, EMPTY_VALUE)
        ArrayInitialize(BufferH, 0)
        ArrayInitialize(BufferL, 0)
    for i in range(limit, 0 - 1, -1):
        BufferH[i] = high[i]
        BufferL[i] = low[i]
    for i in range(limit, 0 - 1, -1):
        SlopeHigh = LRegSlope(BufferH, i)
        SlopeLow = LRegSlope(BufferL, i)
        UpProjBand = high[i]
        DnProjBand = low[i]
        for j in range(1, period + 1):
            UpProjBand = fmax(UpProjBand, high[i + j] + (j * SlopeHigh))
            DnProjBand = fmin(DnProjBand, low[i + j] - (j * SlopeLow))
        BufferBandUP[i] = UpProjBand
        BufferBandDN[i] = DnProjBand
    return rates_total

def LRegSlope(price, index):
    x = 0.0
    y = 0.0
    xy = 0.0
    x2 = 0.0
    temp = 0.0
    m = 0.0
    for i in range(0, period):
        y = y + price[index + i]
        xy = xy + (price[index + i] * i)
        x = x + i
        x2 = x2 + (i * i)
    temp = (period * x2) - (x * x)
    m = _fdiv((period * xy) - (x * y), temp)
    return -m


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ProjectionBands(_MQL5Indicator):
    name = 'Projection_Bands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
    }

