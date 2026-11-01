"""wlxBW5ZoneAlert — converted from MQL5: MQL5 Indicators/wlxBW5ZoneAlert/wlxBW5ZoneAlert.mq5

Copyright: Copyright © 2005, Wellx; Link: http://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Wellx', 'link': 'http://www.metaquotes.net/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'wlxBW5ZoneAlert Sell', 2: 'wlxBW5ZoneAlert Buy'}, 'levels': [], 'description': [], 'name': 'wlxBW5ZoneAlert', 'source': 'MQL5 Indicators/wlxBW5ZoneAlert/wlxBW5ZoneAlert.mq5', 'folder': 'wlxBW5ZoneAlert', 'inputs': [{'mql': 'Dir', 'py': 'Dir', 'param': 'Dir', 'type': 'int', 'default': 0, 'label': 'Направление сигналов', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для подачи сигнала', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Разрешение алерта', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': 'Количество алертов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Direct
ON = 0
OFF = 1
_enum('Direct', {0: 'ON', 1: 'OFF'})

# ---- inputs and global variables
Dir = _input('Dir', ON)  # Направление сигналов
NumberofBar = _input('NumberofBar', 1)  # Номер бара для подачи сигнала
SoundON = _input('SoundON', True)  # Разрешение алерта
NumberofAlerts = _input('NumberofAlerts', 2)  # Количество алертов
EMailON = _input('EMailON', False)  # Разрешение почтовой отправки сигнала
PushON = _input('PushON', False)  # Разрешение отправки сигнала на мобильный
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
AC_Handle = 0
AO_Handle = 0
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global AC_Handle, AO_Handle, ATR_Handle, min_rates_total
    ATR_Period = 12
    AC_Period = 37
    AO_Period = 33
    min_rates_total = MathMax(MathMax(AC_Period, AO_Period) + 4, ATR_Period)
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    AC_Handle = iAC(Symbol(), PERIOD_CURRENT)
    if AC_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора  Accelerator Oscillator')
        return INIT_FAILED
    AO_Handle = iAO(Symbol(), PERIOD_CURRENT)
    if AO_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора  Awesome Oscillator')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 119)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'wlxBW5ZoneAlert'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_flagDown_, _s_OnCalculate_flagUP_
    if ((BarsCalculated(AC_Handle) < rates_total or BarsCalculated(AO_Handle) < rates_total) or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    AC = Arr(0, 0.0)
    AO = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    range_ = 0.0
    flagUP = False
    flagDown = False
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        _s_OnCalculate_flagUP_ = False
        _s_OnCalculate_flagDown_ = False
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    to_copy += 4
    if CopyBuffer(AC_Handle, 0, 0, to_copy, AC) <= 0:
        return 0
    if CopyBuffer(AO_Handle, 0, 0, to_copy, AO) <= 0:
        return 0
    ArraySetAsSeries(AC, True)
    ArraySetAsSeries(AO, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    flagUP = _s_OnCalculate_flagUP_
    flagDown = _s_OnCalculate_flagDown_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if not flagUP:
            if (((AO[bar] > AO[bar + 1] and AO[bar + 1] > AO[bar + 2]) and AO[bar + 2] > AO[bar + 3]) and AO[bar + 3] > AO[bar + 4]) and (((AC[bar] > AC[bar + 1] and AC[bar + 1] > AC[bar + 2]) and AC[bar + 2] > AC[bar + 3]) and AC[bar + 3] > AC[bar + 4]):
                range_ = (ATR[bar] * 3) / 8
                if Dir == ON:
                    BuyBuffer[bar] = low[bar] - range_
                else:
                    SellBuffer[bar] = high[bar] + range_
                flagUP = True
        if not flagDown:
            if (((AO[bar] < AO[bar + 1] and AO[bar + 1] < AO[bar + 2]) and AO[bar + 2] < AO[bar + 3]) and AO[bar + 3] < AO[bar + 4]) and (((AC[bar] < AC[bar + 1] and AC[bar + 1] < AC[bar + 2]) and AC[bar + 2] < AC[bar + 3]) and AC[bar + 3] < AC[bar + 4]):
                range_ = (ATR[bar] * 3) / 8
                if Dir == ON:
                    SellBuffer[bar] = high[bar] + range_
                else:
                    BuyBuffer[bar] = low[bar] - range_
                flagDown = True
        if AO[bar + 0] < AO[bar + 1] or AC[bar + 0] < AC[bar + 1]:
            flagUP = False
        if AO[bar + 0] > AO[bar + 1] or AC[bar + 0] > AC[bar + 1]:
            flagDown = False
        if bar:
            _s_OnCalculate_flagUP_ = flagUP
            _s_OnCalculate_flagDown_ = flagDown
    else:
        bar = _range_end(bar, 0 - 1, -1)
    BuySignal('wlxBW5ZoneAlert', BuyBuffer, rates_total, prev_calculated, close, spread)
    SellSignal('wlxBW5ZoneAlert', SellBuffer, rates_total, prev_calculated, close, spread)
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
_s_OnCalculate_flagUP_ = False
_s_OnCalculate_flagDown_ = False
_s_BuySignal_counter = 0
_s_SellSignal_counter = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WlxBW5ZoneAlert(_MQL5Indicator):
    name = 'wlxBW5ZoneAlert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Dir': _Choice({0: 'По тренду', 1: 'Против тренда'}, default=0),  # Направление сигналов
        'NumberofBar': 1,  # Номер бара для подачи сигнала
        'SoundON': True,  # Разрешение алерта
        'NumberofAlerts': 2,  # Количество алертов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
    }

