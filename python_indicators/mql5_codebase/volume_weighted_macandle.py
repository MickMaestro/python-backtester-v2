"""volume_weighted_macandle — converted from MQL5: MQL5 Indicators/Volume_Weighted_MACandle/volume_weighted_macandle.mq5

Volume_Weighted_MACandle
Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [9639167, 8421504, 8421376]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Volume_Weighted_MACandle Open;High;Low;Close'}, 'levels': [], 'description': ['Volume_Weighted_MACandle'], 'name': 'volume_weighted_macandle', 'source': 'MQL5 Indicators/Volume_Weighted_MACandle/volume_weighted_macandle.mq5', 'folder': 'Volume_Weighted_MACandle', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 12, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'объём', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 12)  # глубина сглаживания
VolumeType = _input('VolumeType', VOLUME_TICK)  # объём
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = Arr(4, 0, dyn=False)

def OnInit():
    global min_rates_total
    min_rates_total = _int(Length)
    PRICE_CLOSE_ = 1
    PRICE_OPEN_ = 2
    PRICE_HIGH_ = 3
    PRICE_LOW_ = 4
    Ind_Handle[0] = iCustom(None, 0, 'Volume_Weighted_MA', Length, PRICE_OPEN_, VolumeType, 0, 0)
    if Ind_Handle[0] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Volume_Weighted_MA[' + _str(0) + ']!')
        return INIT_FAILED
    Ind_Handle[1] = iCustom(None, 0, 'Volume_Weighted_MA', Length, PRICE_HIGH_, VolumeType, 0, 0)
    if Ind_Handle[1] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Volume_Weighted_MA[' + _str(1) + ']!')
        return INIT_FAILED
    Ind_Handle[2] = iCustom(None, 0, 'Volume_Weighted_MA', Length, PRICE_LOW_, VolumeType, 0, 0)
    if Ind_Handle[2] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Volume_Weighted_MA[' + _str(2) + ']!')
        return INIT_FAILED
    Ind_Handle[3] = iCustom(None, 0, 'Volume_Weighted_MA', Length, PRICE_CLOSE_, VolumeType, 0, 0)
    if Ind_Handle[3] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Volume_Weighted_MA[' + _str(3) + ']!')
        return INIT_FAILED
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Volume_Weighted_MACandle'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (((BarsCalculated(Ind_Handle[0]) < rates_total or BarsCalculated(Ind_Handle[1]) < rates_total) or BarsCalculated(Ind_Handle[2]) < rates_total) or BarsCalculated(Ind_Handle[3]) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind_Handle[0], 0, 0, to_copy, ExtOpenBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[1], 0, 0, to_copy, ExtHighBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[2], 0, 0, to_copy, ExtLowBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[3], 0, 0, to_copy, ExtCloseBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Max = MathMax(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        Min = MathMin(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        ExtHighBuffer[bar] = MathMax(Max, ExtHighBuffer[bar])
        ExtLowBuffer[bar] = MathMin(Min, ExtLowBuffer[bar])
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolumeWeightedMacandle(_MQL5Indicator):
    name = 'volume_weighted_macandle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 12,  # глубина сглаживания
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём
    }

