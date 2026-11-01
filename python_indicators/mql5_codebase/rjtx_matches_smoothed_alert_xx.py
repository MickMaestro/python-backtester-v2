"""RJTX_Matches_Smoothed_Alert_xx — converted from MQL5: MQL5 Indicators/RJTX_Matches_Smoothed_Alert_xx/RJTX_Matches_Smoothed_Alert_xx.mq5

We recommend adjust the body and head size of the matches for better visualization.
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 5, 5: 5}, 'colors': {1: [11119017], 2: [36095], 3: [13828244], 4: [9639167], 5: [16748574]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2, 5: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'match 1', 2: 'match 2', 3: 'match 3', 4: 'RJTX_Matches_Smoothed Sell', 5: 'RJTX_Matches_Smoothed Buy'}, 'levels': [], 'description': ['We recommend adjust the body and head size of the matches for better visualization.'], 'name': 'RJTX_Matches_Smoothed_Alert_xx', 'source': 'MQL5 Indicators/RJTX_Matches_Smoothed_Alert_xx/RJTX_Matches_Smoothed_Alert_xx.mq5', 'folder': 'RJTX_Matches_Smoothed_Alert_xx', 'inputs': [{'mql': 'iPeriod', 'py': 'iPeriod', 'param': 'iPeriod', 'type': 'uint', 'default': 10, 'label': 'Период индикатора свечек', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 12, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для подачи сигнала', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Разрешение алерта', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': 'Количество алертов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}, {'mql': 'SellSymb', 'py': 'SellSymb', 'param': 'SellSymb', 'type': 'uint', 'default': 171, 'label': 'Символ продажи', 'sinput': False}, {'mql': 'BuySymb', 'py': 'BuySymb', 'param': 'BuySymb', 'type': 'uint', 'default': 171, 'label': 'Символ покупки', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
iPeriod = _input('iPeriod', 10)  # Период индикатора свечек
XMA_Method = _input('XMA_Method', MODE_SMA_)  # Метод усреднения
XLength = _input('XLength', 12)  # Глубина сглаживания
XPhase = _input('XPhase', 15)  # Параметр сглаживания
NumberofBar = _input('NumberofBar', 1)  # Номер бара для подачи сигнала
SoundON = _input('SoundON', True)  # Разрешение алерта
NumberofAlerts = _input('NumberofAlerts', 2)  # Количество алертов
EMailON = _input('EMailON', False)  # Разрешение почтовой отправки сигнала
PushON = _input('PushON', False)  # Разрешение отправки сигнала на мобильный
SellSymb = _input('SellSymb', 171)  # Символ продажи
BuySymb = _input('BuySymb', 171)  # Символ покупки
LineBuffer0 = Arr(0, 0.0)
LineBuffer1 = Arr(0, 0.0)
LineBuffer2 = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
Count = Arr(0, 0)
xOpen = Arr(0, 0.0)

def Recount_ArrayZeroPos(CoArr, Size):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def OnInit():
    global min_rates_total
    min_rates_total = GetStartBars(XMA_Method, XLength, XPhase)
    min_rates_total = _int(MathMax(iPeriod, min_rates_total))
    ArrayResize(Count, iPeriod + 1)
    ArrayResize(xOpen, iPeriod + 1)
    IndInit(0, LineBuffer0, 0.0, min_rates_total, 0)
    IndInit(1, LineBuffer1, 0.0, min_rates_total, 0)
    IndInit(2, LineBuffer2, 0.0, min_rates_total, 0)
    IndInit(3, SellBuffer, 0.0, min_rates_total, 0)
    IndInit(4, BuyBuffer, 0.0, min_rates_total, 0)
    PlotIndexSetInteger(3, PLOT_ARROW, SellSymb)
    PlotIndexSetInteger(4, PLOT_ARROW, BuySymb)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'RJTX_Matches_Smoothed'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def IndInit(Number, Buffer, Empty_Value, Draw_Begin, nShift):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    PlotIndexSetInteger(Number, PLOT_SHOW_DATA, False)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_p
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    xclose = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        ArrayInitialize(Count, 0)
        ArrayInitialize(xOpen, open[first])
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        xOpen[Count[0]] = XMAO.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, open[bar], bar, False)
        xclose = XMAC.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, close[bar], bar, False)
        if xclose > xOpen[Count[iPeriod]]:
            SellBuffer[bar] = 0.0
            BuyBuffer[bar] = xclose
        else:
            SellBuffer[bar] = xclose
            BuyBuffer[bar] = 0.0
        _sw1 = _s_OnCalculate_p
        if _sw1 == 0:
            LineBuffer0[bar] = xOpen[Count[iPeriod - 1]]
            LineBuffer1[bar] = 0.0
            LineBuffer2[bar] = xclose
        elif _sw1 == 1:
            LineBuffer0[bar] = xclose
            LineBuffer1[bar] = xOpen[Count[iPeriod - 1]]
            LineBuffer2[bar] = 0.0
        elif _sw1 == 2:
            LineBuffer0[bar] = 0.0
            LineBuffer1[bar] = xclose
            LineBuffer2[bar] = xOpen[Count[iPeriod - 1]]
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count, iPeriod + 1)
            _s_OnCalculate_p += 1
        if _s_OnCalculate_p > 2:
            _s_OnCalculate_p = 0
    else:
        bar = _range_end(bar, rates_total, 1)
    BuySignal('RJTX_Matches_Smoothed_Alert', BuyBuffer, rates_total, prev_calculated, close, spread)
    SellSignal('RJTX_Matches_Smoothed_Alert', SellBuffer, rates_total, prev_calculated, close, spread)
    return rates_total

def BuySignal(SignalSirname, BuyArrow, Rates_total, Prev_calculated, Close, Spread):
    global _s_BuySignal_counter
    if Rates_total != Prev_calculated:
        _s_BuySignal_counter = 0
    BuySignal_ = False
    SeriesTest = ArrayGetAsSeries(BuyArrow)
    index = 0
    index1 = 0
    if SeriesTest:
        index = _int(NumberofBar)
        index1 = index + 1
    else:
        index = Rates_total - _int(NumberofBar) - 1
        index1 = index - 1
    if (not BuyArrow[index1]) and BuyArrow[index]:
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

def SellSignal(SignalSirname, SellArrow, Rates_total, Prev_calculated, Close, Spread):
    global _s_SellSignal_counter
    if Rates_total != Prev_calculated:
        _s_SellSignal_counter = 0
    SellSignal_ = False
    SeriesTest = ArrayGetAsSeries(SellArrow)
    index = 0
    index1 = 0
    if SeriesTest:
        index = _int(NumberofBar)
        index1 = index + 1
    else:
        index = Rates_total - _int(NumberofBar) - 1
        index1 = index - 1
    if (not SellArrow[index1]) and SellArrow[index]:
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

# ---- global variables initialised from expressions
XMAO = _alloc(CXMA)
XMAO.__init__()
XMAC = _alloc(CXMA)
XMAC.__init__()

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1
_s_OnCalculate_p = 0
_s_BuySignal_counter = 0
_s_SellSignal_counter = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RJTXMatchesSmoothedAlertXx(_MQL5Indicator):
    name = 'RJTX_Matches_Smoothed_Alert_xx'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iPeriod': 10,  # Период индикатора свечек
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения
        'XLength': 12,  # Глубина сглаживания
        'XPhase': 15,  # Параметр сглаживания
        'NumberofBar': 1,  # Номер бара для подачи сигнала
        'SoundON': True,  # Разрешение алерта
        'NumberofAlerts': 2,  # Количество алертов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
        'SellSymb': 171,  # Символ продажи
        'BuySymb': 171,  # Символ покупки
    }

