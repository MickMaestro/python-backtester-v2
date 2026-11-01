"""Trend Dashboard Indicator — converted from MQL5: MQL5 Indicators/Trend Dashboard Indicator/Trend Dashboard Indicator.mq5

Trend Dashboard - an indicator that shows simple trade recommendations based on the Stochastic, RSI, and CCI readings.
Alerts on indicator confluence.
Supported timeframes: M1, M5, M15, M30, H1, H4, D1, W1, MN1.
Copyright: Tradingforliving.my.id, 2010-2023; Link: https://Tradingforliving.my.id; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Tradingforliving.my.id, 2010-2023', 'link': 'https://Tradingforliving.my.id', 'version': '1.02', 'window': 'separate', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Trend Dashboard - an indicator that shows simple trade recommendations based on the Stochastic, RSI, and CCI readings.', 'Alerts on indicator confluence.', 'Supported timeframes: M1, M5, M15, M30, H1, H4, D1, W1, MN1.'], 'name': 'Trend Dashboard Indicator', 'source': 'MQL5 Indicators/Trend Dashboard Indicator/Trend Dashboard Indicator.mq5', 'folder': 'Trend Dashboard Indicator', 'inputs': [{'mql': 'CheckCandle', 'py': 'CheckCandle', 'param': 'CheckCandle', 'type': 'int', 'default': 1, 'label': 'CheckCandle: Affects both indications and alerts.', 'sinput': False}, {'mql': 'Stochastic_Settings', 'py': 'Stochastic_Settings', 'param': None, 'type': 'string', 'default': '=== Stochastic Settings ===', 'label': '', 'sinput': False}, {'mql': 'PercentK', 'py': 'PercentK', 'param': 'PercentK', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'PercentD', 'py': 'PercentD', 'param': 'PercentD', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'RSI_Settings', 'py': 'RSI_Settings', 'param': None, 'type': 'string', 'default': '=== RSI Settings ===', 'label': '', 'sinput': False}, {'mql': 'RSIP1', 'py': 'RSIP1', 'param': 'RSIP1', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'RSIP2', 'py': 'RSIP2', 'param': 'RSIP2', 'type': 'int', 'default': 70, 'label': '', 'sinput': False}, {'mql': 'Timeframe_Settings', 'py': 'Timeframe_Settings', 'param': None, 'type': 'string', 'default': '=== Timeframe Settings ===', 'label': '', 'sinput': False}, {'mql': 'Enable_M1', 'py': 'Enable_M1', 'param': 'Enable_M1', 'type': 'bool', 'default': False, 'label': 'Enable M1', 'sinput': False}, {'mql': 'Enable_M5', 'py': 'Enable_M5', 'param': 'Enable_M5', 'type': 'bool', 'default': True, 'label': 'Enable M5', 'sinput': False}, {'mql': 'Enable_M15', 'py': 'Enable_M15', 'param': 'Enable_M15', 'type': 'bool', 'default': True, 'label': 'Enable M15', 'sinput': False}, {'mql': 'Enable_M30', 'py': 'Enable_M30', 'param': 'Enable_M30', 'type': 'bool', 'default': True, 'label': 'Enable M30', 'sinput': False}, {'mql': 'Enable_H1', 'py': 'Enable_H1', 'param': 'Enable_H1', 'type': 'bool', 'default': True, 'label': 'Enable H1', 'sinput': False}, {'mql': 'Enable_H4', 'py': 'Enable_H4', 'param': 'Enable_H4', 'type': 'bool', 'default': True, 'label': 'Enable H4', 'sinput': False}, {'mql': 'Enable_D1', 'py': 'Enable_D1', 'param': 'Enable_D1', 'type': 'bool', 'default': True, 'label': 'Enable D1', 'sinput': False}, {'mql': 'Enable_W1', 'py': 'Enable_W1', 'param': 'Enable_W1', 'type': 'bool', 'default': True, 'label': 'Enable W1', 'sinput': False}, {'mql': 'Enable_MN1', 'py': 'Enable_MN1', 'param': 'Enable_MN1', 'type': 'bool', 'default': False, 'label': 'Enable MN1', 'sinput': False}, {'mql': 'My_Alerts', 'py': 'My_Alerts', 'param': None, 'type': 'string', 'default': '=== Alerts ===', 'label': '', 'sinput': False}, {'mql': 'EnableNativeAlerts', 'py': 'EnableNativeAlerts', 'param': 'EnableNativeAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnableEmailAlerts', 'py': 'EnableEmailAlerts', 'param': 'EnableEmailAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnablePushAlerts', 'py': 'EnablePushAlerts', 'param': 'EnablePushAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'My_Colors', 'py': 'My_Colors', 'param': None, 'type': 'string', 'default': '=== Colors ===', 'label': '', 'sinput': False}, {'mql': 'TFColor', 'py': 'TFColor', 'param': None, 'type': 'color', 'default': 14599344, 'label': 'Timeframe Color', 'sinput': False}, {'mql': 'IndicatorColor', 'py': 'IndicatorColor', 'param': None, 'type': 'color', 'default': 11200750, 'label': 'Indicator Color', 'sinput': False}, {'mql': 'BuyColor', 'py': 'BuyColor', 'param': None, 'type': 'color', 'default': 65280, 'label': 'Buy Color', 'sinput': False}, {'mql': 'SellColor', 'py': 'SellColor', 'param': None, 'type': 'color', 'default': 255, 'label': 'Sell Color', 'sinput': False}, {'mql': 'NeutralColor', 'py': 'NeutralColor', 'param': None, 'type': 'color', 'default': 9234160, 'label': 'Neutral Color', 'sinput': False}, {'mql': 'My_Symbols', 'py': 'My_Symbols', 'param': None, 'type': 'string', 'default': '=== Wingdings Symbols ===', 'label': '', 'sinput': False}, {'mql': 'sBuy', 'py': 'sBuy', 'param': 'sBuy', 'type': 'uchar', 'default': 233, 'label': '', 'sinput': False}, {'mql': 'sSell', 'py': 'sSell', 'param': 'sSell', 'type': 'uchar', 'default': 234, 'label': '', 'sinput': False}, {'mql': 'sWait', 'py': 'sWait', 'param': 'sWait', 'type': 'uchar', 'default': 54, 'label': '', 'sinput': False}, {'mql': 'sCCIAgainstBuy', 'py': 'sCCIAgainstBuy', 'param': 'sCCIAgainstBuy', 'type': 'uchar', 'default': 238, 'label': '', 'sinput': False}, {'mql': 'sCCIAgainstSell', 'py': 'sCCIAgainstSell', 'param': 'sCCIAgainstSell', 'type': 'uchar', 'default': 236, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enum_candle_to_check
Current = 0
Previous = 1
_enum('enum_candle_to_check', {0: 'Current', 1: 'Previous'})

# ---- inputs and global variables
CheckCandle = _input('CheckCandle', Previous)  # CheckCandle: Affects both indications and alerts.
Stochastic_Settings = _input('Stochastic_Settings', '=== Stochastic Settings ===')
PercentK = _input('PercentK', 8)
PercentD = _input('PercentD', 3)
Slowing = _input('Slowing', 3)
RSI_Settings = _input('RSI_Settings', '=== RSI Settings ===')
RSIP1 = _input('RSIP1', 14)
RSIP2 = _input('RSIP2', 70)
Timeframe_Settings = _input('Timeframe_Settings', '=== Timeframe Settings ===')
Enable_M1 = _input('Enable_M1', False)  # Enable M1
Enable_M5 = _input('Enable_M5', True)  # Enable M5
Enable_M15 = _input('Enable_M15', True)  # Enable M15
Enable_M30 = _input('Enable_M30', True)  # Enable M30
Enable_H1 = _input('Enable_H1', True)  # Enable H1
Enable_H4 = _input('Enable_H4', True)  # Enable H4
Enable_D1 = _input('Enable_D1', True)  # Enable D1
Enable_W1 = _input('Enable_W1', True)  # Enable W1
Enable_MN1 = _input('Enable_MN1', False)  # Enable MN1
My_Alerts = _input('My_Alerts', '=== Alerts ===')
EnableNativeAlerts = _input('EnableNativeAlerts', False)
EnableEmailAlerts = _input('EnableEmailAlerts', False)
EnablePushAlerts = _input('EnablePushAlerts', False)
My_Colors = _input('My_Colors', '=== Colors ===')
TFColor = _input('TFColor', clrLightSteelBlue)  # Timeframe Color
IndicatorColor = _input('IndicatorColor', clrPaleGoldenrod)  # Indicator Color
BuyColor = _input('BuyColor', clrLime)  # Buy Color
SellColor = _input('SellColor', clrRed)  # Sell Color
NeutralColor = _input('NeutralColor', clrKhaki)  # Neutral Color
My_Symbols = _input('My_Symbols', '=== Wingdings Symbols ===')
sBuy = _input('sBuy', 233)
sSell = _input('sSell', 234)
sWait = _input('sWait', 54)
sCCIAgainstBuy = _input('sCCIAgainstBuy', 238)
sCCIAgainstSell = _input('sCCIAgainstSell', 236)
IndicatorWindow = -1
ShortName = 'Trend Dashboard'
myStochastic = Arr(9, 0, dyn=False)
myRSI1 = Arr(9, 0, dyn=False)
myRSI2 = Arr(9, 0, dyn=False)
myCCIe = Arr(9, 0, dyn=False)
myCCIt = Arr(9, 0, dyn=False)
Confluence = Arr.of([0, 0, 0, 0, 0, 0, 0, 0, 0], fill=0, dyn=False, size=9)
Confluence_prev = Arr.of([0, 0, 0, 0, 0, 0, 0, 0, 0], fill=0, dyn=False, size=9)
scaleX = 100
scaleY = 20
offsetX = 90
offsetY = 10
fontSize = 8
TF = Arr.of([PERIOD_M1, PERIOD_M5, PERIOD_M15, PERIOD_M30, PERIOD_H1, PERIOD_H4, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
eCCI = Arr.of([14, 14, 14, 6, 6, 6, 6, 5, 4], fill=0)
tCCI = Arr.of([100, 50, 34, 14, 14, 14, 14, 12, 10], fill=0)
signalNameStr = Arr.of(['Stoch', 'RSI', 'Entry CCI', 'Trend CCI'], fill="")

def OnInit():
    IndicatorSetString(INDICATOR_SHORTNAME, ShortName)
    if ((((((((not Enable_M1) and (not Enable_M5)) and (not Enable_M15)) and (not Enable_M30)) and (not Enable_H1)) and (not Enable_H4)) and (not Enable_D1)) and (not Enable_W1)) and (not Enable_MN1):
        return INIT_FAILED
    for x in range(0, 9):
        if not TimeframeCheck(TF[x]):
            continue
        myStochastic[x] = iStochastic(None, TF[x], PercentK, PercentD, Slowing, MODE_SMA, STO_LOWHIGH)
        myRSI1[x] = iRSI(None, TF[x], RSIP1, PRICE_TYPICAL)
        myRSI2[x] = iRSI(None, TF[x], RSIP2, PRICE_TYPICAL)
        myCCIe[x] = iCCI(None, TF[x], eCCI[x], PRICE_TYPICAL)
        myCCIt[x] = iCCI(None, TF[x], tCCI[x], PRICE_TYPICAL)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(ChartID(), IndicatorWindow, OBJ_LABEL)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global IndicatorWindow, _s_OnCalculate_Text_prev
    if IndicatorWindow == -1:
        IndicatorWindow = ChartWindowFind(ChartID(), ShortName)
        x = 0
        x_m = 0
        while x < 9:
            if not TimeframeCheck(TF[x]):
                x += 1
                continue
            for y in range(0, 4):
                suffix = IntegerToString(x) + IntegerToString(y)
                name = 'tPs' + suffix
                ObjectCreate(0, name, OBJ_LABEL, IndicatorWindow, 0, 0)
                ObjectSetText_u(name, StringSubstr(EnumToString(TF[x], 'ENUM_TIMEFRAMES'), 7), fontSize, 'Arial Bold', TFColor)
                ObjectSetInteger(0, name, OBJPROP_CORNER, 0)
                ObjectSetInteger(0, name, OBJPROP_XDISTANCE, (x_m * scaleX) + offsetX)
                ObjectSetInteger(0, name, OBJPROP_YDISTANCE, (y * scaleY) + offsetY)
                ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
                name = 'dI' + suffix
                ObjectCreate(0, name, OBJ_LABEL, IndicatorWindow, 0, 0)
                ObjectSetText_u(name, ' ', 10)
                ObjectSetInteger(0, name, OBJPROP_CORNER, 0)
                ObjectSetInteger(0, name, OBJPROP_XDISTANCE, (x_m * scaleX) + (offsetX + 60))
                ObjectSetInteger(0, name, OBJPROP_YDISTANCE, (y * scaleY) + offsetY)
                ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
                name = 'tI' + suffix
                ObjectCreate(0, name, OBJ_LABEL, IndicatorWindow, 0, 0)
                ObjectSetText_u(name, '    ', 9)
                ObjectSetInteger(0, name, OBJPROP_CORNER, 0)
                ObjectSetInteger(0, name, OBJPROP_XDISTANCE, (x_m * scaleX) + (offsetX + 25))
                ObjectSetInteger(0, name, OBJPROP_YDISTANCE, (y * scaleY) + offsetY)
                ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
            x_m += 1
            x += 1
        for y in range(0, 4):
            name = 'tInd' + IntegerToString(y)
            ObjectCreate(0, name, OBJ_LABEL, IndicatorWindow, 0, 0)
            ObjectSetText_u(name, signalNameStr[y], fontSize, 'Arial Bold', IndicatorColor)
            ObjectSetInteger(0, name, OBJPROP_CORNER, 0)
            ObjectSetInteger(0, name, OBJPROP_XDISTANCE, offsetX - 80)
            ObjectSetInteger(0, name, OBJPROP_YDISTANCE, (y * scaleY) + offsetY)
            ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    for x in range(0, 9):
        if not TimeframeCheck(TF[x]):
            continue
        Confluence[x] = 0
        StochasticBuffer_Main = Arr(0, 0.0)
        StochasticBuffer_Signal = Arr(0, 0.0)
        RSI1 = Arr(0, 0.0)
        RSI2 = Arr(0, 0.0)
        CCI_Entry = Arr(0, 0.0)
        CCI_Trend = Arr(0, 0.0)
        ArraySetAsSeries(StochasticBuffer_Main, True)
        ArraySetAsSeries(StochasticBuffer_Signal, True)
        ArraySetAsSeries(RSI1, True)
        ArraySetAsSeries(RSI2, True)
        ArraySetAsSeries(CCI_Entry, True)
        ArraySetAsSeries(CCI_Trend, True)
        if CopyBuffer(myStochastic[x], 0, 0, 2, StochasticBuffer_Main) != 2:
            return 0
        if CopyBuffer(myStochastic[x], 1, 0, 2, StochasticBuffer_Signal) != 2:
            return 0
        if CopyBuffer(myRSI1[x], 0, 0, 2, RSI1) != 2:
            return 0
        if CopyBuffer(myRSI2[x], 0, 0, 2, RSI2) != 2:
            return 0
        if CopyBuffer(myCCIe[x], 0, 0, 3, CCI_Entry) != 3:
            return 0
        if CopyBuffer(myCCIt[x], 0, 0, 3, CCI_Trend) != 3:
            return 0
        if StochasticBuffer_Main[CheckCandle] > StochasticBuffer_Signal[CheckCandle]:
            ObjectSetText_u('dI' + IntegerToString(x) + '0', CharToString(sBuy), fontSize, 'Wingdings', BuyColor)
            ObjectSetText_u('tI' + IntegerToString(x) + '0', ' BUY', 9, 'Arial Bold', BuyColor)
            Confluence[x] += 1
        elif StochasticBuffer_Signal[CheckCandle] > StochasticBuffer_Main[CheckCandle]:
            ObjectSetText_u('dI' + IntegerToString(x) + '0', CharToString(sSell), fontSize, 'Wingdings', SellColor)
            ObjectSetText_u('tI' + IntegerToString(x) + '0', 'SELL', 9, 'Arial Bold', SellColor)
            Confluence[x] -= 1
        else:
            ObjectSetText_u('dI' + IntegerToString(x) + '0', CharToString(sWait), 10, 'Wingdings', NeutralColor)
            ObjectSetText_u('tI' + IntegerToString(x) + '0', 'WAIT', 9, 'Arial Bold', NeutralColor)
        if RSI1[CheckCandle] > RSI2[CheckCandle]:
            ObjectSetText_u('dI' + IntegerToString(x) + '1', CharToString(sBuy), fontSize, 'Wingdings', BuyColor)
            ObjectSetText_u('tI' + IntegerToString(x) + '1', ' BUY', 9, 'Arial Bold', BuyColor)
            Confluence[x] += 1
        elif RSI1[CheckCandle] < RSI2[CheckCandle]:
            ObjectSetText_u('dI' + IntegerToString(x) + '1', CharToString(sSell), fontSize, 'Wingdings', SellColor)
            ObjectSetText_u('tI' + IntegerToString(x) + '1', 'SELL', 9, 'Arial Bold', SellColor)
            Confluence[x] -= 1
        else:
            ObjectSetText_u('dI' + IntegerToString(x) + '1', CharToString(sWait), fontSize, 'Wingdings', NeutralColor)
            ObjectSetText_u('tI' + IntegerToString(x) + '1', 'WAIT', 9, 'Arial Bold', NeutralColor)
        if CCI_Entry[CheckCandle] > 0:
            if CCI_Entry[CheckCandle] > CCI_Entry[CheckCandle + 1]:
                ObjectSetText_u('dI' + IntegerToString(x) + '2', CharToString(sBuy), fontSize, 'Wingdings', BuyColor)
                ObjectSetText_u('tI' + IntegerToString(x) + '2', ' BUY', 9, 'Arial Bold', BuyColor)
                Confluence[x] += 1
            else:
                ObjectSetText_u('dI' + IntegerToString(x) + '2', CharToString(sCCIAgainstBuy), fontSize, 'Wingdings', SellColor)
                ObjectSetText_u('tI' + IntegerToString(x) + '2', 'SELL', 9, 'Arial Bold', SellColor)
                Confluence[x] -= 1
        elif CCI_Entry[CheckCandle] < 0:
            if CCI_Entry[CheckCandle] < CCI_Entry[CheckCandle + 1]:
                ObjectSetText_u('dI' + IntegerToString(x) + '2', CharToString(sSell), fontSize, 'Wingdings', SellColor)
                ObjectSetText_u('tI' + IntegerToString(x) + '2', 'SELL', 9, 'Arial Bold', SellColor)
                Confluence[x] -= 1
            else:
                ObjectSetText_u('dI' + IntegerToString(x) + '2', CharToString(sCCIAgainstSell), fontSize, 'Wingdings', BuyColor)
                ObjectSetText_u('tI' + IntegerToString(x) + '2', ' BUY', 9, 'Arial Bold', BuyColor)
                Confluence[x] += 1
        else:
            ObjectSetText_u('dI' + IntegerToString(x) + '2', CharToString(sWait), 10, 'Wingdings', NeutralColor)
            ObjectSetText_u('tI' + IntegerToString(x) + '2', 'WAIT', 9, 'Arial Bold', NeutralColor)
        if CCI_Trend[CheckCandle] > 0:
            if CCI_Trend[CheckCandle] > CCI_Trend[CheckCandle + 1]:
                ObjectSetText_u('dI' + IntegerToString(x) + '3', CharToString(sBuy), fontSize, 'Wingdings', BuyColor)
                ObjectSetText_u('tI' + IntegerToString(x) + '3', ' BUY', 9, 'Arial Bold', BuyColor)
                Confluence[x] += 1
            else:
                ObjectSetText_u('dI' + IntegerToString(x) + '3', CharToString(sCCIAgainstBuy), fontSize, 'Wingdings', SellColor)
                ObjectSetText_u('tI' + IntegerToString(x) + '3', 'SELL', 9, 'Arial Bold', SellColor)
                Confluence[x] -= 1
        elif CCI_Trend[CheckCandle] < 0:
            if CCI_Trend[CheckCandle] < CCI_Trend[CheckCandle + 1]:
                ObjectSetText_u('dI' + IntegerToString(x) + '3', CharToString(sSell), fontSize, 'Wingdings', SellColor)
                ObjectSetText_u('tI' + IntegerToString(x) + '3', 'SELL', 9, 'Arial Bold', SellColor)
                Confluence[x] -= 1
            else:
                ObjectSetText_u('dI' + IntegerToString(x) + '3', CharToString(sCCIAgainstSell), fontSize, 'Wingdings', BuyColor)
                ObjectSetText_u('tI' + IntegerToString(x) + '3', ' BUY', 9, 'Arial Bold', BuyColor)
                Confluence[x] += 1
        else:
            ObjectSetText_u('dI' + IntegerToString(x) + '3', CharToString(sWait), 10, 'Wingdings', NeutralColor)
            ObjectSetText_u('tI' + IntegerToString(x) + '3', 'WAIT', 9, 'Arial Bold', NeutralColor)
    if (EnableNativeAlerts or EnableEmailAlerts) or EnablePushAlerts:
        buy_text = 'Buy confluence:'
        sell_text = 'Sell confluence:'
        need_alert = False
        buy = False
        sell = False
        for x in range(0, 9):
            if Confluence[x] == 4:
                if buy:
                    buy_text += ','
                buy_text += ' ' + StringSubstr(EnumToString(TF[x], 'ENUM_TIMEFRAMES'), 7)
                if Confluence_prev[x] != 4:
                    need_alert = True
                buy = True
            elif Confluence[x] == -4:
                if sell:
                    sell_text += ','
                sell_text += ' ' + StringSubstr(EnumToString(TF[x], 'ENUM_TIMEFRAMES'), 7)
                if Confluence_prev[x] != -4:
                    need_alert = True
                sell = True
            Confluence_prev[x] = Confluence[x]
        if need_alert:
            Text = 'TA: ' + Symbol() + ' - '
            if buy:
                Text += buy_text
                if sell:
                    Text += '; '
            if sell:
                Text += sell_text
            if Text != _s_OnCalculate_Text_prev:
                if EnableNativeAlerts:
                    Alert(Text)
                if EnableEmailAlerts:
                    SendMail('TA Alert', Text)
                if EnablePushAlerts:
                    SendNotification(Text)
                _s_OnCalculate_Text_prev = Text
    return rates_total

def ObjectSetText_u(name, text, size, font=None, colour=clrNONE):
    ObjectSetString(0, name, OBJPROP_TEXT, text)
    ObjectSetInteger(0, name, OBJPROP_FONTSIZE, size)
    ObjectSetString(0, name, OBJPROP_FONT, font)
    ObjectSetInteger(0, name, OBJPROP_COLOR, colour)

def TimeframeCheck(tf):
    if tf == PERIOD_M1 and (not Enable_M1):
        return False
    if tf == PERIOD_M5 and (not Enable_M5):
        return False
    if tf == PERIOD_M15 and (not Enable_M15):
        return False
    if tf == PERIOD_M30 and (not Enable_M30):
        return False
    if tf == PERIOD_H1 and (not Enable_H1):
        return False
    if tf == PERIOD_H4 and (not Enable_H4):
        return False
    if tf == PERIOD_D1 and (not Enable_D1):
        return False
    if tf == PERIOD_W1 and (not Enable_W1):
        return False
    if tf == PERIOD_MN1 and (not Enable_MN1):
        return False
    return True

# ---- static local variables
_s_OnCalculate_Text_prev = ''


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendDashboardIndicator(_MQL5Indicator):
    name = 'Trend Dashboard Indicator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CheckCandle': _Choice({0: 'Current', 1: 'Previous'}, default=1),  # CheckCandle: Affects both indications and alerts.
        'PercentK': 8,
        'PercentD': 3,
        'Slowing': 3,
        'RSIP1': 14,
        'RSIP2': 70,
        'Enable_M1': False,  # Enable M1
        'Enable_M5': True,  # Enable M5
        'Enable_M15': True,  # Enable M15
        'Enable_M30': True,  # Enable M30
        'Enable_H1': True,  # Enable H1
        'Enable_H4': True,  # Enable H4
        'Enable_D1': True,  # Enable D1
        'Enable_W1': True,  # Enable W1
        'Enable_MN1': False,  # Enable MN1
        'EnableNativeAlerts': False,
        'EnableEmailAlerts': False,
        'EnablePushAlerts': False,
        'sBuy': 233,
        'sSell': 234,
        'sWait': 54,
        'sCCIAgainstBuy': 238,
        'sCCIAgainstSell': 236,
    }

