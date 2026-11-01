"""Tymen_STARCBands_MTF — converted from MQL5: MQL5 Indicators/Tymen_STARC_Bands_MTF/Tymen_STARCBands_MTF.mq5

Multi timeframe Tymen STARC Bands indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 36, 'indicator_plots': 15}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}, 'colors': {1: [32768], 2: [32768], 3: [32768], 4: [32768], 5: [32768], 6: [16711680], 7: [16711680], 8: [16711680], 9: [16711680], 10: [16711680], 11: [255], 12: [255], 13: [255], 14: [255], 15: [255]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}, 'labels': {1: 'Highest', 2: 'Top', 3: 'Middle', 4: 'Bottom', 5: 'Lowest', 6: 'Highest', 7: 'Top', 8: 'Middle', 9: 'Bottom', 10: 'Lowest', 11: 'Highest', 12: 'Top', 13: 'Middle', 14: 'Bottom', 15: 'Lowest'}, 'levels': [], 'description': ['Multi timeframe Tymen STARC Bands indicator'], 'name': 'Tymen_STARCBands_MTF', 'source': 'MQL5 Indicators/Tymen_STARC_Bands_MTF/Tymen_STARCBands_MTF.mq5', 'folder': 'Tymen_STARC_Bands_MTF', 'inputs': [{'mql': 'InpDrawMode', 'py': 'InpDrawMode', 'param': 'InpDrawMode', 'type': 'int', 'default': 0, 'label': 'Drawing mode', 'sinput': False}, {'mql': 'InpShowMiddle', 'py': 'InpShowMiddle', 'param': 'InpShowMiddle', 'type': 'int', 'default': 1, 'label': 'Show middle lines', 'sinput': False}, {'mql': 'InpShowBands1', 'py': 'InpShowBands1', 'param': 'InpShowBands1', 'type': 'int', 'default': 1, 'label': 'Show first Tymen STARC Bands', 'sinput': False}, {'mql': 'InpTimeframe1', 'py': 'InpTimeframe1', 'param': 'InpTimeframe1', 'type': 'int', 'default': 16385, 'label': 'First bands timeframe', 'sinput': False}, {'mql': 'InpPeriodATR1', 'py': 'InpPeriodATR1', 'param': 'InpPeriodATR1', 'type': 'uint', 'default': 15, 'label': 'First bands ATR period', 'sinput': False}, {'mql': 'InpPeriodMA1', 'py': 'InpPeriodMA1', 'param': 'InpPeriodMA1', 'type': 'uint', 'default': 6, 'label': 'First bands MA period', 'sinput': False}, {'mql': 'InpMethod1', 'py': 'InpMethod1', 'param': 'InpMethod1', 'type': 'int', 'default': 1, 'label': 'First bands Method', 'sinput': False}, {'mql': 'InpAppliedPrice1', 'py': 'InpAppliedPrice1', 'param': 'InpAppliedPrice1', 'type': 'int', 'default': 1, 'label': 'First bands Applied price', 'sinput': False}, {'mql': 'InpKATR1', 'py': 'InpKATR1', 'param': 'InpKATR1', 'type': 'double', 'default': 1.0, 'label': 'First bands ATR coefficient', 'sinput': False}, {'mql': 'InpMKATR1', 'py': 'InpMKATR1', 'param': 'InpMKATR1', 'type': 'double', 'default': 0.7, 'label': 'First bands ATR middle coefficient', 'sinput': False}, {'mql': 'InpShowBands2', 'py': 'InpShowBands2', 'param': 'InpShowBands2', 'type': 'int', 'default': 1, 'label': 'Show second Tymen STARC Bands', 'sinput': False}, {'mql': 'InpTimeframe2', 'py': 'InpTimeframe2', 'param': 'InpTimeframe2', 'type': 'int', 'default': 16388, 'label': 'Second bands timeframe', 'sinput': False}, {'mql': 'InpPeriodATR2', 'py': 'InpPeriodATR2', 'param': 'InpPeriodATR2', 'type': 'uint', 'default': 15, 'label': 'Second bands ATR period', 'sinput': False}, {'mql': 'InpPeriodMA2', 'py': 'InpPeriodMA2', 'param': 'InpPeriodMA2', 'type': 'uint', 'default': 6, 'label': 'Second bands MA period', 'sinput': False}, {'mql': 'InpMethod2', 'py': 'InpMethod2', 'param': 'InpMethod2', 'type': 'int', 'default': 1, 'label': 'Second bands Method', 'sinput': False}, {'mql': 'InpAppliedPrice2', 'py': 'InpAppliedPrice2', 'param': 'InpAppliedPrice2', 'type': 'int', 'default': 1, 'label': 'Second bands Applied price', 'sinput': False}, {'mql': 'InpKATR2', 'py': 'InpKATR2', 'param': 'InpKATR2', 'type': 'double', 'default': 1.0, 'label': 'Second bands ATR coefficient', 'sinput': False}, {'mql': 'InpMKATR2', 'py': 'InpMKATR2', 'param': 'InpMKATR2', 'type': 'double', 'default': 0.7, 'label': 'Second bands ATR middle coefficient', 'sinput': False}, {'mql': 'InpShowBands3', 'py': 'InpShowBands3', 'param': 'InpShowBands3', 'type': 'int', 'default': 1, 'label': 'Show third Tymen STARC Bands', 'sinput': False}, {'mql': 'InpTimeframe3', 'py': 'InpTimeframe3', 'param': 'InpTimeframe3', 'type': 'int', 'default': 16408, 'label': 'Third bands timeframe', 'sinput': False}, {'mql': 'InpPeriodATR3', 'py': 'InpPeriodATR3', 'param': 'InpPeriodATR3', 'type': 'uint', 'default': 15, 'label': 'Third bands ATR period', 'sinput': False}, {'mql': 'InpPeriodMA3', 'py': 'InpPeriodMA3', 'param': 'InpPeriodMA3', 'type': 'uint', 'default': 6, 'label': 'Third bands MA period', 'sinput': False}, {'mql': 'InpMethod3', 'py': 'InpMethod3', 'param': 'InpMethod3', 'type': 'int', 'default': 1, 'label': 'Third bands Method', 'sinput': False}, {'mql': 'InpAppliedPrice3', 'py': 'InpAppliedPrice3', 'param': 'InpAppliedPrice3', 'type': 'int', 'default': 1, 'label': 'Third bands Applied price', 'sinput': False}, {'mql': 'InpKATR3', 'py': 'InpKATR3', 'param': 'InpKATR3', 'type': 'double', 'default': 1.0, 'label': 'Third bands ATR coefficient', 'sinput': False}, {'mql': 'InpMKATR3', 'py': 'InpMKATR3', 'param': 'InpMKATR3', 'type': 'double', 'default': 0.7, 'label': 'Third bands ATR middle coefficient', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_MA_MODE
METHOD_SMA = 0
METHOD_EMA = 1
METHOD_SMMA = 2
METHOD_LWMA = 3
METHOD_WILDER_EMA = 4
METHOD_SINE_WMA = 5
METHOD_TRI_MA = 6
METHOD_LSMA = 7
METHOD_HMA = 8
METHOD_ZL_EMA = 9
METHOD_ITREND_MA = 10
METHOD_MOVING_MEDIAN = 11
METHOD_GEO_MEAN = 12
METHOD_REMA = 13
METHOD_ILRS = 14
METHOD_IE_2 = 15
METHOD_TRI_MA_GEN = 16
METHOD_VWMA = 17
_enum('ENUM_MA_MODE', {0: 'METHOD_SMA', 1: 'METHOD_EMA', 2: 'METHOD_SMMA', 3: 'METHOD_LWMA', 4: 'METHOD_WILDER_EMA', 5: 'METHOD_SINE_WMA', 6: 'METHOD_TRI_MA', 7: 'METHOD_LSMA', 8: 'METHOD_HMA', 9: 'METHOD_ZL_EMA', 10: 'METHOD_ITREND_MA', 11: 'METHOD_MOVING_MEDIAN', 12: 'METHOD_GEO_MEAN', 13: 'METHOD_REMA', 14: 'METHOD_ILRS', 15: 'METHOD_IE_2', 16: 'METHOD_TRI_MA_GEN', 17: 'METHOD_VWMA'})

# enum ENUM_DRAW_MODE
DRAW_MODE_STEPS = 0
DRAW_MODE_SLOPE = 1
_enum('ENUM_DRAW_MODE', {0: 'DRAW_MODE_STEPS', 1: 'DRAW_MODE_SLOPE'})

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpDrawMode = _input('InpDrawMode', DRAW_MODE_STEPS)  # Drawing mode
InpShowMiddle = _input('InpShowMiddle', INPUT_YES)  # Show middle lines
InpShowBands1 = _input('InpShowBands1', INPUT_YES)  # Show first Tymen STARC Bands
InpTimeframe1 = _input('InpTimeframe1', PERIOD_H1)  # First bands timeframe
InpPeriodATR1 = _input('InpPeriodATR1', 15)  # First bands ATR period
InpPeriodMA1 = _input('InpPeriodMA1', 6)  # First bands MA period
InpMethod1 = _input('InpMethod1', METHOD_EMA)  # First bands Method
InpAppliedPrice1 = _input('InpAppliedPrice1', PRICE_CLOSE)  # First bands Applied price
InpKATR1 = _input('InpKATR1', 1.0)  # First bands ATR coefficient
InpMKATR1 = _input('InpMKATR1', 0.7)  # First bands ATR middle coefficient
InpShowBands2 = _input('InpShowBands2', INPUT_YES)  # Show second Tymen STARC Bands
InpTimeframe2 = _input('InpTimeframe2', PERIOD_H4)  # Second bands timeframe
InpPeriodATR2 = _input('InpPeriodATR2', 15)  # Second bands ATR period
InpPeriodMA2 = _input('InpPeriodMA2', 6)  # Second bands MA period
InpMethod2 = _input('InpMethod2', METHOD_EMA)  # Second bands Method
InpAppliedPrice2 = _input('InpAppliedPrice2', PRICE_CLOSE)  # Second bands Applied price
InpKATR2 = _input('InpKATR2', 1.0)  # Second bands ATR coefficient
InpMKATR2 = _input('InpMKATR2', 0.7)  # Second bands ATR middle coefficient
InpShowBands3 = _input('InpShowBands3', INPUT_YES)  # Show third Tymen STARC Bands
InpTimeframe3 = _input('InpTimeframe3', PERIOD_D1)  # Third bands timeframe
InpPeriodATR3 = _input('InpPeriodATR3', 15)  # Third bands ATR period
InpPeriodMA3 = _input('InpPeriodMA3', 6)  # Third bands MA period
InpMethod3 = _input('InpMethod3', METHOD_EMA)  # Third bands Method
InpAppliedPrice3 = _input('InpAppliedPrice3', PRICE_CLOSE)  # Third bands Applied price
InpKATR3 = _input('InpKATR3', 1.0)  # Third bands ATR coefficient
InpMKATR3 = _input('InpMKATR3', 0.7)  # Third bands ATR middle coefficient
period_max = 0

class SDataBand(MqlObject):
    _q_fields = ('BufferTopExtr', 'BufferTop', 'BufferMiddle', 'BufferBottom', 'BufferBottomExtr', 'BufferATR', 'BufferPrice', 'BufferTopExtrTMP', 'BufferTopTMP', 'BufferMiddleTMP', 'BufferBottomTMP', 'BufferBottomExtrTMP', 'timeframe', 'applied_price', 'method', 'katr', 'mkatr', 'label', 'show', 'period_ma', 'period_atr', 'handle_ma', 'handle_atr')
    def __init__(self, *args):
        self.BufferTopExtr = Arr(0, 0.0)
        self.BufferTop = Arr(0, 0.0)
        self.BufferMiddle = Arr(0, 0.0)
        self.BufferBottom = Arr(0, 0.0)
        self.BufferBottomExtr = Arr(0, 0.0)
        self.BufferATR = Arr(0, 0.0)
        self.BufferPrice = Arr(0, 0.0)
        self.BufferTopExtrTMP = Arr(0, 0.0)
        self.BufferTopTMP = Arr(0, 0.0)
        self.BufferMiddleTMP = Arr(0, 0.0)
        self.BufferBottomTMP = Arr(0, 0.0)
        self.BufferBottomExtrTMP = Arr(0, 0.0)
        self.timeframe = 0
        self.applied_price = 0
        self.method = 0
        self.katr = 0.0
        self.mkatr = 0.0
        self.label = ""
        self.show = False
        self.period_ma = 0
        self.period_atr = 0
        self.handle_ma = 0
        self.handle_atr = 0

def OnInit():
    global period_max
    EventSetTimer(90)
    DataBuff[0].period_ma = (2 if (InpPeriodMA1 < 2) else InpPeriodMA1)
    DataBuff[0].period_atr = (1 if (InpPeriodATR1 < 1) else InpPeriodATR1)
    DataBuff[0].timeframe = (InpTimeframe1 if (InpTimeframe1 > Period()) else Period())
    DataBuff[0].applied_price = InpAppliedPrice1
    DataBuff[0].katr = InpKATR1
    DataBuff[0].mkatr = InpMKATR1
    DataBuff[0].label = TimeframeToString(InpTimeframe1) + ' '
    DataBuff[0].show = (InpShowBands1 != 0)
    DataBuff[0].method = InpMethod1
    DataBuff[1].period_ma = (2 if (InpPeriodMA2 < 2) else InpPeriodMA2)
    DataBuff[1].period_atr = (1 if (InpPeriodATR2 < 1) else InpPeriodATR2)
    DataBuff[1].timeframe = (InpTimeframe2 if (InpTimeframe2 > Period()) else Period())
    DataBuff[1].applied_price = InpAppliedPrice2
    DataBuff[1].katr = InpKATR2
    DataBuff[1].mkatr = InpMKATR2
    DataBuff[1].label = TimeframeToString(InpTimeframe2) + ' '
    DataBuff[1].show = (InpShowBands2 != 0)
    DataBuff[1].method = InpMethod2
    DataBuff[2].period_ma = (2 if (InpPeriodMA3 < 2) else InpPeriodMA3)
    DataBuff[2].period_atr = (1 if (InpPeriodATR3 < 1) else InpPeriodATR3)
    DataBuff[2].timeframe = (InpTimeframe3 if (InpTimeframe3 > Period()) else Period())
    DataBuff[2].applied_price = InpAppliedPrice3
    DataBuff[2].katr = InpKATR3
    DataBuff[2].mkatr = InpMKATR3
    DataBuff[2].label = TimeframeToString(InpTimeframe3) + ' '
    DataBuff[2].show = (InpShowBands3 != 0)
    DataBuff[2].method = InpMethod3
    period_max = fmax(DataBuff[0].period_ma, fmax(DataBuff[1].period_ma, DataBuff[2].period_ma))
    n = -1
    for i in range(0, 3):
        n += 1
        SetIndexBuffer(n * 5, DataBuff[i].BufferTopExtr)
        PlotIndexSetString(n * 5, PLOT_LABEL, DataBuff[i].label + 'Top Extr')
        PlotIndexSetInteger(n * 5, PLOT_DRAW_TYPE, DataBuff[i].show)
        SetIndexBuffer((n * 5) + 1, DataBuff[i].BufferTop)
        PlotIndexSetString((n * 5) + 1, PLOT_LABEL, DataBuff[i].label + 'Top')
        PlotIndexSetInteger((n * 5) + 1, PLOT_DRAW_TYPE, DataBuff[i].show)
        SetIndexBuffer((n * 5) + 2, DataBuff[i].BufferMiddle)
        PlotIndexSetString((n * 5) + 2, PLOT_LABEL, DataBuff[i].label + 'Middle')
        PlotIndexSetInteger((n * 5) + 2, PLOT_DRAW_TYPE, (InpShowMiddle if DataBuff[i].show else 0))
        SetIndexBuffer((n * 5) + 3, DataBuff[i].BufferBottom)
        PlotIndexSetString((n * 5) + 3, PLOT_LABEL, DataBuff[i].label + 'Bottom')
        PlotIndexSetInteger((n * 5) + 3, PLOT_DRAW_TYPE, DataBuff[i].show)
        SetIndexBuffer((n * 5) + 4, DataBuff[i].BufferBottomExtr)
        PlotIndexSetString((n * 5) + 4, PLOT_LABEL, DataBuff[i].label + 'Bottom Extr')
        PlotIndexSetInteger((n * 5) + 4, PLOT_DRAW_TYPE, DataBuff[i].show)
        SetIndexBuffer((n * 7) + 15, DataBuff[i].BufferPrice)
        SetIndexBuffer((n * 7) + 16, DataBuff[i].BufferATR)
        SetIndexBuffer((n * 7) + 17, DataBuff[i].BufferTopExtrTMP)
        SetIndexBuffer((n * 7) + 18, DataBuff[i].BufferTopTMP)
        SetIndexBuffer((n * 7) + 19, DataBuff[i].BufferMiddleTMP)
        SetIndexBuffer((n * 7) + 20, DataBuff[i].BufferBottomTMP)
        SetIndexBuffer((n * 7) + 21, DataBuff[i].BufferBottomExtrTMP)
        ArraySetAsSeries(DataBuff[i].BufferTopExtr, True)
        ArraySetAsSeries(DataBuff[i].BufferTop, True)
        ArraySetAsSeries(DataBuff[i].BufferMiddle, True)
        ArraySetAsSeries(DataBuff[i].BufferBottom, True)
        ArraySetAsSeries(DataBuff[i].BufferBottomExtr, True)
        ArraySetAsSeries(DataBuff[i].BufferPrice, True)
        ArraySetAsSeries(DataBuff[i].BufferATR, True)
        ArraySetAsSeries(DataBuff[i].BufferTopExtrTMP, True)
        ArraySetAsSeries(DataBuff[i].BufferTopTMP, True)
        ArraySetAsSeries(DataBuff[i].BufferMiddleTMP, True)
        ArraySetAsSeries(DataBuff[i].BufferBottomTMP, True)
        ArraySetAsSeries(DataBuff[i].BufferBottomExtrTMP, True)
        ResetLastError()
        DataBuff[i].handle_ma = iMA(None, DataBuff[i].timeframe, 1, 0, MODE_SMA, DataBuff[i].applied_price)
        if DataBuff[i].handle_ma == INVALID_HANDLE:
            Print(288, ': The iMA(1) object was not created: Error ', GetLastError())
            return INIT_FAILED
        DataBuff[i].handle_atr = iATR(None, DataBuff[i].timeframe, DataBuff[i].period_atr)
        if DataBuff[i].handle_atr == INVALID_HANDLE:
            Print(294, ': The iATR(', _str(DataBuff[i].period_atr), ') object was not created: Error ', GetLastError())
            return INIT_FAILED
    label = TimeframeToString(InpTimeframe1) + ',' + TimeframeToString(InpTimeframe2) + ',' + TimeframeToString(InpTimeframe3) + ' Tymen STARC Bands'
    IndicatorSetString(INDICATOR_SHORTNAME, label)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    for i in range(0, 3):
        Time("", DataBuff[i].timeframe, 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(tick_volume, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 3
        for i in range(0, 3):
            ArrayInitialize(DataBuff[i].BufferTopExtr, EMPTY_VALUE)
            ArrayInitialize(DataBuff[i].BufferTop, EMPTY_VALUE)
            ArrayInitialize(DataBuff[i].BufferMiddle, 0)
            ArrayInitialize(DataBuff[i].BufferBottom, EMPTY_VALUE)
            ArrayInitialize(DataBuff[i].BufferBottomExtr, EMPTY_VALUE)
            ArrayInitialize(DataBuff[i].BufferPrice, 0)
            ArrayInitialize(DataBuff[i].BufferATR, 0)
            ArrayInitialize(DataBuff[i].BufferTopExtrTMP, 0)
            ArrayInitialize(DataBuff[i].BufferTopTMP, 0)
            ArrayInitialize(DataBuff[i].BufferMiddleTMP, 0)
            ArrayInitialize(DataBuff[i].BufferBottomTMP, 0)
            ArrayInitialize(DataBuff[i].BufferBottomExtrTMP, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    for i in range(0, 3):
        if Time("", DataBuff[i].timeframe, 1) == 0:
            return 0
        copied = CopyBuffer(DataBuff[i].handle_atr, 0, 0, count, DataBuff[i].BufferATR)
        if copied < 1:
            return 0
        copied = CopyBuffer(DataBuff[i].handle_ma, 0, 0, count, DataBuff[i].BufferPrice)
        if copied < 1:
            return 0
    for i in range(limit, 0 - 1, -1):
        for j in range(0, 3):
            GetMA(rates_total, DataBuff[j].method, DataBuff[j].period_ma, i, DataBuff[j].BufferPrice, DataBuff[j].BufferMiddleTMP, tick_volume)
            DataBuff[j].BufferTopExtrTMP[i] = DataBuff[j].BufferMiddleTMP[i] + (DataBuff[j].BufferATR[i] * DataBuff[j].katr)
            DataBuff[j].BufferTopTMP[i] = DataBuff[j].BufferMiddleTMP[i] + (DataBuff[j].BufferATR[i] * DataBuff[j].mkatr)
            DataBuff[j].BufferBottomTMP[i] = DataBuff[j].BufferMiddleTMP[i] - (DataBuff[j].BufferATR[i] * DataBuff[j].mkatr)
            DataBuff[j].BufferBottomExtrTMP[i] = DataBuff[j].BufferMiddleTMP[i] - (DataBuff[j].BufferATR[i] * DataBuff[j].katr)
    for i in range(limit, 0 - 1, -1):
        for j in range(0, 3):
            DataConversion(rates_total, "", DataBuff[j].timeframe, i, DataBuff[j].BufferMiddleTMP, DataBuff[j].BufferMiddle, InpDrawMode)
            DataConversion(rates_total, "", DataBuff[j].timeframe, i, DataBuff[j].BufferTopExtrTMP, DataBuff[j].BufferTopExtr, InpDrawMode)
            DataConversion(rates_total, "", DataBuff[j].timeframe, i, DataBuff[j].BufferTopTMP, DataBuff[j].BufferTop, InpDrawMode)
            DataConversion(rates_total, "", DataBuff[j].timeframe, i, DataBuff[j].BufferBottomTMP, DataBuff[j].BufferBottom, InpDrawMode)
            DataConversion(rates_total, "", DataBuff[j].timeframe, i, DataBuff[j].BufferBottomExtrTMP, DataBuff[j].BufferBottomExtr, InpDrawMode)
    return rates_total

def OnTimer():
    for i in range(0, 3):
        Time("", DataBuff[i].timeframe, 1)

def DataConversion(rates_total, symbol_name, timeframe_src, shift, buffer_src, buffer_dest, mode=DRAW_MODE_STEPS):
    if timeframe_src == Period():
        buffer_dest[shift] = buffer_src[shift]
        return
    bar_curr = BarToCurrent(symbol_name, timeframe_src, shift)
    if bar_curr > (rates_total - 1):
        return
    bar_prev = BarToCurrent(symbol_name, timeframe_src, shift + 1)
    bar_next = (BarToCurrent(symbol_name, timeframe_src, shift - 1) if (shift > 0) else 0)
    if (bar_prev == WRONG_VALUE or bar_curr == WRONG_VALUE) or bar_next == WRONG_VALUE:
        return
    buffer_dest[bar_curr] = buffer_src[shift]
    if mode == DRAW_MODE_STEPS:
        for j in range(bar_curr, bar_next - 1, -1):
            buffer_dest[j] = buffer_dest[bar_curr]
    else:
        if bar_prev > (rates_total - 1):
            return
        for j in range(bar_prev, bar_curr - 1, -1):
            buffer_dest[j] = EquationDirect(bar_prev, buffer_dest[bar_prev], bar_curr, buffer_dest[bar_curr], j)
        if shift == 0:
            for j in range(bar_curr, 0 - 1, -1):
                buffer_dest[j] = buffer_dest[bar_curr]

def BarToCurrent(symbol_name, timeframe_src, shift, exact=False):
    time = Time(symbol_name, timeframe_src, shift)
    return (BarShift(symbol_name, Period(), time, exact) if (time != 0) else WRONG_VALUE)

def BarShift(symbol_name, timeframe, time, exact=False):
    res = Bars(symbol_name, timeframe, time + 1, UINT_MAX)
    if exact:
        if (timeframe != PERIOD_MN1 or time > TimeCurrent()) and res == Bars(symbol_name, timeframe, time - PeriodSeconds(timeframe) + 1, UINT_MAX):
            return WRONG_VALUE
    return res

def Time(symbol_name, timeframe, shift):
    array = Arr(0, 0)
    ArraySetAsSeries(array, True)
    return (array[0] if (CopyTime(symbol_name, timeframe, shift, 1, array) == 1) else 0)

def EquationDirect(left_bar, left_price, right_bar, right_price, bar_to_search):
    return (left_price if (right_bar == left_bar) else ((_fdiv(right_price - left_price, right_bar - left_bar) * (bar_to_search - left_bar)) + left_price))

def TimeframeToString(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7)

def GetMA(rates_total, method, period, shift, price, ma, tick_volume):
    _sw1 = method
    if _sw1 == METHOD_EMA:
        ma[shift] = EMA(rates_total, price[shift], ma[shift + 1], period, shift)
    elif _sw1 == METHOD_SMMA:
        ma[shift] = SMMA(rates_total, price, ma[shift + 1], period, shift)
    elif _sw1 == METHOD_LWMA:
        ma[shift] = LWMA(rates_total, price, period, shift)
    elif _sw1 == METHOD_WILDER_EMA:
        ma[shift] = Wilder(rates_total, price[shift], ma[shift + 1], period, shift)
    elif _sw1 == METHOD_SINE_WMA:
        ma[shift] = SineWMA(rates_total, price, period, shift)
    elif _sw1 == METHOD_TRI_MA:
        ma[shift] = TriMA(rates_total, price, period, shift)
    elif _sw1 == METHOD_LSMA:
        ma[shift] = LSMA(rates_total, price, period, shift)
    elif _sw1 == METHOD_HMA:
        ma[shift] = HMA(rates_total, price, period, shift)
    elif _sw1 == METHOD_ZL_EMA:
        ma[shift] = ZeroLagEMA(rates_total, price, ma[shift + 1], period, shift)
    elif _sw1 == METHOD_ITREND_MA:
        ma[shift] = ITrend(rates_total, price, ma, period, shift)
    elif _sw1 == METHOD_MOVING_MEDIAN:
        ma[shift] = Median(rates_total, price, period, shift)
    elif _sw1 == METHOD_GEO_MEAN:
        ma[shift] = GeoMean(rates_total, price, period, shift)
    elif _sw1 == METHOD_REMA:
        ma[shift] = REMA(rates_total, price[shift], ma, period, 0.5, shift)
    elif _sw1 == METHOD_ILRS:
        ma[shift] = ILRS(rates_total, price, period, shift)
    elif _sw1 == METHOD_IE_2:
        ma[shift] = IE2(rates_total, price, period, shift)
    elif _sw1 == METHOD_TRI_MA_GEN:
        ma[shift] = TriMAgen(rates_total, price, period, shift)
    elif _sw1 == METHOD_VWMA:
        ma[shift] = VWMA(rates_total, price, tick_volume, period, shift)
    else:
        ma[shift] = SMA(rates_total, price, period, shift)

def SMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return array_src[shift]
    sum_ = 0.0
    for i in range(0, period):
        sum_ += array_src[shift + i]
    return _fdiv(sum_, period)

def EMA(rates_total, price, prev, period, shift):
    return (price if (shift >= (rates_total - 2) or period < 1) else (prev + (_fdiv(2.0, 1 + period) * (price - prev))))

def Wilder(rates_total, price, prev, period, shift):
    return (price if (shift >= (rates_total - 2) or period < 1) else (prev + _fdiv(price - prev, period)))

def LWMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = 0.0
    weight = 0.0
    for i in range(0, period):
        weight += period - i
        sum_ += array_src[shift + i] * (period - i)
    return (_fdiv(sum_, weight) if (weight > 0) else 0)

def SineWMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = 0.0
    weight = 0.0
    for i in range(0, period):
        weight += sin(_fdiv(M_PI * (i + 1), period + 1))
        sum_ += array_src[shift + i] * sin(_fdiv(M_PI * (i + 1), period + 1))
    return (_fdiv(sum_, weight) if (weight > 0) else 0)

def TriMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sma = 0.0
    len_ = _int(ceil((period + 1) * 0.5))
    sum_ = 0.0
    for i in range(0, len_):
        sma = SMA(rates_total, array_src, len_, shift + i)
        sum_ += sma
    return _fdiv(sum_, len_)

def LSMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = 0.0
    for i in range(period, 1 - 1, -1):
        sum_ += (i - ((period + 1) / 3.0)) * array_src[shift + period - i]
    return _fdiv(sum_ * 6.0, period * (period + 1))

def SMMA(rates_total, array_src, prev, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    smma = 0.0
    if shift == (rates_total - period - 1):
        smma = SMA(rates_total, array_src, period, shift)
    elif shift < (rates_total - period - 1):
        sum_ = 0.0
        for i in range(0, period):
            sum_ += array_src[shift + i + 1]
        smma = _fdiv(sum_ - prev + array_src[shift], period)
    return smma

def HMA(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    tmp1 = Arr(0, 0.0)
    hma = 0.0
    len_ = _int(sqrt(period))
    ArrayResize(tmp1, len_)
    if shift == (rates_total - period - 1):
        hma = array_src[shift]
    elif shift < (rates_total - period - 1):
        for i in range(0, len_):
            tmp1[i] = (2.0 * LWMA(rates_total, array_src, _idiv(period, 2), shift + i)) - LWMA(rates_total, array_src, period, shift + i)
        hma = LWMA(rates_total, tmp1, len_, 0)
    return hma

def ZeroLagEMA(rates_total, array_src, prev, period, shift):
    alfa = _fdiv(2.0, 1 + period)
    lag = _int(0.5 * (period - 1))
    return (array_src[shift] if (shift >= (rates_total - lag)) else ((alfa * ((2.0 * array_src[shift]) - array_src[shift + lag])) + ((1 - alfa) * prev)))

def ITrend(rates_total, array_src, array, period, shift):
    alfa = _fdiv(2.0, period + 1)
    return ((((alfa - (0.25 * alfa * alfa)) * array_src[shift]) + (0.5 * alfa * alfa * array_src[shift + 1]) - ((alfa - (0.75 * alfa * alfa)) * array_src[shift + 2]) + (2 * (1 - alfa) * array[shift + 1]) - ((1 - alfa) * (1 - alfa) * array[shift + 2])) if (shift < (rates_total - 7)) else ((array_src[shift] + (2 * array_src[shift + 1]) + array_src[shift + 2]) / 4.0))

def Median(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    array = Arr(0, 0.0)
    ArrayResize(array, period)
    for i in range(0, period):
        array[i] = array_src[shift + i]
    ArraySort(array)
    num = _int(round(_idiv(period - 1, 2)))
    return (array_src[num] if (fmod(period, 2) > 0) else (0.5 * (array_src[num] + array[num + 1])))

def GeoMean(rates_total, array_src, period, shift):
    gmean = 0.0
    if shift < (rates_total - period):
        gmean = pow(array_src[shift], _fdiv(1.0, period))
        for i in range(1, period):
            gmean *= pow(array_src[shift + i], _fdiv(1.0, period))
    return gmean

def REMA(rates_total, price, array, period, lambda_, shift):
    alpha = _fdiv(2.0, period + 1)
    return (price if (shift >= (rates_total - 3)) else _fdiv((array[shift + 1] * (1 + (2 * lambda_))) + (alpha * (price - array[shift + 1])) - (lambda_ * array[shift + 2]), 1 + lambda_))

def ILRS(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = period * (period - 1) * 0.5
    sum2 = ((period - 1) * period * ((2 * period) - 1)) / 6.0
    sum1 = 0.0
    sumy = 0.0
    for i in range(0, period):
        sum1 += i * array_src[shift + i]
        sumy += array_src[shift + i]
    num1 = (period * sum1) - (sum_ * sumy)
    num2 = (sum_ * sum_) - (period * sum2)
    slope = (_fdiv(num1, num2) if (num2 != 0) else 0)
    return slope + SMA(rates_total, array_src, period, shift)

def IE2(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    return 0.5 * (ILRS(rates_total, array_src, period, shift) + LSMA(rates_total, array_src, period, shift))

def TriMAgen(rates_total, array_src, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    len1 = _int(floor((period + 1) * 0.5))
    len2 = _int(ceil((period + 1) * 0.5))
    sum_ = 0.0
    for i in range(0, len2):
        sum_ += SMA(rates_total, array_src, len1, shift + i)
    return _fdiv(sum_, len2)

def VWMA(rates_total, array_src, volume, period, shift):
    if period < 1 or shift > (rates_total - period - 1):
        return 0.0
    sum_ = 0.0
    weight = 0.0
    for i in range(0, period):
        weight += float(volume[shift + i])
        sum_ += array_src[shift + i] * volume[shift + i]
    return (_fdiv(sum_, weight) if (weight > 0) else 0)

# ---- global variables initialised from expressions
DataBuff = Arr(3, 0, dyn=False, factory=SDataBand)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TymenSTARCBandsMTF(_MQL5Indicator):
    name = 'Tymen_STARCBands_MTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpDrawMode': _Choice({0: 'Steps', 1: 'Slope'}, default=0),  # Drawing mode
        'InpShowMiddle': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show middle lines
        'InpShowBands1': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show first Tymen STARC Bands
        'InpTimeframe1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # First bands timeframe
        'InpPeriodATR1': 15,  # First bands ATR period
        'InpPeriodMA1': 6,  # First bands MA period
        'InpMethod1': _Choice({0: 'Simple', 1: 'Exponential', 2: 'Smoothed', 3: 'Linear-Weighted', 4: 'Wilder Exponential', 5: 'Sine-Weighted', 6: 'Triangular', 7: 'Least Square', 8: 'Hull MA by Alan Hull', 9: 'Zero-Lag Exponential', 10: 'Instantaneous Trendline by J.Ehlers', 11: 'Moving Median', 12: 'Geometric Mean', 13: 'Regularized EMA by Chris Satchwell', 14: 'Integral of Linear Regression Slope', 15: 'Combination of LSMA and ILRS', 16: 'Triangular MA generalized by J.Ehlers', 17: 'Volume-Weighted'}, default=1),  # First bands Method
        'InpAppliedPrice1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # First bands Applied price
        'InpKATR1': 1.0,  # First bands ATR coefficient
        'InpMKATR1': 0.7,  # First bands ATR middle coefficient
        'InpShowBands2': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show second Tymen STARC Bands
        'InpTimeframe2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Second bands timeframe
        'InpPeriodATR2': 15,  # Second bands ATR period
        'InpPeriodMA2': 6,  # Second bands MA period
        'InpMethod2': _Choice({0: 'Simple', 1: 'Exponential', 2: 'Smoothed', 3: 'Linear-Weighted', 4: 'Wilder Exponential', 5: 'Sine-Weighted', 6: 'Triangular', 7: 'Least Square', 8: 'Hull MA by Alan Hull', 9: 'Zero-Lag Exponential', 10: 'Instantaneous Trendline by J.Ehlers', 11: 'Moving Median', 12: 'Geometric Mean', 13: 'Regularized EMA by Chris Satchwell', 14: 'Integral of Linear Regression Slope', 15: 'Combination of LSMA and ILRS', 16: 'Triangular MA generalized by J.Ehlers', 17: 'Volume-Weighted'}, default=1),  # Second bands Method
        'InpAppliedPrice2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Second bands Applied price
        'InpKATR2': 1.0,  # Second bands ATR coefficient
        'InpMKATR2': 0.7,  # Second bands ATR middle coefficient
        'InpShowBands3': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show third Tymen STARC Bands
        'InpTimeframe3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Third bands timeframe
        'InpPeriodATR3': 15,  # Third bands ATR period
        'InpPeriodMA3': 6,  # Third bands MA period
        'InpMethod3': _Choice({0: 'Simple', 1: 'Exponential', 2: 'Smoothed', 3: 'Linear-Weighted', 4: 'Wilder Exponential', 5: 'Sine-Weighted', 6: 'Triangular', 7: 'Least Square', 8: 'Hull MA by Alan Hull', 9: 'Zero-Lag Exponential', 10: 'Instantaneous Trendline by J.Ehlers', 11: 'Moving Median', 12: 'Geometric Mean', 13: 'Regularized EMA by Chris Satchwell', 14: 'Integral of Linear Regression Slope', 15: 'Combination of LSMA and ILRS', 16: 'Triangular MA generalized by J.Ehlers', 17: 'Volume-Weighted'}, default=1),  # Third bands Method
        'InpAppliedPrice3': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Third bands Applied price
        'InpKATR3': 1.0,  # Third bands ATR coefficient
        'InpMKATR3': 0.7,  # Third bands ATR middle coefficient
    }

