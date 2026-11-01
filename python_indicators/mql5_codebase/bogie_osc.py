"""Bogie_Osc — converted from MQL5: MQL5 Indicators/Bogie/Bogie_Osc.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [3937500]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Bogie'}, 'levels': [], 'description': [], 'name': 'Bogie_Osc', 'source': 'MQL5 Indicators/Bogie/Bogie_Osc.mq5', 'folder': 'Bogie', 'inputs': [{'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 7, 'label': 'Fast MA period', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 14, 'label': 'Slow MA period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodFast = _input('InpPeriodFast', 7)  # Fast MA period
InpPeriodSlow = _input('InpPeriodSlow', 14)  # Slow MA period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferBogie = Arr(0, 0.0)
BufferMAF = Arr(0, 0.0)
BufferMAS = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
period_maf = 0
period_mas = 0
handle_maf = 0
handle_mas = 0
handle_ma1 = 0

def OnInit():
    global handle_ma1, handle_maf, handle_mas, period_maf, period_mas
    period_maf = (2 if (InpPeriodFast < 2) else InpPeriodFast)
    period_mas = (2 if (InpPeriodSlow < 2) else InpPeriodSlow)
    if period_mas == period_maf:
        period_mas = period_maf + 1
    SetIndexBuffer(0, BufferBogie, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMAF, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferMAS, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMA1, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Bogie(' + _str(period_maf) + ',' + _str(period_mas) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferBogie, True)
    ArraySetAsSeries(BufferMAF, True)
    ArraySetAsSeries(BufferMAS, True)
    ArraySetAsSeries(BufferMA1, True)
    ResetLastError()
    handle_maf = iMA(None, PERIOD_CURRENT, period_maf - 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_maf == INVALID_HANDLE:
        Print('The iMA(', _str(period_maf - 1), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_mas = iMA(None, PERIOD_CURRENT, period_mas - 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_mas == INVALID_HANDLE:
        Print('The iMA(', _str(period_mas - 1), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma1 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 3:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferBogie, EMPTY_VALUE)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferMAF, 0)
        ArrayInitialize(BufferMAS, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_maf, 0, 0, count, BufferMAF)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_mas, 0, 0, count, BufferMAS)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        left = BufferMAF[i + 1] * (period_maf - 1) * period_mas
        right = BufferMAS[i + 1] * (period_mas - 1) * period_maf
        bottom = period_maf - period_mas
        BogiePX = _fdiv(left - right, (bottom if (bottom != 0) else DBL_MIN))
        ma = BufferMA1[i]
        BufferBogie[i] = (_fdiv(BogiePX, (ma if (ma != 0) else DBL_MIN)) - 1) * 100
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BogieOsc(_MQL5Indicator):
    name = 'Bogie_Osc'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFast': 7,  # Fast MA period
        'InpPeriodSlow': 14,  # Slow MA period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

