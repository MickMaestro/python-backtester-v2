"""OHLC_Volume_Histo — converted from MQL5: MQL5 Indicators/OHLC_Volume_Histo/OHLC_Volume_Histo.mq5

OHLC Volume Histogram indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [3329330, 255, 11119017]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'VolHisto'}, 'levels': [], 'description': ['OHLC Volume Histogram indicator'], 'name': 'OHLC_Volume_Histo', 'source': 'MQL5 Indicators/OHLC_Volume_Histo/OHLC_Volume_Histo.mq5', 'folder': 'OHLC_Volume_Histo', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BufferVolHist = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferVolUP = Arr(0, 0.0)
BufferVolDN = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferVolHist, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferVolUP, INDICATOR_DATA)
    SetIndexBuffer(3, BufferVolDN, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'OHLC Volume Histogram')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferVolHist, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferVolUP, True)
    ArraySetAsSeries(BufferVolDN, True)
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
        ArrayInitialize(BufferVolHist, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferVolUP, 0)
        ArrayInitialize(BufferVolDN, 0)
    for i in range(limit, 0 - 1, -1):
        coeff_up = Point() + (high[i] - open[i])
        coeff_dn = Point() + (close[i] - low[i])
        coeff_sum = coeff_up + coeff_dn
        BufferVolUP[i] = (_fdiv(tick_volume[i] * coeff_up, coeff_sum) if (coeff_sum != 0) else 0)
        BufferVolDN[i] = (_fdiv(tick_volume[i] * coeff_dn, coeff_sum) if (coeff_sum != 0) else 0)
        BufferVolHist[i] = BufferVolUP[i] - BufferVolDN[i]
        BufferColors[i] = (0 if (BufferVolUP[i] > BufferVolDN[i]) else 1 if (BufferVolUP[i] < BufferVolDN[i]) else 2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class OHLCVolumeHisto(_MQL5Indicator):
    name = 'OHLC_Volume_Histo'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

