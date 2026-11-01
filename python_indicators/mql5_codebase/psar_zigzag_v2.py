"""PSAR Zigzag v2 — converted from MQL5: MQL5 Indicators/PSAR Zigzag (Non lagging)/PSAR Zigzag v2.mq5

Version: 2.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 2, 'version': '2.0'}, 'types': {1: 12, 2: 6}, 'colors': {1: [32768, 255], 2: [12632256]}, 'widths': {2: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'PSAR Zigzag v2', 'source': 'MQL5 Indicators/PSAR Zigzag (Non lagging)/PSAR Zigzag v2.mq5', 'folder': 'PSAR Zigzag (Non lagging)', 'inputs': [{'mql': 'Backstep', 'py': 'Backstep', 'param': 'Backstep', 'type': 'int', 'default': 2, 'label': 'Backstep', 'sinput': False}, {'mql': 'SARStep', 'py': 'SARStep', 'param': 'SARStep', 'type': 'double', 'default': 0.01, 'label': 'SAR Step value', 'sinput': False}, {'mql': 'SARMaximum', 'py': 'SARMaximum', 'param': 'SARMaximum', 'type': 'double', 'default': 0.1, 'label': 'SAR Maximum value', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ZigZagState
NONE = 0
LL_FOUND = 1
HL_FOUND = 2
LH_FOUND = 3
HH_FOUND = 4
_enum('ZigZagState', {0: 'NONE', 1: 'LL_FOUND', 2: 'HL_FOUND', 3: 'LH_FOUND', 4: 'HH_FOUND'})

# ---- inputs and global variables
Backstep = _input('Backstep', 2)  # Backstep
SARStep = _input('SARStep', 0.01)  # SAR Step value
SARMaximum = _input('SARMaximum', 0.1)  # SAR Maximum value
ZigzagStart = Arr(0, 0.0)
ZigzagEnd = Arr(0, 0.0)
PrevLegEnd = Arr(0, 0.0)
PSAR = Arr(0, 0.0)
SarCol = Arr(0, 0.0)
lastHighSwing = Arr(0, 0.0)
lastLowSwing = Arr(0, 0.0)
sarHandle = INVALID_HANDLE
LL = 0.0
HL = 0.0
LH = 0.0
HH = 0.0
lastSwingPrice = 0.0
currentState = NONE

def OnInit():
    global sarHandle
    SetIndexBuffer(0, PSAR, INDICATOR_DATA)
    SetIndexBuffer(1, SarCol, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ZigzagStart, INDICATOR_DATA)
    SetIndexBuffer(3, ZigzagEnd, INDICATOR_DATA)
    SetIndexBuffer(4, lastHighSwing, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, lastLowSwing, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    sarHandle = iSAR(Symbol(), Period(), SARStep, SARMaximum)
    if sarHandle == INVALID_HANDLE:
        Print('Failed to create SAR handle')
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global HH, HL, LH, LL, _s_OnCalculate_swing_index, currentState, lastSwingPrice
    to_copy = ((rates_total - prev_calculated + 1) if (prev_calculated > 0) else rates_total)
    if CopyBuffer(sarHandle, 0, 0, to_copy, PSAR) <= 0:
        return rates_total
    start = (50 if (prev_calculated == 0) else (prev_calculated - 1))
    confirmCount = 0
    bs = Backstep
    for i in range(start, rates_total):
        SarCol[i] = (1 if (PSAR[i] > close[i]) else 0)
    for i in range(start + 1, rates_total):
        ZigzagStart[i] = EMPTY_VALUE
        ZigzagEnd[i] = EMPTY_VALUE
        Low = low[i]
        High = high[i]
        j = 1
        while j <= bs and i > 50:
            if high[i - j] > High:
                High = high[i - j]
            if low[i - j] < Low:
                Low = low[i - j]
            j += 1
        _sw1 = currentState
        if _sw1 == NONE:
            if PSAR[i] > high[i]:
                LL = High
                if high[i] == LL:
                    ZigzagStart[i] = LL
                else:
                    ZigzagStart[i - bs] = LL
                lastLowSwing[i] = LL
                lastHighSwing[i] = EMPTY_VALUE
                currentState = LL_FOUND
                lastSwingPrice = lastLowSwing[i]
                _s_OnCalculate_swing_index = i
            else:
                ZigzagStart[i] = High
                ZigzagStart[i - 1] = EMPTY_VALUE
        elif _sw1 == LL_FOUND:
            if PSAR[i] < low[i]:
                HL = Low
                if low[i] == HL:
                    ZigzagEnd[i] = HL
                else:
                    ZigzagEnd[i - bs] = HL
                lastHighSwing[i] = HL
                lastLowSwing[i] = EMPTY_VALUE
                currentState = HL_FOUND
                lastSwingPrice = lastHighSwing[i]
                _s_OnCalculate_swing_index = i
            else:
                ZigzagEnd[i] = Low
                ZigzagEnd[i - 1] = EMPTY_VALUE
        elif _sw1 == HL_FOUND:
            if PSAR[i] > high[i]:
                LH = High
                if high[i] == LH:
                    ZigzagStart[i] = LH
                else:
                    ZigzagStart[i - bs] = LH
                lastLowSwing[i] = LH
                lastHighSwing[i] = EMPTY_VALUE
                currentState = LH_FOUND
                lastSwingPrice = lastLowSwing[i]
                _s_OnCalculate_swing_index = i
            else:
                ZigzagStart[i] = High
                ZigzagStart[i - 1] = EMPTY_VALUE
        elif _sw1 == LH_FOUND:
            if PSAR[i] < low[i]:
                HH = Low
                if low[i] == HH:
                    ZigzagEnd[i] = HH
                else:
                    ZigzagEnd[i - bs] = HH
                lastHighSwing[i] = HH
                lastLowSwing[i] = EMPTY_VALUE
                currentState = HH_FOUND
                lastSwingPrice = lastHighSwing[i]
                _s_OnCalculate_swing_index = i
            else:
                ZigzagEnd[i] = Low
                ZigzagEnd[i - 1] = EMPTY_VALUE
        elif _sw1 == HH_FOUND:
            currentState = NONE
    return rates_total

# ---- static local variables
_s_OnCalculate_swing_index = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PSARZigzagV2(_MQL5Indicator):
    name = 'PSAR Zigzag v2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Backstep': 2,  # Backstep
        'SARStep': 0.01,  # SAR Step value
        'SARMaximum': 0.1,  # SAR Maximum value
    }

