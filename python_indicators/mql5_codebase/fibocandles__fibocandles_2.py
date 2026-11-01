"""fibocandles_ — converted from MQL5: MQL5 Indicators/FiboCandles/fibocandles_.mq5

Fibo Candles 2
Copyright: Copyright © 2010, Ivan Kornilov; Link: excelf@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Ivan Kornilov', 'link': 'excelf@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [8421376, 16711935]}, 'widths': {}, 'styles': {}, 'labels': {1: 'FiboCandles Open; FiboCandles High; FiboCandles Low; FiboCandles Close'}, 'levels': [], 'description': ['Fibo Candles 2'], 'name': 'fibocandles_', 'source': 'MQL5 Indicators/FiboCandles/fibocandles_.mq5', 'folder': 'FiboCandles', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 10, 'label': 'Indicator period', 'sinput': False}, {'mql': 'fiboLevel', 'py': 'fiboLevel', 'param': 'fiboLevel', 'type': 'int', 'default': 1, 'label': 'Fibo level value', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 0, 'label': 'Signal bar index, 0 is a current bar', 'sinput': False}, {'mql': 'alert_mode', 'py': 'alert_mode', 'param': 'alert_mode', 'type': 'int', 'default': 0, 'label': 'Actuation indication version', 'sinput': False}, {'mql': 'AlertCount', 'py': 'AlertCount', 'param': 'AlertCount', 'type': 'uint', 'default': 0, 'label': 'Number of submitted alerts', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_FIBORATIO
LEVEL_1_ = 1
LEVEL_2_ = 2
LEVEL_3_ = 3
LEVEL_4_ = 4
LEVEL_5_ = 5
_enum('ENUM_FIBORATIO', {1: 'LEVEL_1_', 2: 'LEVEL_2_', 3: 'LEVEL_3_', 4: 'LEVEL_4_', 5: 'LEVEL_5_'})

# enum ENUM_ALERT_MODE
OnlySound = 0
OnlyAlert = 1
_enum('ENUM_ALERT_MODE', {0: 'OnlySound', 1: 'OnlyAlert'})

# ---- inputs and global variables
period = _input('period', 10)  # Indicator period
fiboLevel = _input('fiboLevel', LEVEL_1_)  # Fibo level value
SignalBar = _input('SignalBar', 0)  # Signal bar index, 0 is a current bar
alert_mode = _input('alert_mode', OnlySound)  # Actuation indication version
AlertCount = _input('AlertCount', 0)  # Number of submitted alerts
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
level = 0.0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global level, min_rates_total
    min_rates_total = period
    _sw1 = fiboLevel
    if _sw1 == 1:
        level = 0.236
    elif _sw1 == 2:
        level = 0.382
    elif _sw1 == 3:
        level = 0.5
    elif _sw1 == 4:
        level = 0.618
    elif _sw1 == 5:
        level = 0.762
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Fibo Candles 2'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_buycount, _s_OnCalculate_sellcount, _s_OnCalculate_trend_
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    trend = 0
    maxHigh = 0.0
    minLow = 0.0
    range_ = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        _s_OnCalculate_trend_ = 0
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    if rates_total != prev_calculated and AlertCount:
        _s_OnCalculate_buycount = AlertCount
        _s_OnCalculate_sellcount = AlertCount
    trend = _s_OnCalculate_trend_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            _s_OnCalculate_trend_ = trend
        maxHigh = high[ArrayMaximum(high, bar, period)]
        minLow = low[ArrayMinimum(low, bar, period)]
        range_ = maxHigh - minLow
        if open[bar] > close[bar]:
            if not (trend < 0 and (range_ * level) < (close[bar] - minLow)):
                trend = 1
            else:
                trend = -1
        else:
            if not (trend > 0 and (range_ * level) < (maxHigh - close[bar])):
                trend = -1
            else:
                trend = 1
        if trend == 1:
            ExtOpenBuffer[bar] = MathMax(open[bar], close[bar])
            ExtCloseBuffer[bar] = MathMin(open[bar], close[bar])
        if trend == -1:
            ExtOpenBuffer[bar] = MathMin(open[bar], close[bar])
            ExtCloseBuffer[bar] = MathMax(open[bar], close[bar])
        ExtHighBuffer[bar] = high[bar]
        ExtLowBuffer[bar] = low[bar]
        if ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 1.0
        else:
            ExtColorBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if (ExtColorBuffer[SignalBar + 1] == 0 and ExtColorBuffer[SignalBar] == 1) and _s_OnCalculate_buycount:
        if alert_mode == OnlyAlert:
            Alert('FiboCandles: Signal for buying by ', Symbol(), GetStringTimeframe(Period()))
        if alert_mode == OnlySound:
            PlaySound('alert.wav')
        _s_OnCalculate_buycount -= 1
    if (ExtColorBuffer[SignalBar + 1] == 1 and ExtColorBuffer[SignalBar] == 0) and _s_OnCalculate_sellcount:
        if alert_mode == OnlyAlert:
            Alert('FiboCandles: Signal for selling by ', Symbol(), GetStringTimeframe(Period()))
        if alert_mode == OnlySound:
            PlaySound('alert.wav')
        _s_OnCalculate_sellcount -= 1
    return rates_total

# ---- static local variables
_s_OnCalculate_trend_ = 0
_s_OnCalculate_buycount = 0
_s_OnCalculate_sellcount = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Fibocandles(_MQL5Indicator):
    name = 'fibocandles_'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 10,  # Indicator period
        'fiboLevel': _Choice({1: '0.236', 2: '0.382', 3: '0.500', 4: '0.618', 5: '0.762'}, default=1),  # Fibo level value
        'SignalBar': 0,  # Signal bar index, 0 is a current bar
        'alert_mode': _Choice({0: 'only sound', 1: 'only alert'}, default=0),  # Actuation indication version
        'AlertCount': 0,  # Number of submitted alerts
    }

