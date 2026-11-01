"""Smart_Money_Pressure_Oscillator — converted from MQL5: MQL5 Indicators/Smart_Money_Pressure_Oscillator/Smart_Money_Pressure_Oscillator.mq5

Smart Money Pressure Oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [10526303]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'SMP'}, 'levels': [], 'description': ['Smart Money Pressure Oscillator'], 'name': 'Smart_Money_Pressure_Oscillator', 'source': 'MQL5 Indicators/Smart_Money_Pressure_Oscillator/Smart_Money_Pressure_Oscillator.mq5', 'folder': 'Smart_Money_Pressure_Oscillator', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
BufferSMP = Arr(0, 0.0)
BufferSM = Arr(0, 0.0)
BufferVol = Arr(0, 0.0)
BufferVolMA = Arr(0, 0.0)
period_ind = 0
weight_sum = 0

def OnInit():
    global period_ind
    period_ind = (2 if (InpPeriod < 2) else InpPeriod)
    SetIndexBuffer(0, BufferSMP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSM, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferVol, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferVolMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Smart Money Pressure (' + _str(period_ind) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferSMP, True)
    ArraySetAsSeries(BufferSM, True)
    ArraySetAsSeries(BufferVol, True)
    ArraySetAsSeries(BufferVolMA, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < 4 or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    first = rates_total - period_ind - 2
    if limit > 1:
        limit = first
        ArrayInitialize(BufferSMP, EMPTY_VALUE)
        ArrayInitialize(BufferSM, 0)
        ArrayInitialize(BufferVol, 0)
        ArrayInitialize(BufferVolMA, 0)
    for i in range(limit, 0 - 1, -1):
        BufferVol[i] = float(tick_volume[i])
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferVol, BufferVolMA)
    for i in range(limit, 0 - 1, -1):
        if i == first:
            BufferSM[i] = close[i]
        else:
            VolMA = BufferVolMA[i]
            Change = close[i] - close[i + 1]
            BufferSM[i] = ((BufferSM[i + 1] + Change) if (BufferVol[i] > VolMA) else BufferSM[i + 1])
            BufferSMP[i] = _fdiv(close[period_ind] - BufferSM[i], Point())
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SmartMoneyPressureOscillator(_MQL5Indicator):
    name = 'Smart_Money_Pressure_Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpPeriod': 14,  # Period
    }

