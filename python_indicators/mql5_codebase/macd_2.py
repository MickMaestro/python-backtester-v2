"""macd-2 — converted from MQL5: MQL5 Indicators/MACD-2/macd-2.mq5

MACD-2
Copyright: Copyright © 2005, MetaQuotes Software Corp.; Link: http://www.metaquotes.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 10}, 'colors': {1: [65280, 9639167], 2: [2763429, 15631086, 8421504, 16760576, 16711680]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'MACD_Cloud', 2: 'MACD'}, 'levels': [], 'description': ['MACD-2'], 'name': 'macd-2', 'source': 'MQL5 Indicators/MACD-2/macd-2.mq5', 'folder': 'MACD-2', 'inputs': [{'mql': 'FastMACD', 'py': 'FastMACD', 'param': 'FastMACD', 'type': 'uint', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'SlowMACD', 'py': 'SlowMACD', 'param': 'SlowMACD', 'type': 'uint', 'default': 26, 'label': '', 'sinput': False}, {'mql': 'SignalMACD', 'py': 'SignalMACD', 'param': 'SignalMACD', 'type': 'uint', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'PriceMACD', 'py': 'PriceMACD', 'param': 'PriceMACD', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FastMACD = _input('FastMACD', 12)
SlowMACD = _input('SlowMACD', 26)
SignalMACD = _input('SignalMACD', 9)
PriceMACD = _input('PriceMACD', PRICE_CLOSE)
min_rates_total = 0
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
MACD_Handle = 0

def OnInit():
    global MACD_Handle, min_rates_total
    min_rates_total = _int(SignalMACD + MathMax(FastMACD, SlowMACD))
    MACD_Handle = iMACD(None, 0, FastMACD, SlowMACD, SignalMACD, PriceMACD)
    if MACD_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of iMACD')
        return INIT_FAILED
    SetIndexBuffer(0, ExtABuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtABuffer, True)
    SetIndexBuffer(1, ExtBBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtBBuffer, True)
    SetIndexBuffer(2, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(3, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MACD-2')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if BarsCalculated(MACD_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(MACD_Handle, MAIN_LINE, 0, to_copy, ExtABuffer) <= 0:
        return 0
    if CopyBuffer(MACD_Handle, SIGNAL_LINE, 0, to_copy, ExtBBuffer) <= 0:
        return 0
    for bar in range(limit, 0 - 1, -1):
        ExtABuffer[bar] = _fdiv(ExtABuffer[bar], Point())
        ExtBBuffer[bar] = _fdiv(ExtBBuffer[bar], Point())
        IndBuffer[bar] = 3 * (ExtABuffer[bar] - ExtBBuffer[bar])
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    for bar in range(limit, 0 - 1, -1):
        clr = 2
        if IndBuffer[bar] > 0:
            if IndBuffer[bar] > IndBuffer[bar + 1]:
                clr = 4
            if IndBuffer[bar] < IndBuffer[bar + 1]:
                clr = 3
        if IndBuffer[bar] < 0:
            if IndBuffer[bar] < IndBuffer[bar + 1]:
                clr = 0
            if IndBuffer[bar] > IndBuffer[bar + 1]:
                clr = 1
        ColorIndBuffer[bar] = clr
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Macd2(_MQL5Indicator):
    name = 'macd-2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastMACD': 12,
        'SlowMACD': 26,
        'SignalMACD': 9,
        'PriceMACD': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
    }

