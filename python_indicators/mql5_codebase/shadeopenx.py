"""ShadeOpenX — converted from MQL5: MQL5 Indicators/ShadeOpenX/ShadeOpenX.mq5

Индикатор ночных ссесий в виде свечек.
Copyright: Copyright © 2017, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Индикатор ночных ссесий в виде свечек.'], 'name': 'ShadeOpenX', 'source': 'MQL5 Indicators/ShadeOpenX/ShadeOpenX.mq5', 'folder': 'ShadeOpenX', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'ShadeOpenX', 'label': 'имя графических объектов]', 'sinput': False}, {'mql': 'StartH', 'py': 'StartH', 'param': 'StartH', 'type': 'int', 'default': 6, 'label': 'Старт торговли (Часы)', 'sinput': False}, {'mql': 'StartM', 'py': 'StartM', 'param': 'StartM', 'type': 'int', 'default': 30, 'label': 'Старт торговли (Минуты)', 'sinput': False}, {'mql': 'EndH', 'py': 'EndH', 'param': 'EndH', 'type': 'int', 'default': 13, 'label': 'Окончание торговли (Часы)', 'sinput': False}, {'mql': 'EndM', 'py': 'EndM', 'param': 'EndM', 'type': 'int', 'default': 5, 'label': 'Окончание торговли (Минуты)', 'sinput': False}, {'mql': 'Upbody', 'py': 'Upbody', 'param': None, 'type': 'color', 'default': 3329330, 'label': 'цвет тела свечи Рост', 'sinput': False}, {'mql': 'Dnbody', 'py': 'Dnbody', 'param': None, 'type': 'color', 'default': 36095, 'label': 'цвет тела свечи Падение', 'sinput': False}, {'mql': 'Uphigh', 'py': 'Uphigh', 'param': None, 'type': 'color', 'default': 10025880, 'label': 'цвет верхней тени Рост', 'sinput': False}, {'mql': 'Dnhigh', 'py': 'Dnhigh', 'param': None, 'type': 'color', 'default': 65535, 'label': 'цвет верхней тени Падение', 'sinput': False}, {'mql': 'Uplow', 'py': 'Uplow', 'param': None, 'type': 'color', 'default': 10025880, 'label': 'цвет нижней тени Рост', 'sinput': False}, {'mql': 'Dnlow', 'py': 'Dnlow', 'param': None, 'type': 'color', 'default': 65535, 'label': 'цвет нижней тени Падение', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum HOURS
ENUM_HOUR_0 = 0
ENUM_HOUR_1 = 1
ENUM_HOUR_2 = 2
ENUM_HOUR_3 = 3
ENUM_HOUR_4 = 4
ENUM_HOUR_5 = 5
ENUM_HOUR_6 = 6
ENUM_HOUR_7 = 7
ENUM_HOUR_8 = 8
ENUM_HOUR_9 = 9
ENUM_HOUR_10 = 10
ENUM_HOUR_11 = 11
ENUM_HOUR_12 = 12
ENUM_HOUR_13 = 13
ENUM_HOUR_14 = 14
ENUM_HOUR_15 = 15
ENUM_HOUR_16 = 16
ENUM_HOUR_17 = 17
ENUM_HOUR_18 = 18
ENUM_HOUR_19 = 19
ENUM_HOUR_20 = 20
ENUM_HOUR_21 = 21
ENUM_HOUR_22 = 22
ENUM_HOUR_23 = 23
_enum('HOURS', {0: 'ENUM_HOUR_0', 1: 'ENUM_HOUR_1', 2: 'ENUM_HOUR_2', 3: 'ENUM_HOUR_3', 4: 'ENUM_HOUR_4', 5: 'ENUM_HOUR_5', 6: 'ENUM_HOUR_6', 7: 'ENUM_HOUR_7', 8: 'ENUM_HOUR_8', 9: 'ENUM_HOUR_9', 10: 'ENUM_HOUR_10', 11: 'ENUM_HOUR_11', 12: 'ENUM_HOUR_12', 13: 'ENUM_HOUR_13', 14: 'ENUM_HOUR_14', 15: 'ENUM_HOUR_15', 16: 'ENUM_HOUR_16', 17: 'ENUM_HOUR_17', 18: 'ENUM_HOUR_18', 19: 'ENUM_HOUR_19', 20: 'ENUM_HOUR_20', 21: 'ENUM_HOUR_21', 22: 'ENUM_HOUR_22', 23: 'ENUM_HOUR_23'})

# enum MINUTS
ENUM_MINUT_0 = 0
ENUM_MINUT_1 = 1
ENUM_MINUT_2 = 2
ENUM_MINUT_3 = 3
ENUM_MINUT_4 = 4
ENUM_MINUT_5 = 5
ENUM_MINUT_6 = 6
ENUM_MINUT_7 = 7
ENUM_MINUT_8 = 8
ENUM_MINUT_9 = 9
ENUM_MINUT_10 = 10
ENUM_MINUT_11 = 11
ENUM_MINUT_12 = 12
ENUM_MINUT_13 = 13
ENUM_MINUT_14 = 14
ENUM_MINUT_15 = 15
ENUM_MINUT_16 = 16
ENUM_MINUT_17 = 17
ENUM_MINUT_18 = 18
ENUM_MINUT_19 = 19
ENUM_MINUT_20 = 20
ENUM_MINUT_21 = 21
ENUM_MINUT_22 = 22
ENUM_MINUT_23 = 23
ENUM_MINUT_24 = 24
ENUM_MINUT_25 = 25
ENUM_MINUT_26 = 26
ENUM_MINUT_27 = 27
ENUM_MINUT_28 = 28
ENUM_MINUT_29 = 29
ENUM_MINUT_30 = 30
ENUM_MINUT_31 = 31
ENUM_MINUT_32 = 32
ENUM_MINUT_33 = 33
ENUM_MINUT_34 = 34
ENUM_MINUT_35 = 35
ENUM_MINUT_36 = 36
ENUM_MINUT_37 = 37
ENUM_MINUT_38 = 38
ENUM_MINUT_39 = 39
ENUM_MINUT_40 = 40
ENUM_MINUT_41 = 41
ENUM_MINUT_42 = 42
ENUM_MINUT_43 = 43
ENUM_MINUT_44 = 44
ENUM_MINUT_45 = 45
ENUM_MINUT_46 = 46
ENUM_MINUT_47 = 47
ENUM_MINUT_48 = 48
ENUM_MINUT_49 = 49
ENUM_MINUT_50 = 50
ENUM_MINUT_51 = 51
ENUM_MINUT_52 = 52
ENUM_MINUT_53 = 53
ENUM_MINUT_54 = 54
ENUM_MINUT_55 = 55
ENUM_MINUT_56 = 56
ENUM_MINUT_57 = 57
ENUM_MINUT_58 = 58
ENUM_MINUT_59 = 59
_enum('MINUTS', {0: 'ENUM_MINUT_0', 1: 'ENUM_MINUT_1', 2: 'ENUM_MINUT_2', 3: 'ENUM_MINUT_3', 4: 'ENUM_MINUT_4', 5: 'ENUM_MINUT_5', 6: 'ENUM_MINUT_6', 7: 'ENUM_MINUT_7', 8: 'ENUM_MINUT_8', 9: 'ENUM_MINUT_9', 10: 'ENUM_MINUT_10', 11: 'ENUM_MINUT_11', 12: 'ENUM_MINUT_12', 13: 'ENUM_MINUT_13', 14: 'ENUM_MINUT_14', 15: 'ENUM_MINUT_15', 16: 'ENUM_MINUT_16', 17: 'ENUM_MINUT_17', 18: 'ENUM_MINUT_18', 19: 'ENUM_MINUT_19', 20: 'ENUM_MINUT_20', 21: 'ENUM_MINUT_21', 22: 'ENUM_MINUT_22', 23: 'ENUM_MINUT_23', 24: 'ENUM_MINUT_24', 25: 'ENUM_MINUT_25', 26: 'ENUM_MINUT_26', 27: 'ENUM_MINUT_27', 28: 'ENUM_MINUT_28', 29: 'ENUM_MINUT_29', 30: 'ENUM_MINUT_30', 31: 'ENUM_MINUT_31', 32: 'ENUM_MINUT_32', 33: 'ENUM_MINUT_33', 34: 'ENUM_MINUT_34', 35: 'ENUM_MINUT_35', 36: 'ENUM_MINUT_36', 37: 'ENUM_MINUT_37', 38: 'ENUM_MINUT_38', 39: 'ENUM_MINUT_39', 40: 'ENUM_MINUT_40', 41: 'ENUM_MINUT_41', 42: 'ENUM_MINUT_42', 43: 'ENUM_MINUT_43', 44: 'ENUM_MINUT_44', 45: 'ENUM_MINUT_45', 46: 'ENUM_MINUT_46', 47: 'ENUM_MINUT_47', 48: 'ENUM_MINUT_48', 49: 'ENUM_MINUT_49', 50: 'ENUM_MINUT_50', 51: 'ENUM_MINUT_51', 52: 'ENUM_MINUT_52', 53: 'ENUM_MINUT_53', 54: 'ENUM_MINUT_54', 55: 'ENUM_MINUT_55', 56: 'ENUM_MINUT_56', 57: 'ENUM_MINUT_57', 58: 'ENUM_MINUT_58', 59: 'ENUM_MINUT_59'})

# ---- inputs and global variables
SirName = _input('SirName', 'ShadeOpenX')  # имя графических объектов]
StartH = _input('StartH', ENUM_HOUR_6)  # Старт торговли (Часы)
StartM = _input('StartM', ENUM_MINUT_30)  # Старт торговли (Минуты)
EndH = _input('EndH', ENUM_HOUR_13)  # Окончание торговли (Часы)
EndM = _input('EndM', ENUM_MINUT_5)  # Окончание торговли (Минуты)
Upbody = _input('Upbody', clrLimeGreen)  # цвет тела свечи Рост
Dnbody = _input('Dnbody', clrDarkOrange)  # цвет тела свечи Падение
Uphigh = _input('Uphigh', clrPaleGreen)  # цвет верхней тени Рост
Dnhigh = _input('Dnhigh', clrYellow)  # цвет верхней тени Падение
Uplow = _input('Uplow', clrPaleGreen)  # цвет нижней тени Рост
Dnlow = _input('Dnlow', clrYellow)  # цвет нижней тени Падение
min_rates_total = 0
candlebody = ""
candlehigh = ""
candlelow = ""

def OnInit():
    global candlebody, candlehigh, candlelow, min_rates_total
    if StartH > EndH or (StartH == EndH and StartM >= EndM):
        Print('Неверные значения входных переменных старта и окончания торговли!')
        return INIT_PARAMETERS_INCORRECT
    min_rates_total = 2
    candlebody = SirName + '_candlebody'
    candlehigh = SirName + '_candlehigh'
    candlelow = SirName + '_candlelow'
    IndicatorSetString(INDICATOR_SHORTNAME, 'ShadeOpenX')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, candlebody)
    ObjectDelete(0, candlehigh)
    ObjectDelete(0, candlelow)
    ChartRedraw(None)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    iTime_ = Arr(1, 0, dyn=False)
    if CopyTime(Symbol(), PERIOD_D1, _DT(time[0]), 1, iTime_) <= 0:
        return 0
    limit = 0
    for bar in range(0, rates_total - 1):
        if time[bar] < iTime_[0]:
            break
        limit += 1
    for bar in range(limit, 0 - 1, -1):
        if not ShadeOpenCheck(time[bar]):
            continue
        else:
            Start = GetShadeOpenStart(time[bar])
            End = MathMin(GetShadeOpenEnd(time[bar]), time[0])
            iOpen_ = Arr(1, 0.0, dyn=False)
            iClose_ = Arr(1, 0.0, dyn=False)
            iHigh_ = Arr(0, 0.0)
            iLow_ = Arr(0, 0.0)
            ArraySetAsSeries(iHigh_, True)
            ArraySetAsSeries(iLow_, True)
            if CopyOpen(Symbol(), PERIOD_CURRENT, _DT(Start), 1, iOpen_) <= 0:
                return 0
            if CopyHigh(Symbol(), PERIOD_CURRENT, _DT(Start), _DT(End), iHigh_) <= 0:
                return 0
            if CopyLow(Symbol(), PERIOD_CURRENT, _DT(Start), _DT(End), iLow_) <= 0:
                return 0
            if CopyClose(Symbol(), PERIOD_CURRENT, _DT(End), 1, iClose_) <= 0:
                return 0
            ihigh = iHigh_[ArrayMaximum(iHigh_, 0, WHOLE_ARRAY)]
            ilow = iLow_[ArrayMinimum(iLow_, 0, WHOLE_ARRAY)]
            if iClose_[0] >= iOpen_[0]:
                SetRectangle(0, candlebody, 0, Start, iOpen_[0], End, iClose_[0], Upbody, 0, 0, candlebody)
                SetRectangle(0, candlehigh, 0, Start, iClose_[0], End, ihigh, Uphigh, 0, 0, candlehigh)
                SetRectangle(0, candlelow, 0, Start, iOpen_[0], End, ilow, Uplow, 0, 0, candlelow)
            else:
                SetRectangle(0, candlebody, 0, Start, iOpen_[0], End, iClose_[0], Dnbody, 0, 0, candlebody)
                SetRectangle(0, candlehigh, 0, Start, iOpen_[0], End, ihigh, Dnhigh, 0, 0, candlehigh)
                SetRectangle(0, candlelow, 0, Start, iClose_[0], End, ilow, Dnlow, 0, 0, candlelow)
    ChartRedraw(None)
    return rates_total

def CreateRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_RECTANGLE, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_FILL, True)

def SetRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateRectangle(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)

def ShadeOpenCheck(ChkTime):
    Trade = False
    tm = MqlDateTime()
    TimeToStruct(ChkTime, tm)
    if StartH < EndH:
        if tm.hour == StartH and tm.min >= StartM:
            Trade = True
        if tm.hour > StartH and tm.hour < EndH:
            Trade = True
        if (tm.hour > StartH and tm.hour == EndH) and tm.min < EndM:
            Trade = True
    if StartH == EndH:
        if (tm.hour == StartH and tm.min >= StartM) and tm.min < EndM:
            Trade = True
    return Trade

def GetShadeOpenStart(ChkTime):
    Start = 0
    iTime_ = Arr(1, 0, dyn=False)
    if CopyTime(Symbol(), PERIOD_D1, _DT(ChkTime), 1, iTime_) <= 0:
        return 0
    Start = iTime_[0] + (StartH * 60 * 60) + (StartM * 60)
    return Start

def GetShadeOpenEnd(ChkTime):
    End = 0
    iTime_ = Arr(1, 0, dyn=False)
    if CopyTime(Symbol(), PERIOD_D1, _DT(ChkTime), 1, iTime_) <= 0:
        return 0
    End = iTime_[0] + (EndH * 60 * 60) + (EndM * 60)
    return End

def PlotInit(PlotNumber, DrawBegin, PlotShift):
    PlotIndexSetInteger(PlotNumber, PLOT_DRAW_BEGIN, DrawBegin)
    PlotIndexSetInteger(PlotNumber, PLOT_SHIFT, PlotShift)

def ArrayInit(ArrNumber, Array):
    SetIndexBuffer(ArrNumber, Array, INDICATOR_DATA)
    ArraySetAsSeries(Array, True)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ShadeOpenX(_MQL5Indicator):
    name = 'ShadeOpenX'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'StartH': _Choice({0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23'}, default=6),  # Старт торговли (Часы)
        'StartM': _Choice({0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23', 24: '24', 25: '25', 26: '26', 27: '27', 28: '28', 29: '29', 30: '30', 31: '31', 32: '32', 33: '33', 34: '34', 35: '35', 36: '36', 37: '37', 38: '38', 39: '39', 40: '40', 41: '41', 42: '42', 43: '43', 44: '44', 45: '45', 46: '46', 47: '47', 48: '48', 49: '49', 50: '50', 51: '51', 52: '52', 53: '53', 54: '54', 55: '55', 56: '56', 57: '57', 58: '58', 59: '59'}, default=30),  # Старт торговли (Минуты)
        'EndH': _Choice({0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23'}, default=13),  # Окончание торговли (Часы)
        'EndM': _Choice({0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23', 24: '24', 25: '25', 26: '26', 27: '27', 28: '28', 29: '29', 30: '30', 31: '31', 32: '32', 33: '33', 34: '34', 35: '35', 36: '36', 37: '37', 38: '38', 39: '39', 40: '40', 41: '41', 42: '42', 43: '43', 44: '44', 45: '45', 46: '46', 47: '47', 48: '48', 49: '49', 50: '50', 51: '51', 52: '52', 53: '53', 54: '54', 55: '55', 56: '56', 57: '57', 58: '58', 59: '59'}, default=5),  # Окончание торговли (Минуты)
    }

