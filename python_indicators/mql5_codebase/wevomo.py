"""WEVOMO — converted from MQL5: MQL5 Indicators/WEVOMO/WEVOMO.mq5

Weight Volume Move-Adjusted Moving Average
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'VMoveAdjMA', 2: 'WVMovAdjMA'}, 'levels': [], 'description': ['Weight Volume Move-Adjusted Moving Average'], 'name': 'WEVOMO', 'source': 'MQL5 Indicators/WEVOMO/WEVOMO.mq5', 'folder': 'WEVOMO', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpShowVMA', 'py': 'InpShowVMA', 'param': 'InpShowVMA', 'type': 'int', 'default': 1, 'label': 'Show Volume Move MA', 'sinput': False}, {'mql': 'InpShowWMA', 'py': 'InpShowWMA', 'param': 'InpShowWMA', 'type': 'int', 'default': 1, 'label': 'Show Weighted Volume Move MA', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpShowVMA = _input('InpShowVMA', INPUT_YES)  # Show Volume Move MA
InpShowWMA = _input('InpShowWMA', INPUT_YES)  # Show Weighted Volume Move MA
BufferVOMOMA = Arr(0, 0.0)
BufferWEVOMO = Arr(0, 0.0)
BufferDiff = Arr(0, 0.0)
BufferVol = Arr(0, 0.0)
BufferDiffMA = Arr(0, 0.0)
BufferVolMA = Arr(0, 0.0)
period_ind = 0
lsum = 0.0

def OnInit():
    global lsum, period_ind
    period_ind = (2 if (InpPeriod < 2) else InpPeriod)
    lsum = ((period_ind + 1.0) * period_ind) / 2.0
    SetIndexBuffer(0, BufferVOMOMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferWEVOMO, INDICATOR_DATA)
    SetIndexBuffer(2, BufferDiff, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferVol, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferDiffMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferVolMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'WVolume Move-Adjusted MA (' + _str(period_ind) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferVOMOMA, True)
    ArraySetAsSeries(BufferWEVOMO, True)
    ArraySetAsSeries(BufferDiff, True)
    ArraySetAsSeries(BufferVol, True)
    ArraySetAsSeries(BufferDiffMA, True)
    ArraySetAsSeries(BufferVolMA, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_ind - 2
        ArrayInitialize(BufferVOMOMA, EMPTY_VALUE)
        ArrayInitialize(BufferWEVOMO, EMPTY_VALUE)
        ArrayInitialize(BufferDiff, 0)
        ArrayInitialize(BufferVol, 0)
        ArrayInitialize(BufferDiffMA, 0)
        ArrayInitialize(BufferVolMA, 0)
    for i in range(limit, 0 - 1, -1):
        BufferDiff[i] = fabs(close[i] - close[i + 1])
        BufferVol[i] = float(tick_volume[i])
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferDiff, BufferDiffMA)
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferVol, BufferVolMA)
    for i in range(limit, 0 - 1, -1):
        DifferenceSum = BufferDiffMA[i] * period_ind
        VolumeSum = BufferVolMA[i] * period_ind
        if DifferenceSum != 0 and VolumeSum != 0:
            VOMA = 0.0
            MOMA = 0.0
            WMA = 0.0
            for j in range(1, period_ind + 1):
                MOMA += _fdiv(close[i + period_ind - j] * BufferDiff[i + period_ind - j], DifferenceSum)
                VOMA += _fdiv(close[i + period_ind - j] * BufferVol[i + period_ind - j], VolumeSum)
                WMA += close[i + period_ind - j] * j
            WMA = _fdiv(WMA, lsum)
            if InpShowVMA:
                BufferVOMOMA[i] = (MOMA + VOMA) / 2.0
            if InpShowWMA:
                BufferWEVOMO[i] = (MOMA + VOMA + WMA) / 3.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WEVOMO(_MQL5Indicator):
    name = 'WEVOMO'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpShowVMA': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show Volume Move MA
        'InpShowWMA': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show Weighted Volume Move MA
    }

