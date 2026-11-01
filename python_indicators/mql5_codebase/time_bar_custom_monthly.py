"""Time_Bar_Custom_Monthly — converted from MQL5: MQL5 Indicators/Time_Bar_Custom_Monthly/Time_Bar_Custom_Monthly.mq5

Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 4}, 'colors': {1: [7451452]}, 'widths': {1: 4}, 'styles': {1: 0}, 'labels': {1: 'Time_Bar_Custom_Monthly'}, 'levels': [], 'description': [], 'name': 'Time_Bar_Custom_Monthly', 'source': 'MQL5 Indicators/Time_Bar_Custom_Monthly/Time_Bar_Custom_Monthly.mq5', 'folder': 'Time_Bar_Custom_Monthly', 'inputs': [{'mql': 'BarDayMonth', 'py': 'BarDayMonth', 'param': 'BarDayMonth', 'type': 'int', 'default': 1, 'label': 'День месяца установки бара', 'sinput': False}, {'mql': 'BarHours', 'py': 'BarHours', 'param': 'BarHours', 'type': 'int', 'default': 0, 'label': 'Время установки бара (Часы)', 'sinput': False}, {'mql': 'BarMinuts', 'py': 'BarMinuts', 'param': 'BarMinuts', 'type': 'int', 'default': 0, 'label': 'Время установки бара (Минуты)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum MONTH_OF_YEAR
ENUM_MONTH_OF_YEAR_1 = 1
ENUM_MONTH_OF_YEAR_2 = 2
ENUM_MONTH_OF_YEAR_3 = 3
ENUM_MONTH_OF_YEAR_4 = 4
ENUM_MONTH_OF_YEAR_5 = 5
ENUM_MONTH_OF_YEAR_6 = 6
ENUM_MONTH_OF_YEAR_7 = 7
ENUM_MONTH_OF_YEAR_8 = 8
ENUM_MONTH_OF_YEAR_9 = 9
ENUM_MONTH_OF_YEAR_10 = 10
ENUM_MONTH_OF_YEAR_11 = 11
ENUM_MONTH_OF_YEAR_12 = 12
_enum('MONTH_OF_YEAR', {1: 'ENUM_MONTH_OF_YEAR_1', 2: 'ENUM_MONTH_OF_YEAR_2', 3: 'ENUM_MONTH_OF_YEAR_3', 4: 'ENUM_MONTH_OF_YEAR_4', 5: 'ENUM_MONTH_OF_YEAR_5', 6: 'ENUM_MONTH_OF_YEAR_6', 7: 'ENUM_MONTH_OF_YEAR_7', 8: 'ENUM_MONTH_OF_YEAR_8', 9: 'ENUM_MONTH_OF_YEAR_9', 10: 'ENUM_MONTH_OF_YEAR_10', 11: 'ENUM_MONTH_OF_YEAR_11', 12: 'ENUM_MONTH_OF_YEAR_12'})

# enum DAY_OF_MONTH
ENUM_DAY_OF_MONTH_1 = 1
ENUM_DAY_OF_MONTH_2 = 2
ENUM_DAY_OF_MONTH_3 = 3
ENUM_DAY_OF_MONTH_4 = 4
ENUM_DAY_OF_MONTH_5 = 5
ENUM_DAY_OF_MONTH_6 = 6
ENUM_DAY_OF_MONTH_7 = 7
ENUM_DAY_OF_MONTH_8 = 8
ENUM_DAY_OF_MONTH_9 = 9
ENUM_DAY_OF_MONTH_10 = 10
ENUM_DAY_OF_MONTH_11 = 11
ENUM_DAY_OF_MONTH_12 = 12
ENUM_DAY_OF_MONTH_13 = 13
ENUM_DAY_OF_MONTH_14 = 14
ENUM_DAY_OF_MONTH_15 = 15
ENUM_DAY_OF_MONTH_16 = 16
ENUM_DAY_OF_MONTH_17 = 17
ENUM_DAY_OF_MONTH_18 = 18
ENUM_DAY_OF_MONTH_19 = 19
ENUM_DAY_OF_MONTH_20 = 20
ENUM_DAY_OF_MONTH_21 = 21
ENUM_DAY_OF_MONTH_22 = 22
ENUM_DAY_OF_MONTH_23 = 23
ENUM_DAY_OF_MONTH_24 = 24
ENUM_DAY_OF_MONTH_25 = 25
ENUM_DAY_OF_MONTH_26 = 26
ENUM_DAY_OF_MONTH_27 = 27
ENUM_DAY_OF_MONTH_28 = 28
ENUM_DAY_OF_MONTH_29 = 29
ENUM_DAY_OF_MONTH_30 = 30
ENUM_DAY_OF_MONTH_31 = 31
_enum('DAY_OF_MONTH', {1: 'ENUM_DAY_OF_MONTH_1', 2: 'ENUM_DAY_OF_MONTH_2', 3: 'ENUM_DAY_OF_MONTH_3', 4: 'ENUM_DAY_OF_MONTH_4', 5: 'ENUM_DAY_OF_MONTH_5', 6: 'ENUM_DAY_OF_MONTH_6', 7: 'ENUM_DAY_OF_MONTH_7', 8: 'ENUM_DAY_OF_MONTH_8', 9: 'ENUM_DAY_OF_MONTH_9', 10: 'ENUM_DAY_OF_MONTH_10', 11: 'ENUM_DAY_OF_MONTH_11', 12: 'ENUM_DAY_OF_MONTH_12', 13: 'ENUM_DAY_OF_MONTH_13', 14: 'ENUM_DAY_OF_MONTH_14', 15: 'ENUM_DAY_OF_MONTH_15', 16: 'ENUM_DAY_OF_MONTH_16', 17: 'ENUM_DAY_OF_MONTH_17', 18: 'ENUM_DAY_OF_MONTH_18', 19: 'ENUM_DAY_OF_MONTH_19', 20: 'ENUM_DAY_OF_MONTH_20', 21: 'ENUM_DAY_OF_MONTH_21', 22: 'ENUM_DAY_OF_MONTH_22', 23: 'ENUM_DAY_OF_MONTH_23', 24: 'ENUM_DAY_OF_MONTH_24', 25: 'ENUM_DAY_OF_MONTH_25', 26: 'ENUM_DAY_OF_MONTH_26', 27: 'ENUM_DAY_OF_MONTH_27', 28: 'ENUM_DAY_OF_MONTH_28', 29: 'ENUM_DAY_OF_MONTH_29', 30: 'ENUM_DAY_OF_MONTH_30', 31: 'ENUM_DAY_OF_MONTH_31'})

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
BarDayMonth = _input('BarDayMonth', ENUM_DAY_OF_MONTH_1)  # День месяца установки бара
BarHours = _input('BarHours', ENUM_HOUR_0)  # Время установки бара (Часы)
BarMinuts = _input('BarMinuts', ENUM_MINUT_0)  # Время установки бара (Минуты)
ExtUpBuffer = Arr(0, 0.0)
ExtDnBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, ExtUpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtDnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(ExtUpBuffer, True)
    ArraySetAsSeries(ExtDnBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Time_Bar_Custom_Monthly(' + _str(BarHours) + ':' + _str(BarMinuts) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def CheckVLinePoint(bartime):
    global _s_CheckVLinePoint_last_month
    tm = MqlDateTime()
    TimeToStruct(bartime, tm)
    if tm.mon == _s_CheckVLinePoint_last_month:
        return False
    if tm.day < BarDayMonth:
        return False
    elif tm.day > BarDayMonth:
        _s_CheckVLinePoint_last_month = tm.mon
        return True
    if tm.hour == BarHours and tm.min >= BarMinuts:
        _s_CheckVLinePoint_last_month = tm.mon
        return True
    if tm.hour > BarHours:
        _s_CheckVLinePoint_last_month = tm.mon
        return True
    return False

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    for bar in range(limit, 0 - 1, -1):
        ExtUpBuffer[bar] = EMPTY_VALUE
        ExtDnBuffer[bar] = EMPTY_VALUE
        if CheckVLinePoint(time[bar]):
            ExtUpBuffer[bar] = 10 * high[bar]
            ExtDnBuffer[bar] = 0.0
    return rates_total

# ---- static local variables
_s_CheckVLinePoint_last_month = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TimeBarCustomMonthly(_MQL5Indicator):
    name = 'Time_Bar_Custom_Monthly'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BarDayMonth': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23', 24: '24', 25: '25', 26: '26', 27: '27', 28: '28', 29: '29', 30: '30', 31: '31'}, default=1),  # День месяца установки бара
        'BarHours': _Choice({0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23'}, default=0),  # Время установки бара (Часы)
        'BarMinuts': _Choice({0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23', 24: '24', 25: '25', 26: '26', 27: '27', 28: '28', 29: '29', 30: '30', 31: '31', 32: '32', 33: '33', 34: '34', 35: '35', 36: '36', 37: '37', 38: '38', 39: '39', 40: '40', 41: '41', 42: '42', 43: '43', 44: '44', 45: '45', 46: '46', 47: '47', 48: '48', 49: '49', 50: '50', 51: '51', 52: '52', 53: '53', 54: '54', 55: '55', 56: '56', 57: '57', 58: '58', 59: '59'}, default=0),  # Время установки бара (Минуты)
    }

