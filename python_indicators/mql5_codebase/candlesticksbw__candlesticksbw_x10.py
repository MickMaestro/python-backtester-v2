"""CandlesticksBW — converted from MQL5: MQL5 Indicators/CandlesticksBW_x10/CandlesticksBW.mq5

CandlesticksBW
Copyright: Copyright © 2008, Vladimir; Link: finance@allmotion.com.ua; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, Vladimir', 'link': 'finance@allmotion.com.ua', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16776960, 16711680, 32768, 255, 8388736, 16711935]}, 'widths': {}, 'styles': {}, 'labels': {1: 'CandlesticksBW/Open;High;Low;Close'}, 'levels': [], 'description': ['CandlesticksBW'], 'name': 'CandlesticksBW', 'source': 'MQL5 Indicators/CandlesticksBW_x10/CandlesticksBW.mq5', 'folder': 'CandlesticksBW_x10', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
AC_Handle = 0
AO_Handle = 0

def OnInit():
    global AC_Handle, AO_Handle, min_rates_total
    min_rates_total = 34 + 2
    AO_Handle = iAO(Symbol(), PERIOD_CURRENT)
    if AO_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора   Awesome oscillator')
        return INIT_FAILED
    AC_Handle = iAC(Symbol(), PERIOD_CURRENT)
    if AC_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора  Accelerator Oscillator')
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
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'CandlesticksBW'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(AO_Handle) < rates_total or BarsCalculated(AC_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    AO = Arr(0, 0.0)
    AC = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyOpen(Symbol(), PERIOD_CURRENT, 0, to_copy, ExtOpenBuffer) <= 0:
        return 0
    if CopyHigh(Symbol(), PERIOD_CURRENT, 0, to_copy, ExtHighBuffer) <= 0:
        return 0
    if CopyLow(Symbol(), PERIOD_CURRENT, 0, to_copy, ExtLowBuffer) <= 0:
        return 0
    if CopyClose(Symbol(), PERIOD_CURRENT, 0, to_copy, ExtCloseBuffer) <= 0:
        return 0
    to_copy += 1
    if CopyBuffer(AO_Handle, 0, 0, to_copy, AO) <= 0:
        return 0
    if CopyBuffer(AC_Handle, 0, 0, to_copy, AC) <= 0:
        return 0
    ArraySetAsSeries(AO, True)
    ArraySetAsSeries(AC, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        clr = 0
        if AO[bar] >= AO[bar + 1] and AC[bar] >= AC[bar + 1]:
            if open[bar] <= close[bar]:
                clr = 0
            else:
                clr = 1
        elif AO[bar] <= AO[bar + 1] and AC[bar] <= AC[bar + 1]:
            if open[bar] >= close[bar]:
                clr = 5
            else:
                clr = 4
        else:
            if open[bar] <= close[bar]:
                clr = 2
            else:
                clr = 3
        ExtColorBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandlesticksBW(_MQL5Indicator):
    name = 'CandlesticksBW'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

