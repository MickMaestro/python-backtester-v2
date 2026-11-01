"""Tick_Chart — converted from MQL5: MQL5 Indicators/Tick Chart/Tick_Chart.mq5

Copyright: Copyright © 2015, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.004

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.004', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Ask', 2: 'Bid'}, 'levels': [], 'description': [], 'name': 'Tick_Chart', 'source': 'MQL5 Indicators/Tick Chart/Tick_Chart.mq5', 'folder': 'Tick Chart', 'inputs': [{'mql': 'ticks', 'py': 'ticks', 'param': 'ticks', 'type': 'int', 'default': 400, 'label': 'amount requested by ticks', 'sinput': False}, {'mql': 'start', 'py': 'start', 'param': None, 'type': 'datetime', 'default': 1475805963, 'label': 'with a date query tics', 'sinput': False}, {'mql': 'millisecond', 'py': 'millisecond', 'param': 'millisecond', 'type': 'int', 'default': 200, 'label': 'timer', 'sinput': False}, {'mql': 'view', 'py': 'view', 'param': 'view', 'type': 'int', 'default': 300, 'label': 'see how many bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

COPY_TICKS_INFO = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
ExtAsk = Arr(0, 0.0)
ExtBid = Arr(0, 0.0)
first_start = False
copied = 0  # the size of the array of ticks
ticks = _input('ticks', 400)  # amount requested by ticks
start = _input('start', 1475805963)  # with a date query tics
millisecond = _input('millisecond', 200)  # timer
view = _input('view', 300)  # see how many bars

def OnInit():
    global first_start
    if view >= ticks:
        Print('Parameter "see how many bars" must be less than the parameter "amount requested by ticks"')
        return INIT_PARAMETERS_INCORRECT
    SetIndexBuffer(0, ExtAsk, INDICATOR_DATA)
    SetIndexBuffer(1, ExtBid, INDICATOR_DATA)
    ArraySetAsSeries(ExtAsk, True)
    ArraySetAsSeries(ExtBid, True)
    ArrayInitialize(ExtAsk, 0.0)
    ArrayInitialize(ExtBid, 0.0)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArrayFree(ExTicks)
    first_start = True
    EventSetMillisecondTimer(millisecond)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_server, copied, first_start
    Comment('Trader Server Name: ', _s_OnCalculate_server)
    if _s_OnCalculate_server != AccountInfoString(ACCOUNT_SERVER):
        first_start = True
    _s_OnCalculate_server = AccountInfoString(ACCOUNT_SERVER)
    if not first_start:
        return rates_total
    ResetLastError()
    copied = CopyTicks(Symbol(), ExTicks, COPY_TICKS_INFO, _ulong(start) * 1000, ticks)
    err = GetLastError()
    Comment('Booked: ', ticks, ', downloads: ', copied, ', error code: ', err)
    if err == 0:
        first_start = False
    return rates_total

def OnTimer():
    global _s_OnTimer_prev_count
    if first_start:
        return
    if (_s_OnTimer_prev_count + view) < copied:
        j = 0
        for i in range(_s_OnTimer_prev_count, _s_OnTimer_prev_count + view):
            ExtAsk[view - j] = ExTicks[i].ask
            ExtBid[view - j] = ExTicks[i].bid
            j += 1
        _s_OnTimer_prev_count += 1
        ChartRedraw()
    else:
        _s_OnTimer_prev_count = 0

def OnDeinit(reason):
    Comment('')

# ---- global variables initialised from expressions
ExTicks = Arr(0, 0, factory=MqlTick)

# ---- static local variables
_s_OnCalculate_server = ''
_s_OnTimer_prev_count = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TickChart(_MQL5Indicator):
    name = 'Tick_Chart'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ticks': 400,  # amount requested by ticks
        'millisecond': 200,  # timer
        'view': 300,  # see how many bars
    }

