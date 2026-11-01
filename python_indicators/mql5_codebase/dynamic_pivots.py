"""Dynamic pivots — converted from MQL5: MQL5 Indicators/Dynamic Pivots/Dynamic pivots.mq5

Dynamic pivots
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 7}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'colors': {1: [16760576], 2: [16760576], 3: [16760576], 4: [6908265], 5: [255], 6: [255], 7: [255]}, 'widths': {}, 'styles': {4: 2}, 'labels': {1: 'Pivot high 3', 2: 'Pivot high 2', 3: 'Pivot high 1', 4: 'Pivot', 5: 'Pivot low 1', 6: 'Pivot low 2', 7: 'Pivot low 3'}, 'levels': [], 'description': ['Dynamic pivots'], 'name': 'Dynamic pivots', 'source': 'MQL5 Indicators/Dynamic Pivots/Dynamic pivots.mq5', 'folder': 'Dynamic Pivots', 'inputs': [{'mql': 'PivotLevel1', 'py': 'PivotLevel1', 'param': 'PivotLevel1', 'type': 'double', 'default': 0.38, 'label': 'Pivot level 1', 'sinput': False}, {'mql': 'PivotLevel2', 'py': 'PivotLevel2', 'param': 'PivotLevel2', 'type': 'double', 'default': 0.61, 'label': 'Pivot level 2', 'sinput': False}, {'mql': 'PivotLevel3', 'py': 'PivotLevel3', 'param': 'PivotLevel3', 'type': 'double', 'default': 1.0, 'label': 'Pivot level 3', 'sinput': False}, {'mql': 'AlternativeCalculation', 'py': 'AlternativeCalculation', 'param': 'AlternativeCalculation', 'type': 'bool', 'default': True, 'label': 'Use alternative calculation?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PivotLevel1 = _input('PivotLevel1', 0.38)  # Pivot level 1
PivotLevel2 = _input('PivotLevel2', 0.61)  # Pivot level 2
PivotLevel3 = _input('PivotLevel3', 1.0)  # Pivot level 3
AlternativeCalculation = _input('AlternativeCalculation', True)  # Use alternative calculation?
ul3 = Arr(0, 0.0)
ul2 = Arr(0, 0.0)
ul1 = Arr(0, 0.0)
mid = Arr(0, 0.0)
dl1 = Arr(0, 0.0)
dl2 = Arr(0, 0.0)
dl3 = Arr(0, 0.0)
counter = Arr(0, 0.0)

def OnInit():
    if Period() >= PERIOD_D1:
        Alert('Indicator will work only on time frames less than daily')
        return INIT_FAILED
    SetIndexBuffer(0, ul3, INDICATOR_DATA)
    SetIndexBuffer(1, ul2, INDICATOR_DATA)
    SetIndexBuffer(2, ul1, INDICATOR_DATA)
    SetIndexBuffer(3, mid, INDICATOR_DATA)
    SetIndexBuffer(4, dl1, INDICATOR_DATA)
    SetIndexBuffer(5, dl2, INDICATOR_DATA)
    SetIndexBuffer(6, dl3, INDICATOR_DATA)
    SetIndexBuffer(7, counter, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Dynamic pivots')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    _divisor = PeriodSeconds(PERIOD_D1)
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        counter[i] = ((counter[i - 1] if (_idiv(time[i], _divisor) == _idiv(time[i - 1], _divisor)) else i) if (i > 0) else 0)
        _start = _int(counter[i])
        dayHigh = high[ArrayMaximum(high, _start, i - _start + 1)]
        dayLow = low[ArrayMinimum(low, _start, i - _start + 1)]
        range_ = dayHigh - dayLow
        mid[i] = (dayHigh + dayLow) / 2.0
        if AlternativeCalculation:
            ul3[i] = (dayHigh + mid[i]) / 2.0
            dl3[i] = (dayLow + mid[i]) / 2.0
            if PivotLevel1 > 0:
                if PivotLevel1 > 0.5:
                    dl1[i] = EMPTY_VALUE
                    ul1[i] = dayLow + (range_ * PivotLevel1)
                else:
                    ul1[i] = EMPTY_VALUE
                    dl1[i] = dayLow + (range_ * PivotLevel1)
            if PivotLevel2 > 0:
                if PivotLevel2 > 0.5:
                    dl2[i] = EMPTY_VALUE
                    ul2[i] = dayLow + (range_ * PivotLevel2)
                else:
                    ul1[i] = EMPTY_VALUE
                    dl2[i] = dayLow + (range_ * PivotLevel2)
        else:
            if PivotLevel1 > 0:
                ul1[i] = mid[i] + (range_ * PivotLevel1)
                dl1[i] = mid[i] - (range_ * PivotLevel1)
            if PivotLevel2 > 0:
                ul2[i] = mid[i] + (range_ * PivotLevel2)
                dl2[i] = mid[i] - (range_ * PivotLevel2)
            if PivotLevel3 > 0:
                ul3[i] = mid[i] + (range_ * PivotLevel3)
                dl3[i] = mid[i] - (range_ * PivotLevel3)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DynamicPivots(_MQL5Indicator):
    name = 'Dynamic pivots'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PivotLevel1': 0.38,  # Pivot level 1
        'PivotLevel2': 0.61,  # Pivot level 2
        'PivotLevel3': 1.0,  # Pivot level 3
        'AlternativeCalculation': True,  # Use alternative calculation?
    }

