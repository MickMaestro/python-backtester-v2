"""RSICloudBg — converted from MQL5: MQL5 Indicators/RSICloudBG/RSICloudBg.mq5

Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 5, 'indicator_maximum': 100.0, 'indicator_minimum': 0.0}, 'types': {1: 7, 2: 7, 3: 7, 4: 7, 5: 7}, 'colors': {1: [13893506], 2: [15597514], 3: [16769535], 4: [16759295], 5: [3329330, 16711935]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Upper RSICloudBg_Cloud 2', 2: 'Upper RSICloudBg_Cloud 1', 3: 'Lower RSICloudBg_Cloud 1', 4: 'Lower RSICloudBg_Cloud 2', 5: 'RSICloud'}, 'levels': [], 'description': [], 'name': 'RSICloudBg', 'source': 'MQL5 Indicators/RSICloudBG/RSICloudBg.mq5', 'folder': 'RSICloudBG', 'inputs': [{'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'uint', 'default': 14, 'label': 'Период RSI индикатора', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'double', 'default': 70.0, 'label': 'уровень перезакупа', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'double', 'default': 30.0, 'label': 'уровень перепроданности', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RSIPeriod = _input('RSIPeriod', 14)  # Период RSI индикатора
HighLevel = _input('HighLevel', 70.0)  # уровень перезакупа
LowLevel = _input('LowLevel', 30.0)  # уровень перепроданности
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
UpUpBuffer1 = Arr(0, 0.0)
UpDnBuffer1 = Arr(0, 0.0)
DnUpBuffer1 = Arr(0, 0.0)
DnDnBuffer1 = Arr(0, 0.0)
UpUpBuffer2 = Arr(0, 0.0)
UpDnBuffer2 = Arr(0, 0.0)
DnUpBuffer2 = Arr(0, 0.0)
DnDnBuffer2 = Arr(0, 0.0)
IndA_Handle = 0
IndB_Handle = 0
min_rates_total = 0

def OnInit():
    global IndA_Handle, IndB_Handle, min_rates_total
    min_rates_total = _int(RSIPeriod)
    IndA_Handle = iRSI(Symbol(), PERIOD_CURRENT, RSIPeriod, PRICE_HIGH)
    if IndA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI HIGH')
        return INIT_FAILED
    IndB_Handle = iRSI(Symbol(), PERIOD_CURRENT, RSIPeriod, PRICE_LOW)
    if IndB_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI LOW')
        return INIT_FAILED
    IndInit(0, UpUpBuffer2, INDICATOR_DATA)
    IndInit(1, UpDnBuffer2, INDICATOR_DATA)
    PlotInit(0, EMPTY_VALUE, min_rates_total, 0)
    IndInit(2, UpUpBuffer1, INDICATOR_DATA)
    IndInit(3, UpDnBuffer1, INDICATOR_DATA)
    PlotInit(1, EMPTY_VALUE, min_rates_total, 0)
    IndInit(4, DnUpBuffer1, INDICATOR_DATA)
    IndInit(5, DnDnBuffer1, INDICATOR_DATA)
    PlotInit(2, EMPTY_VALUE, min_rates_total, 0)
    IndInit(6, DnUpBuffer2, INDICATOR_DATA)
    IndInit(7, DnDnBuffer2, INDICATOR_DATA)
    PlotInit(3, EMPTY_VALUE, min_rates_total, 0)
    IndInit(8, ExtABuffer, INDICATOR_DATA)
    IndInit(9, ExtBBuffer, INDICATOR_DATA)
    PlotInit(4, EMPTY_VALUE, min_rates_total, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSICloudBG(' + _str(RSIPeriod) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    PlotIndexSetInteger(Number, PLOT_SHOW_DATA, False)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (rates_total < min_rates_total or BarsCalculated(IndA_Handle) < rates_total) or BarsCalculated(IndB_Handle) < rates_total:
        return 0
    to_copy = 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(IndA_Handle, 0, 0, to_copy, ExtABuffer) <= 0:
        return 0
    if CopyBuffer(IndB_Handle, 0, 0, to_copy, ExtBBuffer) <= 0:
        return 0
    for bar in range(limit, 0 - 1, -1):
        UpUpBuffer2[bar] = 100.0
        UpDnBuffer2[bar] = HighLevel
        UpUpBuffer1[bar] = HighLevel
        UpDnBuffer1[bar] = 50.0
        DnUpBuffer1[bar] = 50.0
        DnDnBuffer1[bar] = LowLevel
        DnUpBuffer2[bar] = LowLevel
        DnDnBuffer2[bar] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSICloudBg(_MQL5Indicator):
    name = 'RSICloudBg'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSIPeriod': 14,  # Период RSI индикатора
        'HighLevel': 70.0,  # уровень перезакупа
        'LowLevel': 30.0,  # уровень перепроданности
    }
    y_range = (0.0, 100.0)

