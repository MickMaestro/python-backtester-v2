"""TCI — converted from MQL5: MQL5 Indicators/TCI V2/TCI.mq5

Trend Confirmation Index indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [2263842], 2: [12632256]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'TCI', 2: 'Actual CP'}, 'levels': [], 'description': ['Trend Confirmation Index indicator'], 'name': 'TCI', 'source': 'MQL5 Indicators/TCI V2/TCI.mq5', 'folder': 'TCI V2', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 70.0, 'label': 'Overbought level', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 30.0, 'label': 'Oversold level', 'sinput': False}, {'mql': 'InpShowActual', 'py': 'InpShowActual', 'param': 'InpShowActual', 'type': 'int', 'default': 0, 'label': 'Show actual CPP', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpOverbought = _input('InpOverbought', 70.0)  # Overbought level
InpOversold = _input('InpOversold', 30.0)  # Oversold level
InpShowActual = _input('InpShowActual', INPUT_NO)  # Show actual CPP
BufferTCI = Arr(0, 0.0)
BufferCPP = Arr(0, 0.0)
BufferAVG = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_ind = 0
weight_sum = 0

def OnInit():
    global overbought, oversold, period_ind
    period_ind = (2 if (InpPeriod < 2) else InpPeriod)
    oversold = (0 if (InpOversold < 0) else 99.9 if (InpOversold > 99.9) else InpOversold)
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    if overbought <= oversold:
        overbought = oversold + 0.1
    if oversold >= overbought:
        oversold = overbought - 0.1
    SetIndexBuffer(0, BufferTCI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferCPP, INDICATOR_DATA)
    SetIndexBuffer(2, BufferAVG, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, (DRAW_LINE if InpShowActual else DRAW_NONE))
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend Confirmation Index (' + _str(period_ind) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, oversold)
    ArraySetAsSeries(BufferTCI, True)
    ArraySetAsSeries(BufferCPP, True)
    ArraySetAsSeries(BufferAVG, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < 2:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferTCI, EMPTY_VALUE)
        ArrayInitialize(BufferCPP, EMPTY_VALUE)
        ArrayInitialize(BufferAVG, 0)
    for i in range(limit, 0 - 1, -1):
        BufferCPP[i] = (_fdiv(100.0 * (close[i] - low[i]), high[i] - low[i]) if ((high[i] - low[i]) != 0) else 0)
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferCPP, BufferTCI)
    elif _sw1 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferCPP, BufferTCI)
    elif _sw1 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_ind, BufferCPP, BufferTCI, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferCPP, BufferTCI)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TCI(_MQL5Indicator):
    name = 'TCI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpOverbought': 70.0,  # Overbought level
        'InpOversold': 30.0,  # Oversold level
        'InpShowActual': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Show actual CPP
    }

