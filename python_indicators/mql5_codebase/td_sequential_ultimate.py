"""TD Sequential Ultimate — converted from MQL5: MQL5 Indicators/TD Sequential Ultimate MT5/TD Sequential Ultimate.mq5

Shows setups and countdowns based on Tom DeMark's Sequential method.
TDST support and resistance levels are marked too.
Optional alerts available.
Copyright: https://t.me/ForexEaPremium; Link: https://t.me/ForexEaPremium; Version: 1.03

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'https://t.me/ForexEaPremium', 'link': 'https://t.me/ForexEaPremium', 'version': '1.03', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 5, 2: 5, 3: 0, 4: 0, 5: 0}, 'colors': {1: [255], 2: [32768], 3: [4294967295], 4: [4294967295], 5: [4294967295]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'TDST Resistance', 2: 'TDST Support', 3: 'Setup', 4: 'Countdown', 5: 'Perfection'}, 'levels': [], 'description': ["Shows setups and countdowns based on Tom DeMark's Sequential method.", 'TDST support and resistance levels are marked too.', 'Optional alerts available.'], 'name': 'TD Sequential Ultimate', 'source': 'MQL5 Indicators/TD Sequential Ultimate MT5/TD Sequential Ultimate.mq5', 'folder': 'TD Sequential Ultimate MT5', 'inputs': [{'mql': 'MaxBars', 'py': 'MaxBars', 'param': 'MaxBars', 'type': 'int', 'default': 1000, 'label': 'MaxBars: how many bars to calculate; 0 = all bars.', 'sinput': False}, {'mql': 'BuySetupColor', 'py': 'BuySetupColor', 'param': None, 'type': 'color', 'default': 65280, 'label': '', 'sinput': False}, {'mql': 'SellSetupColor', 'py': 'SellSetupColor', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'CountdownColor', 'py': 'CountdownColor', 'param': None, 'type': 'color', 'default': 42495, 'label': '', 'sinput': False}, {'mql': 'FontFace', 'py': 'FontFace', 'param': None, 'type': 'string', 'default': 'Verdana', 'label': '', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'ArrowWidth', 'py': 'ArrowWidth', 'param': 'ArrowWidth', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'PixelDistance', 'py': 'PixelDistance', 'param': 'PixelDistance', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Prefix', 'py': 'Prefix', 'param': None, 'type': 'string', 'default': 'TDS_', 'label': '', 'sinput': False}, {'mql': 'AlertOnSetup', 'py': 'AlertOnSetup', 'param': 'AlertOnSetup', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'AlertOnPerfecting', 'py': 'AlertOnPerfecting', 'param': 'AlertOnPerfecting', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'AlertOnCountdown13', 'py': 'AlertOnCountdown13', 'param': 'AlertOnCountdown13', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'AlertOnSupportResistance', 'py': 'AlertOnSupportResistance', 'param': 'AlertOnSupportResistance', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'AlertNative', 'py': 'AlertNative', 'param': 'AlertNative', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'AlertEmail', 'py': 'AlertEmail', 'param': 'AlertEmail', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'AlertNotification', 'py': 'AlertNotification', 'param': 'AlertNotification', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_COUNT_TYPE
COUNT_TYPE_BUY_SETUP = 0
COUNT_TYPE_SELL_SETUP = 1
COUNT_TYPE_BUY_COUNTDOWN = 2
COUNT_TYPE_SELL_COUNTDOWN = 3
COUNT_TYPE_BUY_PERFECTION = 4
COUNT_TYPE_SELL_PERFECTION = 5
_enum('ENUM_COUNT_TYPE', {0: 'COUNT_TYPE_BUY_SETUP', 1: 'COUNT_TYPE_SELL_SETUP', 2: 'COUNT_TYPE_BUY_COUNTDOWN', 3: 'COUNT_TYPE_SELL_COUNTDOWN', 4: 'COUNT_TYPE_BUY_PERFECTION', 5: 'COUNT_TYPE_SELL_PERFECTION'})

# enum ENUM_ALERT_TYPE
ALERT_TYPE_SETUP_BUY = 0
ALERT_TYPE_SETUP_SELL = 1
ALERT_TYPE_PERFECTING_BUY = 2
ALERT_TYPE_PERFECTING_SELL = 3
ALERT_TYPE_COUNT13_BUY = 4
ALERT_TYPE_COUNT13_SELL = 5
ALERT_TYPE_SUPPORT = 6
ALERT_TYPE_RESISTANCE = 7
_enum('ENUM_ALERT_TYPE', {0: 'ALERT_TYPE_SETUP_BUY', 1: 'ALERT_TYPE_SETUP_SELL', 2: 'ALERT_TYPE_PERFECTING_BUY', 3: 'ALERT_TYPE_PERFECTING_SELL', 4: 'ALERT_TYPE_COUNT13_BUY', 5: 'ALERT_TYPE_COUNT13_SELL', 6: 'ALERT_TYPE_SUPPORT', 7: 'ALERT_TYPE_RESISTANCE'})

# ---- inputs and global variables
MaxBars = _input('MaxBars', 1000)  # MaxBars: how many bars to calculate; 0 = all bars.
BuySetupColor = _input('BuySetupColor', clrLime)
SellSetupColor = _input('SellSetupColor', clrRed)
CountdownColor = _input('CountdownColor', clrOrange)
FontFace = _input('FontFace', 'Verdana')
FontSize = _input('FontSize', 12)
ArrowWidth = _input('ArrowWidth', 2)
PixelDistance = _input('PixelDistance', 3)
Prefix = _input('Prefix', 'TDS_')
AlertOnSetup = _input('AlertOnSetup', False)
AlertOnPerfecting = _input('AlertOnPerfecting', False)
AlertOnCountdown13 = _input('AlertOnCountdown13', False)
AlertOnSupportResistance = _input('AlertOnSupportResistance', False)
AlertNative = _input('AlertNative', False)
AlertEmail = _input('AlertEmail', False)
AlertNotification = _input('AlertNotification', False)
Resistance = Arr(0, 0.0)
Support = Arr(0, 0.0)
Setup = Arr(0, 0.0)
Countdown = Arr(0, 0.0)
Perfection = Arr(0, 0.0)
FontPixelHeight = 0

def OnInit():
    SetIndexBuffer(0, Resistance, INDICATOR_DATA)
    SetIndexBuffer(1, Support, INDICATOR_DATA)
    SetIndexBuffer(2, Setup, INDICATOR_DATA)
    SetIndexBuffer(3, Countdown, INDICATOR_DATA)
    SetIndexBuffer(4, Perfection, INDICATOR_DATA)
    ArraySetAsSeries(Resistance, True)
    ArraySetAsSeries(Support, True)
    ArraySetAsSeries(Setup, True)
    ArraySetAsSeries(Countdown, True)
    ArraySetAsSeries(Perfection, True)
    PlotIndexSetInteger(0, PLOT_ARROW, 158)
    PlotIndexSetInteger(1, PLOT_ARROW, 158)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    text = '0'
    TextSetFont(FontFace, FontSize * -10)
    w = Box(0)
    TextGetSize(text, w, _GlobRef(globals(), 'FontPixelHeight'))
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, Prefix)

def OnCalculate(rates_total, prev_calculated, Time, open, High, Low, Close, tick_volume, volume, spread):
    global _s_OnCalculate_Countdown_Buy, _s_OnCalculate_Countdown_Buy_8_Close, _s_OnCalculate_Countdown_Sell, _s_OnCalculate_Countdown_Sell_8_Close, _s_OnCalculate_No_More_Countdown_Buy_Until_Next_Buy_Setup, _s_OnCalculate_No_More_Countdown_Sell_Until_Next_Sell_Setup, _s_OnCalculate_Preceding_Close, _s_OnCalculate_Setup_Buy, _s_OnCalculate_Setup_Buy_6_Low, _s_OnCalculate_Setup_Buy_7_Low, _s_OnCalculate_Setup_Buy_First_Candle, _s_OnCalculate_Setup_Buy_Highest_High, _s_OnCalculate_Setup_Buy_Highest_High_Candidate, _s_OnCalculate_Setup_Buy_Needs_Perfecting, _s_OnCalculate_Setup_Buy_Perfected, _s_OnCalculate_Setup_Sell, _s_OnCalculate_Setup_Sell_6_High, _s_OnCalculate_Setup_Sell_7_High, _s_OnCalculate_Setup_Sell_First_Candle, _s_OnCalculate_Setup_Sell_Lowest_Low, _s_OnCalculate_Setup_Sell_Lowest_Low_Candidate, _s_OnCalculate_Setup_Sell_Needs_Perfecting, _s_OnCalculate_Setup_Sell_Perfected, _s_OnCalculate_Use_Preceding_Close
    ArraySetAsSeries(Time, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    if rates_total < 7:
        return 0
    counted_bars = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    if counted_bars < 0:
        return -1
    limit = MathMin(rates_total - 1 - counted_bars, rates_total - 6)
    if limit < 1:
        return prev_calculated
    if prev_calculated == 0:
        _s_OnCalculate_Setup_Buy = 0
        _s_OnCalculate_Setup_Buy_First_Candle = 0
        _s_OnCalculate_Setup_Buy_Highest_High = 0.0
        _s_OnCalculate_Setup_Buy_6_Low = 0.0
        _s_OnCalculate_Setup_Buy_7_Low = 0.0
        _s_OnCalculate_No_More_Countdown_Buy_Until_Next_Buy_Setup = False
        _s_OnCalculate_Setup_Buy_Perfected = False
        _s_OnCalculate_Setup_Buy_Needs_Perfecting = False
        _s_OnCalculate_Countdown_Buy = 0
        _s_OnCalculate_Countdown_Buy_8_Close = 0.0
        _s_OnCalculate_Setup_Sell = 0
        _s_OnCalculate_Setup_Sell_First_Candle = 0
        _s_OnCalculate_Setup_Sell_Lowest_Low = 0.0
        _s_OnCalculate_Setup_Sell_6_High = 0.0
        _s_OnCalculate_Setup_Sell_7_High = 0.0
        _s_OnCalculate_No_More_Countdown_Sell_Until_Next_Sell_Setup = False
        _s_OnCalculate_Setup_Sell_Perfected = False
        _s_OnCalculate_Setup_Sell_Needs_Perfecting = False
        _s_OnCalculate_Countdown_Sell = 0
        _s_OnCalculate_Countdown_Sell_8_Close = 0.0
        ObjectsDeleteAll(0, Prefix)
        for i in range(0, rates_total):
            Setup[i] = 0.0
            Countdown[i] = 0.0
            Perfection[i] = 0.0
            Support[i] = EMPTY_VALUE
            Resistance[i] = EMPTY_VALUE
    limit = MathMin(limit, MaxBars)
    for i in range(limit, 0, -1):
        Setup[i] = 0.0
        Countdown[i] = 0.0
        Perfection[i] = 0.0
        if Resistance[i + 1] != EMPTY_VALUE and Close[i] > Resistance[i + 1]:
            Resistance[i] = EMPTY_VALUE
            if AlertOnSupportResistance:
                DoAlert(i, ALERT_TYPE_RESISTANCE)
        else:
            Resistance[i] = Resistance[i + 1]
        if Support[i + 1] != EMPTY_VALUE and Close[i] < Support[i + 1]:
            Support[i] = EMPTY_VALUE
            if AlertOnSupportResistance:
                DoAlert(i, ALERT_TYPE_SUPPORT)
        else:
            Support[i] = Support[i + 1]
        Resistance[0] = EMPTY_VALUE
        Support[0] = EMPTY_VALUE
        if (Close[i + 1] >= Close[i + 5] and Close[i] < Close[i + 4]) and (_s_OnCalculate_Setup_Buy == 0 or _s_OnCalculate_Setup_Buy == 9):
            _s_OnCalculate_Preceding_Close = Close[i + 1]
            _s_OnCalculate_Use_Preceding_Close = False
            _s_OnCalculate_Setup_Buy = 1
            PutCount(COUNT_TYPE_BUY_SETUP, IntegerToString(_s_OnCalculate_Setup_Buy), Time[i], Low[i])
            _s_OnCalculate_Setup_Buy_First_Candle = Time[i]
            _s_OnCalculate_Setup_Buy_Highest_High_Candidate = High[i]
            Setup[i] = _s_OnCalculate_Setup_Buy
        elif (Close[i] < Close[i + 4] and _s_OnCalculate_Setup_Buy > 0) and _s_OnCalculate_Setup_Buy < 9:
            _s_OnCalculate_Setup_Buy += 1
            Setup[i] = _s_OnCalculate_Setup_Buy
            PutCount(COUNT_TYPE_BUY_SETUP, IntegerToString(_s_OnCalculate_Setup_Buy), Time[i], Low[i])
            if _s_OnCalculate_Setup_Buy_Highest_High_Candidate < High[i]:
                _s_OnCalculate_Setup_Buy_Highest_High_Candidate = High[i]
            if _s_OnCalculate_Setup_Buy == 6:
                _s_OnCalculate_Setup_Buy_6_Low = Low[i]
            if _s_OnCalculate_Setup_Buy == 7:
                _s_OnCalculate_Setup_Buy_7_Low = Low[i]
            if _s_OnCalculate_Setup_Buy == 9:
                if _s_OnCalculate_Countdown_Sell > 0:
                    _s_OnCalculate_Countdown_Sell = 0
                    RemoveCount(COUNT_TYPE_SELL_COUNTDOWN, Time[i], Time)
                _s_OnCalculate_No_More_Countdown_Sell_Until_Next_Sell_Setup = True
                if AlertOnSetup:
                    DoAlert(i, ALERT_TYPE_SETUP_BUY)
                _s_OnCalculate_Setup_Buy_Perfected = False
                _s_OnCalculate_Setup_Buy_Needs_Perfecting = True
                _s_OnCalculate_No_More_Countdown_Buy_Until_Next_Buy_Setup = False
                _s_OnCalculate_Setup_Sell = 0
                if _s_OnCalculate_Preceding_Close > _s_OnCalculate_Setup_Buy_Highest_High_Candidate:
                    _s_OnCalculate_Setup_Buy_Highest_High = _s_OnCalculate_Preceding_Close
                    _s_OnCalculate_Use_Preceding_Close = True
                else:
                    _s_OnCalculate_Setup_Buy_Highest_High = _s_OnCalculate_Setup_Buy_Highest_High_Candidate
                res_count = 9
                if _s_OnCalculate_Use_Preceding_Close:
                    res_count = 10
                for j in range(i, i + res_count):
                    Resistance[j] = _s_OnCalculate_Setup_Buy_Highest_High
                    if High[j] == _s_OnCalculate_Setup_Buy_Highest_High:
                        break
                if Low[i + 1] < _s_OnCalculate_Setup_Buy_6_Low and Low[i + 1] < _s_OnCalculate_Setup_Buy_7_Low:
                    _s_OnCalculate_Setup_Buy_Perfected = True
                    _s_OnCalculate_Setup_Buy_Needs_Perfecting = False
                    Perfection[i + 1] = 1.0
                    PutCount(COUNT_TYPE_BUY_PERFECTION, '233', Time[i + 1], High[i + 1])
                    if AlertOnPerfecting:
                        DoAlert(i + 1, ALERT_TYPE_PERFECTING_BUY)
        elif (Close[i] >= Close[i + 4] and _s_OnCalculate_Setup_Buy != 9) and _s_OnCalculate_Setup_Buy != 0:
            RemoveCount(COUNT_TYPE_BUY_SETUP, _s_OnCalculate_Setup_Buy_First_Candle, Time, _s_OnCalculate_Setup_Buy)
            _s_OnCalculate_Setup_Buy = 0
            _s_OnCalculate_Setup_Buy_First_Candle = 0
            _s_OnCalculate_Setup_Buy_Highest_High_Candidate = 0.0
            _s_OnCalculate_Setup_Buy_Needs_Perfecting = False
            _s_OnCalculate_Setup_Buy_Perfected = False
        if (not _s_OnCalculate_No_More_Countdown_Buy_Until_Next_Buy_Setup) and (_s_OnCalculate_Setup_Buy == 9 or _s_OnCalculate_Countdown_Buy > 0):
            if _s_OnCalculate_Countdown_Buy < 13:
                if Close[i] <= Low[i + 2]:
                    if _s_OnCalculate_Countdown_Buy < 12:
                        _s_OnCalculate_Countdown_Buy += 1
                        if _s_OnCalculate_Countdown_Buy == 8:
                            _s_OnCalculate_Countdown_Buy_8_Close = Close[i]
                        Countdown[i] = _s_OnCalculate_Countdown_Buy
                        PutCount(COUNT_TYPE_BUY_COUNTDOWN, IntegerToString(_s_OnCalculate_Countdown_Buy), Time[i], Low[i])
                    elif Low[i] < _s_OnCalculate_Countdown_Buy_8_Close:
                        _s_OnCalculate_Countdown_Buy += 1
                        Countdown[i] = _s_OnCalculate_Countdown_Buy
                        PutCount(COUNT_TYPE_BUY_COUNTDOWN, IntegerToString(_s_OnCalculate_Countdown_Buy), Time[i], Low[i])
                        if AlertOnCountdown13:
                            DoAlert(i, ALERT_TYPE_COUNT13_BUY)
                        _s_OnCalculate_Countdown_Buy = 0
                        _s_OnCalculate_No_More_Countdown_Buy_Until_Next_Buy_Setup = True
                    else:
                        Countdown[i] = 14.0
                        PutCount(COUNT_TYPE_BUY_COUNTDOWN, '+', Time[i], Low[i])
        if _s_OnCalculate_Countdown_Buy > 0:
            if Low[i] > _s_OnCalculate_Setup_Buy_Highest_High and Close[i + 1] > _s_OnCalculate_Setup_Buy_Highest_High:
                _s_OnCalculate_Countdown_Buy = 0
                RemoveCount(COUNT_TYPE_BUY_COUNTDOWN, Time[i], Time)
                _s_OnCalculate_Setup_Buy = 0
        if (not _s_OnCalculate_Setup_Buy_Perfected) and _s_OnCalculate_Setup_Buy_Needs_Perfecting:
            if Low[i] < _s_OnCalculate_Setup_Buy_6_Low and Low[i] < _s_OnCalculate_Setup_Buy_7_Low:
                _s_OnCalculate_Setup_Buy_Perfected = True
                _s_OnCalculate_Setup_Buy_Needs_Perfecting = False
                Perfection[i] = 1.0
                PutCount(COUNT_TYPE_BUY_PERFECTION, '233', Time[i], High[i])
                if AlertOnPerfecting:
                    DoAlert(i, ALERT_TYPE_PERFECTING_BUY)
        if (Close[i + 1] <= Close[i + 5] and Close[i] > Close[i + 4]) and (_s_OnCalculate_Setup_Sell == 0 or _s_OnCalculate_Setup_Sell == 9):
            _s_OnCalculate_Preceding_Close = Close[i + 1]
            _s_OnCalculate_Use_Preceding_Close = False
            _s_OnCalculate_Setup_Sell = 1
            PutCount(COUNT_TYPE_SELL_SETUP, IntegerToString(_s_OnCalculate_Setup_Sell), Time[i], High[i])
            _s_OnCalculate_Setup_Sell_First_Candle = Time[i]
            _s_OnCalculate_Setup_Sell_Lowest_Low_Candidate = Low[i]
            Setup[i] = -_s_OnCalculate_Setup_Sell
        elif (Close[i] > Close[i + 4] and _s_OnCalculate_Setup_Sell > 0) and _s_OnCalculate_Setup_Sell < 9:
            _s_OnCalculate_Setup_Sell += 1
            Setup[i] = -_s_OnCalculate_Setup_Sell
            PutCount(COUNT_TYPE_SELL_SETUP, IntegerToString(_s_OnCalculate_Setup_Sell), Time[i], High[i])
            if _s_OnCalculate_Setup_Sell_Lowest_Low_Candidate > Low[i]:
                _s_OnCalculate_Setup_Sell_Lowest_Low_Candidate = Low[i]
            if _s_OnCalculate_Setup_Sell == 6:
                _s_OnCalculate_Setup_Sell_6_High = High[i]
            if _s_OnCalculate_Setup_Sell == 7:
                _s_OnCalculate_Setup_Sell_7_High = High[i]
            if _s_OnCalculate_Setup_Sell == 9:
                if _s_OnCalculate_Countdown_Buy > 0:
                    _s_OnCalculate_Countdown_Buy = 0
                    RemoveCount(COUNT_TYPE_BUY_COUNTDOWN, Time[i], Time)
                _s_OnCalculate_No_More_Countdown_Buy_Until_Next_Buy_Setup = True
                if AlertOnSetup:
                    DoAlert(i, ALERT_TYPE_SETUP_SELL)
                _s_OnCalculate_Setup_Sell_Perfected = False
                _s_OnCalculate_Setup_Sell_Needs_Perfecting = True
                _s_OnCalculate_No_More_Countdown_Sell_Until_Next_Sell_Setup = False
                _s_OnCalculate_Setup_Buy = 0
                if _s_OnCalculate_Preceding_Close < _s_OnCalculate_Setup_Sell_Lowest_Low_Candidate:
                    _s_OnCalculate_Setup_Sell_Lowest_Low = _s_OnCalculate_Preceding_Close
                    _s_OnCalculate_Use_Preceding_Close = True
                else:
                    _s_OnCalculate_Setup_Sell_Lowest_Low = _s_OnCalculate_Setup_Sell_Lowest_Low_Candidate
                supp_count = 9
                if _s_OnCalculate_Use_Preceding_Close:
                    supp_count = 10
                for j in range(i, i + supp_count):
                    Support[j] = _s_OnCalculate_Setup_Sell_Lowest_Low
                    if Low[j] == _s_OnCalculate_Setup_Sell_Lowest_Low:
                        break
                if High[i + 1] > _s_OnCalculate_Setup_Sell_6_High and High[i + 1] > _s_OnCalculate_Setup_Sell_7_High:
                    _s_OnCalculate_Setup_Sell_Perfected = True
                    _s_OnCalculate_Setup_Sell_Needs_Perfecting = False
                    Perfection[i + 1] = -1.0
                    PutCount(COUNT_TYPE_SELL_PERFECTION, '234', Time[i + 1], Low[i + 1])
                    if AlertOnPerfecting:
                        DoAlert(i + 1, ALERT_TYPE_PERFECTING_SELL)
        elif (Close[i] <= Close[i + 4] and _s_OnCalculate_Setup_Sell != 9) and _s_OnCalculate_Setup_Sell != 0:
            RemoveCount(COUNT_TYPE_SELL_SETUP, _s_OnCalculate_Setup_Sell_First_Candle, Time, _s_OnCalculate_Setup_Sell)
            _s_OnCalculate_Setup_Sell = 0
            _s_OnCalculate_Setup_Sell_First_Candle = 0
            _s_OnCalculate_Setup_Sell_Lowest_Low_Candidate = 0.0
            _s_OnCalculate_Setup_Sell_Needs_Perfecting = False
            _s_OnCalculate_Setup_Sell_Perfected = False
        if (not _s_OnCalculate_No_More_Countdown_Sell_Until_Next_Sell_Setup) and (_s_OnCalculate_Setup_Sell == 9 or _s_OnCalculate_Countdown_Sell > 0):
            if _s_OnCalculate_Countdown_Sell < 13:
                if Close[i] >= High[i + 2]:
                    if _s_OnCalculate_Countdown_Sell < 12:
                        _s_OnCalculate_Countdown_Sell += 1
                        if _s_OnCalculate_Countdown_Sell == 8:
                            _s_OnCalculate_Countdown_Sell_8_Close = Close[i]
                        Countdown[i] = -_s_OnCalculate_Countdown_Sell
                        PutCount(COUNT_TYPE_SELL_COUNTDOWN, IntegerToString(_s_OnCalculate_Countdown_Sell), Time[i], High[i])
                    elif High[i] > _s_OnCalculate_Countdown_Sell_8_Close:
                        _s_OnCalculate_Countdown_Sell += 1
                        Countdown[i] = -_s_OnCalculate_Countdown_Sell
                        PutCount(COUNT_TYPE_SELL_COUNTDOWN, IntegerToString(_s_OnCalculate_Countdown_Sell), Time[i], High[i])
                        if AlertOnCountdown13:
                            DoAlert(i, ALERT_TYPE_COUNT13_SELL)
                        _s_OnCalculate_Countdown_Sell = 0
                        _s_OnCalculate_No_More_Countdown_Sell_Until_Next_Sell_Setup = True
                    else:
                        Countdown[i] = -14.0
                        PutCount(COUNT_TYPE_SELL_COUNTDOWN, '+', Time[i], High[i])
        if _s_OnCalculate_Countdown_Sell > 0:
            if High[i] < _s_OnCalculate_Setup_Sell_Lowest_Low and Close[i + 1] < _s_OnCalculate_Setup_Sell_Lowest_Low:
                _s_OnCalculate_Countdown_Sell = 0
                RemoveCount(COUNT_TYPE_SELL_COUNTDOWN, Time[i], Time)
                _s_OnCalculate_Setup_Sell = 0
        if (not _s_OnCalculate_Setup_Sell_Perfected) and _s_OnCalculate_Setup_Sell_Needs_Perfecting:
            if High[i] > _s_OnCalculate_Setup_Sell_6_High and High[i] > _s_OnCalculate_Setup_Sell_7_High:
                _s_OnCalculate_Setup_Sell_Perfected = True
                _s_OnCalculate_Setup_Sell_Needs_Perfecting = False
                Perfection[i] = -1.0
                PutCount(COUNT_TYPE_SELL_PERFECTION, '234', Time[i], Low[i])
                if AlertOnPerfecting:
                    DoAlert(i, ALERT_TYPE_PERFECTING_SELL)
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ == CHARTEVENT_CHART_CHANGE:
        RedrawVisibleLabels()

def PutCount(count_type, s, time, price):
    name = Prefix
    colour = clrNONE
    level = 0
    object_type = OBJ_TEXT
    adjust_for_height = False
    _sw1 = count_type
    if _sw1 == COUNT_TYPE_BUY_SETUP:
        name += 'BS'
        colour = BuySetupColor
        level = 1
    elif _sw1 == COUNT_TYPE_SELL_SETUP:
        name += 'SS'
        colour = SellSetupColor
        level = -1
        adjust_for_height = True
    elif _sw1 == COUNT_TYPE_BUY_COUNTDOWN:
        name += 'BC'
        colour = CountdownColor
        level = 2
    elif _sw1 == COUNT_TYPE_SELL_COUNTDOWN:
        name += 'SC'
        colour = CountdownColor
        level = -2
        adjust_for_height = True
    elif _sw1 == COUNT_TYPE_BUY_PERFECTION:
        name += 'BP'
        colour = BuySetupColor
        level = 3
        object_type = OBJ_ARROW
    elif _sw1 == COUNT_TYPE_SELL_PERFECTION:
        name += 'SP'
        colour = SellSetupColor
        level = -3
        object_type = OBJ_ARROW
        adjust_for_height = True
    name += IntegerToString(_int(time))
    ObjectCreate(0, name, object_type, 0, time, price)
    ObjectSetInteger(0, name, OBJPROP_COLOR, colour)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, name, OBJPROP_HIDDEN, False)
    if count_type == COUNT_TYPE_BUY_PERFECTION or count_type == COUNT_TYPE_SELL_PERFECTION:
        ObjectSetInteger(0, name, OBJPROP_ARROWCODE, StringToInteger(s))
        ObjectSetInteger(0, name, OBJPROP_WIDTH, ArrowWidth)
    else:
        ObjectSetInteger(0, name, OBJPROP_FONTSIZE, FontSize)
        ObjectSetString(0, name, OBJPROP_FONT, FontFace)
        ObjectSetString(0, name, OBJPROP_TEXT, s)
        ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_UPPER)
    RedrawOneWickLabel(name, time, price, level)

def RedrawOneWickLabel(name, time, price, level):
    x = Box(0)
    y = Box(0)
    cw = Box(0)
    t = Box(0)
    p = Box(0.0)
    p_0 = Box(0.0)
    if ObjectFind(0, name) == -1:
        return
    distance = 0
    if level < 0:
        distance = (level * _int(FontPixelHeight)) + (level * PixelDistance)
    else:
        distance = ((level - 1) * _int(FontPixelHeight)) + (level * PixelDistance)
    ChartTimePriceToXY(0, 0, time, price, x, y)
    ChartXYToTimePrice(0, x.v, y.v + distance, cw, t, p)
    if (y.v + distance) < 0:
        ChartXYToTimePrice(0, x.v, 0, cw, t, p_0)
        p.v = p_0.v + (p_0.v - p.v)
    ObjectSetDouble(0, name, OBJPROP_PRICE, p.v)

def RedrawVisibleLabels():
    visible_bars = _int(ChartGetInteger(0, CHART_VISIBLE_BARS))
    first_bar = _int(ChartGetInteger(0, CHART_FIRST_VISIBLE_BAR))
    last_bar = first_bar - visible_bars + 1
    for i in range(first_bar, last_bar - 1, -1):
        time = iTime(Symbol(), Period(), i)
        low = iLow(Symbol(), Period(), i)
        high = iHigh(Symbol(), Period(), i)
        time_string = IntegerToString(_int(time))
        RedrawOneWickLabel(Prefix + 'BS' + time_string, time, low, 1)
        RedrawOneWickLabel(Prefix + 'SS' + time_string, time, high, -1)
        RedrawOneWickLabel(Prefix + 'BC' + time_string, time, low, 2)
        RedrawOneWickLabel(Prefix + 'SC' + time_string, time, high, -2)
        RedrawOneWickLabel(Prefix + 'BP' + time_string, time, low, 3)
        RedrawOneWickLabel(Prefix + 'SP' + time_string, time, high, -3)
    ChartRedraw()

def RemoveCount(count_type, begin, Time, n=0):
    name_start = Prefix
    if count_type == COUNT_TYPE_BUY_SETUP:
        name_start += 'BS'
    elif count_type == COUNT_TYPE_SELL_SETUP:
        name_start += 'SS'
    elif count_type == COUNT_TYPE_BUY_COUNTDOWN:
        name_start += 'BC'
    elif count_type == COUNT_TYPE_SELL_COUNTDOWN:
        name_start += 'SC'
    begin_candle = iBarShift(Symbol(), Period(), begin, True)
    if begin_candle == -1:
        return
    if count_type == COUNT_TYPE_BUY_SETUP or count_type == COUNT_TYPE_SELL_SETUP:
        for i in range(begin_candle, begin_candle - n, -1):
            name = name_start + IntegerToString(Time[i])
            ObjectDelete(0, name)
    elif count_type == COUNT_TYPE_BUY_COUNTDOWN or count_type == COUNT_TYPE_SELL_COUNTDOWN:
        i = begin_candle
        while i < Bars(Symbol(), Period()):
            name = name_start + IntegerToString(Time[i])
            if ObjectGetString(ChartID(), name, OBJPROP_TEXT) == '1':
                ObjectDelete(0, name)
                return
            ObjectDelete(0, name)
            i += 1

def DoAlert(i, alert_type):
    if i > 2:
        return
    main_text = 'Sequential: ' + Symbol() + ' @ ' + EnumToString(Period(), 'ENUM_TIMEFRAMES')
    email_subject = main_text
    _sw2 = alert_type
    if _sw2 == ALERT_TYPE_SETUP_BUY:
        main_text += ' Buy Setup completed by ' + TimeToString(iTime(Symbol(), Period(), i)) + ' candle.'
        email_subject += ' Buy Setup'
    elif _sw2 == ALERT_TYPE_SETUP_SELL:
        main_text += ' Sell Setup completed by ' + TimeToString(iTime(Symbol(), Period(), i)) + ' candle.'
        email_subject += ' Sell Setup'
    elif _sw2 == ALERT_TYPE_PERFECTING_BUY:
        main_text += ' Buy Setup Perfected by ' + TimeToString(iTime(Symbol(), Period(), i)) + ' candle.'
        email_subject += ' Buy Perfecting'
    elif _sw2 == ALERT_TYPE_PERFECTING_SELL:
        main_text += ' Sell Setup Perfected by ' + TimeToString(iTime(Symbol(), Period(), i)) + ' candle.'
        email_subject += ' Sell Perfecting'
    elif _sw2 == ALERT_TYPE_COUNT13_BUY:
        main_text += ' Buy Countdown completed by ' + TimeToString(iTime(Symbol(), Period(), i)) + ' candle.'
        email_subject += ' Buy Countdown'
    elif _sw2 == ALERT_TYPE_COUNT13_SELL:
        main_text += ' Sell Countdown completed by ' + TimeToString(iTime(Symbol(), Period(), i)) + ' candle.'
        email_subject += ' Sell Countdown'
    elif _sw2 == ALERT_TYPE_RESISTANCE:
        main_text += ' TDST Resistance broken by ' + TimeToString(iTime(Symbol(), Period(), i)) + ' candle.'
        email_subject += ' Buy TDST Resistance'
    elif _sw2 == ALERT_TYPE_SUPPORT:
        main_text += ' TDST Support broken by ' + TimeToString(iTime(Symbol(), Period(), i)) + ' candle.'
        email_subject += ' TDST Support'
    if AlertNative:
        Alert(main_text)
    if AlertEmail:
        SendMail(email_subject, main_text)
    if AlertNotification:
        SendNotification(main_text)

# ---- static local variables
_s_OnCalculate_Preceding_Close = 0.0
_s_OnCalculate_Use_Preceding_Close = False
_s_OnCalculate_Setup_Buy = 0
_s_OnCalculate_Setup_Buy_First_Candle = 0
_s_OnCalculate_Setup_Buy_Highest_High = 0.0
_s_OnCalculate_Setup_Buy_Highest_High_Candidate = 0.0
_s_OnCalculate_Setup_Buy_6_Low = 0.0
_s_OnCalculate_Setup_Buy_7_Low = 0.0
_s_OnCalculate_No_More_Countdown_Buy_Until_Next_Buy_Setup = False
_s_OnCalculate_Setup_Buy_Perfected = False
_s_OnCalculate_Setup_Buy_Needs_Perfecting = False
_s_OnCalculate_Countdown_Buy = 0
_s_OnCalculate_Countdown_Buy_8_Close = 0.0
_s_OnCalculate_Setup_Sell = 0
_s_OnCalculate_Setup_Sell_First_Candle = 0
_s_OnCalculate_Setup_Sell_Lowest_Low = 0.0
_s_OnCalculate_Setup_Sell_Lowest_Low_Candidate = 0.0
_s_OnCalculate_Setup_Sell_6_High = 0.0
_s_OnCalculate_Setup_Sell_7_High = 0.0
_s_OnCalculate_No_More_Countdown_Sell_Until_Next_Sell_Setup = False
_s_OnCalculate_Setup_Sell_Perfected = False
_s_OnCalculate_Setup_Sell_Needs_Perfecting = False
_s_OnCalculate_Countdown_Sell = 0
_s_OnCalculate_Countdown_Sell_8_Close = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TDSequentialUltimate(_MQL5Indicator):
    name = 'TD Sequential Ultimate'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'MaxBars': 1000,  # MaxBars: how many bars to calculate; 0 = all bars.
        'FontSize': 12,
        'ArrowWidth': 2,
        'PixelDistance': 3,
        'AlertOnSetup': False,
        'AlertOnPerfecting': False,
        'AlertOnCountdown13': False,
        'AlertOnSupportResistance': False,
        'AlertNative': False,
        'AlertEmail': False,
        'AlertNotification': False,
    }

