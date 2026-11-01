"""balance_of_power — converted from MQL5: MQL5 Indicators/Balance of Power/balance_of_power.mq5

Copyright: Copyright 2012, RoboFx; Link: http://www.robofx.org; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2012, RoboFx', 'link': 'http://www.robofx.org', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [11829830, 0]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'BOP'}, 'levels': [], 'description': [], 'name': 'balance_of_power', 'source': 'MQL5 Indicators/Balance of Power/balance_of_power.mq5', 'folder': 'Balance of Power', 'inputs': [{'mql': 'BOP_Period', 'py': 'BOP_Period', 'param': 'BOP_Period', 'type': 'int', 'default': 14, 'label': '--- smoothing period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
BOP_Period = _input('BOP_Period', 14)  # --- smoothing period
Buffer1 = Arr(0, 0.0)  # --- raw data buffer
BOP = Arr(0, 0.0)  # --- main indicator buffer

def OnInit():
    SetIndexBuffer(0, BOP, INDICATOR_DATA)
    SetIndexBuffer(1, Buffer1, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Balance of Power (' + _str(BOP_Period) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    start = 0
    if rates_total < BOP_Period:
        return 0
    if prev_calculated > 1:
        start = prev_calculated - 1
    else:
        start = 1
    for i in range(start, rates_total):
        if (high[i] - low[i]) > 0.0:
            Buffer1[i] = _fdiv(close[i] - open[i], high[i] - low[i])
        else:
            Buffer1[i] = 0.0
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, BOP_Period, Buffer1, BOP)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BalanceOfPower(_MQL5Indicator):
    name = 'balance_of_power'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BOP_Period': 14,  # --- smoothing period
    }

