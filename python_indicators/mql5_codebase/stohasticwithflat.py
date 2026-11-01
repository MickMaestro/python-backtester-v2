"""stohasticwithflat — converted from MQL5: MQL5 Indicators/StohasticWithFlat/stohasticwithflat.mq5

Stochastic indicator With Flat
Copyright: Copyright © 2014, Powered byStep; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Powered byStep', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2, 'indicator_minimum': 0.0, 'indicator_maximum': 100.0}, 'types': {1: 1, 2: 1}, 'colors': {1: [14053594], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Stohastic Oscillator', 2: 'Signal'}, 'levels': [75.0, 50.0, 25.0], 'description': ['Stochastic indicator With Flat'], 'name': 'stohasticwithflat', 'source': 'MQL5 Indicators/StohasticWithFlat/stohasticwithflat.mq5', 'folder': 'StohasticWithFlat', 'inputs': [{'mql': 'BBPeriod', 'py': 'BBPeriod', 'param': 'BBPeriod', 'type': 'uint', 'default': 20, 'label': 'Период для расчета Боллинджера', 'sinput': False}, {'mql': 'StdDeviation', 'py': 'StdDeviation', 'param': 'StdDeviation', 'type': 'double', 'default': 2.0, 'label': 'Кол-во отклонений Боллинджера', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 1, 'label': 'Тип цены Боллинджера', 'sinput': False}, {'mql': 'KPeriod', 'py': 'KPeriod', 'param': 'KPeriod', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field', 'py': 'Price_field', 'param': 'Price_field', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'flat', 'py': 'flat', 'param': 'flat', 'type': 'uint', 'default': 100, 'label': 'Величина флэта в пунктах', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BBPeriod = _input('BBPeriod', 20)  # Период для расчета Боллинджера
StdDeviation = _input('StdDeviation', 2.0)  # Кол-во отклонений Боллинджера
applied_price = _input('applied_price', PRICE_CLOSE)  # Тип цены Боллинджера
KPeriod = _input('KPeriod', 5)
DPeriod = _input('DPeriod', 3)
Slowing = _input('Slowing', 3)
MA_Method = _input('MA_Method', MODE_SMA)
Price_field = _input('Price_field', STO_LOWHIGH)
flat = _input('flat', 100)  # Величина флэта в пунктах
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
SignalBuffer = Arr(0, 0.0)
BB_Handle = 0
STO_Handle = 0
min_rates_total = 0

def OnInit():
    global BB_Handle, STO_Handle, min_rates_total
    min_rates_total = _int(MathMax(BBPeriod, KPeriod + DPeriod + Slowing))
    BB_Handle = iBands(Symbol(), PERIOD_CURRENT, BBPeriod, 0, StdDeviation, applied_price)
    if BB_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iBands')
        return INIT_FAILED
    STO_Handle = iStochastic(Symbol(), PERIOD_CURRENT, KPeriod, DPeriod, Slowing, MA_Method, Price_field)
    if STO_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iStochastic')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, SignalBuffer, INDICATOR_DATA)
    ArraySetAsSeries(SignalBuffer, True)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'StohasticWithFlat')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(BB_Handle) < rates_total or BarsCalculated(STO_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    MainSTO = Arr(0, 0.0)
    SignSTO = Arr(0, 0.0)
    UpBB = Arr(0, 0.0)
    MainBB = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(BB_Handle, UPPER_BAND, 0, to_copy, UpBB) <= 0:
        return 0
    if CopyBuffer(BB_Handle, BASE_LINE, 0, to_copy, MainBB) <= 0:
        return 0
    if CopyBuffer(STO_Handle, MAIN_LINE, 0, to_copy, MainSTO) <= 0:
        return 0
    if CopyBuffer(STO_Handle, SIGNAL_LINE, 0, to_copy, SignSTO) <= 0:
        return 0
    ArraySetAsSeries(UpBB, True)
    ArraySetAsSeries(MainBB, True)
    ArraySetAsSeries(MainSTO, True)
    ArraySetAsSeries(SignSTO, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        res = _fdiv(UpBB[bar] - MainBB[bar], Point())
        if res < flat:
            if MainSTO[bar] > SignSTO[bar]:
                IndBuffer[bar] = 55.0
                SignalBuffer[bar] = 45.0
            if MainSTO[bar] < SignSTO[bar]:
                IndBuffer[bar] = 45.0
                SignalBuffer[bar] = 55.0
        else:
            IndBuffer[bar] = MainSTO[bar]
            SignalBuffer[bar] = SignSTO[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Stohasticwithflat(_MQL5Indicator):
    name = 'stohasticwithflat'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BBPeriod': 20,  # Период для расчета Боллинджера
        'StdDeviation': 2.0,  # Кол-во отклонений Боллинджера
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Тип цены Боллинджера
        'KPeriod': 5,
        'DPeriod': 3,
        'Slowing': 3,
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'flat': 100,  # Величина флэта в пунктах
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }
    y_range = (0.0, 100.0)

