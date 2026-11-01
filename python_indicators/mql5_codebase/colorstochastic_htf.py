"""colorstochastic_htf — converted from MQL5: MQL5 Indicators/ColorStochastic_HTF/colorstochastic_htf.mq5

Stochastic oscillator with a choice of a fixed timeframe
Copyright: Copyright © 2012, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 8}, 'colors': {1: [8421376, 8721863], 2: [8421504, 65280, 16711935]}, 'widths': {2: 5}, 'styles': {2: 0}, 'labels': {1: 'Stochastic HTF', 2: 'Signal line'}, 'levels': [70.0, 50.0, 30.0], 'description': ['Stochastic oscillator with a choice of a fixed timeframe'], 'name': 'colorstochastic_htf', 'source': 'MQL5 Indicators/ColorStochastic_HTF/colorstochastic_htf.mq5', 'folder': 'ColorStochastic_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Chart period', 'sinput': False}, {'mql': 'InpKPeriod', 'py': 'InpKPeriod', 'param': 'InpKPeriod', 'type': 'int', 'default': 5, 'label': 'K period', 'sinput': False}, {'mql': 'InpDPeriod', 'py': 'InpDPeriod', 'param': 'InpDPeriod', 'type': 'int', 'default': 3, 'label': 'D period', 'sinput': False}, {'mql': 'InpSlowing', 'py': 'InpSlowing', 'param': 'InpSlowing', 'type': 'int', 'default': 3, 'label': 'Slowing', 'sinput': False}, {'mql': 'ma_method', 'py': 'ma_method', 'param': 'ma_method', 'type': 'int', 'default': 0, 'label': 'Smoothing type', 'sinput': False}, {'mql': 'price_field', 'py': 'price_field', 'param': 'price_field', 'type': 'int', 'default': 0, 'label': 'Stochastic calculation method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Chart period
InpKPeriod = _input('InpKPeriod', 5)  # K period
InpDPeriod = _input('InpDPeriod', 3)  # D period
InpSlowing = _input('InpSlowing', 3)  # Slowing
ma_method = _input('ma_method', MODE_SMA)  # Smoothing type
price_field = _input('price_field', STO_LOWHIGH)  # Stochastic calculation method
UpStochastic = Arr(0, 0.0)
DnStochastic = Arr(0, 0.0)
StochSignal = Arr(0, 0.0)
ColorStochSignal = Arr(0, 0.0)
Init = False
min_rates_total = 0
Stochastic_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Init, Stochastic_Handle, min_rates_total
    min_rates_total = 3
    Init = True
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Stochastic indicator chart period cannot be less than the current chart period')
        Init = False
        return INIT_FAILED
    Stochastic_Handle = iStochastic(None, TimeFrame, InpKPeriod, InpDPeriod, InpSlowing, ma_method, price_field)
    if Stochastic_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the Stochastic indicator')
        Init = False
        return INIT_FAILED
    SetIndexBuffer(0, UpStochastic, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpStochastic, True)
    SetIndexBuffer(1, DnStochastic, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(DnStochastic, True)
    SetIndexBuffer(2, StochSignal, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(StochSignal, True)
    SetIndexBuffer(3, ColorStochSignal, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ColorStochSignal, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stoch(' + GetStringTimeframe(TimeFrame) + ', ' + _str(InpKPeriod) + ',' + _str(InpDPeriod) + ',' + _str(InpSlowing) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total or (not Init):
        return 0
    if BarsCalculated(Stochastic_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    limit = 0
    bar = 0
    Stoch = Arr(2, 0.0, dyn=False)
    Signal = Arr(2, 0.0, dyn=False)
    StochasticTime = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        UpStochastic[bar] = EMPTY_VALUE
        DnStochastic[bar] = EMPTY_VALUE
        StochSignal[bar] = EMPTY_VALUE
        ColorStochSignal[bar] = 0.0
        if CopyTime(Symbol(), TimeFrame, _DT(time[bar]), 1, StochasticTime) <= 0:
            return 0
        if time[bar] >= StochasticTime[0] and time[bar + 1] < StochasticTime[0]:
            _s_OnCalculate_LastCountBar = bar
            if CopyBuffer(Stochastic_Handle, MAIN_LINE, _DT(time[bar]), 2, Stoch) <= 0:
                return 0
            if CopyBuffer(Stochastic_Handle, SIGNAL_LINE, _DT(time[bar]), 2, Signal) <= 0:
                return 0
            StochSignal[bar] = Signal[1]
            UpStochastic[bar] = 50.0
            DnStochastic[bar] = 50.0
            if Stoch[1] > 50:
                UpStochastic[bar] = Stoch[1]
            if Stoch[1] < 50:
                UpStochastic[bar] = Stoch[1]
            if Stoch[1] > StochSignal[bar]:
                ColorStochSignal[bar] = 1.0
            if Stoch[1] < StochSignal[bar]:
                ColorStochSignal[bar] = 2.0
        if UpStochastic[bar + 1] != EMPTY_VALUE and UpStochastic[bar] == EMPTY_VALUE:
            UpStochastic[bar] = UpStochastic[bar + 1]
            DnStochastic[bar] = DnStochastic[bar + 1]
            StochSignal[bar] = StochSignal[bar + 1]
            ColorStochSignal[bar] = ColorStochSignal[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorstochasticHtf(_MQL5Indicator):
    name = 'colorstochastic_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Chart period
        'InpKPeriod': 5,  # K period
        'InpDPeriod': 3,  # D period
        'InpSlowing': 3,  # Slowing
        'ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Smoothing type
        'price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stochastic calculation method
    }

