"""MACDCandleTrend — converted from MQL5: MQL5 Indicators/MACDCandleTrend/MACDCandleTrend.mq5

Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [3329330]}, 'widths': {1: 5, 2: 5}, 'styles': {}, 'labels': {1: 'MACDCandleTrend Sell', 2: 'MACDCandleTrend Buy'}, 'levels': [], 'description': [], 'name': 'MACDCandleTrend', 'source': 'MQL5 Indicators/MACDCandleTrend/MACDCandleTrend.mq5', 'folder': 'MACDCandleTrend', 'inputs': [{'mql': 'fast_ema_period', 'py': 'fast_ema_period', 'param': 'fast_ema_period', 'type': 'uint', 'default': 12, 'label': 'период быстрой средней', 'sinput': False}, {'mql': 'slow_ema_period', 'py': 'slow_ema_period', 'param': 'slow_ema_period', 'type': 'uint', 'default': 26, 'label': 'период медленной средней', 'sinput': False}, {'mql': 'signal_period', 'py': 'signal_period', 'param': 'signal_period', 'type': 'uint', 'default': 9, 'label': 'период усреднения разности', 'sinput': False}, {'mql': 'mode', 'py': 'mode', 'param': 'mode', 'type': 'int', 'default': 1, 'label': 'источник даных для расчёта', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum MODE
MODE_HISTOGRAM = 0
MODE_SIGNAL_LINE = 1
_enum('MODE', {0: 'MODE_HISTOGRAM', 1: 'MODE_SIGNAL_LINE'})

# ---- inputs and global variables
fast_ema_period = _input('fast_ema_period', 12)  # период быстрой средней
slow_ema_period = _input('slow_ema_period', 26)  # период медленной средней
signal_period = _input('signal_period', 9)  # период усреднения разности
mode = _input('mode', MODE_SIGNAL_LINE)  # источник даных для расчёта
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
OMacd_Handle = 0
CMacd_Handle = 0
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, CMacd_Handle, OMacd_Handle, min_rates_total
    min_rates_total = _int(MathMax(fast_ema_period, slow_ema_period)) + 1
    if mode == MODE_SIGNAL_LINE:
        min_rates_total += _int(signal_period)
    ATR_Period = 15
    min_rates_total = MathMax(min_rates_total, ATR_Period) + 1
    OMacd_Handle = iMACD(None, 0, fast_ema_period, slow_ema_period, signal_period, PRICE_OPEN)
    if OMacd_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMACD[Open]!')
        return INIT_FAILED
    CMacd_Handle = iMACD(None, 0, fast_ema_period, slow_ema_period, signal_period, PRICE_CLOSE)
    if CMacd_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMACD[Close]!')
        return INIT_FAILED
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 82)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 82)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'MACDCandleTrend'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((BarsCalculated(OMacd_Handle) < rates_total or BarsCalculated(CMacd_Handle) < rates_total) or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    OMACD = Arr(0, 0.0)
    CMACD = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(OMacd_Handle, mode, 0, to_copy, OMACD) <= 0:
        return 0
    if CopyBuffer(CMacd_Handle, mode, 0, to_copy, CMACD) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(OMACD, True)
    ArraySetAsSeries(CMACD, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if OMACD[bar + 1] >= CMACD[bar + 1] and OMACD[bar] < CMACD[bar]:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if OMACD[bar + 1] <= CMACD[bar + 1] and OMACD[bar] > CMACD[bar]:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MACDCandleTrend(_MQL5Indicator):
    name = 'MACDCandleTrend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'fast_ema_period': 12,  # период быстрой средней
        'slow_ema_period': 26,  # период медленной средней
        'signal_period': 9,  # период усреднения разности
        'mode': _Choice({0: 'Гистограмма', 1: 'Сигнальная линия'}, default=1),  # источник даных для расчёта
    }

