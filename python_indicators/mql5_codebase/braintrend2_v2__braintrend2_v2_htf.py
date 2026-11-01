"""BrainTrend2_V2 — converted from MQL5: MQL5 Indicators/BrainTrend2_V2_HTF/BrainTrend2_V2.mq5

Copyright: Copyright © 2005, BrainTrading Inc.; Link: http://www.braintrading.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, BrainTrading Inc.', 'link': 'http://www.braintrading.com/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [65280, 8421376, 8421504, 128, 16711935]}, 'widths': {}, 'styles': {}, 'labels': {1: 'BrainTrend2Open;BrainTrend2High;BrainTrend2Low;BrainTrend2Close'}, 'levels': [], 'description': [], 'name': 'BrainTrend2_V2', 'source': 'MQL5 Indicators/BrainTrend2_V2_HTF/BrainTrend2_V2.mq5', 'folder': 'BrainTrend2_V2_HTF', 'inputs': [{'mql': 'ATR_Period', 'py': 'ATR_Period', 'param': 'ATR_Period', 'type': 'uint', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для подачи сигнала', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Разрешение алерта', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': 'Количество алертов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ATR_Period = _input('ATR_Period', 7)
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
river = True
river_ = False
glava = 0
glava_ = 0
min_rates_total = 0
dartp = 0.0
cecf = 0.0
Emaxtra = 0.0
Emaxtra_ = 0.0
Values_ = Arr(0, 0.0)
Values = Arr(0, 0.0)

def OnInit():
    global cecf, dartp, min_rates_total
    dartp = 7.0
    cecf = 0.7
    min_rates_total = _int(ATR_Period) + 2
    if ArrayResize(Values, ATR_Period) < _int(ATR_Period):
        Print('Не удалось распределить память под массив Values')
        return INIT_FAILED
    if ArrayResize(Values_, ATR_Period) < _int(ATR_Period):
        Print('Не удалось распределить память под массив Values_')
        return INIT_FAILED
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
    short_name = 'BrainTrend1_V2'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global Emaxtra, Emaxtra_, glava, glava_, river, river_
    if rates_total < min_rates_total:
        return 0
    bar = 0
    J = 0
    limit = 0
    Curr = 0
    ATR = 0.0
    widcha = 0.0
    TR = 0.0
    Spread = 0.0
    Weight = 0.0
    Series1 = 0.0
    High = 0.0
    Low = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        Emaxtra = close[limit + 1]
        glava = 0
        T_Series2 = close[limit + 2]
        T_Series1 = close[limit + 1]
        if T_Series2 > T_Series1:
            river = True
        else:
            river = False
        TR = spread[limit] + high[limit] - low[limit]
        if MathAbs(spread[limit] + high[limit] - T_Series1) > TR:
            TR = MathAbs(spread[limit] + high[limit] - T_Series1)
        if MathAbs(low[limit] - T_Series1) > TR:
            TR = MathAbs(low[limit] - T_Series1)
        ArrayInitialize(Values, TR)
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(spread, True)
    ArraySetAsSeries(Values, True)
    ArraySetAsSeries(Values_, True)
    glava = glava_
    Emaxtra = Emaxtra_
    river = river_
    ArrayCopy(Values, Values_, 0, WHOLE_ARRAY)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            glava_ = glava
            Emaxtra_ = Emaxtra
            river_ = river
            ArrayCopy(Values_, Values, 0, WHOLE_ARRAY)
        ExtOpenBuffer[bar] = 0.0
        ExtHighBuffer[bar] = 0.0
        ExtLowBuffer[bar] = 0.0
        ExtCloseBuffer[bar] = 0.0
        ExtColorsBuffer[bar] = 2.0
        Spread = spread[bar] * Point()
        High = high[bar]
        Low = low[bar]
        Series1 = close[bar + 1]
        TR = Spread + High - Low
        if MathAbs(Spread + High - Series1) > TR:
            TR = MathAbs(Spread + High - Series1)
        if MathAbs(Low - Series1) > TR:
            TR = MathAbs(Low - Series1)
        Values[glava] = TR
        ATR = 0.0
        Weight = ATR_Period
        Curr = glava
        J = 0
        for J in range(J, _int(ATR_Period) - 1 + 1):
            ATR += Values[Curr] * Weight
            Weight -= 1.0
            Curr -= 1
            if Curr == -1:
                Curr = _int(ATR_Period) - 1
        else:
            J = _range_end(J, _int(ATR_Period) - 1 + 1, 1)
        ATR = _fdiv(2.0 * ATR, dartp * (dartp + 1.0))
        glava += 1
        if glava == ATR_Period:
            glava = 0
        widcha = cecf * ATR
        if river and Low < (Emaxtra - widcha):
            river = False
            Emaxtra = Spread + High
        if (not river) and (Spread + High) > (Emaxtra + widcha):
            river = True
            Emaxtra = Low
        if river and Low > Emaxtra:
            Emaxtra = Low
        if (not river) and (Spread + High) < Emaxtra:
            Emaxtra = Spread + High
        if river:
            ExtOpenBuffer[bar] = open[bar]
            ExtHighBuffer[bar] = High
            ExtLowBuffer[bar] = Low
            ExtCloseBuffer[bar] = close[bar]
            if open[bar] <= close[bar]:
                ExtColorsBuffer[bar] = 0.0
            else:
                ExtColorsBuffer[bar] = 1.0
        else:
            ExtOpenBuffer[bar] = open[bar]
            ExtHighBuffer[bar] = High
            ExtLowBuffer[bar] = Low
            ExtCloseBuffer[bar] = close[bar]
            if open[bar] >= close[bar]:
                ExtColorsBuffer[bar] = 4.0
            else:
                ExtColorsBuffer[bar] = 3.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    BuySignal('BrainTrend2_V2', ExtColorsBuffer, rates_total, prev_calculated, close, spread)
    SellSignal('BrainTrend2_V2', ExtColorsBuffer, rates_total, prev_calculated, close, spread)
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
_s_BuySignal_counter = 0
_s_SellSignal_counter = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BrainTrend2V2(_MQL5Indicator):
    name = 'BrainTrend2_V2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ATR_Period': 7,
        'NumberofBar': 1,  # Номер бара для подачи сигнала
        'SoundON': True,  # Разрешение алерта
        'NumberofAlerts': 2,  # Количество алертов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
    }

