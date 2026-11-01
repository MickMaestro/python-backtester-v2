"""digital_macd — converted from MQL5: MQL5 Indicators/Digital_MACD/digital_macd.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 10, 2: 8}, 'colors': {1: [16711935, 6053069, 8421504, 14822282, 16760576], 2: [255, 8421504, 3329330]}, 'widths': {1: 2, 2: 3}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Digital MACD', 2: 'Signal Line'}, 'levels': [], 'description': [], 'name': 'digital_macd', 'source': 'MQL5 Indicators/Digital_MACD/digital_macd.mq5', 'folder': 'Digital_MACD', 'inputs': [{'mql': 'Signal_Method', 'py': 'Signal_Method', 'param': 'Signal_Method', 'type': 'int', 'default': 0, 'label': 'Signal line averaging method', 'sinput': False}, {'mql': 'Signal_XMA', 'py': 'Signal_XMA', 'param': 'Signal_XMA', 'type': 'int', 'default': 5, 'label': 'Signal line period', 'sinput': False}, {'mql': 'Signal_Phase', 'py': 'Signal_Phase', 'param': 'Signal_Phase', 'type': 'int', 'default': 100, 'label': 'Signal line parameter', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'price constant', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
Signal_Method = _input('Signal_Method', MODE_SMA)  # Signal line averaging method
Signal_XMA = _input('Signal_XMA', 5)  # Signal line period
Signal_Phase = _input('Signal_Phase', 100)  # Signal line parameter
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE_)  # price constant
min_rates_total = 0
min_rates_1 = 0
DMACDBuffer = Arr(0, 0.0)
SignBuffer = Arr(0, 0.0)
ColorDMACDBuffer = Arr(0, 0.0)
ColorSignBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_1, min_rates_total
    min_rates_1 = 66
    min_rates_total = min_rates_1 + XMA.GetStartBars(Signal_Method, Signal_XMA, Signal_Phase) + 2
    SetIndexBuffer(0, DMACDBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorDMACDBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, SignBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ColorSignBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    XMA.XMALengthCheck('Signal_XMA', Signal_XMA)
    XMA.XMAPhaseCheck('Signal_Phase', Signal_Phase, Signal_Method)
    shortname = Box("")
    Smooth = XMA.GetString_MA_Method(Signal_Method)
    StringConcatenate(shortname, 'Digital_MACD( ', Signal_XMA, ', ', Smooth, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first1 = 0
    first2 = 0
    first3 = 0
    bar = 0
    clr = 0
    fast_dma = 0.0
    slow_dma = 0.0
    dmacd = 0.0
    sign_dma = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first1 = min_rates_1
        first2 = min_rates_1 + 1
        first3 = min_rates_total + 1
    else:
        first1 = prev_calculated - 1
        first2 = first1
        first3 = first1
    bar = first1
    for bar in range(bar, rates_total):
        fast_dma = (0.214984061 * PriceSeries(AppliedPrice, bar - 0, open, low, high, close)) + (0.2065763732 * PriceSeries(AppliedPrice, bar - 1, open, low, high, close)) + (0.190372889 * PriceSeries(AppliedPrice, bar - 2, open, low, high, close)) + (0.1675422436 * PriceSeries(AppliedPrice, bar - 3, open, low, high, close)) + (0.139705315 * PriceSeries(AppliedPrice, bar - 4, open, low, high, close)) + (0.1087951881 * PriceSeries(AppliedPrice, bar - 5, open, low, high, close)) + (0.0768869405 * PriceSeries(AppliedPrice, bar - 6, open, low, high, close)) + (0.0460244906 * PriceSeries(AppliedPrice, bar - 7, open, low, high, close)) + (0.0180517395 * PriceSeries(AppliedPrice, bar - 8, open, low, high, close)) - (0.0055294579 * PriceSeries(AppliedPrice, bar - 9, open, low, high, close)) - (0.0236660212 * PriceSeries(AppliedPrice, bar - 10, open, low, high, close)) - (0.0358140055 * PriceSeries(AppliedPrice, bar - 11, open, low, high, close)) - (0.041949776 * PriceSeries(AppliedPrice, bar - 12, open, low, high, close)) - (0.042533145 * PriceSeries(AppliedPrice, bar - 13, open, low, high, close)) - (0.0384279507 * PriceSeries(AppliedPrice, bar - 14, open, low, high, close)) - (0.0307917433 * PriceSeries(AppliedPrice, bar - 15, open, low, high, close)) - (0.0209443384 * PriceSeries(AppliedPrice, bar - 16, open, low, high, close)) - (0.0102335925 * PriceSeries(AppliedPrice, bar - 17, open, low, high, close)) + (9.32767e-05 * PriceSeries(AppliedPrice, bar - 18, open, low, high, close)) + (0.0089950015 * PriceSeries(AppliedPrice, bar - 19, open, low, high, close)) + (0.0157131144 * PriceSeries(AppliedPrice, bar - 20, open, low, high, close)) + (0.0198149331 * PriceSeries(AppliedPrice, bar - 21, open, low, high, close)) + (0.0211989019 * PriceSeries(AppliedPrice, bar - 22, open, low, high, close)) + (0.0200639819 * PriceSeries(AppliedPrice, bar - 23, open, low, high, close)) + (0.0168532934 * PriceSeries(AppliedPrice, bar - 24, open, low, high, close)) + (0.0121825067 * PriceSeries(AppliedPrice, bar - 25, open, low, high, close)) + (0.0067474241 * PriceSeries(AppliedPrice, bar - 26, open, low, high, close)) + (0.0012444305 * PriceSeries(AppliedPrice, bar - 27, open, low, high, close)) - (0.0037087682 * PriceSeries(AppliedPrice, bar - 28, open, low, high, close)) - (0.0076300416 * PriceSeries(AppliedPrice, bar - 29, open, low, high, close)) - (0.0102110543 * PriceSeries(AppliedPrice, bar - 30, open, low, high, close)) - (0.0113306266 * PriceSeries(AppliedPrice, bar - 31, open, low, high, close)) - (0.0110462105 * PriceSeries(AppliedPrice, bar - 32, open, low, high, close)) - (0.0095662166 * PriceSeries(AppliedPrice, bar - 33, open, low, high, close)) - (0.0072080453 * PriceSeries(AppliedPrice, bar - 34, open, low, high, close)) - (0.0043494435 * PriceSeries(AppliedPrice, bar - 35, open, low, high, close)) - (0.001377197 * PriceSeries(AppliedPrice, bar - 36, open, low, high, close)) + (0.0013575268 * PriceSeries(AppliedPrice, bar - 37, open, low, high, close)) + (0.0035760416 * PriceSeries(AppliedPrice, bar - 38, open, low, high, close)) + (0.0050946166 * PriceSeries(AppliedPrice, bar - 39, open, low, high, close)) + (0.0058339574 * PriceSeries(AppliedPrice, bar - 40, open, low, high, close)) + (0.0058160431 * PriceSeries(AppliedPrice, bar - 41, open, low, high, close)) + (0.0051486631 * PriceSeries(AppliedPrice, bar - 42, open, low, high, close)) + (0.0039984014 * PriceSeries(AppliedPrice, bar - 43, open, low, high, close)) + (0.002561938 * PriceSeries(AppliedPrice, bar - 44, open, low, high, close)) + (0.0010531475 * PriceSeries(AppliedPrice, bar - 45, open, low, high, close)) - (0.0003481453 * PriceSeries(AppliedPrice, bar - 46, open, low, high, close)) - (0.0014937154 * PriceSeries(AppliedPrice, bar - 47, open, low, high, close)) - (0.0022905986 * PriceSeries(AppliedPrice, bar - 48, open, low, high, close)) - (0.0027000514 * PriceSeries(AppliedPrice, bar - 49, open, low, high, close)) - (0.002735908 * PriceSeries(AppliedPrice, bar - 50, open, low, high, close)) - (0.0024543322 * PriceSeries(AppliedPrice, bar - 51, open, low, high, close)) - (0.0019409837 * PriceSeries(AppliedPrice, bar - 52, open, low, high, close)) - (0.0012957482 * PriceSeries(AppliedPrice, bar - 53, open, low, high, close)) - (0.0006179734 * PriceSeries(AppliedPrice, bar - 54, open, low, high, close)) + (5.7542e-06 * PriceSeries(AppliedPrice, bar - 55, open, low, high, close)) + (0.0005111297 * PriceSeries(AppliedPrice, bar - 56, open, low, high, close)) + (0.0008605279 * PriceSeries(AppliedPrice, bar - 57, open, low, high, close)) + (0.0010441921 * PriceSeries(AppliedPrice, bar - 58, open, low, high, close)) + (0.0010775684 * PriceSeries(AppliedPrice, bar - 59, open, low, high, close)) + (0.0009966494 * PriceSeries(AppliedPrice, bar - 60, open, low, high, close)) + (0.00085373 * PriceSeries(AppliedPrice, bar - 61, open, low, high, close)) + (0.0007142855 * PriceSeries(AppliedPrice, bar - 62, open, low, high, close)) + (0.0006599146 * PriceSeries(AppliedPrice, bar - 63, open, low, high, close)) - (0.0008151017 * PriceSeries(AppliedPrice, bar - 64, open, low, high, close))
        slow_dma = (0.0825641231 * PriceSeries(AppliedPrice, bar - 0, open, low, high, close)) + (0.082278308 * PriceSeries(AppliedPrice, bar - 1, open, low, high, close)) + (0.0814249974 * PriceSeries(AppliedPrice, bar - 2, open, low, high, close)) + (0.0800166909 * PriceSeries(AppliedPrice, bar - 3, open, low, high, close)) + (0.0780735197 * PriceSeries(AppliedPrice, bar - 4, open, low, high, close)) + (0.0756232268 * PriceSeries(AppliedPrice, bar - 5, open, low, high, close)) + (0.072700974 * PriceSeries(AppliedPrice, bar - 6, open, low, high, close)) + (0.0693478349 * PriceSeries(AppliedPrice, bar - 7, open, low, high, close)) + (0.0656105823 * PriceSeries(AppliedPrice, bar - 8, open, low, high, close)) + (0.0615409157 * PriceSeries(AppliedPrice, bar - 9, open, low, high, close)) + (0.057193954 * PriceSeries(AppliedPrice, bar - 10, open, low, high, close)) + (0.0526285643 * PriceSeries(AppliedPrice, bar - 11, open, low, high, close)) + (0.0479025123 * PriceSeries(AppliedPrice, bar - 12, open, low, high, close)) + (0.0430785482 * PriceSeries(AppliedPrice, bar - 13, open, low, high, close)) + (0.038215288 * PriceSeries(AppliedPrice, bar - 14, open, low, high, close)) + (0.0333706133 * PriceSeries(AppliedPrice, bar - 15, open, low, high, close)) + (0.028602116 * PriceSeries(AppliedPrice, bar - 16, open, low, high, close)) + (0.0239614376 * PriceSeries(AppliedPrice, bar - 17, open, low, high, close)) + (0.0194972056 * PriceSeries(AppliedPrice, bar - 18, open, low, high, close)) + (0.0152532583 * PriceSeries(AppliedPrice, bar - 19, open, low, high, close)) + (0.0112682658 * PriceSeries(AppliedPrice, bar - 20, open, low, high, close)) + (0.0075745482 * PriceSeries(AppliedPrice, bar - 21, open, low, high, close)) + (0.0041980052 * PriceSeries(AppliedPrice, bar - 22, open, low, high, close)) + (0.0011588603 * PriceSeries(AppliedPrice, bar - 23, open, low, high, close)) - (0.0015292889 * PriceSeries(AppliedPrice, bar - 24, open, low, high, close)) - (0.0038593393 * PriceSeries(AppliedPrice, bar - 25, open, low, high, close)) - (0.0058303888 * PriceSeries(AppliedPrice, bar - 26, open, low, high, close)) - (0.0074473108 * PriceSeries(AppliedPrice, bar - 27, open, low, high, close)) - (0.0087203043 * PriceSeries(AppliedPrice, bar - 28, open, low, high, close)) - (0.0096645874 * PriceSeries(AppliedPrice, bar - 29, open, low, high, close)) - (0.0102995666 * PriceSeries(AppliedPrice, bar - 30, open, low, high, close)) - (0.0106483424 * PriceSeries(AppliedPrice, bar - 31, open, low, high, close)) - (0.0107374524 * PriceSeries(AppliedPrice, bar - 32, open, low, high, close)) - (0.0105952115 * PriceSeries(AppliedPrice, bar - 33, open, low, high, close)) - (0.0102516944 * PriceSeries(AppliedPrice, bar - 34, open, low, high, close)) - (0.0097377645 * PriceSeries(AppliedPrice, bar - 35, open, low, high, close)) - (0.0090838346 * PriceSeries(AppliedPrice, bar - 36, open, low, high, close)) - (0.0083237046 * PriceSeries(AppliedPrice, bar - 37, open, low, high, close)) - (0.0074804382 * PriceSeries(AppliedPrice, bar - 38, open, low, high, close)) - (0.0065902734 * PriceSeries(AppliedPrice, bar - 39, open, low, high, close)) - (0.0056742995 * PriceSeries(AppliedPrice, bar - 40, open, low, high, close)) - (0.0047554314 * PriceSeries(AppliedPrice, bar - 41, open, low, high, close)) - (0.0038574209 * PriceSeries(AppliedPrice, bar - 42, open, low, high, close)) - (0.0029983549 * PriceSeries(AppliedPrice, bar - 43, open, low, high, close)) - (0.0021924972 * PriceSeries(AppliedPrice, bar - 44, open, low, high, close)) - (0.0014513858 * PriceSeries(AppliedPrice, bar - 45, open, low, high, close)) - (0.0007848072 * PriceSeries(AppliedPrice, bar - 46, open, low, high, close)) - (0.0001995891 * PriceSeries(AppliedPrice, bar - 47, open, low, high, close)) + (0.0003009728 * PriceSeries(AppliedPrice, bar - 48, open, low, high, close)) + (0.0007162164 * PriceSeries(AppliedPrice, bar - 49, open, low, high, close)) + (0.0010478905 * PriceSeries(AppliedPrice, bar - 50, open, low, high, close)) + (0.0012994016 * PriceSeries(AppliedPrice, bar - 51, open, low, high, close)) + (0.0014755433 * PriceSeries(AppliedPrice, bar - 52, open, low, high, close)) + (0.0015824007 * PriceSeries(AppliedPrice, bar - 53, open, low, high, close)) + (0.0016272598 * PriceSeries(AppliedPrice, bar - 54, open, low, high, close)) + (0.0016185271 * PriceSeries(AppliedPrice, bar - 55, open, low, high, close)) + (0.0015648336 * PriceSeries(AppliedPrice, bar - 56, open, low, high, close)) + (0.0014747659 * PriceSeries(AppliedPrice, bar - 57, open, low, high, close)) + (0.0013569946 * PriceSeries(AppliedPrice, bar - 58, open, low, high, close)) + (0.0012193896 * PriceSeries(AppliedPrice, bar - 59, open, low, high, close)) + (0.0010695971 * PriceSeries(AppliedPrice, bar - 60, open, low, high, close)) + (0.0009140878 * PriceSeries(AppliedPrice, bar - 61, open, low, high, close)) + (0.000759154 * PriceSeries(AppliedPrice, bar - 62, open, low, high, close)) + (0.0016019033 * PriceSeries(AppliedPrice, bar - 63, open, low, high, close))
        dmacd = _fdiv(fast_dma - slow_dma, Point())
        sign_dma = XMA.XMASeries(min_rates_1, prev_calculated, rates_total, Signal_Method, Signal_Phase, Signal_XMA, dmacd, bar, False)
        DMACDBuffer[bar] = dmacd
        SignBuffer[bar] = sign_dma
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first2
    for bar in range(bar, rates_total):
        clr = 2
        if DMACDBuffer[bar] > 0:
            if DMACDBuffer[bar] > DMACDBuffer[bar - 1]:
                clr = 4
            if DMACDBuffer[bar] < DMACDBuffer[bar - 1]:
                clr = 3
        if DMACDBuffer[bar] < 0:
            if DMACDBuffer[bar] < DMACDBuffer[bar - 1]:
                clr = 0
            if DMACDBuffer[bar] > DMACDBuffer[bar - 1]:
                clr = 1
        ColorDMACDBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first3
    for bar in range(bar, rates_total):
        clr = 1
        if DMACDBuffer[bar] > SignBuffer[bar - 1]:
            clr = 2
        if DMACDBuffer[bar] < SignBuffer[bar - 1]:
            clr = 0
        ColorSignBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA = _alloc(CXMA)
XMA.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DigitalMacd(_MQL5Indicator):
    name = 'digital_macd'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Signal_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Signal line averaging method
        'Signal_XMA': 5,  # Signal line period
        'Signal_Phase': 100,  # Signal line parameter
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # price constant
    }

