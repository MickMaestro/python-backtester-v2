"""Constant Range Channel — converted from MQL5: MQL5 Indicators/Constant Range Channel/Constant Range Channel.mq5

MName
MetaTrader Indicator (Build 
Copyright: MCopyright; Link: MProfile; Version: MVersion

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'version': 'MVersion', 'copyright': 'MCopyright', 'link': 'MProfile', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [], 2: [], 3: []}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 2, 3: 0}, 'labels': {1: 'Upper', 2: 'Middle', 3: 'Lower'}, 'levels': [], 'description': ['MName', 'MetaTrader Indicator (Build '], 'name': 'Constant Range Channel', 'source': 'MQL5 Indicators/Constant Range Channel/Constant Range Channel.mq5', 'folder': 'Constant Range Channel', 'inputs': [{'mql': 'i_nStepTicks', 'py': 'i_nStepTicks', 'param': 'i_nStepTicks', 'type': 'uint', 'default': 50, 'label': 'Channel range step size (ticks)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
i_nStepTicks = _input('i_nStepTicks', 50)  # Channel range step size (ticks)
g_dbStepRange = 0.0  # Channel range step size
g_adbUpper = Arr(0, 0.0)  # Buffer for channel's upper level
g_adbMiddle = Arr(0, 0.0)  # Buffer for channel's middle level
g_adbLower = Arr(0, 0.0)  # Buffer for channel's lower level

def OnInit():
    global g_dbStepRange
    if i_nStepTicks < 1:
        Print('Error: Invalid ', 'Range step size!')
        return INIT_PARAMETERS_INCORRECT
    g_dbStepRange = WRONG_VALUE
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    iBuffer = 0
    SetIndexBuffer(((iBuffer := iBuffer + 1) - 1), g_adbUpper, INDICATOR_DATA)
    SetIndexBuffer(((iBuffer := iBuffer + 1) - 1), g_adbMiddle, INDICATOR_DATA)
    SetIndexBuffer(((iBuffer := iBuffer + 1) - 1), g_adbLower, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Constant Range Channel' + '(' + _str(i_nStepTicks) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global g_dbStepRange
    if g_dbStepRange < 0 and rates_total > 0:
        dbTickSize = Box(WRONG_VALUE)
        if SymbolInfoDouble(Symbol(), SYMBOL_TRADE_TICK_SIZE, dbTickSize) and dbTickSize.v > 0:
            g_dbStepRange = dbTickSize.v * i_nStepTicks
        else:
            return 0
    iCur = (0 if (prev_calculated < 1) else (prev_calculated - 1))
    iPrev = iCur - 1
    while True and iCur < rates_total:
        dbLow = low[iCur]
        dbHigh = high[iCur]
        dbMiddle = ((dbLow if (dbLow > g_adbUpper[iPrev]) else dbHigh if (dbHigh < g_adbLower[iPrev]) else g_adbMiddle[iPrev]) if (iPrev >= 0) else close[iCur])
        g_adbMiddle[iCur] = dbMiddle
        g_adbUpper[iCur] = dbMiddle + g_dbStepRange
        g_adbLower[iCur] = dbMiddle - g_dbStepRange
        iCur += 1
        iPrev += 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ConstantRangeChannel(_MQL5Indicator):
    name = 'Constant Range Channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'i_nStepTicks': 50,  # Channel range step size (ticks)
    }

