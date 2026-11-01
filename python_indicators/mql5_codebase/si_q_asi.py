"""si_q_asi — converted from MQL5: MQL5 Indicators/si_q_asi/si_q_asi.mq5

Краткосрочный и Аккумулятивный Индексы колебания цены. \\nCurrent and Accumulative Swing Index
Copyright: Copyright © 2006, Evbut; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Evbut', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [65280, 16760576, 8421504, 16711935, 255]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'si_q_asi'}, 'levels': [], 'description': ['Краткосрочный и Аккумулятивный Индексы колебания цены. \\nCurrent and Accumulative Swing Index'], 'name': 'si_q_asi', 'source': 'MQL5 Indicators/si_q_asi/si_q_asi.mq5', 'folder': 'si_q_asi', 'inputs': [{'mql': 'IndexType', 'py': 'IndexType', 'param': 'IndexType', 'type': 'int', 'default': 0, 'label': 'Тип индекса / Index Type', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_CHOIS
SwingIndex = 0
AccumulativeIndex = 1
_enum('ENUM_CHOIS', {0: 'SwingIndex', 1: 'AccumulativeIndex'})

# ---- inputs and global variables
IndexType = _input('IndexType', SwingIndex)  # Тип индекса / Index Type
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
ATR_Handle = 0

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Period = 15
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    min_rates_total = MathMax(ATR_Period, 2)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'si_q_asi(' + EnumToString(IndexType, 'ENUM_CHOIS') + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 4)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    global _s_OnCalculate_ER_prev, _s_OnCalculate_SI_prev
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    SI = 0.0
    K = 0.0
    SH = 0.0
    R = 0.0
    ER = 0.0
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_SI_prev = 0.0
        _s_OnCalculate_ER_prev = 0.0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ER = _s_OnCalculate_ER_prev
    if CopyBuffer(ATR_Handle, MAIN_LINE, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(Open, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if Close[bar + 1] >= Low[bar] and Close[bar + 1] <= High[bar]:
            ER = 0.0
        else:
            if Close[bar + 1] > High[bar]:
                ER = MathAbs(High[bar] - Close[bar + 1])
            if Close[bar + 1] < Low[bar]:
                ER = MathAbs(Low[bar] - Close[bar + 1])
        K = MathMax(MathAbs(High[bar] - Close[bar + 1]), MathAbs(Low[bar] - Close[bar + 1]))
        SH = MathAbs(Close[bar + 1] - Open[bar + 1])
        R = ATR[bar] - (0.5 * ER) + (0.25 * SH)
        if not R:
            SI = 0.0
        else:
            SI = _fdiv(50 * (Close[bar] - Close[bar + 1] + (0.5 * (Close[bar] - Open[bar])) + (0.25 * (Close[bar + 1] - Open[bar + 1]))) * _fdiv(K, Point()), R)
        if IndexType == SwingIndex:
            IndBuffer[bar] = SI
        else:
            IndBuffer[bar] = SI + _s_OnCalculate_SI_prev
            if bar:
                _s_OnCalculate_SI_prev = SI
        if bar:
            _s_OnCalculate_ER_prev = ER
        clr = 2
        if IndBuffer[bar] >= 0:
            if IndBuffer[bar] >= IndBuffer[bar + 1]:
                clr = 0
            else:
                clr = 1
        else:
            if IndBuffer[bar] <= IndBuffer[bar + 1]:
                clr = 4
            else:
                clr = 3
        ColorBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_SI_prev = 0.0
_s_OnCalculate_ER_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SiQAsi(_MQL5Indicator):
    name = 'si_q_asi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'IndexType': _Choice({0: 'Краткросрочный индекс / Current Index', 1: 'Накопительный индекс / Accumulative Index'}, default=0),  # Тип индекса / Index Type
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

