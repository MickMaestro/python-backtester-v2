"""x4period_rvi_arrows — converted from MQL5: MQL5 Indicators/X4Period_RVI_Arrows/x4period_rvi_arrows.mq5

Copyright: Copyright © 2005, transport_david; Link: http://finance.groups.yahoo.com/group/MetaTrader_Experts_and_Indicators/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, transport_david', 'link': 'http://finance.groups.yahoo.com/group/MetaTrader_Experts_and_Indicators/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 'colors': {1: [9639167], 2: [16748574], 3: [9639167], 4: [16748574], 5: [9639167], 6: [16748574], 7: [9639167], 8: [16748574]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'styles': {}, 'labels': {1: 'X4Period_RVI_Arrows Sell 1', 2: 'X4Period_RVI_Arrows Buy 1', 3: 'X4Period_RVI_Arrows Sell 2', 4: 'X4Period_RVI_Arrows Buy 2', 5: 'X4Period_RVI_Arrows Sell 3', 6: 'X4Period_RVI_Arrows Buy 3', 7: 'X4Period_RVI_Arrows Sell 4', 8: 'X4Period_RVI_Arrows Buy 4'}, 'levels': [], 'description': [], 'name': 'x4period_rvi_arrows', 'source': 'MQL5 Indicators/X4Period_RVI_Arrows/x4period_rvi_arrows.mq5', 'folder': 'X4Period_RVI_Arrows', 'inputs': [{'mql': 'RVIperiod1', 'py': 'RVIperiod1', 'param': 'RVIperiod1', 'type': 'uint', 'default': 7, 'label': 'Period 1', 'sinput': False}, {'mql': 'RVIperiod2', 'py': 'RVIperiod2', 'param': 'RVIperiod2', 'type': 'uint', 'default': 12, 'label': 'Period 2', 'sinput': False}, {'mql': 'RVIperiod3', 'py': 'RVIperiod3', 'param': 'RVIperiod3', 'type': 'uint', 'default': 18, 'label': 'Period 3', 'sinput': False}, {'mql': 'RVIperiod4', 'py': 'RVIperiod4', 'param': 'RVIperiod4', 'type': 'uint', 'default': 32, 'label': 'Period 4', 'sinput': False}, {'mql': 'Size', 'py': 'Size', 'param': 'Size', 'type': 'uint', 'default': 2, 'label': 'Vertical distance between the icons', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RVIperiod1 = _input('RVIperiod1', 7)  # Period 1
RVIperiod2 = _input('RVIperiod2', 12)  # Period 2
RVIperiod3 = _input('RVIperiod3', 18)  # Period 3
RVIperiod4 = _input('RVIperiod4', 32)  # Period 4
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
RVI_Handle = Arr(4, 0, dyn=False)
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = _int(MathMax(ATR_Period, RVIperiod1))
    min_rates_total = _int(MathMax(min_rates_total, RVIperiod2))
    min_rates_total = _int(MathMax(min_rates_total, RVIperiod3))
    min_rates_total = _int(MathMax(min_rates_total, RVIperiod4))
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
        return INIT_FAILED
    RVI_Handle[0] = iRVI(None, 0, RVIperiod1)
    if RVI_Handle[0] == INVALID_HANDLE:
        Print(' Failed to get the handle of the iRVI 1 calculator')
        return INIT_FAILED
    RVI_Handle[1] = iRVI(None, 0, RVIperiod2)
    if RVI_Handle[1] == INVALID_HANDLE:
        Print(' Failed to get the handle of the iRVI 2 calculator')
        return INIT_FAILED
    RVI_Handle[2] = iRVI(None, 0, RVIperiod3)
    if RVI_Handle[2] == INVALID_HANDLE:
        Print(' Failed to get the handle of the iRVI 3 calculator')
        return INIT_FAILED
    RVI_Handle[3] = iRVI(None, 0, RVIperiod4)
    if RVI_Handle[3] == INVALID_HANDLE:
        Print(' Failed to get the handle of the iRVI 4 calculator')
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
    short_name = 'X4Period_RVI_Arrows'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def InitTsIndArrBuffer(Number, Plot, IndBuffer, Empty_Value, Draw_Begin):
    SetIndexBuffer(Number, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(Plot, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Plot, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Plot, PLOT_ARROW, 159)
    ArraySetAsSeries(IndBuffer, True)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((((BarsCalculated(ATR_Handle) < rates_total or BarsCalculated(RVI_Handle[0]) < rates_total) or BarsCalculated(RVI_Handle[1]) < rates_total) or BarsCalculated(RVI_Handle[2]) < rates_total) or BarsCalculated(RVI_Handle[3]) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    RVI1 = Arr(0, 0.0)
    RVI2 = Arr(0, 0.0)
    RVI3 = Arr(0, 0.0)
    RVI4 = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    SIGN1 = Arr(0, 0.0)
    SIGN2 = Arr(0, 0.0)
    SIGN3 = Arr(0, 0.0)
    SIGN4 = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(RVI_Handle[0], 0, 0, to_copy, RVI1) <= 0:
        return 0
    if CopyBuffer(RVI_Handle[1], 0, 0, to_copy, RVI2) <= 0:
        return 0
    if CopyBuffer(RVI_Handle[2], 0, 0, to_copy, RVI3) <= 0:
        return 0
    if CopyBuffer(RVI_Handle[3], 0, 0, to_copy, RVI4) <= 0:
        return 0
    if CopyBuffer(RVI_Handle[0], 1, 0, to_copy, SIGN1) <= 0:
        return 0
    if CopyBuffer(RVI_Handle[1], 1, 0, to_copy, SIGN2) <= 0:
        return 0
    if CopyBuffer(RVI_Handle[2], 1, 0, to_copy, SIGN3) <= 0:
        return 0
    if CopyBuffer(RVI_Handle[3], 1, 0, to_copy, SIGN4) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(RVI1, True)
    ArraySetAsSeries(RVI2, True)
    ArraySetAsSeries(RVI3, True)
    ArraySetAsSeries(RVI4, True)
    ArraySetAsSeries(SIGN1, True)
    ArraySetAsSeries(SIGN2, True)
    ArraySetAsSeries(SIGN3, True)
    ArraySetAsSeries(SIGN4, True)
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
        if RVI1[bar] < SIGN1[bar]:
            SellBuffer1[bar] = high[bar] + ((ATR[bar] * (Size + 1)) / 8)
        if RVI1[bar] > SIGN1[bar]:
            BuyBuffer1[bar] = low[bar] - ((ATR[bar] * (Size + 1)) / 8)
        if RVI2[bar] < SIGN2[bar]:
            SellBuffer2[bar] = high[bar] + ((ATR[bar] * ((2 * Size) + 1)) / 8)
        if RVI2[bar] > SIGN2[bar]:
            BuyBuffer2[bar] = low[bar] - ((ATR[bar] * ((2 * Size) + 1)) / 8)
        if RVI3[bar] < SIGN3[bar]:
            SellBuffer3[bar] = high[bar] + ((ATR[bar] * ((3 * Size) + 1)) / 8)
        if RVI3[bar] > SIGN3[bar]:
            BuyBuffer3[bar] = low[bar] - ((ATR[bar] * ((3 * Size) + 1)) / 8)
        if RVI4[bar] < SIGN4[bar]:
            SellBuffer4[bar] = high[bar] + ((ATR[bar] * ((4 * Size) + 1)) / 8)
        if RVI4[bar] > SIGN4[bar]:
            BuyBuffer4[bar] = low[bar] - ((ATR[bar] * ((4 * Size) + 1)) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class X4periodRviArrows(_MQL5Indicator):
    name = 'x4period_rvi_arrows'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RVIperiod1': 7,  # Period 1
        'RVIperiod2': 12,  # Period 2
        'RVIperiod3': 18,  # Period 3
        'RVIperiod4': 32,  # Period 4
        'Size': 2,  # Vertical distance between the icons
    }

