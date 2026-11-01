"""AMA Histogram — converted from MQL5: MQL5 Indicators/AMA Histogram/AMA Histogram.mq5

Copyright: Copyright © 2018, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.001

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.001', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 3}, 'colors': {1: [14822282]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'iAMA'}, 'levels': [], 'description': [], 'name': 'AMA Histogram', 'source': 'MQL5 Indicators/AMA Histogram/AMA Histogram.mq5', 'folder': 'AMA Histogram', 'inputs': [{'mql': 'ama_period', 'py': 'ama_period', 'param': 'ama_period', 'type': 'int', 'default': 15, 'label': 'period of calculation', 'sinput': False}, {'mql': 'fast_ma_period', 'py': 'fast_ma_period', 'param': 'fast_ma_period', 'type': 'int', 'default': 2, 'label': 'period of fast MA', 'sinput': False}, {'mql': 'slow_ma_period', 'py': 'slow_ma_period', 'param': 'slow_ma_period', 'type': 'int', 'default': 30, 'label': 'period of slow MA', 'sinput': False}, {'mql': 'ama_shift', 'py': 'ama_shift', 'param': 'ama_shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 1, 'label': 'type of price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ama_period = _input('ama_period', 15)  # period of calculation
fast_ma_period = _input('fast_ma_period', 2)  # period of fast MA
slow_ma_period = _input('slow_ma_period', 30)  # period of slow MA
ama_shift = _input('ama_shift', 0)  # horizontal shift
applied_price = _input('applied_price', PRICE_CLOSE)  # type of price
iAMABuffer = Arr(0, 0.0)
iAMABufferTemp = Arr(0, 0.0)
handle = 0
short_name = ""
bars_calculated = 0

def OnInit():
    global handle, name, short_name
    SetIndexBuffer(0, iAMABuffer, INDICATOR_DATA)
    SetIndexBuffer(1, iAMABufferTemp, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_SHIFT, ama_shift)
    name = Symbol()
    StringTrimRight(_GlobRef(globals(), 'name'))
    StringTrimLeft(_GlobRef(globals(), 'name'))
    if StringLen(name) == 0:
        name = Symbol()
    handle = iAMA(name, Period(), ama_period, fast_ma_period, slow_ma_period, ama_shift, applied_price)
    if handle == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iAMA indicator for the symbol %s/%s, error code %d', name, EnumToString(Period(), ''), GetLastError())
        return INIT_FAILED
    short_name = StringFormat('AMA Histogram (%d,%d,%d)', ama_period, fast_ma_period, slow_ma_period)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    values_to_copy = 0
    calculated = BarsCalculated(handle)
    if calculated <= 0:
        PrintFormat('BarsCalculated() returned %d, error code %d', calculated, GetLastError())
        return 0
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBuffer(iAMABufferTemp, ama_shift, handle, values_to_copy):
        return 0
    bars_calculated = calculated
    limit = prev_calculated - 1
    if limit < 0:
        limit = 0
    for i in range(limit, rates_total):
        iAMABuffer[i] = close[i] - iAMABufferTemp[i]
    return rates_total

def FillArrayFromBuffer(ama_buffer, a_shift, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, -a_shift, amount, ama_buffer) < 0:
        PrintFormat('Failed to copy data from the iAMA indicator, error code %d', GetLastError())
        return False
    return True

# ---- global variables initialised from expressions
name = Symbol()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AMAHistogram(_MQL5Indicator):
    name = 'AMA Histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ama_period': 15,  # period of calculation
        'fast_ma_period': 2,  # period of fast MA
        'slow_ma_period': 30,  # period of slow MA
        'ama_shift': 0,  # horizontal shift
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # type of price
    }

