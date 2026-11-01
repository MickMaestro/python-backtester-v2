"""DSSBressertSignAlert — converted from MQL5: MQL5 Indicators/DSSBressertSignAlert/DSSBressertSignAlert.mq5

Copyright: Copyright © 2008, MetaQuotes Software Corp.; Link: http://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [3329330]}, 'widths': {1: 5, 2: 5}, 'styles': {}, 'labels': {1: 'DSSBressertSign Sell', 2: 'DSSBressertSign Buy'}, 'levels': [], 'description': [], 'name': 'DSSBressertSignAlert', 'source': 'MQL5 Indicators/DSSBressertSignAlert/DSSBressertSignAlert.mq5', 'folder': 'DSSBressertSignAlert', 'inputs': [{'mql': 'EMA_period', 'py': 'EMA_period', 'param': 'EMA_period', 'type': 'uint', 'default': 8, 'label': 'период EMA', 'sinput': False}, {'mql': 'Sto_period', 'py': 'Sto_period', 'param': 'Sto_period', 'type': 'uint', 'default': 13, 'label': 'период стохастика', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для подачи сигнала', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Разрешение алерта', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': 'Количество алертов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
EMA_period = _input('EMA_period', 8)  # период EMA
Sto_period = _input('Sto_period', 13)  # период стохастика
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
NumberofBar = _input('NumberofBar', 1)  # Номер бара для подачи сигнала
SoundON = _input('SoundON', True)  # Разрешение алерта
NumberofAlerts = _input('NumberofAlerts', 2)  # Количество алертов
EMailON = _input('EMailON', False)  # Разрешение почтовой отправки сигнала
PushON = _input('PushON', False)  # Разрешение отправки сигнала на мобильный
min_rates_total = 0
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
smooth_coefficient = 0.0
ATR_Handle = 0
Count = Arr(0, 0)
Mit = Arr(0, 0.0)

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
    global ATR_Handle, min_rates_total, smooth_coefficient
    ATR_Period = 12
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    min_rates_total = _int(MathMax(ATR_Period, Sto_period + 1))
    smooth_coefficient = _fdiv(2.0, 1.0 + EMA_period)
    ArrayResize(Count, Sto_period)
    ArrayResize(Mit, Sto_period)
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 170)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 170)
    ArraySetAsSeries(BuyBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'DSSBressertSignAlert(', EMA_period, ', ', Sto_period, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Dss_prev
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    HighRange = 0.0
    LowRange = 0.0
    delta = 0.0
    MIT = 0.0
    DSS = 0.0
    Dss = 0.0
    ATR = Arr(0, 0.0)
    diff = 0.0
    to_copy = 0
    limit = 0
    bar = 0
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(ATR, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        ArrayInitialize(Count, 0)
        ArrayInitialize(Mit, 50.0)
        _s_OnCalculate_Dss_prev = 50.0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        HighRange = high[ArrayMaximum(high, bar, Sto_period)]
        LowRange = low[ArrayMinimum(low, bar, Sto_period)]
        delta = close[bar] - LowRange
        diff = (HighRange - LowRange) * 100.0
        if not diff:
            diff = Point() * 100.0
        MIT = _fdiv(delta, HighRange - LowRange) * 100.0
        Mit[Count[0]] = (smooth_coefficient * (MIT - Mit[Count[1]])) + Mit[Count[1]]
        HighRange = Mit[ArrayMaximum(Mit, 0, Sto_period)]
        LowRange = Mit[ArrayMinimum(Mit, 0, Sto_period)]
        delta = Mit[Count[0]] - LowRange
        DSS = _fdiv(delta, HighRange - LowRange) * 100.0
        Dss = (smooth_coefficient * (DSS - _s_OnCalculate_Dss_prev)) + _s_OnCalculate_Dss_prev
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if Mit[Count[1]] <= _s_OnCalculate_Dss_prev and Mit[Count[0]] > Dss:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if Mit[Count[1]] >= _s_OnCalculate_Dss_prev and Mit[Count[0]] < Dss:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        if bar < (rates_total - 1):
            _s_OnCalculate_Dss_prev = Dss
            Recount_ArrayZeroPos(Count, Sto_period)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    BuySignal('DSSBressertSignAlert', BuyBuffer, rates_total, prev_calculated, close, spread)
    SellSignal('DSSBressertSignAlert', SellBuffer, rates_total, prev_calculated, close, spread)
    return rates_total

def BuySignal(SignalSirname, BuyArrow, Rates_total, Prev_calculated, Close, Spread):
    global _s_BuySignal_counter
    if Rates_total != Prev_calculated:
        _s_BuySignal_counter = 0
    BuySignal_ = False
    SeriesTest = ArrayGetAsSeries(BuyArrow)
    index = 0
    if SeriesTest:
        index = _int(NumberofBar)
    else:
        index = Rates_total - _int(NumberofBar) - 1
    if NormalizeDouble(BuyArrow[index], Digits()) and BuyArrow[index] != EMPTY_VALUE:
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
        Bid += Spread[index]
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
    if SeriesTest:
        index = _int(NumberofBar)
    else:
        index = Rates_total - _int(NumberofBar) - 1
    if NormalizeDouble(SellArrow[index], Digits()) and SellArrow[index] != EMPTY_VALUE:
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
        Bid += Spread[index]
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
_s_Recount_ArrayZeroPos_count = 1
_s_OnCalculate_Dss_prev = 0.0
_s_BuySignal_counter = 0
_s_SellSignal_counter = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DSSBressertSignAlert(_MQL5Indicator):
    name = 'DSSBressertSignAlert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'EMA_period': 8,  # период EMA
        'Sto_period': 13,  # период стохастика
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'NumberofBar': 1,  # Номер бара для подачи сигнала
        'SoundON': True,  # Разрешение алерта
        'NumberofAlerts': 2,  # Количество алертов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
    }

