"""BBands_Stop_v1_Alert — converted from MQL5: MQL5 Indicators/BBands_Stop_v1_Alert/BBands_Stop_v1_Alert.mq5

Copyright: Copyright © 2005, TrendLaboratory Ltd.; Link: http://finance.groups.yahoo.com/group/TrendLaboratory; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, TrendLaboratory Ltd.', 'link': 'http://finance.groups.yahoo.com/group/TrendLaboratory', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 5, 2: 5, 3: 1, 4: 5, 5: 5, 6: 1}, 'colors': {1: [42495], 2: [42495], 3: [42495], 4: [65407], 5: [65407], 6: [65407]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {}, 'labels': {1: 'Sell Signal', 2: 'Sell Stop Signal', 3: 'Sell Stop Line', 4: 'Buy Signal', 5: 'Buy Stop Signal', 6: 'Buy Stop Line'}, 'levels': [], 'description': [], 'name': 'BBands_Stop_v1_Alert', 'source': 'MQL5 Indicators/BBands_Stop_v1_Alert/BBands_Stop_v1_Alert.mq5', 'folder': 'BBands_Stop_v1_Alert', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 20, 'label': 'Период Боллинджера', 'sinput': False}, {'mql': 'Deviation', 'py': 'Deviation', 'param': 'Deviation', 'type': 'double', 'default': 2.0, 'label': 'Девиация', 'sinput': False}, {'mql': 'MoneyRisk', 'py': 'MoneyRisk', 'param': 'MoneyRisk', 'type': 'double', 'default': 1.0, 'label': 'Offset Factor', 'sinput': False}, {'mql': 'Signal', 'py': 'Signal', 'param': 'Signal', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Line', 'py': 'Line', 'param': 'Line', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для подачи сигнала', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Разрешение алерта', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': 'Количество алертов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum DISPLAY_SIGNALS_MODE
OnlyStops = 0
SignalsStops = 1
OnlySignals = 2
_enum('DISPLAY_SIGNALS_MODE', {0: 'OnlyStops', 1: 'SignalsStops', 2: 'OnlySignals'})

# ---- inputs and global variables
Length = _input('Length', 20)  # Период Боллинджера
Deviation = _input('Deviation', 2.0)  # Девиация
MoneyRisk = _input('MoneyRisk', 1.0)  # Offset Factor
Signal = _input('Signal', SignalsStops)
Line = _input('Line', True)
NumberofBar = _input('NumberofBar', 1)  # Номер бара для подачи сигнала
SoundON = _input('SoundON', True)  # Разрешение алерта
NumberofAlerts = _input('NumberofAlerts', 2)  # Количество алертов
EMailON = _input('EMailON', False)  # Разрешение почтовой отправки сигнала
PushON = _input('PushON', False)  # Разрешение отправки сигнала на мобильный
UpTrendBuffer = Arr(0, 0.0)
DownTrendBuffer = Arr(0, 0.0)
UpTrendSignal = Arr(0, 0.0)
DownTrendSignal = Arr(0, 0.0)
UpTrendLine = Arr(0, 0.0)
DownTrendLine = Arr(0, 0.0)
BB_Handle = 0
min_rates_total = 0
MRisk = 0.0

def OnInit():
    global BB_Handle, MRisk, min_rates_total
    min_rates_total = Length + 1
    MRisk = 0.5 * (MoneyRisk - 1)
    BB_Handle = iBands(None, 0, Length, 0, Deviation, PRICE_CLOSE)
    if BB_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iBands')
    SetIndexBuffer(0, DownTrendSignal, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 108)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(DownTrendSignal, True)
    SetIndexBuffer(1, DownTrendBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(DownTrendBuffer, True)
    SetIndexBuffer(2, DownTrendLine, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(DownTrendLine, True)
    SetIndexBuffer(3, UpTrendSignal, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 108)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(UpTrendSignal, True)
    SetIndexBuffer(4, UpTrendBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_ARROW, 159)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(UpTrendBuffer, True)
    SetIndexBuffer(5, UpTrendLine, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(UpTrendLine, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = Box("")
    StringConcatenate(short_name, 'BBands_Stop(', Length, ', ', DoubleToString(Deviation, 2), ', ', DoubleToString(MoneyRisk, 2), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, short_name.v)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_bsmax1, _s_OnCalculate_bsmin1, _s_OnCalculate_smax1, _s_OnCalculate_smin1, _s_OnCalculate_trend_
    if BarsCalculated(BB_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    trend = 0
    to_copy = 0
    maxbar = 0
    smax0 = 0.0
    smin0 = 0.0
    bsmax0 = 0.0
    bsmin0 = 0.0
    UpBB = Arr(0, 0.0)
    DnBB = Arr(0, 0.0)
    dsize = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_smax1 = -999999999.0
        _s_OnCalculate_smin1 = 999999999.0
        _s_OnCalculate_bsmax1 = -999999999.0
        _s_OnCalculate_bsmin1 = 999999999.0
        _s_OnCalculate_trend_ = 0
        bar = rates_total - 1
        for bar in range(bar, limit, -1):
            UpTrendBuffer[bar] = 0.0
            DownTrendBuffer[bar] = 0.0
            UpTrendSignal[bar] = 0.0
            DownTrendSignal[bar] = 0.0
            UpTrendLine[bar] = 0.0
            DownTrendLine[bar] = 0.0
        else:
            bar = _range_end(bar, limit, -1)
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(UpBB, True)
    ArraySetAsSeries(DnBB, True)
    ArraySetAsSeries(close, True)
    to_copy = limit + 1
    maxbar = rates_total - min_rates_total - 1
    if CopyBuffer(BB_Handle, 1, 0, to_copy, UpBB) <= 0:
        return 0
    if CopyBuffer(BB_Handle, 2, 0, to_copy, DnBB) <= 0:
        return 0
    trend = _s_OnCalculate_trend_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            _s_OnCalculate_trend_ = trend
        smax0 = UpBB[bar]
        smin0 = DnBB[bar]
        UpTrendBuffer[bar] = 0.0
        DownTrendBuffer[bar] = 0.0
        UpTrendSignal[bar] = 0.0
        DownTrendSignal[bar] = 0.0
        UpTrendLine[bar] = 0.0
        DownTrendLine[bar] = 0.0
        if bar > maxbar:
            _s_OnCalculate_smin1 = smin0
            _s_OnCalculate_smax1 = smax0
            _s_OnCalculate_bsmax1 = _s_OnCalculate_smax1 + (MRisk * (_s_OnCalculate_smax1 - _s_OnCalculate_smin1))
            _s_OnCalculate_bsmin1 = _s_OnCalculate_smin1 - (MRisk * (_s_OnCalculate_smax1 - _s_OnCalculate_smin1))
            continue
        if close[bar] > _s_OnCalculate_smax1:
            trend = 1
        if close[bar] < _s_OnCalculate_smin1:
            trend = -1
        if trend > 0 and smin0 < _s_OnCalculate_smin1:
            smin0 = _s_OnCalculate_smin1
        if trend < 0 and smax0 > _s_OnCalculate_smax1:
            smax0 = _s_OnCalculate_smax1
        dsize = MRisk * (smax0 - smin0)
        bsmax0 = smax0 + dsize
        bsmin0 = smin0 - dsize
        if trend > 0 and bsmin0 < _s_OnCalculate_bsmin1:
            bsmin0 = _s_OnCalculate_bsmin1
        if trend < 0 and bsmax0 > _s_OnCalculate_bsmax1:
            bsmax0 = _s_OnCalculate_bsmax1
        if trend > 0:
            if Signal and (not UpTrendBuffer[bar + 1]):
                UpTrendSignal[bar] = bsmin0
                UpTrendBuffer[bar] = bsmin0
                if Line:
                    UpTrendLine[bar] = bsmin0
            else:
                UpTrendBuffer[bar] = bsmin0
                if Line:
                    UpTrendLine[bar] = bsmin0
                UpTrendSignal[bar] = 0.0
            if Signal == OnlySignals:
                UpTrendBuffer[bar] = 0.0
            DownTrendSignal[bar] = 0.0
            DownTrendBuffer[bar] = 0.0
            DownTrendLine[bar] = 0.0
        if trend < 0:
            if Signal and (not DownTrendBuffer[bar + 1]):
                DownTrendSignal[bar] = bsmax0
                DownTrendBuffer[bar] = bsmax0
                if Line:
                    DownTrendLine[bar] = bsmax0
            else:
                DownTrendBuffer[bar] = bsmax0
                if Line:
                    DownTrendLine[bar] = bsmax0
                DownTrendSignal[bar] = 0.0
            if Signal == OnlySignals:
                DownTrendBuffer[bar] = 0.0
            UpTrendSignal[bar] = 0.0
            UpTrendBuffer[bar] = 0.0
            UpTrendLine[bar] = 0.0
        if bar > 0:
            _s_OnCalculate_smax1 = smax0
            _s_OnCalculate_smin1 = smin0
            _s_OnCalculate_bsmax1 = bsmax0
            _s_OnCalculate_bsmin1 = bsmin0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    _sw1 = Signal
    if _sw1 == OnlyStops:
        BuySignal('BBands_Stop_v1_Alert', UpTrendBuffer, rates_total, prev_calculated, close, spread)
        SellSignal('BBands_Stop_v1_Alert', DownTrendBuffer, rates_total, prev_calculated, close, spread)
    elif _sw1 == SignalsStops:
        BuySignal('BBands_Stop_v1_Alert', UpTrendBuffer, rates_total, prev_calculated, close, spread)
        SellSignal('BBands_Stop_v1_Alert', DownTrendBuffer, rates_total, prev_calculated, close, spread)
    elif _sw1 == OnlySignals:
        BuySignal('BBands_Stop_v1_Alert', UpTrendSignal, rates_total, prev_calculated, close, spread)
        SellSignal('BBands_Stop_v1_Alert', DownTrendSignal, rates_total, prev_calculated, close, spread)
    return rates_total

def BuySignal(SignalSirname, UpArrow, Rates_total, Prev_calculated, Close, Spread):
    global _s_BuySignal_counter
    if Rates_total != Prev_calculated:
        _s_BuySignal_counter = 0
    BuySignal_ = False
    SeriesTest = ArrayGetAsSeries(UpArrow)
    index = 0
    index1 = 0
    if SeriesTest:
        index = _int(NumberofBar)
        index1 = index + 1
    else:
        index = Rates_total - _int(NumberofBar) - 1
        index1 = index - 1
    if UpArrow[index] and (not UpArrow[index1]):
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

def SellSignal(SignalSirname, DnArrow, Rates_total, Prev_calculated, Close, Spread):
    global _s_SellSignal_counter
    if Rates_total != Prev_calculated:
        _s_SellSignal_counter = 0
    SellSignal_ = False
    SeriesTest = ArrayGetAsSeries(DnArrow)
    index = 0
    index1 = 0
    if SeriesTest:
        index = _int(NumberofBar)
        index1 = index + 1
    else:
        index = Rates_total - _int(NumberofBar) - 1
        index1 = index - 1
    if DnArrow[index] and (not DnArrow[index1]):
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
_s_OnCalculate_trend_ = 0
_s_OnCalculate_smax1 = 0.0
_s_OnCalculate_smin1 = 0.0
_s_OnCalculate_bsmax1 = 0.0
_s_OnCalculate_bsmin1 = 0.0
_s_BuySignal_counter = 0
_s_SellSignal_counter = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BBandsStopV1Alert(_MQL5Indicator):
    name = 'BBands_Stop_v1_Alert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 20,  # Период Боллинджера
        'Deviation': 2.0,  # Девиация
        'MoneyRisk': 1.0,  # Offset Factor
        'Signal': _Choice({0: 'Only Stops', 1: 'Signals & Stops', 2: 'Only Signals'}, default=1),
        'Line': True,
        'NumberofBar': 1,  # Номер бара для подачи сигнала
        'SoundON': True,  # Разрешение алерта
        'NumberofAlerts': 2,  # Количество алертов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
    }

