"""Resistance & Support — converted from MQL5: MQL5 Indicators/Resistance & Support/Resistance & Support.mq5

Resistance & Support
Copyright: Copyright © 2017, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.001

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.001', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [65280], 2: [16711935]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Resistance', 2: 'Support'}, 'levels': [], 'description': ['Resistance & Support'], 'name': 'Resistance & Support', 'source': 'MQL5 Indicators/Resistance & Support/Resistance & Support.mq5', 'folder': 'Resistance & Support', 'inputs': [{'mql': 'InpArrowCode', 'py': 'InpArrowCode', 'param': 'InpArrowCode', 'type': 'uchar', 'default': 159, 'label': "arrow code (Wingdings font's symbol codes)", 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpArrowCode = _input('InpArrowCode', 159)  # arrow code (Wingdings font's symbol codes)
ResistanceBuffer = Arr(0, 0.0)
SupportBuffer = Arr(0, 0.0)
FractalsUpBuffer = Arr(0, 0.0)
FractalsDownBuffer = Arr(0, 0.0)
handle_iFractals = 0  # variable for storing the handle of the iFractals indicator

def OnInit():
    global handle_iFractals
    SetIndexBuffer(0, ResistanceBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SupportBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, FractalsUpBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, FractalsDownBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, InpArrowCode)
    PlotIndexSetInteger(1, PLOT_ARROW, InpArrowCode)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, -5)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, 5)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    handle_iFractals = iFractals(Symbol(), Period())
    if handle_iFractals == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iFractals indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_fractals_down, _s_OnCalculate_prev_fractals_up
    if rates_total < 5:
        return 0
    calculated_Fractals = BarsCalculated(handle_iFractals)
    if calculated_Fractals != rates_total:
        return 0
    values_to_copy = -1
    if prev_calculated == 0:
        values_to_copy = rates_total
    else:
        values_to_copy = rates_total - prev_calculated + 5
    if not FillFractalsArraysFromBuffers(FractalsUpBuffer, FractalsDownBuffer, handle_iFractals, values_to_copy):
        return 0
    limit = (0 if (prev_calculated == 0) else (rates_total - prev_calculated - 5))
    limit = (0 if (limit < 0) else limit)
    for i in range(limit, rates_total):
        if FractalsUpBuffer[i] != EMPTY_VALUE:
            _s_OnCalculate_prev_fractals_up = FractalsUpBuffer[i]
        ResistanceBuffer[i] = _s_OnCalculate_prev_fractals_up
        if FractalsDownBuffer[i] != EMPTY_VALUE:
            _s_OnCalculate_prev_fractals_down = FractalsDownBuffer[i]
        SupportBuffer[i] = _s_OnCalculate_prev_fractals_down
    return rates_total

def FillFractalsArraysFromBuffers(up_arrows, down_arrows, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, 0, amount, up_arrows) < 0:
        PrintFormat('Failed to copy data from the iFractals indicator to the FractalUpBuffer array, error code %d', GetLastError())
        return False
    if CopyBuffer(ind_handle, 1, 0, amount, down_arrows) < 0:
        PrintFormat('Failed to copy data from the iFractals indicator to the FractalDownBuffer array, error code %d', GetLastError())
        return False
    return True

# ---- static local variables
_s_OnCalculate_prev_fractals_up = EMPTY_VALUE
_s_OnCalculate_prev_fractals_down = EMPTY_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ResistanceSupport(_MQL5Indicator):
    name = 'Resistance & Support'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpArrowCode': 159,  # arrow code (Wingdings font's symbol codes)
    }

