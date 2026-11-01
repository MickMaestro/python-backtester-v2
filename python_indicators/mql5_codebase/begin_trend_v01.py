"""begin_trend_v01 — converted from MQL5: MQL5 Indicators/Begin_Trend_v01/begin_trend_v01.mq5

Copyright: Copyright © 2014, Inkov Evgeni; Link: ew123@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Inkov Evgeni', 'link': 'ew123@mail.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [3329330], 2: [255]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Begin_Trend_v01 Up', 2: 'Begin_Trend_v01 Down'}, 'levels': [0.0], 'description': [], 'name': 'begin_trend_v01', 'source': 'MQL5 Indicators/Begin_Trend_v01/begin_trend_v01.mq5', 'folder': 'Begin_Trend_v01', 'inputs': [{'mql': 'Period_Channel', 'py': 'Period_Channel', 'param': 'Period_Channel', 'type': 'uint', 'default': 70, 'label': '', 'sinput': False}, {'mql': 'Period_Input', 'py': 'Period_Input', 'param': 'Period_Input', 'type': 'uint', 'default': 48, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Period_Channel = _input('Period_Channel', 70)
Period_Input = _input('Period_Input', 48)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
Up_Handle = 0
Dn_Handle = 0
Md_Handle = 0
min_rates_total = 0

def OnInit():
    global Dn_Handle, Md_Handle, Up_Handle, min_rates_total
    min_rates_total = _int(MathMax(Period_Channel, Period_Input))
    Up_Handle = iMA(None, 0, Period_Channel, 0, MODE_LWMA, PRICE_HIGH)
    if Up_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    Md_Handle = iMA(None, 0, Period_Input, 0, MODE_SMA, PRICE_CLOSE)
    if Md_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    Dn_Handle = iMA(None, 0, Period_Channel, 0, MODE_LWMA, PRICE_LOW)
    if Dn_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(DnBuffer, True)
    shortname = 'Begin_Trend_v01'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((BarsCalculated(Up_Handle) < rates_total or BarsCalculated(Md_Handle) < rates_total) or BarsCalculated(Dn_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    Up = Arr(0, 0.0)
    Md = Arr(0, 0.0)
    Dn = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 2
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Up_Handle, 0, 0, to_copy, Up) <= 0:
        return 0
    if CopyBuffer(Md_Handle, 0, 0, to_copy, Md) <= 0:
        return 0
    if CopyBuffer(Dn_Handle, 0, 0, to_copy, Dn) <= 0:
        return 0
    ArraySetAsSeries(Up, True)
    ArraySetAsSeries(Md, True)
    ArraySetAsSeries(Dn, True)
    for bar in range(limit, 0 - 1, -1):
        UpBuffer[bar] = Up[bar] - Md[bar]
        DnBuffer[bar] = Dn[bar] - Md[bar]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BeginTrendV01(_MQL5Indicator):
    name = 'begin_trend_v01'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period_Channel': 70,
        'Period_Input': 48,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

