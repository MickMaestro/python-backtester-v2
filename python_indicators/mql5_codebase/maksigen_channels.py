"""maksigen_channels — converted from MQL5: MQL5 Indicators/MaksiGen_Channels/maksigen_channels.mq5

Copyright: Copyright © 2006, MaksiGen; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, MaksiGen', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [16711680], 2: [65280], 3: [255], 4: [16711935]}, 'widths': {1: 2, 2: 5, 3: 5, 4: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Upper 2', 2: 'Upper 1', 3: 'Lower 1', 4: 'Lower 2'}, 'levels': [], 'description': [''], 'name': 'maksigen_channels', 'source': 'MQL5 Indicators/MaksiGen_Channels/maksigen_channels.mq5', 'folder': 'MaksiGen_Channels', 'inputs': [{'mql': 'StartHour1', 'py': 'StartHour1', 'param': 'StartHour1', 'type': 'int', 'default': 0, 'label': 'Session start hour for the channel width', 'sinput': False}, {'mql': 'StartMinute1', 'py': 'StartMinute1', 'param': 'StartMinute1', 'type': 'int', 'default': 0, 'label': 'Minute start hour for the channel width', 'sinput': False}, {'mql': 'EndHour1', 'py': 'EndHour1', 'param': 'EndHour1', 'type': 'int', 'default': 8, 'label': 'Session end hour for the channel width', 'sinput': False}, {'mql': 'EndMinute1', 'py': 'EndMinute1', 'param': 'EndMinute1', 'type': 'int', 'default': 15, 'label': 'Session end minute for the channel width', 'sinput': False}, {'mql': 'StartHour2', 'py': 'StartHour2', 'param': 'StartHour2', 'type': 'int', 'default': 8, 'label': 'Session 1 start hour', 'sinput': False}, {'mql': 'StartMinute2', 'py': 'StartMinute2', 'param': 'StartMinute2', 'type': 'int', 'default': 15, 'label': 'Session 1 start minute', 'sinput': False}, {'mql': 'EndHour2', 'py': 'EndHour2', 'param': 'EndHour2', 'type': 'int', 'default': 12, 'label': 'Session 1 end hour', 'sinput': False}, {'mql': 'EndMinute2', 'py': 'EndMinute2', 'param': 'EndMinute2', 'type': 'int', 'default': 30, 'label': 'Session 1 end minute', 'sinput': False}, {'mql': 'StartHour3', 'py': 'StartHour3', 'param': 'StartHour3', 'type': 'int', 'default': 14, 'label': 'Session 2 start hour', 'sinput': False}, {'mql': 'StartMinute3', 'py': 'StartMinute3', 'param': 'StartMinute3', 'type': 'int', 'default': 0, 'label': 'Session 2 start minute', 'sinput': False}, {'mql': 'EndHour3', 'py': 'EndHour3', 'param': 'EndHour3', 'type': 'int', 'default': 17, 'label': 'Session 2 end hour', 'sinput': False}, {'mql': 'EndMinute3', 'py': 'EndMinute3', 'param': 'EndMinute3', 'type': 'int', 'default': 30, 'label': 'Session 2 end minute', 'sinput': False}, {'mql': 'Dispersion', 'py': 'Dispersion', 'param': 'Dispersion', 'type': 'uint', 'default': 100, 'label': 'Spread of the second channel width in points', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
StartHour1 = _input('StartHour1', H00)  # Session start hour for the channel width
StartMinute1 = _input('StartMinute1', M00)  # Minute start hour for the channel width
EndHour1 = _input('EndHour1', H08)  # Session end hour for the channel width
EndMinute1 = _input('EndMinute1', M15)  # Session end minute for the channel width
StartHour2 = _input('StartHour2', H08)  # Session 1 start hour
StartMinute2 = _input('StartMinute2', M15)  # Session 1 start minute
EndHour2 = _input('EndHour2', H12)  # Session 1 end hour
EndMinute2 = _input('EndMinute2', M30)  # Session 1 end minute
StartHour3 = _input('StartHour3', H14)  # Session 2 start hour
StartMinute3 = _input('StartMinute3', M00)  # Session 2 start minute
EndHour3 = _input('EndHour3', H17)  # Session 2 end hour
EndMinute3 = _input('EndMinute3', M30)  # Session 2 end minute
Dispersion = _input('Dispersion', 100)  # Spread of the second channel width in points
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
Up2Buffer = Arr(0, 0.0)
Up1Buffer = Arr(0, 0.0)
Dn1Buffer = Arr(0, 0.0)
Dn2Buffer = Arr(0, 0.0)
dDispersion = 0.0
min_rates_total = 0

def OnInit():
    global dDispersion, min_rates_total
    min_rates_total = _idiv(PeriodSeconds(PERIOD_D1), PeriodSeconds()) + 1
    dDispersion = Dispersion * Point()
    SetIndexBuffer(0, Up2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(Up2Buffer, True)
    SetIndexBuffer(1, Up1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(Up1Buffer, True)
    SetIndexBuffer(2, Dn1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(Dn1Buffer, True)
    SetIndexBuffer(3, Dn2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(Dn2Buffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MaksiGen_Channels')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_HH, _s_OnCalculate_LL, _s_OnCalculate_day
    if Period() > PERIOD_H1:
        Comment('Indicator MaksiGen_Channels requires timeframe below H2!')
        return 0
    if rates_total < min_rates_total:
        return 0
    bar = 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 3
        _s_OnCalculate_day = -1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Up1Buffer[bar] = 0.0
        Dn1Buffer[bar] = 0.0
        Up2Buffer[bar] = 0.0
        Dn2Buffer[bar] = 0.0
        tmb = MqlDateTime()
        TimeToStruct(time[bar], tmb)
        if ((tmb.hour == EndHour1 and tmb.min > EndMinute1) or tmb.hour > EndHour1) and tmb.day != _s_OnCalculate_day:
            _s_OnCalculate_day = tmb.day
            start1 = 0
            end1 = 0
            for index in range(bar + 1, rates_total - 1):
                tmi = MqlDateTime()
                tmr = MqlDateTime()
                tmf = MqlDateTime()
                TimeToStruct(time[index], tmi)
                TimeToStruct(time[index + 1], tmr)
                TimeToStruct(time[index - 1], tmf)
                if (tmi.hour == StartHour1 and tmr.hour != StartHour1) or (((tmi.hour == StartHour1 and tmr.hour == StartHour1) and tmi.min >= StartMinute1) and tmr.min < StartMinute1):
                    start1 = index
                    break
                if (tmi.hour == EndHour1 and tmf.hour != EndHour1) or (((tmi.hour == EndHour1 and tmf.hour == EndHour1) and tmi.min <= EndMinute1) and tmf.min > EndMinute1):
                    end1 = index
            if (not start1) and (not end1):
                continue
            count = start1 - end1
            _s_OnCalculate_HH = high[ArrayMaximum(high, end1, count)]
            _s_OnCalculate_LL = low[ArrayMinimum(low, end1, count)]
        if ((tmb.hour == StartHour2 and tmb.min >= StartMinute2) or tmb.hour > StartHour2) and ((tmb.hour == EndHour2 and tmb.min <= StartMinute2) or tmb.hour < EndHour2):
            Up1Buffer[bar] = _s_OnCalculate_HH
            Dn1Buffer[bar] = _s_OnCalculate_LL
            Up2Buffer[bar] = _s_OnCalculate_HH + dDispersion
            Dn2Buffer[bar] = _s_OnCalculate_LL - dDispersion
        if ((tmb.hour == StartHour3 and tmb.min >= StartMinute3) or tmb.hour > StartHour3) and ((tmb.hour == EndHour3 and tmb.min <= StartMinute3) or tmb.hour < EndHour3):
            Up1Buffer[bar] = _s_OnCalculate_HH
            Dn1Buffer[bar] = _s_OnCalculate_LL
            Up2Buffer[bar] = _s_OnCalculate_HH + dDispersion
            Dn2Buffer[bar] = _s_OnCalculate_LL - dDispersion
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_HH = 0.0
_s_OnCalculate_LL = 0.0
_s_OnCalculate_day = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MaksigenChannels(_MQL5Indicator):
    name = 'maksigen_channels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'StartHour1': _Choice({0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23'}, default=0),  # Session start hour for the channel width
        'StartMinute1': _Choice({0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23', 24: '24', 25: '25', 26: '26', 27: '27', 28: '28', 29: '29', 30: '30', 31: '31', 32: '32', 33: '33', 34: '34', 35: '35', 36: '36', 37: '37', 38: '38', 39: '39', 40: '40', 41: '41', 42: '42', 43: '43', 44: '44', 45: '45', 46: '46', 47: '47', 48: '48', 49: '49', 50: '50', 51: '51', 52: '52', 53: '53', 54: '54', 55: '55', 56: '56', 57: '57', 58: '58', 59: '59'}, default=0),  # Minute start hour for the channel width
        'EndHour1': _Choice({0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23'}, default=8),  # Session end hour for the channel width
        'EndMinute1': _Choice({0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23', 24: '24', 25: '25', 26: '26', 27: '27', 28: '28', 29: '29', 30: '30', 31: '31', 32: '32', 33: '33', 34: '34', 35: '35', 36: '36', 37: '37', 38: '38', 39: '39', 40: '40', 41: '41', 42: '42', 43: '43', 44: '44', 45: '45', 46: '46', 47: '47', 48: '48', 49: '49', 50: '50', 51: '51', 52: '52', 53: '53', 54: '54', 55: '55', 56: '56', 57: '57', 58: '58', 59: '59'}, default=15),  # Session end minute for the channel width
        'StartHour2': _Choice({0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23'}, default=8),  # Session 1 start hour
        'StartMinute2': _Choice({0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23', 24: '24', 25: '25', 26: '26', 27: '27', 28: '28', 29: '29', 30: '30', 31: '31', 32: '32', 33: '33', 34: '34', 35: '35', 36: '36', 37: '37', 38: '38', 39: '39', 40: '40', 41: '41', 42: '42', 43: '43', 44: '44', 45: '45', 46: '46', 47: '47', 48: '48', 49: '49', 50: '50', 51: '51', 52: '52', 53: '53', 54: '54', 55: '55', 56: '56', 57: '57', 58: '58', 59: '59'}, default=15),  # Session 1 start minute
        'EndHour2': _Choice({0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23'}, default=12),  # Session 1 end hour
        'EndMinute2': _Choice({0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23', 24: '24', 25: '25', 26: '26', 27: '27', 28: '28', 29: '29', 30: '30', 31: '31', 32: '32', 33: '33', 34: '34', 35: '35', 36: '36', 37: '37', 38: '38', 39: '39', 40: '40', 41: '41', 42: '42', 43: '43', 44: '44', 45: '45', 46: '46', 47: '47', 48: '48', 49: '49', 50: '50', 51: '51', 52: '52', 53: '53', 54: '54', 55: '55', 56: '56', 57: '57', 58: '58', 59: '59'}, default=30),  # Session 1 end minute
        'StartHour3': _Choice({0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23'}, default=14),  # Session 2 start hour
        'StartMinute3': _Choice({0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23', 24: '24', 25: '25', 26: '26', 27: '27', 28: '28', 29: '29', 30: '30', 31: '31', 32: '32', 33: '33', 34: '34', 35: '35', 36: '36', 37: '37', 38: '38', 39: '39', 40: '40', 41: '41', 42: '42', 43: '43', 44: '44', 45: '45', 46: '46', 47: '47', 48: '48', 49: '49', 50: '50', 51: '51', 52: '52', 53: '53', 54: '54', 55: '55', 56: '56', 57: '57', 58: '58', 59: '59'}, default=0),  # Session 2 start minute
        'EndHour3': _Choice({0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23'}, default=17),  # Session 2 end hour
        'EndMinute3': _Choice({0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23', 24: '24', 25: '25', 26: '26', 27: '27', 28: '28', 29: '29', 30: '30', 31: '31', 32: '32', 33: '33', 34: '34', 35: '35', 36: '36', 37: '37', 38: '38', 39: '39', 40: '40', 41: '41', 42: '42', 43: '43', 44: '44', 45: '45', 46: '46', 47: '47', 48: '48', 49: '49', 50: '50', 51: '51', 52: '52', 53: '53', 54: '54', 55: '55', 56: '56', 57: '57', 58: '58', 59: '59'}, default=30),  # Session 2 end minute
        'Dispersion': 100,  # Spread of the second channel width in points
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

