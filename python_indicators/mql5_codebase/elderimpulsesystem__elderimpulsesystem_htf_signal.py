"""elderimpulsesystem — converted from MQL5: MQL5 Indicators/ElderImpulseSystem_HTF_Signal/elderimpulsesystem.mq5

Elder Impulse System
Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16711680, 255, 32768]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Open; High; Low; Close'}, 'levels': [], 'description': ['Elder Impulse System'], 'name': 'elderimpulsesystem', 'source': 'MQL5 Indicators/ElderImpulseSystem_HTF_Signal/elderimpulsesystem.mq5', 'folder': 'ElderImpulseSystem_HTF_Signal', 'inputs': [{'mql': 'ma_period', 'py': 'ma_period', 'param': 'ma_period', 'type': 'int', 'default': 13, 'label': 'Period of MA', 'sinput': False}, {'mql': 'fast_ema_period', 'py': 'fast_ema_period', 'param': 'fast_ema_period', 'type': 'int', 'default': 12, 'label': 'MACD fast period', 'sinput': False}, {'mql': 'slow_ema_period', 'py': 'slow_ema_period', 'param': 'slow_ema_period', 'type': 'int', 'default': 26, 'label': 'MACD slow period', 'sinput': False}, {'mql': 'signal_period', 'py': 'signal_period', 'param': 'signal_period', 'type': 'int', 'default': 9, 'label': 'MACD signal period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ma_period = _input('ma_period', 13)  # Period of MA
fast_ema_period = _input('fast_ema_period', 12)  # MACD fast period
slow_ema_period = _input('slow_ema_period', 26)  # MACD slow period
signal_period = _input('signal_period', 9)  # MACD signal period
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
MA_Handle = 0
MACD_Handle = 0

def OnInit():
    global MACD_Handle, MA_Handle, min_rates_total
    min_rates_total = MathMax(ma_period, signal_period + 1) + 2
    MA_Handle = iMA(None, 0, ma_period, 0, MODE_EMA, PRICE_CLOSE)
    if MA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
    MACD_Handle = iMACD(None, 0, fast_ema_period, slow_ema_period, signal_period, PRICE_CLOSE)
    if MACD_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMACD indicator')
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = Box("")
    StringConcatenate(short_name, 'Elder Impuls System(', ma_period, ', ', fast_ema_period, ', ', slow_ema_period, ', ', signal_period, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, short_name.v)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(MA_Handle) < rates_total or BarsCalculated(MACD_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    MA = Arr(0, 0.0)
    MACDM = Arr(0, 0.0)
    MACDS = Arr(0, 0.0)
    dma = 0.0
    dmacd0 = 0.0
    dmacd1 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MA) <= 0:
        return 0
    if CopyBuffer(MACD_Handle, 0, 0, to_copy, MACDM) <= 0:
        return 0
    if CopyBuffer(MACD_Handle, 1, 0, to_copy, MACDS) <= 0:
        return 0
    ArraySetAsSeries(MA, True)
    ArraySetAsSeries(MACDM, True)
    ArraySetAsSeries(MACDS, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtOpenBuffer[bar] = open[bar]
        ExtCloseBuffer[bar] = close[bar]
        ExtHighBuffer[bar] = high[bar]
        ExtLowBuffer[bar] = low[bar]
        dma = MA[bar] - MA[bar + 1]
        dmacd0 = MACDM[bar] - MACDS[bar]
        dmacd1 = MACDM[bar + 1] - MACDS[bar + 1]
        if (dma > 0 and dmacd0 > dmacd1) and dmacd0 > 0:
            ExtColorBuffer[bar] = 2.0
        if (dma < 0 and dmacd0 < dmacd1) and dmacd0 < 0:
            ExtColorBuffer[bar] = 1.0
        if (((MA[bar] <= MA[bar + 1] and dmacd0 > 0) or (dma <= 0 and dmacd0 > dmacd1)) or (dma >= 0 and dmacd0 < 0)) or (dma >= 0 and dmacd0 < dmacd1):
            ExtColorBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Elderimpulsesystem(_MQL5Indicator):
    name = 'elderimpulsesystem'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ma_period': 13,  # Period of MA
        'fast_ema_period': 12,  # MACD fast period
        'slow_ema_period': 26,  # MACD slow period
        'signal_period': 9,  # MACD signal period
    }

