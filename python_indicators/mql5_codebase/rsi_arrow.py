"""RSI_Arrow — converted from MQL5: MQL5 Indicators/RSI Arrow/RSI_Arrow.mq5

The indicator draws the \\"Arrow Up\\" object when
the RSI crosses up the \\"Level Up\\" level
and draws \\"Arrow Down\\" object when
the RSI crosses down the \\"Level Down\\" level
Copyright: Copyright © 2017, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.002

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.002', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'RSI Arrow UP', 2: 'RSI Arrow DOWN'}, 'levels': [], 'description': ['The indicator draws the \\"Arrow Up\\" object when', 'the RSI crosses up the \\"Level Up\\" level', 'and draws \\"Arrow Down\\" object when', 'the RSI crosses down the \\"Level Down\\" level'], 'name': 'RSI_Arrow', 'source': 'MQL5 Indicators/RSI Arrow/RSI_Arrow.mq5', 'folder': 'RSI Arrow', 'inputs': [{'mql': '_0_', 'py': '_0_', 'param': None, 'type': 'string', 'default': '*-*-*-*-*-*', 'label': 'Arrows parameters', 'sinput': True}, {'mql': 'InpLevelUP', 'py': 'InpLevelUP', 'param': 'InpLevelUP', 'type': 'double', 'default': 70.0, 'label': 'Level Up', 'sinput': False}, {'mql': 'InpCodeUP', 'py': 'InpCodeUP', 'param': 'InpCodeUP', 'type': 'ushort', 'default': 241, 'label': 'Symbol code Up', 'sinput': False}, {'mql': 'InpLevelDOWN', 'py': 'InpLevelDOWN', 'param': 'InpLevelDOWN', 'type': 'double', 'default': 30.0, 'label': 'Level Down', 'sinput': False}, {'mql': 'InpCodeDOWN', 'py': 'InpCodeDOWN', 'param': 'InpCodeDOWN', 'type': 'ushort', 'default': 242, 'label': 'Symbol code Down', 'sinput': False}, {'mql': '_1_', 'py': '_1_', 'param': None, 'type': 'string', 'default': '*-*-*-*-*-*', 'label': 'RSI parameters', 'sinput': True}, {'mql': 'ma_period', 'py': 'ma_period', 'param': 'ma_period', 'type': 'int', 'default': 14, 'label': 'period of averaging', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 1, 'label': 'type of price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
_0_ = _input('_0_', '*-*-*-*-*-*')  # Arrows parameters
InpLevelUP = _input('InpLevelUP', 70.0)  # Level Up
InpCodeUP = _input('InpCodeUP', 241)  # Symbol code Up
InpLevelDOWN = _input('InpLevelDOWN', 30.0)  # Level Down
InpCodeDOWN = _input('InpCodeDOWN', 242)  # Symbol code Down
_1_ = _input('_1_', '*-*-*-*-*-*')  # RSI parameters
ma_period = _input('ma_period', 14)  # period of averaging
applied_price = _input('applied_price', PRICE_CLOSE)  # type of price
ArrowsBufferUP = Arr(0, 0.0)
ArrowsBufferDOWN = Arr(0, 0.0)
iRSIBuffer = Arr(0, 0.0)
handle = 0
bars_calculated = 0

def OnInit():
    global handle
    SetIndexBuffer(0, ArrowsBufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, ArrowsBufferDOWN, INDICATOR_DATA)
    SetIndexBuffer(2, iRSIBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, InpCodeUP)
    PlotIndexSetInteger(1, PLOT_ARROW, InpCodeDOWN)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, -5)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, 5)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    handle = iRSI(Symbol(), Period(), ma_period, applied_price)
    if handle == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iRSI indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        return INIT_FAILED
    short_name = StringFormat('RSI Arrow(%s/%s, %d, %d)', Symbol(), EnumToString(Period(), ''), ma_period, applied_price)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    values_to_copy = 0
    calculated = BarsCalculated(handle)
    if calculated <= 0:
        PrintFormat('BarsCalculated() returned %d, error code %d', calculated, GetLastError())
        return 0
    limit = 0
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
        limit = rates_total - values_to_copy
    if not FillArrayFromBuffer(iRSIBuffer, handle, values_to_copy):
        return 0
    for i in range(limit, rates_total):
        if iRSIBuffer[i] > InpLevelUP:
            ArrowsBufferUP[i] = high[i]
        else:
            ArrowsBufferUP[i] = 0.0
        if iRSIBuffer[i] < InpLevelDOWN:
            ArrowsBufferDOWN[i] = low[i]
        else:
            ArrowsBufferDOWN[i] = 0.0
    bars_calculated = calculated
    return rates_total

def FillArrayFromBuffer(rsi_buffer, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, 0, amount, rsi_buffer) < 0:
        PrintFormat('Failed to copy data from the iRSI indicator, error code %d', GetLastError())
        return False
    return True

def OnDeinit(reason):
    Comment('')


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSIArrow(_MQL5Indicator):
    name = 'RSI_Arrow'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpLevelUP': 70.0,  # Level Up
        'InpCodeUP': 241,  # Symbol code Up
        'InpLevelDOWN': 30.0,  # Level Down
        'InpCodeDOWN': 242,  # Symbol code Down
        'ma_period': 14,  # period of averaging
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # type of price
    }

