"""colorstochnr — converted from MQL5: MQL5 Indicators/ColorStochNR_HTF/colorstochnr.mq5

Стохастический осциллятор с подавлением шума, выполненный в виде цветной гистограммы
Copyright: Copyright © 2010, Svinozavr; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Svinozavr', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 11, 2: 8}, 'colors': {1: [8421504, 11186720, 16748574, 9639167, 16711935], 2: [8421504, 65280, 16711935]}, 'widths': {1: 3, 2: 2}, 'styles': {1: 0, 2: 1}, 'labels': {1: 'Main', 2: 'Signal'}, 'levels': [70.0, 50.0, 30.0], 'description': ['Стохастический осциллятор с подавлением шума, выполненный в виде цветной гистограммы'], 'name': 'colorstochnr', 'source': 'MQL5 Indicators/ColorStochNR_HTF/colorstochnr.mq5', 'folder': 'ColorStochNR_HTF', 'inputs': [{'mql': 'Kperiod', 'py': 'Kperiod', 'param': 'Kperiod', 'type': 'uint', 'default': 5, 'label': 'K period', 'sinput': False}, {'mql': 'Dperiod', 'py': 'Dperiod', 'param': 'Dperiod', 'type': 'uint', 'default': 3, 'label': 'D period', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'uint', 'default': 3, 'label': 'Slowing', 'sinput': False}, {'mql': 'Dmethod', 'py': 'Dmethod', 'param': 'Dmethod', 'type': 'int', 'default': 0, 'label': 'Тип сглаживания', 'sinput': False}, {'mql': 'PriceFild', 'py': 'PriceFild', 'param': 'PriceFild', 'type': 'int', 'default': 0, 'label': 'Способ расчета стохастика', 'sinput': False}, {'mql': 'Sens', 'py': 'Sens', 'param': 'Sens', 'type': 'uint', 'default': 0, 'label': 'Чувствительность в пунктах', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_MA_METHOD_
MODE_SMA_ = 0
MODE_EMA_ = 1
_enum('ENUM_MA_METHOD_', {0: 'MODE_SMA_', 1: 'MODE_EMA_'})

# ---- inputs and global variables
Kperiod = _input('Kperiod', 5)  # K period
Dperiod = _input('Dperiod', 3)  # D period
Slowing = _input('Slowing', 3)  # Slowing
Dmethod = _input('Dmethod', MODE_SMA_)  # Тип сглаживания
PriceFild = _input('PriceFild', STO_LOWHIGH)  # Способ расчета стохастика
Sens = _input('Sens', 0)  # Чувствительность в пунктах
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
UpSTOH = Arr(0, 0.0)
DnSTOH = Arr(0, 0.0)
SIGN = Arr(0, 0.0)
ColorSTOH = Arr(0, 0.0)
ColorSIGN = Arr(0, 0.0)
min_rates_total = 0
sens = 0.0  # чувствительность в ценах
kd = 0.0  # коэфф. EMA для сигнальной

def OnInit():
    global kd, min_rates_total, sens
    min_rates_total = _int(Kperiod + Dperiod + Slowing + 1)
    sens = Sens * Point()
    if Dmethod == MODE_EMA_:
        kd = 2.0 / (1 + Dperiod)
    SetIndexBuffer(0, UpSTOH, INDICATOR_DATA)
    ArraySetAsSeries(UpSTOH, True)
    SetIndexBuffer(1, DnSTOH, INDICATOR_DATA)
    ArraySetAsSeries(DnSTOH, True)
    SetIndexBuffer(2, ColorSTOH, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorSTOH, True)
    SetIndexBuffer(3, SIGN, INDICATOR_DATA)
    ArraySetAsSeries(SIGN, True)
    SetIndexBuffer(4, ColorSIGN, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorSIGN, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'StochNR(' + _str(Kperiod) + ',' + _str(Dperiod) + ',' + _str(Slowing) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    Main = 0.0
    prevMain = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        SIGN[limit + 1] = 50.0
        bar = rates_total - 1
        for bar in range(bar, limit, -1):
            UpSTOH[bar] = 50.0
            DnSTOH[bar] = 50.0
        else:
            bar = _range_end(bar, limit, -1)
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Main = Stoch(Kperiod, Slowing, PriceFild, sens, high, low, close, bar)
        if Main < 50:
            DnSTOH[bar] = Main
            UpSTOH[bar] = 50.0
        else:
            UpSTOH[bar] = Main
            DnSTOH[bar] = 50.0
        _sw1 = Dmethod
        if _sw1 == MODE_EMA_:
            SIGN[bar] = (kd * Main) + ((1 - kd) * SIGN[bar + 1])
        elif _sw1 == MODE_SMA_:
            sh = _int(bar + Dperiod)
            OldMain = UpSTOH[sh] + DnSTOH[sh] - 50
            sum_ = (SIGN[bar + 1] * Dperiod) - OldMain
            SIGN[bar] = (sum_ + Main) / Dperiod
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if not prev_calculated:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ColorSTOH[bar] = 0.0
        Main = UpSTOH[bar] + DnSTOH[bar] - 50
        prevMain = UpSTOH[bar + 1] + DnSTOH[bar + 1] - 50
        if Main > 50:
            if Main > prevMain:
                ColorSTOH[bar] = 1.0
            if Main < prevMain:
                ColorSTOH[bar] = 2.0
        if Main < 50:
            if Main < prevMain:
                ColorSTOH[bar] = 3.0
            if Main > prevMain:
                ColorSTOH[bar] = 4.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ColorSIGN[bar] = 0.0
        Main = UpSTOH[bar] + DnSTOH[bar] - 50
        if Main > SIGN[bar]:
            ColorSIGN[bar] = 1.0
        if Main < SIGN[bar]:
            ColorSIGN[bar] = 2.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def Stoch(Kperiod_, Slowing_, PriceFild_, Sens_, High, Low, Close, index):
    delta = 0.0
    sens2 = 0.0
    s0 = 0.0
    max_ = 0.0
    min_ = 0.0
    closesum = 0.0
    for j in range(index, index + Slowing_):
        if PriceFild_ == STO_CLOSECLOSE:
            max_ += Close[ArrayMaximum(Close, j, Kperiod_)]
            min_ += Close[ArrayMinimum(Close, j, Kperiod_)]
        else:
            max_ += High[ArrayMaximum(High, j, Kperiod_)]
            min_ += Low[ArrayMinimum(Low, j, Kperiod_)]
        closesum += Close[j]
    delta = max_ - min_
    if delta < Sens_:
        sens2 = Sens_ / 2
        max_ += sens2
        min_ -= sens2
    delta = max_ - min_
    if delta:
        s0 = _fdiv(closesum - min_, delta)
    else:
        s0 = 1.0
    return 100 * s0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorstochnr(_MQL5Indicator):
    name = 'colorstochnr'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Kperiod': 5,  # K period
        'Dperiod': 3,  # D period
        'Slowing': 3,  # Slowing
        'Dmethod': _Choice({0: 'Простое усреднение', 1: 'Экспоненциальное'}, default=0),  # Тип сглаживания
        'PriceFild': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Способ расчета стохастика
        'Sens': 0,  # Чувствительность в пунктах
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

