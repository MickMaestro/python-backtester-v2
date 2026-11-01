"""Cronex_T_RSI_BBSW — converted from MQL5: MQL5 Indicators/Cronex T RSI BBSW/Cronex_T_RSI_BBSW.mq5

Copyright: Copyright © 2017, Cronex; Link: http://www.metaquotes.net/

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Cronex', 'link': 'http://www.metaquotes.net/', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 7}, 'types': {}, 'colors': {1: [36095], 2: [11829830], 3: [16711680], 4: [65535], 5: [32768], 6: [16711680], 7: [255]}, 'widths': {1: 2, 5: 1, 6: 2, 7: 2}, 'styles': {5: 0}, 'labels': {}, 'levels': [10.0, -10.0], 'description': [], 'name': 'Cronex_T_RSI_BBSW', 'source': 'MQL5 Indicators/Cronex T RSI BBSW/Cronex_T_RSI_BBSW.mq5', 'folder': 'Cronex T RSI BBSW', 'inputs': [{'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'int', 'default': 16, 'label': '', 'sinput': False}, {'mql': 'TCurvature', 'py': 'TCurvature', 'param': 'TCurvature', 'type': 'double', 'default': 0.618, 'label': '', 'sinput': False}, {'mql': 'WideMethod', 'py': 'WideMethod', 'param': 'WideMethod', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'BandsPeriod', 'py': 'BandsPeriod', 'param': 'BandsPeriod', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'BandsDeviations', 'py': 'BandsDeviations', 'param': 'BandsDeviations', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'BandsShift', 'py': 'BandsShift', 'param': 'BandsShift', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RSIPeriod = _input('RSIPeriod', 16)
TCurvature = _input('TCurvature', 0.618)
WideMethod = _input('WideMethod', False)
BandsPeriod = _input('BandsPeriod', 20)
BandsDeviations = _input('BandsDeviations', 2)
BandsShift = _input('BandsShift', 0)
RSITArray = Arr(0, 0.0)
RSIArray = Arr(0, 0.0)
BBMDArray = Arr(0, 0.0)
BBUPArray = Arr(0, 0.0)
BBDNArray = Arr(0, 0.0)
MaxArray = Arr(0, 0.0)
MinArray = Arr(0, 0.0)
BandsHandle = 0
CronesSubHandle = 0

def OnInit():
    global BandsHandle, CronesSubHandle
    SetIndexBuffer(0, RSITArray, INDICATOR_DATA)
    SetIndexBuffer(1, RSIArray, INDICATOR_DATA)
    SetIndexBuffer(2, BBMDArray, INDICATOR_DATA)
    SetIndexBuffer(3, BBUPArray, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BBDNArray, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, MaxArray, INDICATOR_DATA)
    SetIndexBuffer(6, MinArray, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(3, PLOT_LINE_WIDTH, 1)
    PlotIndexSetInteger(3, PLOT_LINE_STYLE, STYLE_DOT)
    PlotIndexSetInteger(3, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(4, PLOT_LINE_WIDTH, 1)
    PlotIndexSetInteger(4, PLOT_LINE_STYLE, STYLE_DOT)
    PlotIndexSetInteger(4, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(5, PLOT_DRAW_TYPE, DRAW_HISTOGRAM)
    PlotIndexSetInteger(6, PLOT_DRAW_TYPE, DRAW_HISTOGRAM)
    PlotIndexSetString(0, PLOT_LABEL, 'RSI T')
    PlotIndexSetString(1, PLOT_LABEL, 'RSI')
    PlotIndexSetString(2, PLOT_LABEL, 'BB Middle')
    PlotIndexSetString(3, PLOT_LABEL, 'BB Upper')
    PlotIndexSetString(4, PLOT_LABEL, 'BB Lower')
    PlotIndexSetString(5, PLOT_LABEL, 'Max Point')
    PlotIndexSetString(6, PLOT_LABEL, 'Min Point')
    IndicatorSetInteger(INDICATOR_DIGITS, _int(SymbolInfoInteger(None, SYMBOL_DIGITS)))
    IndicatorSetString(INDICATOR_SHORTNAME, 'Cronex T RSI BBS (' + IntegerToString(RSIPeriod) + ')')
    CronesSubHandle = iCustom(Symbol(), Period(), 'Cronex_T_RSI_BBSW_sub', RSIPeriod, TCurvature)
    BandsHandle = iBands(Symbol(), Period(), BandsPeriod, BandsShift, BandsDeviations, CronesSubHandle)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    to_calc = rates_total - prev_calculated
    CopyBuffer(CronesSubHandle, 0, 0, to_calc, RSITArray)
    CopyBuffer(CronesSubHandle, 1, 0, to_calc, RSIArray)
    CopyBuffer(BandsHandle, 0, 0, to_calc, BBMDArray)
    CopyBuffer(BandsHandle, 1, 0, to_calc, BBUPArray)
    CopyBuffer(BandsHandle, 2, 0, to_calc, BBDNArray)
    i = 0
    c = 0
    i = 0
    for i in range(i, to_calc):
        c = prev_calculated + i
        MaxArray[c] = 0.0
        MinArray[c] = 0.0
        if ((((BBMDArray[c] < 100 and BBMDArray[c] > -100) and BBUPArray[c] < 100) and BBUPArray[c] > -100) and BBDNArray[c] < 100) and BBDNArray[c] > -100:
            if WideMethod:
                if RSITArray[c] > BBMDArray[c]:
                    if (RSITArray[c] - BBMDArray[c]) > (RSITArray[c - 1] - BBMDArray[c - 1]):
                        MaxArray[c] = RSITArray[c] - BBMDArray[c]
                    else:
                        MinArray[c] = RSITArray[c] - BBMDArray[c]
                elif RSITArray[c] < BBMDArray[c]:
                    if (RSITArray[c] - BBMDArray[c]) < (RSITArray[c - 1] - BBMDArray[c - 1]):
                        MinArray[c] = RSITArray[c] - BBMDArray[c]
                    else:
                        MaxArray[c] = RSITArray[c] - BBMDArray[c]
            else:
                if RSIArray[c] > BBUPArray[c]:
                    MaxArray[c] = RSIArray[c] - BBUPArray[c]
                if RSIArray[c] < BBDNArray[c]:
                    MinArray[c] = RSIArray[c] - BBDNArray[c]
    else:
        i = _range_end(i, to_calc, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CronexTRSIBBSW(_MQL5Indicator):
    name = 'Cronex_T_RSI_BBSW'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSIPeriod': 16,
        'TCurvature': 0.618,
        'WideMethod': False,
        'BandsPeriod': 20,
        'BandsDeviations': 2,
        'BandsShift': 0,
    }

