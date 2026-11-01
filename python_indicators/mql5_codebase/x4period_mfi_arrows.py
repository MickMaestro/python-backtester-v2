"""x4period_mfi_arrows — converted from MQL5: MQL5 Indicators/X4Period_MFI_Arrows/x4period_mfi_arrows.mq5

Copyright: Copyright © 2005, transport_david; Link: http://finance.groups.yahoo.com/group/MetaTrader_Experts_and_Indicators/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, transport_david', 'link': 'http://finance.groups.yahoo.com/group/MetaTrader_Experts_and_Indicators/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 'colors': {1: [7504122], 2: [11186720], 3: [7504122], 4: [11186720], 5: [7504122], 6: [11186720], 7: [7504122], 8: [11186720]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2}, 'styles': {}, 'labels': {1: 'X4Period_MFI_Arrows Sell 1', 2: 'X4Period_MFI_Arrows Buy 1', 3: 'X4Period_MFI_Arrows Sell 2', 4: 'X4Period_MFI_Arrows Buy 2', 5: 'X4Period_MFI_Arrows Sell 3', 6: 'X4Period_MFI_Arrows Buy 3', 7: 'X4Period_MFI_Arrows Sell 4', 8: 'X4Period_MFI_Arrows Buy 4'}, 'levels': [], 'description': [], 'name': 'x4period_mfi_arrows', 'source': 'MQL5 Indicators/X4Period_MFI_Arrows/x4period_mfi_arrows.mq5', 'folder': 'X4Period_MFI_Arrows', 'inputs': [{'mql': 'MFIperiod1', 'py': 'MFIperiod1', 'param': 'MFIperiod1', 'type': 'uint', 'default': 7, 'label': 'Period 1', 'sinput': False}, {'mql': 'MFIperiod2', 'py': 'MFIperiod2', 'param': 'MFIperiod2', 'type': 'uint', 'default': 12, 'label': 'Period 2', 'sinput': False}, {'mql': 'MFIperiod3', 'py': 'MFIperiod3', 'param': 'MFIperiod3', 'type': 'uint', 'default': 18, 'label': 'Period 3', 'sinput': False}, {'mql': 'MFIperiod4', 'py': 'MFIperiod4', 'param': 'MFIperiod4', 'type': 'uint', 'default': 32, 'label': 'Period 4', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'Volume', 'sinput': False}, {'mql': 'rsiUpperTrigger', 'py': 'rsiUpperTrigger', 'param': 'rsiUpperTrigger', 'type': 'uint', 'default': 62, 'label': 'Overbought level', 'sinput': False}, {'mql': 'rsiLowerTrigger', 'py': 'rsiLowerTrigger', 'param': 'rsiLowerTrigger', 'type': 'uint', 'default': 38, 'label': 'Oversold level', 'sinput': False}, {'mql': 'Size', 'py': 'Size', 'param': 'Size', 'type': 'uint', 'default': 2, 'label': 'Vertical distance between the icons', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MFIperiod1 = _input('MFIperiod1', 7)  # Period 1
MFIperiod2 = _input('MFIperiod2', 12)  # Period 2
MFIperiod3 = _input('MFIperiod3', 18)  # Period 3
MFIperiod4 = _input('MFIperiod4', 32)  # Period 4
VolumeType = _input('VolumeType', VOLUME_TICK)  # Volume
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
MFI_Handle = Arr(4, 0, dyn=False)
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = _int(MathMax(ATR_Period, MFIperiod1))
    min_rates_total = _int(MathMax(min_rates_total, MFIperiod2))
    min_rates_total = _int(MathMax(min_rates_total, MFIperiod3))
    min_rates_total = _int(MathMax(min_rates_total, MFIperiod4))
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
        return INIT_FAILED
    MFI_Handle[0] = iMFI(None, 0, MFIperiod1, VolumeType)
    if MFI_Handle[0] == INVALID_HANDLE:
        Print(' Failed to get handle of the iMFI 1 indicator')
        return INIT_FAILED
    MFI_Handle[1] = iMFI(None, 0, MFIperiod2, VolumeType)
    if MFI_Handle[1] == INVALID_HANDLE:
        Print(' Failed to get handle of the iMFI 2 indicator')
        return INIT_FAILED
    MFI_Handle[2] = iMFI(None, 0, MFIperiod3, VolumeType)
    if MFI_Handle[2] == INVALID_HANDLE:
        Print(' Failed to get handle of the iMFI 3 indicator')
        return INIT_FAILED
    MFI_Handle[3] = iMFI(None, 0, MFIperiod4, VolumeType)
    if MFI_Handle[3] == INVALID_HANDLE:
        Print(' Failed to get handle of the iMFI 4 indicator')
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
    short_name = 'X4Period_MFI_Arrows'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def InitTsIndArrBuffer(Number, Plot, IndBuffer, Empty_Value, Draw_Begin):
    SetIndexBuffer(Number, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(Plot, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Plot, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Plot, PLOT_ARROW, 159)
    ArraySetAsSeries(IndBuffer, True)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((((BarsCalculated(ATR_Handle) < rates_total or BarsCalculated(MFI_Handle[0]) < rates_total) or BarsCalculated(MFI_Handle[1]) < rates_total) or BarsCalculated(MFI_Handle[2]) < rates_total) or BarsCalculated(MFI_Handle[3]) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    MFI1 = Arr(0, 0.0)
    MFI2 = Arr(0, 0.0)
    MFI3 = Arr(0, 0.0)
    MFI4 = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(MFI_Handle[0], 0, 0, to_copy, MFI1) <= 0:
        return 0
    if CopyBuffer(MFI_Handle[1], 0, 0, to_copy, MFI2) <= 0:
        return 0
    if CopyBuffer(MFI_Handle[2], 0, 0, to_copy, MFI3) <= 0:
        return 0
    if CopyBuffer(MFI_Handle[3], 0, 0, to_copy, MFI4) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(MFI1, True)
    ArraySetAsSeries(MFI2, True)
    ArraySetAsSeries(MFI3, True)
    ArraySetAsSeries(MFI4, True)
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
        if MFI1[bar] < rsiLowerTrigger:
            SellBuffer1[bar] = high[bar] + ((ATR[bar] * (Size + 1)) / 8)
        if MFI1[bar] > rsiUpperTrigger:
            BuyBuffer1[bar] = low[bar] - ((ATR[bar] * (Size + 1)) / 8)
        if MFI2[bar] < rsiLowerTrigger:
            SellBuffer2[bar] = high[bar] + ((ATR[bar] * ((2 * Size) + 1)) / 8)
        if MFI2[bar] > rsiUpperTrigger:
            BuyBuffer2[bar] = low[bar] - ((ATR[bar] * ((2 * Size) + 1)) / 8)
        if MFI3[bar] < rsiLowerTrigger:
            SellBuffer3[bar] = high[bar] + ((ATR[bar] * ((3 * Size) + 1)) / 8)
        if MFI3[bar] > rsiUpperTrigger:
            BuyBuffer3[bar] = low[bar] - ((ATR[bar] * ((3 * Size) + 1)) / 8)
        if MFI4[bar] < rsiLowerTrigger:
            SellBuffer4[bar] = high[bar] + ((ATR[bar] * ((4 * Size) + 1)) / 8)
        if MFI4[bar] > rsiUpperTrigger:
            BuyBuffer4[bar] = low[bar] - ((ATR[bar] * ((4 * Size) + 1)) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class X4periodMfiArrows(_MQL5Indicator):
    name = 'x4period_mfi_arrows'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MFIperiod1': 7,  # Period 1
        'MFIperiod2': 12,  # Period 2
        'MFIperiod3': 18,  # Period 3
        'MFIperiod4': 32,  # Period 4
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volume
        'rsiUpperTrigger': 62,  # Overbought level
        'rsiLowerTrigger': 38,  # Oversold level
        'Size': 2,  # Vertical distance between the icons
    }

