"""i-gentorlsmaema_v02 — converted from MQL5: MQL5 Indicators/i-GentorLSMAEMA_v02/i-gentorlsmaema_v02.mq5

Copyright: Copyright © 2007, FX Sniper, KimIV; Link: http://www.kimiv.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, FX Sniper, KimIV', 'link': 'http://www.kimiv.ru', 'version': '1.00', 'window': 'separate', 'indicator_maximum': 3.9, 'indicator_minimum': 0.3, 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 8, 2: 8}, 'colors': {1: [255, 8421504, 65280], 2: [65535, 8421504, 16711680]}, 'widths': {1: 5, 2: 5}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Signal line', 2: 'Signal Arrow'}, 'levels': [], 'description': [''], 'name': 'i-gentorlsmaema_v02', 'source': 'MQL5 Indicators/i-GentorLSMAEMA_v02/i-gentorlsmaema_v02.mq5', 'folder': 'i-GentorLSMAEMA_v02', 'inputs': [{'mql': 'LSMAPeriod', 'py': 'LSMAPeriod', 'param': 'LSMAPeriod', 'type': 'uint', 'default': 25, 'label': 'Период LSMA', 'sinput': False}, {'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'uint', 'default': 34, 'label': 'Период MA', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 1, 'label': 'Тип усреднения', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 6, 'label': 'Ценовая константа', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LSMAPeriod = _input('LSMAPeriod', 25)  # Период LSMA
MAPeriod = _input('MAPeriod', 34)  # Период MA
MAType = _input('MAType', MODE_EMA)  # Тип усреднения
MAPrice = _input('MAPrice', PRICE_TYPICAL)  # Ценовая константа
Ind1Buffer = Arr(0, 0.0)
ColorInd1Buffer = Arr(0, 0.0)
Ind2Buffer = Arr(0, 0.0)
ColorInd2Buffer = Arr(0, 0.0)
res = 0.0
lengthvar = 0.0
MA_Handle = 0
min_rates_total = 0

def OnInit():
    global MA_Handle, lengthvar, min_rates_total, res
    min_rates_total = _int(MathMax(LSMAPeriod, MAPeriod))
    lengthvar = (LSMAPeriod + 1) / 3.0
    res = _fdiv(6.0, LSMAPeriod * (LSMAPeriod + 1.0))
    MA_Handle = iMA(Symbol(), PERIOD_CURRENT, MAPeriod, 0, MAType, MAPrice)
    if MA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    SetIndexBuffer(0, Ind1Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Ind1Buffer, True)
    SetIndexBuffer(1, ColorInd1Buffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorInd1Buffer, True)
    SetIndexBuffer(2, Ind2Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Ind2Buffer, True)
    SetIndexBuffer(3, ColorInd2Buffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorInd2Buffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'i-GentorLSMAEMA_v02'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(MA_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    MA = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - _int(MAPeriod) - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(MA, True)
    ArraySetAsSeries(close, True)
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MA) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Ind2Buffer[bar] = 1.4
        ColorInd2Buffer[bar] = 1.0
        if close[bar] > MA[bar]:
            ColorInd2Buffer[bar] = 2.0
        elif close[bar] < MA[bar]:
            ColorInd2Buffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - _int(LSMAPeriod) - 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Ind1Buffer[bar] = 3.0
        ColorInd1Buffer[bar] = 1.0
        sum_ = 0.0
        for iii in range(_int(LSMAPeriod), 1 - 1, -1):
            tmp = (iii - lengthvar) * close[LSMAPeriod - iii + bar]
            sum_ += tmp
        wt = sum_ * res
        if wt > close[bar]:
            ColorInd1Buffer[bar] = 0.0
        elif wt < close[bar]:
            ColorInd1Buffer[bar] = 2.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IGentorlsmaemaV02(_MQL5Indicator):
    name = 'i-gentorlsmaema_v02'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LSMAPeriod': 25,  # Период LSMA
        'MAPeriod': 34,  # Период MA
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Тип усреднения
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Ценовая константа
    }
    y_range = (0.3, 3.9)

