"""Hotkeys_CycleTimeFrames_v1.0 — converted from MQL5: MQL5 Indicators/Hotkeys_CycleTimeFrames_v1.0/Hotkeys_CycleTimeFrames_v1.0.mq5

Hotkeys N, M To Cycle Through Timeframes.
M for next timeframe.
N for prev timeframe.
Copyright: NickBixy; Link: https://www.forexfactory.com/showthread.php?t=904734

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'NickBixy', 'link': 'https://www.forexfactory.com/showthread.php?t=904734', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Hotkeys N, M To Cycle Through Timeframes.', 'M for next timeframe.', 'N for prev timeframe.'], 'name': 'Hotkeys_CycleTimeFrames_v1.0', 'source': 'MQL5 Indicators/Hotkeys_CycleTimeFrames_v1.0/Hotkeys_CycleTimeFrames_v1.0.mq5', 'folder': 'Hotkeys_CycleTimeFrames_v1.0', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}


def OnInit():
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ == CHARTEVENT_KEYDOWN:
        _sw1 = _int(lparam)
        if _sw1 == 78:
            PrevTimeFrame()
        elif _sw1 == 77:
            NextTimeFrame()
        ChartRedraw()

def deinit():
    return 0

def NextTimeFrame():
    if ChartPeriod(0) < PERIOD_M1:
        ChartSetSymbolPeriod(0, None, PERIOD_M1)
    elif ChartPeriod(0) < PERIOD_M5:
        ChartSetSymbolPeriod(0, None, PERIOD_M5)
    elif ChartPeriod(0) < PERIOD_M15:
        ChartSetSymbolPeriod(0, None, PERIOD_M15)
    elif ChartPeriod(0) < PERIOD_M30:
        ChartSetSymbolPeriod(0, None, PERIOD_M30)
    elif ChartPeriod(0) < PERIOD_H1:
        ChartSetSymbolPeriod(0, None, PERIOD_H1)
    elif ChartPeriod(0) < PERIOD_H4:
        ChartSetSymbolPeriod(0, None, PERIOD_H4)
    elif ChartPeriod(0) < PERIOD_D1:
        ChartSetSymbolPeriod(0, None, PERIOD_D1)
    elif ChartPeriod(0) < PERIOD_W1:
        ChartSetSymbolPeriod(0, None, PERIOD_W1)
    elif ChartPeriod(0) < PERIOD_MN1:
        ChartSetSymbolPeriod(0, None, PERIOD_MN1)
    else:
        ChartSetSymbolPeriod(0, None, PERIOD_M1)

def PrevTimeFrame():
    if ChartPeriod(0) > PERIOD_MN1:
        ChartSetSymbolPeriod(0, None, PERIOD_MN1)
    elif ChartPeriod(0) > PERIOD_W1:
        ChartSetSymbolPeriod(0, None, PERIOD_W1)
    elif ChartPeriod(0) > PERIOD_D1:
        ChartSetSymbolPeriod(0, None, PERIOD_D1)
    elif ChartPeriod(0) > PERIOD_H4:
        ChartSetSymbolPeriod(0, None, PERIOD_H4)
    elif ChartPeriod(0) > PERIOD_H1:
        ChartSetSymbolPeriod(0, None, PERIOD_H1)
    elif ChartPeriod(0) > PERIOD_M30:
        ChartSetSymbolPeriod(0, None, PERIOD_M30)
    elif ChartPeriod(0) > PERIOD_M15:
        ChartSetSymbolPeriod(0, None, PERIOD_M15)
    elif ChartPeriod(0) > PERIOD_M5:
        ChartSetSymbolPeriod(0, None, PERIOD_M5)
    elif ChartPeriod(0) > PERIOD_M1:
        ChartSetSymbolPeriod(0, None, PERIOD_M1)
    else:
        ChartSetSymbolPeriod(0, None, PERIOD_MN1)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HotkeysCycleTimeFramesV10(_MQL5Indicator):
    name = 'Hotkeys_CycleTimeFrames_v1.0'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

