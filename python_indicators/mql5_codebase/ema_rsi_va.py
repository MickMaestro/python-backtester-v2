"""ema_rsi_va — converted from MQL5: MQL5 Indicators/EMA_RSI_VA/ema_rsi_va.mq5

Copyright: Integer; Link: https://login.mql5.com/en/users/Integer; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Integer', 'link': 'https://login.mql5.com/en/users/Integer', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Label1'}, 'levels': [], 'description': [], 'name': 'ema_rsi_va', 'source': 'MQL5 Indicators/EMA_RSI_VA/ema_rsi_va.mq5', 'folder': 'EMA_RSI_VA', 'inputs': [{'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'int', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'EMAPeriods', 'py': 'EMAPeriods', 'param': 'EMAPeriods', 'type': 'double', 'default': 14.0, 'label': 'EMA period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_NAME = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
RSIPeriod = _input('RSIPeriod', 14)  # RSI period
EMAPeriods = _input('EMAPeriods', 14.0)  # EMA period
Price = _input('Price', PRICE_CLOSE)  # Applied price
RSIHand = 0
MAHand = 0
Label1Buffer = Arr(0, 0.0)
RSIBuf = Arr(0, 0.0)
MABuf = Arr(0, 0.0)

def OnInit():
    global MAHand, RSIHand
    SetIndexBuffer(0, Label1Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, RSIBuf, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, MABuf, INDICATOR_CALCULATIONS)
    RSIHand = iRSI(None, PERIOD_CURRENT, RSIPeriod, Price)
    MAHand = iMA(None, PERIOD_CURRENT, 1, 0, 0, Price)
    if RSIHand == INVALID_HANDLE or MAHand == INVALID_HANDLE:
        Alert('Error in creation of indicator, please try again')
        return -1
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, RSIPeriod * 2)
    PlotIndexSetString(0, PLOT_LABEL, MQL5InfoString(MQL5_PROGRAM_NAME))
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_error
    start = 0
    if prev_calculated == 0:
        _s_OnCalculate_error = True
    if _s_OnCalculate_error:
        start = RSIPeriod * 2
        Label1Buffer[start - 1] = close[start - 1]
        _s_OnCalculate_error = False
    else:
        start = prev_calculated - 1
    if CopyBuffer(RSIHand, 0, 0, rates_total - start, RSIBuf) == -1 or CopyBuffer(MAHand, 0, 0, rates_total - start, MABuf) == -1:
        _s_OnCalculate_error = True
        return 0
    for i in range(start, rates_total):
        RSvoltl = MathAbs(RSIBuf[i] - 50) + 1.0
        multi = _fdiv(5.0 + (100.0 / RSIPeriod), 0.06 + (0.92 * RSvoltl) + (0.02 * MathPow(RSvoltl, 2)))
        pdsx = multi * EMAPeriods
        if pdsx < 1.0:
            pdsx = 1.0
        Label1Buffer[i] = _fdiv(MABuf[i] * 2.0, pdsx + 1.0) + (Label1Buffer[i - 1] * (1.0 - _fdiv(2.0, pdsx + 1.0)))
    return rates_total

# ---- static local variables
_s_OnCalculate_error = True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EmaRsiVa(_MQL5Indicator):
    name = 'ema_rsi_va'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSIPeriod': 14,  # RSI period
        'EMAPeriods': 14.0,  # EMA period
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

