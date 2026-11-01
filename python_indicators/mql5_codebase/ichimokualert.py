"""IchimokuAlert — converted from MQL5: MQL5 Indicators/Ichimoku Alerting , Tenkan-sen Kijun-sen Cross Alert/IchimokuAlert.mq5

Ichimoku Tenkan_sen Kinjun-sen Cross Alert
Copyright: 2021, MSK Corp.; Link: m.saket@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2021, MSK Corp.', 'link': 'm.saket@gmail.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Tenkan-sen', 2: 'Kijun-sen'}, 'levels': [], 'description': ['Ichimoku Tenkan_sen Kinjun-sen Cross Alert'], 'name': 'IchimokuAlert', 'source': 'MQL5 Indicators/Ichimoku Alerting , Tenkan-sen Kijun-sen Cross Alert/IchimokuAlert.mq5', 'folder': 'Ichimoku Alerting , Tenkan-sen Kijun-sen Cross Alert', 'inputs': [{'mql': 'InpTenkan', 'py': 'InpTenkan', 'param': 'InpTenkan', 'type': 'int', 'default': 9, 'label': 'Tenkan-sen', 'sinput': False}, {'mql': 'InpKijun', 'py': 'InpKijun', 'param': 'InpKijun', 'type': 'int', 'default': 26, 'label': 'Kijun-sen', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpTenkan = _input('InpTenkan', 9)  # Tenkan-sen
InpKijun = _input('InpKijun', 26)  # Kijun-sen
ExtTenkanBuffer = Arr(0, 0.0)
ExtKijunBuffer = Arr(0, 0.0)
LastBars = 0

def OnInit():
    SetIndexBuffer(0, ExtTenkanBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtKijunBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpTenkan)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, InpKijun)
    PlotIndexSetInteger(2, PLOT_SHIFT, InpKijun)
    PlotIndexSetInteger(3, PLOT_SHIFT, -InpKijun)
    PlotIndexSetString(0, PLOT_LABEL, 'Tenkan-sen(' + _str(InpTenkan) + ')')
    PlotIndexSetString(1, PLOT_LABEL, 'Kijun-sen(' + _str(InpKijun) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global LastBars
    start = 0
    if prev_calculated == 0:
        start = 1
    else:
        start = prev_calculated - 1
    for i in range(start, rates_total):
        price_max = Highest(high, InpTenkan, i)
        price_min = Lowest(low, InpTenkan, i)
        ExtTenkanBuffer[i] = (price_max + price_min) / 2.0
        price_max = Highest(high, InpKijun, i)
        price_min = Lowest(low, InpKijun, i)
        ExtKijunBuffer[i] = (price_max + price_min) / 2.0
        ee = ExtTenkanBuffer[i]
        es = ExtKijunBuffer[i]
        ew = ExtTenkanBuffer[i - 1]
        wq = ExtKijunBuffer[i - 1]
        nBars = Bars(Symbol(), PERIOD_CURRENT)
        if LastBars != nBars:
            LastBars = nBars
            if ExtTenkanBuffer[i] > ExtKijunBuffer[i] and ExtTenkanBuffer[i - 1] <= ExtKijunBuffer[i - 1]:
                SendNotification('Cross Up')
            if ExtTenkanBuffer[i] < ExtKijunBuffer[i] and ExtTenkanBuffer[i - 1] >= ExtKijunBuffer[i - 1]:
                SendNotification('Cross Up')
    return rates_total

def Highest(array, range_, from_index):
    res = 0.0
    res = array[from_index]
    i = from_index
    while i > (from_index - range_) and i >= 0:
        if res < array[i]:
            res = array[i]
        i -= 1
    return res

def Lowest(array, range_, from_index):
    res = 0.0
    res = array[from_index]
    i = from_index
    while i > (from_index - range_) and i >= 0:
        if res > array[i]:
            res = array[i]
        i -= 1
    return res


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IchimokuAlert(_MQL5Indicator):
    name = 'IchimokuAlert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpTenkan': 9,  # Tenkan-sen
        'InpKijun': 26,  # Kijun-sen
    }

