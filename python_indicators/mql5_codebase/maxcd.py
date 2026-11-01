"""MAxCD — converted from MQL5: MQL5 Indicators/MAxCD/MAxCD.mq5

Three Moving Averages Convergence/Divergence.
Copyright: Copyright 2019, Roberto Jacobs (3rjfx) ~ By 3rjfx ~ Created: 2019/07/18; Link: https://www.mql5.com/en/users/3rjfx; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2019, Roberto Jacobs (3rjfx) ~ By 3rjfx ~ Created: 2019/07/18', 'link': 'https://www.mql5.com/en/users/3rjfx', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 3, 2: 3, 3: 3}, 'colors': {1: [14822282], 2: [16448255], 3: [16776960]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'MAIN', 2: 'MIDLE', 3: 'FAST'}, 'levels': [], 'description': ['Three Moving Averages Convergence/Divergence.'], 'name': 'MAxCD', 'source': 'MQL5 Indicators/MAxCD/MAxCD.mq5', 'folder': 'MAxCD', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MA1720 = Arr(0, 0.0)
MA2320 = Arr(0, 0.0)
MA1723 = Arr(0, 0.0)
ExtMAIN = Arr(0, 0.0)
ExtMIDL = Arr(0, 0.0)
ExtFAST = Arr(0, 0.0)
ind_name = ""
CDM1MaHandle = 0
CDM2MaHandle = 0
CDM3MaHandle = 0

def OnInit():
    global CDM1MaHandle, CDM2MaHandle, CDM3MaHandle, ind_name
    SetIndexBuffer(0, ExtMAIN, INDICATOR_DATA)
    SetIndexBuffer(1, ExtMIDL, INDICATOR_DATA)
    SetIndexBuffer(2, ExtFAST, INDICATOR_DATA)
    SetIndexBuffer(3, MA1720, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, MA2320, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, MA1723, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, True)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, True)
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, True)
    ind_name = 'MAxCD'
    IndicatorSetString(INDICATOR_SHORTNAME, ind_name)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    CDM1MaHandle = iMA(Symbol(), 0, 10, 0, MODE_LWMA, PRICE_CLOSE)
    CDM2MaHandle = iMA(Symbol(), 0, 23, 0, MODE_LWMA, PRICE_OPEN)
    CDM3MaHandle = iMA(Symbol(), 0, 20, 0, MODE_SMMA, PRICE_MEDIAN)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 53:
        return 0
    calculated = BarsCalculated(CDM1MaHandle)
    if calculated < rates_total:
        return 0
    calculated = BarsCalculated(CDM2MaHandle)
    if calculated < rates_total:
        return 0
    calculated = BarsCalculated(CDM3MaHandle)
    if calculated < rates_total:
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if False:
        return 0
    if CopyBuffer(CDM1MaHandle, 0, 0, to_copy, MA1720) <= 0:
        Print('Getting CDM1 MA buffers is failed! Error', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(CDM2MaHandle, 0, 0, to_copy, MA2320) <= 0:
        Print('Getting CDM2 MA buffers is failed! Error', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(CDM3MaHandle, 0, 0, to_copy, MA1723) <= 0:
        Print('Getting CDM3 MA buffers is failed! Error', GetLastError())
        return 0
    i = 0
    limit = 0
    if prev_calculated == 0:
        limit = 1
    else:
        limit = prev_calculated - 1
    ArrayResize(ExtMAIN, limit)
    ArrayResize(ExtMIDL, limit)
    ArrayResize(ExtFAST, limit)
    ArrayResize(MA1720, limit)
    ArrayResize(MA2320, limit)
    ArrayResize(MA1723, limit)
    ArraySetAsSeries(ExtMAIN, True)
    ArraySetAsSeries(ExtMIDL, True)
    ArraySetAsSeries(ExtFAST, True)
    ArraySetAsSeries(MA1720, True)
    ArraySetAsSeries(MA2320, True)
    ArraySetAsSeries(MA1723, True)
    i = limit - 1
    for i in range(i, 0 - 1, -1):
        ExtMAIN[i] = MA1720[i] - MA1723[i]
        ExtMIDL[i] = MA2320[i] - MA1723[i]
        ExtFAST[i] = MA1720[i] - MA2320[i]
    else:
        i = _range_end(i, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MAxCD(_MQL5Indicator):
    name = 'MAxCD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
    }

