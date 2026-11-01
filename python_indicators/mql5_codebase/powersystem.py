"""PowerSystem — converted from MQL5: MQL5 Indicators/PowerSystem/PowerSystem.mq5

The index according to the EMA index and the trend of MACD indicators calculated signals,
and adding color on candle charts, the default setting is: 
red column represents the rising trend, green column represents the downward trend,
blue column represents no obvious signals.
Copyright: Copyright 2018, MetaQuotes Software Corp.Jianye Xiong; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.Jianye Xiong', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {}, 'widths': {1: 3}, 'styles': {}, 'labels': {1: 'P_Open;P_High;P_Low;P_Close'}, 'levels': [], 'description': ['The index according to the EMA index and the trend of MACD indicators calculated signals,', 'and adding color on candle charts, the default setting is: ', 'red column represents the rising trend, green column represents the downward trend,', 'blue column represents no obvious signals.'], 'name': 'PowerSystem', 'source': 'MQL5 Indicators/PowerSystem/PowerSystem.mq5', 'folder': 'PowerSystem', 'inputs': [{'mql': 'macdfast', 'py': 'macdfast', 'param': 'macdfast', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'macdslow', 'py': 'macdslow', 'param': 'macdslow', 'type': 'int', 'default': 26, 'label': '', 'sinput': False}, {'mql': 'macdsignal', 'py': 'macdsignal', 'param': 'macdsignal', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'emaperiod', 'py': 'emaperiod', 'param': 'emaperiod', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'Rise', 'py': 'Rise', 'param': None, 'type': 'color', 'default': 9639167, 'label': '', 'sinput': False}, {'mql': 'Drop', 'py': 'Drop', 'param': None, 'type': 'color', 'default': 8388352, 'label': '', 'sinput': False}, {'mql': 'Noise', 'py': 'Noise', 'param': None, 'type': 'color', 'default': 15624315, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
macdfast = _input('macdfast', 12)
macdslow = _input('macdslow', 26)
macdsignal = _input('macdsignal', 9)
emaperiod = _input('emaperiod', 12)
Rise = _input('Rise', clrDeepPink)
Drop = _input('Drop', clrSpringGreen)
Noise = _input('Noise', clrMediumSlateBlue)
Handle_macd = 0
Handle_ema = 0
Power_buffer = Arr(0, 0.0)
macd_main_buffer = Arr(0, 0.0)
ema_buffer = Arr(0, 0.0)
color_buffer = Arr(0, 0.0)
buffer_open = Arr(0, 0.0)
buffer_high = Arr(0, 0.0)
buffer_low = Arr(0, 0.0)
buffer_close = Arr(0, 0.0)

def OnInit():
    global Handle_ema, Handle_macd
    SetIndexBuffer(0, buffer_open, INDICATOR_DATA)
    SetIndexBuffer(1, buffer_high, INDICATOR_DATA)
    SetIndexBuffer(2, buffer_low, INDICATOR_DATA)
    SetIndexBuffer(3, buffer_close, INDICATOR_DATA)
    SetIndexBuffer(4, color_buffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, Power_buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, ema_buffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, macd_main_buffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 3)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, Drop)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, Rise)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 2, Noise)
    Handle_macd = iMACD(Symbol(), 0, macdfast, macdslow, macdsignal, PRICE_CLOSE)
    Handle_ema = iMA(Symbol(), 0, emaperiod, 0, MODE_EMA, PRICE_CLOSE)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    digits = Digits()
    CopyBuffer(Handle_ema, 0, 0, rates_total, ema_buffer)
    CopyBuffer(Handle_macd, 0, 0, rates_total, macd_main_buffer)
    start = 0
    start = prev_calculated
    if prev_calculated == 0:
        start = MathMax(emaperiod, macdslow) - 1
    for i in range(start, rates_total - 1 + 1):
        buffer_open[i] = open[i]
        buffer_high[i] = high[i]
        buffer_low[i] = low[i]
        buffer_close[i] = close[i]
        color_buffer[i] = 2.0
        Power_buffer[i] = 0.0
        if (macd_main_buffer[i] - macd_main_buffer[i - 1]) > 0 and (ema_buffer[i] - ema_buffer[i - 1]) > 0:
            Power_buffer[i] = 1.0
            color_buffer[i] = 1.0
        if (macd_main_buffer[i] - macd_main_buffer[i - 1]) < 0 and (ema_buffer[i] - ema_buffer[i - 1]) < 0:
            Power_buffer[i] = -1.0
            color_buffer[i] = 0.0
    return rates_total - 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PowerSystem(_MQL5Indicator):
    name = 'PowerSystem'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'macdfast': 12,
        'macdslow': 26,
        'macdsignal': 9,
        'emaperiod': 12,
    }

