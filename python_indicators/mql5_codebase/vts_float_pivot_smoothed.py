"""VTS_Float_Pivot_Smoothed — converted from MQL5: MQL5 Indicators/VTS_Float_Pivot_Smoothed/VTS_Float_Pivot_Smoothed.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 5, 8: 5}, 'colors': {1: [8388736], 2: [16711680], 3: [8388736], 4: [16711680], 5: [8388736], 6: [16711680], 7: [16711935], 8: [10156544]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2}, 'styles': {}, 'labels': {1: 'VTS Sell', 2: 'VTS Buy', 3: 'VTS Sell', 4: 'VTS Buy', 5: 'VTS Sell', 6: 'VTS Buy', 7: 'VTS Sell', 8: 'VTS Buy'}, 'levels': [], 'description': [], 'name': 'VTS_Float_Pivot_Smoothed', 'source': 'MQL5 Indicators/VTS_Float_Pivot_Smoothed/VTS_Float_Pivot_Smoothed.mq5', 'folder': 'VTS_Float_Pivot_Smoothed', 'inputs': [{'mql': 'IPeriod', 'py': 'IPeriod', 'param': 'IPeriod', 'type': 'int', 'default': 30, 'label': 'Период поиска экстремумов', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 5, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'HMA_Method', 'py': 'HMA_Method', 'param': 'HMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод сглаживания', 'sinput': False}, {'mql': 'HLength', 'py': 'HLength', 'param': 'HLength', 'type': 'uint', 'default': 12, 'label': 'Глубина  сглаживания', 'sinput': False}, {'mql': 'HPhase', 'py': 'HPhase', 'param': 'HPhase', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания,', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum ENUM_APPLIED_PRICE_
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
_enum('ENUM_APPLIED_PRICE_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
IPeriod = _input('IPeriod', 30)  # Период поиска экстремумов
IPC = _input('IPC', PRICE_MEDIAN_)  # ценовая константа
HMA_Method = _input('HMA_Method', MODE_SMA_)  # Метод сглаживания
HLength = _input('HLength', 12)  # Глубина  сглаживания
HPhase = _input('HPhase', 100)  # Параметр сглаживания,
UpIndBuffer1 = Arr(0, 0.0)
DnIndBuffer1 = Arr(0, 0.0)
UpIndBuffer2 = Arr(0, 0.0)
DnIndBuffer2 = Arr(0, 0.0)
UpIndBuffer3 = Arr(0, 0.0)
DnIndBuffer3 = Arr(0, 0.0)
UpIndBuffer4 = Arr(0, 0.0)
DnIndBuffer4 = Arr(0, 0.0)
min_rates_total = 0
Count = Arr(0, 0)
XHigh = Arr(0, 0.0)
XLow = Arr(0, 0.0)

def Recount_ArrayZeroPos(CoArr, Size):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def OnInit():
    global min_rates_total
    min_rates_total = GetStartBars(HMA_Method, HLength, HPhase) + 1
    min_rates_total += MathMax(3, IPeriod)
    min_rates_total += 30
    ArrayResize(Count, IPeriod)
    ArrayResize(XHigh, IPeriod)
    ArrayResize(XLow, IPeriod)
    ArraySetAsSeries(Count, True)
    ArraySetAsSeries(XHigh, True)
    ArraySetAsSeries(XLow, True)
    SetIndexBuffer(0, DnIndBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(1, UpIndBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(2, DnIndBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(3, UpIndBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(4, DnIndBuffer3, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(5, UpIndBuffer3, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(6, DnIndBuffer4, INDICATOR_DATA)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(7, UpIndBuffer4, INDICATOR_DATA)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'VTS_Float_Pivot_Smoothed'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_VTS10_prev, _s_OnCalculate_VTS11_prev, _s_OnCalculate_VTS12_prev, _s_OnCalculate_VTS13_prev, _s_OnCalculate_VTS14_prev, _s_OnCalculate_VTS15_prev, _s_OnCalculate_VTS16_prev, _s_OnCalculate_VTS17_prev, _s_OnCalculate_VTS18_prev, _s_OnCalculate_VTS19_prev, _s_OnCalculate_VTS1_prev, _s_OnCalculate_VTS20_prev, _s_OnCalculate_VTS21_prev, _s_OnCalculate_VTS22_prev, _s_OnCalculate_VTS23_prev, _s_OnCalculate_VTS2_prev, _s_OnCalculate_VTS3_prev, _s_OnCalculate_VTS4_prev, _s_OnCalculate_VTS5_prev, _s_OnCalculate_VTS6_prev, _s_OnCalculate_VTS7_prev, _s_OnCalculate_VTS8_prev, _s_OnCalculate_VTS9_prev, _s_OnCalculate_VTS_prev
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    VTS = 0.0
    VTS1 = 0.0
    VTS2 = 0.0
    VTS3 = 0.0
    VTS4 = 0.0
    VTS5 = 0.0
    VTS6 = 0.0
    VTS7 = 0.0
    VTS8 = 0.0
    VTS9 = 0.0
    VTS10 = 0.0
    VTS11 = 0.0
    VTS12 = 0.0
    VTS13 = 0.0
    VTS14 = 0.0
    VTS15 = 0.0
    VTS16 = 0.0
    VTS17 = 0.0
    VTS18 = 0.0
    VTS19 = 0.0
    VTS20 = 0.0
    VTS21 = 0.0
    VTS22 = 0.0
    VTS23 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        ArrayInitialize(Count, None)
        ArrayInitialize(XHigh, None)
        ArrayInitialize(XLow, None)
        start = min_rates_total - 2
        DnIndBuffer2[start] = PriceSeries(IPC, start, open, low, high, close)
        DnIndBuffer1[start] = DnIndBuffer2[start]
        UpIndBuffer2[start] = DnIndBuffer1[start]
        UpIndBuffer1[start] = UpIndBuffer2[start]
        res = UpIndBuffer1[start]
        _s_OnCalculate_VTS_prev = res
        _s_OnCalculate_VTS1_prev = res
        _s_OnCalculate_VTS2_prev = res
        _s_OnCalculate_VTS3_prev = res
        _s_OnCalculate_VTS4_prev = res
        _s_OnCalculate_VTS5_prev = res
        _s_OnCalculate_VTS6_prev = res
        _s_OnCalculate_VTS7_prev = res
        _s_OnCalculate_VTS8_prev = res
        _s_OnCalculate_VTS9_prev = res
        _s_OnCalculate_VTS10_prev = res
        _s_OnCalculate_VTS11_prev = res
        _s_OnCalculate_VTS12_prev = res
        _s_OnCalculate_VTS13_prev = res
        _s_OnCalculate_VTS14_prev = res
        _s_OnCalculate_VTS15_prev = res
        _s_OnCalculate_VTS16_prev = res
        _s_OnCalculate_VTS17_prev = res
        _s_OnCalculate_VTS18_prev = res
        _s_OnCalculate_VTS19_prev = res
        _s_OnCalculate_VTS20_prev = res
        _s_OnCalculate_VTS21_prev = res
        _s_OnCalculate_VTS22_prev = res
        _s_OnCalculate_VTS23_prev = res
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        pivot = XMAP.XMASeries(0, prev_calculated, rates_total, HMA_Method, HPhase, HLength, PriceSeries(IPC, bar, open, low, high, close), bar, False)
        XHigh[Count[0]] = XMAH.XMASeries(0, prev_calculated, rates_total, HMA_Method, HPhase, HLength, high[bar], bar, False)
        XLow[Count[0]] = XMAL.XMASeries(0, prev_calculated, rates_total, HMA_Method, HPhase, HLength, low[bar], bar, False)
        max_ = XHigh[ArrayMaximum(XHigh, 0, IPeriod)]
        min_ = XLow[ArrayMinimum(XLow, 0, IPeriod)]
        res = (max_ + min_ + pivot) / 3
        VTS1 = ((2 * res) - min_ + res) / 2
        VTS = (res + ((2 * res) - max_)) / 2
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count, IPeriod)
        if bar < (min_rates_total - 1):
            continue
        VTS2 = MathMax(VTS, _s_OnCalculate_VTS_prev)
        VTS3 = MathMin(VTS1, _s_OnCalculate_VTS1_prev)
        VTS4 = MathMax(VTS2, _s_OnCalculate_VTS2_prev)
        VTS5 = MathMin(VTS3, _s_OnCalculate_VTS3_prev)
        VTS6 = MathMax(VTS4, _s_OnCalculate_VTS4_prev)
        VTS7 = MathMin(VTS5, _s_OnCalculate_VTS5_prev)
        VTS8 = MathMax(VTS6, _s_OnCalculate_VTS6_prev)
        VTS9 = MathMin(VTS7, _s_OnCalculate_VTS7_prev)
        VTS10 = MathMax(VTS8, _s_OnCalculate_VTS8_prev)
        VTS11 = MathMin(VTS9, _s_OnCalculate_VTS9_prev)
        VTS12 = MathMax(VTS10, _s_OnCalculate_VTS10_prev)
        VTS13 = MathMin(VTS11, _s_OnCalculate_VTS11_prev)
        VTS14 = MathMax(VTS12, _s_OnCalculate_VTS12_prev)
        VTS15 = MathMin(VTS13, _s_OnCalculate_VTS13_prev)
        VTS16 = MathMax(VTS14, _s_OnCalculate_VTS14_prev)
        VTS17 = MathMin(VTS15, _s_OnCalculate_VTS15_prev)
        VTS18 = MathMax(VTS16, _s_OnCalculate_VTS16_prev)
        VTS19 = MathMin(VTS17, _s_OnCalculate_VTS17_prev)
        VTS20 = MathMax(VTS18, _s_OnCalculate_VTS18_prev)
        VTS21 = MathMin(VTS19, _s_OnCalculate_VTS19_prev)
        VTS22 = MathMax(VTS20, _s_OnCalculate_VTS20_prev)
        VTS23 = MathMin(VTS21, _s_OnCalculate_VTS21_prev)
        UpIndBuffer1[bar] = MathMax(VTS22, _s_OnCalculate_VTS22_prev)
        DnIndBuffer1[bar] = MathMin(VTS23, _s_OnCalculate_VTS23_prev)
        UpIndBuffer2[bar] = MathMax(UpIndBuffer1[bar], UpIndBuffer1[bar - 1])
        DnIndBuffer2[bar] = MathMin(DnIndBuffer1[bar], DnIndBuffer1[bar - 1])
        UpIndBuffer3[bar] = MathMax(UpIndBuffer2[bar], UpIndBuffer2[bar - 1])
        DnIndBuffer3[bar] = MathMin(DnIndBuffer2[bar], DnIndBuffer2[bar - 1])
        UpIndBuffer4[bar] = UpIndBuffer4[bar - 1]
        DnIndBuffer4[bar] = DnIndBuffer4[bar - 1]
        price = PriceSeries(IPC, bar, open, low, high, close)
        if price > DnIndBuffer3[bar]:
            UpIndBuffer4[bar] = UpIndBuffer3[bar]
            DnIndBuffer4[bar] = 0.0
        if price < UpIndBuffer3[bar]:
            DnIndBuffer4[bar] = DnIndBuffer3[bar]
            UpIndBuffer4[bar] = 0.0
        if bar < (rates_total - 1):
            _s_OnCalculate_VTS_prev = VTS
            _s_OnCalculate_VTS1_prev = VTS1
            _s_OnCalculate_VTS2_prev = VTS2
            _s_OnCalculate_VTS3_prev = VTS3
            _s_OnCalculate_VTS4_prev = VTS4
            _s_OnCalculate_VTS5_prev = VTS5
            _s_OnCalculate_VTS6_prev = VTS6
            _s_OnCalculate_VTS7_prev = VTS7
            _s_OnCalculate_VTS8_prev = VTS8
            _s_OnCalculate_VTS9_prev = VTS9
            _s_OnCalculate_VTS10_prev = VTS10
            _s_OnCalculate_VTS11_prev = VTS11
            _s_OnCalculate_VTS12_prev = VTS12
            _s_OnCalculate_VTS13_prev = VTS13
            _s_OnCalculate_VTS14_prev = VTS14
            _s_OnCalculate_VTS15_prev = VTS15
            _s_OnCalculate_VTS16_prev = VTS16
            _s_OnCalculate_VTS17_prev = VTS17
            _s_OnCalculate_VTS18_prev = VTS18
            _s_OnCalculate_VTS19_prev = VTS19
            _s_OnCalculate_VTS20_prev = VTS20
            _s_OnCalculate_VTS21_prev = VTS21
            _s_OnCalculate_VTS22_prev = VTS22
            _s_OnCalculate_VTS23_prev = VTS23
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMAL = _alloc(CXMA)
XMAL.__init__()
XMAH = _alloc(CXMA)
XMAH.__init__()
XMAP = _alloc(CXMA)
XMAP.__init__()

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1
_s_OnCalculate_VTS_prev = 0.0
_s_OnCalculate_VTS1_prev = 0.0
_s_OnCalculate_VTS2_prev = 0.0
_s_OnCalculate_VTS3_prev = 0.0
_s_OnCalculate_VTS4_prev = 0.0
_s_OnCalculate_VTS5_prev = 0.0
_s_OnCalculate_VTS6_prev = 0.0
_s_OnCalculate_VTS7_prev = 0.0
_s_OnCalculate_VTS8_prev = 0.0
_s_OnCalculate_VTS9_prev = 0.0
_s_OnCalculate_VTS10_prev = 0.0
_s_OnCalculate_VTS11_prev = 0.0
_s_OnCalculate_VTS12_prev = 0.0
_s_OnCalculate_VTS13_prev = 0.0
_s_OnCalculate_VTS14_prev = 0.0
_s_OnCalculate_VTS15_prev = 0.0
_s_OnCalculate_VTS16_prev = 0.0
_s_OnCalculate_VTS17_prev = 0.0
_s_OnCalculate_VTS18_prev = 0.0
_s_OnCalculate_VTS19_prev = 0.0
_s_OnCalculate_VTS20_prev = 0.0
_s_OnCalculate_VTS21_prev = 0.0
_s_OnCalculate_VTS22_prev = 0.0
_s_OnCalculate_VTS23_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VTSFloatPivotSmoothed(_MQL5Indicator):
    name = 'VTS_Float_Pivot_Smoothed'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'IPeriod': 30,  # Период поиска экстремумов
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW0_2', 12: 'Demark Price'}, default=5),  # ценовая константа
        'HMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод сглаживания
        'HLength': 12,  # Глубина  сглаживания
        'HPhase': 100,  # Параметр сглаживания,
    }

