"""x4period_wpr_arrows — converted from MQL5: MQL5 Indicators/X4Period_WPR_Arrows/x4period_wpr_arrows.mq5

Copyright: Copyright © 2005, transport_david; Link: http://finance.groups.yahoo.com/group/MetaTrader_Experts_and_Indicators/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, transport_david', 'link': 'http://finance.groups.yahoo.com/group/MetaTrader_Experts_and_Indicators/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 'colors': {1: [11823615], 2: [13749760], 3: [11823615], 4: [13749760], 5: [11823615], 6: [13749760], 7: [11823615], 8: [13749760]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2}, 'styles': {}, 'labels': {1: 'X4Period_WPR_Arrows Sell 1', 2: 'X4Period_WPR_Arrows Buy 1', 3: 'X4Period_WPR_Arrows Sell 2', 4: 'X4Period_WPR_Arrows Buy 2', 5: 'X4Period_WPR_Arrows Sell 3', 6: 'X4Period_WPR_Arrows Buy 3', 7: 'X4Period_WPR_Arrows Sell 4', 8: 'X4Period_WPR_Arrows Buy 4'}, 'levels': [], 'description': [], 'name': 'x4period_wpr_arrows', 'source': 'MQL5 Indicators/X4Period_WPR_Arrows/x4period_wpr_arrows.mq5', 'folder': 'X4Period_WPR_Arrows', 'inputs': [{'mql': 'WPRKperiod1', 'py': 'WPRKperiod1', 'param': 'WPRKperiod1', 'type': 'int', 'default': 5, 'label': 'Period 1', 'sinput': False}, {'mql': 'WPRKperiod2', 'py': 'WPRKperiod2', 'param': 'WPRKperiod2', 'type': 'int', 'default': 7, 'label': 'Period 2', 'sinput': False}, {'mql': 'WPRKperiod3', 'py': 'WPRKperiod3', 'param': 'WPRKperiod3', 'type': 'int', 'default': 11, 'label': 'Period 3', 'sinput': False}, {'mql': 'WPRKperiod4', 'py': 'WPRKperiod4', 'param': 'WPRKperiod4', 'type': 'int', 'default': 17, 'label': 'Period 4', 'sinput': False}, {'mql': 'rsiUpperTrigger', 'py': 'rsiUpperTrigger', 'param': 'rsiUpperTrigger', 'type': 'int', 'default': -20, 'label': 'Overbought level', 'sinput': False}, {'mql': 'rsiLowerTrigger', 'py': 'rsiLowerTrigger', 'param': 'rsiLowerTrigger', 'type': 'int', 'default': -80, 'label': 'Oversold level', 'sinput': False}, {'mql': 'Size', 'py': 'Size', 'param': 'Size', 'type': 'uint', 'default': 2, 'label': 'Vertical distance between the icons', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
WPRKperiod1 = _input('WPRKperiod1', 5)  # Period 1
WPRKperiod2 = _input('WPRKperiod2', 7)  # Period 2
WPRKperiod3 = _input('WPRKperiod3', 11)  # Period 3
WPRKperiod4 = _input('WPRKperiod4', 17)  # Period 4
rsiUpperTrigger = _input('rsiUpperTrigger', -20)  # Overbought level
rsiLowerTrigger = _input('rsiLowerTrigger', -80)  # Oversold level
Size = _input('Size', 2)  # Vertical distance between the icons
SellBuffer1 = Arr(0, 0.0)
BuyBuffer1 = Arr(0, 0.0)
SellBuffer2 = Arr(0, 0.0)
BuyBuffer2 = Arr(0, 0.0)
SellBuffer3 = Arr(0, 0.0)
BuyBuffer3 = Arr(0, 0.0)
SellBuffer4 = Arr(0, 0.0)
BuyBuffer4 = Arr(0, 0.0)
ATR_Handle = 0
WPR_Handle = Arr(4, 0, dyn=False)
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = MathMax(ATR_Period, WPRKperiod1)
    min_rates_total = MathMax(min_rates_total, WPRKperiod2)
    min_rates_total = MathMax(min_rates_total, WPRKperiod3)
    min_rates_total = MathMax(min_rates_total, WPRKperiod4)
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
        return INIT_FAILED
    WPR_Handle[0] = iWPR(None, 0, WPRKperiod1)
    if WPR_Handle[0] == INVALID_HANDLE:
        Print(' Failed to get handle of the iWPR 1 indicator')
        return INIT_FAILED
    WPR_Handle[1] = iWPR(None, 0, WPRKperiod2)
    if WPR_Handle[1] == INVALID_HANDLE:
        Print(' Failed to get handle of the iWPR 2 indicator')
        return INIT_FAILED
    WPR_Handle[2] = iWPR(None, 0, WPRKperiod3)
    if WPR_Handle[2] == INVALID_HANDLE:
        Print(' Failed to get handle of the iWPR 3 indicator')
        return INIT_FAILED
    WPR_Handle[3] = iWPR(None, 0, WPRKperiod4)
    if WPR_Handle[3] == INVALID_HANDLE:
        Print(' Failed to get handle of the iWPR 4 indicator')
        return INIT_FAILED
    InitTsIndArrBuffer(0, 0, SellBuffer1, 0.0, min_rates_total)
    InitTsIndArrBuffer(1, 1, BuyBuffer1, 0.0, min_rates_total)
    InitTsIndArrBuffer(2, 2, SellBuffer2, 0.0, min_rates_total)
    InitTsIndArrBuffer(3, 3, BuyBuffer2, 0.0, min_rates_total)
    InitTsIndArrBuffer(4, 4, SellBuffer3, 0.0, min_rates_total)
    InitTsIndArrBuffer(5, 5, BuyBuffer3, 0.0, min_rates_total)
    InitTsIndArrBuffer(6, 6, SellBuffer4, 0.0, min_rates_total)
    InitTsIndArrBuffer(7, 7, BuyBuffer4, 0.0, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'X4Period_WPR_Arrows'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def InitTsIndArrBuffer(Number, Plot, IndBuffer, Empty_Value, Draw_Begin):
    SetIndexBuffer(Number, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(Plot, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Plot, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Plot, PLOT_ARROW, 167)
    ArraySetAsSeries(IndBuffer, True)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((((BarsCalculated(ATR_Handle) < rates_total or BarsCalculated(WPR_Handle[0]) < rates_total) or BarsCalculated(WPR_Handle[1]) < rates_total) or BarsCalculated(WPR_Handle[2]) < rates_total) or BarsCalculated(WPR_Handle[3]) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    WPR1 = Arr(0, 0.0)
    WPR2 = Arr(0, 0.0)
    WPR3 = Arr(0, 0.0)
    WPR4 = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(WPR_Handle[0], 0, 0, to_copy, WPR1) <= 0:
        return 0
    if CopyBuffer(WPR_Handle[1], 0, 0, to_copy, WPR2) <= 0:
        return 0
    if CopyBuffer(WPR_Handle[2], 0, 0, to_copy, WPR3) <= 0:
        return 0
    if CopyBuffer(WPR_Handle[3], 0, 0, to_copy, WPR4) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(WPR1, True)
    ArraySetAsSeries(WPR2, True)
    ArraySetAsSeries(WPR3, True)
    ArraySetAsSeries(WPR4, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer1[bar] = 0.0
        SellBuffer1[bar] = 0.0
        BuyBuffer2[bar] = 0.0
        SellBuffer2[bar] = 0.0
        BuyBuffer3[bar] = 0.0
        SellBuffer3[bar] = 0.0
        BuyBuffer4[bar] = 0.0
        SellBuffer4[bar] = 0.0
        if WPR1[bar] < rsiLowerTrigger:
            SellBuffer1[bar] = high[bar] + ((ATR[bar] * (Size + 1)) / 8)
        if WPR1[bar] > rsiUpperTrigger:
            BuyBuffer1[bar] = low[bar] - ((ATR[bar] * (Size + 1)) / 8)
        if WPR2[bar] < rsiLowerTrigger:
            SellBuffer2[bar] = high[bar] + ((ATR[bar] * ((2 * Size) + 1)) / 8)
        if WPR2[bar] > rsiUpperTrigger:
            BuyBuffer2[bar] = low[bar] - ((ATR[bar] * ((2 * Size) + 1)) / 8)
        if WPR3[bar] < rsiLowerTrigger:
            SellBuffer3[bar] = high[bar] + ((ATR[bar] * ((3 * Size) + 1)) / 8)
        if WPR3[bar] > rsiUpperTrigger:
            BuyBuffer3[bar] = low[bar] - ((ATR[bar] * ((3 * Size) + 1)) / 8)
        if WPR4[bar] < rsiLowerTrigger:
            SellBuffer4[bar] = high[bar] + ((ATR[bar] * ((4 * Size) + 1)) / 8)
        if WPR4[bar] > rsiUpperTrigger:
            BuyBuffer4[bar] = low[bar] - ((ATR[bar] * ((4 * Size) + 1)) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class X4periodWprArrows(_MQL5Indicator):
    name = 'x4period_wpr_arrows'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'WPRKperiod1': 5,  # Period 1
        'WPRKperiod2': 7,  # Period 2
        'WPRKperiod3': 11,  # Period 3
        'WPRKperiod4': 17,  # Period 4
        'rsiUpperTrigger': -20,  # Overbought level
        'rsiLowerTrigger': -80,  # Oversold level
        'Size': 2,  # Vertical distance between the icons
    }

