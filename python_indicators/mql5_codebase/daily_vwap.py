"""Daily VWAP — converted from MQL5: MQL5 Indicators/Daily VWAP/Daily VWAP.mq5

Copyright: Guillermo Pineda; Link: www.mql5.com/en/users/syllyon; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Guillermo Pineda', 'link': 'www.mql5.com/en/users/syllyon', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'Daily VWAP'}, 'levels': [], 'description': [], 'name': 'Daily VWAP', 'source': 'MQL5 Indicators/Daily VWAP/Daily VWAP.mq5', 'folder': 'Daily VWAP', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
VWAPBuffer = Arr(0, 0.0)
CumulativeTPV = 0.0
CumulativeVolume = 0.0
dtLastDay = 0

def CreateDateTime(dtDay=946684800, pHour=0, pMinute=0, pSecond=0):
    dtReturnDate = 0
    timeStruct = MqlDateTime()
    TimeToStruct(dtDay, timeStruct)
    timeStruct.hour = pHour
    timeStruct.min = pMinute
    timeStruct.sec = pSecond
    dtReturnDate = StructToTime(timeStruct)
    return dtReturnDate

def OnInit():
    SetIndexBuffer(0, VWAPBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Daily VWAP')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global CumulativeTPV, CumulativeVolume, dtLastDay
    start = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    if prev_calculated == 0:
        dtLastDay = 0
    for i in range(start, rates_total):
        timeStruct = MqlDateTime()
        TimeToStruct(time[i], timeStruct)
        if i > 0:
            prevTimeStruct = MqlDateTime()
            TimeToStruct(time[i - 1], prevTimeStruct)
            if timeStruct.day != prevTimeStruct.day:
                CumulativeTPV = 0.0
                CumulativeVolume = 0.0
        typicalPrice = (high[i] + low[i] + close[i]) / 3.0
        barVolume = (tick_volume[i] if (tick_volume[i] > 1) else 1)
        CumulativeTPV += typicalPrice * barVolume
        CumulativeVolume += float(barVolume)
        VWAPBuffer[i] = (_fdiv(CumulativeTPV, CumulativeVolume) if (CumulativeVolume != 0) else 0.0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DailyVWAP(_MQL5Indicator):
    name = 'Daily VWAP'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

