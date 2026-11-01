"""MASi_WaveHist — converted from MQL5: MQL5 Indicators/MASi_WaveHist/MASi_WaveHist.mq5

Raghee's Cicle indicator (aka Wave).
Indicator of the market cycle.
The idea of Raghee Horner.
Copyright: Copyright 2017, Terentyev Aleksey; Link: https://www.mql5.com/ru/users/terentyev23; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2017, Terentyev Aleksey', 'link': 'https://www.mql5.com/ru/users/terentyev23', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_maximum': 1.0, 'indicator_minimum': -1.0}, 'types': {1: 10}, 'colors': {1: [8421376, 16711935]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'MASi_WaveHist'}, 'levels': [], 'description': ["Raghee's Cicle indicator (aka Wave).", 'Indicator of the market cycle.', 'The idea of Raghee Horner.'], 'name': 'MASi_WaveHist', 'source': 'MQL5 Indicators/MASi_WaveHist/MASi_WaveHist.mq5', 'folder': 'MASi_WaveHist', 'inputs': [{'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'uint', 'default': 34, 'label': '', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAPeriod = _input('MAPeriod', 34)
MAType = _input('MAType', MODE_EMA)
MAPrice = _input('MAPrice', PRICE_CLOSE)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
HMA_Handle = 0
LMA_Handle = 0

def OnInit():
    global HMA_Handle, LMA_Handle, min_rates_total
    min_rates_total = _int(MAPeriod) + 1
    HMA_Handle = iMA(None, 0, MAPeriod, 0, MAType, PRICE_HIGH)
    if HMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора HIGH iMA')
        return INIT_FAILED
    LMA_Handle = iMA(None, 0, MAPeriod, 0, MAType, PRICE_LOW)
    if LMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора LOW iMA')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    ArraySetAsSeries(ColorIndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'MASi_WaveHist(', MAPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(HMA_Handle) < rates_total or BarsCalculated(LMA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    HMA = Arr(0, 0.0)
    LMA = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(HMA_Handle, 0, 0, to_copy, HMA) <= 0:
        return 0
    if CopyBuffer(LMA_Handle, 0, 0, to_copy, LMA) <= 0:
        return 0
    ArraySetAsSeries(HMA, True)
    ArraySetAsSeries(LMA, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer[bar] = 0.0
        ColorIndBuffer[bar] = EMPTY_VALUE
        tmp = (1.0 if (close[bar] > HMA[bar]) else -1.0 if (close[bar] < LMA[bar]) else 0.0)
        if tmp > 0:
            IndBuffer[bar] = tmp
            ColorIndBuffer[bar] = 0.0
        elif tmp < 0:
            IndBuffer[bar] = tmp
            ColorIndBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MASiWaveHist(_MQL5Indicator):
    name = 'MASi_WaveHist'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAPeriod': 34,
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }
    y_range = (-1.0, 1.0)

