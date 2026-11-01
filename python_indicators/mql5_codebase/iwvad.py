"""iWVAD — converted from MQL5: MQL5 Indicators/Larry Williams' Variable Accumulation Distribution (WVAD) Indicator/iWVAD.mq5

Copyright: Arthur Albano; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Arthur Albano', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'iWVAD'}, 'levels': [], 'description': [], 'name': 'iWVAD', 'source': "MQL5 Indicators/Larry Williams' Variable Accumulation Distribution (WVAD) Indicator/iWVAD.mq5", 'folder': "Larry Williams' Variable Accumulation Distribution (WVAD) Indicator", 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
iWVAD = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, iWVAD, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, "Larry Williams' iWVAD")
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return 0
    Ask = SymbolInfoDouble(Symbol(), SYMBOL_ASK)
    Bid = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    i = MathMax(prev_calculated - 1, 0)
    while (i < rates_total and (not False)) and Ask > Bid:
        iWVAD[i] = ((_fdiv(close[i] - open[i], high[i] - low[i]) * (volume[i] if (volume[i] > 0) else tick_volume[i] if (tick_volume[i] > 0) else 1)) if (high[i] > low[i]) else None)
        i += 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IWVAD(_MQL5Indicator):
    name = 'iWVAD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

