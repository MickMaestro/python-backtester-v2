"""MACD_Signals — converted from MQL5: MQL5 Indicators/MACD Signals/MACD_Signals.mq5

Copyright: Copyright (c) TheXpert, mailto:TheForEXpert@gmail.com; Link: theforexpert@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright (c) TheXpert, mailto:TheForEXpert@gmail.com', 'link': 'theforexpert@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16777215, 15453831, 2237106]}, 'widths': {1: 1}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'MACD_Signals', 'source': 'MQL5 Indicators/MACD Signals/MACD_Signals.mq5', 'folder': 'MACD Signals', 'inputs': [{'mql': 'Copyright', 'py': 'Copyright', 'param': None, 'type': 'string', 'default': 'Copyright (c) TheXpert, mailto:TheForEXpert@gmail.com', 'label': '', 'sinput': False}, {'mql': '_1', 'py': '_1', 'param': None, 'type': 'string', 'default': 'Parameters for MACD', 'label': '', 'sinput': False}, {'mql': 'MaFast', 'py': 'MaFast', 'param': 'MaFast', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'MaSlow', 'py': 'MaSlow', 'param': 'MaSlow', 'type': 'int', 'default': 73, 'label': '', 'sinput': False}, {'mql': 'MaSignal', 'py': 'MaSignal', 'param': 'MaSignal', 'type': 'int', 'default': 13, 'label': '', 'sinput': False}, {'mql': '_2', 'py': '_2', 'param': None, 'type': 'string', 'default': 'Applied price', 'label': '', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}, {'mql': '_3', 'py': '_3', 'param': None, 'type': 'string', 'default': 'Minimal distance from previous valuable extremum to be valuable', 'label': '', 'sinput': False}, {'mql': 'Sequence', 'py': 'Sequence', 'param': 'Sequence', 'type': 'int', 'default': 17, 'label': '', 'sinput': False}, {'mql': 'Log', 'py': 'Log', 'param': 'Log', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Copyright = _input('Copyright', 'Copyright (c) TheXpert, mailto:TheForEXpert@gmail.com')
_1 = _input('_1', 'Parameters for MACD')
MaFast = _input('MaFast', 5)
MaSlow = _input('MaSlow', 73)
MaSignal = _input('MaSignal', 13)
_2 = _input('_2', 'Applied price')
Price = _input('Price', PRICE_WEIGHTED)
_3 = _input('_3', 'Minimal distance from previous valuable extremum to be valuable')
Sequence = _input('Sequence', 17)
Log = _input('Log', False)
Direction = 0
Last = 0.0
LastTime = 0
Values = Arr(0, 0.0)
ValuesPainting = Arr(0, 0.0)
PatternSignal = Arr(0, 0.0)
Signal = Arr(0, 0.0)
SignalDirection = Arr(0, 0.0)
MACD = Arr(0, 0.0)
SlowMA = Arr(0, 0.0)
symbol = ""
Length = 0
Prev = 0
PrevPrev = 0
PrevPrevPrev = 0
PrevValue = 0.0
PrevPrevValue = 0.0
PrevPrevPrevValue = 0.0
LastSignalValue = 0.0
LastSignal = 0
IsLastSignal = False
MACDOrigin = 0
SlowMAOrigin = 0

def PushBack(Now, NowValue):
    global Prev, PrevPrev, PrevPrevPrev, PrevPrevPrevValue, PrevPrevValue, PrevValue
    if Prev == Now:
        PrevValue = NowValue
    else:
        PrevPrevPrev = PrevPrev
        PrevPrevPrevValue = PrevPrevValue
        PrevPrev = Prev
        PrevPrevValue = PrevValue
        Prev = Now
        PrevValue = NowValue

def OnInit():
    global MACDOrigin, SlowMAOrigin
    SetIndexBuffer(0, Values, INDICATOR_DATA)
    SetIndexBuffer(1, ValuesPainting, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, PatternSignal, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, Signal, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, SignalDirection, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, SlowMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, MACD, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, MaSlow)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MyMACD(' + _str(MaFast) + ', ' + _str(MaSlow) + ', ' + _str(MaSignal) + ')')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    MACDOrigin = iMACD(None, 0, MaFast, MaSlow, MaSignal, Price)
    SlowMAOrigin = iMA(None, 0, MaSlow, 0, MODE_EMA, PRICE_CLOSE)
    ArraySetAsSeries(Values, True)
    ArraySetAsSeries(ValuesPainting, True)
    ArraySetAsSeries(PatternSignal, True)
    ArraySetAsSeries(Signal, True)
    ArraySetAsSeries(SignalDirection, True)
    ArraySetAsSeries(SlowMA, True)
    ArraySetAsSeries(MACD, True)
    return 0

def OnCalculate(bars, counted, time, open, high, low, close, tick_volume, volume, spread):
    global Direction, IsLastSignal, Last, LastSignal, LastSignalValue, Length
    if Log:
        Print('Started')
    toCount = bars - MathMax(counted - 1, 0)
    if toCount <= 0:
        toCount = 1
    if Log:
        Print('MACDOrigin ', MACDOrigin, ' SlowMAOrigin ', SlowMAOrigin, ' bars ', bars, ' counted ', counted, 'toCount ', toCount)
    succeeded = CopyBuffer(MACDOrigin, 1, 0, bars, MACD) != -1
    if not succeeded:
        Print('Problems while getting MACD values, Last Error = ', GetLastError())
        return 0
    succeeded = CopyBuffer(SlowMAOrigin, 0, 0, bars, SlowMA) != -1
    if not succeeded:
        Print('Problems while getting MA values, Last Error = ', GetLastError())
        return 0
    for i in range(toCount - 1, 0 - 1, -1):
        if SlowMA[i] != 0:
            Values[i] = _fdiv(MACD[i], SlowMA[i])
        elif Log:
            Print('Bad MA Value')
    for i in range(toCount - 2, 0 - 1, -1):
        now = Values[i]
        Signal[i + 1] = 0.0
        if i < (bars - 2):
            SignalDirection[i + 1] = SignalDirection[i + 2]
        PatternSignal[i + 1] = 0.0
        if Last == 0:
            Last = now
            continue
        if Direction == 0:
            if Last > now:
                Direction = -1
            if Last < now:
                Direction = 1
            Last = now
            Length = 1
            continue
        if ((now - Last) * Direction) > 0:
            Last = now
            Length += 1
            Signal[i + 1] = 0.0
            continue
        if ((now - Last) * Direction) < 0:
            Direction = -Direction
            Signal[i + 1] = Direction * Values[i + 1]
            Last = now
            if Prev == 0:
                PushBack(Direction, now)
                Length = 1
                continue
            else:
                if IsLastSignal:
                    if Length > Sequence:
                        PushBack(LastSignal, LastSignalValue)
                        PushBack(Direction, now)
                        IsLastSignal = False
                    else:
                        LastSignal = Direction
                        LastSignalValue = now
                        Length = 1
                        continue
                else:
                    if Length > Sequence:
                        PushBack(Direction, now)
                    else:
                        LastSignal = Direction
                        LastSignalValue = now
                        IsLastSignal = True
                        Length = 1
                        continue
                Length = 1
                if Prev == 1 and PrevValue > PrevPrevPrevValue:
                    PatternSignal[i + 1] = 1.0
                if Prev == -1 and PrevValue < PrevPrevPrevValue:
                    PatternSignal[i + 1] = -1.0
                if Prev == 1 and PrevValue > (-0.1 * PrevPrevValue):
                    PatternSignal[i + 1] = 1.0
                if Prev == -1 and PrevValue < (-0.1 * PrevPrevValue):
                    PatternSignal[i + 1] = -1.0
                if PatternSignal[i + 1] != 0:
                    if PatternSignal[i + 1] > 0:
                        SignalDirection[i + 1] = 1.0
                    if PatternSignal[i + 1] < 0:
                        SignalDirection[i + 1] = -1.0
    for j in range(toCount - 1, 0 - 1, -1):
        if SignalDirection[j] > 0:
            ValuesPainting[j] = 1.0
        elif SignalDirection[j] < 0:
            ValuesPainting[j] = 2.0
    return bars


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MACDSignals(_MQL5Indicator):
    name = 'MACD_Signals'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'MaFast': 5,
        'MaSlow': 73,
        'MaSignal': 13,
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=7),
        'Sequence': 17,
        'Log': False,
    }

