"""DMX — converted from MQL5: MQL5 Indicators/DMX/DMX.mq5

Bipolar DMI oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'DMX', 2: 'Signal'}, 'levels': [], 'description': ['Bipolar DMI oscillator'], 'name': 'DMX', 'source': 'MQL5 Indicators/DMX/DMX.mq5', 'folder': 'DMX', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'DMX Period', 'sinput': False}, {'mql': 'InpPeriodSm', 'py': 'InpPeriodSm', 'param': 'InpPeriodSm', 'type': 'uint', 'default': 5, 'label': 'Signal period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # DMX Period
InpPeriodSm = _input('InpPeriodSm', 5)  # Signal period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferDMX = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferDIP = Arr(0, 0.0)
BufferDIM = Arr(0, 0.0)
period_adx = 0
period_smooth = 0
weight_sum = 0
handle_adx = 0

def OnInit():
    global handle_adx, period_adx, period_smooth
    period_adx = (1 if (InpPeriod < 1) else InpPeriod)
    period_smooth = (2 if (InpPeriodSm < 2) else InpPeriodSm)
    SetIndexBuffer(0, BufferDMX, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(2, BufferDIP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferDIM, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'DMX (' + _str(period_adx) + ',' + _str(period_smooth) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferDMX, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferDIP, True)
    ArraySetAsSeries(BufferDIM, True)
    ResetLastError()
    handle_adx = iADX(None, PERIOD_CURRENT, period_adx)
    if handle_adx == INVALID_HANDLE:
        Print('The iADX(', _str(period_adx), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferDMX, EMPTY_VALUE)
        ArrayInitialize(BufferSignal, EMPTY_VALUE)
        ArrayInitialize(BufferDIP, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_adx, PLUSDI_LINE, 0, count, BufferDIP)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_adx, MINUSDI_LINE, 0, count, BufferDIM)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        sum_ = BufferDIP[i] + BufferDIM[i]
        BufferDMX[i] = (_fdiv(BufferDIP[i] - BufferDIM[i], sum_) if (sum_ != 0) else 0)
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_smooth, BufferDMX, BufferSignal)
    elif _sw1 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_smooth, BufferDMX, BufferSignal)
    elif _sw1 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_smooth, BufferDMX, BufferSignal, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_smooth, BufferDMX, BufferSignal)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DMX(_MQL5Indicator):
    name = 'DMX'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # DMX Period
        'InpPeriodSm': 5,  # Signal period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

