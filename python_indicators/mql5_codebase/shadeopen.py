"""ShadeOpen — converted from MQL5: MQL5 Indicators/ShadeOpen/ShadeOpen.mq5

Индикатор ночных ссесий в виде свечек.
Copyright: Copyright © 2017, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 7, 2: 7, 3: 7}, 'colors': {1: [10025880, 65535], 2: [3329330, 36095], 3: [10025880, 65535]}, 'widths': {}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Upper Shade', 2: 'Body', 3: 'Lower Shade'}, 'levels': [], 'description': ['Индикатор ночных ссесий в виде свечек.'], 'name': 'ShadeOpen', 'source': 'MQL5 Indicators/ShadeOpen/ShadeOpen.mq5', 'folder': 'ShadeOpen', 'inputs': [{'mql': 'StartH', 'py': 'StartH', 'param': 'StartH', 'type': 'int', 'default': 6, 'label': 'Старт торговли (Часы)', 'sinput': False}, {'mql': 'StartM', 'py': 'StartM', 'param': 'StartM', 'type': 'int', 'default': 30, 'label': 'Старт торговли (Минуты)', 'sinput': False}, {'mql': 'EndH', 'py': 'EndH', 'param': 'EndH', 'type': 'int', 'default': 13, 'label': 'Окончание торговли (Часы)', 'sinput': False}, {'mql': 'EndM', 'py': 'EndM', 'param': 'EndM', 'type': 'int', 'default': 5, 'label': 'Окончание торговли (Минуты)', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
StartH = _input('StartH', ENUM_HOUR_6)  # Старт торговли (Часы)
StartM = _input('StartM', ENUM_MINUT_30)  # Старт торговли (Минуты)
EndH = _input('EndH', ENUM_HOUR_13)  # Окончание торговли (Часы)
EndM = _input('EndM', ENUM_MINUT_5)  # Окончание торговли (Минуты)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtA1Buffer = Arr(0, 0.0)
ExtB1Buffer = Arr(0, 0.0)
ExtA2Buffer = Arr(0, 0.0)
ExtB2Buffer = Arr(0, 0.0)
ExtA3Buffer = Arr(0, 0.0)
ExtB3Buffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    if StartH > EndH or (StartH == EndH and StartM >= EndM):
        Print('Неверные значения входных переменных старта и окончания торговли!')
        return INIT_PARAMETERS_INCORRECT
    min_rates_total = 2
    ArrayInit(0, ExtA1Buffer)
    ArrayInit(1, ExtB1Buffer)
    ArrayInit(2, ExtA2Buffer)
    ArrayInit(3, ExtB2Buffer)
    ArrayInit(4, ExtA3Buffer)
    ArrayInit(5, ExtB3Buffer)
    PlotInit(0, 2, Shift)
    PlotInit(1, 2, Shift)
    PlotInit(2, 2, Shift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ShadeOpen')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_lshift
    if rates_total < min_rates_total:
        return 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated + _s_OnCalculate_lshift
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    for bar in range(limit, 0 - 1, -1):
        if not ShadeOpenCheck(time[bar]):
            ExtA1Buffer[bar] = 0.0
            ExtB1Buffer[bar] = 0.0
            ExtA2Buffer[bar] = 0.0
            ExtB2Buffer[bar] = 0.0
            ExtA3Buffer[bar] = 0.0
            ExtB3Buffer[bar] = 0.0
            _s_OnCalculate_lshift = 0
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
                ExtA1Buffer[bar] = ihigh
                ExtB1Buffer[bar] = iClose_[0]
                ExtA2Buffer[bar] = iClose_[0]
                ExtB2Buffer[bar] = iOpen_[0]
                ExtA3Buffer[bar] = iOpen_[0]
                ExtB3Buffer[bar] = ilow
            else:
                ExtB1Buffer[bar] = ihigh
                ExtA1Buffer[bar] = iClose_[0]
                ExtA2Buffer[bar] = iClose_[0]
                ExtB2Buffer[bar] = iOpen_[0]
                ExtB3Buffer[bar] = iOpen_[0]
                ExtA3Buffer[bar] = ilow
            _s_OnCalculate_lshift = bar
    return rates_total

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

# ---- static local variables
_s_OnCalculate_lshift = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ShadeOpen(_MQL5Indicator):
    name = 'ShadeOpen'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'StartH': _Choice({0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23'}, default=6),  # Старт торговли (Часы)
        'StartM': _Choice({0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23', 24: '24', 25: '25', 26: '26', 27: '27', 28: '28', 29: '29', 30: '30', 31: '31', 32: '32', 33: '33', 34: '34', 35: '35', 36: '36', 37: '37', 38: '38', 39: '39', 40: '40', 41: '41', 42: '42', 43: '43', 44: '44', 45: '45', 46: '46', 47: '47', 48: '48', 49: '49', 50: '50', 51: '51', 52: '52', 53: '53', 54: '54', 55: '55', 56: '56', 57: '57', 58: '58', 59: '59'}, default=30),  # Старт торговли (Минуты)
        'EndH': _Choice({0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23'}, default=13),  # Окончание торговли (Часы)
        'EndM': _Choice({0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23', 24: '24', 25: '25', 26: '26', 27: '27', 28: '28', 29: '29', 30: '30', 31: '31', 32: '32', 33: '33', 34: '34', 35: '35', 36: '36', 37: '37', 38: '38', 39: '39', 40: '40', 41: '41', 42: '42', 43: '43', 44: '44', 45: '45', 46: '46', 47: '47', 48: '48', 49: '49', 50: '50', 51: '51', 52: '52', 53: '53', 54: '54', 55: '55', 56: '56', 57: '57', 58: '58', 59: '59'}, default=5),  # Окончание торговли (Минуты)
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

