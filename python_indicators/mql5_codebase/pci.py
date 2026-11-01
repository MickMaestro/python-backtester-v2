"""PCI — converted from MQL5: MQL5 Indicators/PCI/PCI.mq5

Phase Change Index indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_minimum': 0.0, 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 10, 2: 3, 3: 1}, 'colors': {1: [32768, 255], 2: [14599344], 3: [12632256]}, 'widths': {1: 1, 2: 2, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Histogram', 2: 'H3', 3: 'PCI'}, 'levels': [], 'description': ['Phase Change Index indicator'], 'name': 'PCI', 'source': 'MQL5 Indicators/PCI/PCI.mq5', 'folder': 'PCI', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 34, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 80.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 20.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 34)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpOverbought = _input('InpOverbought', 80.0)  # Overbought
InpOversold = _input('InpOversold', 20.0)  # Oversold
BufferH1 = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferH3 = Arr(0, 0.0)
BufferPCI = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period = 0
handle_ma = 0

def OnInit():
    global handle_ma, overbought, oversold, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    oversold = (0 if (InpOversold < 0) else 99.9 if (InpOversold > 99.9) else InpOversold)
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    if overbought <= oversold:
        overbought = oversold + 0.1
    if oversold >= overbought:
        oversold = overbought - 0.1
    SetIndexBuffer(0, BufferH1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferH3, INDICATOR_DATA)
    SetIndexBuffer(3, BufferPCI, INDICATOR_DATA)
    SetIndexBuffer(4, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferSignal, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Phase Change Index (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_SOLID)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_SOLID)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_SOLID)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, oversold)
    ArraySetAsSeries(BufferPCI, True)
    ArraySetAsSeries(BufferH3, True)
    ArraySetAsSeries(BufferH1, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferSignal, True)
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
        limit = rates_total - period - 1
        ArrayInitialize(BufferH1, EMPTY_VALUE)
        ArrayInitialize(BufferH3, EMPTY_VALUE)
        ArrayInitialize(BufferPCI, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferSignal, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        Momentum = _fdiv(BufferMA[i] - BufferMA[i + period - 1], period)
        Up = 0.0
        Dn = 0.0
        for j in range(0, period + 1):
            Gradient = BufferMA[i + period] + (Momentum * j)
            if (BufferMA[i + period - j] - Gradient) > 0.0:
                Up += fabs(BufferMA[i + period - j] - Gradient)
            elif (BufferMA[i + period - j] - Gradient) < 0.0:
                Dn += fabs(BufferMA[i + period - j] - Gradient)
        BufferPCI[i] = (_fdiv(100.0 * Up, Up + Dn) if ((Up + Dn) != 0) else 0)
        if Momentum > 0:
            if BufferPCI[i] < oversold:
                BufferSignal[i] = 1.0
            else:
                BufferSignal[i] = BufferSignal[i + 1]
        else:
            if BufferPCI[i] > overbought:
                BufferSignal[i] = -1.0
            else:
                BufferSignal[i] = BufferSignal[i + 1]
        if BufferSignal[i] == 1:
            if BufferPCI[i] > 50:
                BufferH1[i] = BufferPCI[i]
                BufferH3[i] = 50.0
            else:
                BufferH1[i] = 50.0
                BufferH3[i] = BufferPCI[i]
            BufferColors[i] = 0.0
        else:
            if BufferSignal[i] == -1:
                if BufferPCI[i] > 50:
                    BufferH1[i] = BufferPCI[i]
                    BufferH3[i] = 50.0
                    BufferColors[i] = 1.0
                else:
                    BufferH1[i] = 50.0
                    BufferH3[i] = BufferPCI[i]
                BufferColors[i] = 1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PCI(_MQL5Indicator):
    name = 'PCI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 34,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpOverbought': 80.0,  # Overbought
        'InpOversold': 20.0,  # Oversold
    }

