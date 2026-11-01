"""choppy_market_index — converted from MQL5: MQL5 Indicators/Choppy market index/choppy_market_index.mq5

Copyright: Choppy Market Index; Link: https://login.mql5.com/ru/users/Alextp; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Choppy Market Index', 'link': 'https://login.mql5.com/ru/users/Alextp', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2, 'indicator_minimum': 0.0, 'indicator_maximum': 100.0}, 'types': {1: 1, 2: 10}, 'colors': {1: [16711680], 2: [255, 65535, 32768]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Signal', 2: 'Hist'}, 'levels': [60.0, 50.0, 40.0], 'description': [], 'name': 'choppy_market_index', 'source': 'MQL5 Indicators/Choppy market index/choppy_market_index.mq5', 'folder': 'Choppy market index', 'inputs': [{'mql': 'N_Period', 'py': 'N_Period', 'param': 'N_Period', 'type': 'int', 'default': 60, 'label': 'CMI Period', 'sinput': False}, {'mql': 'MA_Period', 'py': 'MA_Period', 'param': 'MA_Period', 'type': 'int', 'default': 10, 'label': 'MA Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
N_Period = _input('N_Period', 60)  # CMI Period
MA_Period = _input('MA_Period', 10)  # MA Period
HistBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
MABuffer = Arr(0, 0.0)
ColorInd = 0
Delta_hl = 0.0
Delta_Close = 0.0

def OnInit():
    SetIndexBuffer(0, MABuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HistBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(HistBuffer, True)
    ArraySetAsSeries(ColorBuffer, True)
    ArraySetAsSeries(MABuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, '(CMI' + ', Period = ' + _str(N_Period) + ', MA = ' + _str(MA_Period) + ' )')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global ColorInd, Delta_Close, Delta_hl
    offset = N_Period + 1
    if rates_total < offset:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    start = 0
    if prev_calculated < rates_total or prev_calculated <= 0:
        for i in range(rates_total - 1, 0 - 1, -1):
            HistBuffer[i] = 0.0
        start = rates_total - offset
    else:
        start = rates_total - prev_calculated
    for i in range(start, 0 - 1, -1):
        Delta_hl = high[ArrayMaximum(high, i, N_Period)] - low[ArrayMinimum(low, i, N_Period)]
        Delta_Close = close[i] - close[i + N_Period]
        if Delta_hl == 0:
            HistBuffer[i] = 0.0
        else:
            HistBuffer[i] = _fdiv(MathAbs(Delta_Close), Delta_hl) * 100
        if Delta_Close > 0:
            if ColorInd < 2:
                ColorInd += 1
            ColorBuffer[i] = ColorInd
        elif Delta_Close < 0:
            if ColorInd > 0:
                ColorInd -= 1
            ColorBuffer[i] = ColorInd
        else:
            ColorBuffer[i] = 1.0
    SimpleMAOnBuffer(rates_total, prev_calculated, N_Period, MA_Period, HistBuffer, MABuffer)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ChoppyMarketIndex(_MQL5Indicator):
    name = 'choppy_market_index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'N_Period': 60,  # CMI Period
        'MA_Period': 10,  # MA Period
    }
    y_range = (0.0, 100.0)

