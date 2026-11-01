"""ichartsswitchsymbol — converted from MQL5: MQL5 Indicators/iChartsSwitchSymbol/ichartsswitchsymbol.mq5

 
      http://dmffx.com
 
      mailto:for-good-letters@yandex.ru
 
Copyright: Integer; Link: https://login.mql5.com/ru/users/Integer

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- OnChartEvent is not called (no chart events).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Integer', 'link': 'https://login.mql5.com/ru/users/Integer', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Label1'}, 'levels': [], 'description': [' ', '      http://dmffx.com', ' ', '      mailto:for-good-letters@yandex.ru', ' '], 'name': 'ichartsswitchsymbol', 'source': 'MQL5 Indicators/iChartsSwitchSymbol/ichartsswitchsymbol.mq5', 'folder': 'iChartsSwitchSymbol', 'inputs': [{'mql': 'Input1', 'py': 'Input1', 'param': 'Input1', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Input1 = _input('Input1', 0)
Label1Buffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, Label1Buffer, INDICATOR_DATA)
    EventSetTimer(1)
    Comment('Drag symbol here')
    return 0

def OnDeinit(r):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def OnTimer():
    Func()

def OnChartEvent(id_, lparam, dparam, sparam):
    Func()

def Func():
    List = Arr(0, 0)
    ChartsList(List)
    for i in range(0, ArraySize(List)):
        if ChartSymbol(List[i]) != Symbol():
            ChartSetSymbolPeriod(List[i], Symbol(), ChartPeriod(List[i]))

def ChartsList(aList):
    ArrayResize(aList, 0)
    tmp = ChartFirst()
    while tmp != -1:
        ArrayResize(aList, ArraySize(aList) + 1)
        aList[ArraySize(aList) - 1] = tmp
        tmp = ChartNext(tmp)
    return ArraySize(aList)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ichartsswitchsymbol(_MQL5Indicator):
    name = 'ichartsswitchsymbol'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Input1': 0,
    }

