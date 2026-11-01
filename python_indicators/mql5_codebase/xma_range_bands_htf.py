"""xma_range_bands_htf — converted from MQL5: MQL5 Indicators/XMA_Range_Bands_HTF/xma_range_bands_htf.mq5

XMA Range Bands HTF
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [13458026], 2: [3329330], 3: [9639167]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'XMA Range Bands HTF', 2: 'Upper XMA Range Bands HTF', 3: 'Lower XMA Range Bands HTF'}, 'levels': [], 'description': ['XMA Range Bands HTF'], 'name': 'xma_range_bands_htf', 'source': 'MQL5 Indicators/XMA_Range_Bands_HTF/xma_range_bands_htf.mq5', 'folder': 'XMA_Range_Bands_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Chart period', 'sinput': False}, {'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'Smoothing method of moving average', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'int', 'default': 100, 'label': 'Smoothing depth of moving average', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'Moving average smoothing parameter,', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 4, 'label': 'Candles size smoothing method', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'int', 'default': 20, 'label': 'Smoothing depth of candles size', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 100, 'label': 'Candles size smoothing parameter,', 'sinput': False}, {'mql': 'Deviation', 'py': 'Deviation', 'param': 'Deviation', 'type': 'double', 'default': 2.0, 'label': 'Channel expansion ratio', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Vertical shift of the indicator in pointsх', 'sinput': False}, {'mql': 'ReDraw', 'py': 'ReDraw', 'param': 'ReDraw', 'type': 'bool', 'default': True, 'label': 'Repeat of information show on the empty bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Chart period
MA_Method1 = _input('MA_Method1', MODE_SMA)  # Smoothing method of moving average
Length1 = _input('Length1', 100)  # Smoothing depth of moving average
Phase1 = _input('Phase1', 15)  # Moving average smoothing parameter,
MA_Method2 = _input('MA_Method2', MODE_JJMA)  # Candles size smoothing method
Length2 = _input('Length2', 20)  # Smoothing depth of candles size
Phase2 = _input('Phase2', 100)  # Candles size smoothing parameter,
Deviation = _input('Deviation', 2.0)  # Channel expansion ratio
IPC = _input('IPC', PRICE_CLOSE)  # Price constant
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # Vertical shift of the indicator in pointsх
ReDraw = _input('ReDraw', True)  # Repeat of information show on the empty bars
ExtLineBuffer0 = Arr(0, 0.0)
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
Init = False
dPriceShift = 0.0
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, Init, dPriceShift, min_rates_total
    min_rates_total = 3
    Init = True
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('XMA_Range_Bands indicator chart period cannot be less than the current chart period')
        Init = False
        return INIT_FAILED
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'XMA_Range_Bands', MA_Method1, Length1, Phase1, MA_Method2, Length2, Phase2, Deviation, IPC, 0, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the XMA_Range_Bands indicator')
        Init = False
        return INIT_FAILED
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, ExtLineBuffer0, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer0, True)
    SetIndexBuffer(1, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLineBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer1, True)
    ArraySetAsSeries(ExtLineBuffer2, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'XMA Range Bands' + '( ' + GetStringTimeframe(TimeFrame) + ' )')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total or (not Init):
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    limit = 0
    bar = 0
    XMA = Arr(2, 0.0, dyn=False)
    Upper = Arr(2, 0.0, dyn=False)
    Lower = Arr(2, 0.0, dyn=False)
    XMATime = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtLineBuffer0[bar] = EMPTY_VALUE
        ExtLineBuffer1[bar] = EMPTY_VALUE
        ExtLineBuffer2[bar] = EMPTY_VALUE
        if CopyTime(Symbol(), TimeFrame, _DT(time[bar]), 1, XMATime) <= 0:
            return 0
        if time[bar] >= XMATime[0] and time[bar + 1] < XMATime[0]:
            _s_OnCalculate_LastCountBar = bar
            if CopyBuffer(Ind_Handle, 0, _DT(time[bar]), 2, XMA) <= 0:
                return 0
            if CopyBuffer(Ind_Handle, 1, _DT(time[bar]), 2, Upper) <= 0:
                return 0
            if CopyBuffer(Ind_Handle, 2, _DT(time[bar]), 2, Lower) <= 0:
                return 0
            ExtLineBuffer0[bar] = XMA[1]
            ExtLineBuffer1[bar] = Upper[1]
            ExtLineBuffer2[bar] = Lower[1]
        if ReDraw:
            if ExtLineBuffer0[bar + 1] != EMPTY_VALUE and ExtLineBuffer0[bar] == EMPTY_VALUE:
                ExtLineBuffer0[bar] = ExtLineBuffer0[bar + 1]
                ExtLineBuffer1[bar] = ExtLineBuffer1[bar + 1]
                ExtLineBuffer2[bar] = ExtLineBuffer2[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XmaRangeBandsHtf(_MQL5Indicator):
    name = 'xma_range_bands_htf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Chart period
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Smoothing method of moving average
        'Length1': 100,  # Smoothing depth of moving average
        'Phase1': 15,  # Moving average smoothing parameter,
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Candles size smoothing method
        'Length2': 20,  # Smoothing depth of candles size
        'Phase2': 100,  # Candles size smoothing parameter,
        'Deviation': 2.0,  # Channel expansion ratio
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Price constant
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'PriceShift': 0,  # Vertical shift of the indicator in pointsх
        'ReDraw': True,  # Repeat of information show on the empty bars
    }

