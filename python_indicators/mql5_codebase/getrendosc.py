"""getrendosc — converted from MQL5: MQL5 Indicators/Trend Oscillator/getrendosc.mq5

Copyright: Copyright © 2007, Forte928; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Forte928', 'link': '', 'version': '1.10', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [3329434], 2: [4678655]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'OscTrend', 2: 'HPFilter'}, 'levels': [80.0, 60.0, 50.0, 40.0, 20.0, 0.0], 'description': [], 'name': 'getrendosc', 'source': 'MQL5 Indicators/Trend Oscillator/getrendosc.mq5', 'folder': 'Trend Oscillator', 'inputs': [{'mql': 'Window', 'py': 'Window', 'param': 'Window', 'type': 'uint', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'OscPeriod', 'py': 'OscPeriod', 'param': 'OscPeriod', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'HPPeriod', 'py': 'HPPeriod', 'param': 'HPPeriod', 'type': 'uint', 'default': 100, 'label': '', 'sinput': False}, {'mql': 'CBars', 'py': 'CBars', 'param': 'CBars', 'type': 'uint', 'default': 500, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'uint', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Window = _input('Window', 1)
OscPeriod = _input('OscPeriod', 14)
HPPeriod = _input('HPPeriod', 100)
CBars = _input('CBars', 500)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
TriggerBuffer = Arr(0, 0.0)
min_rates_total = 0
Count = Arr(0, 0)
Series_v = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = _int(Window + OscPeriod + HPPeriod)
    ArrayResize(Count, OscPeriod)
    ArrayResize(Series_v, OscPeriod)
    ArrayInitialize(Count, 0)
    ArrayInitialize(Series_v, 0.0)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, TriggerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(TriggerBuffer, True)
    shortname = 'geTrendOsc'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    limit = _int(rates_total - Window - 1)
    limit = _int(MathMin(limit, CBars))
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, rates_total - limit)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, rates_total - limit)
    ArraySetAsSeries(Open, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IxHigh = 0.0
        IxLow = 0.0
        IxOpen = 0.0
        IxClose = 0.0
        IxHigh = High[ArrayMaximum(High, bar, Window)]
        IxLow = Low[ArrayMinimum(Low, bar, Window)]
        if (IxHigh - IxLow) > 0:
            IxOpen = Open[bar + Window]
            IxClose = Close[bar]
            Series_v[Count[0]] = _fdiv(IxClose - IxOpen, IxHigh - IxLow)
        else:
            Series_v[Count[0]] = 0.0
        Sumer = 0.0
        AbsSumer = 0.0
        for Px in range(_int(OscPeriod - 1), 0 - 1, -1):
            Sumer += Series_v[Px]
            AbsSumer += MathAbs(Series_v[Px])
        if AbsSumer:
            IndBuffer[bar] = ((_fdiv(Sumer, AbsSumer) * 100) / 2) + 50
        else:
            IndBuffer[bar] = 0.0
        HPFilter(IndBuffer, TriggerBuffer, HPPeriod, limit + 1)
        if bar > 0:
            Recount_ArrayZeroPos(Count, OscPeriod)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def Recount_ArrayZeroPos(CoArr, Size):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def HPFilter(aySource, ayResult, Lambda, iCount):
    Ak = Arr(0, 0.0)
    Bk = Arr(0, 0.0)
    Ck = Arr(0, 0.0)
    H1 = 0.0
    H2 = 0.0
    H3 = 0.0
    H4 = 0.0
    H5 = 0.0
    HH1 = 0.0
    HH2 = 0.0
    HH3 = 0.0
    HH5 = 0.0
    HB = 0.0
    HC = 0.0
    Z = 0.0
    ArrayResize(Ak, iCount)
    ArrayResize(Bk, iCount)
    ArrayResize(Ck, iCount)
    Ak[0] = 1.0 + Lambda
    Bk[0] = -2.0 * Lambda
    Ck[0] = Lambda
    for Hx in range(1, iCount - 2):
        Ak[Hx] = (6.0 * Lambda) + 1.0
        Bk[Hx] = -4.0 * Lambda
        Ck[Hx] = Lambda
    Ak[1] = (5.0 * Lambda) + 1
    Ak[iCount - 1] = 1.0 + Lambda
    Ak[iCount - 2] = (5.0 * Lambda) + 1.0
    Bk[iCount - 2] = -2.0 * Lambda
    Bk[iCount - 1] = 0.0
    Ck[iCount - 2] = 0.0
    Ck[iCount - 1] = 0.0
    for Hx in range(0, iCount):
        Z = Ak[Hx] - (H4 * H1) - (HH5 * HH2)
        HB = Bk[Hx]
        HH1 = H1
        H1 = _fdiv(HB - (H4 * H2), Z)
        Bk[Hx] = H1
        HC = Ck[Hx]
        HH2 = H2
        H2 = _fdiv(HC, Z)
        Ck[Hx] = H2
        Ak[Hx] = _fdiv(aySource[Hx] - (HH3 * HH5) - (H3 * H4), Z)
        HH3 = H3
        H3 = Ak[Hx]
        H4 = HB - (H5 * HH1)
        HH5 = H5
        H5 = HC
    H2 = 0.0
    H1 = Ak[iCount - 1]
    ayResult[iCount - 1] = H1
    for Hx in range(iCount - 2, 0 - 1, -1):
        ayResult[Hx] = Ak[Hx] - (Bk[Hx] * H1) - (Ck[Hx] * H2)
        H2 = H1
        H1 = ayResult[Hx]

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Getrendosc(_MQL5Indicator):
    name = 'getrendosc'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Window': 1,
        'OscPeriod': 14,
        'HPPeriod': 100,
        'CBars': 500,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

