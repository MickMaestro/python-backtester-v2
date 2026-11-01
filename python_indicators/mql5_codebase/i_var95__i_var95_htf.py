"""i-var95 — converted from MQL5: MQL5 Indicators/i-VaR95_HTF/i-var95.mq5

Индикатор отображает значение исторической волатильности
Несколько замечаний: 
1. Данный индикатор не показывает точек входа в рынок и выхода из него
2. Картинка индикатора похожа на картинку изветного ATR, особенно|
   при расчете методом Паркинсона, значения, тем не менее, разные
3. Для расчета VaR используется 95-процентная вероятность,
   то есть индикатор отображает значение в пунктах, которое может быть достигнуто ценой
   с вероятностью 5% за период, равный инвестиционному горизонту (grznt)
Copyright: Copyright © 2009, piccioli@gmail.com; Link: http://piccstick.blogspot.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, piccioli@gmail.com', 'link': 'http://piccstick.blogspot.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 6053069, 16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'HistVolatility'}, 'levels': [], 'description': ['Индикатор отображает значение исторической волатильности', 'Несколько замечаний: ', '1. Данный индикатор не показывает точек входа в рынок и выхода из него', '2. Картинка индикатора похожа на картинку изветного ATR, особенно|', '   при расчете методом Паркинсона, значения, тем не менее, разные', '3. Для расчета VaR используется 95-процентная вероятность,', '   то есть индикатор отображает значение в пунктах, которое может быть достигнуто ценой', '   с вероятностью 5% за период, равный инвестиционному горизонту (grznt)'], 'name': 'i-var95', 'source': 'MQL5 Indicators/i-VaR95_HTF/i-var95.mq5', 'folder': 'i-VaR95_HTF', 'inputs': [{'mql': 'HV_Period', 'py': 'HV_Period', 'param': 'HV_Period', 'type': 'int', 'default': 21, 'label': 'Период расчета исторической волатильности', 'sinput': False}, {'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 1, 'label': 'Метод расчета', 'sinput': False}, {'mql': 'decline', 'py': 'decline', 'param': 'decline', 'type': 'double', 'default': 0.94, 'label': 'Коэффициент сглаживания', 'sinput': False}, {'mql': 'grznt', 'py': 'grznt', 'param': 'grznt', 'type': 'int', 'default': 3, 'label': 'Инвестиционный горизонт для вычисления 95% VaR', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum MODE
SHV = 1
EHV = 2
HLHV = 3
VaR95 = 4
_enum('MODE', {1: 'SHV', 2: 'EHV', 3: 'HLHV', 4: 'VaR95'})

# ---- inputs and global variables
HV_Period = _input('HV_Period', 21)  # Период расчета исторической волатильности
Mode = _input('Mode', SHV)  # Метод расчета
decline = _input('decline', 0.94)  # Коэффициент сглаживания
grznt = _input('grznt', 3)  # Инвестиционный горизонт для вычисления 95% VaR
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
LineBuffer = Arr(0, 0.0)
ColorLineBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = HV_Period + 1
    SetIndexBuffer(0, LineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(LineBuffer, True)
    SetIndexBuffer(1, ColorLineBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorLineBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Historical Volatility(', HV_Period, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(spread, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        LineBuffer[bar] = HistoricalVolatility(Mode, low, high, close, spread, bar)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ColorLineBuffer[bar] = 0.0
        if LineBuffer[bar] > LineBuffer[bar + 1]:
            ColorLineBuffer[bar] = 2.0
        if LineBuffer[bar] < LineBuffer[bar + 1]:
            ColorLineBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def HistoricalVolatility(mode, Low, High, Close, Spread, index):
    start = HV_Period + index - 1
    _sw1 = mode
    _k2 = 0 if _sw1 == SHV else 1 if _sw1 == EHV else 2 if _sw1 == HLHV else 3 if _sw1 == VaR95 else 4
    try:
        if _k2 <= 0:
            tshv = 0.0
            for i in range(start, index - 1, -1):
                tshv += MathLog(_fdiv(Close[i + 1], Close[i + 1]))
            tshv = tshv / HV_Period
            shv = 0.0
            for i in range(start, index - 1, -1):
                shv += (tshv - MathLog(_fdiv(Close[i], Close[i + 1]))) * (tshv - MathLog(_fdiv(Close[i], Close[i + 1])))
            return MathSqrt(shv / (HV_Period - 1))
        if _k2 <= 1:
            tshv = 0.0
            for i in range(start, index - 1, -1):
                tshv += MathLog(_fdiv(Close[i + 1], Close[i + 1]))
            tshv = tshv / HV_Period
            shv = 0.0
            for i in range(start, index - 1, -1):
                shv += (tshv - MathLog(_fdiv(Close[i], Close[i + 1]))) * (tshv - MathLog(_fdiv(Close[i], Close[i + 1])))
            shv = MathSqrt(shv / (HV_Period - 1))
            ehv = MathSqrt((1 - decline) * shv)
        if _k2 <= 2:
            hlhv = 0.0
            for i in range(start, index - 1, -1):
                hlhv += _fdiv(MathLog(_fdiv(High[i], Low[i])) * MathLog(_fdiv(High[i], Low[i])), 4 * MathLog(2))
            return MathSqrt(hlhv / HV_Period)
        if _k2 <= 3:
            tshv = 0.0
            for i in range(start, index - 1, -1):
                tshv += MathLog(_fdiv(Close[i + 1], Close[i + 1]))
            tshv = tshv / HV_Period
            shv = 0.0
            for i in range(start, index - 1, -1):
                shv += (tshv - MathLog(_fdiv(Close[i], Close[i + 1]))) * (tshv - MathLog(_fdiv(Close[i], Close[i + 1])))
            shv = MathSqrt(shv / (HV_Period - 1))
            return (1.65 * shv * 10000 * MathSqrt(grznt)) + (2 * Spread[index])
    except _SwitchBreak:
        pass
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IVar95(_MQL5Indicator):
    name = 'i-var95'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'HV_Period': 21,  # Период расчета исторической волатильности
        'Mode': _Choice({1: 'Simple Historical Volatility', 2: 'Exponential Historical Volatility', 3: 'High-Low Historical Volatility', 4: '95-процентный VaR'}, default=1),  # Метод расчета
        'decline': 0.94,  # Коэффициент сглаживания
        'grznt': 3,  # Инвестиционный горизонт для вычисления 95% VaR
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

