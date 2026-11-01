"""GD — converted from MQL5: MQL5 Indicators/GD/GD.mq5

Generalized DEMA indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'GD'}, 'levels': [], 'description': ['Generalized DEMA indicator'], 'name': 'GD', 'source': 'MQL5 Indicators/GD/GD.mq5', 'folder': 'GD', 'inputs': [{'mql': 'InpVolFactor', 'py': 'InpVolFactor', 'param': 'InpVolFactor', 'type': 'uint', 'default': 70, 'label': 'Volume factor (in percent)', 'sinput': False}, {'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpVolFactor = _input('InpVolFactor', 70)  # Volume factor (in percent)
InpPeriod = _input('InpPeriod', 20)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferGD = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferAVG = Arr(0, 0.0)
vol_factor = 0.0
period_ma = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_ma, vol_factor
    period_ma = (2 if (InpPeriod < 2) else InpPeriod)
    vol_factor = InpVolFactor / 100.0
    SetIndexBuffer(0, BufferGD, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferAVG, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Generalized DEMA (' + _str(period_ma) + ',' + DoubleToString(vol_factor * 100, 0) + '%)')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferGD, True)
    ArraySetAsSeries(BufferAVG, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_ma, 0, MODE_EMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_ma, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferGD, EMPTY_VALUE)
        ArrayInitialize(BufferAVG, 0)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ma, BufferMA, BufferAVG) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferGD[i] = ((1.0 + vol_factor) * BufferMA[i]) - (vol_factor * BufferAVG[i])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GD(_MQL5Indicator):
    name = 'GD'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpVolFactor': 70,  # Volume factor (in percent)
        'InpPeriod': 20,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

