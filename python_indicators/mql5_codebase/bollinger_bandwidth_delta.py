"""Bollinger_Bandwidth_Delta — converted from MQL5: MQL5 Indicators/Bollinger_Bandwidth_Delta/Bollinger_Bandwidth_Delta.mq5

Bollinger Bandwidth Delta oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255, 11119017]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'BBD'}, 'levels': [], 'description': ['Bollinger Bandwidth Delta oscillator'], 'name': 'Bollinger_Bandwidth_Delta', 'source': 'MQL5 Indicators/Bollinger_Bandwidth_Delta/Bollinger_Bandwidth_Delta.mq5', 'folder': 'Bollinger_Bandwidth_Delta', 'inputs': [{'mql': 'InpPeriodBB', 'py': 'InpPeriodBB', 'param': 'InpPeriodBB', 'type': 'uint', 'default': 20, 'label': 'BB period', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 2.0, 'label': 'BB deviation', 'sinput': False}, {'mql': 'InpPeriodDelta', 'py': 'InpPeriodDelta', 'param': 'InpPeriodDelta', 'type': 'uint', 'default': 20, 'label': 'Delta period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpPercent', 'py': 'InpPercent', 'param': 'InpPercent', 'type': 'int', 'default': 0, 'label': 'Show data in percentage', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodBB = _input('InpPeriodBB', 20)  # BB period
InpDeviation = _input('InpDeviation', 2.0)  # BB deviation
InpPeriodDelta = _input('InpPeriodDelta', 20)  # Delta period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpPercent = _input('InpPercent', INPUT_NO)  # Show data in percentage
BufferBBD = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferWidth = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferDev = Arr(0, 0.0)
deviation = 0.0
period_bb = 0
delta = 0
handle_ma = 0
handle_dev = 0

def OnInit():
    global delta, deviation, handle_dev, handle_ma, period_bb
    period_bb = (1 if (InpPeriodBB < 1) else InpPeriodBB)
    delta = (1 if (InpPeriodDelta < 1) else InpPeriodDelta)
    deviation = InpDeviation
    SetIndexBuffer(0, BufferBBD, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferWidth, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferDev, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BB width delta (' + _str(period_bb) + ',' + DoubleToString(deviation, 2) + _str(delta) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(BufferBBD, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferWidth, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferDev, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_bb, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_bb), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_dev = iStdDev(None, PERIOD_CURRENT, period_bb, 0, MODE_SMA, InpAppliedPrice)
    if handle_dev == INVALID_HANDLE:
        Print('The iStdDev(', _str(period_bb), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(delta, 4) or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - delta - 2
        ArrayInitialize(BufferBBD, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferWidth, 0)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferDev, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_dev, 0, 0, count, BufferDev)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        if BufferMA[i] != 0:
            BufferWidth[i] = _fdiv(2 * deviation * BufferDev[i], BufferMA[i])
            if InpPercent:
                BufferBBD[i] = (_setitem(BufferBBD, i, _fdiv(100.0 * (BufferWidth[i] - BufferWidth[i + delta - 1]), BufferWidth[i + delta - 1])) if (BufferWidth[i + delta - 1] != 0) else 0)
            else:
                BufferBBD[i] = _fdiv(BufferWidth[i] - BufferWidth[i + delta - 1], Point())
        else:
            BufferBBD[i] = 0.0
        BufferColors[i] = (0 if (BufferBBD[i] > BufferBBD[i + 1]) else 1 if (BufferBBD[i] < BufferBBD[i + 1]) else 2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BollingerBandwidthDelta(_MQL5Indicator):
    name = 'Bollinger_Bandwidth_Delta'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodBB': 20,  # BB period
        'InpDeviation': 2.0,  # BB deviation
        'InpPeriodDelta': 20,  # Delta period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpPercent': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Show data in percentage
    }

