"""kprmst — converted from MQL5: MQL5 Indicators/KPrmSt_HTF/kprmst.mq5

Стохастик Синтии Кейс
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2, 'indicator_minimum': 0.0, 'indicator_maximum': 100.0}, 'types': {1: 1, 2: 1}, 'colors': {1: [8721863], 2: [16748574]}, 'widths': {1: 1, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'KPrmSt', 2: 'Signal'}, 'levels': [80.0, 50.0, 20.0], 'description': ['Стохастик Синтии Кейс'], 'name': 'kprmst', 'source': 'MQL5 Indicators/KPrmSt_HTF/kprmst.mq5', 'folder': 'KPrmSt_HTF', 'inputs': [{'mql': 'Per1', 'py': 'Per1', 'param': 'Per1', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'Per2', 'py': 'Per2', 'param': 'Per2', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Per3', 'py': 'Per3', 'param': 'Per3', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Per4', 'py': 'Per4', 'param': 'Per4', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'uint', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
Per1 = _input('Per1', 14)
Per2 = _input('Per2', 3)
Per3 = _input('Per3', 3)
Per4 = _input('Per4', 5)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
SignalBuffer = Arr(0, 0.0)
min_rates_total = 0
Count = Arr(0, 0)
MaxArray = Arr(0, 0.0)
MinArray = Arr(0, 0.0)

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

def OnInit():
    global min_rates_total
    min_rates_total = _int(MathMax(Per1, Per4)) + 2
    ArrayResize(Count, Per1)
    ArrayResize(MaxArray, Per1)
    ArrayResize(MinArray, Per1)
    ArrayInitialize(Count, 0)
    ArrayInitialize(MaxArray, 0.0)
    ArrayInitialize(MinArray, 0.0)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, SignalBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total + 1)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(SignalBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'KPrmSt(', Per1, ', ', Per2, ', ', Per3, ', ', Per4, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    maxbar = 0
    sh = 0
    sl = 0
    start1 = 0
    start2 = 0
    res = 0.0
    Range = 0.0
    ind = 0.0
    sig = 0.0
    maxbar = _int(rates_total - Per1 - 1)
    start1 = _int(maxbar - Per4)
    start2 = start1 - 1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = _int(rates_total - Per4 - 1)
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        MaxArray[Count[0]] = high[ArrayMaximum(high, bar, Per4)]
        MinArray[Count[0]] = low[ArrayMinimum(low, bar, Per4)]
        if bar > maxbar:
            Recount_ArrayZeroPos(Count, Per1)
            continue
        sh = ArrayMaximum(MaxArray, 0, WHOLE_ARRAY)
        sl = ArrayMinimum(MinArray, 0, WHOLE_ARRAY)
        Range = MaxArray[sh] - MinArray[sl]
        if Range:
            res = NormalizeDouble(_fdiv(close[bar] - MinArray[sl], Range) * 100, 0)
        else:
            res = 50.0
        ind = _s_OnCalculate_IND.EMASeries(start1, prev_calculated, rates_total, Per2, res, bar, True)
        sig = _s_OnCalculate_SIG.EMASeries(start2, prev_calculated, rates_total, Per3, ind, bar, True)
        IndBuffer[bar] = NormalizeDouble(ind, 0)
        SignalBuffer[bar] = NormalizeDouble(sig, 0)
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count, Per1)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1
_s_OnCalculate_IND = CMoving_Average()
_s_OnCalculate_SIG = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Kprmst(_MQL5Indicator):
    name = 'kprmst'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Per1': 14,
        'Per2': 3,
        'Per3': 3,
        'Per4': 5,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }
    y_range = (0.0, 100.0)

