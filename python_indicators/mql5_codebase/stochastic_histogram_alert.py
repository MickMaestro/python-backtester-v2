"""Stochastic_Histogram_Alert — converted from MQL5: MQL5 Indicators/Stochastic_Histogram_Alert/Stochastic_Histogram_Alert.mq5

Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 7, 2: 11}, 'colors': {1: [65280, 15631086], 2: [16748574, 8421504, 9639167]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'Stochastic Signal', 2: 'Stochastic_Histogram'}, 'levels': [], 'description': [], 'name': 'Stochastic_Histogram_Alert', 'source': 'MQL5 Indicators/Stochastic_Histogram_Alert/Stochastic_Histogram_Alert.mq5', 'folder': 'Stochastic_Histogram_Alert', 'inputs': [{'mql': 'KPeriod', 'py': 'KPeriod', 'param': 'KPeriod', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field', 'py': 'Price_field', 'param': 'Price_field', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'uint', 'default': 60, 'label': 'уровень перезакупа', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'uint', 'default': 40, 'label': 'уровень перепроданности', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для подачи сигнала', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Разрешение алерта', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': 'Количество алертов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
KPeriod = _input('KPeriod', 5)
DPeriod = _input('DPeriod', 3)
Slowing = _input('Slowing', 3)
MA_Method = _input('MA_Method', MODE_SMA)
Price_field = _input('Price_field', STO_LOWHIGH)
HighLevel = _input('HighLevel', 60)  # уровень перезакупа
LowLevel = _input('LowLevel', 40)  # уровень перепроданности
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
NumberofBar = _input('NumberofBar', 1)  # Номер бара для подачи сигнала
SoundON = _input('SoundON', True)  # Разрешение алерта
NumberofAlerts = _input('NumberofAlerts', 2)  # Количество алертов
EMailON = _input('EMailON', False)  # Разрешение почтовой отправки сигнала
PushON = _input('PushON', False)  # Разрешение отправки сигнала на мобильный
min_rates_total = 0
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
UpBuffer1 = Arr(0, 0.0)
DnBuffer1 = Arr(0, 0.0)
Stochastic_Handle = 0

def OnInit():
    global Stochastic_Handle, min_rates_total
    min_rates_total = KPeriod + DPeriod + Slowing
    Stochastic_Handle = iStochastic(None, 0, KPeriod, DPeriod, Slowing, MA_Method, Price_field)
    if Stochastic_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iStochastic')
        return INIT_FAILED
    SetIndexBuffer(0, UpBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(UpBuffer1, True)
    SetIndexBuffer(1, DnBuffer1, INDICATOR_DATA)
    ArraySetAsSeries(DnBuffer1, True)
    SetIndexBuffer(2, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(3, DnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnBuffer, True)
    SetIndexBuffer(4, ColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stochastic_Histogram_Alert(' + _str(KPeriod) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrLimeGreen)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if BarsCalculated(Stochastic_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Stochastic_Handle, MAIN_LINE, 0, to_copy, UpBuffer) <= 0:
        return 0
    if CopyBuffer(Stochastic_Handle, MAIN_LINE, 0, to_copy, UpBuffer1) <= 0:
        return 0
    if CopyBuffer(Stochastic_Handle, SIGNAL_LINE, 0, to_copy, DnBuffer1) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        DnBuffer[bar] = 50.0
        clr = _int(1.0)
        if UpBuffer[bar] > HighLevel:
            clr = _int(0.0)
        elif UpBuffer[bar] < LowLevel:
            clr = _int(2.0)
        ColorBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    BuySignal('Stochastic_Histogram_Alert', rates_total, prev_calculated, Close, Spread)
    SellSignal('Stochastic_Histogram_Alert', rates_total, prev_calculated, Close, Spread)
    return rates_total

def BuySignal(SignalSirname, Rates_total, Prev_calculated, Close, Spread):
    global _s_BuySignal_counter
    if Rates_total != Prev_calculated:
        _s_BuySignal_counter = 0
    BuySignal_ = False
    SeriesTest = ArrayGetAsSeries(UpBuffer1)
    index = 0
    index1 = 0
    if SeriesTest:
        index = _int(NumberofBar)
        index1 = index + 1
    else:
        index = Rates_total - _int(NumberofBar) - 1
        index1 = index - 1
    if DnBuffer1[index1] >= UpBuffer1[index1] and DnBuffer1[index] < UpBuffer1[index]:
        BuySignal_ = True
    if BuySignal_ and _s_BuySignal_counter <= NumberofAlerts:
        _s_BuySignal_counter += 1
        tm = MqlDateTime()
        TimeToStruct(TimeCurrent(), tm)
        text = TimeToString(TimeCurrent(), TIME_DATE) + ' ' + _str(tm.hour) + ':' + _str(tm.min)
        SeriesTest = ArrayGetAsSeries(Close)
        if SeriesTest:
            index = _int(NumberofBar)
        else:
            index = Rates_total - _int(NumberofBar) - 1
        Ask = Close[index]
        Bid = Close[index]
        SeriesTest = ArrayGetAsSeries(Spread)
        if SeriesTest:
            index = _int(NumberofBar)
        else:
            index = Rates_total - _int(NumberofBar) - 1
        Bid += Spread[index] * Point()
        sAsk = DoubleToString(Ask, Digits())
        sBid = DoubleToString(Bid, Digits())
        sPeriod = GetStringTimeframe(ChartPeriod())
        if SoundON:
            Alert('BUY signal \n Ask=', Ask, '\n Bid=', Bid, '\n currtime=', text, '\n Symbol=', Symbol(), ' Period=', sPeriod)
        if EMailON:
            SendMail(SignalSirname + ': BUY signal alert', 'BUY signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
        if PushON:
            SendNotification(SignalSirname + ': BUY signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)

def SellSignal(SignalSirname, Rates_total, Prev_calculated, Close, Spread):
    global _s_SellSignal_counter
    if Rates_total != Prev_calculated:
        _s_SellSignal_counter = 0
    SellSignal_ = False
    SeriesTest = ArrayGetAsSeries(DnBuffer1)
    index = 0
    index1 = 0
    if SeriesTest:
        index = _int(NumberofBar)
        index1 = index + 1
    else:
        index = Rates_total - _int(NumberofBar) - 1
        index1 = index - 1
    if DnBuffer1[index1] <= UpBuffer1[index1] and DnBuffer1[index] > UpBuffer1[index]:
        SellSignal_ = True
    if SellSignal_ and _s_SellSignal_counter <= NumberofAlerts:
        _s_SellSignal_counter += 1
        tm = MqlDateTime()
        TimeToStruct(TimeCurrent(), tm)
        text = TimeToString(TimeCurrent(), TIME_DATE) + ' ' + _str(tm.hour) + ':' + _str(tm.min)
        SeriesTest = ArrayGetAsSeries(Close)
        if SeriesTest:
            index = _int(NumberofBar)
        else:
            index = Rates_total - _int(NumberofBar) - 1
        Ask = Close[index]
        Bid = Close[index]
        SeriesTest = ArrayGetAsSeries(Spread)
        if SeriesTest:
            index = _int(NumberofBar)
        else:
            index = Rates_total - _int(NumberofBar) - 1
        Bid += Spread[index] * Point()
        sAsk = DoubleToString(Ask, Digits())
        sBid = DoubleToString(Bid, Digits())
        sPeriod = GetStringTimeframe(ChartPeriod())
        if SoundON:
            Alert('SELL signal \n Ask=', Ask, '\n Bid=', Bid, '\n currtime=', text, '\n Symbol=', Symbol(), ' Period=', sPeriod)
        if EMailON:
            SendMail(SignalSirname + ': SELL signal alert', 'SELL signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
        if PushON:
            SendNotification(SignalSirname + ': SELL signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

# ---- static local variables
_s_BuySignal_counter = 0
_s_SellSignal_counter = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticHistogramAlert(_MQL5Indicator):
    name = 'Stochastic_Histogram_Alert'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'KPeriod': 5,
        'DPeriod': 3,
        'Slowing': 3,
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'HighLevel': 60,  # уровень перезакупа
        'LowLevel': 40,  # уровень перепроданности
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'NumberofBar': 1,  # Номер бара для подачи сигнала
        'SoundON': True,  # Разрешение алерта
        'NumberofAlerts': 2,  # Количество алертов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
    }

