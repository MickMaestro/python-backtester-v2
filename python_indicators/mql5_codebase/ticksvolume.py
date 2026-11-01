"""TicksVolume — converted from MQL5: MQL5 Indicators/TicksVolume/TicksVolume.mq5

Copyright: Copyright 2016, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2016, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 3, 2: 3, 3: 3, 4: 3}, 'colors': {1: [8388608], 2: [64636], 3: [2237106], 4: [65535]}, 'widths': {1: 6, 2: 2, 3: 6, 4: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Pips Up', 2: 'Tick Up', 3: 'Pips Down', 4: 'Tick Down'}, 'levels': [0.0], 'description': [], 'name': 'TicksVolume', 'source': 'MQL5 Indicators/TicksVolume/TicksVolume.mq5', 'folder': 'TicksVolume', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
UpTick = Arr(0, 0.0)
DnTick = Arr(0, 0.0)
_Bid = 0.0
_Ask = 0.0
PriceUp = 0.0
PriceDn = 0.0
TickUp = 0.0
TickDn = 0.0

def OnInit():
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, UpTick, INDICATOR_DATA)
    SetIndexBuffer(2, DnBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, DnTick, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TicksVolume')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global PriceDn, PriceUp, TickDn, TickUp, _Ask, _Bid, _s_OnCalculate_LastBar
    ArraySetAsSeries(UpBuffer, True)
    ArraySetAsSeries(DnBuffer, True)
    ArraySetAsSeries(UpTick, True)
    ArraySetAsSeries(DnTick, True)
    ArraySetAsSeries(time, True)
    bars = rates_total - 1
    if prev_calculated > 0:
        bars = rates_total - (prev_calculated - 1)
    for i in range(bars, 0 - 1, -1):
        CurBar = time[0]
        last_tick = MqlTick()
        SymbolInfoTick(Symbol(), last_tick)
        Bid = last_tick.bid
        Ask = last_tick.ask
        if _s_OnCalculate_LastBar != CurBar:
            TickUp = 0.0
            TickDn = 0.0
            PriceUp = 0.0
            PriceDn = 0.0
            _s_OnCalculate_LastBar = CurBar
        if _Bid == 0:
            _Bid = Bid
        if _Ask == 0:
            _Ask = Ask
        if Bid > _Bid or (_Bid == Bid and _Ask > Ask):
            PriceUp += Bid - _Bid
            UpBuffer[0] = _fdiv(PriceUp, Point())
            TickUp += 1
            UpTick[0] = TickUp
        if Bid < _Bid or (_Bid == Bid and _Ask < Ask):
            PriceDn += Bid - _Bid
            DnBuffer[0] = _fdiv(PriceDn, Point())
            TickDn -= 1
            DnTick[0] = TickDn
        _Bid = Bid
        _Ask = Ask
    return rates_total

# ---- static local variables
_s_OnCalculate_LastBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TicksVolume(_MQL5Indicator):
    name = 'TicksVolume'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

