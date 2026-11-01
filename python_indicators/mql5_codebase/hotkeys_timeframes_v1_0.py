"""Hotkeys_TimeFrames_v1.0 — converted from MQL5: MQL5 Indicators/Hotkeys_TimeFrames_v1.0/Hotkeys_TimeFrames_v1.0.mq5

Hotkeys Timeframes 1-9 numbers on keyboard but not on number-pad.
1=m1, 2=m5, 3=m15, 4=m30, 5=h1, 6=h4, 7=d1, 8=w1, 9=mn .
Copyright: Copyright 2021, NickBixy; Link: https://www.forexfactory.com/showthread.php?t=904734; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2021, NickBixy', 'link': 'https://www.forexfactory.com/showthread.php?t=904734', 'version': '1.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Hotkeys Timeframes 1-9 numbers on keyboard but not on number-pad.', '1=m1, 2=m5, 3=m15, 4=m30, 5=h1, 6=h4, 7=d1, 8=w1, 9=mn .'], 'name': 'Hotkeys_TimeFrames_v1.0', 'source': 'MQL5 Indicators/Hotkeys_TimeFrames_v1.0/Hotkeys_TimeFrames_v1.0.mq5', 'folder': 'Hotkeys_TimeFrames_v1.0', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}


def OnInit():
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ == CHARTEVENT_KEYDOWN:
        _sw1 = _int(lparam)
        if _sw1 == 49:
            ChartSetSymbolPeriod(0, None, PERIOD_M1)
        elif _sw1 == 50:
            ChartSetSymbolPeriod(0, None, PERIOD_M5)
        elif _sw1 == 51:
            ChartSetSymbolPeriod(0, None, PERIOD_M15)
        elif _sw1 == 52:
            ChartSetSymbolPeriod(0, None, PERIOD_M30)
        elif _sw1 == 53:
            ChartSetSymbolPeriod(0, None, PERIOD_H1)
        elif _sw1 == 54:
            ChartSetSymbolPeriod(0, None, PERIOD_H4)
        elif _sw1 == 55:
            ChartSetSymbolPeriod(0, None, PERIOD_D1)
        elif _sw1 == 56:
            ChartSetSymbolPeriod(0, None, PERIOD_W1)
        elif _sw1 == 57:
            ChartSetSymbolPeriod(0, None, PERIOD_MN1)
        ChartRedraw()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HotkeysTimeFramesV10(_MQL5Indicator):
    name = 'Hotkeys_TimeFrames_v1.0'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

