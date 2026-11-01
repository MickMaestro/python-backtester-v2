"""Hotkeys_CycleMarketWatchSymbols_v1.0 — converted from MQL5: MQL5 Indicators/Hotkeys_CycleMarketWatchSymbols_v1.0/Hotkeys_CycleMarketWatchSymbols_v1.0.mq5

Hotkeys Comma, Period To Cycle Through Market Watch Symbols.
Copyright: Copyright 2021, NickBixy; Link: https://www.forexfactory.com/showthread.php?t=904734; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2021, NickBixy', 'link': 'https://www.forexfactory.com/showthread.php?t=904734', 'version': '1.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Hotkeys Comma, Period To Cycle Through Market Watch Symbols.'], 'name': 'Hotkeys_CycleMarketWatchSymbols_v1.0', 'source': 'MQL5 Indicators/Hotkeys_CycleMarketWatchSymbols_v1.0/Hotkeys_CycleMarketWatchSymbols_v1.0.mq5', 'folder': 'Hotkeys_CycleMarketWatchSymbols_v1.0', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
NumSymbols = 0
StringSymbolList = Arr(0, "")

def OnInit():
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ == CHARTEVENT_KEYDOWN:
        _sw1 = _int(lparam)
        if _sw1 == 188:
            PrevSymbol()
        elif _sw1 == 190:
            NextSymbol()
        ChartRedraw()

def NextSymbol():
    currentIndex = 0
    GetSymbols()
    currentIndex = GetIndex()
    currentIndex += 1
    if currentIndex >= NumSymbols:
        ChartSetSymbolPeriod(0, StringSymbolList[0], 0)
    else:
        ChartSetSymbolPeriod(0, StringSymbolList[currentIndex], 0)

def PrevSymbol():
    currentIndex = 0
    GetSymbols()
    currentIndex = GetIndex()
    currentIndex -= 1
    if currentIndex < 0:
        currentIndex = NumSymbols - 1
        ChartSetSymbolPeriod(0, StringSymbolList[currentIndex], 0)
    else:
        ChartSetSymbolPeriod(0, StringSymbolList[currentIndex], 0)

def GetSymbols():
    global NumSymbols
    numSymbolsMarketWatch = SymbolsTotal(True)
    NumSymbols = numSymbolsMarketWatch
    ArrayResize(StringSymbolList, numSymbolsMarketWatch)
    for i in range(0, numSymbolsMarketWatch):
        StringSymbolList[i] = SymbolName(i, True)

def GetIndex():
    index = 0
    for i in range(0, NumSymbols):
        if Symbol() == StringSymbolList[i]:
            index = i
            break
    return index


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HotkeysCycleMarketWatchSymbolsV10(_MQL5Indicator):
    name = 'Hotkeys_CycleMarketWatchSymbols_v1.0'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

