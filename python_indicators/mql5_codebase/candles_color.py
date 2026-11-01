"""candles_color — converted from MQL5: MQL5 Indicators/Change the color of the candles/candles_color.mq5

Copyright: kourosh1347@yahoo.com; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'kourosh1347@yahoo.com', 'window': 'chart', 'version': '1.0', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {}, 'widths': {1: 3}, 'styles': {}, 'labels': {1: 'Open;High;Low;Close'}, 'levels': [], 'description': [], 'name': 'candles_color', 'source': 'MQL5 Indicators/Change the color of the candles/candles_color.mq5', 'folder': 'Change the color of the candles', 'inputs': [{'mql': 'Start_Day', 'py': 'Start_Day', 'param': 'Start_Day', 'type': 'int', 'default': 4, 'label': 'Starting Day for show', 'sinput': False}, {'mql': 'Start_Hour', 'py': 'Start_Hour', 'param': 'Start_Hour', 'type': 'int', 'default': 6, 'label': 'Starting Hour of day', 'sinput': False}, {'mql': 'Start_Minute', 'py': 'Start_Minute', 'param': 'Start_Minute', 'type': 'int', 'default': 0, 'label': 'Starting Minute of hour', 'sinput': False}, {'mql': 'End_Day', 'py': 'End_Day', 'param': 'End_Day', 'type': 'int', 'default': 4, 'label': 'End of Day', 'sinput': False}, {'mql': 'End_Hour', 'py': 'End_Hour', 'param': 'End_Hour', 'type': 'int', 'default': 20, 'label': 'End Hour of day', 'sinput': False}, {'mql': 'End_Minute', 'py': 'End_Minute', 'param': 'End_Minute', 'type': 'int', 'default': 59, 'label': 'End Hour of day', 'sinput': False}, {'mql': 'Color_Bar_Up_1', 'py': 'Color_Bar_Up_1', 'param': None, 'type': 'color', 'default': 15130800, 'label': '', 'sinput': False}, {'mql': 'Color_Bar_Down_1', 'py': 'Color_Bar_Down_1', 'param': None, 'type': 'color', 'default': 12903679, 'label': '', 'sinput': False}, {'mql': 'Color_Bar_Up_0', 'py': 'Color_Bar_Up_0', 'param': None, 'type': 'color', 'default': 32768, 'label': '', 'sinput': False}, {'mql': 'Color_Bar_Down_0', 'py': 'Color_Bar_Down_0', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Start_Day = _input('Start_Day', 4)  # Starting Day for show
Start_Hour = _input('Start_Hour', 6)  # Starting Hour of day
Start_Minute = _input('Start_Minute', 0)  # Starting Minute of hour
End_Day = _input('End_Day', 4)  # End of Day
End_Hour = _input('End_Hour', 20)  # End Hour of day
End_Minute = _input('End_Minute', 59)  # End Hour of day
Color_Bar_Up_1 = _input('Color_Bar_Up_1', clrPowderBlue)
Color_Bar_Down_1 = _input('Color_Bar_Down_1', clrBisque)
Color_Bar_Up_0 = _input('Color_Bar_Up_0', clrGreen)
Color_Bar_Down_0 = _input('Color_Bar_Down_0', clrRed)
buf_open = Arr(0, 0.0)  # Buffers for data
buf_high = Arr(0, 0.0)  # Buffers for data
buf_low = Arr(0, 0.0)  # Buffers for data
buf_close = Arr(0, 0.0)  # Buffers for data
buf_color_line = Arr(0, 0.0)  # Buffer for color indexes

def OnInit():
    SetIndexBuffer(0, buf_open, INDICATOR_DATA)
    SetIndexBuffer(1, buf_high, INDICATOR_DATA)
    SetIndexBuffer(2, buf_low, INDICATOR_DATA)
    SetIndexBuffer(3, buf_close, INDICATOR_DATA)
    SetIndexBuffer(4, buf_color_line, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 4)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, Color_Bar_Up_0)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, Color_Bar_Down_0)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 2, Color_Bar_Up_1)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 3, Color_Bar_Down_1)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    time_now = MqlDateTime()
    for i in range(prev_calculated, rates_total - 1 + 1):
        buf_open[i] = open[i]
        buf_high[i] = high[i]
        buf_low[i] = low[i]
        buf_close[i] = close[i]
        candle_time = time[i]
        TimeToStruct(time[i], time_now)
        if ((time_now.day_of_week >= Start_Day and time_now.hour >= Start_Hour) and time_now.min >= Start_Minute) and ((time_now.day_of_week <= End_Day and time_now.hour <= End_Hour) and time_now.min <= End_Minute):
            if open[i] >= close[i]:
                buf_color_line[i] = 3.0
            else:
                buf_color_line[i] = 2.0
        else:
            if open[i] >= close[i]:
                buf_color_line[i] = 1.0
            else:
                buf_color_line[i] = 0.0
    return rates_total - 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandlesColor(_MQL5Indicator):
    name = 'candles_color'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Start_Day': 4,  # Starting Day for show
        'Start_Hour': 6,  # Starting Hour of day
        'Start_Minute': 0,  # Starting Minute of hour
        'End_Day': 4,  # End of Day
        'End_Hour': 20,  # End Hour of day
        'End_Minute': 59,  # End Hour of day
    }

