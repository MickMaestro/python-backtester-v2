"""linear_sinus_ft — converted from MQL5: MQL5 Indicators/Linear Sinus FT/linear_sinus_ft.mq5

Copyright: Copyright © 2009, buldakov_a; Link: mailto:buldakov_a@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, buldakov_a', 'link': 'mailto:buldakov_a@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Sinus', 2: 'Out'}, 'levels': [], 'description': [], 'name': 'linear_sinus_ft', 'source': 'MQL5 Indicators/Linear Sinus FT/linear_sinus_ft.mq5', 'folder': 'Linear Sinus FT', 'inputs': [{'mql': 'inHours', 'py': 'inHours', 'param': 'inHours', 'type': 'uint', 'default': 600, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inHours = _input('inHours', 600)
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
SinBuffer = Arr(0, 0.0)
OutBuffer = Arr(0, 0.0)
Hours = 0
min_rates_total = 0
Hour = 0
n = 0
n2 = 0
mBar120 = 0
mBar60 = 0

def OnInit():
    global Hours, mBar120, mBar60, min_rates_total, n, n2
    Hours = _int(MathMax(inHours, 2))
    mPeriod = _idiv(PeriodSeconds(PERIOD_CURRENT), 60)
    mBar120 = _idiv(120, mPeriod)
    mBar60 = _idiv(60, mPeriod)
    n = _idiv(_idiv(Hours * 60, mPeriod), 2)
    n2 = 2 * n
    min_rates_total = (2 * n2) + 1
    SetIndexBuffer(0, SinBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(SinBuffer, True)
    SetIndexBuffer(1, OutBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(OutBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Linear_Sinus_FT(', inHours, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(price, True)
    limit = 0
    bar = 0
    j = 0
    i = 0
    t = 0
    Num = 0.0
    Den = 0.0
    stti = 0.0
    stttti = 0.0
    sOuti = 0.0
    si = 0.0
    sOutti = 0.0
    sOuttti = 0.0
    a = 0.0
    b = 0.0
    c = 0.0
    Alfa = 0.0
    dAlfa = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, rates_total - min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, rates_total - min_rates_total)
    bar = limit + min_rates_total
    for bar in range(bar, 0 - 1, -1):
        SinBuffer[bar] = 0.0
        OutBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    j = n2
    for j in range(j, 0 - 1, -1):
        Num = 0.0
        Den = 0.0
        i = n + n
        for i in range(i, 0 - 1, -1):
            Num = Num + (MathSin(_fdiv(i * 3.14159265, n2)) * price[j + i])
            Den = Den + MathSin(_fdiv(i * 3.14159265, n2))
        else:
            i = _range_end(i, 0 - 1, -1)
        SinBuffer[j + n] = _fdiv(Num, Den)
        i = n
        for i in range(i, 0 - 1, -1):
            SinBuffer[i] = SinBuffer[n + 0] + ((SinBuffer[n + 0] - SinBuffer[n + 1]) * (n - i))
        else:
            i = _range_end(i, 0 - 1, -1)
    else:
        j = _range_end(j, 0 - 1, -1)
    t = n2 + 1
    stti = _idiv((t * t * t) - t, 12)
    stttti = _idiv((3 * t * t * t * t * t) - (10 * t * t * t) + (7 * t), 240)
    sOuti = 0.0
    si = 0.0
    sOutti = 0.0
    sOuttti = 0.0
    i = n2
    for i in range(i, 0 - 1, -1):
        sOuti = sOuti + SinBuffer[i]
        si = si + ((-i) + _idiv(t, 2))
        sOutti = sOutti + (SinBuffer[i] * ((-i) + _idiv(t, 2)))
        sOuttti = sOuttti + (SinBuffer[i] * ((-i) + _idiv(t, 2)) * ((-i) + _idiv(t, 2)))
    else:
        i = _range_end(i, 0 - 1, -1)
    b = _fdiv(sOutti, stti)
    c = _fdiv(-(_fdiv(sOuti, t) - _fdiv(sOuttti, stti)), MathAbs(_fdiv(stti, t) - _fdiv(stttti, stti)))
    a = _fdiv(sOuti - (stti * c), t)
    i = 2 * n
    for i in range(i, 0 - 1, -1):
        OutBuffer[i] = a + (b * ((-i) + _idiv(t, 2))) + (c * ((-i) + _idiv(t, 2)) * ((-i) + _idiv(t, 2)))
    else:
        i = _range_end(i, 0 - 1, -1)
    dAlfa = 0.0
    Alfa = _fdiv(OutBuffer[0] - OutBuffer[mBar60], Point())
    if Alfa > 0:
        dAlfa = _fdiv(OutBuffer[0] - OutBuffer[mBar60] - (OutBuffer[mBar60] - OutBuffer[mBar120]), Point())
    if Alfa < 0:
        dAlfa = _fdiv(OutBuffer[mBar120] - OutBuffer[mBar60] - (OutBuffer[mBar60] - OutBuffer[0]), Point())
    Comment('Date and Time ', TimeToString(TimeCurrent()), '\n', 'Period       ', DoubleToString(Hours, 0), ' hour.', '\n', 'Tilt angle ', DoubleToString(Alfa, 1), ' points/hour.', '  Tilt angle changing ', DoubleToString(dAlfa, 3), ' points/hour.^2')
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LinearSinusFt(_MQL5Indicator):
    name = 'linear_sinus_ft'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inHours': 600,
        'Shift': 0,  # horizontal shift of the indicator in bars
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

