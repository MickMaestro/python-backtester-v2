"""Minions.TimedMAs — converted from MQL5: MQL5 Indicators/Time Based Moving Averages/Minions.TimedMAs.mq5

Minions in the quest for showing you the Perfect Timing through MAs
 
(CC) Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License
Copyright: www.MinionsLabs.com; Link: http://www.MinionsLabs.com; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.MinionsLabs.com', 'link': 'http://www.MinionsLabs.com', 'version': '1.0', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [255], 2: [65535], 3: [42495], 4: [16748574], 5: [13382297], 6: [11119017]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 1}, 'labels': {1: 'MA1', 2: 'MA2', 3: 'MA3', 4: 'MA4', 5: 'MA5', 6: 'MA6'}, 'levels': [], 'description': ['Minions in the quest for showing you the Perfect Timing through MAs', ' ', '(CC) Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License'], 'name': 'Minions.TimedMAs', 'source': 'MQL5 Indicators/Time Based Moving Averages/Minions.TimedMAs.mq5', 'folder': 'Time Based Moving Averages', 'inputs': [{'mql': 'inpMA1Period', 'py': 'inpMA1Period', 'param': 'inpMA1Period', 'type': 'int', 'default': 15, 'label': 'MA1 Period (M1=15/M5=0/M15=0)', 'sinput': False}, {'mql': 'inpMA2Period', 'py': 'inpMA2Period', 'param': 'inpMA2Period', 'type': 'int', 'default': 30, 'label': 'MA2 Period (M1=30/M5=0/M15=0)', 'sinput': False}, {'mql': 'inpMA3Period', 'py': 'inpMA3Period', 'param': 'inpMA3Period', 'type': 'int', 'default': 60, 'label': 'MA3 Period (M1=60/M5=12/M15=0)', 'sinput': False}, {'mql': 'inpMA4Period', 'py': 'inpMA4Period', 'param': 'inpMA4Period', 'type': 'int', 'default': 120, 'label': 'MA4 Period (M1=120/M5=24/M15=8)', 'sinput': False}, {'mql': 'inpMA5Period', 'py': 'inpMA5Period', 'param': 'inpMA5Period', 'type': 'int', 'default': 180, 'label': 'MA5 Period (M1=180/M5=36/M15=12)', 'sinput': False}, {'mql': 'inpMA6Period', 'py': 'inpMA6Period', 'param': 'inpMA6Period', 'type': 'int', 'default': 540, 'label': 'MA6 Period (M1=540/M5=108/M15=36)', 'sinput': False}, {'mql': 'inpMethod', 'py': 'inpMethod', 'param': 'inpMethod', 'type': 'int', 'default': 1, 'label': 'Smoothing Method', 'sinput': False}, {'mql': 'inpAppliedPrice', 'py': 'inpAppliedPrice', 'param': 'inpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'MA Price used', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpMA1Period = _input('inpMA1Period', 15)  # MA1 Period (M1=15/M5=0/M15=0)
inpMA2Period = _input('inpMA2Period', 30)  # MA2 Period (M1=30/M5=0/M15=0)
inpMA3Period = _input('inpMA3Period', 60)  # MA3 Period (M1=60/M5=12/M15=0)
inpMA4Period = _input('inpMA4Period', 120)  # MA4 Period (M1=120/M5=24/M15=8)
inpMA5Period = _input('inpMA5Period', 180)  # MA5 Period (M1=180/M5=36/M15=12)
inpMA6Period = _input('inpMA6Period', 540)  # MA6 Period (M1=540/M5=108/M15=36)
inpMethod = _input('inpMethod', MODE_EMA)  # Smoothing Method
inpAppliedPrice = _input('inpAppliedPrice', PRICE_CLOSE)  # MA Price used
bufferMA1_ID = 0
bufferMA2_ID = 1
bufferMA3_ID = 2
bufferMA4_ID = 3
bufferMA5_ID = 4
bufferMA6_ID = 5
bufferMA1 = Arr(0, 0.0)
bufferMA2 = Arr(0, 0.0)
bufferMA3 = Arr(0, 0.0)
bufferMA4 = Arr(0, 0.0)
bufferMA5 = Arr(0, 0.0)
bufferMA6 = Arr(0, 0.0)
hMA1 = 0  # MAs indicators handles
hMA2 = 0
hMA3 = 0
hMA4 = 0
hMA5 = 0
hMA6 = 0

def OnInit():
    global hMA1, hMA2, hMA3, hMA4, hMA5, hMA6
    SetIndexBuffer(bufferMA1_ID, bufferMA1, INDICATOR_DATA)
    SetIndexBuffer(bufferMA2_ID, bufferMA2, INDICATOR_DATA)
    SetIndexBuffer(bufferMA3_ID, bufferMA3, INDICATOR_DATA)
    SetIndexBuffer(bufferMA4_ID, bufferMA4, INDICATOR_DATA)
    SetIndexBuffer(bufferMA5_ID, bufferMA5, INDICATOR_DATA)
    SetIndexBuffer(bufferMA6_ID, bufferMA6, INDICATOR_DATA)
    PlotIndexSetInteger(bufferMA1_ID, PLOT_DRAW_BEGIN, inpMA1Period)
    PlotIndexSetInteger(bufferMA2_ID, PLOT_DRAW_BEGIN, inpMA2Period)
    PlotIndexSetInteger(bufferMA3_ID, PLOT_DRAW_BEGIN, inpMA3Period)
    PlotIndexSetInteger(bufferMA4_ID, PLOT_DRAW_BEGIN, inpMA4Period)
    PlotIndexSetInteger(bufferMA5_ID, PLOT_DRAW_BEGIN, inpMA5Period)
    PlotIndexSetInteger(bufferMA6_ID, PLOT_DRAW_BEGIN, inpMA6Period)
    if inpMA1Period > 0:
        hMA1 = iMA(Symbol(), Period(), inpMA1Period, 0, inpMethod, inpAppliedPrice)
    if inpMA2Period > 0:
        hMA2 = iMA(Symbol(), Period(), inpMA2Period, 0, inpMethod, inpAppliedPrice)
    if inpMA3Period > 0:
        hMA3 = iMA(Symbol(), Period(), inpMA3Period, 0, inpMethod, inpAppliedPrice)
    if inpMA4Period > 0:
        hMA4 = iMA(Symbol(), Period(), inpMA4Period, 0, inpMethod, inpAppliedPrice)
    if inpMA5Period > 0:
        hMA5 = iMA(Symbol(), Period(), inpMA5Period, 0, inpMethod, inpAppliedPrice)
    if inpMA6Period > 0:
        hMA6 = iMA(Symbol(), Period(), inpMA6Period, 0, inpMethod, inpAppliedPrice)
    if ((((hMA1 == INVALID_HANDLE or hMA2 == INVALID_HANDLE) or hMA3 == INVALID_HANDLE) or hMA4 == INVALID_HANDLE) or hMA5 == INVALID_HANDLE) or hMA6 == INVALID_HANDLE:
        Print('Error starting MA indicators!')
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    values_to_copy = 0
    if prev_calculated == 0 or rates_total > (prev_calculated + 1):
        values_to_copy = rates_total
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if inpMA1Period > 0 and (not FillArrayFromBuffer(hMA1, 0, values_to_copy, bufferMA1)):
        return 0
    if inpMA2Period > 0 and (not FillArrayFromBuffer(hMA2, 0, values_to_copy, bufferMA2)):
        return 0
    if inpMA3Period > 0 and (not FillArrayFromBuffer(hMA3, 0, values_to_copy, bufferMA3)):
        return 0
    if inpMA4Period > 0 and (not FillArrayFromBuffer(hMA4, 0, values_to_copy, bufferMA4)):
        return 0
    if inpMA5Period > 0 and (not FillArrayFromBuffer(hMA5, 0, values_to_copy, bufferMA5)):
        return 0
    if inpMA6Period > 0 and (not FillArrayFromBuffer(hMA6, 0, values_to_copy, bufferMA6)):
        return 0
    return rates_total

def FillArrayFromBuffer(indicatorHandle, indicatorInternalBuffer, itemsQty, bufferToCopyInto):
    ResetLastError()
    if CopyBuffer(indicatorHandle, indicatorInternalBuffer, 0, itemsQty, bufferToCopyInto) < 0:
        Print('Failed to copy data from the Indicator. Error Code:', GetLastError())
        return False
    return True

def OnDeinit(reason):
    IndicatorRelease(hMA1)
    IndicatorRelease(hMA2)
    IndicatorRelease(hMA3)
    IndicatorRelease(hMA4)
    IndicatorRelease(hMA5)
    IndicatorRelease(hMA6)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MinionsTimedMAs(_MQL5Indicator):
    name = 'Minions.TimedMAs'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpMA1Period': 15,  # MA1 Period (M1=15/M5=0/M15=0)
        'inpMA2Period': 30,  # MA2 Period (M1=30/M5=0/M15=0)
        'inpMA3Period': 60,  # MA3 Period (M1=60/M5=12/M15=0)
        'inpMA4Period': 120,  # MA4 Period (M1=120/M5=24/M15=8)
        'inpMA5Period': 180,  # MA5 Period (M1=180/M5=36/M15=12)
        'inpMA6Period': 540,  # MA6 Period (M1=540/M5=108/M15=36)
        'inpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Smoothing Method
        'inpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA Price used
    }

