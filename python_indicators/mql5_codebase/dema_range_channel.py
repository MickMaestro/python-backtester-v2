"""DEMA_Range_Channel — converted from MQL5: MQL5 Indicators/DEMA_Range_Channel_HTF/DEMA_Range_Channel.mq5

DEMA Range Channel
Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.02', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 17}, 'colors': {1: [16443110], 2: [16711680], 3: [255], 4: [16711935, 2763429, 16711680, 16776960]}, 'widths': {2: 1, 3: 1}, 'styles': {2: 0, 3: 0}, 'labels': {1: 'DEMA Range Channel', 2: 'Up Line', 3: 'Down Line', 4: 'Open;High;Low;Close'}, 'levels': [], 'description': ['DEMA Range Channel'], 'name': 'DEMA_Range_Channel', 'source': 'MQL5 Indicators/DEMA_Range_Channel_HTF/DEMA_Range_Channel.mq5', 'folder': 'DEMA_Range_Channel_HTF', 'inputs': [{'mql': 'ma_period', 'py': 'ma_period', 'param': 'ma_period', 'type': 'uint', 'default': 14, 'label': 'Период усреднения', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'uint', 'default': 3, 'label': 'сдвиг по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ma_period = _input('ma_period', 14)  # Период усреднения
Shift = _input('Shift', 3)  # сдвиг по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг по вертикали в пунктах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
UpLineBuffer = Arr(0, 0.0)
DnLineBuffer = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0
HInd_Handle = 0
LInd_Handle = 0

def OnInit():
    global HInd_Handle, LInd_Handle, dPriceShift, min_rates_total
    min_rates_total = _int(ma_period * 2)
    dPriceShift = Point() * PriceShift
    HInd_Handle = iDEMA(Symbol(), PERIOD_CURRENT, ma_period, 0, PRICE_HIGH)
    if HInd_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора DEMA PRICE_HIGH')
        return INIT_FAILED
    LInd_Handle = iDEMA(Symbol(), PERIOD_CURRENT, ma_period, 0, PRICE_LOW)
    if LInd_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора DEMA PRICE_LOW')
        return INIT_FAILED
    SetIndexBuffer(0, UpIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, UpLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, DnLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    SetIndexBuffer(4, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(8, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    ArraySetAsSeries(UpIndBuffer, True)
    ArraySetAsSeries(DnIndBuffer, True)
    ArraySetAsSeries(UpLineBuffer, True)
    ArraySetAsSeries(DnLineBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'DEMA_Range_Channel', ma_period, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(HInd_Handle) < rates_total or BarsCalculated(LInd_Handle) < rates_total:
        return prev_calculated
    to_copy = 0
    limit = 0
    HDEMA = Arr(0, 0.0)
    LDEMA = Arr(0, 0.0)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(HDEMA, True)
    ArraySetAsSeries(LDEMA, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(HInd_Handle, 0, 0, to_copy, UpLineBuffer) <= 0:
        return 0
    if CopyBuffer(LInd_Handle, 0, 0, to_copy, DnLineBuffer) <= 0:
        return 0
    if CopyBuffer(HInd_Handle, 0, 0, to_copy, UpIndBuffer) <= 0:
        return 0
    if CopyBuffer(LInd_Handle, 0, 0, to_copy, DnIndBuffer) <= 0:
        return 0
    for bar in range(limit, 0 - 1, -1):
        UpIndBuffer[bar] += dPriceShift
        UpLineBuffer[bar] = UpIndBuffer[bar]
        DnIndBuffer[bar] -= dPriceShift
        DnLineBuffer[bar] = DnIndBuffer[bar]
    for bar in range(limit, 0 - 1, -1):
        ExtColorBuffer[bar] = EMPTY_VALUE
        ExtLowBuffer[bar] = ExtColorBuffer[bar]
        ExtHighBuffer[bar] = ExtLowBuffer[bar]
        ExtCloseBuffer[bar] = ExtHighBuffer[bar]
        ExtOpenBuffer[bar] = ExtCloseBuffer[bar]
        if close[bar] > UpLineBuffer[bar + Shift]:
            ExtOpenBuffer[bar] = open[bar]
            ExtCloseBuffer[bar] = close[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
            if close[bar] >= open[bar]:
                ExtColorBuffer[bar] = 3.0
            else:
                ExtColorBuffer[bar] = 2.0
        if close[bar] < DnLineBuffer[bar + Shift]:
            ExtOpenBuffer[bar] = open[bar]
            ExtCloseBuffer[bar] = close[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
            if close[bar] <= open[bar]:
                ExtColorBuffer[bar] = 0.0
            else:
                ExtColorBuffer[bar] = 1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DEMARangeChannel(_MQL5Indicator):
    name = 'DEMA_Range_Channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ma_period': 14,  # Период усреднения
        'Shift': 3,  # сдвиг по горизонтали в барах
        'PriceShift': 0,  # cдвиг по вертикали в пунктах
    }

