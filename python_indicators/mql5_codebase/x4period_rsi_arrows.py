"""x4period_rsi_arrows — converted from MQL5: MQL5 Indicators/X4Period_RSI_Arrows/x4period_rsi_arrows.mq5

Copyright: Copyright © 2005, transport_david; Link: http://finance.groups.yahoo.com/group/MetaTrader_Experts_and_Indicators/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, transport_david', 'link': 'http://finance.groups.yahoo.com/group/MetaTrader_Experts_and_Indicators/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 'colors': {1: [16711935], 2: [65280], 3: [16711935], 4: [65280], 5: [16711935], 6: [65280], 7: [16711935], 8: [65280]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2}, 'styles': {}, 'labels': {1: 'X4Period_RSI_Arrows Sell 1', 2: 'X4Period_RSI_Arrows Buy 1', 3: 'X4Period_RSI_Arrows Sell 2', 4: 'X4Period_RSI_Arrows Buy 2', 5: 'X4Period_RSI_Arrows Sell 3', 6: 'X4Period_RSI_Arrows Buy 3', 7: 'X4Period_RSI_Arrows Sell 4', 8: 'X4Period_RSI_Arrows Buy 4'}, 'levels': [], 'description': [], 'name': 'x4period_rsi_arrows', 'source': 'MQL5 Indicators/X4Period_RSI_Arrows/x4period_rsi_arrows.mq5', 'folder': 'X4Period_RSI_Arrows', 'inputs': [{'mql': 'RSIperiod1', 'py': 'RSIperiod1', 'param': 'RSIperiod1', 'type': 'uint', 'default': 7, 'label': 'Period 1', 'sinput': False}, {'mql': 'RSIperiod2', 'py': 'RSIperiod2', 'param': 'RSIperiod2', 'type': 'uint', 'default': 12, 'label': 'Period 2', 'sinput': False}, {'mql': 'RSIperiod3', 'py': 'RSIperiod3', 'param': 'RSIperiod3', 'type': 'uint', 'default': 18, 'label': 'Period 3', 'sinput': False}, {'mql': 'RSIperiod4', 'py': 'RSIperiod4', 'param': 'RSIperiod4', 'type': 'uint', 'default': 32, 'label': 'Period 4', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 7, 'label': 'Price', 'sinput': False}, {'mql': 'rsiUpperTrigger', 'py': 'rsiUpperTrigger', 'param': 'rsiUpperTrigger', 'type': 'uint', 'default': 62, 'label': 'Overbought level', 'sinput': False}, {'mql': 'rsiLowerTrigger', 'py': 'rsiLowerTrigger', 'param': 'rsiLowerTrigger', 'type': 'uint', 'default': 38, 'label': 'Oversold level', 'sinput': False}, {'mql': 'Size', 'py': 'Size', 'param': 'Size', 'type': 'uint', 'default': 2, 'label': 'Vertical distance between the icons', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RSIperiod1 = _input('RSIperiod1', 7)  # Period 1
RSIperiod2 = _input('RSIperiod2', 12)  # Period 2
RSIperiod3 = _input('RSIperiod3', 18)  # Period 3
RSIperiod4 = _input('RSIperiod4', 32)  # Period 4
applied_price = _input('applied_price', PRICE_WEIGHTED)  # Price
rsiUpperTrigger = _input('rsiUpperTrigger', 62)  # Overbought level
rsiLowerTrigger = _input('rsiLowerTrigger', 38)  # Oversold level
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
RSI_Handle = Arr(4, 0, dyn=False)
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = _int(MathMax(ATR_Period, RSIperiod1))
    min_rates_total = _int(MathMax(min_rates_total, RSIperiod2))
    min_rates_total = _int(MathMax(min_rates_total, RSIperiod3))
    min_rates_total = _int(MathMax(min_rates_total, RSIperiod4))
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
        return INIT_FAILED
    RSI_Handle[0] = iRSI(None, 0, RSIperiod1, applied_price)
    if RSI_Handle[0] == INVALID_HANDLE:
        Print(' Failed to get the handle of the iRSI 1 indicator')
        return INIT_FAILED
    RSI_Handle[1] = iRSI(None, 0, RSIperiod2, applied_price)
    if RSI_Handle[1] == INVALID_HANDLE:
        Print(' Failed to get the handle of the iRSI 2 indicator')
        return INIT_FAILED
    RSI_Handle[2] = iRSI(None, 0, RSIperiod3, applied_price)
    if RSI_Handle[2] == INVALID_HANDLE:
        Print(' Failed to get the handle of the iRSI 3 indicator')
        return INIT_FAILED
    RSI_Handle[3] = iRSI(None, 0, RSIperiod4, applied_price)
    if RSI_Handle[3] == INVALID_HANDLE:
        Print(' Failed to get the handle of the iRSI 4 indicator')
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
    short_name = 'X4Period_RSI_Arrows'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def InitTsIndArrBuffer(Number, Plot, IndBuffer, Empty_Value, Draw_Begin):
    SetIndexBuffer(Number, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(Plot, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Plot, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Plot, PLOT_ARROW, 159)
    ArraySetAsSeries(IndBuffer, True)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((((BarsCalculated(ATR_Handle) < rates_total or BarsCalculated(RSI_Handle[0]) < rates_total) or BarsCalculated(RSI_Handle[1]) < rates_total) or BarsCalculated(RSI_Handle[2]) < rates_total) or BarsCalculated(RSI_Handle[3]) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    RSI1 = Arr(0, 0.0)
    RSI2 = Arr(0, 0.0)
    RSI3 = Arr(0, 0.0)
    RSI4 = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(RSI_Handle[0], 0, 0, to_copy, RSI1) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[1], 0, 0, to_copy, RSI2) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[2], 0, 0, to_copy, RSI3) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[3], 0, 0, to_copy, RSI4) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(RSI1, True)
    ArraySetAsSeries(RSI2, True)
    ArraySetAsSeries(RSI3, True)
    ArraySetAsSeries(RSI4, True)
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
        if RSI1[bar] < rsiLowerTrigger:
            SellBuffer1[bar] = high[bar] + ((ATR[bar] * (Size + 1)) / 8)
        if RSI1[bar] > rsiUpperTrigger:
            BuyBuffer1[bar] = low[bar] - ((ATR[bar] * (Size + 1)) / 8)
        if RSI2[bar] < rsiLowerTrigger:
            SellBuffer2[bar] = high[bar] + ((ATR[bar] * ((2 * Size) + 1)) / 8)
        if RSI2[bar] > rsiUpperTrigger:
            BuyBuffer2[bar] = low[bar] - ((ATR[bar] * ((2 * Size) + 1)) / 8)
        if RSI3[bar] < rsiLowerTrigger:
            SellBuffer3[bar] = high[bar] + ((ATR[bar] * ((3 * Size) + 1)) / 8)
        if RSI3[bar] > rsiUpperTrigger:
            BuyBuffer3[bar] = low[bar] - ((ATR[bar] * ((3 * Size) + 1)) / 8)
        if RSI4[bar] < rsiLowerTrigger:
            SellBuffer4[bar] = high[bar] + ((ATR[bar] * ((4 * Size) + 1)) / 8)
        if RSI4[bar] > rsiUpperTrigger:
            BuyBuffer4[bar] = low[bar] - ((ATR[bar] * ((4 * Size) + 1)) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class X4periodRsiArrows(_MQL5Indicator):
    name = 'x4period_rsi_arrows'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSIperiod1': 7,  # Period 1
        'RSIperiod2': 12,  # Period 2
        'RSIperiod3': 18,  # Period 3
        'RSIperiod4': 32,  # Period 4
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=7),  # Price
        'rsiUpperTrigger': 62,  # Overbought level
        'rsiLowerTrigger': 38,  # Oversold level
        'Size': 2,  # Vertical distance between the icons
    }

