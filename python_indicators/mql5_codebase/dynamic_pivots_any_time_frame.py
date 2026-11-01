"""Dynamic pivots (any time frame) — converted from MQL5: MQL5 Indicators/Dynamic pivots - any time frame/Dynamic pivots (any time frame).mq5

Copyright: © mladen, 2021; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2021', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 7}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'colors': {1: [3329330], 2: [3329330], 3: [3329330], 4: [6908265], 5: [5275647], 6: [5275647], 7: [5275647]}, 'widths': {}, 'styles': {4: 2}, 'labels': {1: 'Pivot high 3', 2: 'Pivot high 2', 3: 'Pivot high 1', 4: 'Pivot', 5: 'Pivot low 1', 6: 'Pivot low 2', 7: 'Pivot low 3'}, 'levels': [], 'description': [], 'name': 'Dynamic pivots (any time frame)', 'source': 'MQL5 Indicators/Dynamic pivots - any time frame/Dynamic pivots (any time frame).mq5', 'folder': 'Dynamic pivots - any time frame', 'inputs': [{'mql': 'inpTimeFrame', 'py': 'inpTimeFrame', 'param': 'inpTimeFrame', 'type': 'int', 'default': 16408, 'label': 'Time frame', 'sinput': False}, {'mql': 'inpPivotLevel1', 'py': 'inpPivotLevel1', 'param': 'inpPivotLevel1', 'type': 'double', 'default': 0.38, 'label': 'Pivot level 1', 'sinput': False}, {'mql': 'inpPivotLevel2', 'py': 'inpPivotLevel2', 'param': 'inpPivotLevel2', 'type': 'double', 'default': 0.61, 'label': 'Pivot level 2', 'sinput': False}, {'mql': 'inpPivotLevel3', 'py': 'inpPivotLevel3', 'param': 'inpPivotLevel3', 'type': 'double', 'default': 1.0, 'label': 'Pivot level 3', 'sinput': False}, {'mql': 'inpAlternativeCalculation', 'py': 'inpAlternativeCalculation', 'param': 'inpAlternativeCalculation', 'type': 'bool', 'default': True, 'label': 'Use alternative calculation?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpTimeFrame = _input('inpTimeFrame', PERIOD_D1)  # Time frame
inpPivotLevel1 = _input('inpPivotLevel1', 0.38)  # Pivot level 1
inpPivotLevel2 = _input('inpPivotLevel2', 0.61)  # Pivot level 2
inpPivotLevel3 = _input('inpPivotLevel3', 1.0)  # Pivot level 3
inpAlternativeCalculation = _input('inpAlternativeCalculation', True)  # Use alternative calculation?
ul3 = Arr(0, 0.0)
ul2 = Arr(0, 0.0)
ul1 = Arr(0, 0.0)
mid = Arr(0, 0.0)
dl1 = Arr(0, 0.0)
dl2 = Arr(0, 0.0)
dl3 = Arr(0, 0.0)

class sGlobalStruct(MqlObject):
    _q_fields = ('timeFrame', 'timeFrameSeconds', 'timeFrameOK')
    def __init__(self, *args):
        self.timeFrame = 0
        self.timeFrameSeconds = 0
        self.timeFrameOK = False

class sWorkStruct(MqlObject):
    _q_fields = ('max', 'min')
    def __init__(self, *args):
        self.max = 0.0
        self.min = 0.0

def OnInit():
    global_.timeFrame = MathMax(inpTimeFrame, Period())
    global_.timeFrameSeconds = PeriodSeconds(global_.timeFrame)
    global_.timeFrameOK = Period() < global_.timeFrame
    SetIndexBuffer(0, ul3, INDICATOR_DATA)
    SetIndexBuffer(1, ul2, INDICATOR_DATA)
    SetIndexBuffer(2, ul1, INDICATOR_DATA)
    SetIndexBuffer(3, mid, INDICATOR_DATA)
    SetIndexBuffer(4, dl1, INDICATOR_DATA)
    SetIndexBuffer(5, dl2, INDICATOR_DATA)
    SetIndexBuffer(6, dl3, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, StringSubstr(EnumToString(global_.timeFrame, 'ENUM_TIMEFRAMES'), 7) + ' Dynamic pivots')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_workSize
    if not global_.timeFrameOK:
        return 0
    limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    if _s_OnCalculate_m_workSize < rates_total:
        _s_OnCalculate_m_workSize = ArrayResize(_s_OnCalculate_m_work, rates_total + 500, 2000)
    for i in range(limit, rates_total):
        _timeNow = iTimeAdjust(global_.timeFrame, global_.timeFrameSeconds, time[i])
        _timePrev = (iTimeAdjust(global_.timeFrame, global_.timeFrameSeconds, time[i - 1]) if (i > 0) else -1)
        if _timeNow != _timePrev:
            _s_OnCalculate_m_work[i].max = high[i]
            _s_OnCalculate_m_work[i].min = low[i]
        else:
            _s_OnCalculate_m_work[i].max = (_s_OnCalculate_m_work[i - 1].max if (_s_OnCalculate_m_work[i - 1].max > high[i]) else high[i])
            _s_OnCalculate_m_work[i].min = (_s_OnCalculate_m_work[i - 1].min if (_s_OnCalculate_m_work[i - 1].min < low[i]) else low[i])
        range_ = _s_OnCalculate_m_work[i].max - _s_OnCalculate_m_work[i].min
        mid[i] = (_s_OnCalculate_m_work[i].max + _s_OnCalculate_m_work[i].min) / 2.0
        if inpAlternativeCalculation:
            ul3[i] = (_s_OnCalculate_m_work[i].max + mid[i]) / 2.0
            dl3[i] = (_s_OnCalculate_m_work[i].min + mid[i]) / 2.0
            if inpPivotLevel1 > 0:
                if inpPivotLevel1 > 0.5:
                    dl1[i] = EMPTY_VALUE
                    ul1[i] = _s_OnCalculate_m_work[i].min + (range_ * inpPivotLevel1)
                else:
                    ul1[i] = EMPTY_VALUE
                    dl1[i] = _s_OnCalculate_m_work[i].min + (range_ * inpPivotLevel1)
            if inpPivotLevel2 > 0:
                if inpPivotLevel2 > 0.5:
                    dl2[i] = EMPTY_VALUE
                    ul2[i] = _s_OnCalculate_m_work[i].min + (range_ * inpPivotLevel2)
                else:
                    ul1[i] = EMPTY_VALUE
                    dl2[i] = _s_OnCalculate_m_work[i].min + (range_ * inpPivotLevel2)
        else:
            if inpPivotLevel1 > 0:
                ul1[i] = mid[i] + (range_ * inpPivotLevel1)
                dl1[i] = mid[i] - (range_ * inpPivotLevel1)
            if inpPivotLevel2 > 0:
                ul2[i] = mid[i] + (range_ * inpPivotLevel2)
                dl2[i] = mid[i] - (range_ * inpPivotLevel2)
            if inpPivotLevel3 > 0:
                ul3[i] = mid[i] + (range_ * inpPivotLevel3)
                dl3[i] = mid[i] - (range_ * inpPivotLevel3)
    return rates_total

def iTimeAdjust(_timeFrame, _timeFrameSeconds, _time):
    if _timeFrame == PERIOD_W1:
        _adjustedTime = MqlDateTime()
        TimeToStruct(_time, _adjustedTime)
        _adjustedTime.sec = 0
        _adjustedTime.min = 0
        _adjustedTime.hour = 0
        _time = StructToTime(_adjustedTime)
        return _time - (_adjustedTime.day_of_week * 86400)
    if _timeFrame == PERIOD_MN1:
        _adjustedTime = MqlDateTime()
        TimeToStruct(_time, _adjustedTime)
        _adjustedTime.sec = 0
        _adjustedTime.min = 0
        _adjustedTime.hour = 0
        _adjustedTime.day = 1
        _time = StructToTime(_adjustedTime)
        return _time
    return _int(_idiv(_time, _timeFrameSeconds)) * _timeFrameSeconds

# ---- global variables initialised from expressions
global_ = _alloc(sGlobalStruct)
global_.__init__()

# ---- static local variables
_s_OnCalculate_m_work = Arr(0, 0, factory=sWorkStruct)
_s_OnCalculate_m_workSize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DynamicPivotsAnyTimeFrame(_MQL5Indicator):
    name = 'Dynamic pivots (any time frame)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Time frame
        'inpPivotLevel1': 0.38,  # Pivot level 1
        'inpPivotLevel2': 0.61,  # Pivot level 2
        'inpPivotLevel3': 1.0,  # Pivot level 3
        'inpAlternativeCalculation': True,  # Use alternative calculation?
    }

