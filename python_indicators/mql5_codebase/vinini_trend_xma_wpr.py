"""vinini_trend_xma_wpr — converted from MQL5: MQL5 Indicators/VininI_Trend_XMA_WPR/vinini_trend_xma_wpr.mq5

VininI_Trend_XMA_WPR
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16711935, 8388736, 8421504, 16711680, 16760576]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'VininI_Trend_XMA_WPR'}, 'levels': [], 'description': ['VininI_Trend_XMA_WPR'], 'name': 'vinini_trend_xma_wpr', 'source': 'MQL5 Indicators/VininI_Trend_XMA_WPR/vinini_trend_xma_wpr.mq5', 'folder': 'VininI_Trend_XMA_WPR', 'inputs': [{'mql': 'WPR_Period', 'py': 'WPR_Period', 'param': 'WPR_Period', 'type': 'uint', 'default': 100, 'label': 'iWPR indicator period', 'sinput': False}, {'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'smoothing method of moving averages', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 3, 'label': 'start smoothing depth of moving averages', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'moving averages smoothing parameter,', 'sinput': False}, {'mql': 'MA_Step', 'py': 'MA_Step', 'param': 'MA_Step', 'type': 'uint', 'default': 10, 'label': 'step of depth changing of the moving averages smoothing', 'sinput': False}, {'mql': 'MA_Count', 'py': 'MA_Count', 'param': 'MA_Count', 'type': 'uint', 'default': 50, 'label': 'number of smoothing steps', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 4, 'label': 'indicator smoothing method', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'uint', 'default': 20, 'label': 'indicator smoothing depth', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 100, 'label': 'indicator smoothing parameter,', 'sinput': False}, {'mql': 'UpLevel', 'py': 'UpLevel', 'param': 'UpLevel', 'type': 'int', 'default': 50, 'label': 'Up level (range 0/+100)', 'sinput': False}, {'mql': 'DnLevel', 'py': 'DnLevel', 'param': 'DnLevel', 'type': 'int', 'default': -50, 'label': 'Down level (range -100/0)', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
WPR_Period = _input('WPR_Period', 100)  # iWPR indicator period
MA_Method1 = _input('MA_Method1', MODE_SMA)  # smoothing method of moving averages
Length1 = _input('Length1', 3)  # start smoothing depth of moving averages
Phase1 = _input('Phase1', 15)  # moving averages smoothing parameter,
MA_Step = _input('MA_Step', 10)  # step of depth changing of the moving averages smoothing
MA_Count = _input('MA_Count', 50)  # number of smoothing steps
MA_Method2 = _input('MA_Method2', MODE_JJMA)  # indicator smoothing method
Length2 = _input('Length2', 20)  # indicator smoothing depth
Phase2 = _input('Phase2', 100)  # indicator smoothing parameter,
UpLevel = _input('UpLevel', 50)  # Up level (range 0/+100)
DnLevel = _input('DnLevel', -50)  # Down level (range -100/0)
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
WPR_Handle = 0
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
nsize = 0
period = Arr(0, 0)

def OnInit():
    global WPR_Handle, min_rates_1, min_rates_2, min_rates_total, nsize
    min_rates_1 = _int(WPR_Period)
    min_rates_2 = min_rates_1 + XMA2.GetStartBars(MA_Method1, Length1 + (MA_Step * (MA_Count - 1)), Phase1)
    min_rates_total = min_rates_2 + XMA2.GetStartBars(MA_Method2, Length2, Phase2)
    XMA2.XMALengthCheck('Length1', Length1)
    XMA2.XMALengthCheck('Length2', Length2)
    XMA2.XMAPhaseCheck('Phase1', Phase1, MA_Method1)
    XMA2.XMAPhaseCheck('Phase2', Phase2, MA_Method2)
    nsize = _int(MA_Count)
    if ArrayResize(XMA1, nsize) < nsize:
        Print('Failed to distribute the memory for XMA1[] array')
    if ArrayResize(period, nsize) < nsize:
        Print('Failed to distribute the memory for period[] array')
    WPR_Handle = iWPR(None, 0, WPR_Period)
    if WPR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the WPR indicator')
    for sm in range(0, nsize):
        period[sm] = _int(Length1 + (sm * MA_Step))
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'VininI_Trend_XMA_WPR')
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
    if BarsCalculated(WPR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    xwpr = 0.0
    res = 0.0
    xres = 0.0
    WPR = Arr(1, 0.0, dyn=False)
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
        if CopyBuffer(WPR_Handle, 0, rates_total - bar - 1, 1, WPR) <= 0:
            return 0
        sum_ = 0
        sm = 0
        while sm < nsize:
            xwpr = XMA1[sm].XMASeries(min_rates_1, prev_calculated, rates_total, MA_Method1, Phase1, period[sm], WPR[0], bar, False)
            if WPR[0] > xwpr:
                sum_ += 1
            else:
                sum_ -= 1
            sm += 1
        res = _idiv(100 * sum_, nsize)
        xres = XMA2.XMASeries(min_rates_2, prev_calculated, rates_total, MA_Method2, Phase2, Length2, res, bar, False)
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


class VininiTrendXmaWpr(_MQL5Indicator):
    name = 'vinini_trend_xma_wpr'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'WPR_Period': 100,  # iWPR indicator period
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # smoothing method of moving averages
        'Length1': 3,  # start smoothing depth of moving averages
        'Phase1': 15,  # moving averages smoothing parameter,
        'MA_Step': 10,  # step of depth changing of the moving averages smoothing
        'MA_Count': 50,  # number of smoothing steps
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # indicator smoothing method
        'Length2': 20,  # indicator smoothing depth
        'Phase2': 100,  # indicator smoothing parameter,
        'UpLevel': 50,  # Up level (range 0/+100)
        'DnLevel': -50,  # Down level (range -100/0)
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

