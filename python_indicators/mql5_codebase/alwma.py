"""ALWMA — converted from MQL5: MQL5 Indicators/ALWMA/ALWMA.mq5

Asymmetric Linear Weighted Moving Average
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [3937500]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'ALWMA'}, 'levels': [], 'description': ['Asymmetric Linear Weighted Moving Average'], 'name': 'ALWMA', 'source': 'MQL5 Indicators/ALWMA/ALWMA.mq5', 'folder': 'ALWMA', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpMode', 'py': 'InpMode', 'param': 'InpMode', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_MODE
MODE_REGULAR = 0
MODE_INVERSE = 1
MODE_ASYMMETRIC = 2
MODE_INV_ASYMM = 3
_enum('ENUM_MODE', {0: 'MODE_REGULAR', 1: 'MODE_INVERSE', 2: 'MODE_ASYMMETRIC', 3: 'MODE_INV_ASYMM'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpMode = _input('InpMode', MODE_REGULAR)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferALWMA = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period = 0
period_half = 0
handle_ma = 0

def OnInit():
    global handle_ma, period, period_half
    period = (1 if (InpPeriod < 1) else InpPeriod)
    period_half = _idiv(period, 2)
    SetIndexBuffer(0, BufferALWMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    method = StringSubstr(EnumToString(InpMode, 'ENUM_MODE'), 5)
    IndicatorSetString(INDICATOR_SHORTNAME, ModeToString() + ' LWMA (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferALWMA, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferALWMA, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
    bars = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, bars, BufferMA)
    if copied != bars:
        return 0
    for i in range(limit, 0 - 1, -1):
        count = 0.0
        total = 0.0
        k = 0.0
        for j in range(i + period, i - 1, -1):
            if InpMode == MODE_REGULAR:
                count += 1
            else:
                if InpMode == MODE_INVERSE:
                    if count == 0:
                        count = period
                    else:
                        count -= 1
                else:
                    if InpMode == MODE_ASYMMETRIC:
                        if count == 0:
                            count = 2.0
                        else:
                            if (j - i) < period_half:
                                count += 2
                            else:
                                count -= 2
                    else:
                        if count == 0:
                            count = period
                        else:
                            if (j - i) < period_half:
                                count -= 2
                            else:
                                count += 2
            k += count
            total += BufferMA[j] * count
        BufferALWMA[i] = _fdiv(total, k)
    return rates_total

def ModeToString():
    return ('Regular' if (InpMode == MODE_REGULAR) else 'Inverse' if (InpMode == MODE_INVERSE) else 'Asymmetric' if (InpMode == MODE_ASYMMETRIC) else 'Inverse asymmetric')


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ALWMA(_MQL5Indicator):
    name = 'ALWMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpMode': _Choice({0: 'Regular', 1: 'Inverse', 2: 'Asymmetric', 3: 'Inverse asymmetric'}, default=0),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

