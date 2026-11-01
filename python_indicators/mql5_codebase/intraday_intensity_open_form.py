"""Intraday_Intensity_Open_Form — converted from MQL5: MQL5 Indicators/Intraday_Intensity_Open_Form/Intraday_Intensity_Open_Form.mq5

Intraday Intensity Open Form indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [2263842]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'IDay Intensity'}, 'levels': [], 'description': ['Intraday Intensity Open Form indicator'], 'name': 'Intraday_Intensity_Open_Form', 'source': 'MQL5 Indicators/Intraday_Intensity_Open_Form/Intraday_Intensity_Open_Form.mq5', 'folder': 'Intraday_Intensity_Open_Form', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BufferIntensity = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferIntensity, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Intraday Intensity Open Form')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferIntensity, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferIntensity, 0)
    for i in range(limit, 0 - 1, -1):
        val = ((high[i] - low[i]) if ((high[i] - low[i]) != 0) else 1.0)
        BufferIntensity[i] = BufferIntensity[i + 1] + (_fdiv((2.0 * close[i]) - high[i] - low[i], val) * tick_volume[i])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IntradayIntensityOpenForm(_MQL5Indicator):
    name = 'Intraday_Intensity_Open_Form'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

