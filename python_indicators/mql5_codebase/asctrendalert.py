"""ASCtrendAlert — converted from MQL5: MQL5 Indicators/ASCtrendAlert/ASCtrendAlert.mq5

ASCtrend
Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16711680]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'ASCtrend Sell', 2: 'ASCtrend Buy'}, 'levels': [], 'description': ['ASCtrend'], 'name': 'ASCtrendAlert', 'source': 'MQL5 Indicators/ASCtrendAlert/ASCtrendAlert.mq5', 'folder': 'ASCtrendAlert', 'inputs': [{'mql': 'RISK', 'py': 'RISK', 'param': 'RISK', 'type': 'int', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для подачи сигнала', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Разрешение алерта', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': 'Количество алертов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RISK = _input('RISK', 4)
NumberofBar = _input('NumberofBar', 1)  # Номер бара для подачи сигнала
SoundON = _input('SoundON', True)  # Разрешение алерта
NumberofAlerts = _input('NumberofAlerts', 2)  # Количество алертов
EMailON = _input('EMailON', False)  # Разрешение почтовой отправки сигнала
PushON = _input('PushON', False)  # Разрешение отправки сигнала на мобильный
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
x1 = 0
x2 = 0
value10 = 0
value11 = 0
WPR_Handle = Arr(3, 0, dyn=False)

def OnInit():
    global min_rates_total, value10, value11, x1, x2
    x1 = 67 + RISK
    x2 = 33 - RISK
    value10 = 2
    value11 = value10
    min_rates_total = MathMax(3 + (RISK * 2), 4) + 1
    WPR_Handle[0] = iWPR(None, 0, 3)
    if WPR_Handle[0] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iWPR 1')
    WPR_Handle[1] = iWPR(None, 0, 4)
    if WPR_Handle[1] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iWPR 2')
    WPR_Handle[2] = iWPR(None, 0, 3 + (RISK * 2))
    if WPR_Handle[2] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iWPR 3')
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, 'ASCtrend Sell')
    PlotIndexSetInteger(0, PLOT_ARROW, 108)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(1, PLOT_LABEL, 'ASCtrend Buy')
    PlotIndexSetInteger(1, PLOT_ARROW, 108)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'ASCtrend'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global value11
    if ((BarsCalculated(WPR_Handle[0]) < rates_total or BarsCalculated(WPR_Handle[1]) < rates_total) or BarsCalculated(WPR_Handle[2]) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    count = 0
    iii = 0
    value2 = 0.0
    value3 = 0.0
    Vel = 0.0
    WPR = Arr(0, 0.0)
    TrueCount = 0.0
    Range = 0.0
    AvgRange = 0.0
    MRO1 = 0.0
    MRO2 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(WPR, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Range = 0.0
        AvgRange = 0.0
        count = bar
        for count in range(count, bar + 9 + 1):
            AvgRange = AvgRange + MathAbs(high[count] - low[count])
        else:
            count = _range_end(count, bar + 9 + 1, 1)
        Range = AvgRange / 10
        count = bar
        TrueCount = 0.0
        while count < (bar + 9) and TrueCount < 1:
            if MathAbs(open[count] - close[count + 1]) >= (Range * 2.0):
                TrueCount += 1
            count += 1
        if TrueCount >= 1:
            MRO1 = count
        else:
            MRO1 = -1.0
        count = bar
        TrueCount = 0.0
        while count < (bar + 6) and TrueCount < 1:
            if MathAbs(close[count + 3] - close[count]) >= (Range * 4.6):
                TrueCount += 1
            count += 1
        if TrueCount >= 1:
            MRO2 = count
        else:
            MRO2 = -1.0
        if MRO1 > -1:
            value11 = 0
        else:
            value11 = value10
        if MRO2 > -1:
            value11 = 1
        else:
            value11 = value10
        if CopyBuffer(WPR_Handle[value11], 0, bar, 1, WPR) <= 0:
            return 0
        value2 = 100 - MathAbs(WPR[0])
        SellBuffer[bar] = 0.0
        BuyBuffer[bar] = 0.0
        value3 = 0.0
        if value2 < x2:
            iii = 1
            while (bar + iii) < rates_total:
                if CopyBuffer(WPR_Handle[value11], 0, bar + iii, 1, WPR) <= 0:
                    return 0
                Vel = 100 - MathAbs(WPR[0])
                if Vel >= x2 and Vel <= x1:
                    iii += 1
                else:
                    break
            if Vel > x1:
                value3 = high[bar] + (Range * 0.5)
                SellBuffer[bar] = value3
        if value2 > x1:
            iii = 1
            while (bar + iii) < rates_total:
                if CopyBuffer(WPR_Handle[value11], 0, bar + iii, 1, WPR) <= 0:
                    return 0
                Vel = 100 - MathAbs(WPR[0])
                if Vel >= x2 and Vel <= x1:
                    iii += 1
                else:
                    break
            if Vel < x2:
                value3 = low[bar] - (Range * 0.5)
                BuyBuffer[bar] = value3
    else:
        bar = _range_end(bar, 0 - 1, -1)
    BuySignal('ASCtrend', BuyBuffer, rates_total, prev_calculated, close, spread)
    SellSignal('ASCtrend', SellBuffer, rates_total, prev_calculated, close, spread)
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
_s_BuySignal_counter = 0
_s_SellSignal_counter = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ASCtrendAlert(_MQL5Indicator):
    name = 'ASCtrendAlert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RISK': 4,
        'NumberofBar': 1,  # Номер бара для подачи сигнала
        'SoundON': True,  # Разрешение алерта
        'NumberofAlerts': 2,  # Количество алертов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
    }

