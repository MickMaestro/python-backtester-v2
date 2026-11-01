"""EF — converted from MQL5: MQL5 Indicators/EF/EF.mq5

Ehlers Filter indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [9157775]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'EF'}, 'levels': [], 'description': ['Ehlers Filter indicator'], 'name': 'EF', 'source': 'MQL5 Indicators/EF/EF.mq5', 'folder': 'EF', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpMomentum', 'py': 'InpMomentum', 'param': 'InpMomentum', 'type': 'uint', 'default': 5, 'label': 'Momentum', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpMomentum = _input('InpMomentum', 5)  # Momentum
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferEF = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferCoeff = Arr(0, 0.0)
BufferPriceCoeff = Arr(0, 0.0)
BufferCoeffAVG = Arr(0, 0.0)
BufferPriceCoeffAVG = Arr(0, 0.0)
period_ind = 0
momentum = 0
handle_ma = 0

def OnInit():
    global handle_ma, momentum, period_ind
    period_ind = (2 if (InpPeriod < 2) else InpPeriod)
    momentum = (1 if (InpMomentum < 1) else InpMomentum)
    SetIndexBuffer(0, BufferEF, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferCoeff, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferPriceCoeff, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferCoeffAVG, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferPriceCoeffAVG, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Ehlers Filter (' + _str(period_ind) + ',' + _str(momentum) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferEF, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferCoeff, True)
    ArraySetAsSeries(BufferPriceCoeff, True)
    ArraySetAsSeries(BufferCoeffAVG, True)
    ArraySetAsSeries(BufferPriceCoeffAVG, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - momentum - 1
        ArrayInitialize(BufferEF, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferCoeff, 0)
        ArrayInitialize(BufferPriceCoeff, 0)
        ArrayInitialize(BufferCoeffAVG, 0)
        ArrayInitialize(BufferPriceCoeffAVG, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferCoeff[i] = fabs(BufferMA[i] - BufferMA[i + momentum])
        BufferPriceCoeff[i] = BufferCoeff[i] * BufferMA[i]
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferCoeff, BufferCoeffAVG)
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferPriceCoeff, BufferPriceCoeffAVG)
    for i in range(limit, 0 - 1, -1):
        AvgCoeff = BufferCoeffAVG[i]
        BufferEF[i] = _fdiv(BufferPriceCoeffAVG[i], (AvgCoeff if (AvgCoeff != 0) else 1.0))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EF(_MQL5Indicator):
    name = 'EF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpMomentum': 5,  # Momentum
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

