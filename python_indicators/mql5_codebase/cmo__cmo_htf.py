"""cmo — converted from MQL5: MQL5 Indicators/CMO_HTF/cmo.mq5

CMO
Copyright: Copyright © 2006, TrendLaboratory Ltd.; Link: http://finance.groups.yahoo.com/group/TrendLaboratory; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, TrendLaboratory Ltd.', 'link': 'http://finance.groups.yahoo.com/group/TrendLaboratory', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [11186720, 36095]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'CMO'}, 'levels': [50.0, 0.0, -50.0], 'description': ['CMO'], 'name': 'cmo', 'source': 'MQL5 Indicators/CMO_HTF/cmo.mq5', 'folder': 'CMO_HTF', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 14, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'Method', 'py': 'Method', 'param': 'Method', 'type': 'int', 'default': 0, 'label': 'Тип усреднения', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Цена', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 14)  # Период индикатора
Method = _input('Method', MODE_SMA)  # Тип усреднения
Price = _input('Price', PRICE_CLOSE)  # Цена
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Line1Buffer = Arr(0, 0.0)
Line2Buffer = Arr(0, 0.0)
min_rates_total = 0
MA_Handle = 0
Count = Arr(0, 0)
Bulls = Arr(0, 0.0)
Bears = Arr(0, 0.0)

def Recount_ArrayZeroPos(CountArray, Size):
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
        CountArray[iii] = numb

def OnInit():
    global MA_Handle, min_rates_total
    min_rates_total = _int(Length)
    MA_Handle = iMA(None, 0, Length, 0, Method, Price)
    if MA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
    size = _int(Length)
    if ArrayResize(Count, size) < size:
        Print('Не удалось распределить память под массив Count[]')
    if ArrayResize(Bulls, size) < size:
        Print('Не удалось распределить память под массив Bulls[]')
    if ArrayResize(Bears, size) < size:
        Print('Не удалось распределить память под массив Bears[]')
    ArrayInitialize(Count, 0)
    ArrayInitialize(Bulls, 0)
    ArrayInitialize(Bears, 0)
    SetIndexBuffer(0, Line1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Line1Buffer, True)
    SetIndexBuffer(1, Line2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Line2Buffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'CMO(', Length, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(MA_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    MA = Arr(0, 0.0)
    dPrice = 0.0
    Sum = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 2 - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MA) <= 0:
        return 0
    ArraySetAsSeries(MA, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        dPrice = MA[bar] - MA[bar + 1]
        Bulls[Count[0]] = 0.5 * (MathAbs(dPrice) + dPrice)
        Bears[Count[0]] = 0.5 * (MathAbs(dPrice) - dPrice)
        SumBulls = 0.0
        SumBears = 0.0
        for iii in range(0, _int(Length)):
            SumBulls += Bulls[Count[iii]]
            SumBears += Bears[Count[iii]]
        Sum = SumBulls + SumBears
        if Sum:
            Line1Buffer[bar] = _fdiv(SumBulls - SumBears, SumBulls + SumBears) * 100
        else:
            Line1Buffer[bar] = 0.0
        Line2Buffer[bar] = 0.0
        if bar:
            Recount_ArrayZeroPos(Count, Length)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Cmo(_MQL5Indicator):
    name = 'cmo'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 14,  # Период индикатора
        'Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Тип усреднения
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Цена
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

