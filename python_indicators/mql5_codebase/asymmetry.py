"""asymmetry — converted from MQL5: MQL5 Indicators/Asymmetry_HTF/asymmetry.mq5

Индикатор ассиметрии
Copyright: Copyright © 2008,Fedor Igumnov; Link: igumnovfedor@yandex.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008,Fedor Igumnov', 'link': 'igumnovfedor@yandex.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [15624315]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Asymmetry'}, 'levels': [], 'description': ['Индикатор ассиметрии'], 'name': 'asymmetry', 'source': 'MQL5 Indicators/Asymmetry_HTF/asymmetry.mq5', 'folder': 'Asymmetry_HTF', 'inputs': [{'mql': 'AsPeriod', 'py': 'AsPeriod', 'param': 'AsPeriod', 'type': 'uint', 'default': 30, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
AsPeriod = _input('AsPeriod', 30)  # Период индикатора
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtLineBuffer = Arr(0, 0.0)
RSI_Handle = 0
min_rates_total = 0

def OnInit():
    global RSI_Handle, min_rates_total
    RSI_Handle = iRSI(None, PERIOD_CURRENT, AsPeriod, PRICE_CLOSE)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI')
    min_rates_total = _int(AsPeriod)
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    shortname = Box("")
    StringConcatenate(shortname, 'Asymmetry(', AsPeriod, ' ', Shift, ')')
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(ExtLineBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(RSI_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    i = 0
    RSI = Arr(0, 0.0)
    M = 0.0
    D = 0.0
    MD = 0.0
    stdDev = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = _int(limit + 1 + AsPeriod)
    if CopyBuffer(RSI_Handle, 0, 0, to_copy, RSI) <= 0:
        return 0
    ArraySetAsSeries(RSI, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        M = 0.0
        D = 0.0
        MD = 0.0
        i = 0
        for i in range(i, _int(AsPeriod)):
            M += RSI[bar + i]
        else:
            i = _range_end(i, _int(AsPeriod), 1)
        M = M / AsPeriod
        i = 0
        for i in range(i, _int(AsPeriod)):
            D += MathPow(RSI[bar + i] - M, 2)
        else:
            i = _range_end(i, _int(AsPeriod), 1)
        D = D / AsPeriod
        stdDev = MathSqrt(D)
        i = 0
        for i in range(i, _int(AsPeriod)):
            MD += MathPow(RSI[bar + i] - D, 2)
        else:
            i = _range_end(i, _int(AsPeriod), 1)
        MD = MD / AsPeriod
        ExtLineBuffer[bar] = MathAbs(_fdiv(MD, D * stdDev))
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Asymmetry(_MQL5Indicator):
    name = 'asymmetry'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AsPeriod': 30,  # Период индикатора
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

