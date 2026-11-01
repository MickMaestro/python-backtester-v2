"""rsi-crossover_alert — converted from MQL5: MQL5 Indicators/RSI-Crossover_Alert/rsi-crossover_alert.mq5

Copyright: Copyright © 2005, Jason Robinson (jnrtrading); Link: http://www.jnrtrading.co.uk; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Jason Robinson (jnrtrading)', 'link': 'http://www.jnrtrading.co.uk', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [16748574]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'RSI-Crossover_Alert Sell', 2: 'RSI-Crossover_Alert Buy'}, 'levels': [], 'description': [], 'name': 'rsi-crossover_alert', 'source': 'MQL5 Indicators/RSI-Crossover_Alert/rsi-crossover_alert.mq5', 'folder': 'RSI-Crossover_Alert', 'inputs': [{'mql': 'FastRSI_Period', 'py': 'FastRSI_Period', 'param': 'FastRSI_Period', 'type': 'uint', 'default': 5, 'label': 'Period of averaging for fast moving', 'sinput': False}, {'mql': 'FastPriceMode', 'py': 'FastPriceMode', 'param': 'FastPriceMode', 'type': 'int', 'default': 1, 'label': 'Price for fast moving', 'sinput': False}, {'mql': 'SlowRSI_Period', 'py': 'SlowRSI_Period', 'param': 'SlowRSI_Period', 'type': 'uint', 'default': 20, 'label': 'Period of averaging for slow moving', 'sinput': False}, {'mql': 'SlowPriceMode', 'py': 'SlowPriceMode', 'param': 'SlowPriceMode', 'type': 'int', 'default': 1, 'label': 'Price for slow moving', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FastRSI_Period = _input('FastRSI_Period', 5)  # Period of averaging for fast moving
FastPriceMode = _input('FastPriceMode', PRICE_CLOSE)  # Price for fast moving
SlowRSI_Period = _input('SlowRSI_Period', 20)  # Period of averaging for slow moving
SlowPriceMode = _input('SlowPriceMode', PRICE_CLOSE)  # Price for slow moving
SoundON = True  # Allow alert
EMailON = False  # Allow mailing signal
PushON = False  # Allow to send a signal to the mobile
NumberofAlerts = _input('NumberofAlerts', 2)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
counter = 0
FastRSI_Handle = 0
SlowRSI_Handle = 0
min_rates_total = 0

def OnInit():
    global FastRSI_Handle, SlowRSI_Handle, min_rates_total
    min_rates_total = _int(MathMax(FastRSI_Period, SlowRSI_Period) + 3 + 9)
    FastRSI_Handle = iRSI(None, 0, FastRSI_Period, FastPriceMode)
    if FastRSI_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the FastRSI indicator')
    SlowRSI_Handle = iRSI(None, 0, SlowRSI_Period, SlowPriceMode)
    if SlowRSI_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the SlowRSI indicator')
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
    short_name = 'RSI-Crossover_Alert'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global counter
    if (rates_total < min_rates_total or BarsCalculated(FastRSI_Handle) < rates_total) or BarsCalculated(SlowRSI_Handle) < rates_total:
        return 0
    limit = 0
    count = 0
    FastRSInow = 0.0
    SlowRSInow = 0.0
    FastRSIprevious = 0.0
    SlowRSIprevious = 0.0
    Range = 0.0
    AvgRange = 0.0
    RSI = Arr(0, 0.0)
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
    ArraySetAsSeries(RSI, True)
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
        if CopyBuffer(FastRSI_Handle, 0, bar, 2, RSI) <= 0:
            return 0
        FastRSInow = RSI[0]
        FastRSIprevious = RSI[1]
        if CopyBuffer(SlowRSI_Handle, 0, bar, 2, RSI) <= 0:
            return 0
        SlowRSInow = RSI[0]
        SlowRSIprevious = RSI[1]
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if FastRSInow > SlowRSInow and FastRSIprevious < SlowRSIprevious:
            BuyBuffer[bar] = low[bar] - (Range * 0.75)
        if FastRSInow < SlowRSInow and FastRSIprevious > SlowRSIprevious:
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
            SendMail('RSI-Crossover_Alert: BUY signal alert', 'BUY signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
        if PushON:
            SendNotification('RSI-Crossover_Alert: BUY signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
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
            SendMail('RSI-Crossover_Alert: SELL signal alert', 'SELL signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
        if PushON:
            SendNotification('RSI-Crossover_Alert: SELL signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RsiCrossoverAlert(_MQL5Indicator):
    name = 'rsi-crossover_alert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastRSI_Period': 5,  # Period of averaging for fast moving
        'FastPriceMode': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price for fast moving
        'SlowRSI_Period': 20,  # Period of averaging for slow moving
        'SlowPriceMode': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price for slow moving
        'NumberofAlerts': 2,
    }

