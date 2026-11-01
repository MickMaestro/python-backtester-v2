"""oscillatorcandles — converted from MQL5: MQL5 Indicators/Oscillator Candles/oscillatorcandles.mq5

Oscillator Candles by pipPod
Copyright: Copyright 2015, MetaQuotes Software Corp.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2015, MetaQuotes Software Corp.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [3329330, 2237106]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Oscillator Candles by pipPod'], 'name': 'oscillatorcandles', 'source': 'MQL5 Indicators/Oscillator Candles/oscillatorcandles.mq5', 'folder': 'Oscillator Candles', 'inputs': [{'mql': 'Indicator', 'py': 'Indicator', 'param': 'Indicator', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'MACD', 'py': 'MACD', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'FastEMA', 'py': 'FastEMA', 'param': 'FastEMA', 'type': 'ushort', 'default': 12, 'label': 'Fast EMA Period', 'sinput': False}, {'mql': 'SlowEMA', 'py': 'SlowEMA', 'param': 'SlowEMA', 'type': 'ushort', 'default': 26, 'label': 'Slow EMA Period', 'sinput': False}, {'mql': 'Stochastic', 'py': 'Stochastic', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'Kperiod', 'py': 'Kperiod', 'param': 'Kperiod', 'type': 'ushort', 'default': 7, 'label': 'K Period', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'ushort', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'PriceField', 'py': 'PriceField', 'param': 'PriceField', 'type': 'int', 'default': 0, 'label': 'Price Field', 'sinput': False}, {'mql': 'RSI', 'py': 'RSI', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'ushort', 'default': 14, 'label': 'RSI Period', 'sinput': False}, {'mql': 'CCI', 'py': 'CCI', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'CCIPeriod', 'py': 'CCIPeriod', 'param': 'CCIPeriod', 'type': 'ushort', 'default': 14, 'label': 'CCI Period', 'sinput': False}, {'mql': 'Momentum', 'py': 'Momentum', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'MomPeriod', 'py': 'MomPeriod', 'param': 'MomPeriod', 'type': 'ushort', 'default': 14, 'label': 'Momentum Period', 'sinput': False}, {'mql': '_', 'py': '_', 'param': None, 'type': 'string', 'default': '', 'label': '---', 'sinput': False}, {'mql': 'PriceLine', 'py': 'PriceLine', 'param': 'PriceLine', 'type': 'bool', 'default': True, 'label': 'Horizontal Value Line', 'sinput': False}, {'mql': 'AutoColor', 'py': 'AutoColor', 'param': 'AutoColor', 'type': 'bool', 'default': False, 'label': 'Auto Color Candles', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum indicators
INDICATOR_MACD = 0
INDICATOR_STOCHASTIC = 1
INDICATOR_RSI = 2
INDICATOR_CCI = 3
INDICATOR_MOMENTUM = 4
_enum('indicators', {0: 'INDICATOR_MACD', 1: 'INDICATOR_STOCHASTIC', 2: 'INDICATOR_RSI', 3: 'INDICATOR_CCI', 4: 'INDICATOR_MOMENTUM'})

# ---- inputs and global variables
indicator_level1 = 0.0
indicator_level2 = 20.0
indicator_level3 = 30.0
indicator_level4 = 50.0
indicator_level5 = 70.0
indicator_level6 = 80.0
indicator_level7 = 100.0
indicator_level8 = -100.0
Indicator = _input('Indicator', INDICATOR_MACD)
MACD = _input('MACD', "")
FastEMA = _input('FastEMA', 12)  # Fast EMA Period
SlowEMA = _input('SlowEMA', 26)  # Slow EMA Period
Stochastic = _input('Stochastic', "")
Kperiod = _input('Kperiod', 7)  # K Period
Slowing = _input('Slowing', 3)
PriceField = _input('PriceField', STO_LOWHIGH)  # Price Field
RSI = _input('RSI', "")
RSIPeriod = _input('RSIPeriod', 14)  # RSI Period
CCI = _input('CCI', "")
CCIPeriod = _input('CCIPeriod', 14)  # CCI Period
Momentum = _input('Momentum', "")
MomPeriod = _input('MomPeriod', 14)  # Momentum Period
_ = _input('_', "")  # ---
PriceLine = _input('PriceLine', True)  # Horizontal Value Line
AutoColor = _input('AutoColor', False)  # Auto Color Candles
OpenBuffer = Arr(0, 0.0)
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)
CloseBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
HighesBuffer = Arr(0, 0.0)
LowestBuffer = Arr(0, 0.0)
PriceBuffer = Arr(0, 0.0)
MovAvBuffer = Arr(0, 0.0)
window = 0

def OnInit():
    global window
    shortName = ""
    _sw1 = Indicator
    if _sw1 == INDICATOR_MACD:
        shortName = StringFormat('MACD(%d,%d)', FastEMA, SlowEMA)
        IndicatorSetInteger(INDICATOR_DIGITS, Digits())
        IndicatorSetInteger(INDICATOR_LEVELS, 1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, indicator_level1)
        PlotIndexSetString(0, PLOT_LABEL, 'MACD Open;MACD High;MACD Low;MACD Close')
        for i in range(0, 5):
            PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, SlowEMA - 1)
    elif _sw1 == INDICATOR_STOCHASTIC:
        shortName = StringFormat('Stochastic(%d,%d)', Kperiod, Slowing)
        SetIndexBuffer(5, HighesBuffer, INDICATOR_CALCULATIONS)
        SetIndexBuffer(6, LowestBuffer, INDICATOR_CALCULATIONS)
        IndicatorSetInteger(INDICATOR_DIGITS, 0)
        IndicatorSetInteger(INDICATOR_LEVELS, 3)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, indicator_level2)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, indicator_level4)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, indicator_level6)
        PlotIndexSetString(0, PLOT_LABEL, 'Stoch Open;Stoch High;Stoch Low;Stoch Close')
        for i in range(0, 5):
            PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, Kperiod - 1 + Slowing - 1)
    elif _sw1 == INDICATOR_RSI:
        shortName = StringFormat('RSI(%d)', RSIPeriod)
        IndicatorSetInteger(INDICATOR_DIGITS, 0)
        IndicatorSetInteger(INDICATOR_LEVELS, 3)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, indicator_level3)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, indicator_level4)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, indicator_level5)
        PlotIndexSetString(0, PLOT_LABEL, 'RSI Open;RSI High;RSI Low;RSI Close')
        for i in range(0, 5):
            PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, RSIPeriod - 1)
    elif _sw1 == INDICATOR_CCI:
        shortName = StringFormat('CCI(%d)', CCIPeriod)
        SetIndexBuffer(5, PriceBuffer, INDICATOR_CALCULATIONS)
        SetIndexBuffer(6, MovAvBuffer, INDICATOR_CALCULATIONS)
        IndicatorSetInteger(INDICATOR_DIGITS, 0)
        IndicatorSetInteger(INDICATOR_LEVELS, 3)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, indicator_level1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, indicator_level7)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, indicator_level8)
        PlotIndexSetString(0, PLOT_LABEL, 'CCI Open;CCI High;CCI Low;CCI Close')
        for i in range(0, 5):
            PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, CCIPeriod - 1)
    elif _sw1 == INDICATOR_MOMENTUM:
        shortName = StringFormat('Momentum(%d)', MomPeriod)
        IndicatorSetInteger(INDICATOR_DIGITS, 2)
        IndicatorSetInteger(INDICATOR_LEVELS, 1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, indicator_level7)
        PlotIndexSetString(0, PLOT_LABEL, 'Mom Open;Mom High;Mom Low;Mom Close')
        for i in range(0, 5):
            PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, MomPeriod - 1)
    IndicatorSetString(INDICATOR_SHORTNAME, shortName)
    window = _short(ChartWindowFind(chartID, shortName))
    SetIndexBuffer(0, OpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, LowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, CloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ColorBuffer, INDICATOR_COLOR_INDEX)
    if AutoColor:
        SetColors()
    if (not PriceLine) and ObjectFind(chartID, 'priceLine') != -1:
        ObjectDelete(chartID, 'priceLine')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    toFill = rates_total - prev_calculated
    if prev_calculated > 0:
        toFill += 1
    _sw2 = Indicator
    if _sw2 == INDICATOR_MACD:
        if MACD_f(rates_total, prev_calculated, high, low, close) != toFill:
            return 0
    elif _sw2 == INDICATOR_STOCHASTIC:
        if Stochastic_f(rates_total, prev_calculated, high, low, close) != toFill:
            return 0
    elif _sw2 == INDICATOR_RSI:
        if RSI_f(rates_total, prev_calculated, high, low, close) != toFill:
            return 0
    elif _sw2 == INDICATOR_CCI:
        if CCI_f(rates_total, prev_calculated, high, low, close) != toFill:
            return 0
    elif _sw2 == INDICATOR_MOMENTUM:
        if Momentum_f(rates_total, prev_calculated, high, low, close) != toFill:
            return 0
    return rates_total

def MACD_f(rates_total, prev_calculated, high, low, close):
    global _s_MACD_k, _s_MACD_prevCloseFast, _s_MACD_prevCloseSlow
    if (rates_total <= SlowEMA or FastEMA <= 1) or SlowEMA < FastEMA:
        return 0
    begin = 0
    count = 0
    highFast = 0.0
    highSlow = 0.0
    lowFast = 0.0
    lowSlow = 0.0
    closeFast = 0.0
    closeSlow = 0.0
    if prev_calculated == 0:
        for i in range(0, SlowEMA):
            CloseBuffer[i] = 0.0
            LowBuffer[i] = CloseBuffer[i]
            HighBuffer[i] = LowBuffer[i]
            OpenBuffer[i] = HighBuffer[i]
            count += 1
        begin = SlowEMA
    else:
        begin = prev_calculated - 1
    for i in range(begin, rates_total):
        highFast = ExponentialMA(i, FastEMA, _s_MACD_prevCloseFast, high)
        highSlow = ExponentialMA(i, SlowEMA, _s_MACD_prevCloseSlow, high)
        lowFast = ExponentialMA(i, FastEMA, _s_MACD_prevCloseFast, low)
        lowSlow = ExponentialMA(i, SlowEMA, _s_MACD_prevCloseSlow, low)
        closeFast = ExponentialMA(i, FastEMA, _s_MACD_prevCloseFast, close)
        closeSlow = ExponentialMA(i, SlowEMA, _s_MACD_prevCloseSlow, close)
        HighBuffer[i] = highFast - highSlow
        LowBuffer[i] = lowFast - lowSlow
        CloseBuffer[i] = closeFast - closeSlow
        if _s_MACD_k != i:
            _s_MACD_prevCloseFast = closeFast
            _s_MACD_prevCloseSlow = closeSlow
            OpenBuffer[i] = CloseBuffer[i - 1]
            _s_MACD_k = i
        ColorBuffer[i] = (0 if (CloseBuffer[i] > OpenBuffer[i]) else 1)
        if PriceLine:
            PriceLine_f(CloseBuffer[i])
        count += 1
    return count

def Stochastic_f(rates_total, prev_calculated, high, low, close):
    global _s_Stochastic_k
    if rates_total <= (Kperiod + Slowing) or Kperiod <= 1:
        return 0
    begin = 0
    count = 0
    sumLowH = 0.0
    sumLowL = 0.0
    sumLowC = 0.0
    sumHigh = 0.0
    min_ = 0.0
    max_ = 0.0
    begin = Kperiod - 1
    if begin < prev_calculated:
        begin = prev_calculated - 1
    else:
        for i in range(0, begin):
            HighesBuffer[i] = 0.0
            LowestBuffer[i] = HighesBuffer[i]
    for i in range(begin, rates_total):
        min_ = 1000000.0
        max_ = -1000000.0
        for k in range(i - Kperiod + 1, i + 1):
            _sw3 = PriceField
            if _sw3 == STO_LOWHIGH:
                if min_ > low[k]:
                    min_ = low[k]
                if max_ < high[k]:
                    max_ = high[k]
            elif _sw3 == STO_CLOSECLOSE:
                if min_ > close[k]:
                    min_ = close[k]
                if max_ < close[k]:
                    max_ = close[k]
        LowestBuffer[i] = min_
        HighesBuffer[i] = max_
    begin = Kperiod - 1
    if begin < prev_calculated:
        begin = prev_calculated - 1
    else:
        for i in range(0, begin):
            CloseBuffer[i] = 0.0
            LowBuffer[i] = CloseBuffer[i]
            HighBuffer[i] = LowBuffer[i]
            OpenBuffer[i] = HighBuffer[i]
            count += 1
    for i in range(begin, rates_total):
        sumHigh = 0.0
        sumLowC = sumHigh
        sumLowL = sumLowC
        sumLowH = sumLowL
        for k in range(i - Slowing + 1, i + 1):
            sumLowH += high[i] - LowestBuffer[k]
            sumLowL += low[i] - LowestBuffer[k]
            sumLowC += close[k] - LowestBuffer[k]
            sumHigh += HighesBuffer[k] - LowestBuffer[k]
        if _s_Stochastic_k != i:
            OpenBuffer[i] = CloseBuffer[i - 1]
            _s_Stochastic_k = i
        if sumHigh == 0.0:
            CloseBuffer[i] = 50.0
            LowBuffer[i] = CloseBuffer[i]
            HighBuffer[i] = LowBuffer[i]
        else:
            HighBuffer[i] = OpenBuffer[i] + (((_fdiv(sumLowH, sumHigh) * 100) - OpenBuffer[i]) / Slowing)
            LowBuffer[i] = OpenBuffer[i] + (((_fdiv(sumLowL, sumHigh) * 100) - OpenBuffer[i]) / Slowing)
            CloseBuffer[i] = _fdiv(sumLowC, sumHigh) * 100
        ColorBuffer[i] = (0 if (CloseBuffer[i] > OpenBuffer[i]) else 1)
        if PriceLine:
            PriceLine_f(CloseBuffer[i])
        count += 1
    return count

def RSI_f(rates_total, prev_calculated, high, low, close):
    global _s_RSI_k, _s_RSI_prevNegative, _s_RSI_prevPositive
    if rates_total <= RSIPeriod or RSIPeriod <= 1:
        return 0
    begin = 0
    count = 0
    diffC = 0.0
    diffH = 0.0
    diffL = 0.0
    currPositive = 0.0
    currNegative = 0.0
    begin = prev_calculated - 1
    if begin <= RSIPeriod:
        CloseBuffer[0] = 0.0
        LowBuffer[0] = CloseBuffer[0]
        HighBuffer[0] = LowBuffer[0]
        OpenBuffer[0] = HighBuffer[0]
        sumPositive = 0.0
        sumNegative = 0.0
        count += 1
        for i in range(1, RSIPeriod + 1):
            CloseBuffer[i] = 0.0
            LowBuffer[i] = CloseBuffer[i]
            HighBuffer[i] = LowBuffer[i]
            OpenBuffer[i] = HighBuffer[i]
            diffC = close[i] - close[i - 1]
            sumPositive += (diffC if (diffC > 0.0) else 0.0)
            sumNegative += ((-diffC) if (diffC < 0.0) else 0.0)
            count += 1
        currPositive = sumPositive / RSIPeriod
        currNegative = sumNegative / RSIPeriod
        if currNegative != 0.0:
            CloseBuffer[RSIPeriod] = 100.0 - _fdiv(100.0, 1.0 + _fdiv(currPositive, currNegative))
            LowBuffer[RSIPeriod] = CloseBuffer[RSIPeriod]
            HighBuffer[RSIPeriod] = LowBuffer[RSIPeriod]
            OpenBuffer[RSIPeriod] = HighBuffer[RSIPeriod]
        elif currPositive != 0.0:
            CloseBuffer[RSIPeriod] = 100.0
            LowBuffer[RSIPeriod] = CloseBuffer[RSIPeriod]
            HighBuffer[RSIPeriod] = LowBuffer[RSIPeriod]
            OpenBuffer[RSIPeriod] = HighBuffer[RSIPeriod]
        else:
            CloseBuffer[RSIPeriod] = 50.0
            LowBuffer[RSIPeriod] = CloseBuffer[RSIPeriod]
            HighBuffer[RSIPeriod] = LowBuffer[RSIPeriod]
            OpenBuffer[RSIPeriod] = HighBuffer[RSIPeriod]
        _s_RSI_prevPositive = currPositive
        _s_RSI_prevNegative = currNegative
        begin = RSIPeriod + 1
    for i in range(begin, rates_total):
        diffC = close[i] - close[i - 1]
        diffH = (high[i] - close[i - 1]) / RSIPeriod
        diffL = (low[i] - close[i - 1]) / RSIPeriod
        currPositive = ((_s_RSI_prevPositive * (RSIPeriod - 1)) + (diffC if (diffC > 0.0) else 0.0)) / RSIPeriod
        currNegative = ((_s_RSI_prevNegative * (RSIPeriod - 1)) + ((-diffC) if (diffC < 0.0) else 0.0)) / RSIPeriod
        if _s_RSI_prevNegative != 0.0:
            HighBuffer[i] = 100.0 - _fdiv(100.0, 1.0 + _fdiv(_s_RSI_prevPositive + diffH, _s_RSI_prevNegative))
            LowBuffer[i] = 100.0 - _fdiv(100.0, 1.0 + _fdiv(_s_RSI_prevPositive, _s_RSI_prevNegative - diffL))
        elif _s_RSI_prevPositive != 0.0:
            LowBuffer[i] = 100.0
            HighBuffer[i] = LowBuffer[i]
        else:
            LowBuffer[i] = 50.0
            HighBuffer[i] = LowBuffer[i]
        if currNegative != 0.0:
            CloseBuffer[i] = 100.0 - _fdiv(100.0, 1.0 + _fdiv(currPositive, currNegative))
        elif currPositive != 0.0:
            CloseBuffer[i] = 100.0
        else:
            CloseBuffer[i] = 50.0
        if _s_RSI_k != i:
            _s_RSI_prevPositive = currPositive
            _s_RSI_prevNegative = currNegative
            OpenBuffer[i] = CloseBuffer[i - 1]
            _s_RSI_k = i
        ColorBuffer[i] = (0 if (CloseBuffer[i] > OpenBuffer[i]) else 1)
        if PriceLine:
            PriceLine_f(CloseBuffer[i])
        count += 1
    return count

def CCI_f(rates_total, prev_calculated, high, low, close):
    global _s_CCI_m
    if rates_total <= CCIPeriod or CCIPeriod <= 1:
        return 0
    begin = 0
    count = 0
    sum_ = 0.0
    mul = 0.0
    if prev_calculated < 1:
        for i in range(0, CCIPeriod - 1):
            CloseBuffer[i] = 0.0
            LowBuffer[i] = CloseBuffer[i]
            HighBuffer[i] = LowBuffer[i]
            OpenBuffer[i] = HighBuffer[i]
            PriceBuffer[i] = (high[i] + low[i] + close[i]) / 3
            MovAvBuffer[i] = 0.0
            count += 1
    begin = prev_calculated - 1
    if begin < (CCIPeriod - 1):
        begin = CCIPeriod - 1
    for i in range(begin, rates_total):
        PriceBuffer[i] = (high[i] + low[i] + close[i]) / 3
        MovAvBuffer[i] = SimpleMA(i, CCIPeriod, PriceBuffer)
    mul = 0.015 / CCIPeriod
    begin = prev_calculated - 1
    if begin < (CCIPeriod - 1):
        begin = CCIPeriod - 1
    for i in range(begin, rates_total):
        sum_ = 0.0
        k = i - CCIPeriod + 1
        while k <= i:
            sum_ += MathAbs(PriceBuffer[k] - MovAvBuffer[i])
            k += 1
        sum_ *= mul
        if sum_ == 0.0:
            CloseBuffer[i] = 0.0
            LowBuffer[i] = CloseBuffer[i]
            HighBuffer[i] = LowBuffer[i]
        else:
            HighBuffer[i] = _fdiv(high[i] - MovAvBuffer[i], sum_)
            LowBuffer[i] = _fdiv(low[i] - MovAvBuffer[i], sum_)
            CloseBuffer[i] = _fdiv(close[i] - MovAvBuffer[i], sum_)
        if _s_CCI_m != i:
            OpenBuffer[i] = CloseBuffer[i - 1]
            _s_CCI_m = i
        ColorBuffer[i] = (0 if (CloseBuffer[i] > OpenBuffer[i]) else 1)
        if PriceLine:
            PriceLine_f(CloseBuffer[i])
        count += 1
    return count

def Momentum_f(rates_total, prev_calculated, high, low, close):
    global _s_Momentum_closeMomPeriod, _s_Momentum_k
    if rates_total <= MomPeriod or MomPeriod <= 0:
        return 0
    begin = 0
    count = 0
    if prev_calculated <= 0:
        for i in range(0, MomPeriod):
            CloseBuffer[i] = 0.0
            LowBuffer[i] = CloseBuffer[i]
            HighBuffer[i] = LowBuffer[i]
            OpenBuffer[i] = HighBuffer[i]
            count += 1
        begin = MomPeriod
    else:
        begin = prev_calculated - 1
    for i in range(begin, rates_total):
        if _s_Momentum_k != i:
            _s_Momentum_closeMomPeriod = close[i - MomPeriod]
            OpenBuffer[i] = CloseBuffer[i - 1]
            _s_Momentum_k = i
        HighBuffer[i] = _fdiv(high[i] * 100, _s_Momentum_closeMomPeriod)
        LowBuffer[i] = _fdiv(low[i] * 100, _s_Momentum_closeMomPeriod)
        CloseBuffer[i] = _fdiv(close[i] * 100, _s_Momentum_closeMomPeriod)
        ColorBuffer[i] = (0 if (CloseBuffer[i] > OpenBuffer[i]) else 1)
        if PriceLine:
            PriceLine_f(CloseBuffer[i])
        count += 1
    return count

def PriceLine_f(close_price):
    if ObjectFind(chartID, 'priceLine') != -1:
        ObjectDelete(chartID, 'priceLine')
    if not ObjectCreate(chartID, 'priceLine', OBJ_HLINE, window, 0, close_price):
        Print('PriceLine', ': error ', GetLastError())
        return
    ObjectSetInteger(chartID, 'priceLine', OBJPROP_WIDTH, 1)
    ObjectSetInteger(chartID, 'priceLine', OBJPROP_STYLE, STYLE_SOLID)
    ObjectSetInteger(chartID, 'priceLine', OBJPROP_COLOR, clrLightSlateGray)
    ObjectSetInteger(chartID, 'priceLine', OBJPROP_HIDDEN, True)
    ObjectSetInteger(chartID, 'priceLine', OBJPROP_SELECTABLE, False)
    return

def SetColors():
    colorBase = clrNONE
    colorQote = clrNONE
    base = ""
    qote = ""
    Name = Arr.of(['AUD', 'CAD', 'CHF', 'EUR', 'GBP', 'JPY', 'NZD', 'USD', 'XAU'], fill="", dyn=False, size=9)
    Color = Arr.of([clrDarkOrange, clrWhiteSmoke, clrFireBrick, clrRoyalBlue, clrSilver, clrYellow, clrDarkViolet, clrLimeGreen, clrGold], fill=0, dyn=False, size=9)
    base = StringSubstr(Symbol(), 0, 3)
    qote = StringSubstr(Symbol(), 3, 3)
    for i in range(0, 9):
        if base == Name[i]:
            colorBase = Color[i]
        if qote == Name[i]:
            colorQote = Color[i]
    if (not PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, colorBase)) or (not PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, colorQote)):
        return False
    if ChartGetInteger(0, CHART_COLOR_CANDLE_BULL) != colorBase:
        if (not ChartSetInteger(0, CHART_COLOR_CANDLE_BULL, colorBase)) or (not ChartSetInteger(0, CHART_COLOR_CHART_UP, colorBase)):
            return False
    if ChartGetInteger(0, CHART_COLOR_CANDLE_BEAR) != colorQote:
        if (not ChartSetInteger(0, CHART_COLOR_CANDLE_BEAR, colorQote)) or (not ChartSetInteger(0, CHART_COLOR_CHART_DOWN, colorQote)):
            return False
    return True

# ---- global variables initialised from expressions
chartID = ChartID()

# ---- static local variables
_s_MACD_prevCloseFast = 0.0
_s_MACD_prevCloseSlow = 0.0
_s_MACD_k = 0
_s_Stochastic_k = 0
_s_RSI_prevPositive = 0.0
_s_RSI_prevNegative = 0.0
_s_RSI_k = 0
_s_CCI_m = 0
_s_Momentum_closeMomPeriod = 0.0
_s_Momentum_k = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Oscillatorcandles(_MQL5Indicator):
    name = 'oscillatorcandles'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Indicator': _Choice({0: 'Moving Average Convergence/Divergence', 1: 'Stochastic Oscillator', 2: 'Relative Strength Index', 3: 'Commodity Channel Index', 4: 'Momentum Index'}, default=0),
        'FastEMA': 12,  # Fast EMA Period
        'SlowEMA': 26,  # Slow EMA Period
        'Kperiod': 7,  # K Period
        'Slowing': 3,
        'PriceField': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Price Field
        'RSIPeriod': 14,  # RSI Period
        'CCIPeriod': 14,  # CCI Period
        'MomPeriod': 14,  # Momentum Period
        'PriceLine': True,  # Horizontal Value Line
        'AutoColor': False,  # Auto Color Candles
    }

