"""fiboZigZag — converted from MQL5: MQL5 Indicators/Fibonacci ZigZag/fiboZigZag.mq5

Copyright: Author; Link: https://www.mql5.com/en/users/lorio; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Author', 'link': 'https://www.mql5.com/en/users/lorio', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'fiboZigZag', 'source': 'MQL5 Indicators/Fibonacci ZigZag/fiboZigZag.mq5', 'folder': 'Fibonacci ZigZag', 'inputs': [{'mql': 'retracement', 'py': 'retracement', 'param': 'retracement', 'type': 'double', 'default': 23.6, 'label': 'retracement amount', 'sinput': False}, {'mql': 'minSizeInAtrUnits', 'py': 'minSizeInAtrUnits', 'param': 'minSizeInAtrUnits', 'type': 'double', 'default': 0.0, 'label': 'min size of waves in atr units', 'sinput': False}, {'mql': 'rollingAtrPeriod', 'py': 'rollingAtrPeriod', 'param': 'rollingAtrPeriod', 'type': 'int', 'default': 14, 'label': 'rolling atr period', 'sinput': False}, {'mql': 'Color', 'py': 'Color', 'param': None, 'type': 'color', 'default': 16748574, 'label': 'wave color', 'sinput': False}, {'mql': 'Width', 'py': 'Width', 'param': 'Width', 'type': 'int', 'default': 3, 'label': 'wave width', 'sinput': False}, {'mql': 'Style', 'py': 'Style', 'param': 'Style', 'type': 'int', 'default': 0, 'label': 'wave style', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
retracement = _input('retracement', 23.6)  # retracement amount
minSizeInAtrUnits = _input('minSizeInAtrUnits', 0.0)  # min size of waves in atr units
rollingAtrPeriod = _input('rollingAtrPeriod', 14)  # rolling atr period
Color = _input('Color', clrDodgerBlue)  # wave color
Width = _input('Width', 3)  # wave width
Style = _input('Style', STYLE_SOLID)  # wave style
upWaves = Arr(0, 0.0)
dwWaves = Arr(0, 0.0)
wave_type = 0
wave_start_price = 0.0
wave_end_price = 0.0
wave_start_distance = 0
wave_end_distance = 0
high_mem = 0.0
distance_from_high = 0
low_mem = 0.0
distance_from_low = 0
rollingAtr = 0.0
rollingAtrs = 0

def OnInit():
    SetIndexBuffer(0, upWaves, INDICATOR_DATA)
    SetIndexBuffer(1, dwWaves, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_ZIGZAG)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, Color)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, Width)
    PlotIndexSetInteger(0, PLOT_LINE_STYLE, Style)
    resetSystem()
    return INIT_SUCCEEDED

def resetSystem():
    global distance_from_high, distance_from_low, high_mem, low_mem, rollingAtr, rollingAtrs, wave_end_distance, wave_end_price, wave_start_distance, wave_start_price, wave_type
    ArrayFill(upWaves, 0, ArraySize(upWaves), 0.0)
    ArrayFill(dwWaves, 0, ArraySize(dwWaves), 0.0)
    wave_type = 0
    wave_start_price = 0.0
    wave_end_price = 0.0
    wave_start_distance = 0
    wave_end_distance = 0
    high_mem = 0.0
    low_mem = 0.0
    distance_from_high = 0
    distance_from_low = 0
    rollingAtr = 0.0
    rollingAtrs = 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global distance_from_high, distance_from_low, high_mem, low_mem, rollingAtr, rollingAtrs, wave_end_distance, wave_end_price, wave_start_distance, wave_start_price, wave_type
    from_ = rates_total - 1
    if prev_calculated == 0:
        from_ = 1
        resetSystem()
        rollingAtr = _fdiv(high[0] - low[0], Point())
        rollingAtrs = 1
    for i in range(from_, rates_total - 1):
        if i == 1:
            Comment('Atr Unit ' + DoubleToString(rollingAtr, 1) + ' pts\nMin wave size ' + DoubleToString(rollingAtr * minSizeInAtrUnits, 1) + ' pts')
        distance_from_high += 1
        distance_from_low += 1
        rollingAtrs += 1
        if rollingAtrs > rollingAtrPeriod:
            new_portion = _fdiv(high[i] - low[i], Point()) / float(rollingAtrPeriod)
            rollingAtr = rollingAtr - (rollingAtr / float(rollingAtrPeriod)) + new_portion
        elif rollingAtrs <= rollingAtrPeriod:
            rollingAtr += _fdiv(high[i] - low[i], Point())
            if rollingAtrs == rollingAtrPeriod:
                rollingAtr = _fdiv(rollingAtr, float(rollingAtrs))
                high_mem = high[i]
                low_mem = low[i]
                distance_from_high = 0
                distance_from_low = 0
        if rollingAtrs > rollingAtrPeriod:
            if wave_type != 0:
                wave_start_distance += 1
                wave_end_distance += 1
            if wave_type != 0:
                if wave_type == 1:
                    if high[i] > wave_end_price:
                        upWaves[i - wave_end_distance] = 0.0
                        upWaves[i] = high[i]
                        wave_end_price = high[i]
                        wave_end_distance = 0
                        high_mem = high[i]
                        distance_from_high = 0
                        low_mem = low[i]
                        distance_from_low = 0
                    if low[i] < low_mem or distance_from_low == 0:
                        low_mem = low[i]
                        distance_from_low = 0
                        size_of_wave = _fdiv(wave_end_price - wave_start_price, Point())
                        size_of_retracement = _fdiv(wave_end_price - low_mem, Point())
                        if size_of_wave > 0.0:
                            retraced = _fdiv(size_of_retracement, size_of_wave) * 100.0
                            new_wave_size_in_atr_units = _fdiv(_fdiv(wave_end_price - low_mem, Point()), rollingAtr)
                            if new_wave_size_in_atr_units >= minSizeInAtrUnits:
                                if retraced >= retracement:
                                    wave_type = -1
                                    wave_start_price = high[i - distance_from_high]
                                    wave_start_distance = distance_from_high
                                    wave_end_price = low[i]
                                    wave_end_distance = 0
                                    upWaves[i - wave_start_distance] = high_mem
                                    dwWaves[i] = low[i]
                                    high_mem = high[i]
                                    distance_from_high = 0
                                    low_mem = low[i]
                                    distance_from_low = 0
                elif wave_type == -1:
                    if low[i] < wave_end_price:
                        dwWaves[i - wave_end_distance] = 0.0
                        dwWaves[i] = low[i]
                        wave_end_price = low[i]
                        wave_end_distance = 0
                        high_mem = high[i]
                        distance_from_high = 0
                        low_mem = low[i]
                        distance_from_low = 0
                    if high[i] > high_mem or distance_from_high == 0:
                        high_mem = high[i]
                        distance_from_high = 0
                        size_of_wave = _fdiv(wave_start_price - wave_end_price, Point())
                        size_of_retracement = _fdiv(high_mem - wave_end_price, Point())
                        if size_of_wave > 0.0:
                            retraced = _fdiv(size_of_retracement, size_of_wave) * 100.0
                            new_wave_size_in_atr_units = _fdiv(_fdiv(high_mem - wave_end_price, Point()), rollingAtr)
                            if new_wave_size_in_atr_units >= minSizeInAtrUnits:
                                if retraced >= retracement:
                                    wave_type = 1
                                    wave_start_price = low_mem
                                    wave_start_distance = distance_from_low
                                    wave_end_price = high[i]
                                    wave_end_distance = 0
                                    dwWaves[i - wave_start_distance] = low_mem
                                    upWaves[i] = high[i]
                                    high_mem = high[i]
                                    distance_from_high = 0
                                    low_mem = low[i]
                                    distance_from_low = 0
            else:
                if high[i] > high_mem and low[i] >= low_mem:
                    new_wave_size_in_atr_units = _fdiv(_fdiv(high[i] - low_mem, Point()), rollingAtr)
                    if new_wave_size_in_atr_units >= minSizeInAtrUnits:
                        wave_type = 1
                        wave_start_price = low_mem
                        wave_start_distance = distance_from_low
                        wave_end_price = high[i]
                        wave_end_distance = 0
                        dwWaves[i - wave_start_distance] = low_mem
                        upWaves[i] = high[i]
                        high_mem = high[i]
                        distance_from_high = 0
                        low_mem = low[i]
                        distance_from_low = 0
                elif low[i] < low_mem and high[i] <= high_mem:
                    new_wave_size_in_atr_units = _fdiv(_fdiv(high_mem - low[i], Point()), rollingAtr)
                    if new_wave_size_in_atr_units >= minSizeInAtrUnits:
                        wave_type = -1
                        wave_start_price = high_mem
                        wave_start_distance = distance_from_high
                        wave_end_price = low[i]
                        wave_end_distance = 0
                        upWaves[i - wave_start_distance] = high_mem
                        dwWaves[i] = low[i]
                        high_mem = high[i]
                        distance_from_high = 0
                        low_mem = low[i]
                        distance_from_low = 0
                elif low[i] < low_mem and high[i] > high_mem:
                    high_mem = high[i]
                    low_mem = low[i]
                    distance_from_high = 0
                    distance_from_low = 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FiboZigZag(_MQL5Indicator):
    name = 'fiboZigZag'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'retracement': 23.6,  # retracement amount
        'minSizeInAtrUnits': 0.0,  # min size of waves in atr units
        'rollingAtrPeriod': 14,  # rolling atr period
        'Width': 3,  # wave width
        'Style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # wave style
    }

