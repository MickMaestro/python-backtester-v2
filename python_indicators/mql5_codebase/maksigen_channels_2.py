"""maksigen_channels_2 — converted from MQL5: MQL5 Indicators/Maksigen channels - 2/maksigen_channels_2.mq5

Copyright: © 2016, MetaQuotes Software Corp.; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© 2016, MetaQuotes Software Corp.', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 6}, 'types': {1: 7, 2: 7, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [14474460], 2: [14474460], 3: [65280], 4: [3329330], 5: [255], 6: [42495]}, 'widths': {3: 2, 4: 5, 5: 5, 6: 2}, 'styles': {3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'Area 2', 2: 'Area1', 3: 'Upper 2', 4: 'Upper 1', 5: 'Lower 1', 6: 'Lower 2'}, 'levels': [], 'description': [''], 'name': 'maksigen_channels_2', 'source': 'MQL5 Indicators/Maksigen channels - 2/maksigen_channels_2.mq5', 'folder': 'Maksigen channels - 2', 'inputs': [{'mql': 'StartHour1', 'py': 'StartHour1', 'param': 'StartHour1', 'type': 'int', 'default': 0, 'label': 'Session start hour for the channel width', 'sinput': False}, {'mql': 'StartMinute1', 'py': 'StartMinute1', 'param': 'StartMinute1', 'type': 'int', 'default': 0, 'label': 'Minute start hour for the channel width', 'sinput': False}, {'mql': 'EndHour1', 'py': 'EndHour1', 'param': 'EndHour1', 'type': 'int', 'default': 8, 'label': 'Session end hour for the channel width', 'sinput': False}, {'mql': 'EndMinute1', 'py': 'EndMinute1', 'param': 'EndMinute1', 'type': 'int', 'default': 15, 'label': 'Session end minute for the channel width', 'sinput': False}, {'mql': 'StartHour2', 'py': 'StartHour2', 'param': 'StartHour2', 'type': 'int', 'default': 8, 'label': 'Session 1 start hour', 'sinput': False}, {'mql': 'StartMinute2', 'py': 'StartMinute2', 'param': 'StartMinute2', 'type': 'int', 'default': 15, 'label': 'Session 1 start minute', 'sinput': False}, {'mql': 'EndHour2', 'py': 'EndHour2', 'param': 'EndHour2', 'type': 'int', 'default': 12, 'label': 'Session 1 end hour', 'sinput': False}, {'mql': 'EndMinute2', 'py': 'EndMinute2', 'param': 'EndMinute2', 'type': 'int', 'default': 30, 'label': 'Session 1 end minute', 'sinput': False}, {'mql': 'StartHour3', 'py': 'StartHour3', 'param': 'StartHour3', 'type': 'int', 'default': 14, 'label': 'Session 2 start hour', 'sinput': False}, {'mql': 'StartMinute3', 'py': 'StartMinute3', 'param': 'StartMinute3', 'type': 'int', 'default': 0, 'label': 'Session 2 start minute', 'sinput': False}, {'mql': 'EndHour3', 'py': 'EndHour3', 'param': 'EndHour3', 'type': 'int', 'default': 17, 'label': 'Session 2 end hour', 'sinput': False}, {'mql': 'EndMinute3', 'py': 'EndMinute3', 'param': 'EndMinute3', 'type': 'int', 'default': 30, 'label': 'Session 2 end minute', 'sinput': False}, {'mql': 'Dispersion', 'py': 'Dispersion', 'param': 'Dispersion', 'type': 'uint', 'default': 100, 'label': 'Spread of the second channel width in points', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
maxValues = Arr(0, 0.0)
minValues = Arr(0, 0.0)
fillu2 = Arr(0, 0.0)
fillu1 = Arr(0, 0.0)
filld1 = Arr(0, 0.0)
filld2 = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, fillu2, INDICATOR_DATA)
    SetIndexBuffer(1, filld2, INDICATOR_DATA)
    SetIndexBuffer(2, fillu1, INDICATOR_DATA)
    SetIndexBuffer(3, filld1, INDICATOR_DATA)
    SetIndexBuffer(4, Up2Buffer, INDICATOR_DATA)
    SetIndexBuffer(5, Up1Buffer, INDICATOR_DATA)
    SetIndexBuffer(6, Dn1Buffer, INDICATOR_DATA)
    SetIndexBuffer(7, Dn2Buffer, INDICATOR_DATA)
    SetIndexBuffer(8, maxValues, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, minValues, INDICATOR_CALCULATIONS)
    for i in range(0, 6):
        PlotIndexSetInteger(i, PLOT_SHIFT, Shift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MaksiGen_Channels')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_warned
    if Period() > PERIOD_H1:
        Comment('Indicator MaksiGen_Channels requires timeframe below H2!')
        _s_OnCalculate_warned = True
        return 0
    if _s_OnCalculate_warned:
        Comment('')
        _s_OnCalculate_warned = False
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    dDispersion = Dispersion * Point()
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        Dn2Buffer[i] = EMPTY_VALUE
        Up2Buffer[i] = Dn2Buffer[i]
        Dn1Buffer[i] = Up2Buffer[i]
        Up1Buffer[i] = Dn1Buffer[i]
        maxValues[i] = (maxValues[i - 1] if (i > 0) else high[i])
        minValues[i] = (minValues[i - 1] if (i > 0) else low[i])
        if i > 0:
            if checkTimeLimits_2(StartHour1, StartMinute1, EndHour1, EndMinute1, time[i]):
                if checkTimeLimits_2(StartHour1, StartMinute1, EndHour1, EndMinute1, time[i - 1]):
                    maxValues[i] = MathMax(maxValues[i - 1], high[i])
                    minValues[i] = MathMin(minValues[i - 1], low[i])
                else:
                    maxValues[i] = high[i]
                    minValues[i] = low[i]
        if checkTimeLimits_2(StartHour2, StartMinute2, EndHour2, EndMinute2, time[i]):
            Up1Buffer[i] = maxValues[i]
            Dn1Buffer[i] = minValues[i]
            Up2Buffer[i] = Up1Buffer[i] + dDispersion
            Dn2Buffer[i] = Dn1Buffer[i] - dDispersion
        if checkTimeLimits_2(StartHour3, StartMinute3, EndHour3, EndMinute3, time[i]):
            Up1Buffer[i] = maxValues[i]
            Dn1Buffer[i] = minValues[i]
            Up2Buffer[i] = Up1Buffer[i] + dDispersion
            Dn2Buffer[i] = Dn1Buffer[i] - dDispersion
        fillu1[i] = Up1Buffer[i]
        fillu2[i] = Up2Buffer[i]
        filld1[i] = Dn1Buffer[i]
        filld2[i] = Dn2Buffer[i]
    return rates_total

def checkTimeLimits_1(startHour, endHour, timeToCheck):
    return checkTimeLimits_3(startHour, 0, 0, endHour, 0, 0, timeToCheck)

def checkTimeLimits_2(startHour, startMinute, endHour, endMinute, timeToCheck):
    return checkTimeLimits_3(startHour, startMinute, 0, endHour, endMinute, 0, timeToCheck)

def checkTimeLimits_3(startHour, startMinute, startSecond, endHour, endMinute, endSecond, timeToCheck):
    answer = False
    tempTime = MqlDateTime()
    TimeToStruct(timeToCheck, tempTime)
    startTime = 0
    endTime = 0
    checkTime = 0
    startTime = (_ctMinMax(startHour, 0, 24) * 3600) + (_ctMinMax(startMinute, 0, 60) * 60) + _ctMinMax(startSecond, 0, 60)
    endTime = (_ctMinMax(endHour, 0, 24) * 3600) + (_ctMinMax(endMinute, 0, 60) * 60) + _ctMinMax(endSecond, 0, 60)
    checkTime = (_ctMinMax(tempTime.hour, 0, 24) * 3600) + (_ctMinMax(tempTime.min, 0, 60) * 60) + _ctMinMax(tempTime.sec, 0, 60)
    if startTime > endTime:
        answer = checkTime >= startTime or checkTime < endTime
    else:
        answer = checkTime >= startTime and checkTime < endTime
    return answer

def _ctMinMax(value, min_, max_):
    return _uint(MathMax(MathMin(value, max_), min_))

# ---- static local variables
_s_OnCalculate_warned = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MaksigenChannels2(_MQL5Indicator):
    name = 'maksigen_channels_2'
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

