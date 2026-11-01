"""SchaffTrendCycle — converted from MQL5: MQL5 Indicators/Schaff Trend Cycle MT5/SchaffTrendCycle.mq5

Schaff Trend Cycle - Cyclical Stochastic over Stochastic over MACD.
Falling below 75 is a sell signal.
Rising above 25 is a buy signal.
Four kinds of alert: arrows, text, sound, email, and push.
Copyright: https://t.me/ForexEaPremium; Link: https://t.me/ForexEaPremium; Version: 1.04

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'https://t.me/ForexEaPremium', 'link': 'https://t.me/ForexEaPremium', 'version': '1.04', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1, 'indicator_minimum': 0.0, 'indicator_maximum': 100.0}, 'types': {1: 1}, 'colors': {1: [13382297]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Schaff Trend Cycle'}, 'levels': [25.0, 75.0], 'description': ['Schaff Trend Cycle - Cyclical Stochastic over Stochastic over MACD.', 'Falling below 75 is a sell signal.', 'Rising above 25 is a buy signal.', 'Four kinds of alert: arrows, text, sound, email, and push.'], 'name': 'SchaffTrendCycle', 'source': 'MQL5 Indicators/Schaff Trend Cycle MT5/SchaffTrendCycle.mq5', 'folder': 'Schaff Trend Cycle MT5', 'inputs': [{'mql': 'MAShort', 'py': 'MAShort', 'param': 'MAShort', 'type': 'int', 'default': 23, 'label': '', 'sinput': False}, {'mql': 'MALong', 'py': 'MALong', 'param': 'MALong', 'type': 'int', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'Cycle', 'py': 'Cycle', 'param': 'Cycle', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'ShowArrows', 'py': 'ShowArrows', 'param': 'ShowArrows', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'UpColor', 'py': 'UpColor', 'param': None, 'type': 'color', 'default': 16711680, 'label': '', 'sinput': False}, {'mql': 'DownColor', 'py': 'DownColor', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'ShowAlerts', 'py': 'ShowAlerts', 'param': 'ShowAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'SoundAlerts', 'py': 'SoundAlerts', 'param': 'SoundAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EmailAlerts', 'py': 'EmailAlerts', 'param': 'EmailAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'PushAlerts', 'py': 'PushAlerts', 'param': 'PushAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAShort = _input('MAShort', 23)
MALong = _input('MALong', 50)
Cycle = _input('Cycle', 10)
ShowArrows = _input('ShowArrows', False)
UpColor = _input('UpColor', clrBlue)
DownColor = _input('DownColor', clrRed)
ShowAlerts = _input('ShowAlerts', False)
SoundAlerts = _input('SoundAlerts', False)
EmailAlerts = _input('EmailAlerts', False)
PushAlerts = _input('PushAlerts', False)
Factor = 0.5
BarsRequired = 0
LastAlert = 315532800
MACD = Arr(0, 0.0)
ST = Arr(0, 0.0)
ST2 = Arr(0, 0.0)
MAShortBuf = Arr(0, 0.0)
MALongBuf = Arr(0, 0.0)

def OnInit():
    global BarsRequired
    IndicatorSetString(INDICATOR_SHORTNAME, 'STC(' + IntegerToString(MAShort) + ',' + IntegerToString(MALong) + ',' + IntegerToString(Cycle) + ')')
    SetIndexBuffer(0, ST2, INDICATOR_DATA)
    SetIndexBuffer(1, ST, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, MACD, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, MALong + (Cycle * 2))
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    BarsRequired = MALong + (Cycle * 2)

def OnDeinit(reason):
    ObjectsDeleteAll(0, 'ST_down_')
    ObjectsDeleteAll(0, 'ST_up_')

def OnCalculate(rates_total, prev_calculated, Time, open, High, Low, close, tick_volume, volume, spread):
    global LastAlert, _s_OnCalculate_st1_pass, _s_OnCalculate_st2_pass
    if rates_total <= BarsRequired:
        return rates_total
    counted_bars = prev_calculated
    LLV = 0.0
    HHV = 0.0
    shift = 0
    n = 1
    i = 0
    myMA = 0
    st1_count = 0
    check_st1 = False
    check_st2 = False
    if counted_bars < BarsRequired:
        i = 0
        for i in range(i, BarsRequired):
            ST2[i] = 0.0
        else:
            i = _range_end(i, BarsRequired, 1)
        i = 0
        for i in range(i, BarsRequired):
            ST[i] = 0.0
        else:
            i = _range_end(i, BarsRequired, 1)
    if counted_bars > 0:
        counted_bars -= 1
    shift = counted_bars - BarsRequired + MALong - 1
    if shift < 0:
        shift = 0
    myMA = iMA(None, 0, MAShort, 0, MODE_EMA, PRICE_CLOSE)
    if CopyBuffer(myMA, 0, 0, rates_total, MAShortBuf) != rates_total:
        return 0
    myMA = iMA(None, 0, MALong, 0, MODE_EMA, PRICE_CLOSE)
    if CopyBuffer(myMA, 0, 0, rates_total, MALongBuf) != rates_total:
        return 0
    while shift < rates_total:
        MACD[shift] = MAShortBuf[shift] - MALongBuf[shift]
        if n >= Cycle:
            check_st1 = True
        else:
            n += 1
        if check_st1:
            i = 0
            for i in range(i, Cycle):
                if i == 0:
                    LLV = MACD[shift - i]
                    HHV = MACD[shift - i]
                else:
                    if LLV > MACD[shift - i]:
                        LLV = MACD[shift - i]
                    if HHV < MACD[shift - i]:
                        HHV = MACD[shift - i]
            else:
                i = _range_end(i, Cycle, 1)
            if (HHV - LLV) != 0:
                ST[shift] = _fdiv(MACD[shift] - LLV, HHV - LLV) * 100
            else:
                ST[shift] = ST[shift - 1]
            if _s_OnCalculate_st1_pass:
                ST[shift] = (Factor * (ST[shift] - ST[shift - 1])) + ST[shift - 1]
            _s_OnCalculate_st1_pass = True
            if st1_count >= Cycle:
                check_st2 = True
            else:
                st1_count += 1
            if check_st2:
                i = 0
                for i in range(i, Cycle):
                    if i == 0:
                        LLV = ST[shift - i]
                        HHV = ST[shift - i]
                    else:
                        if LLV > ST[shift - i]:
                            LLV = ST[shift - i]
                        if HHV < ST[shift - i]:
                            HHV = ST[shift - i]
                else:
                    i = _range_end(i, Cycle, 1)
                if (HHV - LLV) != 0:
                    ST2[shift] = _fdiv(ST[shift] - LLV, HHV - LLV) * 100
                else:
                    ST2[shift] = ST2[shift - 1]
                if _s_OnCalculate_st2_pass:
                    ST2[shift] = (Factor * (ST2[shift] - ST2[shift - 1])) + ST2[shift - 1]
                _s_OnCalculate_st2_pass = True
        if shift > 0:
            if ST2[shift] < 75 and ST2[shift - 1] >= 75:
                if ShowArrows:
                    name = 'ST_down_' + TimeToString(Time[shift])
                    offset = (High[shift] - Low[shift]) / 2
                    ObjectCreate(0, name, OBJ_ARROW, 0, Time[shift], High[shift] + offset + (spread[shift] * Point()))
                    ObjectSetInteger(0, name, OBJPROP_ARROWCODE, 234)
                    ObjectSetInteger(0, name, OBJPROP_COLOR, DownColor)
                    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
                if shift == (rates_total - 2) and LastAlert != Time[rates_total - 1]:
                    if ShowAlerts:
                        Alert('Bearish signal on ' + Symbol() + '.')
                    if SoundAlerts:
                        PlaySound('alert.wav')
                    if EmailAlerts:
                        SendMail('Schaff Trend Cycle Alert', 'Bearish signal on ' + TimeToString(Time[rates_total - 1]) + ' on ' + Symbol() + '.')
                    if PushAlerts:
                        SendNotification('STC Alert: Bearish signal on ' + TimeToString(Time[rates_total - 1]) + ' on ' + Symbol() + '.')
                    LastAlert = Time[rates_total - 1]
            elif ST2[shift] > 25 and ST2[shift - 1] <= 25:
                if ShowArrows:
                    name = 'ST_up_' + TimeToString(Time[shift])
                    offset = (High[shift] - Low[shift]) / 2
                    ObjectCreate(0, name, OBJ_ARROW, 0, Time[shift], Low[shift] - offset)
                    ObjectSetInteger(0, name, OBJPROP_ARROWCODE, 233)
                    ObjectSetInteger(0, name, OBJPROP_COLOR, UpColor)
                    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
                if shift == (rates_total - 2) and LastAlert != Time[rates_total - 1]:
                    if ShowAlerts:
                        Alert('Bullish signal on ' + Symbol() + '.')
                    if SoundAlerts:
                        PlaySound('alert.wav')
                    if EmailAlerts:
                        SendMail('Schaff Trend Cycle Alert', 'Bullish signal on ' + TimeToString(Time[rates_total - 1]) + ' on ' + Symbol() + '.')
                    if PushAlerts:
                        SendNotification('STC Alert: Bullish signal on ' + TimeToString(Time[rates_total - 1]) + ' on ' + Symbol() + '.')
                    LastAlert = Time[rates_total - 1]
        shift += 1
    return rates_total

# ---- static local variables
_s_OnCalculate_st1_pass = False
_s_OnCalculate_st2_pass = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SchaffTrendCycle(_MQL5Indicator):
    name = 'SchaffTrendCycle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAShort': 23,
        'MALong': 50,
        'Cycle': 10,
        'ShowArrows': False,
        'ShowAlerts': False,
        'SoundAlerts': False,
        'EmailAlerts': False,
        'PushAlerts': False,
    }
    y_range = (0.0, 100.0)

