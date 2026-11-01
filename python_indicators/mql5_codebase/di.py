"""DI — converted from MQL5: MQL5 Indicators/DI/DI.mq5

Damping index indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [2237106]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Damping IDX'}, 'levels': [], 'description': ['Damping index indicator'], 'name': 'DI', 'source': 'MQL5 Indicators/DI/DI.mq5', 'folder': 'DI', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 5, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpLevDmp', 'py': 'InpLevDmp', 'param': 'InpLevDmp', 'type': 'double', 'default': 1.0, 'label': 'Damping level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 5)  # Period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpLevDmp = _input('InpLevDmp', 1.0)  # Damping level
BufferDI = Arr(0, 0.0)
BufferMAH = Arr(0, 0.0)
BufferMAL = Arr(0, 0.0)
damping_level = 0.0
period = 0
handle_maH = 0
handle_maL = 0

def OnInit():
    global damping_level, handle_maH, handle_maL, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    damping_level = (0 if (InpLevDmp < 0) else InpLevDmp)
    SetIndexBuffer(0, BufferDI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMAH, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferMAL, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Damping index (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, damping_level)
    ArraySetAsSeries(BufferDI, True)
    ArraySetAsSeries(BufferMAH, True)
    ArraySetAsSeries(BufferMAL, True)
    ResetLastError()
    handle_maH = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, PRICE_HIGH)
    if handle_maH == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by PRICE_HIGH object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_maL = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, PRICE_LOW)
    if handle_maL == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by PRICE_LOW object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferDI, EMPTY_VALUE)
        ArrayInitialize(BufferMAH, 0)
        ArrayInitialize(BufferMAL, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_maH, 0, 0, count, BufferMAH)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_maL, 0, 0, count, BufferMAL)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        R = BufferMAH[i + period] - BufferMAL[i + period]
        BufferDI[i] = _fdiv(BufferMAH[i] - BufferMAL[i], (R if (R != 0) else 1.0))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DI(_MQL5Indicator):
    name = 'DI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 5,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpLevDmp': 1.0,  # Damping level
    }

