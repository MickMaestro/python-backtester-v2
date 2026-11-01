"""Standard_Deviation_Moving_Average_Ratio — converted from MQL5: MQL5 Indicators/Standard_Deviation_Moving_Average_Ratio/Standard_Deviation_Moving_Average_Ratio.mq5

Standard Deviations/Moving Average Ratio indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [9408444]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Ratio'}, 'levels': [], 'description': ['Standard Deviations/Moving Average Ratio indicator'], 'name': 'Standard_Deviation_Moving_Average_Ratio', 'source': 'MQL5 Indicators/Standard_Deviation_Moving_Average_Ratio/Standard_Deviation_Moving_Average_Ratio.mq5', 'folder': 'Standard_Deviation_Moving_Average_Ratio', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferRatio = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferDev = Arr(0, 0.0)
period = 0
handle_dev = 0
handle_ma = 0

def OnInit():
    global handle_dev, handle_ma, period
    period = (2 if (InpPeriod < 2) else InpPeriod)
    SetIndexBuffer(0, BufferRatio, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDev, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'StdDev/MA Ratio (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferRatio, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferDev, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_dev = iStdDev(None, PERIOD_CURRENT, period, 0, MODE_SMA, InpAppliedPrice)
    if handle_dev == INVALID_HANDLE:
        Print('The iStdDev(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferRatio, EMPTY_VALUE)
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
        BufferRatio[i] = (_fdiv(BufferDev[i], BufferMA[i]) if (BufferMA[i] != 0) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StandardDeviationMovingAverageRatio(_MQL5Indicator):
    name = 'Standard_Deviation_Moving_Average_Ratio'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

