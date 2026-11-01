"""Heikin Ashi Lines — converted from MQL5: MQL5 Indicators/Heikin Ashi Lines/Heikin Ashi Lines.mq5

MName
MetaTrader Indicator (Build 
Copyright: MCopyright; Link: MProfile; Version: MVersion

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'version': 'MVersion', 'copyright': 'MCopyright', 'link': 'MProfile', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {1: 1, 2: 1}, 'colors': {1: [8421504], 2: [8421504]}, 'widths': {1: 1, 2: 2}, 'styles': {1: 2, 2: 0}, 'labels': {1: 'haOpen', 2: 'haClose'}, 'levels': [], 'description': ['MName', 'MetaTrader Indicator (Build '], 'name': 'Heikin Ashi Lines', 'source': 'MQL5 Indicators/Heikin Ashi Lines/Heikin Ashi Lines.mq5', 'folder': 'Heikin Ashi Lines', 'inputs': [{'mql': 'i_dbPeriod', 'py': 'i_dbPeriod', 'param': 'i_dbPeriod', 'type': 'double', 'default': 3.0, 'label': 'Averaging period (standard = 3.0)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
i_dbPeriod = _input('i_dbPeriod', 3.0)  # Averaging period (standard = 3.0)
g_adbHaOpen = Arr(0, 0.0)  # Buffer for Heikin Ashi open price (exponential moving average)
g_adbHaClose = Arr(0, 0.0)  # Buffer for Heikin Ashi close price (total price)
g_dbAlphaWeight = 0.0  # Alpha weight to be used for exponential moving average

def OnInit():
    global g_dbAlphaWeight
    if i_dbPeriod < 1.0:
        Print('Error: Invalid ', 'averaging period!')
        return INIT_PARAMETERS_INCORRECT
    g_dbAlphaWeight = _fdiv(2.0, i_dbPeriod + 1.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, g_adbHaOpen, INDICATOR_DATA)
    SetIndexBuffer(1, g_adbHaClose, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Heikin Ashi Lines' + '(' + DoubleToString(i_dbPeriod, 3) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    iCur = (0 if (prev_calculated < 1) else (prev_calculated - 1))
    iPrev = iCur - 1
    while True and iCur < rates_total:
        dbHaClosePrev = (g_adbHaClose[iPrev] if (iPrev >= 0) else close[iCur])
        dbHaOpenPrev = (g_adbHaOpen[iPrev] if (iPrev >= 0) else open[iCur])
        g_adbHaOpen[iCur] = dbHaOpenPrev + ((dbHaClosePrev - dbHaOpenPrev) * g_dbAlphaWeight)
        g_adbHaClose[iCur] = (open[iCur] + close[iCur] + high[iCur] + low[iCur]) * 0.25
        iCur += 1
        iPrev += 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HeikinAshiLines(_MQL5Indicator):
    name = 'Heikin Ashi Lines'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'i_dbPeriod': 3.0,  # Averaging period (standard = 3.0)
    }

