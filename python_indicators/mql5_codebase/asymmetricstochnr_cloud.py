"""asymmetricstochnr_cloud — converted from MQL5: MQL5 Indicators/AsymmetricStochNR_Cloud/asymmetricstochnr_cloud.mq5

Asymmetric Stoch NR
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16760576, 14524637]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Asymmetric Stochastic NR'}, 'levels': [], 'description': ['Asymmetric Stoch NR'], 'name': 'asymmetricstochnr_cloud', 'source': 'MQL5 Indicators/AsymmetricStochNR_Cloud/asymmetricstochnr_cloud.mq5', 'folder': 'AsymmetricStochNR_Cloud', 'inputs': [{'mql': 'KperiodShort', 'py': 'KperiodShort', 'param': 'KperiodShort', 'type': 'uint', 'default': 5, 'label': 'Период %K', 'sinput': False}, {'mql': 'KperiodLong', 'py': 'KperiodLong', 'param': 'KperiodLong', 'type': 'uint', 'default': 12, 'label': 'Период %K', 'sinput': False}, {'mql': 'DMethod', 'py': 'DMethod', 'param': 'DMethod', 'type': 'int', 'default': 0, 'label': 'Метод сглаживания сигнальной линии', 'sinput': False}, {'mql': 'Dperiod', 'py': 'Dperiod', 'param': 'Dperiod', 'type': 'uint', 'default': 7, 'label': 'Период сигнальной линии %D', 'sinput': False}, {'mql': 'DPhase', 'py': 'DPhase', 'param': 'DPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания сигнальной линии', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'uint', 'default': 3, 'label': 'Замедление', 'sinput': False}, {'mql': 'PriceField', 'py': 'PriceField', 'param': 'PriceField', 'type': 'int', 'default': 0, 'label': 'Параметр выбора цен для расчета', 'sinput': False}, {'mql': 'Sens', 'py': 'Sens', 'param': 'Sens', 'type': 'uint', 'default': 7, 'label': 'Чувствительность в пунктах', 'sinput': False}, {'mql': 'OverBought', 'py': 'OverBought', 'param': 'OverBought', 'type': 'uint', 'default': 80, 'label': 'Уровень перекупленности в %%', 'sinput': False}, {'mql': 'OverSold', 'py': 'OverSold', 'param': 'OverSold', 'type': 'uint', 'default': 20, 'label': 'Уровень перепроданности в %%', 'sinput': False}, {'mql': 'UpLevelsColor', 'py': 'UpLevelsColor', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Цвет уровня перекупленности', 'sinput': False}, {'mql': 'DnLevelsColor', 'py': 'DnLevelsColor', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Цвет уровня перепроданности', 'sinput': False}, {'mql': 'Levelstyle', 'py': 'Levelstyle', 'param': 'Levelstyle', 'type': 'int', 'default': 1, 'label': 'Стиль уровней', 'sinput': False}, {'mql': 'LevelsWidth', 'py': 'LevelsWidth', 'param': 'LevelsWidth', 'type': 'int', 'default': 1, 'label': 'Толщина уровней', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum WIDTH
Width_1 = 1
Width_2 = 2
Width_3 = 3
Width_4 = 4
Width_5 = 5
_enum('WIDTH', {1: 'Width_1', 2: 'Width_2', 3: 'Width_3', 4: 'Width_4', 5: 'Width_5'})

# enum STYLE
SOLID_ = 0
DASH_ = 1
DOT_ = 2
DASHDOT_ = 3
DASHDOTDOT_ = 4
_enum('STYLE', {0: 'SOLID_', 1: 'DASH_', 2: 'DOT_', 3: 'DASHDOT_', 4: 'DASHDOTDOT_'})

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
UpLevelsColor = _input('UpLevelsColor', clrBlue)  # Цвет уровня перекупленности
DnLevelsColor = _input('DnLevelsColor', clrMagenta)  # Цвет уровня перепроданности
Levelstyle = _input('Levelstyle', DASH_)  # Стиль уровней
LevelsWidth = _input('LevelsWidth', Width_1)  # Толщина уровней
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Stoch = Arr(0, 0.0)
XStoch = Arr(0, 0.0)
sens = 0.0  # чувствительность в ценах
min_rates_total = 0
min_rates_stoch = 0

def OnInit():
    global min_rates_stoch, min_rates_total, sens
    min_rates_stoch = _int(MathMax(KperiodShort, KperiodLong) + Slowing)
    min_rates_total = min_rates_stoch + XMA.GetStartBars(DMethod, Dperiod, DPhase)
    sens = Sens * Point()
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, OverSold)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, DnLevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, Levelstyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 0, LevelsWidth)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, OverBought)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, UpLevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, Levelstyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 1, LevelsWidth)
    XMA.XMALengthCheck('Dperiod', Dperiod)
    XMA.XMALengthCheck('Dperiod', Dperiod)
    XMA.XMAPhaseCheck('DPhase', DPhase, DMethod)
    SetIndexBuffer(0, Stoch, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Stoch, True)
    SetIndexBuffer(1, XStoch, INDICATOR_DATA)
    ArraySetAsSeries(XStoch, True)
    shortname = Box("")
    Smooth = ""
    Smooth = XMA.GetString_MA_Method(DMethod)
    StringConcatenate(shortname, 'Asymmetric Stochastic NR(', KperiodShort, ',', KperiodLong, ',', Dperiod, ',', Smooth, ',', Slowing, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Kperiod0, _s_OnCalculate_Kperiod1
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    maxbar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_stoch
        _s_OnCalculate_Kperiod0 = KperiodShort
        _s_OnCalculate_Kperiod1 = KperiodShort
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    maxbar = rates_total - 1 - min_rates_stoch
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Stoch[bar] = Stoch_f(_s_OnCalculate_Kperiod0, _s_OnCalculate_Kperiod1, Slowing, PriceField, sens, bar, low, high, close)
        XStoch[bar] = XMA.XMASeries(maxbar, prev_calculated, rates_total, DMethod, DPhase, Dperiod, Stoch[bar], bar, True)
        if XStoch[bar + 1] > OverBought:
            _s_OnCalculate_Kperiod0 = KperiodShort
            _s_OnCalculate_Kperiod1 = KperiodLong
        if XStoch[bar + 1] < OverSold:
            _s_OnCalculate_Kperiod0 = KperiodLong
            _s_OnCalculate_Kperiod1 = KperiodShort
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def Stoch_f(Kperiod0, Kperiod1, Slowing_, PriceField_, sens_, Bar, Low, High, Close):
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AsymmetricstochnrCloud(_MQL5Indicator):
    name = 'asymmetricstochnr_cloud'
    pane = _Pane.SEPARATE
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
        'Levelstyle': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=1),  # Стиль уровней
        'LevelsWidth': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Толщина уровней
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

