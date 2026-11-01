"""Objective — converted from MQL5: MQL5 Indicators/Objective_HTF/Objective.mq5

Objective
Copyright: Copyright © 2011, LeMan.; Link: b-market@mail.ru; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, LeMan.', 'link': 'b-market@mail.ru', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'colors': {1: [255], 2: [255], 3: [255], 4: [255], 5: [32768], 6: [32768], 7: [32768], 8: [32768]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'styles': {1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4, 8: 4}, 'labels': {}, 'levels': [], 'description': ['Objective'], 'name': 'Objective', 'source': 'MQL5 Indicators/Objective_HTF/Objective.mq5', 'folder': 'Objective_HTF', 'inputs': [{'mql': 'Sample', 'py': 'Sample', 'param': 'Sample', 'type': 'uint', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'Quartile_1', 'py': 'Quartile_1', 'param': 'Quartile_1', 'type': 'uint', 'default': 25, 'label': '', 'sinput': False}, {'mql': 'Quartile_2', 'py': 'Quartile_2', 'param': 'Quartile_2', 'type': 'uint', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'Quartile_3', 'py': 'Quartile_3', 'param': 'Quartile_3', 'type': 'uint', 'default': 75, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Sample = _input('Sample', 20)
Quartile_1 = _input('Quartile_1', 25)
Quartile_2 = _input('Quartile_2', 50)
Quartile_3 = _input('Quartile_3', 75)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
n0 = 0
n1 = 0
n2 = 0
n3 = 0
HOArray = Arr(0, 0.0)
OLArray = Arr(0, 0.0)
min_rates_total = 0
N_ = 0

class CIndicatorsBuffers(MqlObject):
    _q_fields = ('IndBuffer',)
    def __init__(self, *args):
        self.IndBuffer = Arr(0, 0.0)

def GetVelue(InVelueName, InVelue):
    if InVelue > 100:
        Print('Параметр ' + InVelueName + ' не может быть больше 100! Будет использовано значение по умолчанию, равное 100!')
        return 100
    if InVelue < 0:
        Print('Параметр ' + InVelueName + ' не может быть меньше 0! Будет использовано значение по умолчанию, равное 0!')
        return 0
    return InVelue

def OnInit():
    global N_, min_rates_total, n0, n1, n2, n3
    P1 = GetVelue('Quartile_1', Quartile_1)
    P2 = GetVelue('Quartile_2', Quartile_2)
    P3 = GetVelue('Quartile_3', Quartile_3)
    N_ = _int(Sample)
    if N_ < 3:
        N_ = 3
        Print('Параметр Sample не может быть меньше 3! Будет использовано значение по умолчанию, равное 3!')
    min_rates_total = N_
    n0 = N_ - 1
    n1 = _int(MathRound((N_ * P1) / 100))
    if not n1:
        n1 = 100
    n2 = _int(MathRound((N_ * P2) / 100))
    if not n2:
        n2 = 100
    n3 = _int(MathRound((N_ * P3) / 100))
    if not n3:
        n3 = 100
    if ArrayResize(HOArray, N_) < N_:
        Print('Не удалось распределить память под массив HOArray[]')
    if ArrayResize(OLArray, N_) < N_:
        Print('Не удалось распределить память под массив OLArray[]')
    for numb in range(0, 8):
        shortname = Box('')
        StringConcatenate(shortname, 'Ouartile ', numb + 1, ')')
        PlotIndexSetString(numb, PLOT_LABEL, shortname.v)
        PlotIndexSetDouble(numb, PLOT_EMPTY_VALUE, EMPTY_VALUE)
        PlotIndexSetInteger(numb, PLOT_DRAW_BEGIN, min_rates_total)
        PlotIndexSetInteger(numb, PLOT_SHIFT, Shift)
        SetIndexBuffer(numb, Ind[numb].IndBuffer, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Objective')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    q = Arr(8, 0.0, dyn=False)
    if prev_calculated == 0:
        first = min_rates_total - 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        for kkk in range(0, N_):
            HOArray[kkk] = high[bar - kkk] - open[bar - kkk]
        for kkk in range(0, N_):
            OLArray[kkk] = open[bar - kkk] - low[bar - kkk]
        ArraySort(HOArray)
        ArraySort(OLArray)
        q[0] = -OLArray[n1]
        q[1] = -OLArray[n2]
        q[2] = -OLArray[n3]
        q[3] = -OLArray[n0]
        q[4] = HOArray[n1]
        q[5] = HOArray[n2]
        q[6] = HOArray[n3]
        q[7] = HOArray[n0]
        for numb in range(0, 8):
            Ind[numb].IndBuffer[bar] = open[bar] + q[numb]
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
Ind = Arr(8, 0, dyn=False, factory=CIndicatorsBuffers)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Objective(_MQL5Indicator):
    name = 'Objective'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Sample': 20,
        'Quartile_1': 25,
        'Quartile_2': 50,
        'Quartile_3': 75,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

