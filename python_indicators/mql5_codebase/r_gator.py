"""r_gator — converted from MQL5: MQL5 Indicators/r_Gator_HTF/r_gator.mq5

Аналог  Аллигатора с меньшей задержкой сигналов
Copyright: Copyright © 2006, Rosych; Link: rosych@mail.ru; Version: 1.03

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Rosych', 'link': 'rosych@mail.ru', 'version': '1.03', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [32768], 3: [16711680]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'r_Gator Fast', 2: 'r_Gator', 3: 'r_Gator Slow'}, 'levels': [], 'description': ['Аналог  Аллигатора с меньшей задержкой сигналов'], 'name': 'r_gator', 'source': 'MQL5 Indicators/r_Gator_HTF/r_gator.mq5', 'folder': 'r_Gator_HTF', 'inputs': [{'mql': 'period1', 'py': 'period1', 'param': 'period1', 'type': 'uint', 'default': 5, 'label': 'Период быстрой MA', 'sinput': False}, {'mql': 'period2', 'py': 'period2', 'param': 'period2', 'type': 'uint', 'default': 8, 'label': 'Период средней MA', 'sinput': False}, {'mql': 'period3', 'py': 'period3', 'param': 'period3', 'type': 'uint', 'default': 13, 'label': 'Период медленной MA', 'sinput': False}, {'mql': 'Shift1', 'py': 'Shift1', 'param': 'Shift1', 'type': 'int', 'default': 0, 'label': 'Сдвиг быстрой MA по горизонтали в барах', 'sinput': False}, {'mql': 'Shift2', 'py': 'Shift2', 'param': 'Shift2', 'type': 'int', 'default': 0, 'label': 'Сдвиг средней MA по горизонтали в барах', 'sinput': False}, {'mql': 'Shift3', 'py': 'Shift3', 'param': 'Shift3', 'type': 'int', 'default': 0, 'label': 'Сдвиг медленной MA по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period1 = _input('period1', 5)  # Период быстрой MA
period2 = _input('period2', 8)  # Период средней MA
period3 = _input('period3', 13)  # Период медленной MA
Shift1 = _input('Shift1', 0)  # Сдвиг быстрой MA по горизонтали в барах
Shift2 = _input('Shift2', 0)  # Сдвиг средней MA по горизонтали в барах
Shift3 = _input('Shift3', 0)  # Сдвиг медленной MA по горизонтали в барах
Buffer1 = Arr(0, 0.0)
Buffer2 = Arr(0, 0.0)
Buffer3 = Arr(0, 0.0)
min_rates_total = 0
MA_Handle = Arr(3, 0, dyn=False, dims=(4, 7,))  # [номер мувинга][метод усреднения][цена-1]

class CArray(MqlObject):
    _q_fields = ('Array',)
    def __init__(self, *args):
        self.Array = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = _int(MathMax(period1, MathMax(period2, period3)))
    MAPeriod = Arr(3, 0, dyn=False)
    MAPeriod[0] = period1
    MAPeriod[1] = period2
    MAPeriod[2] = period3
    for i in range(0, 3):
        for k in range(0, 4):
            for r in range(0, 7):
                MA_Handle[i][k][r] = iMA(None, 0, MAPeriod[i], 0, k, r + 1)
                if MA_Handle[i][k][r] == INVALID_HANDLE:
                    Print(' Не удалось получить хендл индикатора iMA')
                    return INIT_FAILED
    SetIndexBuffer(0, Buffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Buffer1, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift1)
    SetIndexBuffer(1, Buffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Buffer2, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift2)
    SetIndexBuffer(2, Buffer3, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Buffer3, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift3)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'r_Gator'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Comment('')
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(0, 3):
        for k in range(0, 4):
            for r in range(0, 7):
                if BarsCalculated(MA_Handle[i][k][r]) < rates_total:
                    return 0
    if rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    for i in range(0, 3):
        for k in range(0, 4):
            for r in range(0, 7):
                ArraySetAsSeries(Arr__v[i][k][r].Array, True)
    to_copy = limit + 1
    for i in range(0, 3):
        for k in range(0, 4):
            for r in range(0, 7):
                if CopyBuffer(MA_Handle[i][k][r], 0, 0, to_copy, Arr__v[i][k][r].Array) <= 0:
                    return 0
    for bar in range(limit, 0 - 1, -1):
        Buffer1[bar] = 0.0
        for k in range(0, 4):
            for r in range(0, 7):
                Buffer1[bar] += Arr__v[0][k][r].Array[bar]
        Buffer1[bar] = Buffer1[bar] / 28
        Buffer2[bar] = 0.0
        for k in range(0, 4):
            for r in range(0, 7):
                Buffer2[bar] += Arr__v[1][k][r].Array[bar]
        Buffer2[bar] = Buffer2[bar] / 28
        Buffer3[bar] = 0.0
        for k in range(0, 4):
            for r in range(0, 7):
                Buffer3[bar] += Arr__v[2][k][r].Array[bar]
        Buffer3[bar] = Buffer3[bar] / 28
    return rates_total

# ---- global variables initialised from expressions
Arr__v = Arr(3, 0, dyn=False, factory=CArray, dims=(4, 7,))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RGator(_MQL5Indicator):
    name = 'r_gator'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period1': 5,  # Период быстрой MA
        'period2': 8,  # Период средней MA
        'period3': 13,  # Период медленной MA
        'Shift1': 0,  # Сдвиг быстрой MA по горизонтали в барах
        'Shift2': 0,  # Сдвиг средней MA по горизонтали в барах
        'Shift3': 0,  # Сдвиг медленной MA по горизонтали в барах
    }

