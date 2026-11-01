"""Wilder's Average True Range — converted from MQL5: MQL5 Indicators/Wilder's Average True Range (ATR)/Wilder's Average True Range.mq5

MName
An implementation of the original Average True Range indicator by John Welles Wilder Jr.
as described in his book, New Concepts in Technical Trading Systems [1978].
MetaTrader Indicator (Build 
Copyright: MCopyright; Link: MProfile; Version: MVersion

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'version': 'MVersion', 'copyright': 'MCopyright', 'link': 'MProfile', 'window': 'separate', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {1: 1}, 'colors': {1: [10135078]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Average true range'}, 'levels': [], 'description': ['MName', 'An implementation of the original Average True Range indicator by John Welles Wilder Jr.', 'as described in his book, New Concepts in Technical Trading Systems [1978].', 'MetaTrader Indicator (Build '], 'name': "Wilder's Average True Range", 'source': "MQL5 Indicators/Wilder's Average True Range (ATR)/Wilder's Average True Range.mq5", 'folder': "Wilder's Average True Range (ATR)", 'inputs': [{'mql': 'i_dbAveragingPeriod', 'py': 'i_dbAveragingPeriod', 'param': 'i_dbAveragingPeriod', 'type': 'double', 'default': 7.0, 'label': 'Averaging period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
i_dbAveragingPeriod = _input('i_dbAveragingPeriod', 7.0)  # Averaging period
g_adbATR = Arr(0, 0.0)  # Buffer for average true range
g_dbEmaWeight = 0.0  # Weight to be used for exponential moving averages

def OnInit():
    global g_dbEmaWeight
    if i_dbAveragingPeriod < 1.0:
        Print('Error: Invalid ', 'averaging period')
        return INIT_PARAMETERS_INCORRECT
    g_dbEmaWeight = 1.0 / i_dbAveragingPeriod
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, g_adbATR, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat("Wilder's Average True Range (ATR) ( %.2f )", i_dbAveragingPeriod))
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    iCur = (0 if (prev_calculated < 1 or prev_calculated > rates_total) else (prev_calculated - 1))
    iPrev = iCur - 1
    while True and iCur < rates_total:
        if iPrev >= 0:
            dbClosePrev = close[iPrev]
            dbTrueRange = fmax(high[iCur], dbClosePrev) - fmin(low[iCur], dbClosePrev)
            dbATRPrev = g_adbATR[iPrev]
            g_adbATR[iCur] = dbATRPrev + ((dbTrueRange - dbATRPrev) * g_dbEmaWeight)
        else:
            g_adbATR[iCur] = high[iCur] - low[iCur]
        iCur += 1
        iPrev += 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WilderSAverageTrueRange(_MQL5Indicator):
    name = "Wilder's Average True Range"
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'i_dbAveragingPeriod': 7.0,  # Averaging period
    }

