"""EMA_Trend — converted from MQL5: MQL5 Indicators/EMA_Trend/EMA_Trend.mq5

MA Trend indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [16711680], 2: [16748574], 3: [255], 4: [42495]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Fast MA High', 2: 'Fast MA Low', 3: 'Slow MA High', 4: 'Slow MA Low'}, 'levels': [], 'description': ['MA Trend indicator'], 'name': 'EMA_Trend', 'source': 'MQL5 Indicators/EMA_Trend/EMA_Trend.mq5', 'folder': 'EMA_Trend', 'inputs': [{'mql': 'InpPeriodFastMA', 'py': 'InpPeriodFastMA', 'param': 'InpPeriodFastMA', 'type': 'uint', 'default': 21, 'label': 'Fast MA period', 'sinput': False}, {'mql': 'InpMethodFastMA', 'py': 'InpMethodFastMA', 'param': 'InpMethodFastMA', 'type': 'int', 'default': 1, 'label': 'Fast MA method', 'sinput': False}, {'mql': 'InpPeriodSlowMA', 'py': 'InpPeriodSlowMA', 'param': 'InpPeriodSlowMA', 'type': 'uint', 'default': 34, 'label': 'Slow MA period', 'sinput': False}, {'mql': 'InpMethodSlowMA', 'py': 'InpMethodSlowMA', 'param': 'InpMethodSlowMA', 'type': 'int', 'default': 1, 'label': 'Slow MA method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodFastMA = _input('InpPeriodFastMA', 21)  # Fast MA period
InpMethodFastMA = _input('InpMethodFastMA', MODE_EMA)  # Fast MA method
InpPeriodSlowMA = _input('InpPeriodSlowMA', 34)  # Slow MA period
InpMethodSlowMA = _input('InpMethodSlowMA', MODE_EMA)  # Slow MA method
BufferFH = Arr(0, 0.0)
BufferFL = Arr(0, 0.0)
BufferSH = Arr(0, 0.0)
BufferSL = Arr(0, 0.0)
period_fma = 0
period_sma = 0
handle_fhma = 0
handle_flma = 0
handle_shma = 0
handle_slma = 0

def OnInit():
    global handle_fhma, handle_flma, handle_shma, handle_slma, period_fma, period_sma
    period_fma = (1 if (InpPeriodFastMA < 1) else InpPeriodFastMA)
    period_sma = (1 if (InpPeriodSlowMA < 1) else InpPeriodSlowMA)
    SetIndexBuffer(0, BufferFH, INDICATOR_DATA)
    SetIndexBuffer(1, BufferFL, INDICATOR_DATA)
    SetIndexBuffer(2, BufferSH, INDICATOR_DATA)
    SetIndexBuffer(3, BufferSL, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MA Trend (' + _str(period_fma) + ',' + _str(period_sma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferFH, True)
    ArraySetAsSeries(BufferFL, True)
    ArraySetAsSeries(BufferSH, True)
    ArraySetAsSeries(BufferSL, True)
    ResetLastError()
    handle_fhma = iMA(None, PERIOD_CURRENT, period_fma, 0, InpMethodFastMA, PRICE_HIGH)
    if handle_fhma == INVALID_HANDLE:
        Print(80, ': The iMA(', _str(period_fma), ') by PRICE_HIGH object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_flma = iMA(None, PERIOD_CURRENT, period_fma, 0, InpMethodFastMA, PRICE_LOW)
    if handle_flma == INVALID_HANDLE:
        Print(86, ': The iMA(', _str(period_fma), ') by PRICE_LOW object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_shma = iMA(None, PERIOD_CURRENT, period_sma, 0, InpMethodSlowMA, PRICE_HIGH)
    if handle_shma == INVALID_HANDLE:
        Print(92, ': The iMA(', _str(period_sma), ') by PRICE_HIGH object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_slma = iMA(None, PERIOD_CURRENT, period_sma, 0, InpMethodSlowMA, PRICE_LOW)
    if handle_slma == INVALID_HANDLE:
        Print(98, ': The iMA(', _str(period_sma), ') by PRICE_LOW object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferFH, EMPTY_VALUE)
        ArrayInitialize(BufferFL, EMPTY_VALUE)
        ArrayInitialize(BufferSH, EMPTY_VALUE)
        ArrayInitialize(BufferSL, EMPTY_VALUE)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_fhma, 0, 0, count, BufferFH)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_flma, 0, 0, count, BufferFL)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_shma, 0, 0, count, BufferSH)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_slma, 0, 0, count, BufferSL)
    if copied != count:
        return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EMATrend(_MQL5Indicator):
    name = 'EMA_Trend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFastMA': 21,  # Fast MA period
        'InpMethodFastMA': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Fast MA method
        'InpPeriodSlowMA': 34,  # Slow MA period
        'InpMethodSlowMA': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Slow MA method
    }

