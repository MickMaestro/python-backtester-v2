"""TP — converted from MQL5: MQL5 Indicators/Advance Trend Pressure/TP.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16760576], 2: [7451452], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Trend', 2: 'Up', 3: 'Down'}, 'levels': [], 'description': [], 'name': 'TP', 'source': 'MQL5 Indicators/Advance Trend Pressure/TP.mq5', 'folder': 'Advance Trend Pressure', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpShowUpDn', 'py': 'InpShowUpDn', 'param': 'InpShowUpDn', 'type': 'int', 'default': 0, 'label': 'Show lines Up and Down', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpShowUpDn = _input('InpShowUpDn', INPUT_NO)  # Show lines Up and Down
BufferTP = Arr(0, 0.0)
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
period = 0

def OnInit():
    global period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferTP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(2, BufferDN, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Advance Trend Pressure(' + _str(period) + ')')
    ArraySetAsSeries(BufferTP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferUP, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferTP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferUP, EMPTY_VALUE)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    for i in range(limit, 0 - 1, -1):
        summ_up = 0.0
        summ_dn = 0.0
        for n in range(0, period):
            if close[i + n] > open[i + n]:
                summ_up += close[i + n] - open[i + n]
                summ_up += open[i + n] - low[i + n]
                summ_dn += high[i + n] - close[i + n]
            elif close[i + n] < open[i + n]:
                summ_dn += open[i + n] - close[i + n]
                summ_dn += high[i + n] - open[i + n]
                summ_up += close[i + n] - low[i + n]
        if InpShowUpDn:
            BufferUP[i] = summ_up
            BufferDN[i] = summ_dn
        else:
            BufferDN[i] = EMPTY_VALUE
            BufferUP[i] = BufferDN[i]
        BufferTP[i] = summ_up - summ_dn
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TP(_MQL5Indicator):
    name = 'TP'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpShowUpDn': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Show lines Up and Down
    }

