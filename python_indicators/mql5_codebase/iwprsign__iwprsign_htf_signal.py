"""iWPRSign — converted from MQL5: MQL5 Indicators/iWPRSign_HTF_Signal/iWPRSign.mq5

Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [36095], 2: [15570276]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'iWPRSign Sell', 2: 'iWPRSign Buy'}, 'levels': [], 'description': [], 'name': 'iWPRSign', 'source': 'MQL5 Indicators/iWPRSign_HTF_Signal/iWPRSign.mq5', 'folder': 'iWPRSign_HTF_Signal', 'inputs': [{'mql': 'ATR_Period', 'py': 'ATR_Period', 'param': 'ATR_Period', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'WPRPeriod', 'py': 'WPRPeriod', 'param': 'WPRPeriod', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'UpLevel', 'py': 'UpLevel', 'param': 'UpLevel', 'type': 'int', 'default': -30, 'label': 'уровень перекупленности', 'sinput': False}, {'mql': 'DnLevel', 'py': 'DnLevel', 'param': 'DnLevel', 'type': 'int', 'default': -70, 'label': 'уровень перепроданности', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ATR_Period = _input('ATR_Period', 14)
WPRPeriod = _input('WPRPeriod', 14)
UpLevel = _input('UpLevel', -30)  # уровень перекупленности
DnLevel = _input('DnLevel', -70)  # уровень перепроданности
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
WPR_Handle = 0
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, WPR_Handle, min_rates_total
    min_rates_total = _int(MathMax(WPRPeriod + 1, ATR_Period)) + 1
    WPR_Handle = iWPR(Symbol(), None, WPRPeriod)
    if WPR_Handle == INVALID_HANDLE:
        Print('Не удалось получить хендл индикатора WPRPeriod')
        return INIT_FAILED
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 175)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 175)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'iWPRSign'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(WPR_Handle) < rates_total or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    WPR = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(WPR_Handle, 0, MAIN_LINE, to_copy + 1, WPR) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(WPR, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if WPR[bar] > DnLevel and WPR[bar + 1] <= DnLevel:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if WPR[bar] < UpLevel and WPR[bar + 1] >= UpLevel:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IWPRSign(_MQL5Indicator):
    name = 'iWPRSign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ATR_Period': 14,
        'WPRPeriod': 14,
        'UpLevel': -30,  # уровень перекупленности
        'DnLevel': -70,  # уровень перепроданности
    }

