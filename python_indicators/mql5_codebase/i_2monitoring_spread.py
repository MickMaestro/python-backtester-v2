"""2monitoring-spread — converted from MQL5: MQL5 Indicators/Monitoring Spread/2monitoring-spread.mq5


Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Functions not available here: FileReadLong, FileWriteLong
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3, 'indicator_minimum': -1.0}, 'types': {1: 3, 2: 3, 3: 3}, 'colors': {1: [8421504], 2: [255], 3: [55295]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': '2monitoring-spread', 'source': 'MQL5 Indicators/Monitoring Spread/2monitoring-spread.mq5', 'folder': 'Monitoring Spread', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MaxSpread = Arr(0, 0.0)
AvgSpread = Arr(0, 0.0)
MinSpread = Arr(0, 0.0)
MinSp = 0
MaxSp = 0
Vol = 0
PrevTime = 0
AvgSp = 0.0
Ask = 0.0
Bid = 0.0
FileName = ""
Flag = False

def RealSymbol(smb):
    return SymbolInfoDouble(smb, SYMBOL_BID) != 0

def OnInit():
    global FileName, Flag
    SetIndexBuffer(0, MaxSpread, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, 'Max')
    ArraySetAsSeries(MaxSpread, True)
    SetIndexBuffer(1, AvgSpread, INDICATOR_DATA)
    PlotIndexSetString(1, PLOT_LABEL, 'Avg')
    ArraySetAsSeries(AvgSpread, True)
    SetIndexBuffer(2, MinSpread, INDICATOR_DATA)
    PlotIndexSetString(2, PLOT_LABEL, 'Min')
    ArraySetAsSeries(MinSpread, True)
    Flag = RealSymbol(Symbol())
    FileName = Symbol() + EnumToString(Period(), '') + '_Spread.dat'
    return 0

def OnDeinit(reason):
    if Flag:
        WriteSpread()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global Ask, Bid, PrevTime, _s_OnCalculate_FirstRun
    Ask = SymbolInfoDouble(Symbol(), SYMBOL_ASK)
    Bid = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ArraySetAsSeries(time, True)
    if not Flag:
        GetData()
        return rates_total
    if _s_OnCalculate_FirstRun:
        GetData()
        CreateNewSpread()
        PrevTime = time[0]
        _s_OnCalculate_FirstRun = False
        return rates_total
    if PrevTime == time[0]:
        ModifySpread()
        PrevTime = time[0]
    else:
        WriteSpread()
        CreateNewSpread()
        PrevTime = time[0]
    MaxSpread[0] = MaxSp
    AvgSpread[0] = _fdiv(AvgSp, Vol)
    MinSpread[0] = MinSp
    return rates_total

def CreateNewSpread():
    global AvgSp, MaxSp, MinSp, Vol
    MinSp = _int(_fdiv(Ask - Bid, Point()) + 0.1)
    MaxSp = MinSp
    AvgSp = MinSp
    Vol = 1

def ModifySpread():
    global AvgSp, MaxSp, MinSp, Vol
    Spread = _int(_fdiv(Ask - Bid, Point()) + 0.1)
    if Spread > MaxSp:
        MaxSp = Spread
    elif Spread < MinSp:
        MinSp = Spread
    AvgSp += Spread
    Vol += 1

def GetData():
    h = FileOpen(FileName, (FILE_BIN | FILE_READ) | FILE_ANSI)
    if h < 0:
        return
    while not FileIsEnding(h):
        dt = _long(_missing('FileReadLong')(h))
        Max = FileReadDouble(h)
        Avg = FileReadDouble(h)
        Min = FileReadDouble(h)
        i = _int(iBarShift_u(Symbol(), Period(), dt, True))
        if i >= 0:
            MaxSpread[i] = Max
            AvgSpread[i] = Avg
            MinSpread[i] = Min
    FileClose(h)

def WriteSpread():
    global AvgSp
    h = FileOpen(FileName, ((FILE_BIN | FILE_READ) | FILE_WRITE) | FILE_ANSI)
    AvgSp = _fdiv(AvgSp, Vol)
    FileSeek(h, 0, SEEK_END)
    _missing('FileWriteLong')(h, PrevTime)
    FileWriteDouble(h, MaxSp)
    FileWriteDouble(h, AvgSp)
    FileWriteDouble(h, MinSp)
    FileClose(h)

def iBarShift_u(smb, tf, time, exac=False):
    rates = Arr(0, 0)
    if time < 0:
        return -1
    bar = CopyTime(smb, tf, _DT(iTime_u(smb, tf, 0)), _DT(time), rates)
    if bar <= 0:
        return -1
    if exac and iTime_u(smb, tf, bar - 1) != time:
        return -1
    return bar - 1

def iTime_u(smb, tf, i):
    rates = Arr(0, 0)
    if i < 0:
        return -1
    if CopyTime(smb, tf, i, 1, rates) > 0:
        return rates[0]
    return -1

# ---- static local variables
_s_OnCalculate_FirstRun = True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ind2monitoringSpread(_MQL5Indicator):
    name = '2monitoring-spread'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

