"""rsicloud — converted from MQL5: MQL5 Indicators/RSICloud_HTF/rsicloud.mq5

Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [13688896, 55295]}, 'widths': {}, 'styles': {}, 'labels': {1: 'RSICloud'}, 'levels': [70.0, 50.0, 30.0], 'description': [], 'name': 'rsicloud', 'source': 'MQL5 Indicators/RSICloud_HTF/rsicloud.mq5', 'folder': 'RSICloud_HTF', 'inputs': [{'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'uint', 'default': 14, 'label': 'Период RSI индикатора', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RSIPeriod = _input('RSIPeriod', 14)  # Период RSI индикатора
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
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
    SetIndexBuffer(0, ExtABuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtABuffer, True)
    SetIndexBuffer(1, ExtBBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtBBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSICloud')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (rates_total < min_rates_total or BarsCalculated(IndA_Handle) < rates_total) or BarsCalculated(IndB_Handle) < rates_total:
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated + 1
    if CopyBuffer(IndA_Handle, 0, 0, to_copy, ExtABuffer) <= 0:
        return 0
    if CopyBuffer(IndB_Handle, 0, 0, to_copy, ExtBBuffer) <= 0:
        return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Rsicloud(_MQL5Indicator):
    name = 'rsicloud'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSIPeriod': 14,  # Период RSI индикатора
    }

