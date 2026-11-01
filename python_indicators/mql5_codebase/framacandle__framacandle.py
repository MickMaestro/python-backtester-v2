"""framacandle — converted from MQL5: MQL5 Indicators/FrAMACandle/framacandle.mq5

FrAMACandle Smoothed
Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [9639167, 8421504, 16748574]}, 'widths': {}, 'styles': {}, 'labels': {1: 'FrAMACandle Open;FrAMACandle High;FrAMACandle Low;FrAMACandle Close'}, 'levels': [], 'description': ['FrAMACandle Smoothed'], 'name': 'framacandle', 'source': 'MQL5 Indicators/FrAMACandle/framacandle.mq5', 'folder': 'FrAMACandle', 'inputs': [{'mql': 'FrAMA_Period', 'py': 'FrAMA_Period', 'param': 'FrAMA_Period', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FrAMA_Period = _input('FrAMA_Period', 14)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
FrAMA_Handle = Arr(4, 0, dyn=False)

def OnInit():
    global min_rates_total
    min_rates_total = _int(FrAMA_Period)
    FrAMA_Handle[0] = iFrAMA(None, 0, FrAMA_Period, 0, PRICE_OPEN)
    if FrAMA_Handle[0] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iFrAMA[' + _str(0) + ']!')
    FrAMA_Handle[1] = iFrAMA(None, 0, FrAMA_Period, 0, PRICE_HIGH)
    if FrAMA_Handle[1] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iFrAMA[' + _str(1) + ']!')
    FrAMA_Handle[2] = iFrAMA(None, 0, FrAMA_Period, 0, PRICE_LOW)
    if FrAMA_Handle[2] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iFrAMA[' + _str(2) + ']!')
    FrAMA_Handle[3] = iFrAMA(None, 0, FrAMA_Period, 0, PRICE_CLOSE)
    if FrAMA_Handle[3] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iFrAMA[' + _str(3) + ']!')
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
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'FrAMACandl'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (((BarsCalculated(FrAMA_Handle[0]) < rates_total or BarsCalculated(FrAMA_Handle[1]) < rates_total) or BarsCalculated(FrAMA_Handle[2]) < rates_total) or BarsCalculated(FrAMA_Handle[3]) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    clr = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(FrAMA_Handle[0], 0, 0, to_copy, ExtOpenBuffer) <= 0:
        return 0
    if CopyBuffer(FrAMA_Handle[1], 0, 0, to_copy, ExtHighBuffer) <= 0:
        return 0
    if CopyBuffer(FrAMA_Handle[2], 0, 0, to_copy, ExtLowBuffer) <= 0:
        return 0
    if CopyBuffer(FrAMA_Handle[3], 0, 0, to_copy, ExtCloseBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Max = MathMax(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        Min = MathMin(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        ExtHighBuffer[bar] = MathMax(Max, ExtHighBuffer[bar])
        ExtLowBuffer[bar] = MathMin(Min, ExtLowBuffer[bar])
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            clr = 2
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            clr = 0
        else:
            clr = 1
        ExtColorBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Framacandle(_MQL5Indicator):
    name = 'framacandle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FrAMA_Period': 14,
    }

