"""colorstochastic — converted from MQL5: MQL5 Indicators/ColorStochastic/colorstochastic.mq5

Stochastic oscillator is used as a color histogram
Copyright: Copyright © 2012, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 11, 2: 8}, 'colors': {1: [8421504, 7451452, 16711680, 255, 16711935], 2: [8421504, 65280, 9639167]}, 'widths': {1: 3, 2: 2}, 'styles': {1: 0, 2: 1}, 'labels': {1: 'Main', 2: 'Signal'}, 'levels': [70.0, 50.0, 30.0], 'description': ['Stochastic oscillator is used as a color histogram'], 'name': 'colorstochastic', 'source': 'MQL5 Indicators/ColorStochastic/colorstochastic.mq5', 'folder': 'ColorStochastic', 'inputs': [{'mql': 'InpKPeriod', 'py': 'InpKPeriod', 'param': 'InpKPeriod', 'type': 'int', 'default': 5, 'label': 'K period', 'sinput': False}, {'mql': 'InpDPeriod', 'py': 'InpDPeriod', 'param': 'InpDPeriod', 'type': 'int', 'default': 3, 'label': 'D period', 'sinput': False}, {'mql': 'InpSlowing', 'py': 'InpSlowing', 'param': 'InpSlowing', 'type': 'int', 'default': 3, 'label': 'Slowing', 'sinput': False}, {'mql': 'ma_method', 'py': 'ma_method', 'param': 'ma_method', 'type': 'int', 'default': 0, 'label': 'smoothing type', 'sinput': False}, {'mql': 'price_field', 'py': 'price_field', 'param': 'price_field', 'type': 'int', 'default': 0, 'label': 'stochastic calculation method', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpKPeriod = _input('InpKPeriod', 5)  # K period
InpDPeriod = _input('InpDPeriod', 3)  # D period
InpSlowing = _input('InpSlowing', 3)  # Slowing
ma_method = _input('ma_method', MODE_SMA)  # smoothing type
price_field = _input('price_field', STO_LOWHIGH)  # stochastic calculation method
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
UpSTOH = Arr(0, 0.0)
DnSTOH = Arr(0, 0.0)
SIGN = Arr(0, 0.0)
ColorSTOH = Arr(0, 0.0)
ColorSIGN = Arr(0, 0.0)
min_rates_total = 0
STOH_Handle = 0

def OnInit():
    global STOH_Handle, min_rates_total
    min_rates_total = InpKPeriod + InpDPeriod + InpSlowing + 1
    STOH_Handle = iStochastic(None, 0, InpKPeriod, InpDPeriod, InpSlowing, ma_method, price_field)
    if STOH_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic indicator')
    SetIndexBuffer(0, UpSTOH, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpSTOH, True)
    SetIndexBuffer(1, DnSTOH, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(DnSTOH, True)
    SetIndexBuffer(2, ColorSTOH, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ColorSTOH, True)
    SetIndexBuffer(3, SIGN, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(SIGN, True)
    SetIndexBuffer(4, ColorSIGN, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ColorSIGN, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stoch(' + _str(InpKPeriod) + ',' + _str(InpDPeriod) + ',' + _str(InpSlowing) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(STOH_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    to_copy = 0
    Stoh = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(Stoh, True)
    to_copy = limit + 2
    if CopyBuffer(STOH_Handle, MAIN_LINE, 0, to_copy, Stoh) <= 0:
        return 0
    if CopyBuffer(STOH_Handle, SIGNAL_LINE, 0, to_copy, SIGN) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if Stoh[bar] < 50:
            DnSTOH[bar] = Stoh[bar]
            UpSTOH[bar] = 50.0
        else:
            UpSTOH[bar] = Stoh[bar]
            DnSTOH[bar] = 50.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if not prev_calculated:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ColorSTOH[bar] = 0.0
        if Stoh[bar] > 50:
            if Stoh[bar] > Stoh[bar + 1]:
                ColorSTOH[bar] = 1.0
            if Stoh[bar] < Stoh[bar + 1]:
                ColorSTOH[bar] = 2.0
        if Stoh[bar] < 50:
            if Stoh[bar] < Stoh[bar + 1]:
                ColorSTOH[bar] = 3.0
            if Stoh[bar] > Stoh[bar + 1]:
                ColorSTOH[bar] = 4.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ColorSIGN[bar] = 0.0
        if Stoh[bar] > SIGN[bar + 1]:
            ColorSIGN[bar] = 1.0
        if Stoh[bar] < SIGN[bar + 1]:
            ColorSIGN[bar] = 2.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorstochastic(_MQL5Indicator):
    name = 'colorstochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpKPeriod': 5,  # K period
        'InpDPeriod': 3,  # D period
        'InpSlowing': 3,  # Slowing
        'ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # smoothing type
        'price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # stochastic calculation method
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

