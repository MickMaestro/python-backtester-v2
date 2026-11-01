"""RSICandleV2 — converted from MQL5: MQL5 Indicators/RSICandleV2/RSICandleV2.mq5

RSICandle Smoothed
Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [255, 15631086, 16760576, 16711680]}, 'widths': {}, 'styles': {}, 'labels': {1: 'RSICandle Open;RSICandle High;RSICandle Low;RSICandle Close'}, 'levels': [], 'description': ['RSICandle Smoothed'], 'name': 'RSICandleV2', 'source': 'MQL5 Indicators/RSICandleV2/RSICandleV2.mq5', 'folder': 'RSICandleV2', 'inputs': [{'mql': 'RSI_Period', 'py': 'RSI_Period', 'param': 'RSI_Period', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'uint', 'default': 60, 'label': 'уровень перекупленности', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'uint', 'default': 40, 'label': 'уровень перепроданности', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RSI_Period = _input('RSI_Period', 14)
HighLevel = _input('HighLevel', 60)  # уровень перекупленности
LowLevel = _input('LowLevel', 40)  # уровень перепроданности
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
RSI_Handle = Arr(4, 0, dyn=False)

def OnInit():
    global min_rates_total
    min_rates_total = _int(RSI_Period)
    RSI_Handle[0] = iRSI(None, 0, RSI_Period, PRICE_OPEN)
    if RSI_Handle[0] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI[' + _str(0) + ']!')
    RSI_Handle[1] = iRSI(None, 0, RSI_Period, PRICE_HIGH)
    if RSI_Handle[1] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI[' + _str(1) + ']!')
    RSI_Handle[2] = iRSI(None, 0, RSI_Period, PRICE_LOW)
    if RSI_Handle[2] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI[' + _str(2) + ']!')
    RSI_Handle[3] = iRSI(None, 0, RSI_Period, PRICE_CLOSE)
    if RSI_Handle[3] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI[' + _str(3) + ']!')
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
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    short_name = 'RSICandleV2'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, MathMin(100, HighLevel))
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, MathMax(0, LowLevel))
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (((BarsCalculated(RSI_Handle[0]) < rates_total or BarsCalculated(RSI_Handle[1]) < rates_total) or BarsCalculated(RSI_Handle[2]) < rates_total) or BarsCalculated(RSI_Handle[3]) < rates_total) or rates_total < min_rates_total:
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
    if CopyBuffer(RSI_Handle[0], 0, 0, to_copy, ExtOpenBuffer) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[1], 0, 0, to_copy, ExtHighBuffer) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[2], 0, 0, to_copy, ExtLowBuffer) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[3], 0, 0, to_copy, ExtCloseBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Max = MathMax(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        Min = MathMin(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        ExtHighBuffer[bar] = MathMax(Max, ExtHighBuffer[bar])
        Max = ExtHighBuffer[bar]
        ExtLowBuffer[bar] = MathMin(Min, ExtLowBuffer[bar])
        Min = ExtLowBuffer[bar]
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            if Max > HighLevel or (Max > LowLevel and Min <= LowLevel):
                clr = 3
            else:
                clr = 2
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            if Min < LowLevel or (Max > HighLevel and Min <= HighLevel):
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


class RSICandleV2(_MQL5Indicator):
    name = 'RSICandleV2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSI_Period': 14,
        'HighLevel': 60,  # уровень перекупленности
        'LowLevel': 40,  # уровень перепроданности
    }

