"""Better_Bollinger_Band — converted from MQL5: MQL5 Indicators/Better_Bollinger_Band/Better_Bollinger_Band.mq5

Better Bollinger Band indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [32768], 2: [16711680], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'DETop', 2: 'DECentral', 3: 'DEBottom'}, 'levels': [], 'description': ['Better Bollinger Band indicator'], 'name': 'Better_Bollinger_Band', 'source': 'MQL5 Indicators/Better_Bollinger_Band/Better_Bollinger_Band.mq5', 'folder': 'Better_Bollinger_Band', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 2.0, 'label': 'Deviation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpDeviation = _input('InpDeviation', 2.0)  # Deviation
BufferTop = Arr(0, 0.0)
BufferCentral = Arr(0, 0.0)
BufferBottom = Arr(0, 0.0)
BufferMT = Arr(0, 0.0)
BufferUT = Arr(0, 0.0)
BufferMT2 = Arr(0, 0.0)
BufferUT2 = Arr(0, 0.0)
deviation = 0.0
alpha = 0.0
period = 0

def OnInit():
    global alpha, deviation, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    deviation = InpDeviation
    alpha = _fdiv(2.0, 1.0 + period)
    SetIndexBuffer(0, BufferTop, INDICATOR_DATA)
    SetIndexBuffer(1, BufferCentral, INDICATOR_DATA)
    SetIndexBuffer(2, BufferBottom, INDICATOR_DATA)
    SetIndexBuffer(3, BufferMT, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferUT, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMT2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferUT2, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Better BB(' + _str(period) + ',' + DoubleToString(deviation, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferTop, True)
    ArraySetAsSeries(BufferCentral, True)
    ArraySetAsSeries(BufferBottom, True)
    ArraySetAsSeries(BufferMT, True)
    ArraySetAsSeries(BufferUT, True)
    ArraySetAsSeries(BufferMT2, True)
    ArraySetAsSeries(BufferUT2, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 2
        ArrayInitialize(BufferTop, EMPTY_VALUE)
        ArrayInitialize(BufferCentral, EMPTY_VALUE)
        ArrayInitialize(BufferBottom, EMPTY_VALUE)
        ArrayInitialize(BufferMT, 0)
        ArrayInitialize(BufferUT, 0)
        ArrayInitialize(BufferMT2, 0)
        ArrayInitialize(BufferUT2, 0)
    for i in range(limit, 0 - 1, -1):
        median = (high[i] + low[i]) / 2.0
        BufferMT[i] = (alpha * median) + ((1.0 - alpha) * BufferMT[i + 1])
        BufferUT[i] = (alpha * BufferMT[i]) + ((1.0 - alpha) * BufferUT[i + 1])
        BufferCentral[i] = _fdiv(((2.0 - alpha) * BufferMT[i]) - BufferUT[i], 1.0 - alpha)
        BufferMT2[i] = (alpha * fabs(median - BufferCentral[i])) + ((1.0 - alpha) * BufferMT2[i + 1])
        BufferUT2[i] = (alpha * BufferMT2[i]) + ((1.0 - alpha) * BufferUT2[i + 1])
        dt2 = _fdiv(((2.0 - alpha) * BufferMT2[i]) - BufferUT2[i], 1.0 - alpha)
        BufferTop[i] = BufferCentral[i] + (deviation * dt2)
        BufferBottom[i] = BufferCentral[i] - (deviation * dt2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BetterBollingerBand(_MQL5Indicator):
    name = 'Better_Bollinger_Band'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpDeviation': 2.0,  # Deviation
    }

