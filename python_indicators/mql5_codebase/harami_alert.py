"""Harami_Alert — converted from MQL5: MQL5 Indicators/Harami_Alert/Harami_Alert.mq5

Harami
Copyright: Copyright © 2009, Paul Stringer; Link: http://www.metaquotes.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Paul Stringer', 'link': 'http://www.metaquotes.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Up Harami', 2: 'Down Harami'}, 'levels': [], 'description': ['Harami'], 'name': 'Harami_Alert', 'source': 'MQL5 Indicators/Harami_Alert/Harami_Alert.mq5', 'folder': 'Harami_Alert', 'inputs': [{'mql': 'MinMasterSize', 'py': 'MinMasterSize', 'param': 'MinMasterSize', 'type': 'uint', 'default': 40, 'label': '', 'sinput': False}, {'mql': 'MaxMasterSize', 'py': 'MaxMasterSize', 'param': 'MaxMasterSize', 'type': 'uint', 'default': 500, 'label': '', 'sinput': False}, {'mql': 'MinHaramiSize', 'py': 'MinHaramiSize', 'param': 'MinHaramiSize', 'type': 'uint', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'MaxHaramiSize', 'py': 'MaxHaramiSize', 'param': 'MaxHaramiSize', 'type': 'uint', 'default': 300, 'label': '', 'sinput': False}, {'mql': 'MaxRatioHaramiToMaster', 'py': 'MaxRatioHaramiToMaster', 'param': 'MaxRatioHaramiToMaster', 'type': 'double', 'default': 0.75, 'label': '', 'sinput': False}, {'mql': 'MinRatioHaramiToMaster', 'py': 'MinRatioHaramiToMaster', 'param': 'MinRatioHaramiToMaster', 'type': 'double', 'default': 0.5, 'label': '', 'sinput': False}, {'mql': 'ArrowOffSet', 'py': 'ArrowOffSet', 'param': 'ArrowOffSet', 'type': 'uint', 'default': 35, 'label': '', 'sinput': False}, {'mql': 'UpLable', 'py': 'UpLable', 'param': 'UpLable', 'type': 'int', 'default': 218, 'label': 'лейба верхнего фрактала', 'sinput': False}, {'mql': 'DnLable', 'py': 'DnLable', 'param': 'DnLable', 'type': 'int', 'default': 217, 'label': 'лейба нижнего фрактала', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для подачи сигнала', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Разрешение алерта', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': 'Количество алертов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MinMasterSize = _input('MinMasterSize', 40)
MaxMasterSize = _input('MaxMasterSize', 500)
MinHaramiSize = _input('MinHaramiSize', 20)
MaxHaramiSize = _input('MaxHaramiSize', 300)
MaxRatioHaramiToMaster = _input('MaxRatioHaramiToMaster', 0.75)
MinRatioHaramiToMaster = _input('MinRatioHaramiToMaster', 0.5)
ArrowOffSet = _input('ArrowOffSet', 35)
UpLable = _input('UpLable', 218)  # лейба верхнего фрактала
DnLable = _input('DnLable', 217)  # лейба нижнего фрактала
NumberofBar = _input('NumberofBar', 1)  # Номер бара для подачи сигнала
SoundON = _input('SoundON', True)  # Разрешение алерта
NumberofAlerts = _input('NumberofAlerts', 2)  # Количество алертов
EMailON = _input('EMailON', False)  # Разрешение почтовой отправки сигнала
PushON = _input('PushON', False)  # Разрешение отправки сигнала на мобильный
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
dMinMasterSize = 0.0
dMaxMasterSize = 0.0
dMinHaramiSize = 0.0
dMaxHaramiSize = 0.0
dArrowOffSet = 0.0

def OnInit():
    global dArrowOffSet, dMaxHaramiSize, dMaxMasterSize, dMinHaramiSize, dMinMasterSize, min_rates_total
    min_rates_total = 6
    dMinMasterSize = MinMasterSize * Point()
    dMaxMasterSize = MaxMasterSize * Point()
    dMinHaramiSize = MinHaramiSize * Point()
    dMaxHaramiSize = MaxHaramiSize * Point()
    dArrowOffSet = ArrowOffSet * Point()
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, UpLable)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, DnLable)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Harami'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    for bar in range(limit, 1 - 1, -1):
        SellBuffer[bar - 1] = 0.0
        BuyBuffer[bar - 1] = SellBuffer[bar - 1]
        _MasterBarSize = MathAbs(open[bar + 1] - close[bar + 1])
        _HaramiBarSize = MathAbs(open[bar] - close[bar])
        MaxM = _MasterBarSize - dMaxMasterSize
        MinM = _MasterBarSize - dMinMasterSize
        MaxH = _HaramiBarSize - dMaxHaramiSize
        MinH = _HaramiBarSize - dMinHaramiSize
        if not _MasterBarSize:
            _MasterBarSize = Point()
        res = _fdiv(_HaramiBarSize, _MasterBarSize)
        if ((((MaxM and MinM) and MaxH) and MinH) and res <= MaxRatioHaramiToMaster) and res >= MinRatioHaramiToMaster:
            if ((open[bar + 1] > close[bar + 1] and open[bar] < close[bar]) and close[bar + 1] < open[bar]) and open[bar + 1] > close[bar]:
                BuyBuffer[bar - 1] = low[bar - 1] - dArrowOffSet
            if ((open[bar + 1] < close[bar + 1] and open[bar] > close[bar]) and close[bar + 1] > open[bar]) and open[bar + 1] < close[bar]:
                SellBuffer[bar - 1] = high[bar - 1] + dArrowOffSet
    BuySignal('Harami_Alert', BuyBuffer, rates_total, prev_calculated, close, spread)
    SellSignal('Harami_Alert', SellBuffer, rates_total, prev_calculated, close, spread)
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
_s_BuySignal_counter = 0
_s_SellSignal_counter = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HaramiAlert(_MQL5Indicator):
    name = 'Harami_Alert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MinMasterSize': 40,
        'MaxMasterSize': 500,
        'MinHaramiSize': 20,
        'MaxHaramiSize': 300,
        'MaxRatioHaramiToMaster': 0.75,
        'MinRatioHaramiToMaster': 0.5,
        'ArrowOffSet': 35,
        'UpLable': 218,  # лейба верхнего фрактала
        'DnLable': 217,  # лейба нижнего фрактала
        'NumberofBar': 1,  # Номер бара для подачи сигнала
        'SoundON': True,  # Разрешение алерта
        'NumberofAlerts': 2,  # Количество алертов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
    }

