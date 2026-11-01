"""Projection_Oscillator — converted from MQL5: MQL5 Indicators/Projection_Oscillator/Projection_Oscillator.mq5

Projection oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Projection osc'}, 'levels': [], 'description': ['Projection oscillator'], 'name': 'Projection_Oscillator', 'source': 'MQL5 Indicators/Projection_Oscillator/Projection_Oscillator.mq5', 'folder': 'Projection_Oscillator', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 90.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 10.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpOverbought = _input('InpOverbought', 90.0)  # Overbought
InpOversold = _input('InpOversold', 10.0)  # Oversold
BufferPO = Arr(0, 0.0)
BufferH = Arr(0, 0.0)
BufferL = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period = 0

def OnInit():
    global overbought, oversold, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else (overbought - 0.1) if (InpOversold >= overbought) else InpOversold)
    SetIndexBuffer(0, BufferPO, INDICATOR_DATA)
    SetIndexBuffer(1, BufferH, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferL, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Projection oscillator (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Oversold')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, (2 * period) - 1)
    ArraySetAsSeries(BufferPO, True)
    ArraySetAsSeries(BufferH, True)
    ArraySetAsSeries(BufferL, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferPO, EMPTY_VALUE)
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
        BufferPO[i] = (_fdiv(100.0 * (close[i] - DnProjBand), UpProjBand - DnProjBand) if (UpProjBand != DnProjBand) else 0)
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


class ProjectionOscillator(_MQL5Indicator):
    name = 'Projection_Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpOverbought': 90.0,  # Overbought
        'InpOversold': 10.0,  # Oversold
    }

