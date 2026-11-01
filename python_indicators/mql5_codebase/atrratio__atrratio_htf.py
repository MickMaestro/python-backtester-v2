"""atrratio — converted from MQL5: MQL5 Indicators/ATRratio_HTF/atrratio.mq5

ATR ratio
Copyright: Copyright © 2005, Luis Guilherme Damiani; Link: http://www.damianifx.com.br; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Luis Guilherme Damiani', 'link': 'http://www.damianifx.com.br', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [13850042]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'ATR ratio'}, 'levels': [1.0], 'description': ['ATR ratio'], 'name': 'atrratio', 'source': 'MQL5 Indicators/ATRratio_HTF/atrratio.mq5', 'folder': 'ATRratio_HTF', 'inputs': [{'mql': 'Short_ATRPeriod', 'py': 'Short_ATRPeriod', 'param': 'Short_ATRPeriod', 'type': 'int', 'default': 7, 'label': 'Период быстрого ATR', 'sinput': False}, {'mql': 'Long_ATRPeriod', 'py': 'Long_ATRPeriod', 'param': 'Long_ATRPeriod', 'type': 'int', 'default': 49, 'label': 'Период медленного ATR', 'sinput': False}, {'mql': 'ATRShift', 'py': 'ATRShift', 'param': 'ATRShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Short_ATRPeriod = _input('Short_ATRPeriod', 7)  # Период быстрого ATR
Long_ATRPeriod = _input('Long_ATRPeriod', 49)  # Период медленного ATR
ATRShift = _input('ATRShift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtLineBuffer = Arr(0, 0.0)
SATR_Handle = 0
LATR_Handle = 0
min_rates_total = 0

def OnInit():
    global LATR_Handle, SATR_Handle, min_rates_total
    SATR_Handle = iATR(None, PERIOD_CURRENT, Short_ATRPeriod)
    if SATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
    LATR_Handle = iATR(None, PERIOD_CURRENT, Long_ATRPeriod)
    if LATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
    min_rates_total = MathMax(Short_ATRPeriod, Long_ATRPeriod)
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    shortname = Box("")
    StringConcatenate(shortname, 'ATR ratio(', Short_ATRPeriod, ' ', Long_ATRPeriod, ')')
    PlotIndexSetInteger(0, PLOT_SHIFT, ATRShift)
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(SATR_Handle) < rates_total or BarsCalculated(LATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    SRange = Arr(0, 0.0)
    LRange = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(SATR_Handle, 0, 0, to_copy, SRange) <= 0:
        return 0
    if CopyBuffer(LATR_Handle, 0, 0, to_copy, LRange) <= 0:
        return 0
    ArraySetAsSeries(SRange, True)
    ArraySetAsSeries(LRange, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if LRange[bar] != 0.0 and LRange[bar] != EMPTY_VALUE:
            ExtLineBuffer[bar] = _fdiv(SRange[bar], LRange[bar])
        else:
            ExtLineBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Atrratio(_MQL5Indicator):
    name = 'atrratio'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Short_ATRPeriod': 7,  # Период быстрого ATR
        'Long_ATRPeriod': 49,  # Период медленного ATR
        'ATRShift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

