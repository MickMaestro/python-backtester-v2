"""Alligator_With_VAMA — converted from MQL5: MQL5 Indicators/VAMA based Alligator/Alligator_With_VAMA.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16711680], 2: [255], 3: [65280]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Jaws', 2: 'Teeth', 3: 'Lips'}, 'levels': [], 'description': [], 'name': 'Alligator_With_VAMA', 'source': 'MQL5 Indicators/VAMA based Alligator/Alligator_With_VAMA.mq5', 'folder': 'VAMA based Alligator', 'inputs': [{'mql': 'InpPeriodJaws', 'py': 'InpPeriodJaws', 'param': 'InpPeriodJaws', 'type': 'uint', 'default': 13, 'label': 'Period of Jaws line', 'sinput': False}, {'mql': 'InpShiftJaws', 'py': 'InpShiftJaws', 'param': 'InpShiftJaws', 'type': 'int', 'default': 8, 'label': 'Shift of Jaws line', 'sinput': False}, {'mql': 'InpPeriodTeeth', 'py': 'InpPeriodTeeth', 'param': 'InpPeriodTeeth', 'type': 'uint', 'default': 8, 'label': 'Period of Teeth line', 'sinput': False}, {'mql': 'InpShiftTeeth', 'py': 'InpShiftTeeth', 'param': 'InpShiftTeeth', 'type': 'int', 'default': 5, 'label': 'Shift of Teeth line', 'sinput': False}, {'mql': 'InpPeriodLips', 'py': 'InpPeriodLips', 'param': 'InpPeriodLips', 'type': 'uint', 'default': 5, 'label': 'Period of Lips line', 'sinput': False}, {'mql': 'InpShiftLips', 'py': 'InpShiftLips', 'param': 'InpShiftLips', 'type': 'int', 'default': 3, 'label': 'Shift of Lips line', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodJaws = _input('InpPeriodJaws', 13)  # Period of Jaws line
InpShiftJaws = _input('InpShiftJaws', 8)  # Shift of Jaws line
InpPeriodTeeth = _input('InpPeriodTeeth', 8)  # Period of Teeth line
InpShiftTeeth = _input('InpShiftTeeth', 5)  # Shift of Teeth line
InpPeriodLips = _input('InpPeriodLips', 5)  # Period of Lips line
InpShiftLips = _input('InpShiftLips', 3)  # Shift of Lips line
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferJaws = Arr(0, 0.0)
BufferTeeth = Arr(0, 0.0)
BufferLips = Arr(0, 0.0)
period_jaws = 0
period_teeth = 0
period_lips = 0
handle_jaws = 0
handle_teeth = 0
handle_lips = 0
bars_minimum = 0

def OnInit():
    global bars_minimum, handle_jaws, handle_lips, handle_teeth, period_jaws, period_lips, period_teeth
    period_jaws = (1 if (InpPeriodJaws < 1) else InpPeriodJaws)
    period_teeth = (1 if (InpPeriodTeeth < 1) else InpPeriodTeeth)
    period_lips = (1 if (InpPeriodLips < 1) else InpPeriodLips)
    SetIndexBuffer(0, BufferJaws, INDICATOR_DATA)
    SetIndexBuffer(1, BufferTeeth, INDICATOR_DATA)
    SetIndexBuffer(2, BufferLips, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Alligator with VAMA')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, period_jaws - 1)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, period_teeth - 1)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, period_lips - 1)
    PlotIndexSetInteger(0, PLOT_SHIFT, InpShiftJaws)
    PlotIndexSetInteger(1, PLOT_SHIFT, InpShiftTeeth)
    PlotIndexSetInteger(2, PLOT_SHIFT, InpShiftLips)
    PlotIndexSetString(0, PLOT_LABEL, 'Jaws(' + _str(period_jaws) + ')')
    PlotIndexSetString(1, PLOT_LABEL, 'Teeth(' + _str(period_teeth) + ')')
    PlotIndexSetString(2, PLOT_LABEL, 'Lips(' + _str(period_lips) + ')')
    ArraySetAsSeries(BufferJaws, True)
    ArraySetAsSeries(BufferTeeth, True)
    ArraySetAsSeries(BufferLips, True)
    ResetLastError()
    handle_jaws = iCustom(Symbol(), PERIOD_CURRENT, 'VAMA', period_jaws, InpAppliedPrice)
    if handle_jaws == INVALID_HANDLE:
        Print('Error creating VAMA indicator handle for Javs line: ', GetLastError())
    ResetLastError()
    handle_teeth = iCustom(Symbol(), PERIOD_CURRENT, 'VAMA', period_teeth, InpAppliedPrice)
    if handle_jaws == INVALID_HANDLE:
        Print('Error creating VAMA indicator handle for Teeth line: ', GetLastError())
    ResetLastError()
    handle_lips = iCustom(Symbol(), PERIOD_CURRENT, 'VAMA', period_lips, InpAppliedPrice)
    if handle_jaws == INVALID_HANDLE:
        Print('Error creating VAMA indicator handle for Lips line: ', GetLastError())
    bars_minimum = period_jaws + InpShiftJaws
    if bars_minimum < (period_teeth + InpShiftTeeth):
        bars_minimum = period_teeth + InpShiftTeeth
    if bars_minimum < (period_lips * 2):
        bars_minimum = period_lips * 2
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < bars_minimum:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferJaws, EMPTY_VALUE)
        ArrayInitialize(BufferTeeth, EMPTY_VALUE)
        ArrayInitialize(BufferLips, EMPTY_VALUE)
    copied = (rates_total if (limit > 1) else 1)
    copied_jaws = CopyBuffer(handle_jaws, 0, 0, copied, BufferJaws)
    if copied_jaws != copied:
        return 0
    copied_teeth = CopyBuffer(handle_teeth, 0, 0, copied, BufferTeeth)
    if copied_teeth != copied:
        return 0
    copied_lips = CopyBuffer(handle_lips, 0, 0, copied, BufferLips)
    if copied_lips != copied:
        return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AlligatorWithVAMA(_MQL5Indicator):
    name = 'Alligator_With_VAMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodJaws': 13,  # Period of Jaws line
        'InpShiftJaws': 8,  # Shift of Jaws line
        'InpPeriodTeeth': 8,  # Period of Teeth line
        'InpShiftTeeth': 5,  # Shift of Teeth line
        'InpPeriodLips': 5,  # Period of Lips line
        'InpShiftLips': 3,  # Shift of Lips line
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

