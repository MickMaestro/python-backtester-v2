"""KWAN_NRP — converted from MQL5: MQL5 Indicators/KWAN_NRP_HTF/KWAN_NRP.mq5

Metatrader4 Code by jjk2. Based on MBA Thesis from Simon Fraser University written by C.E. ALDEA.
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [7451452, 8421504, 16711935]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'KWAN_NRP'}, 'levels': [], 'description': ['Metatrader4 Code by jjk2. Based on MBA Thesis from Simon Fraser University written by C.E. ALDEA.'], 'name': 'KWAN_NRP', 'source': 'MQL5 Indicators/KWAN_NRP_HTF/KWAN_NRP.mq5', 'folder': 'KWAN_NRP_HTF', 'inputs': [{'mql': 'InpKPeriod', 'py': 'InpKPeriod', 'param': 'InpKPeriod', 'type': 'uint', 'default': 5, 'label': 'K period', 'sinput': False}, {'mql': 'InpDPeriod', 'py': 'InpDPeriod', 'param': 'InpDPeriod', 'type': 'uint', 'default': 3, 'label': 'D period', 'sinput': False}, {'mql': 'InpSlowing', 'py': 'InpSlowing', 'param': 'InpSlowing', 'type': 'uint', 'default': 3, 'label': 'Slowing', 'sinput': False}, {'mql': 'ma_method', 'py': 'ma_method', 'param': 'ma_method', 'type': 'int', 'default': 0, 'label': 'тип сглаживания', 'sinput': False}, {'mql': 'price_field', 'py': 'price_field', 'param': 'price_field', 'type': 'int', 'default': 0, 'label': 'способ расчета стохастика', 'sinput': False}, {'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'uint', 'default': 14, 'label': 'период индикатора RSI', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': 'цена RSI', 'sinput': False}, {'mql': 'MomentumPeriod', 'py': 'MomentumPeriod', 'param': 'MomentumPeriod', 'type': 'uint', 'default': 14, 'label': 'Период индикатора Momentum', 'sinput': False}, {'mql': 'MomentumPrice', 'py': 'MomentumPrice', 'param': 'MomentumPrice', 'type': 'int', 'default': 1, 'label': 'Цена индикатора Momentum', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 3, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
InpKPeriod = _input('InpKPeriod', 5)  # K period
InpDPeriod = _input('InpDPeriod', 3)  # D period
InpSlowing = _input('InpSlowing', 3)  # Slowing
ma_method = _input('ma_method', MODE_SMA)  # тип сглаживания
price_field = _input('price_field', STO_LOWHIGH)  # способ расчета стохастика
RSIPeriod = _input('RSIPeriod', 14)  # период индикатора RSI
RSIPrice = _input('RSIPrice', PRICE_CLOSE)  # цена RSI
MomentumPeriod = _input('MomentumPeriod', 14)  # Период индикатора Momentum
MomentumPrice = _input('MomentumPrice', PRICE_CLOSE)  # Цена индикатора Momentum
XMA_Method = _input('XMA_Method', MODE_SMA_)  # метод усреднения
XLength = _input('XLength', 3)  # глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр сглаживания,
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_1 = 0
min_rates_total = 0
Stoch_Handle = 0
RSI_Handle = 0
Mom_Handle = 0

def OnInit():
    global Mom_Handle, RSI_Handle, Stoch_Handle, min_rates_1, min_rates_total
    min_rates_1 = _int(InpKPeriod + InpDPeriod + InpSlowing + 1)
    min_rates_1 = _int(MathMax(min_rates_1, MathMax(RSIPeriod, MomentumPeriod)))
    min_rates_total = min_rates_1 + GetStartBars(XMA_Method, XLength, XPhase)
    Stoch_Handle = iStochastic(None, 0, InpKPeriod, InpDPeriod, InpSlowing, ma_method, price_field)
    if Stoch_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iStochastic')
        return INIT_FAILED
    RSI_Handle = iRSI(None, 0, RSIPeriod, RSIPrice)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI')
        return INIT_FAILED
    Mom_Handle = iMomentum(Symbol(), PERIOD_CURRENT, MomentumPeriod, MomentumPrice)
    if Mom_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMomentum')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ColorIndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'KWAN_NRP')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((BarsCalculated(Stoch_Handle) < rates_total or BarsCalculated(RSI_Handle) < rates_total) or BarsCalculated(Mom_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    to_copy = 0
    maxbar = 0
    Stoch = Arr(0, 0.0)
    RSI = Arr(0, 0.0)
    Mom = Arr(0, 0.0)
    kwan = 0.0
    maxbar = rates_total - min_rates_total - 1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(Stoch, True)
    ArraySetAsSeries(RSI, True)
    ArraySetAsSeries(Mom, True)
    if CopyBuffer(Stoch_Handle, SIGNAL_LINE, 0, to_copy, Stoch) <= 0:
        return 0
    if CopyBuffer(RSI_Handle, 0, 0, to_copy, RSI) <= 0:
        return 0
    if CopyBuffer(Mom_Handle, 0, 0, to_copy, Mom) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if Mom[bar]:
            kwan = _fdiv(Stoch[bar] * RSI[bar], Mom[bar])
        else:
            kwan = 100.0
        IndBuffer[bar] = XMA1.XMASeries(maxbar, prev_calculated, rates_total, XMA_Method, XPhase, XLength, kwan, bar, True)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if not prev_calculated:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ColorIndBuffer[bar] = 1.0
        if IndBuffer[bar] > IndBuffer[bar + 1]:
            ColorIndBuffer[bar] = 0.0
        if IndBuffer[bar] < IndBuffer[bar + 1]:
            ColorIndBuffer[bar] = 2.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KWANNRP(_MQL5Indicator):
    name = 'KWAN_NRP'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpKPeriod': 5,  # K period
        'InpDPeriod': 3,  # D period
        'InpSlowing': 3,  # Slowing
        'ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # тип сглаживания
        'price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # способ расчета стохастика
        'RSIPeriod': 14,  # период индикатора RSI
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # цена RSI
        'MomentumPeriod': 14,  # Период индикатора Momentum
        'MomentumPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Цена индикатора Momentum
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения
        'XLength': 3,  # глубина сглаживания
        'XPhase': 15,  # параметр сглаживания,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

