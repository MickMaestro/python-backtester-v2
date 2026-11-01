"""RangeBreakOut — converted from MQL5: MQL5 Indicators/Range BreakOut Indicator - Indicator Buffer Only/RangeBreakOut.mq5

Download Expert Advisors and Indicator for FREE!
Want an EA with Indicator, contact me on telegram: @sopheak_khmer_trader
Copyright: BestForexScript.Com; Link: https://bestforexscript.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'BestForexScript.Com', 'link': 'https://bestforexscript.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 7}, 'colors': {1: [16711680], 2: [16711680], 3: [16748574, 255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Range High', 2: 'Range Low', 3: 'Range Fill'}, 'levels': [], 'description': ['Download Expert Advisors and Indicator for FREE!', 'Want an EA with Indicator, contact me on telegram: @sopheak_khmer_trader'], 'name': 'RangeBreakOut', 'source': 'MQL5 Indicators/Range BreakOut Indicator - Indicator Buffer Only/RangeBreakOut.mq5', 'folder': 'Range BreakOut Indicator - Indicator Buffer Only', 'inputs': [{'mql': 'InpFromTime', 'py': 'InpFromTime', 'param': None, 'type': 'string', 'default': '00:00', 'label': 'Range Start Time', 'sinput': False}, {'mql': 'InpToTime', 'py': 'InpToTime', 'param': None, 'type': 'string', 'default': '05:00', 'label': 'Range End Time', 'sinput': False}, {'mql': 'InpEndTime', 'py': 'InpEndTime', 'param': None, 'type': 'string', 'default': '20:00', 'label': 'Trade End Time', 'sinput': False}, {'mql': 'InpMinPip', 'py': 'InpMinPip', 'param': 'InpMinPip', 'type': 'int', 'default': 250, 'label': 'Minimum Size (point)', 'sinput': False}, {'mql': 'InpMaxPip', 'py': 'InpMaxPip', 'param': 'InpMaxPip', 'type': 'int', 'default': 500, 'label': 'Maximum Size (point)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpFromTime = _input('InpFromTime', '00:00')  # Range Start Time
InpToTime = _input('InpToTime', '05:00')  # Range End Time
InpEndTime = _input('InpEndTime', '20:00')  # Trade End Time
InpMinPip = _input('InpMinPip', 250)  # Minimum Size (point)
InpMaxPip = _input('InpMaxPip', 500)  # Maximum Size (point)
maxday = 10
ZoneHighBuffer = Arr(0, 0.0)
ZoneLowBuffer = Arr(0, 0.0)
FillHighBuffer = Arr(0, 0.0)
FillLowBuffer = Arr(0, 0.0)
FillColors = Arr(0, 0.0)

def OnInit():
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, ZoneHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ZoneLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, FillHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, FillLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, FillColors, INDICATOR_COLOR_INDEX)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RangeBreakOut (' + InpFromTime + '-' + InpToTime + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global maxday
    if PeriodSeconds(PERIOD_CURRENT) > PeriodSeconds(PERIOD_H1):
        return 0
    if maxday > iBars(Symbol(), PERIOD_D1):
        maxday = iBars(Symbol(), PERIOD_D1)
    if rates_total < 4:
        return 0
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(ZoneHighBuffer, True)
    ArraySetAsSeries(ZoneLowBuffer, True)
    ArraySetAsSeries(FillHighBuffer, True)
    ArraySetAsSeries(FillLowBuffer, True)
    ArraySetAsSeries(FillColors, True)
    dtime = iTime(Symbol(), PERIOD_D1, maxday - 1)
    limit = iBarShift(Symbol(), Period(), dtime, False)
    for i in range(limit, 0 - 1, -1):
        dt = MqlDateTime()
        TimeToStruct(time[i], dt)
        fromtime = StringToTime(_str(dt.year) + '.' + _str(dt.mon) + '.' + _str(dt.day) + ' ' + InpFromTime + ':00')
        totime = StringToTime(_str(dt.year) + '.' + _str(dt.mon) + '.' + _str(dt.day) + ' ' + InpToTime + ':00')
        endtime = StringToTime(_str(dt.year) + '.' + _str(dt.mon) + '.' + _str(dt.day) + ' ' + InpEndTime + ':00')
        if totime < fromtime:
            totime += 24 * 3600
        if endtime < fromtime:
            endtime += 24 * 3600
        fromshift = iBarShift(Symbol(), Period(), fromtime, False)
        toshift = iBarShift(Symbol(), Period(), totime, False)
        highest = iHighest(Symbol(), Period(), MODE_HIGH, fromshift - toshift + 1, toshift)
        lowest = iLowest(Symbol(), Period(), MODE_LOW, fromshift - toshift + 1, toshift)
        zhigh = high[highest]
        zlow = low[lowest]
        zlength = zhigh - zlow
        if zhigh == 0 or zlow == 0:
            continue
        ZoneHighBuffer[i] = EMPTY_VALUE
        ZoneLowBuffer[i] = EMPTY_VALUE
        FillHighBuffer[i] = 0.0
        FillLowBuffer[i] = 0.0
        if time[i] >= fromtime and time[i] <= endtime:
            if time[i] <= totime:
                if zlength >= (InpMinPip * Point()) and zlength <= (InpMaxPip * Point()):
                    FillHighBuffer[i] = zhigh
                    FillLowBuffer[i] = zlow
                    FillColors[i] = 0.0
                else:
                    FillHighBuffer[i] = zlow
                    FillLowBuffer[i] = zhigh
                    FillColors[i] = 1.0
            ZoneHighBuffer[i] = zhigh
            ZoneLowBuffer[i] = zlow
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RangeBreakOut(_MQL5Indicator):
    name = 'RangeBreakOut'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpMinPip': 250,  # Minimum Size (point)
        'InpMaxPip': 500,  # Maximum Size (point)
    }

