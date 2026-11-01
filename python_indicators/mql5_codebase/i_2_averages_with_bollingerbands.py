"""2_Averages_with_BollingerBands — converted from MQL5: MQL5 Indicators/2 Moving Averages with Bollinger Bands/2_Averages_with_BollingerBands.mq5

mkbokul@gmail.com
2 Moving Averages With Bollinger Bands
This Indicator will be work in all time frame
WARNING: Use this software at your own risk.
The creator of this script cannot be held responsible for any damage or loss. 
Copyright: Copyright 2025, Mir Mostof Kamal; Link: https://www.mql5.com/en/users/bokul; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2025, Mir Mostof Kamal', 'link': 'https://www.mql5.com/en/users/bokul', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 7}, 'types': {1: 1, 2: 1, 3: 5, 4: 5, 5: 1, 6: 1, 7: 1}, 'colors': {1: [16711680], 2: [255], 3: [65280], 4: [17919], 5: [65535], 6: [65535], 7: [65535]}, 'widths': {3: 2, 4: 2}, 'styles': {}, 'labels': {1: 'MA1', 2: 'MA2', 3: 'Buy Signal', 4: 'Sell Signal', 5: 'BB Upper', 6: 'BB Middle', 7: 'BB Lower'}, 'levels': [], 'description': ['mkbokul@gmail.com', '2 Moving Averages With Bollinger Bands', 'This Indicator will be work in all time frame', 'WARNING: Use this software at your own risk.', 'The creator of this script cannot be held responsible for any damage or loss. '], 'name': '2_Averages_with_BollingerBands', 'source': 'MQL5 Indicators/2 Moving Averages with Bollinger Bands/2_Averages_with_BollingerBands.mq5', 'folder': '2 Moving Averages with Bollinger Bands', 'inputs': [{'mql': 'MA1_Settings', 'py': 'MA1_Settings', 'param': None, 'type': 'string', 'default': '=== MA1 Settings ===', 'label': '', 'sinput': False}, {'mql': 'MA1_Period', 'py': 'MA1_Period', 'param': 'MA1_Period', 'type': 'int', 'default': 7, 'label': '1st MA Period:', 'sinput': False}, {'mql': 'MA1_Method', 'py': 'MA1_Method', 'param': 'MA1_Method', 'type': 'int', 'default': 1, 'label': '1st MA Method:', 'sinput': False}, {'mql': 'MA1_Price', 'py': 'MA1_Price', 'param': 'MA1_Price', 'type': 'int', 'default': 1, 'label': '1st MA Price:', 'sinput': False}, {'mql': 'MA2_Settings', 'py': 'MA2_Settings', 'param': None, 'type': 'string', 'default': '=== MA2 Settings ===', 'label': '', 'sinput': False}, {'mql': 'MA2_Period', 'py': 'MA2_Period', 'param': 'MA2_Period', 'type': 'int', 'default': 21, 'label': '2nd MA Period:', 'sinput': False}, {'mql': 'MA2_Method', 'py': 'MA2_Method', 'param': 'MA2_Method', 'type': 'int', 'default': 0, 'label': '2nd MA Method:', 'sinput': False}, {'mql': 'MA2_Price', 'py': 'MA2_Price', 'param': 'MA2_Price', 'type': 'int', 'default': 1, 'label': '2nd MA Price:', 'sinput': False}, {'mql': 'Alerts_Settings', 'py': 'Alerts_Settings', 'param': None, 'type': 'string', 'default': '=== Alerts Settings ===', 'label': '', 'sinput': False}, {'mql': 'EnableAlerts', 'py': 'EnableAlerts', 'param': 'EnableAlerts', 'type': 'bool', 'default': True, 'label': 'Alerts On/Off:', 'sinput': False}, {'mql': 'EnableSound', 'py': 'EnableSound', 'param': 'EnableSound', 'type': 'bool', 'default': True, 'label': 'Email Alerts On/Off:', 'sinput': False}, {'mql': 'EnableEmail', 'py': 'EnableEmail', 'param': 'EnableEmail', 'type': 'bool', 'default': False, 'label': 'Alerts Sound On/Off:', 'sinput': False}, {'mql': 'BB_Settings', 'py': 'BB_Settings', 'param': None, 'type': 'string', 'default': '--- Bollinger Bands Settings ---', 'label': '', 'sinput': False}, {'mql': 'Enable_BB', 'py': 'Enable_BB', 'param': 'Enable_BB', 'type': 'bool', 'default': True, 'label': 'Enable/Disable BB :', 'sinput': False}, {'mql': 'BB_Period', 'py': 'BB_Period', 'param': 'BB_Period', 'type': 'int', 'default': 60, 'label': 'BB Period :', 'sinput': False}, {'mql': 'BB_Deviation', 'py': 'BB_Deviation', 'param': 'BB_Deviation', 'type': 'double', 'default': 2.0, 'label': 'BB Deviation:', 'sinput': False}, {'mql': 'BB_Shift', 'py': 'BB_Shift', 'param': 'BB_Shift', 'type': 'int', 'default': 0, 'label': 'BB Shift :', 'sinput': False}, {'mql': 'BB_Price', 'py': 'BB_Price', 'param': 'BB_Price', 'type': 'int', 'default': 1, 'label': 'BB Applied Price :', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MA1_Settings = _input('MA1_Settings', '=== MA1 Settings ===')
MA1_Period = _input('MA1_Period', 7)  # 1st MA Period:
MA1_Method = _input('MA1_Method', MODE_EMA)  # 1st MA Method:
MA1_Price = _input('MA1_Price', PRICE_CLOSE)  # 1st MA Price:
MA2_Settings = _input('MA2_Settings', '=== MA2 Settings ===')
MA2_Period = _input('MA2_Period', 21)  # 2nd MA Period:
MA2_Method = _input('MA2_Method', MODE_SMA)  # 2nd MA Method:
MA2_Price = _input('MA2_Price', PRICE_CLOSE)  # 2nd MA Price:
Alerts_Settings = _input('Alerts_Settings', '=== Alerts Settings ===')
EnableAlerts = _input('EnableAlerts', True)  # Alerts On/Off:
EnableSound = _input('EnableSound', True)  # Email Alerts On/Off:
EnableEmail = _input('EnableEmail', False)  # Alerts Sound On/Off:
BB_Settings = _input('BB_Settings', '--- Bollinger Bands Settings ---')
Enable_BB = _input('Enable_BB', True)  # Enable/Disable BB :
BB_Period = _input('BB_Period', 60)  # BB Period :
BB_Deviation = _input('BB_Deviation', 2.0)  # BB Deviation:
BB_Shift = _input('BB_Shift', 0)  # BB Shift :
BB_Price = _input('BB_Price', PRICE_CLOSE)  # BB Applied Price :
MA1_Buffer = Arr(0, 0.0)
MA2_Buffer = Arr(0, 0.0)
BuyArrow = Arr(0, 0.0)
SellArrow = Arr(0, 0.0)
BB_Upper = Arr(0, 0.0)
BB_Middle = Arr(0, 0.0)
BB_Lower = Arr(0, 0.0)
handle_ma1 = 0
handle_ma2 = 0
handle_bb = 0
lastAlertTime = 0

def OnInit():
    global handle_bb, handle_ma1, handle_ma2
    SetIndexBuffer(0, MA1_Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, MA2_Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, BuyArrow, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_ARROW, 233)
    SetIndexBuffer(3, SellArrow, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_ARROW, 234)
    SetIndexBuffer(4, BB_Upper, INDICATOR_DATA)
    SetIndexBuffer(5, BB_Middle, INDICATOR_DATA)
    SetIndexBuffer(6, BB_Lower, INDICATOR_DATA)
    handle_ma1 = iMA(Symbol(), Period(), MA1_Period, 0, MA1_Method, MA1_Price)
    handle_ma2 = iMA(Symbol(), Period(), MA2_Period, 0, MA2_Method, MA2_Price)
    if Enable_BB:
        handle_bb = iBands(Symbol(), Period(), BB_Period, BB_Shift, BB_Deviation, BB_Price)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    global lastAlertTime
    if rates_total < (MathMax(MA1_Period, MA2_Period) + 2):
        return 0
    close = Arr(0, 0.0)
    high = Arr(0, 0.0)
    low = Arr(0, 0.0)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    CopyClose(Symbol(), Period(), 0, rates_total, close)
    CopyHigh(Symbol(), Period(), 0, rates_total, high)
    CopyLow(Symbol(), Period(), 0, rates_total, low)
    CopyBuffer(handle_ma1, 0, 0, rates_total, MA1_Buffer)
    CopyBuffer(handle_ma2, 0, 0, rates_total, MA2_Buffer)
    if Enable_BB:
        CopyBuffer(handle_bb, 1, 0, rates_total, BB_Upper)
        CopyBuffer(handle_bb, 0, 0, rates_total, BB_Middle)
        CopyBuffer(handle_bb, 2, 0, rates_total, BB_Lower)
    for i in range(rates_total - 2, 1 - 1, -1):
        BuyArrow[i] = EMPTY_VALUE
        SellArrow[i] = EMPTY_VALUE
        if MA1_Buffer[i] > MA2_Buffer[i] and MA1_Buffer[i + 1] <= MA2_Buffer[i + 1]:
            BuyArrow[i] = low[i] - (5 * Point())
            if i == 1 and TimeCurrent() != lastAlertTime:
                TriggerAlert('BUY')
                lastAlertTime = TimeCurrent()
        elif MA1_Buffer[i] < MA2_Buffer[i] and MA1_Buffer[i + 1] >= MA2_Buffer[i + 1]:
            SellArrow[i] = high[i] + (5 * Point())
            if i == 1 and TimeCurrent() != lastAlertTime:
                TriggerAlert('SELL')
                lastAlertTime = TimeCurrent()
    return rates_total

def TriggerAlert(type_):
    msg = StringFormat('2MA_BB: %s signal on %s %s at %s', type_, Symbol(), PeriodToStr(Period()), TimeToString(TimeCurrent(), TIME_DATE | TIME_MINUTES))
    if EnableAlerts:
        Alert(msg)
    if EnableSound:
        PlaySound('alert.wav')
    if EnableEmail:
        SendMail('DoubleMA Signal', msg)

def PeriodToStr(tf):
    _sw1 = tf
    if _sw1 == PERIOD_M1:
        return 'M1'
    elif _sw1 == PERIOD_M5:
        return 'M5'
    elif _sw1 == PERIOD_M15:
        return 'M15'
    elif _sw1 == PERIOD_M30:
        return 'M30'
    elif _sw1 == PERIOD_H1:
        return 'H1'
    elif _sw1 == PERIOD_H4:
        return 'H4'
    elif _sw1 == PERIOD_D1:
        return 'D1'
    elif _sw1 == PERIOD_W1:
        return 'W1'
    elif _sw1 == PERIOD_MN1:
        return 'MN1'
    else:
        return IntegerToString(tf)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ind2AveragesWithBollingerBands(_MQL5Indicator):
    name = '2_Averages_with_BollingerBands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'MA1_Period': 7,  # 1st MA Period:
        'MA1_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # 1st MA Method:
        'MA1_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # 1st MA Price:
        'MA2_Period': 21,  # 2nd MA Period:
        'MA2_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # 2nd MA Method:
        'MA2_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # 2nd MA Price:
        'EnableAlerts': True,  # Alerts On/Off:
        'EnableSound': True,  # Email Alerts On/Off:
        'EnableEmail': False,  # Alerts Sound On/Off:
        'Enable_BB': True,  # Enable/Disable BB :
        'BB_Period': 60,  # BB Period :
        'BB_Deviation': 2.0,  # BB Deviation:
        'BB_Shift': 0,  # BB Shift :
        'BB_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # BB Applied Price :
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

