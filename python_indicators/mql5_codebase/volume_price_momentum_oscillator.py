"""Volume_Price_Momentum_Oscillator — converted from MQL5: MQL5 Indicators/Volume_Price_Momentum_Oscillator/Volume_Price_Momentum_Oscillator.mq5

Volume Price Momentum oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'VPMO'}, 'levels': [], 'description': ['Volume Price Momentum oscillator'], 'name': 'Volume_Price_Momentum_Oscillator', 'source': 'MQL5 Indicators/Volume_Price_Momentum_Oscillator/Volume_Price_Momentum_Oscillator.mq5', 'folder': 'Volume_Price_Momentum_Oscillator', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 3, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 3)  # Period
BufferVPMO = Arr(0, 0.0)
BufferVPM = Arr(0, 0.0)
period_ma = 0

def OnInit():
    global period_ma
    period_ma = (2 if (InpPeriod < 2) else InpPeriod)
    SetIndexBuffer(0, BufferVPMO, INDICATOR_DATA)
    SetIndexBuffer(1, BufferVPM, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volume Price Momentum Osc(' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferVPMO, True)
    ArraySetAsSeries(BufferVPM, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < fmax(period_ma, 4) or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferVPMO, EMPTY_VALUE)
        ArrayInitialize(BufferVPM, 0)
    for i in range(limit, 0 - 1, -1):
        BufferVPM[i] = _fdiv(tick_volume[i] * (close[i] - close[i + 1]), Point())
    return ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ma, BufferVPM, BufferVPMO)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolumePriceMomentumOscillator(_MQL5Indicator):
    name = 'Volume_Price_Momentum_Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 3,  # Period
    }

