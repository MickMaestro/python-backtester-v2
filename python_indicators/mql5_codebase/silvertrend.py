"""SilverTrend — converted from MQL5: MQL5 Indicators/MultiSilverTrend_x10/SilverTrend.mq5

Copyright: SilverTrend  rewritten by CrazyChart; Link: http://viac.ru/; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'SilverTrend  rewritten by CrazyChart', 'link': 'http://viac.ru/', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [65280, 8421376, 8421504, 8388736, 255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'SilverTrendOpen;SilverTrendHigh;SilverTrendLow;SilverTrendClose'}, 'levels': [], 'description': [], 'name': 'SilverTrend', 'source': 'MQL5 Indicators/MultiSilverTrend_x10/SilverTrend.mq5', 'folder': 'MultiSilverTrend_x10', 'inputs': [{'mql': 'SSP', 'py': 'SSP', 'param': 'SSP', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'RISK', 'py': 'RISK', 'param': 'RISK', 'type': 'int', 'default': 3, 'label': 'степень риска', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для подачи сигнала', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Разрешение алерта', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': 'Количество алертов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SSP = _input('SSP', 9)
RISK = _input('RISK', 3)  # степень риска
NumberofBar = _input('NumberofBar', 1)  # Номер бара для подачи сигнала
SoundON = _input('SoundON', True)  # Разрешение алерта
NumberofAlerts = _input('NumberofAlerts', 2)  # Количество алертов
EMailON = _input('EMailON', False)  # Разрешение почтовой отправки сигнала
PushON = _input('PushON', False)  # Разрешение отправки сигнала на мобильный
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorsBuffer = Arr(0, 0.0)
K = 0
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = SSP + 1
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorsBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorsBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'SilverTrend'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global K, _s_OnCalculate_trend_prev
    if rates_total < min_rates_total:
        return 0
    limit = 0
    trend = 0
    Range = 0.0
    AvgRange = 0.0
    smin = 0.0
    smax = 0.0
    SsMax = 0.0
    SsMin = 0.0
    price = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        K = 33 - RISK
        limit = rates_total - min_rates_total
        _s_OnCalculate_trend_prev = 0
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(spread, True)
    for bar in range(limit, 0 - 1, -1):
        ExtOpenBuffer[bar] = open[bar]
        ExtHighBuffer[bar] = high[bar]
        ExtLowBuffer[bar] = low[bar]
        ExtCloseBuffer[bar] = close[bar]
        ExtColorsBuffer[bar] = 2.0
        trend = _s_OnCalculate_trend_prev
        Range = 0.0
        AvgRange = 0.0
        for iii in range(bar, bar + SSP + 1):
            AvgRange += MathAbs(high[iii] - low[iii])
        Range = AvgRange / (SSP + 1)
        SsMax = low[bar]
        SsMin = close[bar]
        for kkk in range(bar, bar + SSP - 1 + 1):
            price = high[kkk]
            if SsMax < price:
                SsMax = price
            price = low[kkk]
            if SsMin >= price:
                SsMin = price
        smin = SsMin + (((SsMax - SsMin) * K) / 100)
        smax = SsMax - (((SsMax - SsMin) * K) / 100)
        if close[bar] < smin:
            trend = -1
        if close[bar] > smax:
            trend = 1
        if trend > 0:
            if open[bar] <= close[bar]:
                ExtColorsBuffer[bar] = 0.0
            else:
                ExtColorsBuffer[bar] = 1.0
        if trend < 0:
            if open[bar] >= close[bar]:
                ExtColorsBuffer[bar] = 4.0
            else:
                ExtColorsBuffer[bar] = 3.0
        if bar > 0:
            _s_OnCalculate_trend_prev = trend
    BuySignal('SilverTrend', ExtColorsBuffer, rates_total, prev_calculated, close, spread)
    SellSignal('SilverTrend', ExtColorsBuffer, rates_total, prev_calculated, close, spread)
    return rates_total

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика!')
        Print('Следует изменить входные параметры индикатора!')
        return False
    return True

def BuySignal(SignalSirname, ColorBuff, Rates_total, Prev_calculated, Close, Spread):
    global _s_BuySignal_counter
    if Rates_total != Prev_calculated:
        _s_BuySignal_counter = 0
    BuySignal_ = False
    SeriesTest = ArrayGetAsSeries(ColorBuff)
    index = 0
    index1 = 0
    if SeriesTest:
        index = _int(NumberofBar)
        index1 = index + 1
    else:
        index = Rates_total - _int(NumberofBar) - 1
        index1 = index - 1
    if ColorBuff[index1] > 1 and ColorBuff[index] < 2:
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

def SellSignal(SignalSirname, ColorBuff, Rates_total, Prev_calculated, Close, Spread):
    global _s_SellSignal_counter
    if Rates_total != Prev_calculated:
        _s_SellSignal_counter = 0
    SellSignal_ = False
    SeriesTest = ArrayGetAsSeries(ColorBuff)
    index = 0
    index1 = 0
    if SeriesTest:
        index = _int(NumberofBar)
        index1 = index + 1
    else:
        index = Rates_total - _int(NumberofBar) - 1
        index1 = index - 1
    if ColorBuff[index1] < 3 and ColorBuff[index] > 2:
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

# ---- static local variables
_s_OnCalculate_trend_prev = 0
_s_BuySignal_counter = 0
_s_SellSignal_counter = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SilverTrend(_MQL5Indicator):
    name = 'SilverTrend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SSP': 9,
        'RISK': 3,  # степень риска
        'NumberofBar': 1,  # Номер бара для подачи сигнала
        'SoundON': True,  # Разрешение алерта
        'NumberofAlerts': 2,  # Количество алертов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
    }

