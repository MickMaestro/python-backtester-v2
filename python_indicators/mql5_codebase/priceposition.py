"""PricePosition — converted from MQL5: MQL5 Indicators/PricePosition/PricePosition.mq5

PricePosition indicator provide the position of price in the point of angle
when the price was rise or down, where the chance to buy or sell.
Copyright: Copyright 2016, Roberto Jacobs (3rjfx); Link: https://www.mql5.com/en/users/3rjfx; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2016, Roberto Jacobs (3rjfx)', 'link': 'https://www.mql5.com/en/users/3rjfx', 'version': '2.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 2}, 'colors': {}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': ['PricePosition indicator provide the position of price in the point of angle', 'when the price was rise or down, where the chance to buy or sell.'], 'name': 'PricePosition', 'source': 'MQL5 Indicators/PricePosition/PricePosition.mq5', 'folder': 'PricePosition', 'inputs': [{'mql': 'corn', 'py': 'corn', 'param': 'corn', 'type': 'int', 'default': 1, 'label': 'Corner Position', 'sinput': False}, {'mql': 'UseAlert', 'py': 'UseAlert', 'param': 'UseAlert', 'type': 'int', 'default': 1, 'label': 'Turn On Alert (Yes) or (No)', 'sinput': False}, {'mql': 'SectionColor', 'py': 'SectionColor', 'param': None, 'type': 'color', 'default': 14822282, 'label': 'Color Section Line', 'sinput': False}, {'mql': 'BuyColor', 'py': 'BuyColor', 'param': None, 'type': 'color', 'default': 16776960, 'label': 'BUY Color', 'sinput': False}, {'mql': 'SellColor', 'py': 'SellColor', 'param': None, 'type': 'color', 'default': 17919, 'label': 'SELL Color', 'sinput': False}, {'mql': 'clrNT', 'py': 'clrNT', 'param': None, 'type': 'color', 'default': 65535, 'label': 'No Trend Color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum YN
Yes = 1
No = 0
_enum('YN', {1: 'Yes', 0: 'No'})

# enum corner
RightHand = 1
LeftHand = 0
_enum('corner', {1: 'RightHand', 0: 'LeftHand'})

# ---- inputs and global variables
corn = _input('corn', RightHand)  # Corner Position
UseAlert = _input('UseAlert', Yes)  # Turn On Alert (Yes) or (No)
SectionColor = _input('SectionColor', clrBlueViolet)  # Color Section Line
BuyColor = _input('BuyColor', clrAqua)  # BUY Color
SellColor = _input('SellColor', clrOrangeRed)  # SELL Color
clrNT = _input('clrNT', clrYellow)  # No Trend Color
angle = Arr(0, 0.0)
signal = Arr(0, 0.0)
media1 = Arr(0, 0.0)
media2 = Arr(0, 0.0)
media1Handle = 0
media2Handle = 0
day = Arr.of(['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], fill="")
short_name = ""
cor = 0
xdis = 0
ydis = 135
clrfont = 0
cal = 0
pal = 0
prc = 0
pdn = 0

def OnInit():
    global cor, media1Handle, media2Handle, short_name, xdis
    SetIndexBuffer(0, angle, INDICATOR_DATA)
    SetIndexBuffer(1, signal, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, media1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, media2, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, SectionColor)
    PlotIndexSetString(0, PLOT_LABEL, 'Turn')
    PlotIndexSetString(1, PLOT_LABEL, None)
    PlotIndexSetString(2, PLOT_LABEL, None)
    PlotIndexSetString(3, PLOT_LABEL, None)
    PlotIndexSetString(4, PLOT_LABEL, None)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, True)
    short_name = 'PricePosition'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    media1Handle = iMA(Symbol(), PERIOD_CURRENT, 26, 0, MODE_SMMA, PRICE_MEDIAN)
    if media1Handle == INVALID_HANDLE:
        printf('Error creating Media1 MA indicator for ', Symbol())
        return INIT_FAILED
    media2Handle = iMA(Symbol(), PERIOD_CURRENT, 20, 0, MODE_SMA, PRICE_MEDIAN)
    if media2Handle == INVALID_HANDLE:
        printf('Error creating Media2 MA indicator for ', Symbol())
        return INIT_FAILED
    cor = (CORNER_RIGHT_UPPER if (corn == 1) else CORNER_LEFT_UPPER)
    xdis = (133 if (corn == 1) else 30)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(ChartID(), 0, -1)
    GlobalVariablesDeleteAll()
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global cal, clrfont, pal, pdn, prc
    i = 0
    limit = 0
    limit = rates_total - prev_calculated
    if prev_calculated > 0:
        limit += 1
    ArraySetAsSeries(angle, True)
    ArraySetAsSeries(signal, True)
    ArraySetAsSeries(media1, True)
    ArraySetAsSeries(media2, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    calculatedM1 = BarsCalculated(media1Handle)
    if calculatedM1 < rates_total:
        Print('Not all data of SMMA 26 is calculated (', calculatedM1, 'bars ). Error', GetLastError())
        return 0
    to_copyM1 = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copyM1 = rates_total
    else:
        to_copyM1 = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copyM1 += 1
    if False:
        return 0
    if CopyBuffer(media1Handle, 0, 0, to_copyM1, media1) <= 0:
        Print('Getting SMMA 26 buffers is failed! Error:', GetLastError())
        return 0
    calculatedM2 = BarsCalculated(media2Handle)
    if calculatedM2 < rates_total:
        Print('Not all data of SMA 20 is calculated (', calculatedM2, 'bars ). Error', GetLastError())
        return 0
    to_copyM2 = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copyM2 = rates_total
    else:
        to_copyM2 = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copyM2 += 1
    if False:
        return 0
    if CopyBuffer(media2Handle, 0, 0, to_copyM2, media2) <= 0:
        Print('Getting SMA 20 buffers is failed! Error:', GetLastError())
        return 0
    i = limit - 1
    for i in range(i, 0 - 1, -1):
        signal[i] = (media1[i] + media2[i]) / 2
    else:
        i = _range_end(i, 0 - 1, -1)
    i = limit - 1
    for i in range(i, 0 - 1, -1):
        if open[i] <= signal[i] and close[i] >= signal[i]:
            angle[i] = low[i]
        elif open[i] >= signal[i] and close[i] <= signal[i]:
            angle[i] = high[i]
        else:
            angle[i] = EMPTY_VALUE
    else:
        i = _range_end(i, 0 - 1, -1)
    priceturn = 0.0
    seek = 0
    s = 0
    while seek < 1:
        if angle[s] != EMPTY_VALUE:
            priceturn = angle[s]
            seek += 1
        s += 1
    if close[0] > priceturn:
        CreateLabel(0, 'AngleDirection', 'BUY', 'Verdana', 28, BuyColor, cor, xdis, ydis)
        CreateLabel(0, 'AngleLevel', 'above ' + DoubleToString(priceturn, Digits()), 'Verdana', 10, BuyColor, cor, xdis, ydis + 45)
        clrfont = BuyColor
        cal = 1
        if cal != pal and UseAlert == 1:
            Alert('*' + short_name + ': ' + Symbol() + ', TF: ', strTF(Period()) + ', @ ' + TimeToString(TimeCurrent(), TIME_DATE | TIME_MINUTES) + ' --- BUY above --- ', DoubleToString(priceturn, Digits()))
            pal = cal
    if close[0] < priceturn:
        CreateLabel(0, 'AngleDirection', 'SELL', 'Verdana', 28, SellColor, cor, xdis, ydis)
        CreateLabel(0, 'AngleLevel', 'below ' + DoubleToString(priceturn, Digits()), 'Verdana', 10, SellColor, cor, xdis, ydis + 45)
        clrfont = SellColor
        cal = -1
        if cal != pal and UseAlert == 1:
            Alert('*' + short_name + ': ' + Symbol() + ', TF: ', strTF(Period()) + ', @ ' + TimeToString(TimeCurrent(), TIME_DATE | TIME_MINUTES) + ' --- SELL below --- ', DoubleToString(priceturn, Digits()))
            pal = cal
    bararw = ''
    barclr = 0
    if close[0] > open[0]:
        bararw = CharToString(241)
        barclr = BuyColor
    elif close[0] < open[0]:
        bararw = CharToString(242)
        barclr = SellColor
    else:
        bararw = CharToString(91)
        barclr = clrNT
    if close[0] > open[0]:
        prc = 1
        if prc != pdn and UseAlert == 1:
            Alert('*' + short_name + ': ' + Symbol() + ', TF: ', strTF(Period()) + ', @ ' + TimeToString(TimeCurrent(), TIME_DATE | TIME_MINUTES) + ' --- Rising --- ')
            pdn = prc
    elif close[0] < open[0]:
        prc = -1
        if prc != pdn and UseAlert == 1:
            Alert('*' + short_name + ': ' + Symbol() + ', TF: ', strTF(Period()) + ', @ ' + TimeToString(TimeCurrent(), TIME_DATE | TIME_MINUTES) + ' --- Down --- ')
            pdn = prc
    else:
        prc = 0
        if prc != pdn and UseAlert == 1:
            Alert('*' + short_name + ': ' + Symbol() + ', TF: ', strTF(Period()) + ', @ ' + TimeToString(TimeCurrent(), TIME_DATE | TIME_MINUTES) + ' --- Wait --- ')
            pdn = prc
    da = (-78 if (corn == 1) else 78)
    aj = (-2 if (corn == 1) else 2)
    CreateLabel(0, 'DIRARROW', bararw, 'Wingdings', 25, barclr, cor, xdis + da, ydis - 45)
    CreateLabel(0, 'DIRARROW', bararw, 'Wingdings', 25, barclr, cor, xdis + da, ydis - 45)
    CreateLabel(0, 'OPEN', 'O: ' + DoubleToString(open[0], Digits()), 'Verdana', 10, barclr, cor, xdis, ydis - 57)
    CreateLabel(0, 'HIGH', 'H: ' + DoubleToString(high[0], Digits()), 'Verdana', 10, barclr, cor, xdis, ydis - 44)
    CreateLabel(0, 'LOW', 'L: ' + DoubleToString(low[0], Digits()), 'Verdana', 10, barclr, cor, xdis + aj, ydis - 31)
    CreateLabel(0, 'CLOSE', 'C: ' + DoubleToString(close[0], Digits()), 'Verdana', 10, barclr, cor, xdis, ydis - 18)
    CreateLabel(0, 'txDay', day[TimeDayOfWeek_u(TimeCurrent())], 'Verdana', 14, clrNT, cor, xdis, ydis + 65)
    CreateLabel(0, 'txTime', TimeToString(TimeCurrent(), TIME_SECONDS), 'Verdana', 14, clrNT, cor, xdis, ydis + 87)
    return rates_total

def TimeDayOfWeek_u(date):
    tm = MqlDateTime()
    TimeToStruct(date, tm)
    return tm.day_of_week

def CreateLabel(chart_id, lable_name, label_text, font_model, font_size, label_color, chart_corner, x_cor, y_cor):
    if ObjectFind(chart_id, lable_name) < 0:
        if ObjectCreate(chart_id, lable_name, OBJ_LABEL, 0, 0, 0, 0, 0):
            ObjectSetString(chart_id, lable_name, OBJPROP_TEXT, label_text)
            ObjectSetString(chart_id, lable_name, OBJPROP_FONT, font_model)
            ObjectSetInteger(chart_id, lable_name, OBJPROP_FONTSIZE, font_size)
            ObjectSetInteger(chart_id, lable_name, OBJPROP_COLOR, label_color)
            ObjectSetInteger(chart_id, lable_name, OBJPROP_CORNER, chart_corner)
            ObjectSetInteger(chart_id, lable_name, OBJPROP_XDISTANCE, x_cor)
            ObjectSetInteger(chart_id, lable_name, OBJPROP_YDISTANCE, y_cor)
        else:
            Print('Failed to create the object OBJ_LABEL ', lable_name, ', Error code = ', GetLastError())
    else:
        ObjectSetString(chart_id, lable_name, OBJPROP_TEXT, label_text)
        ObjectSetString(chart_id, lable_name, OBJPROP_FONT, font_model)
        ObjectSetInteger(chart_id, lable_name, OBJPROP_FONTSIZE, font_size)
        ObjectSetInteger(chart_id, lable_name, OBJPROP_COLOR, label_color)
        ObjectSetInteger(chart_id, lable_name, OBJPROP_CORNER, chart_corner)
        ObjectSetInteger(chart_id, lable_name, OBJPROP_XDISTANCE, x_cor)
        ObjectSetInteger(chart_id, lable_name, OBJPROP_YDISTANCE, y_cor)

def strTF(period):
    periodcur = ""
    _sw1 = period
    if _sw1 == PERIOD_M1:
        periodcur = 'M1'
    elif _sw1 == PERIOD_M5:
        periodcur = 'M5'
    elif _sw1 == PERIOD_M15:
        periodcur = 'M15'
    elif _sw1 == PERIOD_M30:
        periodcur = 'M30'
    elif _sw1 == PERIOD_H1:
        periodcur = 'H1'
    elif _sw1 == PERIOD_H4:
        periodcur = 'H4'
    elif _sw1 == PERIOD_D1:
        periodcur = 'D1'
    elif _sw1 == PERIOD_W1:
        periodcur = 'W1'
    elif _sw1 == PERIOD_MN1:
        periodcur = 'MN'
    return periodcur


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PricePosition(_MQL5Indicator):
    name = 'PricePosition'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'corn': _Choice({1: 'RightHand', 0: 'LeftHand'}, default=1),  # Corner Position
        'UseAlert': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Turn On Alert (Yes) or (No)
    }

