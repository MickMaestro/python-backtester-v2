"""RangeExpansionIndex — converted from MQL5: MQL5 Indicators/Range Expansion Index (REI) MT5/RangeExpansionIndex.mq5

Calculates Tom DeMark's Range Expansion Index.
Going above 60 and then dropping below 60 signals price weakness.
Going below -60 and the rising above -60 signals price strength.
For more info see The New Science of Technical Analysis.
Copyright: https://t.me/ForexEaPremium; Link: https://t.me/ForexEaPremium; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'https://t.me/ForexEaPremium', 'link': 'https://t.me/ForexEaPremium', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [60.0, -60.0], 'description': ["Calculates Tom DeMark's Range Expansion Index.", 'Going above 60 and then dropping below 60 signals price weakness.', 'Going below -60 and the rising above -60 signals price strength.', 'For more info see The New Science of Technical Analysis.'], 'name': 'RangeExpansionIndex', 'source': 'MQL5 Indicators/Range Expansion Index (REI) MT5/RangeExpansionIndex.mq5', 'folder': 'Range Expansion Index (REI) MT5', 'inputs': [{'mql': 'REI_Period', 'py': 'REI_Period', 'param': 'REI_Period', 'type': 'int', 'default': 8, 'label': 'REI Period', 'sinput': False}, {'mql': 'EnableNativeAlerts', 'py': 'EnableNativeAlerts', 'param': 'EnableNativeAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnableEmailAlerts', 'py': 'EnableEmailAlerts', 'param': 'EnableEmailAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnablePushAlerts', 'py': 'EnablePushAlerts', 'param': 'EnablePushAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'TriggerCandle', 'py': 'TriggerCandle', 'param': 'TriggerCandle', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enum_candle_to_check
Current = 0
Previous = 1
_enum('enum_candle_to_check', {0: 'Current', 1: 'Previous'})

# ---- inputs and global variables
REI_Period = _input('REI_Period', 8)  # REI Period
EnableNativeAlerts = _input('EnableNativeAlerts', False)
EnableEmailAlerts = _input('EnableEmailAlerts', False)
EnablePushAlerts = _input('EnablePushAlerts', False)
TriggerCandle = _input('TriggerCandle', Previous)
REI = Arr(0, 0.0)
LastAlertTime = 0

def OnInit():
    IndicatorSetString(INDICATOR_SHORTNAME, 'REI(' + IntegerToString(REI_Period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    SetIndexBuffer(0, REI, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, REI_Period + 8)

def OnCalculate(rates_total, prev_calculated, Time, open, High, Low, Close, tick_volume, volume, spread):
    global LastAlertTime
    limit = 0
    if rates_total <= (REI_Period + 8):
        return 0
    counted_bars = prev_calculated
    if counted_bars < (8 + REI_Period):
        limit = 8 + REI_Period
    else:
        limit = rates_total - 1
    for i in range(rates_total - 1, limit - 1, -1):
        SubValueSum = 0.0
        AbsDailyValueSum = 0.0
        for j in range(0, REI_Period):
            SubValueSum += SubValue(i - j, High, Low, Close)
            AbsDailyValueSum += AbsDailyValue(i - j, High, Low, Close)
        if AbsDailyValueSum != 0:
            REI[i] = _fdiv(SubValueSum, AbsDailyValueSum) * 100
        else:
            REI[i] = 0.0
    if (TriggerCandle > 0 and Time[rates_total - 1] > LastAlertTime) or TriggerCandle == 0:
        Text = ""
        if REI[rates_total - 1 - TriggerCandle] < 60 and REI[rates_total - 2 - TriggerCandle] >= 60:
            Text = 'REI: ' + Symbol() + ' - ' + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7) + ' - Crossed 60 from above.'
            if EnableNativeAlerts:
                Alert(Text)
            if EnableEmailAlerts:
                SendMail('REI Alert', Text)
            if EnablePushAlerts:
                SendNotification(Text)
            LastAlertTime = Time[rates_total - 1]
        if REI[rates_total - 1 - TriggerCandle] > -60 and REI[rates_total - 2 - TriggerCandle] <= -60:
            Text = 'REI: ' + Symbol() + ' - ' + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7) + ' - Crossed -60 from below.'
            if EnableNativeAlerts:
                Alert(Text)
            if EnableEmailAlerts:
                SendMail('REI Alert', Text)
            if EnablePushAlerts:
                SendNotification(Text)
            LastAlertTime = Time[rates_total - 1]
    return rates_total

def SubValue(i, High, Low, Close):
    num_zero1 = 0
    num_zero2 = 0
    diff1 = High[i] - High[i - 2]
    diff2 = Low[i] - Low[i - 2]
    if ((High[i - 2] < Close[i - 7] and High[i - 2] < Close[i - 8]) and High[i] < High[i - 5]) and High[i] < High[i - 6]:
        num_zero1 = 0
    else:
        num_zero1 = 1
    if ((Low[i - 2] > Close[i - 7] and Low[i - 2] > Close[i - 8]) and Low[i] > Low[i - 5]) and Low[i] > Low[i - 6]:
        num_zero2 = 0
    else:
        num_zero2 = 1
    return num_zero1 * num_zero2 * (diff1 + diff2)

def AbsDailyValue(i, High, Low, Close):
    diff1 = MathAbs(High[i] - High[i - 2])
    diff2 = MathAbs(Low[i] - Low[i - 2])
    return diff1 + diff2


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RangeExpansionIndex(_MQL5Indicator):
    name = 'RangeExpansionIndex'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'REI_Period': 8,  # REI Period
        'EnableNativeAlerts': False,
        'EnableEmailAlerts': False,
        'EnablePushAlerts': False,
        'TriggerCandle': _Choice({0: 'Current', 1: 'Previous'}, default=1),
    }

