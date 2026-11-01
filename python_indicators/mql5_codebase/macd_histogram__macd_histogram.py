"""macd_histogram — converted from MQL5: MQL5 Indicators/MACD_Histogram/macd_histogram.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 3, 4: 5, 5: 5}, 'colors': {1: [16748574], 2: [255], 3: [12632256], 4: [65280], 5: [16711935]}, 'widths': {1: 2, 2: 1, 3: 1, 4: 4, 5: 4}, 'styles': {1: 0, 2: 4, 3: 4}, 'labels': {1: 'MACD', 2: 'Signal Line', 3: 'MACD Histogram', 4: 'Buy', 5: 'Sell'}, 'levels': [], 'description': [], 'name': 'macd_histogram', 'source': 'MQL5 Indicators/MACD_Histogram/macd_histogram.mq5', 'folder': 'MACD_Histogram', 'inputs': [{'mql': 'Fast_MA', 'py': 'Fast_MA', 'param': 'Fast_MA', 'type': 'int', 'default': 12, 'label': 'Fast MA period', 'sinput': False}, {'mql': 'Slow_MA', 'py': 'Slow_MA', 'param': 'Slow_MA', 'type': 'int', 'default': 26, 'label': 'SMMA smoothing depth', 'sinput': False}, {'mql': 'MA_Method_', 'py': 'MA_Method_', 'param': 'MA_Method_', 'type': 'int', 'default': 1, 'label': 'Indicator smoothing method', 'sinput': False}, {'mql': 'Signal_SMA', 'py': 'Signal_SMA', 'param': 'Signal_SMA', 'type': 'int', 'default': 9, 'label': 'Signal line period', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'drawIndicatorTrendLines', 'py': 'drawIndicatorTrendLines', 'param': 'drawIndicatorTrendLines', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'drawPriceTrendLines', 'py': 'drawPriceTrendLines', 'param': 'drawPriceTrendLines', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'displayAlert', 'py': 'displayAlert', 'param': 'displayAlert', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'BulliDiverColor', 'py': 'BulliDiverColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'BearDiverColor', 'py': 'BearDiverColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

Lime = 0x00FF00  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
Fast_MA = _input('Fast_MA', 12)  # Fast MA period
Slow_MA = _input('Slow_MA', 26)  # SMMA smoothing depth
MA_Method_ = _input('MA_Method_', MODE_EMA)  # Indicator smoothing method
Signal_SMA = _input('Signal_SMA', 9)  # Signal line period
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE_)  # Price constant
drawIndicatorTrendLines = _input('drawIndicatorTrendLines', True)
drawPriceTrendLines = _input('drawPriceTrendLines', True)
displayAlert = _input('displayAlert', True)
lastAlerttime = 0
indicatorName = ""
start = 0
macd_start = 0
MACDLineBuffer = Arr(0, 0.0)
SignalLineBuffer = Arr(0, 0.0)
HistogramBuffer = Arr(0, 0.0)
bullishDivergence = Arr(0, 0.0)
bearishDivergence = Arr(0, 0.0)

def OnInit():
    global macd_start, start
    if MA_Method_ != MODE_EMA:
        macd_start = MathMax(Fast_MA, Slow_MA)
    start = macd_start + Signal_SMA + 1
    SetIndexBuffer(0, MACDLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, macd_start)
    PlotIndexSetString(0, PLOT_LABEL, 'MACD')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(MACDLineBuffer, True)
    SetIndexBuffer(1, SignalLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, start)
    PlotIndexSetString(1, PLOT_LABEL, 'Signal MA')
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(SignalLineBuffer, True)
    SetIndexBuffer(2, HistogramBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, start)
    PlotIndexSetString(2, PLOT_LABEL, 'Signal MA')
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(HistogramBuffer, True)
    SetIndexBuffer(3, bullishDivergence, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, start)
    PlotIndexSetString(3, PLOT_LABEL, 'Buy')
    PlotIndexSetInteger(3, PLOT_ARROW, 233)
    ArraySetAsSeries(bullishDivergence, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(4, bearishDivergence, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, start)
    PlotIndexSetString(4, PLOT_LABEL, 'Sell')
    PlotIndexSetInteger(4, PLOT_ARROW, 234)
    ArraySetAsSeries(bearishDivergence, True)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    StringConcatenate(_GlobRef(globals(), 'indicatorName'), 'MACD( ', Fast_MA, ', ', Slow_MA, ', ', Signal_SMA, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, indicatorName)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnDeinit(reason):
    Name = ""
    for obj in range(ObjectsTotal(0, -1, -1) - 1, 0 - 1, -1):
        Name = ObjectName(0, obj, -1, -1)
        if StringSubstr(Name, 0, 21) == 'MACD_DivergenceLine.0':
            ObjectDelete(0, Name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < start:
        return 0
    MaxBar1 = 0
    MaxBar2 = 0
    MaxBar3 = 0
    limit1 = 0
    limit2 = 0
    limit3 = 0
    bar = 0
    price_ = 0.0
    fast_ma = 0.0
    slow_ma = 0.0
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit1 = rates_total - 1
        limit2 = limit1 - macd_start - 1
        limit3 = limit1 - start - start
    else:
        limit1 = rates_total - prev_calculated
        limit2 = limit1
        limit3 = limit1
    MaxBar1 = rates_total - 1
    MaxBar2 = MaxBar1 - macd_start
    MaxBar3 = MaxBar1 - start
    bar = limit1
    for bar in range(bar, 0 - 1, -1):
        price_ = PriceSeries(AppliedPrice, bar, open, low, high, close)
        fast_ma = _s_OnCalculate_MA1.MASeries(MaxBar1, prev_calculated, rates_total, Fast_MA, MA_Method_, price_, bar, True)
        slow_ma = _s_OnCalculate_MA2.MASeries(MaxBar1, prev_calculated, rates_total, Slow_MA, MA_Method_, price_, bar, True)
        MACDLineBuffer[bar] = fast_ma - slow_ma
        SignalLineBuffer[bar] = _s_OnCalculate_MA3.SMASeries(MaxBar2, prev_calculated, rates_total, Signal_SMA, MACDLineBuffer[bar], bar, True)
        if bar > MaxBar3:
            HistogramBuffer[bar] = 0.0
        else:
            HistogramBuffer[bar] = MACDLineBuffer[bar] - SignalLineBuffer[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit3 + 2
    for bar in range(bar, 0 - 1, -1):
        bullishDivergence[bar] = EMPTY_VALUE
        bearishDivergence[bar] = EMPTY_VALUE
        CatchBullishDivergence(low, time, MaxBar3, bar)
        CatchBearishDivergence(high, time, MaxBar3, bar)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def CatchBullishDivergence(low, time, rates_total_, shift):
    if IsIndicatorTrough(shift) == False:
        return
    currentTrough = shift
    lastTrough = GetIndicatorLastTrough(shift, rates_total_)
    if lastTrough == -1:
        return
    if MACDLineBuffer[currentTrough] > MACDLineBuffer[lastTrough] and low[currentTrough] < low[lastTrough]:
        bullishDivergence[currentTrough] = MACDLineBuffer[currentTrough] - 0.0001
        if drawPriceTrendLines == True:
            DrawPriceTrendLine(time[currentTrough], time[lastTrough], low[currentTrough], low[lastTrough], BulliDiverColor, STYLE_SOLID)
        if drawIndicatorTrendLines == True:
            DrawIndicatorTrendLine(time[currentTrough], time[lastTrough], MACDLineBuffer[currentTrough], MACDLineBuffer[lastTrough], BulliDiverColor, STYLE_SOLID)
        if displayAlert == True:
            DisplayAlert(time, 'Classical bullish divergence on: ', currentTrough)
    if MACDLineBuffer[currentTrough] < MACDLineBuffer[lastTrough] and low[currentTrough] > low[lastTrough]:
        bullishDivergence[currentTrough] = MACDLineBuffer[currentTrough] - 0.0001
        if drawPriceTrendLines == True:
            DrawPriceTrendLine(time[currentTrough], time[lastTrough], low[currentTrough], low[lastTrough], BulliDiverColor, STYLE_DOT)
        if drawIndicatorTrendLines == True:
            DrawIndicatorTrendLine(time[currentTrough], time[lastTrough], MACDLineBuffer[currentTrough], MACDLineBuffer[lastTrough], BulliDiverColor, STYLE_DOT)
        if displayAlert == True:
            DisplayAlert(time, 'Reverse bullish divergence on: ', currentTrough)

def CatchBearishDivergence(high, time, rates_total_, shift):
    if IsIndicatorPeak(shift) == False:
        return
    currentPeak = shift
    lastPeak = GetIndicatorLastPeak(shift, rates_total_)
    if lastPeak == -1:
        return
    if MACDLineBuffer[currentPeak] < MACDLineBuffer[lastPeak] and high[currentPeak] > high[lastPeak]:
        bearishDivergence[currentPeak] = MACDLineBuffer[currentPeak] + 0.0001
        if drawPriceTrendLines == True:
            DrawPriceTrendLine(time[currentPeak], time[lastPeak], high[currentPeak], high[lastPeak], BearDiverColor, STYLE_SOLID)
        if drawIndicatorTrendLines == True:
            DrawIndicatorTrendLine(time[currentPeak], time[lastPeak], MACDLineBuffer[currentPeak], MACDLineBuffer[lastPeak], BearDiverColor, STYLE_SOLID)
        if displayAlert == True:
            DisplayAlert(time, 'Classical bearish divergence on: ', currentPeak)
    if MACDLineBuffer[currentPeak] > MACDLineBuffer[lastPeak] and high[currentPeak] < high[lastPeak]:
        bearishDivergence[currentPeak] = MACDLineBuffer[currentPeak] + 0.0001
        if drawPriceTrendLines == True:
            DrawPriceTrendLine(time[currentPeak], time[lastPeak], high[currentPeak], high[lastPeak], BearDiverColor, STYLE_DOT)
        if drawIndicatorTrendLines == True:
            DrawIndicatorTrendLine(time[currentPeak], time[lastPeak], MACDLineBuffer[currentPeak], MACDLineBuffer[lastPeak], BearDiverColor, STYLE_DOT)
        if displayAlert == True:
            DisplayAlert(time, 'Reverse bearish divergence on: ', currentPeak)

def IsIndicatorPeak(shift):
    if shift == 0:
        return False
    if (MACDLineBuffer[shift] >= MACDLineBuffer[shift + 1] and MACDLineBuffer[shift] > MACDLineBuffer[shift + 2]) and MACDLineBuffer[shift] > MACDLineBuffer[shift - 1]:
        return True
    return False

def IsIndicatorTrough(shift):
    if shift == 0:
        return False
    if (MACDLineBuffer[shift] <= MACDLineBuffer[shift + 1] and MACDLineBuffer[shift] < MACDLineBuffer[shift + 2]) and MACDLineBuffer[shift] < MACDLineBuffer[shift - 1]:
        return True
    return False

def GetIndicatorLastPeak(shift, rates_total_):
    for i in range(shift + 5, rates_total_):
        if ((SignalLineBuffer[i] >= SignalLineBuffer[i + 1] and SignalLineBuffer[i] >= SignalLineBuffer[i + 2]) and SignalLineBuffer[i] >= SignalLineBuffer[i - 1]) and SignalLineBuffer[i] >= SignalLineBuffer[i - 2]:
            for j in range(i, rates_total_):
                if ((MACDLineBuffer[j] >= MACDLineBuffer[j + 1] and MACDLineBuffer[j] > MACDLineBuffer[j + 2]) and MACDLineBuffer[j] >= MACDLineBuffer[j - 1]) and MACDLineBuffer[j] > MACDLineBuffer[j - 2]:
                    return j
    return -1

def GetIndicatorLastTrough(shift, rates_total_):
    for i in range(shift + 5, rates_total_):
        if ((SignalLineBuffer[i] <= SignalLineBuffer[i + 1] and SignalLineBuffer[i] <= SignalLineBuffer[i + 2]) and SignalLineBuffer[i] <= SignalLineBuffer[i - 1]) and SignalLineBuffer[i] <= SignalLineBuffer[i - 2]:
            for j in range(i, rates_total_):
                if ((MACDLineBuffer[j] <= MACDLineBuffer[j + 1] and MACDLineBuffer[j] < MACDLineBuffer[j + 2]) and MACDLineBuffer[j] <= MACDLineBuffer[j - 1]) and MACDLineBuffer[j] < MACDLineBuffer[j - 2]:
                    return j
    return -1

def DisplayAlert(time, message, shift):
    global lastAlerttime
    if shift <= 2 and time[shift] != lastAlerttime:
        lastAlerttime = time[shift]
        Alert(message, Symbol(), ' , ', EnumToString(Period(), ''), ' minutes chart')

def DrawPriceTrendLine(x1, x2, y1, y2, lineColor, style):
    label = 'MACD_DivergenceLine.0# ' + DoubleToString(x1, 0)
    if ObjectFind(0, label) == -1:
        ObjectCreate(0, label, OBJ_TREND, 0, x1, y1, x2, y2)
        ObjectSetInteger(0, label, OBJPROP_COLOR, lineColor)
        ObjectSetInteger(0, label, OBJPROP_STYLE, style)
        ObjectSetInteger(0, label, OBJPROP_WIDTH, 1)
        ObjectSetInteger(0, label, OBJPROP_RAY, 0)
        ObjectSetInteger(0, label, OBJPROP_BACK, True)
    else:
        ObjectMove(0, label, 0, x1, y1)
        ObjectMove(0, label, 1, x2, y2)

def DrawIndicatorTrendLine(x1, x2, y1, y2, lineColor, style):
    indicatorWindow = ChartWindowFind(0, indicatorName)
    if indicatorWindow < 0:
        return
    label = 'MACD_DivergenceLine.0$# ' + DoubleToString(x1, 0)
    if ObjectFind(0, label) == -1:
        ObjectCreate(0, label, OBJ_TREND, indicatorWindow, x1, y1, x2, y2)
        ObjectSetInteger(0, label, OBJPROP_COLOR, lineColor)
        ObjectSetInteger(0, label, OBJPROP_STYLE, style)
        ObjectSetInteger(0, label, OBJPROP_WIDTH, 1)
        ObjectSetInteger(0, label, OBJPROP_RAY, 0)
        ObjectSetInteger(0, label, OBJPROP_BACK, True)
    else:
        ObjectMove(0, label, 0, x1, y1)
        ObjectMove(0, label, 1, x2, y2)

# ---- global variables initialised from expressions
BulliDiverColor = _input('BulliDiverColor', _uint(Lime))
BearDiverColor = _input('BearDiverColor', _uint(Red))

# ---- static local variables
_s_OnCalculate_MA1 = CMoving_Average()
_s_OnCalculate_MA2 = CMoving_Average()
_s_OnCalculate_MA3 = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MacdHistogram(_MQL5Indicator):
    name = 'macd_histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Fast_MA': 12,  # Fast MA period
        'Slow_MA': 26,  # SMMA smoothing depth
        'MA_Method_': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Indicator smoothing method
        'Signal_SMA': 9,  # Signal line period
        'AppliedPrice': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'}, default=1),  # Price constant
        'drawIndicatorTrendLines': True,
        'drawPriceTrendLines': True,
        'displayAlert': True,
    }

