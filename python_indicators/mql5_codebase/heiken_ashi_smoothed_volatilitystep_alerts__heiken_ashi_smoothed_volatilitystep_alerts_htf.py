"""Heiken_Ashi_Smoothed_VolatilityStep_Alerts — converted from MQL5: MQL5 Indicators/Heiken_Ashi_Smoothed_VolatilityStep_Alerts_HTF/Heiken_Ashi_Smoothed_VolatilityStep_Alerts.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 3}, 'colors': {1: [13458026]}, 'widths': {1: 4}, 'styles': {1: 0}, 'labels': {1: 'Heiken_Ashi_Smoothed_VolatilityStep'}, 'levels': [], 'description': [], 'name': 'Heiken_Ashi_Smoothed_VolatilityStep_Alerts', 'source': 'MQL5 Indicators/Heiken_Ashi_Smoothed_VolatilityStep_Alerts_HTF/Heiken_Ashi_Smoothed_VolatilityStep_Alerts.mq5', 'folder': 'Heiken_Ashi_Smoothed_VolatilityStep_Alerts_HTF', 'inputs': [{'mql': 'HMA_Method', 'py': 'HMA_Method', 'param': 'HMA_Method', 'type': 'int', 'default': 4, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'HLength', 'py': 'HLength', 'param': 'HLength', 'type': 'uint', 'default': 5, 'label': 'Глубина  усреднения', 'sinput': False}, {'mql': 'HPhase', 'py': 'HPhase', 'param': 'HPhase', 'type': 'int', 'default': 100, 'label': 'Параметр усреднения,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'LevelsTotal', 'py': 'LevelsTotal', 'param': 'LevelsTotal', 'type': 'uint', 'default': 20, 'label': 'количество уровеней', 'sinput': False}, {'mql': 'StartLevel', 'py': 'StartLevel', 'param': 'StartLevel', 'type': 'uint', 'default': 50, 'label': 'стартовый уровень', 'sinput': False}, {'mql': 'LevelsStep', 'py': 'LevelsStep', 'param': 'LevelsStep', 'type': 'uint', 'default': 50, 'label': 'расстояние между уровнями', 'sinput': False}, {'mql': 'LevelsColor', 'py': 'LevelsColor', 'param': None, 'type': 'color', 'default': 36095, 'label': 'цвет уровеней', 'sinput': False}, {'mql': 'AlertLevel', 'py': 'AlertLevel', 'param': 'AlertLevel', 'type': 'uint', 'default': 150, 'label': 'Уровень срабатывания', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для подачи сигнала', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Разрешение алерта', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': 'Количество алертов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}, {'mql': 'AlertLevelColor', 'py': 'AlertLevelColor', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'цвет уровня срабатывания', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
HMA_Method = _input('HMA_Method', MODE_JJMA)  # Метод усреднения
HLength = _input('HLength', 5)  # Глубина  усреднения
HPhase = _input('HPhase', 100)  # Параметр усреднения,
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
LevelsTotal = _input('LevelsTotal', 20)  # количество уровеней
StartLevel = _input('StartLevel', 50)  # стартовый уровень
LevelsStep = _input('LevelsStep', 50)  # расстояние между уровнями
LevelsColor = _input('LevelsColor', clrDarkOrange)  # цвет уровеней
AlertLevel = _input('AlertLevel', 150)  # Уровень срабатывания
NumberofBar = _input('NumberofBar', 1)  # Номер бара для подачи сигнала
SoundON = _input('SoundON', True)  # Разрешение алерта
NumberofAlerts = _input('NumberofAlerts', 2)  # Количество алертов
EMailON = _input('EMailON', False)  # Разрешение почтовой отправки сигнала
PushON = _input('PushON', False)  # Разрешение отправки сигнала на мобильный
AlertLevelColor = _input('AlertLevelColor', clrMagenta)  # цвет уровня срабатывания
IndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = GetStartBars(HMA_Method, HLength, HPhase) + 1
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = 'Heiken_Ashi_Smoothed_VolatilityStep_Alerts(' + _str(HLength) + ',' + _str(AlertLevel) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, LevelsTotal + 1)
    for numb in range(0, _int(LevelsTotal)):
        level = _int(StartLevel + (LevelsStep * numb))
        IndicatorSetDouble(INDICATOR_LEVELVALUE, numb, level)
        IndicatorSetInteger(INDICATOR_LEVELCOLOR, numb, LevelsColor)
        IndicatorSetInteger(INDICATOR_LEVELSTYLE, numb, STYLE_DASHDOTDOT)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, LevelsTotal, AlertLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, LevelsTotal, AlertLevelColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, LevelsTotal, STYLE_SOLID)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, LevelsTotal, 3)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_HAC_prev, _s_OnCalculate_HAO_prev
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    XmaOpen = 0.0
    XmaHigh = 0.0
    XmaLow = 0.0
    XmaClose = 0.0
    Volatility = 0.0
    Res = 0.0
    O = 0.0
    H = 0.0
    L = 0.0
    C = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        _s_OnCalculate_HAO_prev = (open[first] + close[first]) / 2
        _s_OnCalculate_HAC_prev = (open[first] + high[first] + low[first] + close[first]) / 4
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        IndBuffer[bar] = 0.0
        XmaOpen = XMAO.XMASeries(0, prev_calculated, rates_total, HMA_Method, HPhase, HLength, open[bar], bar, False)
        XmaClose = XMAC.XMASeries(0, prev_calculated, rates_total, HMA_Method, HPhase, HLength, close[bar], bar, False)
        XmaHigh = XMAH.XMASeries(0, prev_calculated, rates_total, HMA_Method, HPhase, HLength, high[bar], bar, False)
        XmaLow = XMAL.XMASeries(0, prev_calculated, rates_total, HMA_Method, HPhase, HLength, low[bar], bar, False)
        if bar < min_rates_total:
            continue
        O = (_s_OnCalculate_HAO_prev + _s_OnCalculate_HAC_prev) / 2
        C = (XmaOpen + XmaHigh + XmaLow + XmaClose) / 4
        H = MathMax(XmaHigh, MathMax(O, C))
        L = MathMin(XmaLow, MathMin(O, C))
        Volatility = _fdiv(H - L, Point())
        if Volatility >= StartLevel:
            Res = MathMax(Volatility - StartLevel, 0)
            IndBuffer[bar] = StartLevel + (LevelsStep * _int(Res / LevelsStep))
        if bar < (rates_total - 1):
            _s_OnCalculate_HAO_prev = O
            _s_OnCalculate_HAC_prev = C
    else:
        bar = _range_end(bar, rates_total, 1)
    TrendSignal('Heiken_Ashi_Smoothed_VolatilityStep_Alerts', rates_total, prev_calculated, close, spread)
    return rates_total

def TrendSignal(SignalSirname, Rates_total, Prev_calculated, Close, Spread):
    global _s_TrendSignal_counter
    if Rates_total != Prev_calculated:
        _s_TrendSignal_counter = 0
    SignalText = ''
    Signal = False
    index = Rates_total - 1 - _int(NumberofBar)
    index1 = Rates_total - 1 - _int(NumberofBar) - 1
    if IndBuffer[index1] <= AlertLevel and IndBuffer[index] > AlertLevel:
        Signal = True
        SignalText = SignalText + 'Усиление тренда: Округлённая волатильность на баре номер ' + _str(NumberofBar) + ' превысила уровень ' + _str(AlertLevel) + '!'
    if Signal and _s_TrendSignal_counter <= NumberofAlerts:
        _s_TrendSignal_counter += 1
        tm = MqlDateTime()
        TimeToStruct(TimeCurrent(), tm)
        text = TimeToString(TimeCurrent(), TIME_DATE) + ' ' + _str(tm.hour) + ':' + _str(tm.min)
        Ask = Close[index]
        Bid = Close[index]
        Bid += Spread[index] * Point()
        sAsk = DoubleToString(Ask, Digits())
        sBid = DoubleToString(Bid, Digits())
        sPeriod = GetStringTimeframe(ChartPeriod())
        if SoundON:
            Alert(SignalText + '\n Ask=', Ask, '\n Bid=', Bid, '\n currtime=', text, '\n Symbol=', Symbol(), ' Period=', sPeriod)
        if EMailON:
            SendMail(SignalSirname + ': ' + SignalText, ' at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
        if PushON:
            SendNotification(SignalSirname + ': ' + SignalText + ' at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

# ---- global variables initialised from expressions
XMAO = _alloc(CXMA)
XMAO.__init__()
XMAL = _alloc(CXMA)
XMAL.__init__()
XMAH = _alloc(CXMA)
XMAH.__init__()
XMAC = _alloc(CXMA)
XMAC.__init__()

# ---- static local variables
_s_OnCalculate_HAO_prev = 0.0
_s_OnCalculate_HAC_prev = 0.0
_s_TrendSignal_counter = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HeikenAshiSmoothedVolatilityStepAlerts(_MQL5Indicator):
    name = 'Heiken_Ashi_Smoothed_VolatilityStep_Alerts'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'HMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения
        'HLength': 5,  # Глубина  усреднения
        'HPhase': 100,  # Параметр усреднения,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'LevelsTotal': 20,  # количество уровеней
        'StartLevel': 50,  # стартовый уровень
        'LevelsStep': 50,  # расстояние между уровнями
        'AlertLevel': 150,  # Уровень срабатывания
        'NumberofBar': 1,  # Номер бара для подачи сигнала
        'SoundON': True,  # Разрешение алерта
        'NumberofAlerts': 2,  # Количество алертов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
    }

