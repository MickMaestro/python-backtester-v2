"""Test_CustomCCI — converted from MQL5: MQL5 Indicators/MT5 CCI with shift parameter/Test_CustomCCI.mq5

Copyright: Copyright 2023, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'CCI'}, 'levels': [-100.0, 100.0], 'description': [], 'name': 'Test_CustomCCI', 'source': 'MQL5 Indicators/MT5 CCI with shift parameter/Test_CustomCCI.mq5', 'folder': 'MT5 CCI with shift parameter', 'inputs': [{'mql': 'ma_period', 'py': 'ma_period', 'param': 'ma_period', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'shift', 'py': 'shift', 'param': 'shift', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ma_period = _input('ma_period', 14)
applied_price = _input('applied_price', PRICE_CLOSE)
shift = _input('shift', 0)
custom_cci_handle = INVALID_HANDLE
test_buf = Arr(0, 0.0)

def OnInit():
    global custom_cci_handle
    SetIndexBuffer(0, test_buf, INDICATOR_DATA)
    custom_cci_handle = iCustom(Symbol(), Period(), 'Examples\\CCI_withShift.ex5', ma_period, applied_price, shift)
    if custom_cci_handle == INVALID_HANDLE:
        Print('Still shows as invalid handle. Failed to initialize custom CCI indicator!')
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    copied = CopyBuffer(custom_cci_handle, 0, 0, rates_total, test_buf)
    if copied <= 0:
        Print('Failed to copy CCI values!')
        return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TestCustomCCI(_MQL5Indicator):
    name = 'Test_CustomCCI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ma_period': 14,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'shift': 0,
    }

