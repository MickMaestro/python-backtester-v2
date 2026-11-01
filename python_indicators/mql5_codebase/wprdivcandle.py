"""WPRdivCandle — converted from MQL5: MQL5 Indicators/WPRdivCandle/WPRdivCandle.mq5

Индикатор окрашивает свечи на основе осциллятора WPR
Copyright: Copyright © 2006, RickD; Link: http://e2e-fx.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, RickD', 'link': 'http://e2e-fx.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [55295, 3937500, 8421504, 16748574, 16776960]}, 'widths': {}, 'styles': {}, 'labels': {1: 'WPRdivCandle Open;WPRdivCandle High;WPRdivCandle Low;WPRdivCandle Close'}, 'levels': [], 'description': ['Индикатор окрашивает свечи на основе осциллятора WPR'], 'name': 'WPRdivCandle', 'source': 'MQL5 Indicators/WPRdivCandle/WPRdivCandle.mq5', 'folder': 'WPRdivCandle', 'inputs': [{'mql': 'WPRPeriod', 'py': 'WPRPeriod', 'param': 'WPRPeriod', 'type': 'uint', 'default': 14, 'label': 'период индикатора', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': -20, 'label': 'уровень перезакупа', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -80, 'label': 'уровень перепроданности', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
WPRPeriod = _input('WPRPeriod', 14)  # период индикатора
HighLevel = _input('HighLevel', -20)  # уровень перезакупа
LowLevel = _input('LowLevel', -80)  # уровень перепроданности
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
WPRchastic_Handle = 0

def OnInit():
    global WPRchastic_Handle, min_rates_total
    min_rates_total = _int(WPRPeriod)
    WPRchastic_Handle = iWPR(None, 0, WPRPeriod)
    if WPRchastic_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iWPR')
        return INIT_FAILED
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'WPRdivCandle'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(WPRchastic_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    clr = 0
    WPR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(WPRchastic_Handle, MAIN_LINE, 0, to_copy, WPR) <= 0:
        return 0
    if CopyOpen(Symbol(), PERIOD_CURRENT, 0, to_copy, ExtOpenBuffer) <= 0:
        return 0
    if CopyHigh(Symbol(), PERIOD_CURRENT, 0, to_copy, ExtHighBuffer) <= 0:
        return 0
    if CopyLow(Symbol(), PERIOD_CURRENT, 0, to_copy, ExtLowBuffer) <= 0:
        return 0
    if CopyClose(Symbol(), PERIOD_CURRENT, 0, to_copy, ExtCloseBuffer) <= 0:
        return 0
    ArraySetAsSeries(WPR, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        clr = 2
        if WPR[bar] > HighLevel:
            clr = 4
        elif WPR[bar] < LowLevel:
            clr = 0
        elif WPR[bar] > -50:
            clr = 3
        elif WPR[bar] < -50:
            clr = 1
        ExtColorBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WPRdivCandle(_MQL5Indicator):
    name = 'WPRdivCandle'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'WPRPeriod': 14,  # период индикатора
        'HighLevel': -20,  # уровень перезакупа
        'LowLevel': -80,  # уровень перепроданности
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

