"""Monthly VWAP — converted from MQL5: MQL5 Indicators/Monthly VWAP/Monthly VWAP.mq5

Copyright: Guillermo Pineda; Link: www.mql5.com/en/users/syllyon; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Guillermo Pineda', 'link': 'www.mql5.com/en/users/syllyon', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'Monthly VWAP'}, 'levels': [], 'description': [], 'name': 'Monthly VWAP', 'source': 'MQL5 Indicators/Monthly VWAP/Monthly VWAP.mq5', 'folder': 'Monthly VWAP', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
VWAPBuffer = Arr(0, 0.0)
nPriceArr = Arr(0, 0.0)
nTotalTPV = Arr(0, 0.0)
nTotalVol = Arr(0, 0.0)
nSumMonthlyTPV = 0.0
nSumMonthlyVol = 0.0
nIdx = 0
nIdxMonthly = 0
bIsFirstRun = True
LastTimePeriod = PERIOD_MN1

def CreateDateTime(dtDay=946684800, pHour=0, pMinute=0, pSecond=0):
    dtReturnDate = 0
    timeStruct = MqlDateTime()
    TimeToStruct(dtDay, timeStruct)
    timeStruct.hour = pHour
    timeStruct.min = pMinute
    timeStruct.sec = pSecond
    dtReturnDate = StructToTime(timeStruct)
    timeStruct.day = 1
    dtReturnDate = StructToTime(timeStruct)
    return dtReturnDate

def OnInit():
    SetIndexBuffer(0, VWAPBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Monthly VWAP')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global LastTimePeriod, bIsFirstRun, dtLastMonth, nIdx, nIdxMonthly, nSumMonthlyTPV, nSumMonthlyVol
    if PERIOD_CURRENT != LastTimePeriod:
        bIsFirstRun = True
        LastTimePeriod = PERIOD_CURRENT
    if rates_total > prev_calculated or bIsFirstRun:
        ArrayResize(nPriceArr, rates_total)
        ArrayResize(nTotalTPV, rates_total)
        ArrayResize(nTotalVol, rates_total)
        nIdx = nIdxMonthly
        nSumMonthlyTPV = 0.0
        nSumMonthlyVol = 0.0
        while nIdx < rates_total:
            if CreateDateTime(time[nIdx]) != dtLastMonth:
                nIdxMonthly = nIdx
                nSumMonthlyTPV = 0.0
                nSumMonthlyVol = 0.0
            nPriceArr[nIdx] = (close[nIdx] + high[nIdx] + low[nIdx]) / 3
            if tick_volume[nIdx]:
                nTotalTPV[nIdx] = nPriceArr[nIdx] * tick_volume[nIdx]
                nTotalVol[nIdx] = float(tick_volume[nIdx])
            elif volume[nIdx]:
                nTotalTPV[nIdx] = nPriceArr[nIdx] * volume[nIdx]
                nTotalVol[nIdx] = float(volume[nIdx])
            if nIdx >= nIdxMonthly:
                nSumMonthlyTPV += nTotalTPV[nIdx]
                nSumMonthlyVol += nTotalVol[nIdx]
                VWAPBuffer[nIdx] = _fdiv(nSumMonthlyTPV, nSumMonthlyVol)
            dtLastMonth = CreateDateTime(time[nIdx])
            nIdx += 1
        bIsFirstRun = False
    return rates_total

# ---- global variables initialised from expressions
dtLastMonth = CreateDateTime()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MonthlyVWAP(_MQL5Indicator):
    name = 'Monthly VWAP'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

