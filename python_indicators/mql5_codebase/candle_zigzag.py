"""Candle_ZigZag — converted from MQL5: MQL5 Indicators/Candle ZigZag/Candle_ZigZag.mq5

Copyright: Copyright 2024, Rajesh Kumar Nait; Link: https://www.mql5.com/en/users/rajeshnait/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, Rajesh Kumar Nait', 'link': 'https://www.mql5.com/en/users/rajeshnait/seller', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 13}, 'colors': {1: [9639167, 16775408]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'ZigZag Lowest;ZigZag Highest'}, 'levels': [], 'description': [], 'name': 'Candle_ZigZag', 'source': 'MQL5 Indicators/Candle ZigZag/Candle_ZigZag.mq5', 'folder': 'Candle ZigZag', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'int', 'default': 1, 'label': 'Candlestick period', 'sinput': False}, {'mql': 'modeclose', 'py': 'modeclose', 'param': 'modeclose', 'type': 'bool', 'default': False, 'label': 'Close Mode?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 1)  # Candlestick period
modeclose = _input('modeclose', False)  # Close Mode?
LowestBuffer = Arr(0, 0.0)
HighestBuffer = Arr(0, 0.0)
ZigZagColors = Arr(0, 0.0)
minRates = 0

def OnInit():
    global minRates
    minRates = InpPeriod
    SetIndexBuffer(0, LowestBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HighestBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ZigZagColors, INDICATOR_COLOR_INDEX)
    for i in range(0, 1):
        PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, minRates)
        PlotIndexSetInteger(i, PLOT_SHIFT, 0)
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Candle ZigZag (' + _str(InpPeriod) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate__highValue, _s_OnCalculate__lastHighPos, _s_OnCalculate__lastLowPos, _s_OnCalculate__lowValue, _s_OnCalculate__up
    startBar = 0
    lastHighPos = 0
    lastLowPos = 0
    highValue = 0.0
    lowValue = 0.0
    up = False
    if rates_total < minRates:
        Print('Not enough data to calculate')
        return 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        startBar = minRates
    else:
        startBar = prev_calculated - 1
    up = _s_OnCalculate__up
    highValue = _s_OnCalculate__highValue
    lowValue = _s_OnCalculate__lowValue
    lastHighPos = _s_OnCalculate__lastHighPos
    lastLowPos = _s_OnCalculate__lastLowPos
    for bar in range(startBar, rates_total):
        if rates_total != prev_calculated and bar == (rates_total - 1):
            _s_OnCalculate__up = up
            _s_OnCalculate__highValue = highValue
            _s_OnCalculate__lowValue = lowValue
            _s_OnCalculate__lastHighPos = lastHighPos
            _s_OnCalculate__lastLowPos = lastLowPos
        if up:
            ZigZagColors[bar] = 1.0
            if high[bar] > highValue and close[bar] > open[bar]:
                HighestBuffer[lastHighPos] = 0.0
                if modeclose:
                    highValue = close[bar]
                    HighestBuffer[bar] = highValue
                else:
                    highValue = high[bar]
                    HighestBuffer[bar] = highValue
                lastHighPos = bar
                LowestBuffer[bar] = 0.0
            elif close[bar] < open[bar]:
                up = False
                if modeclose:
                    lowValue = close[bar]
                    LowestBuffer[bar] = lowValue
                else:
                    lowValue = low[bar]
                    LowestBuffer[bar] = lowValue
                lastLowPos = bar
                HighestBuffer[bar] = 0.0
                ZigZagColors[bar] = 0.0
            else:
                HighestBuffer[bar] = 0.0
                LowestBuffer[bar] = 0.0
        else:
            ZigZagColors[bar] = 0.0
            if low[bar] < lowValue and close[bar] < open[bar]:
                LowestBuffer[lastLowPos] = 0.0
                if modeclose:
                    lowValue = close[bar]
                    LowestBuffer[bar] = lowValue
                else:
                    lowValue = low[bar]
                    LowestBuffer[bar] = lowValue
                lastLowPos = bar
                HighestBuffer[bar] = 0.0
            elif close[bar] > open[bar]:
                up = True
                if modeclose:
                    highValue = close[bar]
                    HighestBuffer[bar] = highValue
                else:
                    highValue = high[bar]
                    HighestBuffer[bar] = highValue
                lastHighPos = bar
                LowestBuffer[bar] = 0.0
                ZigZagColors[bar] = 1.0
            else:
                HighestBuffer[bar] = 0.0
                LowestBuffer[bar] = 0.0
    return rates_total

# ---- static local variables
_s_OnCalculate__lastHighPos = 0
_s_OnCalculate__lastLowPos = 0
_s_OnCalculate__highValue = 0.0
_s_OnCalculate__lowValue = 0.0
_s_OnCalculate__up = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleZigZag(_MQL5Indicator):
    name = 'Candle_ZigZag'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpPeriod': 1,  # Candlestick period
        'modeclose': False,  # Close Mode?
    }

