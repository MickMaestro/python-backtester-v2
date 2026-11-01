"""ATR Channels — converted from MQL5: MQL5 Indicators/ATR Channels Indicator/ATR Channels.mq5

ATR Channels
Copyright: Copyright 2025, matfx.; Link: https://theregulartrader.blogspot.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2025, matfx.', 'link': 'https://theregulartrader.blogspot.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 7}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'colors': {1: [14822282], 2: [14772545], 3: [16760576], 4: [16776960], 5: [16760576], 6: [14772545], 7: [14822282]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Upper Band3', 2: 'Upper Band2', 3: 'Upper Band1', 4: 'Middle Band', 5: 'Lower Band1', 6: 'Lower Band2', 7: 'Lower Band3'}, 'levels': [], 'description': ['ATR Channels'], 'name': 'ATR Channels', 'source': 'MQL5 Indicators/ATR Channels Indicator/ATR Channels.mq5', 'folder': 'ATR Channels Indicator', 'inputs': [{'mql': 'InpSMAPeriod', 'py': 'InpSMAPeriod', 'param': 'InpSMAPeriod', 'type': 'int', 'default': 49, 'label': 'Period of SMA', 'sinput': False}, {'mql': 'InpATRPeriod', 'py': 'InpATRPeriod', 'param': 'InpATRPeriod', 'type': 'int', 'default': 18, 'label': 'Period of ATR', 'sinput': False}, {'mql': 'InpATRFactor1', 'py': 'InpATRFactor1', 'param': 'InpATRFactor1', 'type': 'double', 'default': 1.6, 'label': 'ATR multiplier1', 'sinput': False}, {'mql': 'InpATRFactor2', 'py': 'InpATRFactor2', 'param': 'InpATRFactor2', 'type': 'double', 'default': 3.2, 'label': 'ATR multiplier2', 'sinput': False}, {'mql': 'InpATRFactor3', 'py': 'InpATRFactor3', 'param': 'InpATRFactor3', 'type': 'double', 'default': 4.8, 'label': 'ATR multiplier3', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpSMAPeriod = _input('InpSMAPeriod', 49)  # Period of SMA
InpATRPeriod = _input('InpATRPeriod', 18)  # Period of ATR
InpATRFactor1 = _input('InpATRFactor1', 1.6)  # ATR multiplier1
InpATRFactor2 = _input('InpATRFactor2', 3.2)  # ATR multiplier2
InpATRFactor3 = _input('InpATRFactor3', 4.8)  # ATR multiplier3
ExtSMAPeriod = 0
ExtATRPeriod = 0
ExtATRFactor1 = 0.0
ExtATRFactor2 = 0.0
ExtATRFactor3 = 0.0
ExtUpp3Buffer = Arr(0, 0.0)
ExtUpp2Buffer = Arr(0, 0.0)
ExtUpp1Buffer = Arr(0, 0.0)
ExtSMABuffer = Arr(0, 0.0)
ExtDwn1Buffer = Arr(0, 0.0)
ExtDwn2Buffer = Arr(0, 0.0)
ExtDwn3Buffer = Arr(0, 0.0)
ExtSMAHandle = 0
ExtATRHandle = 0
ExtPrefixUniq = ""
ExtPeriod = 0

def OnInit():
    global ExtATRFactor1, ExtATRFactor2, ExtATRFactor3, ExtATRHandle, ExtATRPeriod, ExtPeriod, ExtPrefixUniq, ExtSMAHandle, ExtSMAPeriod
    if InpSMAPeriod < 10:
        ExtSMAPeriod = 20
        PrintFormat('Incorrect value for input variable InpEMAPeriod=%d. Indicator will use value=%d for calculations.', InpSMAPeriod, ExtSMAPeriod)
    else:
        ExtSMAPeriod = InpSMAPeriod
    if InpATRPeriod < 3:
        ExtATRPeriod = 18
        PrintFormat('Incorrect value for input variable InpATRPeriod=%d. Indicator will use value=%d for calculations.', InpATRPeriod, ExtATRPeriod)
    else:
        ExtATRPeriod = InpATRPeriod
    if InpATRFactor1 < 1.0:
        ExtATRFactor1 = 1.6
        PrintFormat('Incorrect value for input variable InpBandsDeviations=%f. Indicator will use value=%f for calculations.', InpATRFactor1, ExtATRFactor1)
    else:
        ExtATRFactor1 = InpATRFactor1
    if InpATRFactor2 < 1.0:
        ExtATRFactor2 = 3.2
        PrintFormat('Incorrect value for input variable InpBandsDeviations=%f. Indicator will use value=%f for calculations.', InpATRFactor2, ExtATRFactor2)
    else:
        ExtATRFactor2 = InpATRFactor2
    if InpATRFactor3 < 1.0:
        ExtATRFactor3 = 4.8
        PrintFormat('Incorrect value for input variable InpBandsDeviations=%f. Indicator will use value=%f for calculations.', InpATRFactor3, ExtATRFactor3)
    else:
        ExtATRFactor3 = InpATRFactor3
    SetIndexBuffer(0, ExtUpp3Buffer)
    SetIndexBuffer(1, ExtUpp2Buffer)
    SetIndexBuffer(2, ExtUpp1Buffer)
    SetIndexBuffer(3, ExtSMABuffer)
    SetIndexBuffer(4, ExtDwn1Buffer)
    SetIndexBuffer(5, ExtDwn2Buffer)
    SetIndexBuffer(6, ExtDwn3Buffer)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpSMAPeriod + 1)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, InpSMAPeriod + 1)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, InpSMAPeriod + 1)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, InpSMAPeriod + 1)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, InpSMAPeriod + 1)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, InpSMAPeriod + 1)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, InpSMAPeriod + 1)
    PlotIndexSetInteger(0, PLOT_SHIFT, 1)
    PlotIndexSetInteger(1, PLOT_SHIFT, 1)
    PlotIndexSetInteger(2, PLOT_SHIFT, 1)
    PlotIndexSetInteger(3, PLOT_SHIFT, 1)
    PlotIndexSetInteger(4, PLOT_SHIFT, 1)
    PlotIndexSetInteger(5, PLOT_SHIFT, 1)
    PlotIndexSetInteger(6, PLOT_SHIFT, 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ATR Channels')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ExtSMAHandle = iMA(None, 0, InpSMAPeriod, 0, MODE_LWMA, PRICE_CLOSE)
    ExtATRHandle = iATR(None, 0, InpATRPeriod)
    ExtPeriod = PeriodSeconds(Period())
    number = StringFormat('%I64d', GetTickCount64())
    ExtPrefixUniq = StringSubstr(number, StringLen(number) - 4)
    ExtPrefixUniq = ExtPrefixUniq + '_KLT'
    Print('Indicator "ATR Channels" started, prefix=', ExtPrefixUniq)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if prev_calculated == 0:
        ArrayFill(ExtUpp1Buffer, 0, rates_total, 0)
        ArrayFill(ExtUpp2Buffer, 0, rates_total, 0)
        ArrayFill(ExtUpp3Buffer, 0, rates_total, 0)
        ArrayFill(ExtSMABuffer, 0, rates_total, 0)
        ArrayFill(ExtDwn1Buffer, 0, rates_total, 0)
        ArrayFill(ExtDwn2Buffer, 0, rates_total, 0)
        ArrayFill(ExtDwn3Buffer, 0, rates_total, 0)
        if CopyBuffer(ExtSMAHandle, 0, 0, rates_total, ExtSMABuffer) < 0:
            return 0
        atr = Arr(0, 0.0)
        if CopyBuffer(ExtATRHandle, 0, 0, rates_total, atr) < 0:
            return 0
        start = MathMax(InpSMAPeriod, InpATRPeriod) + 1
        for i in range(start, rates_total):
            ExtUpp3Buffer[i] = ExtSMABuffer[i] + (InpATRFactor3 * atr[i])
            ExtUpp2Buffer[i] = ExtSMABuffer[i] + (InpATRFactor2 * atr[i])
            ExtUpp1Buffer[i] = ExtSMABuffer[i] + (InpATRFactor1 * atr[i])
            ExtDwn1Buffer[i] = ExtSMABuffer[i] - (InpATRFactor1 * atr[i])
            ExtDwn2Buffer[i] = ExtSMABuffer[i] - (InpATRFactor2 * atr[i])
            ExtDwn3Buffer[i] = ExtSMABuffer[i] - (InpATRFactor3 * atr[i])
        return rates_total
    start = prev_calculated - 2
    for i in range(start, rates_total):
        reverse_index = rates_total - i
        sma = Arr(0, 0.0)
        if CopyBuffer(ExtSMAHandle, 0, reverse_index, 1, sma) < 0:
            return prev_calculated
        atr = Arr(0, 0.0)
        if CopyBuffer(ExtATRHandle, 0, reverse_index, 1, atr) < 0:
            return prev_calculated
        ExtSMABuffer[i] = sma[0]
        ExtUpp1Buffer[i] = sma[0] + (InpATRFactor1 * atr[0])
        ExtUpp2Buffer[i] = sma[0] + (InpATRFactor2 * atr[0])
        ExtUpp3Buffer[i] = sma[0] + (InpATRFactor3 * atr[0])
        ExtDwn1Buffer[i] = sma[0] - (InpATRFactor1 * atr[0])
        ExtDwn2Buffer[i] = sma[0] - (InpATRFactor2 * atr[0])
        ExtDwn3Buffer[i] = sma[0] - (InpATRFactor3 * atr[0])
    return rates_total

def OnDeinit(reason):
    Print('Indicator "ATR Channels" stopped, delete all objects with prefix=', ExtPrefixUniq)
    ObjectsDeleteAll(0, ExtPrefixUniq, 0, OBJ_ARROW_RIGHT_PRICE)
    ChartRedraw(0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ATRChannels(_MQL5Indicator):
    name = 'ATR Channels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpSMAPeriod': 49,  # Period of SMA
        'InpATRPeriod': 18,  # Period of ATR
        'InpATRFactor1': 1.6,  # ATR multiplier1
        'InpATRFactor2': 3.2,  # ATR multiplier2
        'InpATRFactor3': 4.8,  # ATR multiplier3
    }

