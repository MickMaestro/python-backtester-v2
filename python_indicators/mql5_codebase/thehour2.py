"""TheHour2 — converted from MQL5: MQL5 Indicators/Buffers for each hour (binary) and an hour buffer from 0-23 - for data collection purposes/TheHour2.mq5

Copyright: Sam Beatson, PhD; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Sam Beatson, PhD', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 25, 'indicator_plots': 25}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {1: 'Hour 00', 2: 'Hour 01', 3: 'Hour 02', 4: 'Hour 03', 5: 'Hour 04', 6: 'Hour 05', 7: 'Hour 06', 8: 'Hour 07', 9: 'Hour 08', 10: 'Hour 09', 11: 'Hour 10', 12: 'Hour 11', 13: 'Hour 12', 14: 'Hour 13', 15: 'Hour 14', 16: 'Hour 15', 17: 'Hour 16', 18: 'Hour 17', 19: 'Hour 18', 20: 'Hour 19', 21: 'Hour 20', 22: 'Hour 21', 23: 'Hour 22', 24: 'Hour 23', 25: 'Hour'}, 'levels': [], 'description': [], 'name': 'TheHour2', 'source': 'MQL5 Indicators/Buffers for each hour (binary) and an hour buffer from 0-23 - for data collection purposes/TheHour2.mq5', 'folder': 'Buffers for each hour (binary) and an hour buffer from 0-23 - for data collection purposes', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
hourBuffer0 = Arr(0, 0.0)
hourBuffer1 = Arr(0, 0.0)
hourBuffer2 = Arr(0, 0.0)
hourBuffer3 = Arr(0, 0.0)
hourBuffer4 = Arr(0, 0.0)
hourBuffer5 = Arr(0, 0.0)
hourBuffer6 = Arr(0, 0.0)
hourBuffer7 = Arr(0, 0.0)
hourBuffer8 = Arr(0, 0.0)
hourBuffer9 = Arr(0, 0.0)
hourBuffer10 = Arr(0, 0.0)
hourBuffer11 = Arr(0, 0.0)
hourBuffer12 = Arr(0, 0.0)
hourBuffer13 = Arr(0, 0.0)
hourBuffer14 = Arr(0, 0.0)
hourBuffer15 = Arr(0, 0.0)
hourBuffer16 = Arr(0, 0.0)
hourBuffer17 = Arr(0, 0.0)
hourBuffer18 = Arr(0, 0.0)
hourBuffer19 = Arr(0, 0.0)
hourBuffer20 = Arr(0, 0.0)
hourBuffer21 = Arr(0, 0.0)
hourBuffer22 = Arr(0, 0.0)
hourBuffer23 = Arr(0, 0.0)
hourBuffer = Arr(0, 0.0)
bar_hour = 0

def OnInit():
    IndicatorSetString(INDICATOR_SHORTNAME, 'Hourly Buffers (0/1)')
    SetIndexBuffer(0, hourBuffer0, INDICATOR_DATA)
    SetIndexBuffer(1, hourBuffer1, INDICATOR_DATA)
    SetIndexBuffer(2, hourBuffer2, INDICATOR_DATA)
    SetIndexBuffer(3, hourBuffer3, INDICATOR_DATA)
    SetIndexBuffer(4, hourBuffer4, INDICATOR_DATA)
    SetIndexBuffer(5, hourBuffer5, INDICATOR_DATA)
    SetIndexBuffer(6, hourBuffer6, INDICATOR_DATA)
    SetIndexBuffer(7, hourBuffer7, INDICATOR_DATA)
    SetIndexBuffer(8, hourBuffer8, INDICATOR_DATA)
    SetIndexBuffer(9, hourBuffer9, INDICATOR_DATA)
    SetIndexBuffer(10, hourBuffer10, INDICATOR_DATA)
    SetIndexBuffer(11, hourBuffer11, INDICATOR_DATA)
    SetIndexBuffer(12, hourBuffer12, INDICATOR_DATA)
    SetIndexBuffer(13, hourBuffer13, INDICATOR_DATA)
    SetIndexBuffer(14, hourBuffer14, INDICATOR_DATA)
    SetIndexBuffer(15, hourBuffer15, INDICATOR_DATA)
    SetIndexBuffer(16, hourBuffer16, INDICATOR_DATA)
    SetIndexBuffer(17, hourBuffer17, INDICATOR_DATA)
    SetIndexBuffer(18, hourBuffer18, INDICATOR_DATA)
    SetIndexBuffer(19, hourBuffer19, INDICATOR_DATA)
    SetIndexBuffer(20, hourBuffer20, INDICATOR_DATA)
    SetIndexBuffer(21, hourBuffer21, INDICATOR_DATA)
    SetIndexBuffer(22, hourBuffer22, INDICATOR_DATA)
    SetIndexBuffer(23, hourBuffer23, INDICATOR_DATA)
    SetIndexBuffer(24, hourBuffer, INDICATOR_DATA)
    for i in range(0, 24):
        PlotIndexSetInteger(i, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetInteger(i, PLOT_SHOW_DATA, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bar_hour
    if rates_total <= 0:
        return 0
    start = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    for i in range(start, rates_total):
        bar_hour = _int(_idiv(_imod(time[i], 86400), 3600))
        hourBuffer0[i] = 0.0
        hourBuffer1[i] = 0.0
        hourBuffer2[i] = 0.0
        hourBuffer3[i] = 0.0
        hourBuffer4[i] = 0.0
        hourBuffer5[i] = 0.0
        hourBuffer6[i] = 0.0
        hourBuffer7[i] = 0.0
        hourBuffer8[i] = 0.0
        hourBuffer9[i] = 0.0
        hourBuffer10[i] = 0.0
        hourBuffer11[i] = 0.0
        hourBuffer12[i] = 0.0
        hourBuffer13[i] = 0.0
        hourBuffer14[i] = 0.0
        hourBuffer15[i] = 0.0
        hourBuffer16[i] = 0.0
        hourBuffer17[i] = 0.0
        hourBuffer18[i] = 0.0
        hourBuffer19[i] = 0.0
        hourBuffer20[i] = 0.0
        hourBuffer21[i] = 0.0
        hourBuffer22[i] = 0.0
        hourBuffer23[i] = 0.0
        hourBuffer[i] = EMPTY_VALUE
        _sw1 = bar_hour
        if _sw1 == 0:
            hourBuffer0[i] = 1.0
            hourBuffer[i] = bar_hour
        elif _sw1 == 1:
            hourBuffer1[i] = 1.0
            hourBuffer[i] = bar_hour
        elif _sw1 == 2:
            hourBuffer2[i] = 1.0
            hourBuffer[i] = bar_hour
        elif _sw1 == 3:
            hourBuffer3[i] = 1.0
            hourBuffer[i] = bar_hour
        elif _sw1 == 4:
            hourBuffer4[i] = 1.0
            hourBuffer[i] = bar_hour
        elif _sw1 == 5:
            hourBuffer5[i] = 1.0
            hourBuffer[i] = bar_hour
        elif _sw1 == 6:
            hourBuffer6[i] = 1.0
            hourBuffer[i] = bar_hour
        elif _sw1 == 7:
            hourBuffer7[i] = 1.0
            hourBuffer[i] = bar_hour
        elif _sw1 == 8:
            hourBuffer8[i] = 1.0
            hourBuffer[i] = bar_hour
        elif _sw1 == 9:
            hourBuffer9[i] = 1.0
            hourBuffer[i] = bar_hour
        elif _sw1 == 10:
            hourBuffer10[i] = 1.0
            hourBuffer[i] = bar_hour
        elif _sw1 == 11:
            hourBuffer11[i] = 1.0
            hourBuffer[i] = bar_hour
        elif _sw1 == 12:
            hourBuffer12[i] = 1.0
            hourBuffer[i] = bar_hour
        elif _sw1 == 13:
            hourBuffer13[i] = 1.0
            hourBuffer[i] = bar_hour
        elif _sw1 == 14:
            hourBuffer14[i] = 1.0
            hourBuffer[i] = bar_hour
        elif _sw1 == 15:
            hourBuffer15[i] = 1.0
            hourBuffer[i] = bar_hour
        elif _sw1 == 16:
            hourBuffer16[i] = 1.0
            hourBuffer[i] = bar_hour
        elif _sw1 == 17:
            hourBuffer17[i] = 1.0
            hourBuffer[i] = bar_hour
        elif _sw1 == 18:
            hourBuffer18[i] = 1.0
            hourBuffer[i] = bar_hour
        elif _sw1 == 19:
            hourBuffer19[i] = 1.0
            hourBuffer[i] = bar_hour
        elif _sw1 == 20:
            hourBuffer20[i] = 1.0
            hourBuffer[i] = bar_hour
        elif _sw1 == 21:
            hourBuffer21[i] = 1.0
            hourBuffer[i] = bar_hour
        elif _sw1 == 22:
            hourBuffer22[i] = 1.0
            hourBuffer[i] = bar_hour
        elif _sw1 == 23:
            hourBuffer23[i] = 1.0
            hourBuffer[i] = bar_hour
        localHourText = HourToText(bar_hour)
        Comment('The hour is: ', localHourText)
    return rates_total

def HourToText(bh):
    TextHour = ""
    _sw2 = bh
    if _sw2 == 0:
        TextHour = '12 am'
    elif _sw2 == 1:
        TextHour = '1 am'
    elif _sw2 == 2:
        TextHour = '2 am'
    elif _sw2 == 3:
        TextHour = '3 am'
    elif _sw2 == 4:
        TextHour = '4 am'
    elif _sw2 == 5:
        TextHour = '5 am'
    elif _sw2 == 6:
        TextHour = '6 am'
    elif _sw2 == 7:
        TextHour = '7 am'
    elif _sw2 == 8:
        TextHour = '8 am'
    elif _sw2 == 9:
        TextHour = '9 am'
    elif _sw2 == 10:
        TextHour = '10 am'
    elif _sw2 == 11:
        TextHour = '11 am'
    elif _sw2 == 12:
        TextHour = '12 pm'
    elif _sw2 == 13:
        TextHour = '1 pm'
    elif _sw2 == 14:
        TextHour = '2 pm'
    elif _sw2 == 15:
        TextHour = '3 pm'
    elif _sw2 == 16:
        TextHour = '4 pm'
    elif _sw2 == 17:
        TextHour = '5 pm'
    elif _sw2 == 18:
        TextHour = '6 pm'
    elif _sw2 == 19:
        TextHour = '7 pm'
    elif _sw2 == 20:
        TextHour = '8 pm'
    elif _sw2 == 21:
        TextHour = '9 pm'
    elif _sw2 == 22:
        TextHour = '10 pm'
    elif _sw2 == 23:
        TextHour = '11 pm'
    else:
        TextHour = 'Unknown'
    return TextHour


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TheHour2(_MQL5Indicator):
    name = 'TheHour2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

