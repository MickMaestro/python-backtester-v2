"""RVIWithFlat — converted from MQL5: MQL5 Indicators/RVIWithFlat_HTF/RVIWithFlat.mq5

Relative Vigor Index With Flat
Copyright: Copyright © 2014, Powered byStep; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Powered byStep', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 7, 2: 1}, 'colors': {1: [8421376, 16711935], 2: [16711680]}, 'widths': {2: 5}, 'styles': {2: 0}, 'labels': {1: 'RVI Oscillator', 2: 'Flat'}, 'levels': [0.0], 'description': ['Relative Vigor Index With Flat'], 'name': 'RVIWithFlat', 'source': 'MQL5 Indicators/RVIWithFlat_HTF/RVIWithFlat.mq5', 'folder': 'RVIWithFlat_HTF', 'inputs': [{'mql': 'BBPeriod', 'py': 'BBPeriod', 'param': 'BBPeriod', 'type': 'uint', 'default': 20, 'label': 'Период для расчета Боллинджера', 'sinput': False}, {'mql': 'StdDeviation', 'py': 'StdDeviation', 'param': 'StdDeviation', 'type': 'double', 'default': 2.0, 'label': 'Девиация Боллинджера', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 1, 'label': 'Тип цены Боллинджера', 'sinput': False}, {'mql': 'RVIPeriod', 'py': 'RVIPeriod', 'param': 'RVIPeriod', 'type': 'uint', 'default': 14, 'label': 'Период RVI', 'sinput': False}, {'mql': 'flat', 'py': 'flat', 'param': 'flat', 'type': 'uint', 'default': 100, 'label': 'величина флэта в пунктах', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BBPeriod = _input('BBPeriod', 20)  # Период для расчета Боллинджера
StdDeviation = _input('StdDeviation', 2.0)  # Девиация Боллинджера
applied_price = _input('applied_price', PRICE_CLOSE)  # Тип цены Боллинджера
RVIPeriod = _input('RVIPeriod', 14)  # Период RVI
flat = _input('flat', 100)  # величина флэта в пунктах
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
SignalBuffer = Arr(0, 0.0)
IndBuffer1 = Arr(0, 0.0)
BB_Handle = 0
RVI_Handle = 0
min_rates_total = 0

def OnInit():
    global BB_Handle, RVI_Handle, min_rates_total
    min_rates_total = _int(MathMax(BBPeriod, RVIPeriod))
    BB_Handle = iBands(Symbol(), PERIOD_CURRENT, BBPeriod, 0, StdDeviation, applied_price)
    if BB_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iBands')
        return INIT_FAILED
    RVI_Handle = iRVI(Symbol(), PERIOD_CURRENT, RVIPeriod)
    if RVI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRVI')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, SignalBuffer, INDICATOR_DATA)
    ArraySetAsSeries(SignalBuffer, True)
    SetIndexBuffer(2, IndBuffer1, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer1, True)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RVIWithFlat')
    IndicatorSetInteger(INDICATOR_DIGITS, 4)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(BB_Handle) < rates_total or BarsCalculated(RVI_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    MainRVI = Arr(0, 0.0)
    SignRVI = Arr(0, 0.0)
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
    if CopyBuffer(RVI_Handle, MAIN_LINE, 0, to_copy, MainRVI) <= 0:
        return 0
    if CopyBuffer(RVI_Handle, SIGNAL_LINE, 0, to_copy, SignRVI) <= 0:
        return 0
    ArraySetAsSeries(UpBB, True)
    ArraySetAsSeries(MainBB, True)
    ArraySetAsSeries(MainRVI, True)
    ArraySetAsSeries(SignRVI, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        res = _fdiv(UpBB[bar] - MainBB[bar], Point())
        if res < flat:
            if MainRVI[bar] > SignRVI[bar]:
                IndBuffer[bar] = 1e-09
                SignalBuffer[bar] = 1e-09
                IndBuffer1[bar] = 0.0
            if MainRVI[bar] < SignRVI[bar]:
                IndBuffer[bar] = 1e-09
                SignalBuffer[bar] = 1e-09
                IndBuffer1[bar] = 0.0
        else:
            IndBuffer1[bar] = EMPTY_VALUE
            IndBuffer[bar] = MainRVI[bar]
            SignalBuffer[bar] = SignRVI[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RVIWithFlat(_MQL5Indicator):
    name = 'RVIWithFlat'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BBPeriod': 20,  # Период для расчета Боллинджера
        'StdDeviation': 2.0,  # Девиация Боллинджера
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Тип цены Боллинджера
        'RVIPeriod': 14,  # Период RVI
        'flat': 100,  # величина флэта в пунктах
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

