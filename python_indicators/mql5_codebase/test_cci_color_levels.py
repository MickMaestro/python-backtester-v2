"""Test CCI Color Levels — converted from MQL5: MQL5 Indicators/CCI Color Levels/Test CCI Color Levels.mq5

The adviser shows an example of obtaining values of the CCI Color Levels indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: http://wmua.ru/slesar/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- The program has no OnCalculate: it draws only chart objects or reacts to events.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'http://wmua.ru/slesar/', 'version': '1.000'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['The adviser shows an example of obtaining values of the CCI Color Levels indicator'], 'name': 'Test CCI Color Levels', 'source': 'MQL5 Indicators/CCI Color Levels/Test CCI Color Levels.mq5', 'folder': 'CCI Color Levels', 'inputs': [{'mql': 'Inp_CCI_ma_period', 'py': 'Inp_CCI_ma_period', 'param': 'Inp_CCI_ma_period', 'type': 'int', 'default': 14, 'label': 'Averaging period', 'sinput': False}, {'mql': 'Inp_CCI_LevelUP', 'py': 'Inp_CCI_LevelUP', 'param': 'Inp_CCI_LevelUP', 'type': 'double', 'default': 90.0, 'label': 'Level UP', 'sinput': False}, {'mql': 'Inp_CCI_LevelDOWN', 'py': 'Inp_CCI_LevelDOWN', 'param': 'Inp_CCI_LevelDOWN', 'type': 'double', 'default': -90.0, 'label': 'Level DOWN', 'sinput': False}], 'short_form': False, 'has_oncalculate': False, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_CCI_ma_period = _input('Inp_CCI_ma_period', 14)  # Averaging period
Inp_CCI_LevelUP = _input('Inp_CCI_LevelUP', 90.0)  # Level UP
Inp_CCI_LevelDOWN = _input('Inp_CCI_LevelDOWN', -90.0)  # Level DOWN
handle_iCustom = 0  # variable for storing the handle of the iCustom indicator

def OnInit():
    global handle_iCustom
    handle_iCustom = iCustom(Symbol(), Period(), 'CCI Color Levels', Inp_CCI_ma_period, Inp_CCI_LevelUP, Inp_CCI_LevelDOWN)
    if handle_iCustom == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iCCI indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnTick():
    level_up = iCustomGet(handle_iCustom, 0, 0)
    cci = iCustomGet(handle_iCustom, 2, 0)
    level_down = iCustomGet(handle_iCustom, 4, 0)
    text = 'Lelev UP #0: ' + DoubleToString(level_up, 2) + '\n' + 'CCI #0: ' + DoubleToString(cci, 2) + '\n' + 'Lelev DOWN #0: ' + DoubleToString(level_down, 2)
    Comment(text)

def iCustomGet(handle, buffer, index):
    Custom = Arr(1, 0.0, dyn=False)
    ResetLastError()
    if CopyBuffer(handle, buffer, index, 1, Custom) < 0:
        PrintFormat('Failed to copy data from the iCustom indicator, error code %d', GetLastError())
        return 0.0
    return Custom[0]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TestCCIColorLevels(_MQL5Indicator):
    name = 'Test CCI Color Levels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_CCI_ma_period': 14,  # Averaging period
        'Inp_CCI_LevelUP': 90.0,  # Level UP
        'Inp_CCI_LevelDOWN': -90.0,  # Level DOWN
    }

