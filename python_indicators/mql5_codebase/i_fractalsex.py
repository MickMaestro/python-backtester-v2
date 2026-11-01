"""i-fractalsex — converted from MQL5: MQL5 Indicators/i-FractalsEx/i-fractalsex.mq5

Copyright: Copyright © 2007, RickD; Link: www.e2e-fx.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, RickD', 'link': 'www.e2e-fx.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [11823615], 2: [16748574]}, 'widths': {1: 5, 2: 5}, 'styles': {}, 'labels': {1: 'Down Fractal', 2: 'Up Fractal'}, 'levels': [], 'description': [], 'name': 'i-fractalsex', 'source': 'MQL5 Indicators/i-FractalsEx/i-fractalsex.mq5', 'folder': 'i-FractalsEx', 'inputs': [{'mql': 'Fr_Period', 'py': 'Fr_Period', 'param': 'Fr_Period', 'type': 'uint', 'default': 6, 'label': 'Количество свечек', 'sinput': False}, {'mql': 'UpLabel', 'py': 'UpLabel', 'param': 'UpLabel', 'type': 'int', 'default': 176, 'label': 'Код символа верхнего фрактала', 'sinput': False}, {'mql': 'DnLabel', 'py': 'DnLabel', 'param': 'DnLabel', 'type': 'int', 'default': 176, 'label': 'Код символа нижнего фрактала', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Fr_Period = _input('Fr_Period', 6)  # Количество свечек
UpLabel = _input('UpLabel', 176)  # Код символа верхнего фрактала
DnLabel = _input('DnLabel', 176)  # Код символа нижнего фрактала
DnBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(Fr_Period + 1 + Fr_Period)
    SetIndexBuffer(0, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, UpLabel)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, DnLabel)
    ArraySetAsSeries(UpBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'i-FractalsEx'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated + _int(Fr_Period)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    for bar in range(limit, 0 - 1, -1):
        UpBuffer[bar] = EMPTY_VALUE
        DnBuffer[bar] = EMPTY_VALUE
        if is_upper_fr(rates_total, high, Fr_Period, bar):
            UpBuffer[bar] = high[bar]
        if is_lower_fr(rates_total, low, Fr_Period, bar):
            DnBuffer[bar] = low[bar]
    return rates_total

def is_upper_fr(Rates_Total, High, period, shift):
    if (shift + period) >= Rates_Total or (shift - period) < 0:
        return False
    for iii in range(1, period + 1):
        if High[shift] < High[shift + iii]:
            return False
        if High[shift] < High[shift - iii]:
            return False
    return True

def is_lower_fr(Rates_Total, Low, period, shift):
    if (shift + period) >= Rates_Total or (shift - period) < 0:
        return False
    for iii in range(1, period + 1):
        if Low[shift] > Low[shift + iii]:
            return False
        if Low[shift] > Low[shift - iii]:
            return False
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IFractalsex(_MQL5Indicator):
    name = 'i-fractalsex'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Fr_Period': 6,  # Количество свечек
        'UpLabel': 176,  # Код символа верхнего фрактала
        'DnLabel': 176,  # Код символа нижнего фрактала
    }

