"""Dtm — converted from MQL5: MQL5 Indicators/Dtm_HTF/Dtm.mq5

Copyright: Copyright 2002, Finware.ru Ltd.; Link: http://www.forex-instruments.info; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2002, Finware.ru Ltd.', 'link': 'http://www.forex-instruments.info', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [8421376, 55295]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Dtm'}, 'levels': [0.0], 'description': [], 'name': 'Dtm', 'source': 'MQL5 Indicators/Dtm_HTF/Dtm.mq5', 'folder': 'Dtm_HTF', 'inputs': [{'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
FTLMBuffer = Arr(0, 0.0)
STLMBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 84 + 1
    SetIndexBuffer(0, FTLMBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, STLMBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'Dtm(', EnumToString(IPC, 'ENUM_APPLIED_PRICE_'), ',', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 5)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    value1 = 0.0
    value2 = 0.0
    value3 = 0.0
    value4 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total + 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        value1 = (0.112952 * PriceSeries(IPC, bar - 0, open, low, high, close)) + (0.111644 * PriceSeries(IPC, bar - 1, open, low, high, close)) + (0.109058 * PriceSeries(IPC, bar - 2, open, low, high, close)) + (0.105254 * PriceSeries(IPC, bar - 3, open, low, high, close)) + (0.10032 * PriceSeries(IPC, bar - 4, open, low, high, close)) + (0.094368 * PriceSeries(IPC, bar - 5, open, low, high, close)) + (0.087532 * PriceSeries(IPC, bar - 6, open, low, high, close)) + (0.079966 * PriceSeries(IPC, bar - 7, open, low, high, close)) + (0.071834 * PriceSeries(IPC, bar - 8, open, low, high, close)) + (0.063313 * PriceSeries(IPC, bar - 9, open, low, high, close)) + (0.054575 * PriceSeries(IPC, bar - 10, open, low, high, close)) + (0.045801 * PriceSeries(IPC, bar - 11, open, low, high, close)) + (0.037159 * PriceSeries(IPC, bar - 12, open, low, high, close)) + (0.028809 * PriceSeries(IPC, bar - 13, open, low, high, close)) + (0.020898 * PriceSeries(IPC, bar - 14, open, low, high, close)) + (0.013548 * PriceSeries(IPC, bar - 15, open, low, high, close)) + (0.00687 * PriceSeries(IPC, bar - 16, open, low, high, close)) + (0.000944 * PriceSeries(IPC, bar - 17, open, low, high, close)) - (0.004166 * PriceSeries(IPC, bar - 18, open, low, high, close)) - (0.008428 * PriceSeries(IPC, bar - 19, open, low, high, close)) - (0.011828 * PriceSeries(IPC, bar - 20, open, low, high, close)) - (0.014378 * PriceSeries(IPC, bar - 21, open, low, high, close)) - (0.016112 * PriceSeries(IPC, bar - 22, open, low, high, close)) - (0.01708 * PriceSeries(IPC, bar - 23, open, low, high, close)) - (0.017348 * PriceSeries(IPC, bar - 24, open, low, high, close)) - (0.016998 * PriceSeries(IPC, bar - 25, open, low, high, close)) - (0.016118 * PriceSeries(IPC, bar - 26, open, low, high, close)) - (0.014806 * PriceSeries(IPC, bar - 27, open, low, high, close)) - (0.013156 * PriceSeries(IPC, bar - 28, open, low, high, close)) - (0.01127 * PriceSeries(IPC, bar - 29, open, low, high, close)) - (0.009238 * PriceSeries(IPC, bar - 30, open, low, high, close)) - (0.007152 * PriceSeries(IPC, bar - 31, open, low, high, close)) - (0.00509 * PriceSeries(IPC, bar - 32, open, low, high, close)) - (0.00312 * PriceSeries(IPC, bar - 33, open, low, high, close)) - (0.001302 * PriceSeries(IPC, bar - 34, open, low, high, close)) + (0.000322 * PriceSeries(IPC, bar - 35, open, low, high, close)) + (0.001714 * PriceSeries(IPC, bar - 36, open, low, high, close)) + (0.002858 * PriceSeries(IPC, bar - 37, open, low, high, close)) + (0.003744 * PriceSeries(IPC, bar - 38, open, low, high, close)) + (0.004372 * PriceSeries(IPC, bar - 39, open, low, high, close)) + (0.004754 * PriceSeries(IPC, bar - 40, open, low, high, close)) + (0.00491 * PriceSeries(IPC, bar - 41, open, low, high, close)) + (0.004864 * PriceSeries(IPC, bar - 42, open, low, high, close)) + (0.004646 * PriceSeries(IPC, bar - 43, open, low, high, close)) + (0.004288 * PriceSeries(IPC, bar - 44, open, low, high, close)) + (0.003824 * PriceSeries(IPC, bar - 45, open, low, high, close)) + (0.003288 * PriceSeries(IPC, bar - 46, open, low, high, close)) + (0.002712 * PriceSeries(IPC, bar - 47, open, low, high, close)) + (0.002124 * PriceSeries(IPC, bar - 48, open, low, high, close)) + (0.001548 * PriceSeries(IPC, bar - 49, open, low, high, close)) + (0.00101 * PriceSeries(IPC, bar - 50, open, low, high, close)) + (0.000522 * PriceSeries(IPC, bar - 51, open, low, high, close)) + (9.8e-05 * PriceSeries(IPC, bar - 52, open, low, high, close)) - (0.000254 * PriceSeries(IPC, bar - 53, open, low, high, close)) - (0.00053 * PriceSeries(IPC, bar - 54, open, low, high, close)) - (0.000734 * PriceSeries(IPC, bar - 55, open, low, high, close)) - (0.000866 * PriceSeries(IPC, bar - 56, open, low, high, close)) - (0.000934 * PriceSeries(IPC, bar - 57, open, low, high, close)) - (0.000948 * PriceSeries(IPC, bar - 58, open, low, high, close)) - (0.000914 * PriceSeries(IPC, bar - 59, open, low, high, close)) - (0.000844 * PriceSeries(IPC, bar - 60, open, low, high, close)) - (0.00075 * PriceSeries(IPC, bar - 61, open, low, high, close)) - (0.000638 * PriceSeries(IPC, bar - 62, open, low, high, close)) - (0.00052 * PriceSeries(IPC, bar - 63, open, low, high, close)) - (0.000922 * PriceSeries(IPC, bar - 64, open, low, high, close))
        value2 = (0.038953 * PriceSeries(IPC, bar - 0, open, low, high, close)) + (0.042502 * PriceSeries(IPC, bar - 1, open, low, high, close)) + (0.045773 * PriceSeries(IPC, bar - 2, open, low, high, close)) + (0.048702 * PriceSeries(IPC, bar - 3, open, low, high, close)) + (0.051237 * PriceSeries(IPC, bar - 4, open, low, high, close)) + (0.053326 * PriceSeries(IPC, bar - 5, open, low, high, close)) + (0.054931 * PriceSeries(IPC, bar - 6, open, low, high, close)) + (0.056018 * PriceSeries(IPC, bar - 7, open, low, high, close)) + (0.056566 * PriceSeries(IPC, bar - 8, open, low, high, close)) + (0.056566 * PriceSeries(IPC, bar - 9, open, low, high, close)) + (0.056018 * PriceSeries(IPC, bar - 10, open, low, high, close)) + (0.054931 * PriceSeries(IPC, bar - 11, open, low, high, close)) + (0.053326 * PriceSeries(IPC, bar - 12, open, low, high, close)) + (0.051237 * PriceSeries(IPC, bar - 13, open, low, high, close)) + (0.048702 * PriceSeries(IPC, bar - 14, open, low, high, close)) + (0.045773 * PriceSeries(IPC, bar - 15, open, low, high, close)) + (0.042502 * PriceSeries(IPC, bar - 16, open, low, high, close)) + (0.038953 * PriceSeries(IPC, bar - 17, open, low, high, close)) + (0.03519 * PriceSeries(IPC, bar - 18, open, low, high, close)) + (0.031281 * PriceSeries(IPC, bar - 19, open, low, high, close)) + (0.027295 * PriceSeries(IPC, bar - 20, open, low, high, close)) + (0.023298 * PriceSeries(IPC, bar - 21, open, low, high, close)) + (0.019357 * PriceSeries(IPC, bar - 22, open, low, high, close)) + (0.015532 * PriceSeries(IPC, bar - 23, open, low, high, close)) + (0.01188 * PriceSeries(IPC, bar - 24, open, low, high, close)) + (0.008451 * PriceSeries(IPC, bar - 25, open, low, high, close)) + (0.005287 * PriceSeries(IPC, bar - 26, open, low, high, close)) + (0.002424 * PriceSeries(IPC, bar - 27, open, low, high, close)) - (0.000112 * PriceSeries(IPC, bar - 28, open, low, high, close)) - (0.002305 * PriceSeries(IPC, bar - 29, open, low, high, close)) - (0.004142 * PriceSeries(IPC, bar - 30, open, low, high, close)) - (0.005624 * PriceSeries(IPC, bar - 31, open, low, high, close)) - (0.006758 * PriceSeries(IPC, bar - 32, open, low, high, close)) - (0.007558 * PriceSeries(IPC, bar - 33, open, low, high, close)) - (0.008042 * PriceSeries(IPC, bar - 34, open, low, high, close)) - (0.00824 * PriceSeries(IPC, bar - 35, open, low, high, close)) - (0.008177 * PriceSeries(IPC, bar - 36, open, low, high, close)) - (0.00789 * PriceSeries(IPC, bar - 37, open, low, high, close)) - (0.007415 * PriceSeries(IPC, bar - 38, open, low, high, close)) - (0.006786 * PriceSeries(IPC, bar - 39, open, low, high, close)) - (0.006041 * PriceSeries(IPC, bar - 40, open, low, high, close)) - (0.005219 * PriceSeries(IPC, bar - 41, open, low, high, close)) - (0.004349 * PriceSeries(IPC, bar - 42, open, low, high, close)) - (0.003466 * PriceSeries(IPC, bar - 43, open, low, high, close)) - (0.002596 * PriceSeries(IPC, bar - 44, open, low, high, close)) - (0.001764 * PriceSeries(IPC, bar - 45, open, low, high, close)) - (0.000991 * PriceSeries(IPC, bar - 46, open, low, high, close)) - (0.000294 * PriceSeries(IPC, bar - 47, open, low, high, close)) + (0.000318 * PriceSeries(IPC, bar - 48, open, low, high, close)) + (0.000835 * PriceSeries(IPC, bar - 49, open, low, high, close)) + (0.001254 * PriceSeries(IPC, bar - 50, open, low, high, close)) + (0.001575 * PriceSeries(IPC, bar - 51, open, low, high, close)) + (0.001801 * PriceSeries(IPC, bar - 52, open, low, high, close)) + (0.001937 * PriceSeries(IPC, bar - 53, open, low, high, close)) + (0.001993 * PriceSeries(IPC, bar - 54, open, low, high, close)) + (0.001978 * PriceSeries(IPC, bar - 55, open, low, high, close)) + (0.001902 * PriceSeries(IPC, bar - 56, open, low, high, close)) + (0.001777 * PriceSeries(IPC, bar - 57, open, low, high, close)) + (0.001616 * PriceSeries(IPC, bar - 58, open, low, high, close)) + (0.001428 * PriceSeries(IPC, bar - 59, open, low, high, close)) + (0.001228 * PriceSeries(IPC, bar - 60, open, low, high, close)) + (0.00102 * PriceSeries(IPC, bar - 61, open, low, high, close)) + (0.000816 * PriceSeries(IPC, bar - 62, open, low, high, close)) + (0.000622 * PriceSeries(IPC, bar - 63, open, low, high, close)) + (0.000445 * PriceSeries(IPC, bar - 64, open, low, high, close)) + (0.000287 * PriceSeries(IPC, bar - 65, open, low, high, close)) + (0.000154 * PriceSeries(IPC, bar - 66, open, low, high, close)) + (4.5e-05 * PriceSeries(IPC, bar - 67, open, low, high, close)) - (4e-05 * PriceSeries(IPC, bar - 68, open, low, high, close)) - (0.0001 * PriceSeries(IPC, bar - 69, open, low, high, close)) - (0.000139 * PriceSeries(IPC, bar - 70, open, low, high, close)) - (0.000159 * PriceSeries(IPC, bar - 71, open, low, high, close)) - (0.000161 * PriceSeries(IPC, bar - 72, open, low, high, close)) - (0.000672 * PriceSeries(IPC, bar - 73, open, low, high, close))
        value3 = (0.0729811286 * PriceSeries(IPC, bar - 0, open, low, high, close)) + (0.072783929 * PriceSeries(IPC, bar - 1, open, low, high, close)) + (0.0721970455 * PriceSeries(IPC, bar - 2, open, low, high, close)) + (0.0712248998 * PriceSeries(IPC, bar - 3, open, low, high, close)) + (0.0698810899 * PriceSeries(IPC, bar - 4, open, low, high, close)) + (0.0681787637 * PriceSeries(IPC, bar - 5, open, low, high, close)) + (0.0661384062 * PriceSeries(IPC, bar - 6, open, low, high, close)) + (0.0637836328 * PriceSeries(IPC, bar - 7, open, low, high, close)) + (0.0611379416 * PriceSeries(IPC, bar - 8, open, low, high, close)) + (0.058232872 * PriceSeries(IPC, bar - 9, open, low, high, close)) + (0.0551006677 * PriceSeries(IPC, bar - 10, open, low, high, close)) + (0.0517729856 * PriceSeries(IPC, bar - 11, open, low, high, close)) + (0.048286452 * PriceSeries(IPC, bar - 12, open, low, high, close)) + (0.0446761673 * PriceSeries(IPC, bar - 13, open, low, high, close)) + (0.0409807341 * PriceSeries(IPC, bar - 14, open, low, high, close)) + (0.0372349199 * PriceSeries(IPC, bar - 15, open, low, high, close)) + (0.0334766035 * PriceSeries(IPC, bar - 16, open, low, high, close)) + (0.0297389677 * PriceSeries(IPC, bar - 17, open, low, high, close)) + (0.0260572889 * PriceSeries(IPC, bar - 18, open, low, high, close)) + (0.02246205 * PriceSeries(IPC, bar - 19, open, low, high, close)) + (0.0189846476 * PriceSeries(IPC, bar - 20, open, low, high, close)) + (0.0156508337 * PriceSeries(IPC, bar - 21, open, low, high, close)) + (0.0124844115 * PriceSeries(IPC, bar - 22, open, low, high, close)) + (0.0095064451 * PriceSeries(IPC, bar - 23, open, low, high, close)) + (0.0067348956 * PriceSeries(IPC, bar - 24, open, low, high, close)) + (0.0041825353 * PriceSeries(IPC, bar - 25, open, low, high, close)) + (0.0018620649 * PriceSeries(IPC, bar - 26, open, low, high, close)) - (0.0002214306 * PriceSeries(IPC, bar - 27, open, low, high, close)) - (0.0020618579 * PriceSeries(IPC, bar - 28, open, low, high, close)) - (0.0036612349 * PriceSeries(IPC, bar - 29, open, low, high, close)) - (0.0050199184 * PriceSeries(IPC, bar - 30, open, low, high, close)) - (0.0061460477 * PriceSeries(IPC, bar - 31, open, low, high, close)) - (0.0070453847 * PriceSeries(IPC, bar - 32, open, low, high, close)) - (0.0077311361 * PriceSeries(IPC, bar - 33, open, low, high, close)) - (0.0082154598 * PriceSeries(IPC, bar - 34, open, low, high, close)) - (0.0085069196 * PriceSeries(IPC, bar - 35, open, low, high, close)) - (0.0086364464 * PriceSeries(IPC, bar - 36, open, low, high, close)) - (0.0086063959 * PriceSeries(IPC, bar - 37, open, low, high, close)) - (0.0084385053 * PriceSeries(IPC, bar - 38, open, low, high, close)) - (0.0081544217 * PriceSeries(IPC, bar - 39, open, low, high, close)) - (0.0077720532 * PriceSeries(IPC, bar - 40, open, low, high, close)) - (0.0073096701 * PriceSeries(IPC, bar - 41, open, low, high, close)) - (0.0067829639 * PriceSeries(IPC, bar - 42, open, low, high, close)) - (0.0062100031 * PriceSeries(IPC, bar - 43, open, low, high, close)) - (0.0056056555 * PriceSeries(IPC, bar - 44, open, low, high, close)) - (0.0049866671 * PriceSeries(IPC, bar - 45, open, low, high, close)) - (0.0043657084 * PriceSeries(IPC, bar - 46, open, low, high, close)) - (0.0037560684 * PriceSeries(IPC, bar - 47, open, low, high, close)) - (0.0031670013 * PriceSeries(IPC, bar - 48, open, low, high, close)) - (0.0026079202 * PriceSeries(IPC, bar - 49, open, low, high, close)) - (0.0020858529 * PriceSeries(IPC, bar - 50, open, low, high, close)) - (0.001606464 * PriceSeries(IPC, bar - 51, open, low, high, close)) - (0.0011734916 * PriceSeries(IPC, bar - 52, open, low, high, close)) - (0.0007908741 * PriceSeries(IPC, bar - 53, open, low, high, close)) - (0.0004588212 * PriceSeries(IPC, bar - 54, open, low, high, close)) - (0.000179039 * PriceSeries(IPC, bar - 55, open, low, high, close)) + (5.10113e-05 * PriceSeries(IPC, bar - 56, open, low, high, close)) + (0.0002315881 * PriceSeries(IPC, bar - 57, open, low, high, close)) + (0.0003671215 * PriceSeries(IPC, bar - 58, open, low, high, close)) + (0.0004595615 * PriceSeries(IPC, bar - 59, open, low, high, close)) + (0.0005144014 * PriceSeries(IPC, bar - 60, open, low, high, close)) + (0.0005345365 * PriceSeries(IPC, bar - 61, open, low, high, close)) + (0.0005256791 * PriceSeries(IPC, bar - 62, open, low, high, close)) + (0.002887134 * PriceSeries(IPC, bar - 63, open, low, high, close))
        value4 = (0.0077174463 * PriceSeries(IPC, bar - 0, open, low, high, close)) + (0.0093613543 * PriceSeries(IPC, bar - 1, open, low, high, close)) + (0.0110760659 * PriceSeries(IPC, bar - 2, open, low, high, close)) + (0.0128488828 * PriceSeries(IPC, bar - 3, open, low, high, close)) + (0.0146643234 * PriceSeries(IPC, bar - 4, open, low, high, close)) + (0.0165073564 * PriceSeries(IPC, bar - 5, open, low, high, close)) + (0.0183605871 * PriceSeries(IPC, bar - 6, open, low, high, close)) + (0.0202076529 * PriceSeries(IPC, bar - 7, open, low, high, close)) + (0.0220298758 * PriceSeries(IPC, bar - 8, open, low, high, close)) + (0.0238101118 * PriceSeries(IPC, bar - 9, open, low, high, close)) + (0.025529326 * PriceSeries(IPC, bar - 10, open, low, high, close)) + (0.0271702104 * PriceSeries(IPC, bar - 11, open, low, high, close)) + (0.0287147044 * PriceSeries(IPC, bar - 12, open, low, high, close)) + (0.030147198 * PriceSeries(IPC, bar - 13, open, low, high, close)) + (0.0314517917 * PriceSeries(IPC, bar - 14, open, low, high, close)) + (0.0326129335 * PriceSeries(IPC, bar - 15, open, low, high, close)) + (0.0336190364 * PriceSeries(IPC, bar - 16, open, low, high, close)) + (0.0344584557 * PriceSeries(IPC, bar - 17, open, low, high, close)) + (0.0351210901 * PriceSeries(IPC, bar - 18, open, low, high, close)) + (0.0356004564 * PriceSeries(IPC, bar - 19, open, low, high, close)) + (0.0358898494 * PriceSeries(IPC, bar - 20, open, low, high, close)) + (0.0359870888 * PriceSeries(IPC, bar - 21, open, low, high, close)) + (0.0358898494 * PriceSeries(IPC, bar - 22, open, low, high, close)) + (0.0356004564 * PriceSeries(IPC, bar - 23, open, low, high, close)) + (0.0351210901 * PriceSeries(IPC, bar - 24, open, low, high, close)) + (0.0344584557 * PriceSeries(IPC, bar - 25, open, low, high, close)) + (0.0336190364 * PriceSeries(IPC, bar - 26, open, low, high, close)) + (0.0326129335 * PriceSeries(IPC, bar - 27, open, low, high, close)) + (0.0314517917 * PriceSeries(IPC, bar - 28, open, low, high, close)) + (0.030147198 * PriceSeries(IPC, bar - 29, open, low, high, close)) + (0.0287147044 * PriceSeries(IPC, bar - 30, open, low, high, close)) + (0.0271702104 * PriceSeries(IPC, bar - 31, open, low, high, close)) + (0.025529326 * PriceSeries(IPC, bar - 32, open, low, high, close)) + (0.0238101118 * PriceSeries(IPC, bar - 33, open, low, high, close)) + (0.0220298758 * PriceSeries(IPC, bar - 34, open, low, high, close)) + (0.0202076529 * PriceSeries(IPC, bar - 35, open, low, high, close)) + (0.0183605871 * PriceSeries(IPC, bar - 36, open, low, high, close)) + (0.0165073564 * PriceSeries(IPC, bar - 37, open, low, high, close)) + (0.0146643234 * PriceSeries(IPC, bar - 38, open, low, high, close)) + (0.0128488828 * PriceSeries(IPC, bar - 39, open, low, high, close)) + (0.0110760659 * PriceSeries(IPC, bar - 40, open, low, high, close)) + (0.0093613543 * PriceSeries(IPC, bar - 41, open, low, high, close)) + (0.0077174463 * PriceSeries(IPC, bar - 42, open, low, high, close)) + (0.0061560794 * PriceSeries(IPC, bar - 43, open, low, high, close)) + (0.0046876404 * PriceSeries(IPC, bar - 44, open, low, high, close)) + (0.0033209857 * PriceSeries(IPC, bar - 45, open, low, high, close)) + (0.0020624135 * PriceSeries(IPC, bar - 46, open, low, high, close)) + (0.0009181866 * PriceSeries(IPC, bar - 47, open, low, high, close)) - (0.0001091877 * PriceSeries(IPC, bar - 48, open, low, high, close)) - (0.0010167048 * PriceSeries(IPC, bar - 49, open, low, high, close)) - (0.0018053597 * PriceSeries(IPC, bar - 50, open, low, high, close)) - (0.0024753283 * PriceSeries(IPC, bar - 51, open, low, high, close)) - (0.0030306241 * PriceSeries(IPC, bar - 52, open, low, high, close)) - (0.0034740883 * PriceSeries(IPC, bar - 53, open, low, high, close)) - (0.0038122332 * PriceSeries(IPC, bar - 54, open, low, high, close)) - (0.0040510538 * PriceSeries(IPC, bar - 55, open, low, high, close)) - (0.004194773 * PriceSeries(IPC, bar - 56, open, low, high, close)) - (0.0042586429 * PriceSeries(IPC, bar - 57, open, low, high, close)) - (0.004243825 * PriceSeries(IPC, bar - 58, open, low, high, close)) - (0.0041610379 * PriceSeries(IPC, bar - 59, open, low, high, close)) - (0.0040209559 * PriceSeries(IPC, bar - 60, open, low, high, close)) - (0.0038324095 * PriceSeries(IPC, bar - 61, open, low, high, close)) - (0.0036044078 * PriceSeries(IPC, bar - 62, open, low, high, close)) - (0.0033446882 * PriceSeries(IPC, bar - 63, open, low, high, close)) - (0.0030621605 * PriceSeries(IPC, bar - 64, open, low, high, close)) - (0.0027641559 * PriceSeries(IPC, bar - 65, open, low, high, close)) - (0.002458932 * PriceSeries(IPC, bar - 66, open, low, high, close)) - (0.0021527365 * PriceSeries(IPC, bar - 67, open, low, high, close)) - (0.0018521222 * PriceSeries(IPC, bar - 68, open, low, high, close)) - (0.0015616524 * PriceSeries(IPC, bar - 69, open, low, high, close)) - (0.0012859688 * PriceSeries(IPC, bar - 70, open, low, high, close)) - (0.0010285368 * PriceSeries(IPC, bar - 71, open, low, high, close)) - (0.0007921495 * PriceSeries(IPC, bar - 72, open, low, high, close)) - (0.0005786502 * PriceSeries(IPC, bar - 73, open, low, high, close)) - (0.000389981 * PriceSeries(IPC, bar - 74, open, low, high, close)) - (0.0002262453 * PriceSeries(IPC, bar - 75, open, low, high, close)) - (8.82844e-05 * PriceSeries(IPC, bar - 76, open, low, high, close)) + (2.51537e-05 * PriceSeries(IPC, bar - 77, open, low, high, close)) + (0.0001141964 * PriceSeries(IPC, bar - 78, open, low, high, close)) + (0.0001810281 * PriceSeries(IPC, bar - 79, open, low, high, close)) + (0.0002266104 * PriceSeries(IPC, bar - 80, open, low, high, close)) + (0.000253652 * PriceSeries(IPC, bar - 81, open, low, high, close)) + (0.0002635807 * PriceSeries(IPC, bar - 82, open, low, high, close)) + (0.000259213 * PriceSeries(IPC, bar - 83, open, low, high, close)) + (0.0014236495 * PriceSeries(IPC, bar - 84, open, low, high, close))
        STLMBuffer[bar] = value3 - value4
        FTLMBuffer[bar] = value1 - value2
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def PriceSeries(applied_price, bar, Open, Low, High, Close):
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        return Close[bar]
    elif _sw1 == PRICE_OPEN:
        return Open[bar]
    elif _sw1 == PRICE_HIGH:
        return High[bar]
    elif _sw1 == PRICE_LOW:
        return Low[bar]
    elif _sw1 == PRICE_MEDIAN:
        return (High[bar] + Low[bar]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (Close[bar] + High[bar] + Low[bar]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * Close[bar]) + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 8:
        return (Open[bar] + Close[bar]) / 2.0
    elif _sw1 == 9:
        return (Open[bar] + Close[bar] + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 10:
        if Close[bar] > Open[bar]:
            return High[bar]
        else:
            if Close[bar] < Open[bar]:
                return Low[bar]
            else:
                return Close[bar]
    elif _sw1 == 11:
        if Close[bar] > Open[bar]:
            return (High[bar] + Close[bar]) / 2.0
        else:
            if Close[bar] < Open[bar]:
                return (Low[bar] + Close[bar]) / 2.0
            else:
                return Close[bar]
    elif _sw1 == 12:
        res = High[bar] + Low[bar] + Close[bar]
        if Close[bar] < Open[bar]:
            res = (res + Low[bar]) / 2
        if Close[bar] > Open[bar]:
            res = (res + High[bar]) / 2
        if Close[bar] == Open[bar]:
            res = (res + Close[bar]) / 2
        return (res - Low[bar] + (res - High[bar])) / 2
    else:
        return Close[bar]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dtm(_MQL5Indicator):
    name = 'Dtm'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

