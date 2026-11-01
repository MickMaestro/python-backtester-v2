"""x4period_stochastic_arrows — converted from MQL5: MQL5 Indicators/X4Period_Stochastic_Arrows/x4period_stochastic_arrows.mq5

Copyright: Copyright © 2005, transport_david; Link: http://finance.groups.yahoo.com/group/MetaTrader_Experts_and_Indicators/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, transport_david', 'link': 'http://finance.groups.yahoo.com/group/MetaTrader_Experts_and_Indicators/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 'colors': {1: [42495], 2: [32768], 3: [42495], 4: [32768], 5: [42495], 6: [32768], 7: [42495], 8: [32768]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2}, 'styles': {}, 'labels': {1: 'X4Period_Stochastic_Arrows Sell 1', 2: 'X4Period_Stochastic_Arrows Buy 1', 3: 'X4Period_Stochastic_Arrows Sell 2', 4: 'X4Period_Stochastic_Arrows Buy 2', 5: 'X4Period_Stochastic_Arrows Sell 3', 6: 'X4Period_Stochastic_Arrows Buy 3', 7: 'X4Period_Stochastic_Arrows Sell 4', 8: 'X4Period_Stochastic_Arrows Buy 4'}, 'levels': [], 'description': [], 'name': 'x4period_stochastic_arrows', 'source': 'MQL5 Indicators/X4Period_Stochastic_Arrows/x4period_stochastic_arrows.mq5', 'folder': 'X4Period_Stochastic_Arrows', 'inputs': [{'mql': 'Kperiod1', 'py': 'Kperiod1', 'param': 'Kperiod1', 'type': 'uint', 'default': 5, 'label': 'Period %K 1', 'sinput': False}, {'mql': 'Kperiod2', 'py': 'Kperiod2', 'param': 'Kperiod2', 'type': 'uint', 'default': 7, 'label': 'Period %K 2', 'sinput': False}, {'mql': 'Kperiod3', 'py': 'Kperiod3', 'param': 'Kperiod3', 'type': 'uint', 'default': 11, 'label': 'Period %K 3', 'sinput': False}, {'mql': 'Kperiod4', 'py': 'Kperiod4', 'param': 'Kperiod4', 'type': 'uint', 'default': 17, 'label': 'Period %K 4', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'int', 'default': 3, 'label': 'Period %D', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'int', 'default': 3, 'label': 'Slowing', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': 'Method of averaging', 'sinput': False}, {'mql': 'Price_field', 'py': 'Price_field', 'param': 'Price_field', 'type': 'int', 'default': 0, 'label': 'Prices', 'sinput': False}, {'mql': 'rsiUpperTrigger', 'py': 'rsiUpperTrigger', 'param': 'rsiUpperTrigger', 'type': 'uint', 'default': 62, 'label': 'Overbought levels', 'sinput': False}, {'mql': 'rsiLowerTrigger', 'py': 'rsiLowerTrigger', 'param': 'rsiLowerTrigger', 'type': 'uint', 'default': 38, 'label': 'Oversold level', 'sinput': False}, {'mql': 'Size', 'py': 'Size', 'param': 'Size', 'type': 'uint', 'default': 2, 'label': 'Vertical distance between the icons', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Kperiod1 = _input('Kperiod1', 5)  # Period %K 1
Kperiod2 = _input('Kperiod2', 7)  # Period %K 2
Kperiod3 = _input('Kperiod3', 11)  # Period %K 3
Kperiod4 = _input('Kperiod4', 17)  # Period %K 4
DPeriod = _input('DPeriod', 3)  # Period %D
Slowing = _input('Slowing', 3)  # Slowing
MA_Method = _input('MA_Method', MODE_SMA)  # Method of averaging
Price_field = _input('Price_field', STO_LOWHIGH)  # Prices
rsiUpperTrigger = _input('rsiUpperTrigger', 62)  # Overbought levels
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
Stochastic_Handle = Arr(4, 0, dyn=False)
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = _int(MathMax(ATR_Period, Kperiod1))
    min_rates_total = _int(MathMax(min_rates_total, Kperiod2))
    min_rates_total = _int(MathMax(min_rates_total, Kperiod3))
    min_rates_total = _int(MathMax(min_rates_total, Kperiod4))
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
        return INIT_FAILED
    Stochastic_Handle[0] = iStochastic(None, 0, Kperiod1, DPeriod, Slowing, MA_Method, Price_field)
    if Stochastic_Handle[0] == INVALID_HANDLE:
        Print(' Failed to get the handle of the iStochastic 1 indicator')
        return INIT_FAILED
    Stochastic_Handle[1] = iStochastic(None, 0, Kperiod2, DPeriod, Slowing, MA_Method, Price_field)
    if Stochastic_Handle[1] == INVALID_HANDLE:
        Print(' Failed to get the handle of the iStochastic 2 indicator')
        return INIT_FAILED
    Stochastic_Handle[2] = iStochastic(None, 0, Kperiod3, DPeriod, Slowing, MA_Method, Price_field)
    if Stochastic_Handle[2] == INVALID_HANDLE:
        Print(' Failed to get the handle of the iStochastic 3 indicator')
        return INIT_FAILED
    Stochastic_Handle[3] = iStochastic(None, 0, Kperiod4, DPeriod, Slowing, MA_Method, Price_field)
    if Stochastic_Handle[3] == INVALID_HANDLE:
        Print(' Failed to get the handle of the iStochastic 4 indicator')
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
    short_name = 'X4Period_Stochastic_Arrows'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def InitTsIndArrBuffer(Number, Plot, IndBuffer, Empty_Value, Draw_Begin):
    SetIndexBuffer(Number, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(Plot, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Plot, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Plot, PLOT_ARROW, 159)
    ArraySetAsSeries(IndBuffer, True)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((((BarsCalculated(ATR_Handle) < rates_total or BarsCalculated(Stochastic_Handle[0]) < rates_total) or BarsCalculated(Stochastic_Handle[1]) < rates_total) or BarsCalculated(Stochastic_Handle[2]) < rates_total) or BarsCalculated(Stochastic_Handle[3]) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    Stochastic1 = Arr(0, 0.0)
    Stochastic2 = Arr(0, 0.0)
    Stochastic3 = Arr(0, 0.0)
    Stochastic4 = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Stochastic_Handle[0], 0, 0, to_copy, Stochastic1) <= 0:
        return 0
    if CopyBuffer(Stochastic_Handle[1], 0, 0, to_copy, Stochastic2) <= 0:
        return 0
    if CopyBuffer(Stochastic_Handle[2], 0, 0, to_copy, Stochastic3) <= 0:
        return 0
    if CopyBuffer(Stochastic_Handle[3], 0, 0, to_copy, Stochastic4) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(Stochastic1, True)
    ArraySetAsSeries(Stochastic2, True)
    ArraySetAsSeries(Stochastic3, True)
    ArraySetAsSeries(Stochastic4, True)
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
        if Stochastic1[bar] < rsiLowerTrigger:
            SellBuffer1[bar] = high[bar] + ((ATR[bar] * (Size + 1)) / 8)
        if Stochastic1[bar] > rsiUpperTrigger:
            BuyBuffer1[bar] = low[bar] - ((ATR[bar] * (Size + 1)) / 8)
        if Stochastic2[bar] < rsiLowerTrigger:
            SellBuffer2[bar] = high[bar] + ((ATR[bar] * ((2 * Size) + 1)) / 8)
        if Stochastic2[bar] > rsiUpperTrigger:
            BuyBuffer2[bar] = low[bar] - ((ATR[bar] * ((2 * Size) + 1)) / 8)
        if Stochastic3[bar] < rsiLowerTrigger:
            SellBuffer3[bar] = high[bar] + ((ATR[bar] * ((3 * Size) + 1)) / 8)
        if Stochastic3[bar] > rsiUpperTrigger:
            BuyBuffer3[bar] = low[bar] - ((ATR[bar] * ((3 * Size) + 1)) / 8)
        if Stochastic4[bar] < rsiLowerTrigger:
            SellBuffer4[bar] = high[bar] + ((ATR[bar] * ((4 * Size) + 1)) / 8)
        if Stochastic4[bar] > rsiUpperTrigger:
            BuyBuffer4[bar] = low[bar] - ((ATR[bar] * ((4 * Size) + 1)) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class X4periodStochasticArrows(_MQL5Indicator):
    name = 'x4period_stochastic_arrows'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Kperiod1': 5,  # Period %K 1
        'Kperiod2': 7,  # Period %K 2
        'Kperiod3': 11,  # Period %K 3
        'Kperiod4': 17,  # Period %K 4
        'DPeriod': 3,  # Period %D
        'Slowing': 3,  # Slowing
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method of averaging
        'Price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Prices
        'rsiUpperTrigger': 62,  # Overbought levels
        'rsiLowerTrigger': 38,  # Oversold level
        'Size': 2,  # Vertical distance between the icons
    }

