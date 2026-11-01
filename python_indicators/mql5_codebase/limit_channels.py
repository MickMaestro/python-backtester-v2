"""Limit channels — converted from MQL5: MQL5 Indicators/Limit channels/Limit channels.mq5

Copyright: © mladen, 2021; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2021', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [3329330], 2: [3329330], 3: [3329330], 4: [5275647], 5: [5275647], 6: [5275647]}, 'widths': {1: 2, 2: 1, 5: 1, 6: 2}, 'styles': {1: 0, 2: 0, 3: 2, 4: 2, 5: 0, 6: 0}, 'labels': {1: 'Level up 3', 2: 'Level up 2', 3: 'Level up 1', 4: 'Level down 1', 5: 'Level down 2', 6: 'Level down 3'}, 'levels': [], 'description': [], 'name': 'Limit channels', 'source': 'MQL5 Indicators/Limit channels/Limit channels.mq5', 'folder': 'Limit channels', 'inputs': [{'mql': 'inpAtrPeriod', 'py': 'inpAtrPeriod', 'param': 'inpAtrPeriod', 'type': 'int', 'default': 50, 'label': 'ATR period', 'sinput': False}, {'mql': 'inpAtrMultiplier', 'py': 'inpAtrMultiplier', 'param': 'inpAtrMultiplier', 'type': 'double', 'default': 5.0, 'label': 'ATR multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpAtrPeriod = _input('inpAtrPeriod', 50)  # ATR period
inpAtrMultiplier = _input('inpAtrMultiplier', 5.0)  # ATR multiplier
up1 = Arr(0, 0.0)
up2 = Arr(0, 0.0)
up3 = Arr(0, 0.0)
down1 = Arr(0, 0.0)
down2 = Arr(0, 0.0)
down3 = Arr(0, 0.0)

class sWorkStruct(MqlObject):
    _q_fields = ('tr', 'trSum')
    def __init__(self, *args):
        self.tr = 0.0
        self.trSum = 0.0

def OnInit():
    SetIndexBuffer(0, up3, INDICATOR_DATA)
    SetIndexBuffer(1, up2, INDICATOR_DATA)
    SetIndexBuffer(2, up1, INDICATOR_DATA)
    SetIndexBuffer(3, down1, INDICATOR_DATA)
    SetIndexBuffer(4, down2, INDICATOR_DATA)
    SetIndexBuffer(5, down3, INDICATOR_DATA)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_workSize
    limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    if _s_OnCalculate_m_workSize < rates_total:
        _s_OnCalculate_m_workSize = ArrayResize(_s_OnCalculate_m_work, rates_total + 500, 2000)
    for i in range(limit, rates_total):
        _s_OnCalculate_m_work[i].tr = (((high[i] if (high[i] > close[i - 1]) else close[i - 1]) - (low[i] if (low[i] < close[i - 1]) else close[i - 1])) if (i > 0) else (high[i] - low[i]))
        if i > inpAtrPeriod:
            _s_OnCalculate_m_work[i].trSum = _s_OnCalculate_m_work[i - 1].trSum + _s_OnCalculate_m_work[i].tr - _s_OnCalculate_m_work[i - inpAtrPeriod].tr
        else:
            _s_OnCalculate_m_work[i].trSum = _s_OnCalculate_m_work[i].tr
            k = 1
            while k < inpAtrPeriod and i >= k:
                _s_OnCalculate_m_work[i].trSum += _s_OnCalculate_m_work[i - k].tr
                k += 1
        if i == 0:
            up3[i] = high[i]
            up2[i] = up3[i]
            up1[i] = up2[i]
            down3[i] = low[i]
            down2[i] = down3[i]
            down1[i] = down2[i]
        else:
            _atr = (inpAtrMultiplier * _s_OnCalculate_m_work[i - 1].trSum) / float(inpAtrPeriod)
            if high[i] > up3[i - 1]:
                up3[i] = high[i]
            elif high[i] < up3[i - 1]:
                up3[i] = MathMin(high[i] + (_atr * 1.0), up3[i - 1])
            else:
                up3[i] = up3[i - 1]
            if high[i] > up2[i - 1]:
                up2[i] = high[i]
            elif high[i] < up2[i - 1]:
                up2[i] = MathMin(high[i] + (_atr * 0.5), up2[i - 1])
            else:
                up2[i] = up2[i - 1]
            if high[i] > up1[i - 1]:
                up1[i] = high[i]
            elif high[i] < up1[i - 1]:
                up1[i] = MathMin(high[i] + (_atr * 0.1), up1[i - 1])
            else:
                up1[i] = up1[i - 1]
            if low[i] < down1[i - 1]:
                down1[i] = low[i]
            elif low[i] > down1[i - 1]:
                down1[i] = MathMax(low[i] - (_atr * 0.1), down1[i - 1])
            else:
                down1[i] = down1[i - 1]
            if low[i] < down2[i - 1]:
                down2[i] = low[i]
            elif low[i] > down2[i - 1]:
                down2[i] = MathMax(low[i] - (_atr * 0.5), down2[i - 1])
            else:
                down2[i] = down2[i - 1]
            if low[i] < down3[i - 1]:
                down3[i] = low[i]
            elif low[i] > down3[i - 1]:
                down3[i] = MathMax(low[i] - (_atr * 1.0), down3[i - 1])
            else:
                down3[i] = down3[i - 1]
    return rates_total

# ---- static local variables
_s_OnCalculate_m_work = Arr(0, 0, factory=sWorkStruct)
_s_OnCalculate_m_workSize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LimitChannels(_MQL5Indicator):
    name = 'Limit channels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpAtrPeriod': 50,  # ATR period
        'inpAtrMultiplier': 5.0,  # ATR multiplier
    }

