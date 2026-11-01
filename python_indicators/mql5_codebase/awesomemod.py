"""AwesomeMod — converted from MQL5: MQL5 Indicators/AwesomeMod/AwesomeMod.mq5

Awesome Modified oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 2}, 'types': {1: 10, 2: 10}, 'colors': {1: [16711680, 255], 2: [32768, 36095]}, 'widths': {1: 1, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Slow AO', 2: 'Fast AO'}, 'levels': [], 'description': ['Awesome Modified oscillator'], 'name': 'AwesomeMod', 'source': 'MQL5 Indicators/AwesomeMod/AwesomeMod.mq5', 'folder': 'AwesomeMod', 'inputs': [{'mql': 'InpPeriodFastEMA', 'py': 'InpPeriodFastEMA', 'param': 'InpPeriodFastEMA', 'type': 'uint', 'default': 18, 'label': 'Fast EMA period', 'sinput': False}, {'mql': 'InpPeriodMediumEMA', 'py': 'InpPeriodMediumEMA', 'param': 'InpPeriodMediumEMA', 'type': 'uint', 'default': 40, 'label': 'Medium EMA period', 'sinput': False}, {'mql': 'InpPeriodSlowEMA', 'py': 'InpPeriodSlowEMA', 'param': 'InpPeriodSlowEMA', 'type': 'uint', 'default': 200, 'label': 'Slow EMA period', 'sinput': False}, {'mql': 'InpPeriodFastAO', 'py': 'InpPeriodFastAO', 'param': 'InpPeriodFastAO', 'type': 'uint', 'default': 12, 'label': 'AO. Fast MA period', 'sinput': False}, {'mql': 'InpPeriodSlowAO', 'py': 'InpPeriodSlowAO', 'param': 'InpPeriodSlowAO', 'type': 'uint', 'default': 18, 'label': 'AO. Slow MA period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodFastEMA = _input('InpPeriodFastEMA', 18)  # Fast EMA period
InpPeriodMediumEMA = _input('InpPeriodMediumEMA', 40)  # Medium EMA period
InpPeriodSlowEMA = _input('InpPeriodSlowEMA', 200)  # Slow EMA period
InpPeriodFastAO = _input('InpPeriodFastAO', 12)  # AO. Fast MA period
InpPeriodSlowAO = _input('InpPeriodSlowAO', 18)  # AO. Slow MA period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferSAO = Arr(0, 0.0)
BufferSAOColors = Arr(0, 0.0)
BufferFAO = Arr(0, 0.0)
BufferFAOColors = Arr(0, 0.0)
BufferFEMA = Arr(0, 0.0)
BufferMEMA = Arr(0, 0.0)
BufferSEMA = Arr(0, 0.0)
BufferSAOTMP = Arr(0, 0.0)
BufferFAOTMP = Arr(0, 0.0)
period_fema = 0
period_mema = 0
period_sema = 0
period_fao = 0
period_sao = 0
handle_fma = 0
handle_mma = 0
handle_sma = 0

def OnInit():
    global handle_fma, handle_mma, handle_sma, period_fao, period_fema, period_mema, period_sao, period_sema
    period_fema = (1 if (InpPeriodFastEMA < 1) else InpPeriodFastEMA)
    period_mema = (1 if (InpPeriodMediumEMA < 1) else InpPeriodMediumEMA)
    period_sema = (1 if (InpPeriodSlowEMA < 1) else InpPeriodSlowEMA)
    period_fao = (2 if (InpPeriodFastAO < 2) else InpPeriodFastAO)
    period_sao = (2 if (InpPeriodSlowAO < 2) else InpPeriodSlowAO)
    SetIndexBuffer(0, BufferSAO, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSAOColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferFAO, INDICATOR_DATA)
    SetIndexBuffer(3, BufferFAOColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, BufferFEMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMEMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferSEMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferSAOTMP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferFAOTMP, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'AOModOSC(' + _str(period_fema) + ',' + _str(period_mema) + ',' + _str(period_sema) + ',' + _str(period_fao) + ',' + _str(period_sao) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferSAO, True)
    ArraySetAsSeries(BufferSAOColors, True)
    ArraySetAsSeries(BufferFAO, True)
    ArraySetAsSeries(BufferFAOColors, True)
    ArraySetAsSeries(BufferFEMA, True)
    ArraySetAsSeries(BufferMEMA, True)
    ArraySetAsSeries(BufferSEMA, True)
    ArraySetAsSeries(BufferSAOTMP, True)
    ArraySetAsSeries(BufferFAOTMP, True)
    ResetLastError()
    handle_fma = iMA(None, PERIOD_CURRENT, period_fema, 0, MODE_EMA, InpAppliedPrice)
    if handle_fma == INVALID_HANDLE:
        Print('The Fast iMA(', _str(period_fema), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_mma = iMA(None, PERIOD_CURRENT, period_mema, 0, MODE_EMA, InpAppliedPrice)
    if handle_mma == INVALID_HANDLE:
        Print('The Medium iMA(', _str(period_mema), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sma = iMA(None, PERIOD_CURRENT, period_sema, 0, MODE_EMA, InpAppliedPrice)
    if handle_sma == INVALID_HANDLE:
        Print('The Slow iMA(', _str(period_sema), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    ArraySetAsSeries(low, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferSAO, EMPTY_VALUE)
        ArrayInitialize(BufferFAO, EMPTY_VALUE)
        ArrayInitialize(BufferFEMA, 0)
        ArrayInitialize(BufferMEMA, 0)
        ArrayInitialize(BufferSEMA, 0)
        ArrayInitialize(BufferSAOTMP, 0)
        ArrayInitialize(BufferFAOTMP, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_fma, 0, 0, count, BufferFEMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_mma, 0, 0, count, BufferMEMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sma, 0, 0, count, BufferSEMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferFAOTMP[i] = ((100.0 * (_fdiv(BufferFEMA[i], BufferMEMA[i]) - 1.0)) if (BufferMEMA[i] != 0) else 0)
        BufferSAOTMP[i] = ((100.0 * (_fdiv(BufferMEMA[i], BufferSEMA[i]) - 1.0)) if (BufferSEMA[i] != 0) else 0)
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sao, BufferSAOTMP, BufferSAO)
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_fao, BufferFAOTMP, BufferFAO)
    for i in range(limit, 0 - 1, -1):
        BufferSAOColors[i] = (0 if (BufferSAO[i + 1] < BufferSAO[i]) else 1)
        BufferFAOColors[i] = (0 if (BufferFAO[i + 1] < BufferFAO[i]) else 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AwesomeMod(_MQL5Indicator):
    name = 'AwesomeMod'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFastEMA': 18,  # Fast EMA period
        'InpPeriodMediumEMA': 40,  # Medium EMA period
        'InpPeriodSlowEMA': 200,  # Slow EMA period
        'InpPeriodFastAO': 12,  # AO. Fast MA period
        'InpPeriodSlowAO': 18,  # AO. Slow MA period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

