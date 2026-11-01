"""Rainbow_Volume — converted from MQL5: MQL5 Indicators/Rainbow_Volume/Rainbow_Volume.mq5

Rainbow Volume indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 16748574, 255, 55295, 12632256]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'VOL'}, 'levels': [], 'description': ['Rainbow Volume indicator'], 'name': 'Rainbow_Volume', 'source': 'MQL5 Indicators/Rainbow_Volume/Rainbow_Volume.mq5', 'folder': 'Rainbow_Volume', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
BufferVOL = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
period = 0

def OnInit():
    global period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferVOL, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Rainbow Volume (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    ArraySetAsSeries(BufferVOL, True)
    ArraySetAsSeries(BufferColors, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < period:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferVOL, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        BufferVOL[i] = float(tick_volume[i])
        BufferColors[i] = (0 if (close[i] > close[i + period] and tick_volume[i] > tick_volume[i + period]) else 1 if (close[i] > close[i + period] and tick_volume[i] < tick_volume[i + period]) else 2 if (close[i] < close[i + period] and tick_volume[i] > tick_volume[i + period]) else 3 if (close[i] < close[i + period] and tick_volume[i] < tick_volume[i + period]) else 4)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RainbowVolume(_MQL5Indicator):
    name = 'Rainbow_Volume'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
    }

