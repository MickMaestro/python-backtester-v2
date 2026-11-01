"""CAD — converted from MQL5: MQL5 Indicators/CAD/CAD.mq5

Consecutive Advance/Decline indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Advance', 2: 'Decline'}, 'levels': [], 'description': ['Consecutive Advance/Decline indicator'], 'name': 'CAD', 'source': 'MQL5 Indicators/CAD/CAD.mq5', 'folder': 'CAD', 'inputs': [{'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferAdvance = Arr(0, 0.0)
BufferDecline = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
handle_ma = 0

def OnInit():
    global handle_ma
    SetIndexBuffer(0, BufferAdvance, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDecline, INDICATOR_DATA)
    SetIndexBuffer(2, BufferMA, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Consecutive Advance/Decline')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(BufferAdvance, True)
    ArraySetAsSeries(BufferDecline, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferAdvance, EMPTY_VALUE)
        ArrayInitialize(BufferDecline, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        if i == (rates_total - 2):
            BufferDecline[i] = 0.0
            BufferAdvance[i] = BufferDecline[i]
        else:
            if BufferMA[i] > BufferMA[i + 1]:
                BufferAdvance[i] = BufferAdvance[i + 1] + 1
                BufferDecline[i] = 0.0
            else:
                if BufferMA[i] < BufferMA[i + 1]:
                    BufferDecline[i] = BufferDecline[i + 1] + 1
                    BufferAdvance[i] = 0.0
                else:
                    BufferDecline[i] = 0.0
                    BufferAdvance[i] = BufferDecline[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CAD(_MQL5Indicator):
    name = 'CAD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

