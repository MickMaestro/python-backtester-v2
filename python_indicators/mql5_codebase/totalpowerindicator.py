"""TotalPowerIndicator — converted from MQL5: MQL5 Indicators/Total Power Indicator MT5/TotalPowerIndicator.mq5

Displays the concentration of bull power periods, bear power periods, and total periods when either bulls or bears had prevalence.
Supports two events for alerts:
1. Bull/Bear Power == 100, which is a strong reversal signal.
2. Bull/Bear Crossover, which is a strong trend signal.
Copyright: https://t.me/ForexEaPremium; Link: https://t.me/ForexEaPremium; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'https://t.me/ForexEaPremium', 'link': 'https://t.me/ForexEaPremium', 'version': '1.01', 'window': 'separate', 'indicator_minimum': -10.0, 'indicator_maximum': 110.0, 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [11186720], 2: [3937500], 3: [25600]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'Total Power', 2: 'Bear Power', 3: 'Bull Power'}, 'levels': [0.0, 50.0, 100.0], 'description': ['Displays the concentration of bull power periods, bear power periods, and total periods when either bulls or bears had prevalence.', 'Supports two events for alerts:', '1. Bull/Bear Power == 100, which is a strong reversal signal.', '2. Bull/Bear Crossover, which is a strong trend signal.'], 'name': 'TotalPowerIndicator', 'source': 'MQL5 Indicators/Total Power Indicator MT5/TotalPowerIndicator.mq5', 'folder': 'Total Power Indicator MT5', 'inputs': [{'mql': 'Lookback_Period', 'py': 'Lookback_Period', 'param': 'Lookback_Period', 'type': 'int', 'default': 45, 'label': 'Lookback Period', 'sinput': False}, {'mql': 'Power_Period', 'py': 'Power_Period', 'param': 'Power_Period', 'type': 'int', 'default': 10, 'label': 'Power Period', 'sinput': False}, {'mql': 'AlertOn100Power', 'py': 'AlertOn100Power', 'param': 'AlertOn100Power', 'type': 'bool', 'default': False, 'label': 'Alert on 100 Power', 'sinput': False}, {'mql': 'AlertOnCrossover', 'py': 'AlertOnCrossover', 'param': 'AlertOnCrossover', 'type': 'bool', 'default': False, 'label': 'Alert on Crossover', 'sinput': False}, {'mql': 'EnableNativeAlerts', 'py': 'EnableNativeAlerts', 'param': 'EnableNativeAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnableEmailAlerts', 'py': 'EnableEmailAlerts', 'param': 'EnableEmailAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnablePushAlerts', 'py': 'EnablePushAlerts', 'param': 'EnablePushAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'TriggerCandle', 'py': 'TriggerCandle', 'param': 'TriggerCandle', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enum_candle_to_check
Current = 0
Previous = 1
_enum('enum_candle_to_check', {0: 'Current', 1: 'Previous'})

# ---- inputs and global variables
Lookback_Period = _input('Lookback_Period', 45)  # Lookback Period
Power_Period = _input('Power_Period', 10)  # Power Period
AlertOn100Power = _input('AlertOn100Power', False)  # Alert on 100 Power
AlertOnCrossover = _input('AlertOnCrossover', False)  # Alert on Crossover
EnableNativeAlerts = _input('EnableNativeAlerts', False)
EnableEmailAlerts = _input('EnableEmailAlerts', False)
EnablePushAlerts = _input('EnablePushAlerts', False)
TriggerCandle = _input('TriggerCandle', Previous)
Power = Arr(0, 0.0)
Bears = Arr(0, 0.0)
Bulls = Arr(0, 0.0)
BearB = Arr(0, 0.0)
BullB = Arr(0, 0.0)
myBear = 0
myBull = 0
LastAlertTime = 0

def OnInit():
    global myBear, myBull
    SetIndexBuffer(0, Power, INDICATOR_DATA)
    SetIndexBuffer(1, Bears, INDICATOR_DATA)
    SetIndexBuffer(2, Bulls, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Power_Period + Lookback_Period)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, Power_Period + Lookback_Period)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, Power_Period + Lookback_Period)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TPI (' + IntegerToString(Lookback_Period) + ', ' + IntegerToString(Power_Period) + ')')
    myBear = iBearsPower(None, 0, Power_Period)
    myBull = iBullsPower(None, 0, Power_Period)

def OnCalculate(rates_total, prev_calculated, Time, open, high, low, close, tickvolume, volume, spread):
    global LastAlertTime
    counted_bars = prev_calculated
    if rates_total < (Power_Period + Lookback_Period):
        return 0
    limit = counted_bars
    if limit < (Power_Period + Lookback_Period):
        limit = Power_Period + Lookback_Period
    for i in range(limit, rates_total):
        bearcount = 0
        bullcount = 0
        if CopyBuffer(myBear, 0, rates_total - i - 1, Lookback_Period, BearB) != Lookback_Period:
            return 0
        if CopyBuffer(myBull, 0, rates_total - i - 1, Lookback_Period, BullB) != Lookback_Period:
            return 0
        for j in range(Lookback_Period - 1, 0 - 1, -1):
            if BearB[j] < 0:
                bearcount += 1
            if BullB[j] > 0:
                bullcount += 1
        Power[i] = _idiv(MathAbs(bullcount - bearcount) * 100, Lookback_Period)
        Bears[i] = _idiv(bearcount * 100, Lookback_Period)
        Bulls[i] = _idiv(bullcount * 100, Lookback_Period)
    if (TriggerCandle > 0 and Time[rates_total - 1] > LastAlertTime) or TriggerCandle == 0:
        Text = ""
        if AlertOn100Power:
            if Bulls[rates_total - 1 - TriggerCandle] == 100 and Bulls[TriggerCandle + 1] < 100:
                Text = 'TPI: ' + Symbol() + ' - ' + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7) + ' - Bull Power = 100!'
                if EnableNativeAlerts:
                    Alert(Text)
                if EnableEmailAlerts:
                    SendMail('TPI Alert', Text)
                if EnablePushAlerts:
                    SendNotification(Text)
                LastAlertTime = Time[rates_total - 1]
            if Bears[rates_total - 1 - TriggerCandle] == 100 and Bears[TriggerCandle + 1] < 100:
                Text = 'TPI: ' + Symbol() + ' - ' + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7) + ' - Bear Power = 100!'
                if EnableNativeAlerts:
                    Alert(Text)
                if EnableEmailAlerts:
                    SendMail('TPI Alert', Text)
                if EnablePushAlerts:
                    SendNotification(Text)
                LastAlertTime = Time[rates_total - 1]
        if AlertOnCrossover:
            if Bulls[rates_total - 1 - TriggerCandle] > Bears[rates_total - 1 - TriggerCandle] and Bulls[rates_total - 2 - TriggerCandle] <= Bears[rates_total - 2 - TriggerCandle]:
                Text = 'TPI: ' + Symbol() + ' - ' + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7) + ' - Bull Power is now greater than Bear Power.'
                if EnableNativeAlerts:
                    Alert(Text)
                if EnableEmailAlerts:
                    SendMail('TPI Alert', Text)
                if EnablePushAlerts:
                    SendNotification(Text)
                LastAlertTime = Time[rates_total - 1]
            if Bulls[rates_total - 1 - TriggerCandle] < Bears[rates_total - 1 - TriggerCandle] and Bulls[rates_total - 2 - TriggerCandle] >= Bears[rates_total - 2 - TriggerCandle]:
                Text = 'TPI: ' + Symbol() + ' - ' + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7) + ' - Bear Power is now greater than Bull Power.'
                if EnableNativeAlerts:
                    Alert(Text)
                if EnableEmailAlerts:
                    SendMail('TPI Alert', Text)
                if EnablePushAlerts:
                    SendNotification(Text)
                LastAlertTime = Time[rates_total - 1]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TotalPowerIndicator(_MQL5Indicator):
    name = 'TotalPowerIndicator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Lookback_Period': 45,  # Lookback Period
        'Power_Period': 10,  # Power Period
        'AlertOn100Power': False,  # Alert on 100 Power
        'AlertOnCrossover': False,  # Alert on Crossover
        'EnableNativeAlerts': False,
        'EnableEmailAlerts': False,
        'EnablePushAlerts': False,
        'TriggerCandle': _Choice({0: 'Current', 1: 'Previous'}, default=1),
    }
    y_range = (-10.0, 110.0)

