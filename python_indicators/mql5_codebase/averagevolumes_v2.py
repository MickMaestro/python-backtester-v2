"""averagevolumes_v2 — converted from MQL5: MQL5 Indicators/Average Volumes (Volumes Forecasting)/averagevolumes_v2.mq5

Averaged value of the volumes.
victorg, www.mql5.com, 2013.
Copyright: Copyright 2013, victorg.; Link: https://login.mql5.com/ru/users/victorg; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2013, victorg.', 'link': 'https://login.mql5.com/ru/users/victorg', 'version': '2.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2, 'indicator_minimum': 0.0}, 'types': {1: 3, 2: 1}, 'colors': {1: [25600], 2: [11186720]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {}, 'levels': [], 'description': ['Averaged value of the volumes.', 'victorg, www.mql5.com, 2013.'], 'name': 'averagevolumes_v2', 'source': 'MQL5 Indicators/Average Volumes (Volumes Forecasting)/averagevolumes_v2.mq5', 'folder': 'Average Volumes (Volumes Forecasting)', 'inputs': [{'mql': 'inpNumAver', 'py': 'inpNumAver', 'param': 'inpNumAver', 'type': 'int', 'default': 12, 'label': 'Number of weeks for averaging', 'sinput': False}, {'mql': 'inpVolMod', 'py': 'inpVolMod', 'param': 'inpVolMod', 'type': 'int', 'default': 0, 'label': 'Volume mode', 'sinput': False}, {'mql': 'inpMedian', 'py': 'inpMedian', 'param': 'inpMedian', 'type': 'bool', 'default': False, 'label': 'Median filtering', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum vmode
Tick_Volume = 0
Real_Volume = 1
_enum('vmode', {0: 'Tick_Volume', 1: 'Real_Volume'})

# ---- inputs and global variables
inpNumAver = _input('inpNumAver', 12)  # Number of weeks for averaging
inpVolMod = _input('inpVolMod', Tick_Volume)  # Volume mode
inpMedian = _input('inpMedian', False)  # Median filtering
VBuf = Arr(0, 0.0)
VHBuf = Arr(0, 0.0)
Volume = Arr(0, 0.0)
MFilt = Arr(0, 0.0)
Count = Arr(0, 0)
NumAver = 0
PSeconds = 0
Len = 0
Shift = 0
OldDay = 0

def OnInit():
    global Len, NumAver, OldDay, PSeconds, Shift
    str_ = ""
    if inpNumAver < 2:
        NumAver = 2
    else:
        NumAver = inpNumAver
    PSeconds = PeriodSeconds(Period())
    Len = _idiv(604800, PSeconds)
    if Len < 1:
        Len = 1
    ArrayResize(Volume, Len)
    ArrayResize(Count, Len)
    if inpMedian == True:
        ArrayResize(MFilt, Len)
    Shift = _idiv(172800, PSeconds)
    SetIndexBuffer(0, VHBuf, INDICATOR_DATA)
    SetIndexBuffer(1, VBuf, INDICATOR_DATA)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    str_ = 'AvrVolumes (' + _str(NumAver) + ')'
    if inpVolMod == Tick_Volume:
        str_ += ' TickVolume'
    elif inpVolMod == Real_Volume:
        str_ += ' RealVolume'
    IndicatorSetString(INDICATOR_SHORTNAME, str_)
    OldDay = 0
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global OldDay
    i = 0
    k = 0
    m = 0
    n = 0
    rt = 0
    sp = Arr(1, 0, dyn=False)
    max_ = 0
    min_ = 0
    a = 0.0
    b = 0.0
    dt = 0
    if rates_total < Len:
        return 0
    rt = rates_total - 1
    dt = _idiv(time[rt], 86400)
    if prev_calculated <= 0 or dt != OldDay:
        OldDay = dt
        m = TerminalInfoInteger(TERMINAL_MAXBARS)
        n = Len * NumAver
        if n > m:
            n = m
        CopySpread(Symbol(), Period(), n - 1, 1, sp)
        m = 0
        ArrayInitialize(Volume, 0)
        ArrayInitialize(Count, 0)
        i = rt
        for i in range(i, 0, -1):
            k = _idiv(_int(_imod(time[i], 604800)), PSeconds)
            if inpVolMod == Tick_Volume:
                Volume[k] += float(tick_volume[i])
            elif inpVolMod == Real_Volume:
                Volume[k] += float(volume[i])
            Count[k] += 1
            if Count[k] > m:
                m = Count[k]
            if Count[k] > NumAver:
                break
        else:
            i = _range_end(i, 0, -1)
        i = 0
        for i in range(i, Len):
            if Count[i] > 1:
                Volume[i] = _fdiv(Volume[i], Count[i])
        else:
            i = _range_end(i, Len, 1)
        PlotIndexSetString(1, PLOT_LABEL, _str(m - 1) + ' week average')
        if inpMedian == True and Len > 2:
            if Volume[0] < Volume[1]:
                max_ = 1
            else:
                max_ = 0
            i = 2
            for i in range(i, Len):
                min_ = (2 * i) - 3 - max_
                if Volume[i] < Volume[min_]:
                    max_ = i - 1
                    MFilt[max_] = Volume[min_]
                elif Volume[i] > Volume[max_]:
                    MFilt[i - 1] = Volume[max_]
                    max_ = i
                else:
                    MFilt[i - 1] = Volume[i]
                    max_ = min_ + 1
            else:
                i = _range_end(i, Len, 1)
            k = Len - 1
            if Volume[k] < Volume[0]:
                a = Volume[k]
                b = Volume[0]
            else:
                a = Volume[0]
                b = Volume[k]
            if Volume[k - 1] < a:
                MFilt[k] = a
            elif Volume[k - 1] > b:
                MFilt[k] = b
            else:
                MFilt[k] = Volume[k - 1]
            if Volume[0] < Volume[1]:
                a = Volume[0]
                b = Volume[1]
            else:
                a = Volume[1]
                b = Volume[0]
            if Volume[k] < a:
                MFilt[0] = a
            elif Volume[k] > b:
                MFilt[0] = b
            else:
                MFilt[0] = Volume[k]
            ArrayCopy(Volume, MFilt, 0, 0)
    if rates_total != prev_calculated:
        n = rates_total - Len
        if n < 1:
            n = 1
        i = n
        for i in range(i, rt):
            k = _idiv(_int(_imod(time[i], 604800)), PSeconds)
            m = i - Shift
            if m >= 0:
                VBuf[m] = Volume[k]
            if inpVolMod == Tick_Volume:
                VHBuf[i] = float(tick_volume[i])
            elif inpVolMod == Tick_Volume:
                VHBuf[i] = float(volume[i])
        else:
            i = _range_end(i, rt, 1)
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, n)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, n - Shift)
        k = _idiv(_int(_imod(time[rt], 604800)), PSeconds)
        i = rt - Shift
        for i in range(i, rates_total):
            VBuf[i] = Volume[k]
            k += 1
            if k >= Len:
                k = 0
        else:
            i = _range_end(i, rates_total, 1)
    if inpVolMod == Tick_Volume:
        VHBuf[rt] = float(tick_volume[rt])
    elif inpVolMod == Tick_Volume:
        VHBuf[rt] = float(volume[rt])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AveragevolumesV2(_MQL5Indicator):
    name = 'averagevolumes_v2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpNumAver': 12,  # Number of weeks for averaging
        'inpVolMod': _Choice({0: 'Tick_Volume', 1: 'Real_Volume'}, default=0),  # Volume mode
        'inpMedian': False,  # Median filtering
    }

