"""gaps_cb — converted from MQL5: MQL5 Indicators/Gaps/gaps_cb.mq5

Copyright: Tapochun; Link: https://login.mql5.com/ru/users/tapochun; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Tapochun', 'link': 'https://login.mql5.com/ru/users/tapochun', 'version': '1.00', 'window': 'separate', 'indicator_minimum': 0.0, 'indicator_plots': 1, 'indicator_buffers': 2}, 'types': {1: 10}, 'colors': {1: [65280, 255, 8421504]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'gaps_cb', 'source': 'MQL5 Indicators/Gaps/gaps_cb.mq5', 'folder': 'Gaps', 'inputs': [{'mql': 'inpBigGap', 'py': 'inpBigGap', 'param': 'inpBigGap', 'type': 'int', 'default': 0, 'label': 'Размер большого гэпа (подсвечивается)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
bufValue = Arr(0, 0.0)  # Буфер значений гэпов
bufValueClr = Arr(0, 0.0)  # Буфер цвета гэпов
inpBigGap = _input('inpBigGap', 0)  # Размер большого гэпа (подсвечивается)

def OnInit():
    SetIndexBuffer(0, bufValue)
    SetIndexBuffer(1, bufValueClr, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    if inpBigGap > 0:
        IndicatorSetInteger(INDICATOR_LEVELS, 1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, inpBigGap)
        IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Big Gap')
    IndicatorSetString(INDICATOR_SHORTNAME, 'Gap')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total <= 0:
        return 0
    if prev_calculated != 0:
        if rates_total > prev_calculated:
            Calculation(rates_total - 1, rates_total, inpBigGap, open, close)
    else:
        Calculation(1, rates_total, inpBigGap, open, close)
    return rates_total

def Calculation(first, rates_total, bigGap, open, close):
    gap = 0
    for i in range(1, rates_total):
        gap = _int(MathRound(MathAbs(_fdiv(open[i] - close[i - 1], Point()))))
        bufValue[i] = gap
        if gap >= bigGap:
            if open[i] > close[i - 1]:
                bufValueClr[i] = 1.0
            else:
                bufValueClr[i] = 0.0
        else:
            bufValueClr[i] = 2.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GapsCb(_MQL5Indicator):
    name = 'gaps_cb'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpBigGap': 0,  # Размер большого гэпа (подсвечивается)
    }

