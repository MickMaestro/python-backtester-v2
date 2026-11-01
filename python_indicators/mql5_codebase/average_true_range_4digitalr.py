"""Average_True_Range_4digitalr — converted from MQL5: MQL5 Indicators/Average True Range (digital)/Average_True_Range_4digitalr.mq5

The value of the indicator Average True Range (ATR) from several timeframes
Copyright: Copyright © 2017, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['The value of the indicator Average True Range (ATR) from several timeframes'], 'name': 'Average_True_Range_4digitalr', 'source': 'MQL5 Indicators/Average True Range (digital)/Average_True_Range_4digitalr.mq5', 'folder': 'Average True Range (digital)', 'inputs': [{'mql': 'period_first', 'py': 'period_first', 'param': 'period_first', 'type': 'int', 'default': 15, 'label': 'period first ATR', 'sinput': False}, {'mql': 'ma_period_first', 'py': 'ma_period_first', 'param': 'ma_period_first', 'type': 'int', 'default': 14, 'label': 'averaging period first ATR', 'sinput': False}, {'mql': 'period_second', 'py': 'period_second', 'param': 'period_second', 'type': 'int', 'default': 16385, 'label': 'period second ATR', 'sinput': False}, {'mql': 'ma_period_second', 'py': 'ma_period_second', 'param': 'ma_period_second', 'type': 'int', 'default': 14, 'label': 'averaging period second ATR', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period_first = _input('period_first', PERIOD_M15)  # period first ATR
ma_period_first = _input('ma_period_first', 14)  # averaging period first ATR
period_second = _input('period_second', PERIOD_H1)  # period second ATR
ma_period_second = _input('ma_period_second', 14)  # averaging period second ATR
handle_iATR_first = 0  # variable for storing the handle of the iATR indicator
handle_iATR_second = 0  # variable for storing the handle of the iATR indicator

def OnInit():
    global handle_iATR_first, handle_iATR_second
    handle_iATR_first = iATR(Symbol(), period_first, ma_period_first)
    if handle_iATR_first == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iATR indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(period_first, 'ENUM_TIMEFRAMES'), GetLastError())
        return INIT_FAILED
    handle_iATR_second = iATR(Symbol(), period_second, ma_period_second)
    if handle_iATR_second == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iATR indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(period_second, 'ENUM_TIMEFRAMES'), GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if prev_calculated == 0:
        return rates_total
    text = 'ATR(' + IntegerToString(ma_period_first) + '),' + EnumToString(period_first, 'ENUM_TIMEFRAMES') + ': ' + DoubleToString(iATRGet(handle_iATR_first, 0), Digits()) + '\n' + 'ATR(' + IntegerToString(ma_period_second) + '),' + EnumToString(period_second, 'ENUM_TIMEFRAMES') + ': ' + DoubleToString(iATRGet(handle_iATR_second, 0), Digits())
    Comment(text)
    return rates_total

def iATRGet(handle_iATR, index):
    ATR = Arr(1, 0.0, dyn=False)
    ResetLastError()
    if CopyBuffer(handle_iATR, 0, index, 1, ATR) < 0:
        PrintFormat('Failed to copy data from the iATR indicator, error code %d', GetLastError())
        return 0.0
    return ATR[0]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AverageTrueRange4digitalr(_MQL5Indicator):
    name = 'Average_True_Range_4digitalr'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period_first': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=15),  # period first ATR
        'ma_period_first': 14,  # averaging period first ATR
        'period_second': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # period second ATR
        'ma_period_second': 14,  # averaging period second ATR
    }

