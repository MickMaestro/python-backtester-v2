"""Forecast — converted from MQL5: MQL5 Indicators/Forecast/Forecast.mq5

Forecast oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [11186720], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Forecast', 2: 'Signal'}, 'levels': [], 'description': ['Forecast oscillator'], 'name': 'Forecast', 'source': 'MQL5 Indicators/Forecast/Forecast.mq5', 'folder': 'Forecast', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpPeriodSignal', 'py': 'InpPeriodSignal', 'param': 'InpPeriodSignal', 'type': 'uint', 'default': 3, 'label': 'Signal period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpPeriodSignal = _input('InpPeriodSignal', 3)  # Signal period
BufferFO = Arr(0, 0.0)
BufferSig = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period_fc = 0
period_sig = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_fc, period_sig
    period_fc = (1 if (InpPeriod < 1) else InpPeriod)
    period_sig = (1 if (InpPeriodSignal < 1) else InpPeriodSignal)
    SetIndexBuffer(0, BufferFO, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSig, INDICATOR_DATA)
    SetIndexBuffer(2, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Forecast Oscillator (' + _str(period_fc) + ',' + _str(period_sig) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferFO, True)
    ArraySetAsSeries(BufferSig, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_fc, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_fc - 1
        ArrayInitialize(BufferFO, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        t = period_fc
        sx = 0.0
        sy = 0.0
        sxy = 0.0
        sx2 = 0.0
        for j in range(i + period_fc, i + 1 - 1, -1):
            sy += BufferMA[j]
            sx += t
            sx2 += t * t
            sxy += BufferMA[j] * t
            t -= 1
        b = _fdiv((period_fc * sxy) - (sx * sy), (period_fc * sx2) - (sx * sx))
        a = _fdiv(sy - (b * sx), period_fc)
        tsf = a + b
        BufferFO[i] = (_fdiv(100.0 * (BufferMA[i] - tsf), BufferMA[i]) if (BufferMA[i] != 0) else 0)
        BufferSig[i] = GetSMA(rates_total, i, period_sig, BufferFO)
    return rates_total

def GetSMA(rates_total, index, period, price, as_series=True):
    result = 0.0
    check_index = ((index <= (rates_total - period - 1)) if as_series else (index >= (period - 1)))
    if period < 1 or (not check_index):
        return 0.0
    for i in range(0, period):
        result = result + (price[index + i] if as_series else price[index - i])
    return _fdiv(result, period)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Forecast(_MQL5Indicator):
    name = 'Forecast'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpPeriodSignal': 3,  # Signal period
    }

