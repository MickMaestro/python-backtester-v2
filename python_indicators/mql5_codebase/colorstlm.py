"""colorstlm — converted from MQL5: MQL5 Indicators/ColorSTLM_HTF/colorstlm.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 10, 2: 1}, 'colors': {1: [255, 16711935, 8421504, 8421376, 8388352], 2: [8421504]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 4}, 'labels': {1: 'STLM HISTOGRAM', 2: 'STLM'}, 'levels': [0.0], 'description': [], 'name': 'colorstlm', 'source': 'MQL5 Indicators/ColorSTLM_HTF/colorstlm.mq5', 'folder': 'ColorSTLM_HTF', 'inputs': [{'mql': 'JLength', 'py': 'JLength', 'param': 'JLength', 'type': 'int', 'default': 3, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'JPhase', 'py': 'JPhase', 'param': 'JPhase', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'STLMShift', 'py': 'STLMShift', 'param': 'STLMShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг STLM по горизонтали в барах', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
JLength = _input('JLength', 3)  # Глубина сглаживания
JPhase = _input('JPhase', 100)  # Параметр сглаживания
STLMShift = _input('STLMShift', 0)  # Сдвиг STLM по горизонтали в барах
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
    shortname = 'STLM'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 1)

def OnCalculate(rates_total, prev_calculated, begin, price):
    global _s_OnCalculate_minbar
    if rates_total < (min_rates_total + begin):
        return 0
    first = 0
    bar = 0
    STLM = 0.0
    JSTLM = 0.0
    value1 = 0.0
    value2 = 0.0
    clr = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = STLMPeriod - 1 + begin
        _s_OnCalculate_minbar = first
        if begin > 0:
            PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, begin + min_rates_total)
            PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, begin + min_rates_total)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        value1 = (0.0982862174 * price[bar - 0]) + (0.0975682269 * price[bar - 1]) + (0.0961401078 * price[bar - 2]) + (0.0940230544 * price[bar - 3]) + (0.091243709 * price[bar - 4]) + (0.0878391006 * price[bar - 5]) + (0.0838544303 * price[bar - 6]) + (0.079340635 * price[bar - 7]) + (0.0743569346 * price[bar - 8]) + (0.0689666682 * price[bar - 9]) + (0.0632381578 * price[bar - 10]) + (0.0572428925 * price[bar - 11]) + (0.0510534242 * price[bar - 12]) + (0.0447468229 * price[bar - 13]) + (0.038395995 * price[bar - 14]) + (0.0320735368 * price[bar - 15]) + (0.0258537721 * price[bar - 16]) + (0.0198005183 * price[bar - 17]) + (0.0139807863 * price[bar - 18]) + (0.0084512448 * price[bar - 19]) + (0.0032639979 * price[bar - 20]) - (0.0015350359 * price[bar - 21]) - (0.0059060082 * price[bar - 22]) - (0.0098190256 * price[bar - 23]) - (0.0132507215 * price[bar - 24]) - (0.0161875265 * price[bar - 25]) - (0.0186164872 * price[bar - 26]) - (0.0205446727 * price[bar - 27]) - (0.0219739146 * price[bar - 28]) - (0.0229204861 * price[bar - 29]) - (0.0234080863 * price[bar - 30]) - (0.0234566315 * price[bar - 31]) - (0.0231017777 * price[bar - 32]) - (0.02237969 * price[bar - 33]) - (0.0213300463 * price[bar - 34]) - (0.0199924534 * price[bar - 35]) - (0.0184126992 * price[bar - 36]) - (0.0166377699 * price[bar - 37]) - (0.0147139428 * price[bar - 38]) - (0.0126796776 * price[bar - 39]) - (0.0105938331 * price[bar - 40]) - (0.008473677 * price[bar - 41]) - (0.006384185 * price[bar - 42]) - (0.0043466731 * price[bar - 43]) - (0.0023956944 * price[bar - 44]) - (0.000553518 * price[bar - 45]) + (0.0011421469 * price[bar - 46]) + (0.0026845693 * price[bar - 47]) + (0.0040471369 * price[bar - 48]) + (0.0052380201 * price[bar - 49]) + (0.0062194591 * price[bar - 50]) + (0.0070340085 * price[bar - 51]) + (0.0076266453 * price[bar - 52]) + (0.0080376628 * price[bar - 53]) + (0.0083037666 * price[bar - 54]) + (0.0083694798 * price[bar - 55]) + (0.0082901022 * price[bar - 56]) + (0.0080741359 * price[bar - 57]) + (0.007754382 * price[bar - 58]) + (0.0073260526 * price[bar - 59]) + (0.0068163569 * price[bar - 60]) + (0.0062325477 * price[bar - 61]) + (0.0056078229 * price[bar - 62]) + (0.0049516078 * price[bar - 63]) + (0.0161380976 * price[bar - 64])
        value2 = (-0.0074151919 * price[bar - 0]) - (0.0060698985 * price[bar - 1]) - (0.0044979052 * price[bar - 2]) - (0.0027054278 * price[bar - 3]) - (0.0007031702 * price[bar - 4]) + (0.0014951741 * price[bar - 5]) + (0.0038713513 * price[bar - 6]) + (0.0064043271 * price[bar - 7]) + (0.0090702334 * price[bar - 8]) + (0.0118431116 * price[bar - 9]) + (0.0146922652 * price[bar - 10]) + (0.0175884606 * price[bar - 11]) + (0.0204976517 * price[bar - 12]) + (0.0233865835 * price[bar - 13]) + (0.0262218588 * price[bar - 14]) + (0.0289681736 * price[bar - 15]) + (0.0315922931 * price[bar - 16]) + (0.0340614696 * price[bar - 17]) + (0.0363444061 * price[bar - 18]) + (0.0384120882 * price[bar - 19]) + (0.0402373884 * price[bar - 20]) + (0.0417969735 * price[bar - 21]) + (0.0430701377 * price[bar - 22]) + (0.0440399188 * price[bar - 23]) + (0.0446941124 * price[bar - 24]) + (0.04502301 * price[bar - 25]) + (0.04502301 * price[bar - 26]) + (0.0446941124 * price[bar - 27]) + (0.0440399188 * price[bar - 28]) + (0.0430701377 * price[bar - 29]) + (0.0417969735 * price[bar - 30]) + (0.0402373884 * price[bar - 31]) + (0.0384120882 * price[bar - 32]) + (0.0363444061 * price[bar - 33]) + (0.0340614696 * price[bar - 34]) + (0.0315922931 * price[bar - 35]) + (0.0289681736 * price[bar - 36]) + (0.0262218588 * price[bar - 37]) + (0.0233865835 * price[bar - 38]) + (0.0204976517 * price[bar - 39]) + (0.0175884606 * price[bar - 40]) + (0.0146922652 * price[bar - 41]) + (0.0118431116 * price[bar - 42]) + (0.0090702334 * price[bar - 43]) + (0.0064043271 * price[bar - 44]) + (0.0038713513 * price[bar - 45]) + (0.0014951741 * price[bar - 46]) - (0.0007031702 * price[bar - 47]) - (0.0027054278 * price[bar - 48]) - (0.0044979052 * price[bar - 49]) - (0.0060698985 * price[bar - 50]) - (0.0074151919 * price[bar - 51]) - (0.0085278517 * price[bar - 52]) - (0.0094111161 * price[bar - 53]) - (0.0100658241 * price[bar - 54]) - (0.0104994302 * price[bar - 55]) - (0.0107227904 * price[bar - 56]) - (0.010745028 * price[bar - 57]) - (0.0105824763 * price[bar - 58]) - (0.0102517019 * price[bar - 59]) - (0.0097708805 * price[bar - 60]) - (0.0091581551 * price[bar - 61]) - (0.0084345004 * price[bar - 62]) - (0.0076214397 * price[bar - 63]) - (0.0067401718 * price[bar - 64]) - (0.0058083144 * price[bar - 65]) - (0.0048528295 * price[bar - 66]) - (0.0038816271 * price[bar - 67]) - (0.0029244713 * price[bar - 68]) - (0.0019911267 * price[bar - 69]) - (0.0010974211 * price[bar - 70]) - (0.0002535559 * price[bar - 71]) + (0.0005231953 * price[bar - 72]) + (0.0012297491 * price[bar - 73]) + (0.0018539149 * price[bar - 74]) + (0.0023994354 * price[bar - 75]) + (0.0028490136 * price[bar - 76]) + (0.0032221429 * price[bar - 77]) + (0.0034936183 * price[bar - 78]) + (0.0036818974 * price[bar - 79]) + (0.0038037944 * price[bar - 80]) + (0.0038338964 * price[bar - 81]) + (0.003797535 * price[bar - 82]) + (0.0036986051 * price[bar - 83]) + (0.003552132 * price[bar - 84]) + (0.0033559226 * price[bar - 85]) + (0.0031224409 * price[bar - 86]) + (0.0028550092 * price[bar - 87]) + (0.0025688349 * price[bar - 88]) + (0.0022682355 * price[bar - 89]) + (0.0073925495 * price[bar - 90])
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


class Colorstlm(_MQL5Indicator):
    name = 'colorstlm'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'JLength': 3,  # Глубина сглаживания
        'JPhase': 100,  # Параметр сглаживания
        'STLMShift': 0,  # Сдвиг STLM по горизонтали в барах
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

