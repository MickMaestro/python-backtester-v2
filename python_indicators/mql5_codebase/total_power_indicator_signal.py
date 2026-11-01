"""Total_Power_Indicator_Signal — converted from MQL5: MQL5 Indicators/Total_Power_Indicator_Signal/Total_Power_Indicator_Signal.mq5

Displays the concentration of bull PowerBuffer periods, bear power periods
 and total periods when either bulls or bears had prevailance.
Copyright: Copyright © 2011, www.EarnForex.com; Link: http://www.earnforex.com/; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, www.EarnForex.com', 'link': 'http://www.earnforex.com/', 'version': '1.0', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'Total_Power_Indicator_Signal Sell', 2: 'Total_Power_Indicator_Signal Buy'}, 'levels': [], 'description': ['Displays the concentration of bull PowerBuffer periods, bear power periods', ' and total periods when either bulls or bears had prevailance.'], 'name': 'Total_Power_Indicator_Signal', 'source': 'MQL5 Indicators/Total_Power_Indicator_Signal/Total_Power_Indicator_Signal.mq5', 'folder': 'Total_Power_Indicator_Signal', 'inputs': [{'mql': 'PowerPeriod', 'py': 'PowerPeriod', 'param': 'PowerPeriod', 'type': 'int', 'default': 10, 'label': 'период индикатора', 'sinput': False}, {'mql': 'LookbackPeriod', 'py': 'LookbackPeriod', 'param': 'LookbackPeriod', 'type': 'int', 'default': 45, 'label': 'период сглаживания', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для подачи сигнала', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Разрешение алерта', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': 'Количество алертов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PowerPeriod = _input('PowerPeriod', 10)  # период индикатора
LookbackPeriod = _input('LookbackPeriod', 45)  # период сглаживания
NumberofBar = _input('NumberofBar', 1)  # Номер бара для подачи сигнала
SoundON = _input('SoundON', True)  # Разрешение алерта
NumberofAlerts = _input('NumberofAlerts', 2)  # Количество алертов
EMailON = _input('EMailON', False)  # Разрешение почтовой отправки сигнала
PushON = _input('PushON', False)  # Разрешение отправки сигнала на мобильный
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
Bulls_Handle = 0
Bears_Handle = 0
ATR_Handle = 0

def OnInit():
    global ATR_Handle, Bears_Handle, Bulls_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = LookbackPeriod + PowerPeriod
    min_rates_total = MathMax(min_rates_total, ATR_Period) + 2
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    Bulls_Handle = iBullsPower(None, 0, PowerPeriod)
    if Bulls_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Bulls')
        return INIT_FAILED
    Bears_Handle = iBearsPower(None, 0, PowerPeriod)
    if Bears_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Bears')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 93)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 93)
    ArraySetAsSeries(BuyBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Total Power Indicator(', PowerPeriod, ', ', LookbackPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Bears_prev, _s_OnCalculate_Bulls_prev
    if ((BarsCalculated(Bulls_Handle) < rates_total or BarsCalculated(Bears_Handle) < rates_total) or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    bearscount = 0
    bullscount = 0
    BULLS = Arr(0, 0.0)
    BEARS = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    Bulls = 0.0
    Bears = 0.0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(BULLS, True)
    ArraySetAsSeries(BEARS, True)
    ArraySetAsSeries(ATR, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + min_rates_total + 1
    if CopyBuffer(Bulls_Handle, 0, 0, to_copy, BULLS) <= 0:
        return 0
    if CopyBuffer(Bears_Handle, 0, 0, to_copy, BEARS) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        bearscount = 0
        bullscount = 0
        for kkk in range(LookbackPeriod - 1, 0 - 1, -1):
            if BULLS[bar + kkk] > 0:
                bullscount += 1
            if BEARS[bar + kkk] < 0:
                bearscount += 1
        Bulls = MathMax(0, MathMin(100, (_idiv(bullscount * 100, LookbackPeriod) - 50) * 2))
        Bears = MathMax(0, MathMin(100, (_idiv(bearscount * 100, LookbackPeriod) - 50) * 2))
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if _s_OnCalculate_Bulls_prev <= _s_OnCalculate_Bears_prev and Bulls > Bears:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if _s_OnCalculate_Bulls_prev >= _s_OnCalculate_Bears_prev and Bulls < Bears:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        if bar:
            _s_OnCalculate_Bulls_prev = Bulls
            _s_OnCalculate_Bears_prev = Bears
    else:
        bar = _range_end(bar, 0 - 1, -1)
    BuySignal('Total_Power_Indicator_Signal', BuyBuffer, rates_total, prev_calculated, close, spread)
    SellSignal('Total_Power_Indicator_Signal', SellBuffer, rates_total, prev_calculated, close, spread)
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
_s_OnCalculate_Bulls_prev = 0.0
_s_OnCalculate_Bears_prev = 0.0
_s_BuySignal_counter = 0
_s_SellSignal_counter = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TotalPowerIndicatorSignal(_MQL5Indicator):
    name = 'Total_Power_Indicator_Signal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PowerPeriod': 10,  # период индикатора
        'LookbackPeriod': 45,  # период сглаживания
        'NumberofBar': 1,  # Номер бара для подачи сигнала
        'SoundON': True,  # Разрешение алерта
        'NumberofAlerts': 2,  # Количество алертов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
    }

