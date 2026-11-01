"""rvi-crossover_alert — converted from MQL5: MQL5 Indicators/RVI-Crossover_Alert/rvi-crossover_alert.mq5

Copyright: Copyright © 2005, Jason Robinson (jnrtrading); Link: http://www.jnrtrading.co.uk; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Jason Robinson (jnrtrading)', 'link': 'http://www.jnrtrading.co.uk', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [8721863], 2: [11186720]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'RVI-Crossover_Alert Sell', 2: 'RVI-Crossover_Alert Buy'}, 'levels': [], 'description': [], 'name': 'rvi-crossover_alert', 'source': 'MQL5 Indicators/RVI-Crossover_Alert/rvi-crossover_alert.mq5', 'folder': 'RVI-Crossover_Alert', 'inputs': [{'mql': 'RVI_Period', 'py': 'RVI_Period', 'param': 'RVI_Period', 'type': 'uint', 'default': 5, 'label': 'Period of averaging for RVI', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RVI_Period = _input('RVI_Period', 5)  # Period of averaging for RVI
SoundON = True  # Allow alert
EMailON = False  # Allow mailing signal
PushON = False  # Allow to send a signal to the mobile
NumberofAlerts = _input('NumberofAlerts', 2)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
counter = 0
RVI_Handle = 0
min_rates_total = 0

def OnInit():
    global RVI_Handle, min_rates_total
    min_rates_total = _int(RVI_Period + 3 + 9)
    RVI_Handle = iRVI(None, 0, RVI_Period)
    if RVI_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the RVI indicator')
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'RVI-Crossover_Alert'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global counter
    if rates_total < min_rates_total or BarsCalculated(RVI_Handle) < rates_total:
        return 0
    limit = 0
    count = 0
    RVInow = 0.0
    Signalnow = 0.0
    RVIprevious = 0.0
    Signalprevious = 0.0
    Range = 0.0
    AvgRange = 0.0
    RVI = Arr(0, 0.0)
    Ask = 0.0
    Bid = 0.0
    text = ""
    sAsk = ""
    sBid = ""
    sPeriod = ""
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(RVI, True)
    ArraySetAsSeries(RVI, True)
    for bar in range(limit, 0 - 1, -1):
        count = bar
        Range = 0.0
        AvgRange = 0.0
        count = bar
        for count in range(count, bar + 9 + 1):
            AvgRange = AvgRange + MathAbs(high[count] - low[count])
        else:
            count = _range_end(count, bar + 9 + 1, 1)
        Range = AvgRange / 10
        if CopyBuffer(RVI_Handle, MAIN_LINE, bar, 2, RVI) <= 0:
            return 0
        RVInow = RVI[0]
        RVIprevious = RVI[1]
        if CopyBuffer(RVI_Handle, SIGNAL_LINE, bar, 2, RVI) <= 0:
            return 0
        Signalnow = RVI[0]
        Signalprevious = RVI[1]
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if RVInow > Signalnow and RVIprevious < Signalprevious:
            BuyBuffer[bar] = low[bar] - (Range * 0.75)
        if RVInow < Signalnow and RVIprevious > Signalprevious:
            SellBuffer[bar] = high[bar] + (Range * 0.75)
    if rates_total != prev_calculated:
        counter = 0
    if BuyBuffer[1] and counter <= NumberofAlerts:
        counter += 1
        tm = MqlDateTime()
        TimeToStruct(TimeCurrent(), tm)
        text = TimeToString(TimeCurrent(), TIME_DATE) + ' ' + _str(tm.hour) + ':' + _str(tm.min)
        Ask = close[0]
        Bid = close[0] + spread[0]
        sAsk = DoubleToString(Ask, Digits())
        sBid = DoubleToString(Bid, Digits())
        sPeriod = EnumToString(ChartPeriod(), '')
        if SoundON:
            Alert('BUY signal at Ask=', Ask, '\n Bid=', Bid, '\n currtime=', text, '\n Symbol=', Symbol(), ' Period=', sPeriod)
        if EMailON:
            SendMail('RVI-Crossover_Alert: BUY signal alert', 'BUY signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
        if PushON:
            SendNotification('RVI-Crossover_Alert: BUY signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
    if SellBuffer[1] and counter <= NumberofAlerts:
        counter += 1
        tm = MqlDateTime()
        TimeToStruct(TimeCurrent(), tm)
        text = TimeToString(TimeCurrent(), TIME_DATE) + ' ' + _str(tm.hour) + ':' + _str(tm.min)
        Ask = close[0]
        Bid = close[0] + spread[0]
        sAsk = DoubleToString(Ask, Digits())
        sBid = DoubleToString(Bid, Digits())
        sPeriod = EnumToString(ChartPeriod(), '')
        if SoundON:
            Alert('SELL signal at Ask=', sAsk, '\n Bid=', sBid, '\n Date=', text, '\n Symbol=', Symbol(), ' Period=', sPeriod)
        if EMailON:
            SendMail('RVI-Crossover_Alert: SELL signal alert', 'SELL signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
        if PushON:
            SendNotification('RVI-Crossover_Alert: SELL signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RviCrossoverAlert(_MQL5Indicator):
    name = 'rvi-crossover_alert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RVI_Period': 5,  # Period of averaging for RVI
        'NumberofAlerts': 2,
    }

