"""shadeny — converted from MQL5: MQL5 Indicators/ShadeNY/shadeny.mq5

Copyright: Copyright © 2006, sx ted; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, sx ted', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16760576]}, 'widths': {}, 'styles': {1: 0}, 'labels': {1: 'ShadeNY'}, 'levels': [], 'description': [], 'name': 'shadeny', 'source': 'MQL5 Indicators/ShadeNY/shadeny.mq5', 'folder': 'ShadeNY', 'inputs': [{'mql': 'StartHour', 'py': 'StartHour', 'param': 'StartHour', 'type': 'int', 'default': 7, 'label': 'Session start hour', 'sinput': False}, {'mql': 'StartMinute', 'py': 'StartMinute', 'param': 'StartMinute', 'type': 'int', 'default': 0, 'label': 'Session start minute', 'sinput': False}, {'mql': 'EndHour', 'py': 'EndHour', 'param': 'EndHour', 'type': 'int', 'default': 13, 'label': 'Session end hour', 'sinput': False}, {'mql': 'EndMinute', 'py': 'EndMinute', 'param': 'EndMinute', 'type': 'int', 'default': 0, 'label': 'Session start minute', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'uint', 'default': 0, 'label': 'Horizontal shift of the channel in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Hour
H00 = 0
H01 = 1
H02 = 2
H03 = 3
H04 = 4
H05 = 5
H06 = 6
H07 = 7
H08 = 8
H09 = 9
H10 = 10
H11 = 11
H12 = 12
H13 = 13
H14 = 14
H15 = 15
H16 = 16
H17 = 17
H18 = 18
H19 = 19
H20 = 20
H21 = 21
H22 = 22
H23 = 23
_enum('Hour', {0: 'H00', 1: 'H01', 2: 'H02', 3: 'H03', 4: 'H04', 5: 'H05', 6: 'H06', 7: 'H07', 8: 'H08', 9: 'H09', 10: 'H10', 11: 'H11', 12: 'H12', 13: 'H13', 14: 'H14', 15: 'H15', 16: 'H16', 17: 'H17', 18: 'H18', 19: 'H19', 20: 'H20', 21: 'H21', 22: 'H22', 23: 'H23'})

# enum Min
M00 = 0
M01 = 1
M02 = 2
M03 = 3
M04 = 4
M05 = 5
M06 = 6
M07 = 7
M08 = 8
M09 = 9
M10 = 10
M11 = 11
M12 = 12
M13 = 13
M14 = 14
M15 = 15
M16 = 16
M17 = 17
M18 = 18
M19 = 19
M20 = 20
M21 = 21
M22 = 22
M23 = 23
M24 = 24
M25 = 25
M26 = 26
M27 = 27
M28 = 28
M29 = 29
M30 = 30
M31 = 31
M32 = 32
M33 = 33
M34 = 34
M35 = 35
M36 = 36
M37 = 37
M38 = 38
M39 = 39
M40 = 40
M41 = 41
M42 = 42
M43 = 43
M44 = 44
M45 = 45
M46 = 46
M47 = 47
M48 = 48
M49 = 49
M50 = 50
M51 = 51
M52 = 52
M53 = 53
M54 = 54
M55 = 55
M56 = 56
M57 = 57
M58 = 58
M59 = 59
_enum('Min', {0: 'M00', 1: 'M01', 2: 'M02', 3: 'M03', 4: 'M04', 5: 'M05', 6: 'M06', 7: 'M07', 8: 'M08', 9: 'M09', 10: 'M10', 11: 'M11', 12: 'M12', 13: 'M13', 14: 'M14', 15: 'M15', 16: 'M16', 17: 'M17', 18: 'M18', 19: 'M19', 20: 'M20', 21: 'M21', 22: 'M22', 23: 'M23', 24: 'M24', 25: 'M25', 26: 'M26', 27: 'M27', 28: 'M28', 29: 'M29', 30: 'M30', 31: 'M31', 32: 'M32', 33: 'M33', 34: 'M34', 35: 'M35', 36: 'M36', 37: 'M37', 38: 'M38', 39: 'M39', 40: 'M40', 41: 'M41', 42: 'M42', 43: 'M43', 44: 'M44', 45: 'M45', 46: 'M46', 47: 'M47', 48: 'M48', 49: 'M49', 50: 'M50', 51: 'M51', 52: 'M52', 53: 'M53', 54: 'M54', 55: 'M55', 56: 'M56', 57: 'M57', 58: 'M58', 59: 'M59'})

# ---- inputs and global variables
StartHour = _input('StartHour', H07)  # Session start hour
StartMinute = _input('StartMinute', M00)  # Session start minute
EndHour = _input('EndHour', H13)  # Session end hour
EndMinute = _input('EndMinute', M00)  # Session start minute
Shift = _input('Shift', 0)  # Horizontal shift of the channel in bars
min_rates_total = 0
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    if Period() > PERIOD_H1:
        Print('The ShadeNY requires timeframe below H2!')
        return INIT_FAILED
    min_rates_total = _idiv(PeriodSeconds(PERIOD_D1), PeriodSeconds(PERIOD_CURRENT)) + 1
    SetIndexBuffer(0, ExtABuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtABuffer, True)
    SetIndexBuffer(1, ExtBBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtBBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 2)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ShadeNY')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    global _s_OnCalculate_start
    if rates_total < min_rates_total:
        return 0
    HH = 0.0
    LL = 0.0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 2
        _s_OnCalculate_start = 0
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Time, True)
    _s_OnCalculate_start += limit
    for bar in range(limit, 0 - 1, -1):
        ExtABuffer[bar] = 0.0
        ExtBBuffer[bar] = 0.0
        tm0 = MqlDateTime()
        tm1 = MqlDateTime()
        tmx = MqlDateTime()
        TimeToStruct(Time[bar], tm0)
        TimeToStruct(Time[bar + 1], tm1)
        TimeToStruct(Time[MathMax(bar - 1, 0)], tmx)
        if (((tm0.hour == StartHour and tm0.min == StartMinute) or ((tm0.hour == StartHour and tm0.min > StartMinute) and (tm1.hour != StartHour or (tm1.hour == StartHour and tm1.min < StartMinute)))) or ((tm0.hour > StartHour and tm1.hour == StartHour) and tm1.min < StartMinute)) or (tm0.hour > StartHour and tm0.day != tm1.day):
            _s_OnCalculate_start = bar
        if ((tm0.hour == StartHour and tm0.min >= StartMinute) or tm0.hour > StartHour) and ((tm0.hour == EndHour and tm0.min <= EndMinute) or tm0.hour < EndHour):
            if ((not bar) or tmx.hour > EndHour) or (tmx.hour == EndHour and (tmx.min > EndMinute or tm0.day != tmx.day)):
                HH = High[ArrayMaximum(High, bar, _s_OnCalculate_start - bar + 1)]
                LL = Low[ArrayMinimum(Low, bar, _s_OnCalculate_start - bar + 1)]
                for index in range(_s_OnCalculate_start, bar - 1, -1):
                    ExtABuffer[index] = HH
                    ExtBBuffer[index] = LL
    return rates_total

# ---- static local variables
_s_OnCalculate_start = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Shadeny(_MQL5Indicator):
    name = 'shadeny'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'StartHour': _Choice({0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23'}, default=7),  # Session start hour
        'StartMinute': _Choice({0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23', 24: '24', 25: '25', 26: '26', 27: '27', 28: '28', 29: '29', 30: '30', 31: '31', 32: '32', 33: '33', 34: '34', 35: '35', 36: '36', 37: '37', 38: '38', 39: '39', 40: '40', 41: '41', 42: '42', 43: '43', 44: '44', 45: '45', 46: '46', 47: '47', 48: '48', 49: '49', 50: '50', 51: '51', 52: '52', 53: '53', 54: '54', 55: '55', 56: '56', 57: '57', 58: '58', 59: '59'}, default=0),  # Session start minute
        'EndHour': _Choice({0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23'}, default=13),  # Session end hour
        'EndMinute': _Choice({0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23', 24: '24', 25: '25', 26: '26', 27: '27', 28: '28', 29: '29', 30: '30', 31: '31', 32: '32', 33: '33', 34: '34', 35: '35', 36: '36', 37: '37', 38: '38', 39: '39', 40: '40', 41: '41', 42: '42', 43: '43', 44: '44', 45: '45', 46: '46', 47: '47', 48: '48', 49: '49', 50: '50', 51: '51', 52: '52', 53: '53', 54: '54', 55: '55', 56: '56', 57: '57', 58: '58', 59: '59'}, default=0),  # Session start minute
        'Shift': 0,  # Horizontal shift of the channel in bars
    }

