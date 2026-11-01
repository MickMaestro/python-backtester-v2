"""BarSpread — converted from MQL5: MQL5 Indicators/Simple bar spread indicator as reported by the OnCalculate data/BarSpread.mq5

MName
MetaTrader Indicator (Build 
Copyright: MCopyright; Link: MProfile; Version: MVersion

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'version': 'MVersion', 'copyright': 'MCopyright', 'link': 'MProfile', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Spread (Bar)'}, 'levels': [], 'description': ['MName', 'MetaTrader Indicator (Build '], 'name': 'BarSpread', 'source': 'MQL5 Indicators/Simple bar spread indicator as reported by the OnCalculate data/BarSpread.mq5', 'folder': 'Simple bar spread indicator as reported by the OnCalculate data', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
g_adbSpread = Arr(0, 0.0)  # Buffer for bar's spread

def OnInit():
    IndicatorSetString(INDICATOR_SHORTNAME, 'Bar Spread')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    SetIndexBuffer(0, g_adbSpread, INDICATOR_DATA)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range((0 if (prev_calculated < 1) else (prev_calculated - 1)), rates_total):
        g_adbSpread[i] = spread[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BarSpread(_MQL5Indicator):
    name = 'BarSpread'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

