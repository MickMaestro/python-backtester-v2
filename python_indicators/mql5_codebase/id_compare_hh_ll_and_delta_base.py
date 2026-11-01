"""ID Compare HH LL and delta base — converted from MQL5: MQL5 Indicators/ID Compare HH LL and delta base/ID Compare HH LL and delta base.mq5

Copyright: Dina Paches; Link: https://dipaches.blogspot.com; Version: 1.098

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Dina Paches', 'link': 'https://dipaches.blogspot.com', 'version': '1.098', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 10, 2: 10}, 'colors': {1: [5197615, 9498256, 9639167, 55295], 2: [9498256, 5197615, 55295, 9639167]}, 'widths': {1: 5, 2: 5}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'High High delta', 2: 'Low Low delta'}, 'levels': [], 'description': [], 'name': 'ID Compare HH LL and delta base', 'source': 'MQL5 Indicators/ID Compare HH LL and delta base/ID Compare HH LL and delta base.mq5', 'folder': 'ID Compare HH LL and delta base', 'inputs': [{'mql': 'i_delta_base', 'py': 'i_delta_base', 'param': 'i_delta_base', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'i_bars', 'py': 'i_bars', 'param': 'i_bars', 'type': 'uint', 'default': 1000, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
i_delta_base = _input('i_delta_base', 5)
i_bars = _input('i_bars', 1000)
gp_delta_base = 0.0
buff_0 = Arr(0, 0.0)
buff_0_clr = Arr(0, 0.0)
buff_1 = Arr(0, 0.0)
buff_1_clr = Arr(0, 0.0)
gp_bars = 0
gp_digits = 0
gp_symbol = ""
gp_period = 0

def OnInit():
    global gp_bars, gp_delta_base, gp_digits, gp_period, gp_symbol
    gp_bars = (1 if (i_bars < 1) else _int(i_bars))
    gp_symbol = Symbol()
    gp_period = Period()
    gp_digits = Digits()
    gp_delta_base = i_delta_base * Point()
    IndicatorSetString(INDICATOR_SHORTNAME, 'ID Compare HH LL (delta base = ' + IntegerToString(i_delta_base) + ' points; bars = ' + IntegerToString(gp_bars) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, gp_digits)
    SetIndexBuffer(0, buff_0, INDICATOR_DATA)
    SetIndexBuffer(1, buff_0_clr, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, buff_1, INDICATOR_DATA)
    SetIndexBuffer(3, buff_1_clr, INDICATOR_COLOR_INDEX)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    BuffSetAsSerios()
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_sp_continue, _s_OnCalculate_sp_limit
    if prev_calculated == 0:
        _s_OnCalculate_sp_limit = MathMin(rates_total - 2, gp_bars + 2) - 1
        if _s_OnCalculate_sp_limit < (1 + 2):
            return 0
        BuffInitializeAndSetAsSerios()
        _s_OnCalculate_sp_continue = True
    elif (rates_total - prev_calculated) == 1:
        _s_OnCalculate_sp_limit = 1 + 2
        _s_OnCalculate_sp_continue = True
    if _s_OnCalculate_sp_continue:
        _s_OnCalculate_sp_continue = ActionsHighHigh(_s_OnCalculate_sp_limit)
        if not _s_OnCalculate_sp_continue:
            return 0
        _s_OnCalculate_sp_continue = ActionsLowLow(_s_OnCalculate_sp_limit)
        if not _s_OnCalculate_sp_continue:
            return 0
        buff_0[0] = EMPTY_VALUE
        buff_1[0] = EMPTY_VALUE
        _s_OnCalculate_sp_continue = False
    return rates_total

def BuffSetAsSerios():
    ArraySetAsSeries(buff_0, True)
    ArraySetAsSeries(buff_0_clr, True)
    ArraySetAsSeries(buff_1, True)
    ArraySetAsSeries(buff_1_clr, True)
    return

def BuffInitializeAndSetAsSerios():
    ArrayInitialize(buff_0, EMPTY_VALUE)
    ArrayInitialize(buff_1, EMPTY_VALUE)
    BuffSetAsSerios()

def ActionsHighHigh(limit):
    ArrayResizeAndSetAsSeries(_s_ActionsHighHigh_high_arr, limit, True)
    if not CopyHighArr(limit, _s_ActionsHighHigh_high_arr):
        return False
    delta = 0.0
    for i in range(1, limit - 1):
        delta = _s_ActionsHighHigh_high_arr[i] - _s_ActionsHighHigh_high_arr[i + 1]
        ActionsHighDeltaAndDeltaBase(delta, i)
    ArrayFree(_s_ActionsHighHigh_high_arr)
    return True

def ActionsLowLow(limit):
    ArrayResizeAndSetAsSeries(_s_ActionsLowLow_low_arr, limit, True)
    if not CopyLowArr(limit, _s_ActionsLowLow_low_arr):
        return False
    delta = 0.0
    for i in range(1, limit - 1):
        delta = _s_ActionsLowLow_low_arr[i] - _s_ActionsLowLow_low_arr[i + 1]
        ActionsLowDeltaAndDeltaBase(delta, i)
    ArrayFree(_s_ActionsLowLow_low_arr)
    return True

def ArrayResizeAndSetAsSeries(array, new_size, flag):
    ArrayResize(array, new_size, new_size)
    ArraySetAsSeries(array, flag)

def CopyHighArr(size, array):
    copied = CopyHigh(gp_symbol, gp_period, 0, size, array)
    if copied < size:
        Print('Error CopyHigh')
        return False
    return True

def CopyLowArr(size, array):
    copied = CopyLow(gp_symbol, gp_period, 0, size, array)
    if copied < size:
        Print('Error CopyLow')
        return False
    return True

def ActionsHighDeltaAndDeltaBase(delta, index, clr_index=0):
    if delta < 0:
        delta *= -1
        clr_index = 1
    if NormalizeDouble(delta - gp_delta_base, gp_digits) < 0:
        clr_index = (2 if (clr_index == 0) else 3)
    buff_0[index] = delta
    buff_0_clr[index] = clr_index

def ActionsLowDeltaAndDeltaBase(delta, index, clr_index=0):
    if delta > 0:
        delta *= -1
        clr_index = 1
    if NormalizeDouble(delta + gp_delta_base, gp_digits) > 0:
        clr_index = (2 if (clr_index == 0) else 3)
    buff_1[index] = delta
    buff_1_clr[index] = clr_index

# ---- static local variables
_s_OnCalculate_sp_limit = 0
_s_OnCalculate_sp_continue = False
_s_ActionsHighHigh_high_arr = Arr(0, 0.0)
_s_ActionsLowLow_low_arr = Arr(0, 0.0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IDCompareHHLLAndDeltaBase(_MQL5Indicator):
    name = 'ID Compare HH LL and delta base'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'i_delta_base': 5,
        'i_bars': 1000,
    }

