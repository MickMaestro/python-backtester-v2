"""DayImpuls — converted from MQL5: MQL5 Indicators/DayImpuls/DayImpuls.mq5

Copyright: Copyright © 2018, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.001

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.001', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [64636]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Impuls'}, 'levels': [], 'description': [], 'name': 'DayImpuls', 'source': 'MQL5 Indicators/DayImpuls/DayImpuls.mq5', 'folder': 'DayImpuls', 'inputs': [{'mql': 'Inp_ma_period', 'py': 'Inp_ma_period', 'param': 'Inp_ma_period', 'type': 'int', 'default': 14, 'label': 'averaging period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
Inp_ma_period = _input('Inp_ma_period', 14)  # averaging period
ImpulsBuffer = Arr(0, 0.0)
ImpulsBufferTemp = Arr(0, 0.0)
ImpulsBufferTempDbl = Arr(0, 0.0)
m_point = 0.0

def OnInit():
    global m_point
    SetIndexBuffer(0, ImpulsBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ImpulsBufferTemp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, ImpulsBufferTempDbl, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Impuls(' + _str(Inp_ma_period) + ')')
    m_point = Point()
    if m_point == 0.0:
        Print('ERROR: Point = 0')
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 0
    for i in range(limit, rates_total):
        ImpulsBufferTemp[i] = _fdiv(close[i] - open[i], m_point)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, Inp_ma_period, ImpulsBufferTemp, ImpulsBufferTempDbl)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, Inp_ma_period, ImpulsBufferTempDbl, ImpulsBuffer)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DayImpuls(_MQL5Indicator):
    name = 'DayImpuls'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_ma_period': 14,  # averaging period
    }

