"""stream — converted from MQL5: MQL5 Indicators/Stream/stream.mq5

Copyright: Copyright © 2016, Yuriy Tokman (YTG); Link: В расчет принимается тело бара, цена открытия и цена закрытия бара.; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Yuriy Tokman (YTG)', 'link': 'В расчет принимается тело бара, цена открытия и цена закрытия бара.', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'Stream Sell', 2: 'Stream Buy'}, 'levels': [], 'description': [], 'name': 'stream', 'source': 'MQL5 Indicators/Stream/stream.mq5', 'folder': 'Stream', 'inputs': [{'mql': 'Bars_Size', 'py': 'Bars_Size', 'param': 'Bars_Size', 'type': 'uint', 'default': 100, 'label': 'Минимальный размер тела бара для срабатывания', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Bars_Size = _input('Bars_Size', 100)  # Минимальный размер тела бара для срабатывания
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
dBars_Size = 0.0
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, dBars_Size, min_rates_total
    ATR_Period = 15
    min_rates_total = ATR_Period
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    dBars_Size = Bars_Size * Point()
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 226)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 225)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Stream(' + _str(Bars_Size) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    range_ = 0.0
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        range_ = close[bar] - open[bar]
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if range_ > dBars_Size:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if range_ < (-dBars_Size):
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Stream(_MQL5Indicator):
    name = 'stream'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Bars_Size': 100,  # Минимальный размер тела бара для срабатывания
    }

