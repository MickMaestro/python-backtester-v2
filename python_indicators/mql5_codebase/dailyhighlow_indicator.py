"""DailyHighLow Indicator — converted from MQL5: MQL5 Indicators/DailyHighLow Indicator for MQL5/DailyHighLow Indicator.mq5

Copyright: Copyright 2023, Geraked; Link: https://github.com/geraked; Version: 1.3

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, Geraked', 'link': 'https://github.com/geraked', 'version': '1.3', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [12632256], 2: [12632256]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'High', 2: 'Low'}, 'levels': [], 'description': [], 'name': 'DailyHighLow Indicator', 'source': 'MQL5 Indicators/DailyHighLow Indicator for MQL5/DailyHighLow Indicator.mq5', 'folder': 'DailyHighLow Indicator for MQL5', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16408, 'label': '', 'sinput': False}, {'mql': 'Previous', 'py': 'Previous', 'param': 'Previous', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_DHL_PRICE
DHL_LOWHIGH = 0
DHL_OPENCLOSE = 1
DHL_CLOSECLOSE = 2
_enum('ENUM_DHL_PRICE', {0: 'DHL_LOWHIGH', 1: 'DHL_OPENCLOSE', 2: 'DHL_CLOSECLOSE'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_D1)
Previous = _input('Previous', True)
Price = _input('Price', DHL_LOWHIGH)
tf = 0
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)

def OnInit():
    global tf
    SetIndexBuffer(0, HighBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, LowBuffer, INDICATOR_DATA)
    tf = (PERIOD_CURRENT if (PeriodSeconds(TimeFrame) < PeriodSeconds(PERIOD_CURRENT)) else TimeFrame)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(HighBuffer, True)
    ArraySetAsSeries(LowBuffer, True)
    limit = rates_total - prev_calculated
    if limit == 0:
        limit = 1
    i1 = iBarShift(None, 0, iTime(None, tf, 1))
    i2 = iBarShift(None, 0, iTime(None, tf, 2))
    if i1 == -1 or i2 == -1:
        return 0
    k = i2 - i1
    limit = MathMax(i2 - i1 + 2, limit)
    if limit > rates_total:
        return 0
    if iBarShift(None, tf, time[rates_total - (i2 - i1 + 2)]) == -1:
        return 0
    for i in range(0, limit):
        j = iBarShift(None, tf, time[i])
        if j == -1:
            continue
        if Previous:
            j += 1
        if Price == DHL_LOWHIGH:
            HighBuffer[i] = iHigh(None, tf, j)
            LowBuffer[i] = iLow(None, tf, j)
        else:
            i1_2 = iBarShift(None, 0, iTime(None, tf, j))
            i2_2 = (0 if (j == 0) else iBarShift(None, 0, iTime(None, tf, j - 1)))
            cnt = i1_2 - i2_2
            if cnt < k:
                cnt += 1
            elif cnt == k:
                if i1_2 > i2_2:
                    i2_2 += 1
            ihc = iHighest(None, 0, MODE_CLOSE, cnt, i2_2)
            iho = iHighest(None, 0, MODE_OPEN, cnt, i2_2)
            ilc = iLowest(None, 0, MODE_CLOSE, cnt, i2_2)
            ilo = iLowest(None, 0, MODE_OPEN, cnt, i2_2)
            if ihc < 0 or ihc >= rates_total:
                continue
            if iho < 0 or iho >= rates_total:
                continue
            if ilc < 0 or ilc >= rates_total:
                continue
            if ilo < 0 or ilo >= rates_total:
                continue
            if Price == DHL_CLOSECLOSE:
                HighBuffer[i] = close[ihc]
                LowBuffer[i] = close[ilc]
            elif Price == DHL_OPENCLOSE:
                HighBuffer[i] = MathMax(close[ihc], open[iho])
                LowBuffer[i] = MathMin(close[ilc], open[ilo])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DailyHighLowIndicator(_MQL5Indicator):
    name = 'DailyHighLow Indicator'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),
        'Previous': True,
        'Price': _Choice({0: 'Low/High', 1: 'Open/Close', 2: 'Close/Close'}, default=0),
    }

