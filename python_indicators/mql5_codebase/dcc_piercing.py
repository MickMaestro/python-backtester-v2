"""DCC_Piercing — converted from MQL5: MQL5 Indicators/DCC _ Piercing/DCC_Piercing.mq5

Copyright: Rajesh Nait, Copyright 2023; Link: https://www.mql5.com/en/users/rajeshnait/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Rajesh Nait, Copyright 2023', 'link': 'https://www.mql5.com/en/users/rajeshnait/seller', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16448255], 2: [16448255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: '+DCCP', 2: '-DCCP'}, 'levels': [], 'description': [], 'name': 'DCC_Piercing', 'source': 'MQL5 Indicators/DCC _ Piercing/DCC_Piercing.mq5', 'folder': 'DCC _ Piercing', 'inputs': [{'mql': 'InpBullishDCCPCode', 'py': 'InpBullishDCCPCode', 'param': 'InpBullishDCCPCode', 'type': 'uchar', 'default': 217, 'label': 'BullishDCCP: code for style DRAW_ARROW (font Wingdings)', 'sinput': False}, {'mql': 'InpBullishDCCPShift', 'py': 'InpBullishDCCPShift', 'param': 'InpBullishDCCPShift', 'type': 'int', 'default': 10, 'label': 'BullishDCCP: vertical shift of arrows in pixels', 'sinput': False}, {'mql': 'InpBearishDCCPCode', 'py': 'InpBearishDCCPCode', 'param': 'InpBearishDCCPCode', 'type': 'uchar', 'default': 218, 'label': 'BearishDCCP: code for style DRAW_ARROW (font Wingdings)', 'sinput': False}, {'mql': 'InpBearishDCCPShift', 'py': 'InpBearishDCCPShift', 'param': 'InpBearishDCCPShift', 'type': 'int', 'default': 10, 'label': 'BearishDCCP: vertical shift of arrows in pixels', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpBullishDCCPCode = _input('InpBullishDCCPCode', 217)  # BullishDCCP: code for style DRAW_ARROW (font Wingdings)
InpBullishDCCPShift = _input('InpBullishDCCPShift', 10)  # BullishDCCP: vertical shift of arrows in pixels
InpBearishDCCPCode = _input('InpBearishDCCPCode', 218)  # BearishDCCP: code for style DRAW_ARROW (font Wingdings)
InpBearishDCCPShift = _input('InpBearishDCCPShift', 10)  # BearishDCCP: vertical shift of arrows in pixels
BullishDCCPBuffer = Arr(0, 0.0)
BearishDCCPBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, BullishDCCPBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, BearishDCCPBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, InpBullishDCCPCode)
    PlotIndexSetInteger(1, PLOT_ARROW, InpBearishDCCPCode)
    ArraySetAsSeries(BullishDCCPBuffer, True)
    ArraySetAsSeries(BearishDCCPBuffer, True)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, InpBullishDCCPShift)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, -InpBearishDCCPShift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    for i in range(limit, 0 - 1, -1):
        BullishDCCPBuffer[i] = 0.0
        BearishDCCPBuffer[i] = 0.0
        BearishDCCPBuffer[0] = 0.0
        if (open[i] > close[i] and open[i + 1] < close[i + 1]) and open[i] > close[i + 1]:
            BearishDCCPBuffer[i] = high[i]
        BullishDCCPBuffer[0] = 0.0
        if (open[i] < close[i] and open[i + 1] > close[i + 1]) and open[i] < close[i + 1]:
            BullishDCCPBuffer[i] = low[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DCCPiercing(_MQL5Indicator):
    name = 'DCC_Piercing'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpBullishDCCPCode': 217,  # BullishDCCP: code for style DRAW_ARROW (font Wingdings)
        'InpBullishDCCPShift': 10,  # BullishDCCP: vertical shift of arrows in pixels
        'InpBearishDCCPCode': 218,  # BearishDCCP: code for style DRAW_ARROW (font Wingdings)
        'InpBearishDCCPShift': 10,  # BearishDCCP: vertical shift of arrows in pixels
    }

