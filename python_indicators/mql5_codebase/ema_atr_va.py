"""ema_atr_va — converted from MQL5: MQL5 Indicators/EMA_ATR_VA/ema_atr_va.mq5

Copyright: Integer; Link: https://login.mql5.com/en/users/Integer; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Integer', 'link': 'https://login.mql5.com/en/users/Integer', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Label1'}, 'levels': [], 'description': [], 'name': 'ema_atr_va', 'source': 'MQL5 Indicators/EMA_ATR_VA/ema_atr_va.mq5', 'folder': 'EMA_ATR_VA', 'inputs': [{'mql': 'ATRPeriod', 'py': 'ATRPeriod', 'param': 'ATRPeriod', 'type': 'int', 'default': 14, 'label': 'ATR Period', 'sinput': False}, {'mql': 'EMAPeriod', 'py': 'EMAPeriod', 'param': 'EMAPeriod', 'type': 'double', 'default': 14.0, 'label': 'EMA period', 'sinput': False}, {'mql': 'Sensitivity', 'py': 'Sensitivity', 'param': 'Sensitivity', 'type': 'double', 'default': 100.0, 'label': 'Sensitivity (-100 to 100)', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_NAME = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
ATRPeriod = _input('ATRPeriod', 14)  # ATR Period
EMAPeriod = _input('EMAPeriod', 14.0)  # EMA period
Sensitivity = _input('Sensitivity', 100.0)  # Sensitivity (-100 to 100)
Price = _input('Price', PRICE_CLOSE)  # Price
ATRHand = 0
MAHand = 0
sens = 0.0
Label1Buffer = Arr(0, 0.0)
ATRBuf = Arr(0, 0.0)
MABuf = Arr(0, 0.0)

def OnInit():
    global ATRHand, MAHand, sens
    sens = Sensitivity / 100.0
    SetIndexBuffer(0, Label1Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, ATRBuf, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, MABuf, INDICATOR_CALCULATIONS)
    ATRHand = iATR(None, PERIOD_CURRENT, ATRPeriod)
    MAHand = iMA(None, PERIOD_CURRENT, 1, 0, 0, Price)
    if ATRHand == INVALID_HANDLE or MAHand == INVALID_HANDLE:
        Alert('Error in creation of indicator, please try again')
        return -1
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ATRPeriod * 2)
    PlotIndexSetString(0, PLOT_LABEL, MQL5InfoString(MQL5_PROGRAM_NAME))
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_error
    start = 0
    if prev_calculated == 0:
        _s_OnCalculate_error = True
    if _s_OnCalculate_error:
        start = ATRPeriod * 2
        Label1Buffer[start - 1] = close[start - 1]
        _s_OnCalculate_error = False
    else:
        start = prev_calculated - 1
    if CopyBuffer(ATRHand, 0, 0, rates_total - start, ATRBuf) == -1 or CopyBuffer(MAHand, 0, 0, rates_total - start, MABuf) == -1:
        _s_OnCalculate_error = True
        return 0
    for i in range(start, rates_total):
        mxv = ATRBuf[ArrayMaximum(ATRBuf, i - ATRPeriod + 1, ATRPeriod)]
        mnv = ATRBuf[ArrayMinimum(ATRBuf, i - ATRPeriod + 1, ATRPeriod)]
        r = mxv - mnv
        if r == 0:
            Label1Buffer[i] = Label1Buffer[i - 1]
            continue
        ATRvlty = _fdiv(ATRBuf[i] - mnv, r)
        multi = 0.0
        if ATRvlty <= 0.5:
            multi = (10.0 * MathPow(ATRvlty, 3.4739)) + 0.1
        else:
            multi = (10 * MathPow(ATRvlty, 3.32)) + 1e-06
        if sens > 0:
            multi = _fdiv(1.0, multi)
        if multi < 1.0:
            multi = 1.0 - ((1.0 - multi) * MathAbs(sens))
        else:
            multi = ((multi - 1.0) * MathAbs(sens)) + 1.0
        pdsx = EMAPeriod * multi
        if pdsx < 1.0:
            pdsx = 1.0
        Label1Buffer[i] = _fdiv(MABuf[i] * 2.0, pdsx + 1.0) + (Label1Buffer[i - 1] * (1.0 - _fdiv(2.0, pdsx + 1.0)))
    return rates_total

# ---- static local variables
_s_OnCalculate_error = True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EmaAtrVa(_MQL5Indicator):
    name = 'ema_atr_va'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ATRPeriod': 14,  # ATR Period
        'EMAPeriod': 14.0,  # EMA period
        'Sensitivity': 100.0,  # Sensitivity (-100 to 100)
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

