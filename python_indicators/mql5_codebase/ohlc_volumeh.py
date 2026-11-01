"""OHLC_VolumeH — converted from MQL5: MQL5 Indicators/OHLC_VolumeH/OHLC_VolumeH.mq5

OHLC Volume Histogram indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255, 11119017]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'OHLCV'}, 'levels': [], 'description': ['OHLC Volume Histogram indicator'], 'name': 'OHLC_VolumeH', 'source': 'MQL5 Indicators/OHLC_VolumeH/OHLC_VolumeH.mq5', 'folder': 'OHLC_VolumeH', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BufferOHLCV = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferOHLCV, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'OHLC VolumeH')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferOHLCV, True)
    ArraySetAsSeries(BufferColors, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferOHLCV, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        up_coeff = high[i] - open[i]
        dn_coeff = close[i] - low[i]
        sum_coeff = up_coeff + dn_coeff
        if sum_coeff != 0:
            up_v = _fdiv(tick_volume[i] * up_coeff, sum_coeff)
            dn_v = _fdiv(tick_volume[i] * dn_coeff, sum_coeff)
            BufferOHLCV[i] = up_v - dn_v
            BufferColors[i] = (0 if (up_v > dn_v) else 1 if (up_v < dn_v) else 2)
        else:
            BufferOHLCV[i] = 0.0
            BufferColors[i] = 2.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class OHLCVolumeH(_MQL5Indicator):
    name = 'OHLC_VolumeH'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

