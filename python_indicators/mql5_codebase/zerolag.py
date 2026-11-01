"""ZeroLag — converted from MQL5: MQL5 Indicators/ZeroLag/ZeroLag.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'ZL'}, 'levels': [], 'description': [], 'name': 'ZeroLag', 'source': 'MQL5 Indicators/ZeroLag/ZeroLag.mq5', 'folder': 'ZeroLag', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpGainLimit', 'py': 'InpGainLimit', 'param': 'InpGainLimit', 'type': 'uint', 'default': 50, 'label': 'Gain limit', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpGainLimit = _input('InpGainLimit', 50)  # Gain limit
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferZL = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
BufferEMA = Arr(0, 0.0)
handle_sma = 0
handle_ema = 0
period = 0
gain_limit = 0
gain10 = 0.0
alpha = 0.0

def OnInit():
    global alpha, gain10, gain_limit, handle_ema, handle_sma, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    gain_limit = _int(InpGainLimit)
    alpha = _fdiv(2.0, 1.0 + period)
    gain10 = gain_limit / 10.0
    SetIndexBuffer(0, BufferZL, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferEMA, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Zero lag EMA(' + _str(period) + ',' + _str(gain_limit) + ')')
    ArraySetAsSeries(BufferZL, True)
    ArraySetAsSeries(BufferSMA, True)
    ArraySetAsSeries(BufferEMA, True)
    ResetLastError()
    handle_sma = iMA(Symbol(), PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_sma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_ema = iMA(Symbol(), PERIOD_CURRENT, period, 0, MODE_EMA, InpAppliedPrice)
    if handle_ema == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 3:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferZL, 0)
        ArrayInitialize(BufferSMA, 0)
        ArrayInitialize(BufferEMA, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_sma, 0, 0, count, BufferSMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ema, 0, 0, count, BufferEMA)
    if copied != count:
        return 0
    diff = 0.0
    gain = 0.0
    for i in range(limit, 0 - 1, -1):
        err = BufferSMA[i] - BufferZL[i + 1]
        if fabs(alpha * err) > 1e-09:
            val = alpha * err
            diff = BufferZL[i + 1] - BufferEMA[i]
            gain = (_fdiv(err + (alpha * diff), val) if (val != 0) else 0)
        val = fmax(fmin(gain, gain10), -gain10)
        gain = ((floor((val * 10) + 0.5) / 10) if (val > 0) else (ceil((val * 10) - 0.5) / 10))
        BufferZL[i] = (alpha * (BufferEMA[i] + (gain * err))) + ((1 - alpha) * BufferZL[i + 1])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ZeroLag(_MQL5Indicator):
    name = 'ZeroLag'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpGainLimit': 50,  # Gain limit
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

