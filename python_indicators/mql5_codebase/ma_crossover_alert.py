"""ma-crossover_alert — converted from MQL5: MQL5 Indicators/MA-Crossover_Alert/ma-crossover_alert.mq5

Copyright: Copyright © 2005, Jason Robinson (jnrtrading); Link: http://www.jnrtrading.co.uk; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Jason Robinson (jnrtrading)', 'link': 'http://www.jnrtrading.co.uk', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'MA-Crossover_Alert Sell', 2: 'MA-Crossover_Alert Buy'}, 'levels': [], 'description': [], 'name': 'ma-crossover_alert', 'source': 'MQL5 Indicators/MA-Crossover_Alert/ma-crossover_alert.mq5', 'folder': 'MA-Crossover_Alert', 'inputs': [{'mql': 'FastMA_Mode', 'py': 'FastMA_Mode', 'param': 'FastMA_Mode', 'type': 'int', 'default': 1, 'label': 'Smoothing method for fast moving', 'sinput': False}, {'mql': 'FastMA_Period', 'py': 'FastMA_Period', 'param': 'FastMA_Period', 'type': 'uint', 'default': 5, 'label': 'Period of averaging for fast moving', 'sinput': False}, {'mql': 'FastPriceMode', 'py': 'FastPriceMode', 'param': 'FastPriceMode', 'type': 'int', 'default': 1, 'label': 'Price for fast moving', 'sinput': False}, {'mql': 'SlowMA_Mode', 'py': 'SlowMA_Mode', 'param': 'SlowMA_Mode', 'type': 'int', 'default': 1, 'label': 'Smoothing method for slow moving', 'sinput': False}, {'mql': 'SlowMA_Period', 'py': 'SlowMA_Period', 'param': 'SlowMA_Period', 'type': 'uint', 'default': 20, 'label': 'Period of averaging for slow moving', 'sinput': False}, {'mql': 'SlowPriceMode', 'py': 'SlowPriceMode', 'param': 'SlowPriceMode', 'type': 'int', 'default': 1, 'label': 'Price for slow moving', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Smooth_Method
MODE_SMA_ = 0
MODE_EMA_ = 1
MODE_SMMA_ = 2
MODE_LWMA_ = 3
MODE_LSMA_ = 4
_enum('Smooth_Method', {0: 'MODE_SMA_', 1: 'MODE_EMA_', 2: 'MODE_SMMA_', 3: 'MODE_LWMA_', 4: 'MODE_LSMA_'})

# ---- inputs and global variables
FastMA_Mode = _input('FastMA_Mode', MODE_EMA_)  # Smoothing method for fast moving
FastMA_Period = _input('FastMA_Period', 5)  # Period of averaging for fast moving
FastPriceMode = _input('FastPriceMode', PRICE_CLOSE)  # Price for fast moving
SlowMA_Mode = _input('SlowMA_Mode', MODE_EMA_)  # Smoothing method for slow moving
SlowMA_Period = _input('SlowMA_Period', 20)  # Period of averaging for slow moving
SlowPriceMode = _input('SlowPriceMode', PRICE_CLOSE)  # Price for slow moving
SoundON = True  # Alert
EmailON = False  # Email
NumberofAlerts = _input('NumberofAlerts', 2)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
counter = 0
flagval1 = False
flagval2 = False
FaMA_Handle = 0
SlMA_Handle = 0
StartBars = 0

def OnInit():
    global FaMA_Handle, SlMA_Handle, StartBars
    StartBars = _int(MathMax(FastMA_Period, SlowMA_Period) + 3 + 9)
    if FastMA_Mode != MODE_LSMA_:
        FaMA_Handle = iMA(None, 0, FastMA_Period, 0, FastMA_Mode, FastPriceMode)
        if FaMA_Handle == INVALID_HANDLE:
            Print(' Failed to get handle of the FaMA indicator')
    if SlowMA_Mode != MODE_LSMA_:
        SlMA_Handle = iMA(None, 0, SlowMA_Period, 0, SlowMA_Mode, SlowPriceMode)
        if SlMA_Handle == INVALID_HANDLE:
            Print(' Failed to get handle of the SlMA indicator')
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'MA-Crossover_Alert'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global counter, flagval1, flagval2
    if rates_total < StartBars:
        return 0
    if FastMA_Mode != MODE_LSMA_ and BarsCalculated(FaMA_Handle) < rates_total:
        return 0
    if SlowMA_Mode != MODE_LSMA_ and BarsCalculated(SlMA_Handle) < rates_total:
        return 0
    limit = 0
    count = 0
    fastMAnow = 0.0
    slowMAnow = 0.0
    fastMAprevious = 0.0
    slowMAprevious = 0.0
    Range = 0.0
    AvgRange = 0.0
    MA = Arr(0, 0.0)
    Ask = 0.0
    Bid = 0.0
    text = ""
    sAsk = ""
    sBid = ""
    sPeriod = ""
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - StartBars
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(MA, True)
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
        if FastMA_Mode == MODE_LSMA_:
            fastMAnow = LSMA(open, high, low, close, FastMA_Period, FastPriceMode, bar)
            fastMAprevious = LSMA(open, high, low, close, FastMA_Period, FastPriceMode, bar + 1)
        else:
            if CopyBuffer(FaMA_Handle, 0, bar, 2, MA) <= 0:
                return 0
            fastMAnow = MA[0]
            fastMAprevious = MA[1]
        if SlowMA_Mode == MODE_LSMA_:
            slowMAnow = LSMA(open, high, low, close, SlowMA_Period, SlowPriceMode, bar)
            slowMAprevious = LSMA(open, high, low, close, SlowMA_Period, SlowPriceMode, bar + 1)
        else:
            if CopyBuffer(SlMA_Handle, 0, bar, 2, MA) <= 0:
                return 0
            slowMAnow = MA[0]
            slowMAprevious = MA[1]
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if fastMAnow > slowMAnow and fastMAprevious < slowMAprevious:
            if bar == 1 and (not flagval1):
                flagval1 = True
                flagval2 = False
            BuyBuffer[bar] = low[bar] - (Range * 0.75)
        if fastMAnow < slowMAnow and fastMAprevious > slowMAprevious:
            if (bar == 1) & (not flagval2):
                flagval2 = True
                flagval1 = False
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
        if EmailON:
            SendMail('BUY signal alert', 'BUY signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
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
        if EmailON:
            SendMail('SELL signal alert', 'SELL signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
    return rates_total

def LSMA(Open, High, Low, Close, Rperiod, prMode, shift):
    i = 0
    sum_ = 0.0
    pr = 0.0
    length = 0
    lengthvar = 0.0
    tmp = 0.0
    wt = 0.0
    length = Rperiod
    sum_ = 0.0
    i = length
    for i in range(i, 1 - 1, -1):
        lengthvar = length + 1
        lengthvar = lengthvar / 3
        tmp = 0.0
        _sw1 = prMode
        if _sw1 == PRICE_CLOSE:
            pr = Close[length - i + shift]
        elif _sw1 == PRICE_OPEN:
            pr = Open[length - i + shift]
        elif _sw1 == PRICE_HIGH:
            pr = High[length - i + shift]
        elif _sw1 == PRICE_LOW:
            pr = Low[length - i + shift]
        elif _sw1 == PRICE_MEDIAN:
            pr = (High[length - i + shift] + Low[length - i + shift]) / 2
        elif _sw1 == PRICE_TYPICAL:
            pr = (High[length - i + shift] + Low[length - i + shift] + Close[length - i + shift]) / 3
        elif _sw1 == PRICE_WEIGHTED:
            pr = (High[length - i + shift] + Low[length - i + shift] + Close[length - i + shift] + Close[length - i + shift]) / 4
        tmp = (i - lengthvar) * pr
        sum_ += tmp
    else:
        i = _range_end(i, 1 - 1, -1)
    wt = _fdiv(sum_ * 6, length * (length + 1))
    return wt


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MaCrossoverAlert(_MQL5Indicator):
    name = 'ma-crossover_alert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastMA_Mode': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'LSMA'}, default=1),  # Smoothing method for fast moving
        'FastMA_Period': 5,  # Period of averaging for fast moving
        'FastPriceMode': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price for fast moving
        'SlowMA_Mode': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'LSMA'}, default=1),  # Smoothing method for slow moving
        'SlowMA_Period': 20,  # Period of averaging for slow moving
        'SlowPriceMode': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price for slow moving
        'NumberofAlerts': 2,
    }

