"""NoRepaintHeikenAshi — converted from MQL5: MQL5 Indicators/No Repaint Heiken Ashi/NoRepaintHeikenAshi.mq5

Copyright: Copyright © 2023, Nomocp.; Link: https://t.me/nomocp; Version: 1.1

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2023, Nomocp.', 'link': 'https://t.me/nomocp', 'version': '1.1', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [15136253, 6908265]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Heiken Ashi Open;Heiken Ashi High;Heiken Ashi Low;Heiken Ashi Close'}, 'levels': [], 'description': [], 'name': 'NoRepaintHeikenAshi', 'source': 'MQL5 Indicators/No Repaint Heiken Ashi/NoRepaintHeikenAshi.mq5', 'folder': 'No Repaint Heiken Ashi', 'inputs': [{'mql': 'inpRepaintMode', 'py': 'inpRepaintMode', 'param': 'inpRepaintMode', 'type': 'bool', 'default': False, 'label': 'Enable Repaint Mode', 'sinput': True}, {'mql': 'inpFasterMode', 'py': 'inpFasterMode', 'param': 'inpFasterMode', 'type': 'bool', 'default': True, 'label': 'Enable Faster Mode', 'sinput': True}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRepaintMode = _input('inpRepaintMode', False)  # Enable Repaint Mode
inpFasterMode = _input('inpFasterMode', True)  # Enable Faster Mode
bufferOpen = Arr(0, 0.0)
bufferHigh = Arr(0, 0.0)
bufferLow = Arr(0, 0.0)
bufferClose = Arr(0, 0.0)
bufferColor = Arr(0, 0.0)
count = (0 if inpRepaintMode else 1)
start = 0
countCandle = 1

def OnInit():
    SetIndexBuffer(0, bufferOpen, INDICATOR_DATA)
    SetIndexBuffer(1, bufferHigh, INDICATOR_DATA)
    SetIndexBuffer(2, bufferLow, INDICATOR_DATA)
    SetIndexBuffer(3, bufferClose, INDICATOR_DATA)
    SetIndexBuffer(4, bufferColor, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Heiken Ashi')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global countCandle, start
    if prev_calculated == 0:
        bufferLow[0] = low[0]
        bufferHigh[0] = high[0]
        bufferOpen[0] = open[0]
        bufferClose[0] = close[0]
        countCandle = (-1 if (open[0] < close[0]) else 1)
        bufferColor[0] = (0 if (open[0] < close[0]) else 1)
        start = 1
    else:
        start = prev_calculated - 1
    if inpFasterMode:
        HeikenAshiFasterCalculate(open, high, low, close, rates_total)
    else:
        HeikenAshiNormalCalculate(open, high, low, close, rates_total)
    return rates_total

def HeikenAshiNormalCalculate(open, high, low, close, rates):
    for i in range(start, rates):
        pos = i - count
        ha_open = (bufferOpen[i - 1] + bufferClose[i - 1]) / 2
        ha_close = (open[pos] + high[pos] + low[pos] + close[pos]) / 4
        ha_high = MathMax(high[pos], MathMax(ha_open, ha_close))
        ha_low = MathMin(low[pos], MathMin(ha_open, ha_close))
        bufferLow[i] = ha_low
        bufferHigh[i] = ha_high
        bufferOpen[i] = ha_open
        bufferClose[i] = ha_close
        bufferColor[i] = (0 if (ha_open < ha_close) else 1)

def HeikenAshiFasterCalculate(open, high, low, close, rates):
    global countCandle
    for i in range(start, rates):
        pos = i - count
        ha_open = (bufferOpen[i - 1] + bufferClose[i - 1]) / 2
        ha_close = ((2 * open[i]) + high[pos] + low[pos]) / 4
        ha_close = AddWeight(ha_close, countCandle, (high[pos] if (countCandle > 0) else low[pos]))
        ha_high = MathMax(high[pos], MathMax(ha_open, ha_close))
        ha_low = MathMin(low[pos], MathMin(ha_open, ha_close))
        bufferLow[i] = ha_low
        bufferHigh[i] = ha_high
        bufferOpen[i] = ha_open
        bufferClose[i] = ha_close
        bufferColor[i] = (0 if (ha_open < ha_close) else 1)
        if (not HasNewCandle()) and start != 1:
            continue
        if ha_open < ha_close:
            if bufferColor[i - 1] == 1:
                countCandle = -1
            else:
                countCandle -= 1
        else:
            if bufferColor[i - 1] == 0:
                countCandle = 1
            else:
                countCandle += 1

def AddWeight(closePrice, weight, extremePrice):
    return _fdiv(closePrice + (extremePrice * MathAbs(weight)), MathAbs(weight) + 1)

def HasNewCandle():
    global _s_HasNewCandle_lastTime
    lastBarTime = SeriesInfoInteger(Symbol(), Period(), SERIES_LASTBAR_DATE)
    if _s_HasNewCandle_lastTime is _UNSET:
        _s_HasNewCandle_lastTime = lastBarTime
    if _s_HasNewCandle_lastTime == lastBarTime:
        return False
    _s_HasNewCandle_lastTime = lastBarTime
    return True

# ---- static local variables
_s_HasNewCandle_lastTime = _UNSET


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NoRepaintHeikenAshi(_MQL5Indicator):
    name = 'NoRepaintHeikenAshi'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRepaintMode': False,  # Enable Repaint Mode
        'inpFasterMode': True,  # Enable Faster Mode
    }

