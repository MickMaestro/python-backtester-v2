"""asymmetricstochnr_sign — converted from MQL5: MQL5 Indicators/AsymmetricStochNR_Sign/asymmetricstochnr_sign.mq5

Asymmetric Stoch NR
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16760576], 2: [14524637]}, 'widths': {1: 5, 2: 5}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Buy AsymmetricStochNR signal', 2: 'Sell AsymmetricStochNR signal'}, 'levels': [], 'description': ['Asymmetric Stoch NR'], 'name': 'asymmetricstochnr_sign', 'source': 'MQL5 Indicators/AsymmetricStochNR_Sign/asymmetricstochnr_sign.mq5', 'folder': 'AsymmetricStochNR_Sign', 'inputs': [{'mql': 'KperiodShort', 'py': 'KperiodShort', 'param': 'KperiodShort', 'type': 'uint', 'default': 5, 'label': 'Период %K', 'sinput': False}, {'mql': 'KperiodLong', 'py': 'KperiodLong', 'param': 'KperiodLong', 'type': 'uint', 'default': 12, 'label': 'Период %K', 'sinput': False}, {'mql': 'DMethod', 'py': 'DMethod', 'param': 'DMethod', 'type': 'int', 'default': 0, 'label': 'Метод сглаживания сигнальной линии', 'sinput': False}, {'mql': 'Dperiod', 'py': 'Dperiod', 'param': 'Dperiod', 'type': 'uint', 'default': 7, 'label': 'Период сигнальной линии %D', 'sinput': False}, {'mql': 'DPhase', 'py': 'DPhase', 'param': 'DPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания сигнальной линии', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'uint', 'default': 3, 'label': 'Замедление', 'sinput': False}, {'mql': 'PriceField', 'py': 'PriceField', 'param': 'PriceField', 'type': 'int', 'default': 0, 'label': 'Параметр выбора цен для расчета', 'sinput': False}, {'mql': 'Sens', 'py': 'Sens', 'param': 'Sens', 'type': 'uint', 'default': 7, 'label': 'Чувствительность в пунктах', 'sinput': False}, {'mql': 'OverBought', 'py': 'OverBought', 'param': 'OverBought', 'type': 'uint', 'default': 80, 'label': 'Уровень перекупленности в %%', 'sinput': False}, {'mql': 'OverSold', 'py': 'OverSold', 'param': 'OverSold', 'type': 'uint', 'default': 20, 'label': 'Уровень перепроданности в %%', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
KperiodShort = _input('KperiodShort', 5)  # Период %K
KperiodLong = _input('KperiodLong', 12)  # Период %K
DMethod = _input('DMethod', MODE_SMA_)  # Метод сглаживания сигнальной линии
Dperiod = _input('Dperiod', 7)  # Период сигнальной линии %D
DPhase = _input('DPhase', 15)  # Параметр сглаживания сигнальной линии
Slowing = _input('Slowing', 3)  # Замедление
PriceField = _input('PriceField', STO_LOWHIGH)  # Параметр выбора цен для расчета
Sens = _input('Sens', 7)  # Чувствительность в пунктах
OverBought = _input('OverBought', 80)  # Уровень перекупленности в %%
OverSold = _input('OverSold', 20)  # Уровень перепроданности в %%
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
SignUp = Arr(0, 0.0)
SignDown = Arr(0, 0.0)
sens = 0.0  # чувствительность в ценах
ATR_Handle = 0
min_rates_total = 0
min_rates_stoch = 0

def OnInit():
    global ATR_Handle, min_rates_stoch, min_rates_total, sens
    min_rates_stoch = _int(MathMax(KperiodShort, KperiodLong) + Slowing)
    min_rates_total = min_rates_stoch + XMA.GetStartBars(DMethod, Dperiod, DPhase) + 1
    ATR_Period = 15
    min_rates_total = MathMax(min_rates_total, ATR_Period) + 1
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    sens = Sens * Point()
    XMA.XMALengthCheck('Dperiod', Dperiod)
    XMA.XMALengthCheck('Dperiod', Dperiod)
    XMA.XMAPhaseCheck('DPhase', DPhase, DMethod)
    SetIndexBuffer(0, SignUp, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(SignUp, True)
    SetIndexBuffer(1, SignDown, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(SignDown, True)
    shortname = Box("")
    Smooth = ""
    Smooth = XMA.GetString_MA_Method(DMethod)
    StringConcatenate(shortname, 'Asymmetric Stochastic NR(', KperiodShort, ',', KperiodLong, ',', Dperiod, ',', Smooth, ',', Slowing, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Kperiod0, _s_OnCalculate_Kperiod1, _s_OnCalculate_Stoch_prev, _s_OnCalculate_XStoch_prev
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    maxbar = 0
    ATR = Arr(0, 0.0)
    Stoch_ = 0.0
    XStoch = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_stoch
        _s_OnCalculate_Kperiod0 = KperiodShort
        _s_OnCalculate_Kperiod1 = KperiodShort
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(ATR, True)
    maxbar = rates_total - 1 - min_rates_stoch
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Stoch_ = Stoch(_s_OnCalculate_Kperiod0, _s_OnCalculate_Kperiod1, Slowing, PriceField, sens, bar, low, high, close)
        XStoch = XMA.XMASeries(maxbar, prev_calculated, rates_total, DMethod, DPhase, Dperiod, Stoch_, bar, True)
        if _s_OnCalculate_XStoch_prev > OverBought:
            _s_OnCalculate_Kperiod0 = KperiodShort
            _s_OnCalculate_Kperiod1 = KperiodLong
        if _s_OnCalculate_XStoch_prev < OverSold:
            _s_OnCalculate_Kperiod0 = KperiodLong
            _s_OnCalculate_Kperiod1 = KperiodShort
        SignUp[bar] = 0.0
        SignDown[bar] = 0.0
        if _s_OnCalculate_XStoch_prev >= _s_OnCalculate_Stoch_prev and XStoch < Stoch_:
            SignUp[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if _s_OnCalculate_Stoch_prev >= _s_OnCalculate_XStoch_prev and Stoch_ < XStoch:
            SignDown[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        if bar:
            _s_OnCalculate_Stoch_prev = Stoch_
            _s_OnCalculate_XStoch_prev = XStoch
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def Stoch(Kperiod0, Kperiod1, Slowing_, PriceField_, sens_, Bar, Low, High, Close):
    max_ = 0.0
    min_ = 0.0
    c = 0.0
    delta = 0.0
    diff = 0.0
    c = 0.0
    max_ = 0.0
    min_ = 0.0
    end = Bar + Slowing_
    for j in range(Bar, end):
        if PriceField_ == STO_CLOSECLOSE:
            max_ += Close[ArrayMaximum(Close, j, Kperiod0)]
            min_ += Close[ArrayMinimum(Close, j, Kperiod1)]
        if PriceField_ == STO_LOWHIGH:
            max_ += High[ArrayMaximum(High, j, Kperiod0)]
            min_ += Low[ArrayMinimum(Low, j, Kperiod1)]
        c += Close[j]
    sens_ *= Slowing_
    delta = max_ - min_
    diff = sens - delta
    if diff > 0:
        delta = sens
        min_ -= diff / 2
    if delta:
        return _fdiv(100 * (c - min_), delta)
    return -2.0

# ---- global variables initialised from expressions
XMA = _alloc(CXMA)
XMA.__init__()

# ---- static local variables
_s_OnCalculate_Kperiod0 = 0
_s_OnCalculate_Kperiod1 = 0
_s_OnCalculate_Stoch_prev = 0.0
_s_OnCalculate_XStoch_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AsymmetricstochnrSign(_MQL5Indicator):
    name = 'asymmetricstochnr_sign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'KperiodShort': 5,  # Период %K
        'KperiodLong': 12,  # Период %K
        'DMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод сглаживания сигнальной линии
        'Dperiod': 7,  # Период сигнальной линии %D
        'DPhase': 15,  # Параметр сглаживания сигнальной линии
        'Slowing': 3,  # Замедление
        'PriceField': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Параметр выбора цен для расчета
        'Sens': 7,  # Чувствительность в пунктах
        'OverBought': 80,  # Уровень перекупленности в %%
        'OverSold': 20,  # Уровень перепроданности в %%
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

