"""vinini_trend — converted from MQL5: MQL5 Indicators/VininI_Trend/vinini_trend.mq5

VininI_Trend
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [255, 128, 8421504, 8421376, 3329330]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'VininI_Trend'}, 'levels': [], 'description': ['VininI_Trend'], 'name': 'vinini_trend', 'source': 'MQL5 Indicators/VininI_Trend/vinini_trend.mq5', 'folder': 'VininI_Trend', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'smoothing method of moving averages', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 3, 'label': 'start smoothing depth of moving averages', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'moving averages smoothing parameter,', 'sinput': False}, {'mql': 'MA_Step', 'py': 'MA_Step', 'param': 'MA_Step', 'type': 'uint', 'default': 10, 'label': 'step of depth changing of the moving averages smoothing', 'sinput': False}, {'mql': 'MA_Count', 'py': 'MA_Count', 'param': 'MA_Count', 'type': 'uint', 'default': 50, 'label': 'number of smoothing steps', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 4, 'label': 'indicator smoothing method', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'uint', 'default': 20, 'label': 'indicator smoothing depth', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 100, 'label': 'indicator smoothing parameter,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'price constant', 'sinput': False}, {'mql': 'UpLevel', 'py': 'UpLevel', 'param': 'UpLevel', 'type': 'int', 'default': 50, 'label': 'Up level (range 0/+100)', 'sinput': False}, {'mql': 'DnLevel', 'py': 'DnLevel', 'param': 'DnLevel', 'type': 'int', 'default': -50, 'label': 'Down level (range -100/0)', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
MA_Method1 = _input('MA_Method1', MODE_SMA)  # smoothing method of moving averages
Length1 = _input('Length1', 3)  # start smoothing depth of moving averages
Phase1 = _input('Phase1', 15)  # moving averages smoothing parameter,
MA_Step = _input('MA_Step', 10)  # step of depth changing of the moving averages smoothing
MA_Count = _input('MA_Count', 50)  # number of smoothing steps
MA_Method2 = _input('MA_Method2', MODE_JJMA)  # indicator smoothing method
Length2 = _input('Length2', 20)  # indicator smoothing depth
Phase2 = _input('Phase2', 100)  # indicator smoothing parameter,
IPC = _input('IPC', PRICE_CLOSE)  # price constant
UpLevel = _input('UpLevel', 50)  # Up level (range 0/+100)
DnLevel = _input('DnLevel', -50)  # Down level (range -100/0)
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_ = 0
nsize = 0
period = Arr(0, 0)

def OnInit():
    global min_rates_, min_rates_total, nsize
    min_rates_ = XMA2.GetStartBars(MA_Method1, Length1 + (MA_Step * (MA_Count - 1)), Phase1)
    min_rates_total = min_rates_ + XMA2.GetStartBars(MA_Method2, Length2, Phase2)
    XMA2.XMALengthCheck('Length1', Length1)
    XMA2.XMALengthCheck('Length2', Length2)
    XMA2.XMAPhaseCheck('Phase1', Phase1, MA_Method1)
    XMA2.XMAPhaseCheck('Phase2', Phase2, MA_Method2)
    nsize = _int(MA_Count)
    if ArrayResize(XMA1, nsize) < nsize:
        Print('Failed to distribute the memory for XMA1[] array')
    if ArrayResize(period, nsize) < nsize:
        Print('Failed to distribute the memory for period[] array')
    for sm in range(0, nsize):
        period[sm] = _int(Length1 + (sm * MA_Step))
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'VininI_Trend')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, UpLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, DnLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price_ = 0.0
    xma = 0.0
    res = 0.0
    xres = 0.0
    first = 0
    bar = 0
    clr = 0
    sum_ = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        sum_ = 0
        sm = 0
        while sm < nsize:
            xma = XMA1[sm].XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, period[sm], price_, bar, False)
            if close[bar] > xma:
                sum_ += 1
            else:
                sum_ -= 1
            sm += 1
        res = _idiv(100 * sum_, nsize)
        xres = XMA2.XMASeries(min_rates_, prev_calculated, rates_total, MA_Method2, Phase2, Length2, res, bar, False)
        IndBuffer[bar] = xres
        clr = 2
        if xres > UpLevel:
            clr = 4
        elif xres > 0:
            clr = 3
        if xres < DnLevel:
            clr = 0
        elif xres < 0:
            clr = 1
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = Arr(0, 0, factory=CXMA)
XMA2 = _alloc(CXMA)
XMA2.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VininiTrend(_MQL5Indicator):
    name = 'vinini_trend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # smoothing method of moving averages
        'Length1': 3,  # start smoothing depth of moving averages
        'Phase1': 15,  # moving averages smoothing parameter,
        'MA_Step': 10,  # step of depth changing of the moving averages smoothing
        'MA_Count': 50,  # number of smoothing steps
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # indicator smoothing method
        'Length2': 20,  # indicator smoothing depth
        'Phase2': 100,  # indicator smoothing parameter,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # price constant
        'UpLevel': 50,  # Up level (range 0/+100)
        'DnLevel': -50,  # Down level (range -100/0)
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

