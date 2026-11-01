"""begin_trend_v02 — converted from MQL5: MQL5 Indicators/Begin_Trend_v02_HTF/begin_trend_v02.mq5

Copyright: Copyright © 2014, Inkov Evgeni; Link: ew123@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Inkov Evgeni', 'link': 'ew123@mail.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 3, 4: 3}, 'colors': {1: [3329330], 2: [255], 3: [65280], 4: [255]}, 'widths': {1: 2, 2: 2, 3: 4, 4: 4}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Begin_Trend_v02 Up', 2: 'Begin_Trend_v02 Down', 3: 'Begin_Trend_v02 Up', 4: 'Begin_Trend_v02 Down'}, 'levels': [100.0, 50.0, 0.0, -50.0, -100.0], 'description': [], 'name': 'begin_trend_v02', 'source': 'MQL5 Indicators/Begin_Trend_v02_HTF/begin_trend_v02.mq5', 'folder': 'Begin_Trend_v02_HTF', 'inputs': [{'mql': 'Period_Channel', 'py': 'Period_Channel', 'param': 'Period_Channel', 'type': 'uint', 'default': 70, 'label': '', 'sinput': False}, {'mql': 'Period_Input', 'py': 'Period_Input', 'param': 'Period_Input', 'type': 'uint', 'default': 48, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Period_Channel = _input('Period_Channel', 70)
Period_Input = _input('Period_Input', 48)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Up1Buffer = Arr(0, 0.0)
Dn1Buffer = Arr(0, 0.0)
Up2Buffer = Arr(0, 0.0)
Dn2Buffer = Arr(0, 0.0)
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
    SetIndexBuffer(0, Up1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Up1Buffer, True)
    SetIndexBuffer(1, Dn1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Dn1Buffer, True)
    SetIndexBuffer(2, Up2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Up2Buffer, True)
    SetIndexBuffer(3, Dn2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Dn2Buffer, True)
    shortname = 'Begin_Trend_v02'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
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
        d = MathMax(MathAbs(Up[bar] - Dn[bar]), MathMax(MathAbs(Up[bar] - Md[bar]), MathAbs(Dn[bar] - Md[bar])))
        if not d:
            d = 1e-10
        Up1Buffer[bar] = _fdiv(Up[bar] - Md[bar], d) * 100.0
        Dn1Buffer[bar] = _fdiv(Dn[bar] - Md[bar], d) * 100.0
        Up2Buffer[bar] = EMPTY_VALUE
        Dn2Buffer[bar] = EMPTY_VALUE
        if Up1Buffer[bar] < 0:
            Dn2Buffer[bar] = Up1Buffer[bar]
        if Dn1Buffer[bar] > 0:
            Up2Buffer[bar] = Dn1Buffer[bar]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BeginTrendV02(_MQL5Indicator):
    name = 'begin_trend_v02'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period_Channel': 70,
        'Period_Input': 48,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

