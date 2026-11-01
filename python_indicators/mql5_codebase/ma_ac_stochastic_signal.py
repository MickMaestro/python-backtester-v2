"""ma_ac_stochastic_signal — converted from MQL5: MQL5 Indicators/MA_AC_Stochastic_Signal/ma_ac_stochastic_signal.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 10}, 'colors': {1: [8388736, 8421376], 2: [8421504, 255, 65280]}, 'widths': {2: 5}, 'styles': {}, 'labels': {1: 'MA Signal', 2: 'AC Stochastic Signal'}, 'levels': [], 'description': [], 'name': 'ma_ac_stochastic_signal', 'source': 'MQL5 Indicators/MA_AC_Stochastic_Signal/ma_ac_stochastic_signal.mq5', 'folder': 'MA_AC_Stochastic_Signal', 'inputs': [{'mql': 'MA_Period', 'py': 'MA_Period', 'param': 'MA_Period', 'type': 'int', 'default': 9, 'label': 'MA period', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'MA_Price', 'py': 'MA_Price', 'param': 'MA_Price', 'type': 'int', 'default': 1, 'label': 'Prices calculation method', 'sinput': False}, {'mql': 'STO_Period', 'py': 'STO_Period', 'param': 'STO_Period', 'type': 'int', 'default': 5, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'STO_Slowing', 'py': 'STO_Slowing', 'param': 'STO_Slowing', 'type': 'int', 'default': 3, 'label': 'Stochastic slowing', 'sinput': False}, {'mql': 'STO_Method', 'py': 'STO_Method', 'param': 'STO_Method', 'type': 'int', 'default': 0, 'label': 'Stochastic smoothing method', 'sinput': False}, {'mql': 'STO_Price', 'py': 'STO_Price', 'param': 'STO_Price', 'type': 'int', 'default': 0, 'label': 'Stochastic prices calculation method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MA_Period = _input('MA_Period', 9)  # MA period
MA_Method = _input('MA_Method', MODE_SMA)  # Smoothing method
MA_Price = _input('MA_Price', PRICE_CLOSE)  # Prices calculation method
STO_Period = _input('STO_Period', 5)  # Stochastic period
STO_Slowing = _input('STO_Slowing', 3)  # Stochastic slowing
STO_Method = _input('STO_Method', MODE_SMA)  # Stochastic smoothing method
STO_Price = _input('STO_Price', STO_LOWHIGH)  # Stochastic prices calculation method
MA_Handle = 0
AC_Handle = 0
STO_Handle = 0
min_rates_total = 0
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
ExtCBuffer = Arr(0, 0.0)
ExtColorCBuffer = Arr(0, 0.0)

def OnInit():
    global AC_Handle, MA_Handle, STO_Handle, min_rates_total
    min_rates_total = MathMax(37 + 1, MathMax(MA_Period, STO_Period + STO_Slowing))
    MA_Handle = iMA(None, 0, MA_Period, 0, STO_Method, STO_Price)
    if MA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the MA indicator')
    STO_Handle = iStochastic(None, 0, STO_Period, 3, STO_Slowing, STO_Method, STO_Price)
    if STO_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the Stochastic indicator')
    AC_Handle = iAC(None, 0)
    if AC_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the AC indicator')
    SetIndexBuffer(0, ExtABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtABuffer, True)
    SetIndexBuffer(1, ExtBBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtBBuffer, True)
    SetIndexBuffer(2, ExtCBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtCBuffer, True)
    SetIndexBuffer(3, ExtColorCBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtColorCBuffer, True)
    shortname = 'MA AC Stochastic_Signal'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 1)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    global _s_OnCalculate_trend
    if ((BarsCalculated(MA_Handle) < rates_total or BarsCalculated(AC_Handle) < rates_total) or BarsCalculated(STO_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    STO = Arr(0, 0.0)
    AC = Arr(0, 0.0)
    MA = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_trend = 0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MA) <= 0:
        return 0
    if CopyBuffer(STO_Handle, 0, 0, to_copy, STO) <= 0:
        return 0
    to_copy += 1
    if CopyBuffer(AC_Handle, 0, 0, to_copy, AC) <= 0:
        return 0
    ArraySetAsSeries(MA, True)
    ArraySetAsSeries(STO, True)
    ArraySetAsSeries(AC, True)
    ArraySetAsSeries(Close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if Close[bar] > MA[bar]:
            ExtBBuffer[bar] = 1.0
            ExtABuffer[bar] = 0.0
        if Close[bar] <= MA[bar]:
            ExtBBuffer[bar] = -1.0
            ExtABuffer[bar] = 0.0
        ExtCBuffer[bar] = 0.0
        ExtColorCBuffer[bar] = 0.0
        if ((AC[bar] > 0 and AC[bar] > AC[bar + 1]) and STO[bar] > 50) and _s_OnCalculate_trend != 1:
            ExtCBuffer[bar] = 1.0
            ExtColorCBuffer[bar] = 2.0
            if bar:
                _s_OnCalculate_trend = 1
        if ((AC[bar] < 0 and AC[bar] < AC[bar + 1]) and STO[bar] < 50) and _s_OnCalculate_trend != -1:
            ExtCBuffer[bar] = -1.0
            ExtColorCBuffer[bar] = 1.0
            if bar:
                _s_OnCalculate_trend = -1
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_trend = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MaAcStochasticSignal(_MQL5Indicator):
    name = 'ma_ac_stochastic_signal'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Period': 9,  # MA period
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Smoothing method
        'MA_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Prices calculation method
        'STO_Period': 5,  # Stochastic period
        'STO_Slowing': 3,  # Stochastic slowing
        'STO_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Stochastic smoothing method
        'STO_Price': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stochastic prices calculation method
    }

