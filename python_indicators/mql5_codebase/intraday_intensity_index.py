"""Intraday_Intensity_Index — converted from MQL5: MQL5 Indicators/Intraday_Intensity_Index/Intraday_Intensity_Index.mq5

Intraday Intensity Index indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [2237106]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Intensity Idx'}, 'levels': [], 'description': ['Intraday Intensity Index indicator'], 'name': 'Intraday_Intensity_Index', 'source': 'MQL5 Indicators/Intraday_Intensity_Index/Intraday_Intensity_Index.mq5', 'folder': 'Intraday_Intensity_Index', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 21, 'label': 'Period', 'sinput': False}, {'mql': 'InpUseNorm', 'py': 'InpUseNorm', 'param': 'InpUseNorm', 'type': 'int', 'default': 1, 'label': 'Use normalization', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 21)  # Period
InpUseNorm = _input('InpUseNorm', INPUT_YES)  # Use normalization
BufferIIDX = Arr(0, 0.0)
BufferRAW = Arr(0, 0.0)
BufferAVG1 = Arr(0, 0.0)
BufferAVG2 = Arr(0, 0.0)
BufferVol = Arr(0, 0.0)
period_ind = 0

def OnInit():
    global period_ind
    period_ind = (2 if (InpPeriod < 2) else InpPeriod)
    SetIndexBuffer(0, BufferIIDX, INDICATOR_DATA)
    SetIndexBuffer(1, BufferRAW, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferAVG1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferAVG2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferVol, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Intraday Intensity Index (' + _str(period_ind) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferIIDX, True)
    ArraySetAsSeries(BufferRAW, True)
    ArraySetAsSeries(BufferAVG1, True)
    ArraySetAsSeries(BufferAVG2, True)
    ArraySetAsSeries(BufferVol, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < 4 or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferIIDX, EMPTY_VALUE)
        ArrayInitialize(BufferRAW, 0)
        ArrayInitialize(BufferAVG1, 0)
        ArrayInitialize(BufferAVG2, 0)
        ArrayInitialize(BufferVol, 0)
    for i in range(limit, 0 - 1, -1):
        v = high[i] - low[i]
        BufferRAW[i] = _fdiv((2.0 * close[i]) - high[i] - low[i], (v if (v != 0) else 1.0)) * tick_volume[i]
        BufferVol[i] = float(tick_volume[i])
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferRAW, BufferAVG1)
    if InpUseNorm:
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferVol, BufferAVG2)
    for i in range(limit, 0 - 1, -1):
        BufferIIDX[i] = (_fdiv(100.0 * BufferAVG1[i], ((BufferAVG2[i] * Point()) if (BufferAVG2[i] != 0) else 1.0)) if InpUseNorm else (BufferAVG1[i] * period_ind)) * Point()
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IntradayIntensityIndex(_MQL5Indicator):
    name = 'Intraday_Intensity_Index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 21,  # Period
        'InpUseNorm': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use normalization
    }

