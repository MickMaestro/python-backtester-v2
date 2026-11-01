"""k_iupdown — converted from MQL5: MQL5 Indicators/Up and Down Indicator/k_iupdown.mq5

Copyright: Karlis Balcers; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Karlis Balcers', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [8388352, 3329330, 32768, 25600, 8036607, 17919, 3937500, 128]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'k_iupdown', 'source': 'MQL5 Indicators/Up and Down Indicator/k_iupdown.mq5', 'folder': 'Up and Down Indicator', 'inputs': [{'mql': 'comment', 'py': 'comment', 'param': None, 'type': 'string', 'default': 'Index from 1-10 to increase sensitivity.', 'label': '', 'sinput': False}, {'mql': 'tick_volume_index', 'py': 'tick_volume_index', 'param': 'tick_volume_index', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
comment = _input('comment', 'Index from 1-10 to increase sensitivity.')
tick_volume_index = _input('tick_volume_index', 7)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorsBuffer = Arr(0, 0.0)
total_vol = 0
count_bars = 0
passNo = 0

def OnInit():
    global count_bars, total_vol
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorsBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'K_iUpDown')
    total_vol = 0
    count_bars = 0
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global count_bars, passNo, total_vol
    i = 0
    vol_up = True
    passNo += 1
    if i < prev_calculated:
        i = prev_calculated - 1
    while i < rates_total:
        if i != 0:
            total_vol += tick_volume[i]
            count_bars += 1
        x = 0.0
        if count_bars == 0:
            x = (tick_volume[i] * 100.0) / tick_volume_index
        else:
            avg_vol = _fdiv(1.0 * total_vol, count_bars)
            x = _fdiv(tick_volume[i] * 100.0, avg_vol * tick_volume_index)
        col = 0
        if x > 0:
            col = 0
        if x > 25:
            col = 1
        if x > 50:
            col = 2
        if x > 75:
            col = 3
        if open[i] < close[i]:
            ExtColorsBuffer[i] = col
        else:
            ExtColorsBuffer[i] = 4 + col
        ExtOpenBuffer[i] = 0.0
        ExtHighBuffer[i] = high[i] - open[i]
        ExtLowBuffer[i] = low[i] - open[i]
        ExtCloseBuffer[i] = close[i] - open[i]
        i += 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KIupdown(_MQL5Indicator):
    name = 'k_iupdown'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'tick_volume_index': 7,
    }

