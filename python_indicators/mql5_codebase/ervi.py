"""ERVI — converted from MQL5: MQL5 Indicators/ERVI/ERVI.mq5

John F.Ehlers RVI oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'RVI', 2: 'Signal'}, 'levels': [], 'description': ['John F.Ehlers RVI oscillator'], 'name': 'ERVI', 'source': 'MQL5 Indicators/ERVI/ERVI.mq5', 'folder': 'ERVI', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
BufferRVI = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferValue1 = Arr(0, 0.0)
BufferValue2 = Arr(0, 0.0)
BufferSMAV1 = Arr(0, 0.0)
BufferSMAV2 = Arr(0, 0.0)
period_sm = 0

def OnInit():
    global period_sm
    period_sm = (2 if (InpPeriod < 2) else InpPeriod)
    SetIndexBuffer(0, BufferRVI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(2, BufferValue1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferValue2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferSMAV1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferSMAV2, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ERVI(' + _str(period_sm) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferRVI, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferValue1, True)
    ArraySetAsSeries(BufferValue2, True)
    ArraySetAsSeries(BufferSMAV1, True)
    ArraySetAsSeries(BufferSMAV2, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 4
        ArrayInitialize(BufferRVI, EMPTY_VALUE)
        ArrayInitialize(BufferSignal, EMPTY_VALUE)
        ArrayInitialize(BufferValue1, 0)
        ArrayInitialize(BufferValue2, 0)
        ArrayInitialize(BufferSMAV1, 0)
        ArrayInitialize(BufferSMAV2, 0)
    for i in range(limit, 0 - 1, -1):
        BufferValue1[i] = (close[i] - open[i] + (2.0 * (close[i + 1] - open[i + 1])) + (2.0 * (close[i + 2] - open[i + 2])) + (close[i + 3] - open[i + 3])) / 6.0
        BufferValue2[i] = (high[i] - low[i] + (2.0 * (high[i + 1] - low[i + 1])) + (2.0 * (high[i + 2] - low[i + 2])) + (high[i + 3] - low[i + 3])) / 6.0
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferValue1, BufferSMAV1)
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferValue2, BufferSMAV2)
    for i in range(limit, 0 - 1, -1):
        num = BufferSMAV1[i]
        denom = BufferSMAV2[i]
        BufferRVI[i] = (_fdiv(num, denom) if (denom != 0) else 0)
        BufferSignal[i] = (BufferRVI[i] + (2.0 * BufferRVI[i + 1]) + (2.0 * BufferRVI[i + 2]) + BufferRVI[i + 3]) / 6.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ERVI(_MQL5Indicator):
    name = 'ERVI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
    }

