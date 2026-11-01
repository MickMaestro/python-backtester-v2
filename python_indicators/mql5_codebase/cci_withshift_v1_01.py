"""CCI_withShift_v1.01 — converted from MQL5: MQL5 Indicators/MT5 CCI with shift parameter/CCI_withShift_v1.01.mq5

CCI with shift
Copyright: Phade & MetaQuotes Ltd.; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Phade & MetaQuotes Ltd.', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'CCI'}, 'levels': [-100.0, 100.0], 'description': ['CCI with shift'], 'name': 'CCI_withShift_v1.01', 'source': 'MQL5 Indicators/MT5 CCI with shift parameter/CCI_withShift_v1.01.mq5', 'folder': 'MT5 CCI with shift parameter', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'shift', 'py': 'shift', 'param': 'shift', 'type': 'int', 'default': 1, 'label': 'Shift', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period = _input('period', 14)  # Period
applied_price = _input('applied_price', PRICE_CLOSE)  # Applied price
shift = _input('shift', 1)  # Shift
cci_handle = 0
plotting_buffer = Arr(0, 0.0)
data = Arr(0, 0.0)

def OnInit():
    global cci_handle
    cci_handle = iCCI(Symbol(), Period(), period, applied_price)
    if cci_handle == INVALID_HANDLE:
        Print('Failed to create CCI indicator!')
        return INIT_FAILED
    indicator_name = 'CCI(' + IntegerToString(period) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, indicator_name)
    SetIndexBuffer(0, plotting_buffer, INDICATOR_DATA)
    SetIndexBuffer(1, data, INDICATOR_CALCULATIONS)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    IndicatorRelease(cci_handle)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total <= (period + shift):
        return 0
    calculated = BarsCalculated(cci_handle)
    if calculated < rates_total:
        Print('Not all data of handle is calculated (', calculated, ' bars). Error ', GetLastError())
        return 0
    to_copy = (rates_total if (prev_calculated > rates_total or prev_calculated < 0) else (rates_total - prev_calculated))
    if prev_calculated > 0:
        to_copy += 1
    copied = CopyBuffer(cci_handle, 0, 0, to_copy, data)
    if copied <= 0:
        Print('Failed to copy CCI values!')
        return 0
    limit = (0 if (prev_calculated == 0) else (prev_calculated - 1))
    for i in range(rates_total - 1, MathMax(limit, shift), -1):
        plotting_buffer[i - shift] = data[i]
    for i in range(rates_total - shift, rates_total):
        plotting_buffer[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CCIWithShiftV101(_MQL5Indicator):
    name = 'CCI_withShift_v1.01'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'period': 14,  # Period
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'shift': 1,  # Shift
    }

