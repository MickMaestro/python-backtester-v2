"""Ozymandias_System_Alert — converted from MQL5: MQL5 Indicators/Ozymandias_System_Alert/Ozymandias_System_Alert.mq5

Copyright: Copyright © 2014, GoldnMoney; Link: http://www.mql5.com; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, GoldnMoney', 'link': 'http://www.mql5.com', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 4}, 'types': {1: 8, 2: 1, 3: 1, 4: 17}, 'colors': {1: [9639167, 16748574], 2: [9408444], 3: [9408444], 4: [55295, 2763429, 32768, 3329330]}, 'widths': {1: 3, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Ozymandias', 2: 'Upper Ozymandias', 3: 'Lower Ozymandias', 4: 'OzymandiasOpen;OzymandiasHigh;OzymandiasLow;OzymandiasClose'}, 'levels': [], 'description': [], 'name': 'Ozymandias_System_Alert', 'source': 'MQL5 Indicators/Ozymandias_System_Alert/Ozymandias_System_Alert.mq5', 'folder': 'Ozymandias_System_Alert', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'uint', 'default': 0, 'label': 'Сдвиг канала по горизонтали в право в барах', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для подачи сигнала', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Разрешение алерта', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': 'Количество алертов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 2)
MAType = _input('MAType', MODE_SMA)
Shift = _input('Shift', 0)  # Сдвиг канала по горизонтали в право в барах
NumberofBar = _input('NumberofBar', 1)  # Номер бара для подачи сигнала
SoundON = _input('SoundON', True)  # Разрешение алерта
NumberofAlerts = _input('NumberofAlerts', 2)  # Количество алертов
EMailON = _input('EMailON', False)  # Разрешение почтовой отправки сигнала
PushON = _input('PushON', False)  # Разрешение отправки сигнала на мобильный
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
min_rates_total = 0
ATR_Handle = 0
HMA_Handle = 0
LMA_Handle = 0

def OnInit():
    global ATR_Handle, HMA_Handle, LMA_Handle, min_rates_total
    min_rates_total = _int(Length)
    ATR_Period = 100
    min_rates_total = MathMax(min_rates_total, ATR_Period)
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    HMA_Handle = iMA(None, 0, Length, 0, MAType, PRICE_HIGH)
    if HMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    LMA_Handle = iMA(None, 0, Length, 0, MAType, PRICE_LOW)
    if LMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    SetIndexBuffer(2, UpBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpBuffer, True)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    SetIndexBuffer(3, DnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, None)
    SetIndexBuffer(4, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(8, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    shortname = 'Ozymandias_System_Alert'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_maxl1, _s_OnCalculate_minh1, _s_OnCalculate_nexttrend1, _s_OnCalculate_trend1
    if ((BarsCalculated(ATR_Handle) < rates_total or BarsCalculated(HMA_Handle) < rates_total) or BarsCalculated(LMA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    trend0 = 0
    nexttrend0 = 0
    hh = 0.0
    ll = 0.0
    maxl0 = 0.0
    minh0 = 0.0
    lma = 0.0
    hma = 0.0
    atr = 0.0
    ATR = Arr(0, 0.0)
    HMA = Arr(0, 0.0)
    LMA = Arr(0, 0.0)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(HMA, True)
    ArraySetAsSeries(LMA, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_trend1 = 0
        _s_OnCalculate_nexttrend1 = 0
        _s_OnCalculate_maxl1 = 0.0
        _s_OnCalculate_minh1 = 9999999.0
        IndBuffer[limit + 1] = close[limit + 1]
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    if CopyBuffer(HMA_Handle, 0, 0, to_copy, HMA) <= 0:
        return 0
    if CopyBuffer(LMA_Handle, 0, 0, to_copy, LMA) <= 0:
        return 0
    nexttrend0 = _s_OnCalculate_nexttrend1
    maxl0 = _s_OnCalculate_maxl1
    minh0 = _s_OnCalculate_minh1
    for bar in range(limit, 0 - 1, -1):
        hh = high[ArrayMaximum(high, bar, Length)]
        ll = low[ArrayMinimum(low, bar, Length)]
        lma = LMA[bar]
        hma = HMA[bar]
        atr = ATR[bar] / 2
        trend0 = _s_OnCalculate_trend1
        if nexttrend0 == 1:
            maxl0 = MathMax(ll, maxl0)
            if hma < maxl0 and close[bar] < low[bar + 1]:
                trend0 = 1
                nexttrend0 = 0
                minh0 = hh
        if nexttrend0 == 0:
            minh0 = MathMin(hh, minh0)
            if lma > minh0 and close[bar] > high[bar + 1]:
                trend0 = 0
                nexttrend0 = 1
                maxl0 = ll
        if trend0 == 0:
            if _s_OnCalculate_trend1 != 0.0:
                IndBuffer[bar] = IndBuffer[bar + 1]
                ColorIndBuffer[bar] = 1.0
            else:
                IndBuffer[bar] = MathMax(maxl0, IndBuffer[bar + 1])
                ColorIndBuffer[bar] = 1.0
            UpBuffer[bar] = IndBuffer[bar] + atr
            DnBuffer[bar] = IndBuffer[bar] - atr
        else:
            if _s_OnCalculate_trend1 != 1:
                IndBuffer[bar] = IndBuffer[bar + 1]
                ColorIndBuffer[bar] = 0.0
            else:
                IndBuffer[bar] = MathMin(minh0, IndBuffer[bar + 1])
                ColorIndBuffer[bar] = 0.0
            UpBuffer[bar] = IndBuffer[bar] + atr
            DnBuffer[bar] = IndBuffer[bar] - atr
        if bar:
            _s_OnCalculate_nexttrend1 = nexttrend0
            _s_OnCalculate_trend1 = trend0
            _s_OnCalculate_maxl1 = maxl0
            _s_OnCalculate_minh1 = minh0
    for bar in range(limit, 0 - 1, -1):
        ExtColorBuffer[bar] = 0.0
        ExtLowBuffer[bar] = ExtColorBuffer[bar]
        ExtHighBuffer[bar] = ExtLowBuffer[bar]
        ExtCloseBuffer[bar] = ExtHighBuffer[bar]
        ExtOpenBuffer[bar] = ExtCloseBuffer[bar]
        ExtColorBuffer[bar] = 4.0
        if close[bar] > UpBuffer[bar + Shift]:
            ExtOpenBuffer[bar] = open[bar]
            ExtCloseBuffer[bar] = close[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
            if close[bar] >= open[bar]:
                ExtColorBuffer[bar] = 3.0
            else:
                ExtColorBuffer[bar] = 2.0
        if close[bar] < DnBuffer[bar + Shift]:
            ExtOpenBuffer[bar] = open[bar]
            ExtCloseBuffer[bar] = close[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
            if close[bar] <= open[bar]:
                ExtColorBuffer[bar] = 0.0
            else:
                ExtColorBuffer[bar] = 1.0
    BuySignal('Ozymandias_System_Alert', ExtColorBuffer, rates_total, prev_calculated, close, spread)
    SellSignal('Ozymandias_System_Alert', ExtColorBuffer, rates_total, prev_calculated, close, spread)
    return rates_total

def BuySignal(SignalSirname, ColorArrow, Rates_total, Prev_calculated, Close, Spread):
    global _s_BuySignal_counter
    if Rates_total != Prev_calculated:
        _s_BuySignal_counter = 0
    BuySignal_ = False
    SeriesTest = ArrayGetAsSeries(ColorArrow)
    index = 0
    index1 = 0
    if SeriesTest:
        index = _int(NumberofBar)
        index1 = index + 1
    else:
        index = Rates_total - _int(NumberofBar) - 1
        index1 = index - 1
    if (ColorArrow[index] == 2 or ColorArrow[index] == 3) and (ColorArrow[index1] < 2 or ColorArrow[index1] == 4):
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

def SellSignal(SignalSirname, ColorArrow, Rates_total, Prev_calculated, Close, Spread):
    global _s_SellSignal_counter
    if Rates_total != Prev_calculated:
        _s_SellSignal_counter = 0
    SellSignal_ = False
    SeriesTest = ArrayGetAsSeries(ColorArrow)
    index = 0
    index1 = 0
    if SeriesTest:
        index = _int(NumberofBar)
        index1 = index + 1
    else:
        index = Rates_total - _int(NumberofBar) - 1
        index1 = index - 1
    if (ColorArrow[index] == 0 or ColorArrow[index] == 1) and ColorArrow[index1] > 1:
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
_s_OnCalculate_trend1 = 0
_s_OnCalculate_nexttrend1 = 0
_s_OnCalculate_maxl1 = 0.0
_s_OnCalculate_minh1 = 0.0
_s_BuySignal_counter = 0
_s_SellSignal_counter = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class OzymandiasSystemAlert(_MQL5Indicator):
    name = 'Ozymandias_System_Alert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 2,
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Shift': 0,  # Сдвиг канала по горизонтали в право в барах
        'NumberofBar': 1,  # Номер бара для подачи сигнала
        'SoundON': True,  # Разрешение алерта
        'NumberofAlerts': 2,  # Количество алертов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
    }

