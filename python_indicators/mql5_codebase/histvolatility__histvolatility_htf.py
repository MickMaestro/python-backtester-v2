"""histvolatility — converted from MQL5: MQL5 Indicators/HistVolatility_HTF/histvolatility.mq5

Copyright: Copyright © 2008, Victor Umnyashkin; Link: v354@hotbox.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, Victor Umnyashkin', 'link': 'v354@hotbox.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 8388736, 13749760]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'HistVolatility'}, 'levels': [], 'description': [], 'name': 'histvolatility', 'source': 'MQL5 Indicators/HistVolatility_HTF/histvolatility.mq5', 'folder': 'HistVolatility_HTF', 'inputs': [{'mql': 'Per', 'py': 'Per', 'param': 'Per', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'Scale', 'py': 'Scale', 'param': 'Scale', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Trading_Day_In_Year', 'py': 'Trading_Day_In_Year', 'param': 'Trading_Day_In_Year', 'type': 'int', 'default': 365, 'label': '', 'sinput': False}, {'mql': 'Percent', 'py': 'Percent', 'param': 'Percent', 'type': 'int', 'default': 100, 'label': '', 'sinput': False}, {'mql': 'Coeff', 'py': 'Coeff', 'param': 'Coeff', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Scale_
S1_ = 1
S2_ = 2
S3_ = 3
_enum('Scale_', {1: 'S1_', 2: 'S2_', 3: 'S3_'})

# ---- inputs and global variables
Per = _input('Per', 21)
Scale = _input('Scale', S3_)
Trading_Day_In_Year = _input('Trading_Day_In_Year', 365)
Percent = _input('Percent', 100)
Coeff = _input('Coeff', 1.0)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
LineBuffer = Arr(0, 0.0)
ColorLineBuffer = Arr(0, 0.0)
YearBase = 0
min_rates_total = 0

def OnInit():
    global YearBase, min_rates_total
    min_rates_total = Per + 1
    YearBase = _idiv(Trading_Day_In_Year * PeriodSeconds(PERIOD_D1), PeriodSeconds(PERIOD_CURRENT))
    SetIndexBuffer(0, LineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(LineBuffer, True)
    SetIndexBuffer(1, ColorLineBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorLineBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'HistVolatility(', Per, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (min_rates_total + begin):
        return 0
    Volatility = 0.0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total - begin
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + 1 + begin)
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(price, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Volatility = WVHiVol(Per, price, bar, Scale)
        LineBuffer[bar] = Volatility * MathSqrt((1.0 * YearBase) / Per) * Percent * Coeff
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

def WVHiVol(N, Price, index, IsLog):
    Mid = 0.0
    MidLog = 0.0
    MidIncr = 0.0
    delta = 0.0
    Vol = 0.0
    VolLog = 0.0
    VolIncr = 0.0
    Mid = 0.0
    MidIncr = 0.0
    MidLog = 0.0
    for i in range(0, N):
        delta = Price[index + i] - Price[index + i + 1]
        Mid += delta
        delta = _fdiv(delta, Price[index + i])
        MidIncr += delta
        delta = _fdiv(Price[index + i], Price[index + i + 1])
        MidLog += MathLog(delta)
    Vol = 0.0
    VolLog = 0.0
    VolIncr = 0.0
    for i in range(0, N):
        delta = Price[index + i] - Price[index + i + 1]
        Vol += (delta - Mid) * (delta - Mid)
        delta = _fdiv(delta, Price[i])
        VolIncr += (delta - MidIncr) * (delta - MidIncr)
        delta = MathLog(_fdiv(Price[index + i], Price[index + i + 1]))
        VolLog += (delta - MidLog) * (delta - MidLog)
    if IsLog == S2_:
        return MathSqrt(_fdiv(Vol, N - 1.0))
    if IsLog == S1_:
        return MathSqrt(_fdiv(VolIncr, N - 1.0))
    return MathSqrt(_fdiv(VolLog, N - 1.0))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Histvolatility(_MQL5Indicator):
    name = 'histvolatility'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Per': 21,
        'Scale': _Choice({1: '1', 2: '2', 3: '3'}, default=3),
        'Trading_Day_In_Year': 365,
        'Percent': 100,
        'Coeff': 1.0,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

