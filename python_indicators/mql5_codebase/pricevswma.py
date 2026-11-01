"""pricevswma — converted from MQL5: MQL5 Indicators/PriceVSwma/pricevswma.mq5

Copyright: Copyright © 2007, perky_z; Link: perky_z@yahoo.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, perky_z', 'link': 'perky_z@yahoo.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [36095], 2: [14822282]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'PriceVSwma', 2: 'Signal PriceVSwma'}, 'levels': [70.0, 30.0], 'description': [], 'name': 'pricevswma', 'source': 'MQL5 Indicators/PriceVSwma/pricevswma.mq5', 'folder': 'PriceVSwma', 'inputs': [{'mql': 'InpKPeriod1', 'py': 'InpKPeriod1', 'param': 'InpKPeriod1', 'type': 'uint', 'default': 8, 'label': 'K period 1', 'sinput': False}, {'mql': 'InpDPeriod1', 'py': 'InpDPeriod1', 'param': 'InpDPeriod1', 'type': 'uint', 'default': 3, 'label': 'D period 1', 'sinput': False}, {'mql': 'InpKPeriod2', 'py': 'InpKPeriod2', 'param': 'InpKPeriod2', 'type': 'uint', 'default': 89, 'label': 'K period 2', 'sinput': False}, {'mql': 'InpDPeriod2', 'py': 'InpDPeriod2', 'param': 'InpDPeriod2', 'type': 'uint', 'default': 21, 'label': 'D period 2', 'sinput': False}, {'mql': 'InpKPeriod3', 'py': 'InpKPeriod3', 'param': 'InpKPeriod3', 'type': 'uint', 'default': 55, 'label': 'K period 3', 'sinput': False}, {'mql': 'InpDPeriod3', 'py': 'InpDPeriod3', 'param': 'InpDPeriod3', 'type': 'uint', 'default': 13, 'label': 'D period 3', 'sinput': False}, {'mql': 'InpKPeriod4', 'py': 'InpKPeriod4', 'param': 'InpKPeriod4', 'type': 'uint', 'default': 34, 'label': 'K period 4', 'sinput': False}, {'mql': 'InpDPeriod4', 'py': 'InpDPeriod4', 'param': 'InpDPeriod4', 'type': 'uint', 'default': 8, 'label': 'D period 4', 'sinput': False}, {'mql': 'InpKPeriod5', 'py': 'InpKPeriod5', 'param': 'InpKPeriod5', 'type': 'uint', 'default': 21, 'label': 'K period 5', 'sinput': False}, {'mql': 'InpDPeriod5', 'py': 'InpDPeriod5', 'param': 'InpDPeriod5', 'type': 'uint', 'default': 5, 'label': 'D period 5', 'sinput': False}, {'mql': 'InpSlowing', 'py': 'InpSlowing', 'param': 'InpSlowing', 'type': 'uint', 'default': 3, 'label': 'Slowing', 'sinput': False}, {'mql': 'ma_method', 'py': 'ma_method', 'param': 'ma_method', 'type': 'int', 'default': 0, 'label': 'smoothing type', 'sinput': False}, {'mql': 'price_field', 'py': 'price_field', 'param': 'price_field', 'type': 'int', 'default': 0, 'label': 'stochastic calculation method', 'sinput': False}, {'mql': 'Smoothing', 'py': 'Smoothing', 'param': 'Smoothing', 'type': 'uint', 'default': 15, 'label': 'indicator smoothing', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'uint', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpKPeriod1 = _input('InpKPeriod1', 8)  # K period 1
InpDPeriod1 = _input('InpDPeriod1', 3)  # D period 1
InpKPeriod2 = _input('InpKPeriod2', 89)  # K period 2
InpDPeriod2 = _input('InpDPeriod2', 21)  # D period 2
InpKPeriod3 = _input('InpKPeriod3', 55)  # K period 3
InpDPeriod3 = _input('InpDPeriod3', 13)  # D period 3
InpKPeriod4 = _input('InpKPeriod4', 34)  # K period 4
InpDPeriod4 = _input('InpDPeriod4', 8)  # D period 4
InpKPeriod5 = _input('InpKPeriod5', 21)  # K period 5
InpDPeriod5 = _input('InpDPeriod5', 5)  # D period 5
InpSlowing = _input('InpSlowing', 3)  # Slowing
ma_method = _input('ma_method', MODE_SMA)  # smoothing type
price_field = _input('price_field', STO_LOWHIGH)  # stochastic calculation method
Smoothing = _input('Smoothing', 15)  # indicator smoothing
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
SignBuffer = Arr(0, 0.0)
CP_Handle = 0
STOH_Handle = Arr(5, 0, dyn=False)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates = Arr(5, 0, dyn=False)
    min_rates[0] = InpKPeriod1 + InpDPeriod1 + InpSlowing
    min_rates[1] = InpKPeriod2 + InpDPeriod2 + InpSlowing
    min_rates[2] = InpKPeriod3 + InpDPeriod3 + InpSlowing
    min_rates[3] = InpKPeriod4 + InpDPeriod4 + InpSlowing
    min_rates[4] = InpKPeriod5 + InpDPeriod5 + InpSlowing
    ArraySetAsSeries(min_rates, True)
    min_rates_total = _int(min_rates[ArrayMaximum(min_rates, 0, 5)])
    STOH_Handle[0] = iStochastic(None, 0, InpKPeriod1, InpDPeriod1, InpSlowing, ma_method, price_field)
    if STOH_Handle[0] == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic 1 indicator')
    STOH_Handle[1] = iStochastic(None, 0, InpKPeriod2, InpDPeriod2, InpSlowing, ma_method, price_field)
    if STOH_Handle[1] == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic 2 indicator')
    STOH_Handle[2] = iStochastic(None, 0, InpKPeriod3, InpDPeriod3, InpSlowing, ma_method, price_field)
    if STOH_Handle[2] == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic 3 indicator')
    STOH_Handle[3] = iStochastic(None, 0, InpKPeriod4, InpDPeriod4, InpSlowing, ma_method, price_field)
    if STOH_Handle[3] == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic 4 indicator')
    STOH_Handle[4] = iStochastic(None, 0, InpKPeriod5, InpDPeriod5, InpSlowing, ma_method, price_field)
    if STOH_Handle[4] == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic 5 indicator')
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, SignBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SignBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'PriceVSwma')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for count in range(0, 5):
        if BarsCalculated(STOH_Handle[count]) < rates_total:
            return 0
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    to_copy = 0
    Sto1 = Arr(0, 0.0)
    Sto2 = Arr(0, 0.0)
    Sto3 = Arr(0, 0.0)
    Sto4 = Arr(0, 0.0)
    Sto5 = Arr(0, 0.0)
    stoh1 = 0.0
    stoh2 = 0.0
    stoh3 = 0.0
    stoh4 = 0.0
    stoh5 = 0.0
    mov = 0.0
    stohsmoothed = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        SignBuffer[limit + 1] = 0.0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(Sto1, True)
    ArraySetAsSeries(Sto2, True)
    ArraySetAsSeries(Sto3, True)
    ArraySetAsSeries(Sto4, True)
    ArraySetAsSeries(Sto5, True)
    if CopyBuffer(STOH_Handle[0], MAIN_LINE, 0, to_copy, Sto1) <= 0:
        return 0
    if CopyBuffer(STOH_Handle[1], MAIN_LINE, 0, to_copy, Sto2) <= 0:
        return 0
    if CopyBuffer(STOH_Handle[2], MAIN_LINE, 0, to_copy, Sto3) <= 0:
        return 0
    if CopyBuffer(STOH_Handle[3], MAIN_LINE, 0, to_copy, Sto4) <= 0:
        return 0
    if CopyBuffer(STOH_Handle[4], MAIN_LINE, 0, to_copy, Sto5) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        stoh1 = Sto1[bar] * 0.05
        stoh2 = Sto2[bar] * 0.43
        stoh3 = Sto3[bar] * 0.26
        stoh4 = Sto4[bar] * 0.16
        stoh5 = Sto5[bar] * 0.1
        mov = stoh1 + stoh2 + stoh3 + stoh4 + stoh5
        stohsmoothed = (mov / Smoothing) + ((SignBuffer[bar + 1] * (Smoothing - 1)) / Smoothing)
        IndBuffer[bar] = mov
        SignBuffer[bar] = stohsmoothed
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Pricevswma(_MQL5Indicator):
    name = 'pricevswma'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpKPeriod1': 8,  # K period 1
        'InpDPeriod1': 3,  # D period 1
        'InpKPeriod2': 89,  # K period 2
        'InpDPeriod2': 21,  # D period 2
        'InpKPeriod3': 55,  # K period 3
        'InpDPeriod3': 13,  # D period 3
        'InpKPeriod4': 34,  # K period 4
        'InpDPeriod4': 8,  # D period 4
        'InpKPeriod5': 21,  # K period 5
        'InpDPeriod5': 5,  # D period 5
        'InpSlowing': 3,  # Slowing
        'ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # smoothing type
        'price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # stochastic calculation method
        'Smoothing': 15,  # indicator smoothing
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

