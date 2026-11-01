"""CCI Arrows — converted from MQL5: MQL5 Indicators/CCI Arrows MT5/CCI Arrows.mq5

CCI arrows based on the cross of the zero line from below or from above.
Displays red and blue arrows for Short and Long signals.
Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'version': '1.02', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['CCI arrows based on the cross of the zero line from below or from above.', 'Displays red and blue arrows for Short and Long signals.'], 'name': 'CCI Arrows', 'source': 'MQL5 Indicators/CCI Arrows MT5/CCI Arrows.mq5', 'folder': 'CCI Arrows MT5', 'inputs': [{'mql': 'CCI_Period', 'py': 'CCI_Period', 'param': 'CCI_Period', 'type': 'int', 'default': 14, 'label': 'CCI Period', 'sinput': False}, {'mql': 'EnableNativeAlerts', 'py': 'EnableNativeAlerts', 'param': 'EnableNativeAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnableEmailAlerts', 'py': 'EnableEmailAlerts', 'param': 'EnableEmailAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnablePushAlerts', 'py': 'EnablePushAlerts', 'param': 'EnablePushAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'TriggerCandle', 'py': 'TriggerCandle', 'param': 'TriggerCandle', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enum_candle_to_check
Current = 0
Previous = 1
_enum('enum_candle_to_check', {0: 'Current', 1: 'Previous'})

# ---- inputs and global variables
CCI_Period = _input('CCI_Period', 14)  # CCI Period
EnableNativeAlerts = _input('EnableNativeAlerts', False)
EnableEmailAlerts = _input('EnableEmailAlerts', False)
EnablePushAlerts = _input('EnablePushAlerts', False)
TriggerCandle = _input('TriggerCandle', Previous)
dUpCCIBuffer = Arr(0, 0.0)
dDownCCIBuffer = Arr(0, 0.0)
myCCI = 0
LastAlertDirection = 0
LastAlertTime = 0
FirstRun = False

def OnInit():
    global FirstRun, LastAlertDirection, LastAlertTime, myCCI
    FirstRun = True
    LastAlertDirection = 0
    LastAlertTime = 0
    IndicatorSetString(INDICATOR_SHORTNAME, 'CCI Arrows (' + IntegerToString(CCI_Period) + ')')
    SetIndexBuffer(0, dUpCCIBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, dDownCCIBuffer, INDICATOR_DATA)
    ArraySetAsSeries(dUpCCIBuffer, True)
    ArraySetAsSeries(dDownCCIBuffer, True)
    PlotIndexSetInteger(0, PLOT_ARROW, 233)
    PlotIndexSetInteger(1, PLOT_ARROW, 234)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetString(0, PLOT_LABEL, 'CCI Buy')
    PlotIndexSetString(1, PLOT_LABEL, 'CCI Sell')
    myCCI = iCCI(None, 0, CCI_Period, PRICE_CLOSE)

def OnCalculate(rates_total, prev_calculated, Time, open, High, Low, close, tick_volume, volume, spread):
    global FirstRun, LastAlertDirection, LastAlertTime
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Time, True)
    counted_bars = prev_calculated
    if counted_bars > 0:
        counted_bars -= 1
    limit = rates_total - 1 - counted_bars
    CCIBuffer = Arr(0, 0.0)
    CopyBuffer(myCCI, 0, 0, rates_total, CCIBuffer)
    ArraySetAsSeries(CCIBuffer, True)
    if limit == 1:
        limit += 1
    for i in range(0, limit):
        dUpCCIBuffer[i] = 0.0
        dDownCCIBuffer[i] = 0.0
        myCCInow = CCIBuffer[i]
        myCCI2 = CCIBuffer[i + 1]
        if myCCInow >= 0:
            if myCCInow > 0 and myCCI2 < 0:
                distance = (High[iHighest(Symbol(), Period(), MODE_HIGH, 20, i)] - Low[iLowest(Symbol(), Period(), MODE_LOW, 20, i)]) * 0.02
                dUpCCIBuffer[i] = Low[i] - (2 * distance)
        if myCCInow < 0:
            if myCCInow < 0 and myCCI2 > 0:
                distance = (High[iHighest(Symbol(), Period(), MODE_HIGH, 20, i)] - Low[iLowest(Symbol(), Period(), MODE_LOW, 20, i)]) * 0.02
                dDownCCIBuffer[i] = High[i] + (2 * distance)
    if (not FirstRun) and ((EnableNativeAlerts or EnableEmailAlerts) or EnablePushAlerts):
        if (TriggerCandle > 0 and Time[0] > LastAlertTime) or TriggerCandle == 0:
            Text = ""
            if dUpCCIBuffer[TriggerCandle] != 0 and LastAlertDirection != 1:
                Text = 'Up Arrow'
                if EnableNativeAlerts:
                    Alert(Text)
                Text = 'CCI Arrows: ' + Symbol() + ' - ' + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7) + ' - ' + Text + '.'
                if EnableEmailAlerts:
                    SendMail('CCI Arrows Alert', Text)
                if EnablePushAlerts:
                    SendNotification(Text)
                LastAlertTime = Time[0]
                LastAlertDirection = 1
            if dDownCCIBuffer[TriggerCandle] != 0 and LastAlertDirection != -1:
                Text = 'Down Arrow'
                if EnableNativeAlerts:
                    Alert(Text)
                Text = 'CCI Arrows: ' + Symbol() + ' - ' + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7) + ' - ' + Text + '.'
                if EnableEmailAlerts:
                    SendMail('CCI Arrows Alert', Text)
                if EnablePushAlerts:
                    SendNotification(Text)
                LastAlertTime = Time[0]
                LastAlertDirection = -1
    FirstRun = False
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CCIArrows(_MQL5Indicator):
    name = 'CCI Arrows'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CCI_Period': 14,  # CCI Period
        'EnableNativeAlerts': False,
        'EnableEmailAlerts': False,
        'EnablePushAlerts': False,
        'TriggerCandle': _Choice({0: 'Current', 1: 'Previous'}, default=1),
    }

