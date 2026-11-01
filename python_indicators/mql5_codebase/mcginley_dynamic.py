"""McGinley_Dynamic — converted from MQL5: MQL5 Indicators/McGinley Dynamic Indicator/McGinley_Dynamic.mq5

Copyright: Copyright 2018, Samuel Williams; Link: https://www.mql5.com/en/users/sambo3261; Version: 1.1

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, Samuel Williams', 'link': 'https://www.mql5.com/en/users/sambo3261', 'version': '1.1', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [65535]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'MD'}, 'levels': [], 'description': [], 'name': 'McGinley_Dynamic', 'source': 'MQL5 Indicators/McGinley Dynamic Indicator/McGinley_Dynamic.mq5', 'folder': 'McGinley Dynamic Indicator', 'inputs': [{'mql': 'MD_smooth', 'py': 'MD_smooth', 'param': 'MD_smooth', 'type': 'int', 'default': 125, 'label': 'Smoothing parameter (60% of equivalent MA period)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MD_smooth = _input('MD_smooth', 125)  # Smoothing parameter (60% of equivalent MA period)
MDBuffer = Arr(0, 0.0)
EMABuffer = Arr(0, 0.0)
EMAHandle = 0
CopiedEMA = 0

def OnInit():
    global EMAHandle
    SetIndexBuffer(0, MDBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, EMABuffer, INDICATOR_CALCULATIONS)
    periodTemp = _int(MathRound(MD_smooth * 0.6))
    EMAHandle = iMA(Symbol(), Period(), periodTemp, 0, MODE_EMA, PRICE_CLOSE)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global CopiedEMA
    i = 0
    start = 0
    CopiedEMA = CopyBuffer(EMAHandle, 0, 0, rates_total, EMABuffer)
    if CopiedEMA < 0:
        PrintFormat('Error in copy EMA buffer, code %d', GetLastError())
    if rates_total < 2:
        return 0
    if prev_calculated == 0:
        firstMD = 0.0
        i = 1
        for i in range(i, 2 + 1):
            MDBuffer[i] = EMABuffer[i]
            firstMD += _fdiv(close[i] - EMABuffer[i - 1], _fdiv(MD_smooth * close[i], EMABuffer[i - 1]))
        else:
            i = _range_end(i, 2 + 1, 1)
        start = 2 + 1
    else:
        start = prev_calculated - 1
    i = start
    for i in range(i, rates_total):
        MDBuffer[i] = MDBuffer[i - 1] + _fdiv(close[i] - MDBuffer[i - 1], MD_smooth * _fdiv(close[i], MDBuffer[i - 1]))
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class McGinleyDynamic(_MQL5Indicator):
    name = 'McGinley_Dynamic'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MD_smooth': 125,  # Smoothing parameter (60% of equivalent MA period)
    }

