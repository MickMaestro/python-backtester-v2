"""ColorSTLM_HISTOGRAM — converted from MQL5: MQL5 Indicators/STLMCandle/ColorSTLM_HISTOGRAM.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 10, 2: 1}, 'colors': {1: [255, 16711935, 8421504, 8421376, 8388352], 2: [8421504]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 4}, 'labels': {1: 'STLM HISTOGRAM', 2: 'STLM'}, 'levels': [0.0], 'description': [], 'name': 'ColorSTLM_HISTOGRAM', 'source': 'MQL5 Indicators/STLMCandle/ColorSTLM_HISTOGRAM.mq5', 'folder': 'STLMCandle', 'inputs': [{'mql': 'JLength', 'py': 'JLength', 'param': 'JLength', 'type': 'int', 'default': 3, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'JPhase', 'py': 'JPhase', 'param': 'JPhase', 'type': 'int', 'default': 100, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 7, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'STLMShift', 'py': 'STLMShift', 'param': 'STLMShift', 'type': 'int', 'default': 0, 'label': 'сдвиг STLM по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
JLength = _input('JLength', 3)  # глубина сглаживания
JPhase = _input('JPhase', 100)  # параметр сглаживания,
IPC = _input('IPC', PRICE_WEIGHTED_)  # ценовая константа
STLMShift = _input('STLMShift', 0)  # сдвиг STLM по горизонтали в барах
STLMPeriod = 91
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
IndBuffer_ = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = STLMPeriod + 1 + 30
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, IndBuffer_, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, STLMPeriod)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, STLMPeriod)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = 'ColorSTLM_HISTOGRAM'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_minbar
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    STLM = 0.0
    JSTLM = 0.0
    value1 = 0.0
    value2 = 0.0
    clr = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = STLMPeriod - 1
        _s_OnCalculate_minbar = first
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        value1 = (0.0982862174 * PriceSeries(IPC, bar - 0, open, low, high, close)) + (0.0975682269 * PriceSeries(IPC, bar - 1, open, low, high, close)) + (0.0961401078 * PriceSeries(IPC, bar - 2, open, low, high, close)) + (0.0940230544 * PriceSeries(IPC, bar - 3, open, low, high, close)) + (0.091243709 * PriceSeries(IPC, bar - 4, open, low, high, close)) + (0.0878391006 * PriceSeries(IPC, bar - 5, open, low, high, close)) + (0.0838544303 * PriceSeries(IPC, bar - 6, open, low, high, close)) + (0.079340635 * PriceSeries(IPC, bar - 7, open, low, high, close)) + (0.0743569346 * PriceSeries(IPC, bar - 8, open, low, high, close)) + (0.0689666682 * PriceSeries(IPC, bar - 9, open, low, high, close)) + (0.0632381578 * PriceSeries(IPC, bar - 10, open, low, high, close)) + (0.0572428925 * PriceSeries(IPC, bar - 11, open, low, high, close)) + (0.0510534242 * PriceSeries(IPC, bar - 12, open, low, high, close)) + (0.0447468229 * PriceSeries(IPC, bar - 13, open, low, high, close)) + (0.038395995 * PriceSeries(IPC, bar - 14, open, low, high, close)) + (0.0320735368 * PriceSeries(IPC, bar - 15, open, low, high, close)) + (0.0258537721 * PriceSeries(IPC, bar - 16, open, low, high, close)) + (0.0198005183 * PriceSeries(IPC, bar - 17, open, low, high, close)) + (0.0139807863 * PriceSeries(IPC, bar - 18, open, low, high, close)) + (0.0084512448 * PriceSeries(IPC, bar - 19, open, low, high, close)) + (0.0032639979 * PriceSeries(IPC, bar - 20, open, low, high, close)) - (0.0015350359 * PriceSeries(IPC, bar - 21, open, low, high, close)) - (0.0059060082 * PriceSeries(IPC, bar - 22, open, low, high, close)) - (0.0098190256 * PriceSeries(IPC, bar - 23, open, low, high, close)) - (0.0132507215 * PriceSeries(IPC, bar - 24, open, low, high, close)) - (0.0161875265 * PriceSeries(IPC, bar - 25, open, low, high, close)) - (0.0186164872 * PriceSeries(IPC, bar - 26, open, low, high, close)) - (0.0205446727 * PriceSeries(IPC, bar - 27, open, low, high, close)) - (0.0219739146 * PriceSeries(IPC, bar - 28, open, low, high, close)) - (0.0229204861 * PriceSeries(IPC, bar - 29, open, low, high, close)) - (0.0234080863 * PriceSeries(IPC, bar - 30, open, low, high, close)) - (0.0234566315 * PriceSeries(IPC, bar - 31, open, low, high, close)) - (0.0231017777 * PriceSeries(IPC, bar - 32, open, low, high, close)) - (0.02237969 * PriceSeries(IPC, bar - 33, open, low, high, close)) - (0.0213300463 * PriceSeries(IPC, bar - 34, open, low, high, close)) - (0.0199924534 * PriceSeries(IPC, bar - 35, open, low, high, close)) - (0.0184126992 * PriceSeries(IPC, bar - 36, open, low, high, close)) - (0.0166377699 * PriceSeries(IPC, bar - 37, open, low, high, close)) - (0.0147139428 * PriceSeries(IPC, bar - 38, open, low, high, close)) - (0.0126796776 * PriceSeries(IPC, bar - 39, open, low, high, close)) - (0.0105938331 * PriceSeries(IPC, bar - 40, open, low, high, close)) - (0.008473677 * PriceSeries(IPC, bar - 41, open, low, high, close)) - (0.006384185 * PriceSeries(IPC, bar - 42, open, low, high, close)) - (0.0043466731 * PriceSeries(IPC, bar - 43, open, low, high, close)) - (0.0023956944 * PriceSeries(IPC, bar - 44, open, low, high, close)) - (0.000553518 * PriceSeries(IPC, bar - 45, open, low, high, close)) + (0.0011421469 * PriceSeries(IPC, bar - 46, open, low, high, close)) + (0.0026845693 * PriceSeries(IPC, bar - 47, open, low, high, close)) + (0.0040471369 * PriceSeries(IPC, bar - 48, open, low, high, close)) + (0.0052380201 * PriceSeries(IPC, bar - 49, open, low, high, close)) + (0.0062194591 * PriceSeries(IPC, bar - 50, open, low, high, close)) + (0.0070340085 * PriceSeries(IPC, bar - 51, open, low, high, close)) + (0.0076266453 * PriceSeries(IPC, bar - 52, open, low, high, close)) + (0.0080376628 * PriceSeries(IPC, bar - 53, open, low, high, close)) + (0.0083037666 * PriceSeries(IPC, bar - 54, open, low, high, close)) + (0.0083694798 * PriceSeries(IPC, bar - 55, open, low, high, close)) + (0.0082901022 * PriceSeries(IPC, bar - 56, open, low, high, close)) + (0.0080741359 * PriceSeries(IPC, bar - 57, open, low, high, close)) + (0.007754382 * PriceSeries(IPC, bar - 58, open, low, high, close)) + (0.0073260526 * PriceSeries(IPC, bar - 59, open, low, high, close)) + (0.0068163569 * PriceSeries(IPC, bar - 60, open, low, high, close)) + (0.0062325477 * PriceSeries(IPC, bar - 61, open, low, high, close)) + (0.0056078229 * PriceSeries(IPC, bar - 62, open, low, high, close)) + (0.0049516078 * PriceSeries(IPC, bar - 63, open, low, high, close)) + (0.0161380976 * PriceSeries(IPC, bar - 64, open, low, high, close))
        value2 = (-0.0074151919 * PriceSeries(IPC, bar - 0, open, low, high, close)) - (0.0060698985 * PriceSeries(IPC, bar - 1, open, low, high, close)) - (0.0044979052 * PriceSeries(IPC, bar - 2, open, low, high, close)) - (0.0027054278 * PriceSeries(IPC, bar - 3, open, low, high, close)) - (0.0007031702 * PriceSeries(IPC, bar - 4, open, low, high, close)) + (0.0014951741 * PriceSeries(IPC, bar - 5, open, low, high, close)) + (0.0038713513 * PriceSeries(IPC, bar - 6, open, low, high, close)) + (0.0064043271 * PriceSeries(IPC, bar - 7, open, low, high, close)) + (0.0090702334 * PriceSeries(IPC, bar - 8, open, low, high, close)) + (0.0118431116 * PriceSeries(IPC, bar - 9, open, low, high, close)) + (0.0146922652 * PriceSeries(IPC, bar - 10, open, low, high, close)) + (0.0175884606 * PriceSeries(IPC, bar - 11, open, low, high, close)) + (0.0204976517 * PriceSeries(IPC, bar - 12, open, low, high, close)) + (0.0233865835 * PriceSeries(IPC, bar - 13, open, low, high, close)) + (0.0262218588 * PriceSeries(IPC, bar - 14, open, low, high, close)) + (0.0289681736 * PriceSeries(IPC, bar - 15, open, low, high, close)) + (0.0315922931 * PriceSeries(IPC, bar - 16, open, low, high, close)) + (0.0340614696 * PriceSeries(IPC, bar - 17, open, low, high, close)) + (0.0363444061 * PriceSeries(IPC, bar - 18, open, low, high, close)) + (0.0384120882 * PriceSeries(IPC, bar - 19, open, low, high, close)) + (0.0402373884 * PriceSeries(IPC, bar - 20, open, low, high, close)) + (0.0417969735 * PriceSeries(IPC, bar - 21, open, low, high, close)) + (0.0430701377 * PriceSeries(IPC, bar - 22, open, low, high, close)) + (0.0440399188 * PriceSeries(IPC, bar - 23, open, low, high, close)) + (0.0446941124 * PriceSeries(IPC, bar - 24, open, low, high, close)) + (0.04502301 * PriceSeries(IPC, bar - 25, open, low, high, close)) + (0.04502301 * PriceSeries(IPC, bar - 26, open, low, high, close)) + (0.0446941124 * PriceSeries(IPC, bar - 27, open, low, high, close)) + (0.0440399188 * PriceSeries(IPC, bar - 28, open, low, high, close)) + (0.0430701377 * PriceSeries(IPC, bar - 29, open, low, high, close)) + (0.0417969735 * PriceSeries(IPC, bar - 30, open, low, high, close)) + (0.0402373884 * PriceSeries(IPC, bar - 31, open, low, high, close)) + (0.0384120882 * PriceSeries(IPC, bar - 32, open, low, high, close)) + (0.0363444061 * PriceSeries(IPC, bar - 33, open, low, high, close)) + (0.0340614696 * PriceSeries(IPC, bar - 34, open, low, high, close)) + (0.0315922931 * PriceSeries(IPC, bar - 35, open, low, high, close)) + (0.0289681736 * PriceSeries(IPC, bar - 36, open, low, high, close)) + (0.0262218588 * PriceSeries(IPC, bar - 37, open, low, high, close)) + (0.0233865835 * PriceSeries(IPC, bar - 38, open, low, high, close)) + (0.0204976517 * PriceSeries(IPC, bar - 39, open, low, high, close)) + (0.0175884606 * PriceSeries(IPC, bar - 40, open, low, high, close)) + (0.0146922652 * PriceSeries(IPC, bar - 41, open, low, high, close)) + (0.0118431116 * PriceSeries(IPC, bar - 42, open, low, high, close)) + (0.0090702334 * PriceSeries(IPC, bar - 43, open, low, high, close)) + (0.0064043271 * PriceSeries(IPC, bar - 44, open, low, high, close)) + (0.0038713513 * PriceSeries(IPC, bar - 45, open, low, high, close)) + (0.0014951741 * PriceSeries(IPC, bar - 46, open, low, high, close)) - (0.0007031702 * PriceSeries(IPC, bar - 47, open, low, high, close)) - (0.0027054278 * PriceSeries(IPC, bar - 48, open, low, high, close)) - (0.0044979052 * PriceSeries(IPC, bar - 49, open, low, high, close)) - (0.0060698985 * PriceSeries(IPC, bar - 50, open, low, high, close)) - (0.0074151919 * PriceSeries(IPC, bar - 51, open, low, high, close)) - (0.0085278517 * PriceSeries(IPC, bar - 52, open, low, high, close)) - (0.0094111161 * PriceSeries(IPC, bar - 53, open, low, high, close)) - (0.0100658241 * PriceSeries(IPC, bar - 54, open, low, high, close)) - (0.0104994302 * PriceSeries(IPC, bar - 55, open, low, high, close)) - (0.0107227904 * PriceSeries(IPC, bar - 56, open, low, high, close)) - (0.010745028 * PriceSeries(IPC, bar - 57, open, low, high, close)) - (0.0105824763 * PriceSeries(IPC, bar - 58, open, low, high, close)) - (0.0102517019 * PriceSeries(IPC, bar - 59, open, low, high, close)) - (0.0097708805 * PriceSeries(IPC, bar - 60, open, low, high, close)) - (0.0091581551 * PriceSeries(IPC, bar - 61, open, low, high, close)) - (0.0084345004 * PriceSeries(IPC, bar - 62, open, low, high, close)) - (0.0076214397 * PriceSeries(IPC, bar - 63, open, low, high, close)) - (0.0067401718 * PriceSeries(IPC, bar - 64, open, low, high, close)) - (0.0058083144 * PriceSeries(IPC, bar - 65, open, low, high, close)) - (0.0048528295 * PriceSeries(IPC, bar - 66, open, low, high, close)) - (0.0038816271 * PriceSeries(IPC, bar - 67, open, low, high, close)) - (0.0029244713 * PriceSeries(IPC, bar - 68, open, low, high, close)) - (0.0019911267 * PriceSeries(IPC, bar - 69, open, low, high, close)) - (0.0010974211 * PriceSeries(IPC, bar - 70, open, low, high, close)) - (0.0002535559 * PriceSeries(IPC, bar - 71, open, low, high, close)) + (0.0005231953 * PriceSeries(IPC, bar - 72, open, low, high, close)) + (0.0012297491 * PriceSeries(IPC, bar - 73, open, low, high, close)) + (0.0018539149 * PriceSeries(IPC, bar - 74, open, low, high, close)) + (0.0023994354 * PriceSeries(IPC, bar - 75, open, low, high, close)) + (0.0028490136 * PriceSeries(IPC, bar - 76, open, low, high, close)) + (0.0032221429 * PriceSeries(IPC, bar - 77, open, low, high, close)) + (0.0034936183 * PriceSeries(IPC, bar - 78, open, low, high, close)) + (0.0036818974 * PriceSeries(IPC, bar - 79, open, low, high, close)) + (0.0038037944 * PriceSeries(IPC, bar - 80, open, low, high, close)) + (0.0038338964 * PriceSeries(IPC, bar - 81, open, low, high, close)) + (0.003797535 * PriceSeries(IPC, bar - 82, open, low, high, close)) + (0.0036986051 * PriceSeries(IPC, bar - 83, open, low, high, close)) + (0.003552132 * PriceSeries(IPC, bar - 84, open, low, high, close)) + (0.0033559226 * PriceSeries(IPC, bar - 85, open, low, high, close)) + (0.0031224409 * PriceSeries(IPC, bar - 86, open, low, high, close)) + (0.0028550092 * PriceSeries(IPC, bar - 87, open, low, high, close)) + (0.0025688349 * PriceSeries(IPC, bar - 88, open, low, high, close)) + (0.0022682355 * PriceSeries(IPC, bar - 89, open, low, high, close)) + (0.0073925495 * PriceSeries(IPC, bar - 90, open, low, high, close))
        STLM = value1 - value2
        JSTLM = _s_OnCalculate_JMA.JJMASeries(_s_OnCalculate_minbar, prev_calculated, rates_total, 0, JPhase, JLength, STLM, bar, False)
        IndBuffer[bar] = JSTLM
        IndBuffer_[bar] = JSTLM
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        clr = 2.0
        if IndBuffer[bar] > 0:
            if IndBuffer[bar - 1] > IndBuffer[bar]:
                clr = 3.0
            else:
                clr = 4.0
        if IndBuffer[bar] < 0:
            if IndBuffer[bar - 1] < IndBuffer[bar]:
                clr = 1.0
            else:
                clr = 0.0
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_minbar = 0
_s_OnCalculate_JMA = CJJMA()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorSTLMHISTOGRAM(_MQL5Indicator):
    name = 'ColorSTLM_HISTOGRAM'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'JLength': 3,  # глубина сглаживания
        'JPhase': 100,  # параметр сглаживания,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=7),  # ценовая константа
        'STLMShift': 0,  # сдвиг STLM по горизонтали в барах
    }

