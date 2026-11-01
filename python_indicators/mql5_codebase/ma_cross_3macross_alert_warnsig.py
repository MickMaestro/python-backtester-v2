"""MA Cross 3MACross Alert WarnSig — converted from MQL5: MQL5 Indicators/MA Cross 3MACross Alert WarnSig/MA Cross 3MACross Alert WarnSig.mq5

Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'version': '1.000', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [16711680], 2: [255], 3: [65535], 4: [55295]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {}, 'labels': {1: 'Cross Up', 2: 'Cross Down', 3: 'Cross Ghost Up', 4: 'Cross Ghost Down'}, 'levels': [], 'description': [], 'name': 'MA Cross 3MACross Alert WarnSig', 'source': 'MQL5 Indicators/MA Cross 3MACross Alert WarnSig/MA Cross 3MACross Alert WarnSig.mq5', 'folder': 'MA Cross 3MACross Alert WarnSig', 'inputs': [{'mql': '_0_', 'py': '_0_', 'param': None, 'type': 'string', 'default': 'Parameters of the first Moving Average', 'label': '', 'sinput': True}, {'mql': 'InpMAPeriodFirst', 'py': 'InpMAPeriodFirst', 'param': 'InpMAPeriodFirst', 'type': 'int', 'default': 5, 'label': 'Period of the first Moving Average', 'sinput': False}, {'mql': 'InpMAShiftFirst', 'py': 'InpMAShiftFirst', 'param': 'InpMAShiftFirst', 'type': 'int', 'default': 0, 'label': 'Shift of the first Moving Average', 'sinput': False}, {'mql': 'InpMAMethodFirst', 'py': 'InpMAMethodFirst', 'param': 'InpMAMethodFirst', 'type': 'int', 'default': 2, 'label': 'Method of the first Moving Average', 'sinput': False}, {'mql': '_1_', 'py': '_1_', 'param': None, 'type': 'string', 'default': 'Parameters of the second Moving Average', 'label': '', 'sinput': True}, {'mql': 'InpMAPeriodSecond', 'py': 'InpMAPeriodSecond', 'param': 'InpMAPeriodSecond', 'type': 'int', 'default': 13, 'label': 'Period of the second Moving Average', 'sinput': False}, {'mql': 'InpMAShiftSecond', 'py': 'InpMAShiftSecond', 'param': 'InpMAShiftSecond', 'type': 'int', 'default': 0, 'label': 'Shift of the second Moving Average', 'sinput': False}, {'mql': 'InpMAMethodSecond', 'py': 'InpMAMethodSecond', 'param': 'InpMAMethodSecond', 'type': 'int', 'default': 2, 'label': 'Method of the second Moving Average', 'sinput': False}, {'mql': '_2_', 'py': '_2_', 'param': None, 'type': 'string', 'default': 'Parameters of the Third Moving Average', 'label': '', 'sinput': True}, {'mql': 'InpMAPeriodThird', 'py': 'InpMAPeriodThird', 'param': 'InpMAPeriodThird', 'type': 'int', 'default': 34, 'label': 'Period of the third Moving Average', 'sinput': False}, {'mql': 'InpMAShiftThird', 'py': 'InpMAShiftThird', 'param': 'InpMAShiftThird', 'type': 'int', 'default': 0, 'label': 'Shift of the third Moving Average', 'sinput': False}, {'mql': 'InpMAMethodThird', 'py': 'InpMAMethodThird', 'param': 'InpMAMethodThird', 'type': 'int', 'default': 2, 'label': 'Method of the third Moving Average', 'sinput': False}, {'mql': 'crossesOnCurrent', 'py': 'crossesOnCurrent', 'param': 'crossesOnCurrent', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'alertsOn', 'py': 'alertsOn', 'param': 'alertsOn', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'alertsMessage', 'py': 'alertsMessage', 'param': 'alertsMessage', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'alertsSound', 'py': 'alertsSound', 'param': 'alertsSound', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'alertsEmail', 'py': 'alertsEmail', 'param': 'alertsEmail', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
_0_ = _input('_0_', 'Parameters of the first Moving Average')
InpMAPeriodFirst = _input('InpMAPeriodFirst', 5)  # Period of the first Moving Average
InpMAShiftFirst = _input('InpMAShiftFirst', 0)  # Shift of the first Moving Average
InpMAMethodFirst = _input('InpMAMethodFirst', MODE_SMMA)  # Method of the first Moving Average
_1_ = _input('_1_', 'Parameters of the second Moving Average')
InpMAPeriodSecond = _input('InpMAPeriodSecond', 13)  # Period of the second Moving Average
InpMAShiftSecond = _input('InpMAShiftSecond', 0)  # Shift of the second Moving Average
InpMAMethodSecond = _input('InpMAMethodSecond', MODE_SMMA)  # Method of the second Moving Average
_2_ = _input('_2_', 'Parameters of the Third Moving Average')
InpMAPeriodThird = _input('InpMAPeriodThird', 34)  # Period of the third Moving Average
InpMAShiftThird = _input('InpMAShiftThird', 0)  # Shift of the third Moving Average
InpMAMethodThird = _input('InpMAMethodThird', MODE_SMMA)  # Method of the third Moving Average
crossesOnCurrent = _input('crossesOnCurrent', True)
alertsOn = _input('alertsOn', True)
alertsMessage = _input('alertsMessage', True)
alertsSound = _input('alertsSound', False)
alertsEmail = _input('alertsEmail', False)
handle_iMA_First = 0  # variable for storing the handle of the iMA indicator
handle_iMA_Second = 0  # variable for storing the handle of the iMA indicator
handle_iMA_Third = 0  # variable for storing the handle of the iMA indicator
CrossUp = Arr(0, 0.0)
CrossDown = Arr(0, 0.0)
CrossGhostUp = Arr(0, 0.0)
CrossGhostDown = Arr(0, 0.0)

def OnInit():
    global handle_iMA_First, handle_iMA_Second, handle_iMA_Third
    if InpMAPeriodFirst <= 0:
        Print('The "Period of the first Moving Average" parameter can\'t be less or is equal to zero')
        return INIT_PARAMETERS_INCORRECT
    if InpMAPeriodSecond <= 0:
        Print('The "Period of the second Moving Average" parameter can\'t be less or is equal to zero')
        return INIT_PARAMETERS_INCORRECT
    if InpMAPeriodThird <= 0:
        Print('The "Period of the third Moving Average" parameter can\'t be less or is equal to zero')
        return INIT_PARAMETERS_INCORRECT
    if InpMAPeriodFirst >= InpMAPeriodSecond:
        Print('Parameter "Period of the first Moving Average" can\'t be more or is equal to a paramter of "Period of the second Moving Average"')
        return INIT_PARAMETERS_INCORRECT
    if InpMAPeriodSecond >= InpMAPeriodThird:
        Print('Parameter "Period of the second Moving Averagee" can\'t be more or is equal to a paramter of "Period of the third Moving Average"')
        return INIT_PARAMETERS_INCORRECT
    handle_iMA_First = iMA(Symbol(), Period(), InpMAPeriodFirst, InpMAShiftFirst, InpMAMethodFirst, PRICE_CLOSE)
    if handle_iMA_First == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMA indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        return INIT_FAILED
    handle_iMA_Second = iMA(Symbol(), Period(), InpMAPeriodSecond, InpMAShiftSecond, InpMAMethodSecond, PRICE_CLOSE)
    if handle_iMA_Second == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMA indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        return INIT_FAILED
    handle_iMA_Third = iMA(Symbol(), Period(), InpMAPeriodThird, InpMAShiftThird, InpMAMethodThird, PRICE_CLOSE)
    if handle_iMA_Third == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMA indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        return INIT_FAILED
    SetIndexBuffer(0, CrossUp, INDICATOR_DATA)
    SetIndexBuffer(1, CrossDown, INDICATOR_DATA)
    SetIndexBuffer(2, CrossGhostUp, INDICATOR_DATA)
    SetIndexBuffer(3, CrossGhostDown, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 241)
    PlotIndexSetInteger(1, PLOT_ARROW, 242)
    PlotIndexSetInteger(2, PLOT_ARROW, 241)
    PlotIndexSetInteger(3, PLOT_ARROW, 242)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, 5)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, -5)
    PlotIndexSetInteger(2, PLOT_ARROW_SHIFT, 5)
    PlotIndexSetInteger(3, PLOT_ARROW_SHIFT, -5)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(CrossUp, True)
    ArraySetAsSeries(CrossDown, True)
    ArraySetAsSeries(CrossGhostUp, True)
    ArraySetAsSeries(CrossGhostDown, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 10 or rates_total < InpMAPeriodThird:
        return 0
    limit = rates_total - prev_calculated + 1
    if prev_calculated == 0:
        limit = rates_total - 1
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    for i in range(limit, 0 - 1, -1):
        First = Arr(0, 0.0)
        Second = Arr(0, 0.0)
        Third = Arr(0, 0.0)
        ArraySetAsSeries(First, True)
        ArraySetAsSeries(Second, True)
        ArraySetAsSeries(Third, True)
        buffer_num = 0
        start_pos = i
        count = 2
        get_first = True
        get_second = True
        get_third = True
        get_first = iMAGet(handle_iMA_First, buffer_num, start_pos, count, First)
        get_second = iMAGet(handle_iMA_Second, buffer_num, start_pos, count, Second)
        get_third = iMAGet(handle_iMA_Third, buffer_num, start_pos, count, Third)
        if ((not get_first) or (not get_second)) or (not get_third):
            continue
        Range = 0.0
        counter = i - 9
        counter = (0 if (counter < 0) else counter)
        for j in range(counter, i + 1):
            Range += MathAbs(high[j] - low[j])
        Range = Range / 10.0
        if crossesOnCurrent == False and i == 0:
            continue
        crossID = 0
        curr = 0.0
        prev = 0.0
        point = 0.0
        while True:
            curr = First[0] - Second[0]
            prev = First[1] - Second[1]
            point = (First[0] + First[1]) / 2
            if (curr * prev) <= 0:
                crossID = 1
                break
            curr = First[0] - Third[0]
            prev = First[1] - Third[1]
            if (curr * prev) <= 0:
                crossID = 2
                break
            curr = Second[0] - Third[0]
            prev = Second[1] - Third[1]
            point = (Second[0] + Second[1]) / 2
            if (curr * prev) <= 0:
                crossID = 3
                break
            break
        CrossUp[i] = EMPTY_VALUE
        CrossDown[i] = EMPTY_VALUE
        CrossGhostUp[i] = EMPTY_VALUE
        CrossGhostDown[i] = EMPTY_VALUE
        if crossID > 0:
            if alertsOn:
                curr_norm = NormalizeDouble(curr, Digits())
                if (i == 0 and crossesOnCurrent == True) or (i == 1 and crossesOnCurrent == False):
                    _sw1 = crossID
                    if _sw1 == 1:
                        if curr_norm > 0.0:
                            doAlert(' 3MACross: "First MA" crossed "Second MA" UP', time[i], close[i])
                        elif curr_norm < 0.0:
                            doAlert(' 3MACross: "First MA" crossed "Second MA" DOWN', time[i], close[i])
                    elif _sw1 == 2:
                        if curr_norm > 0.0:
                            doAlert(' 3MACross: "First MA" crossed "Third MA" UP', time[i], close[i])
                        elif curr_norm < 0.0:
                            doAlert(' 3MACross: "First MA" crossed "Third MA" DOWN', time[i], close[i])
                    elif _sw1 == 3:
                        if curr_norm > 0.0:
                            doAlert(' 3MACross: "Second MA" crossed "Third MA" UP', time[i], close[i])
                        elif curr_norm < 0.0:
                            doAlert(' 3MACross: "Second MA" crossed "Third MA" DOWN', time[i], close[i])
                if i == 0:
                    if curr_norm > 0.0:
                        CrossGhostUp[i] = point - (Range * 0.5)
                    elif curr_norm < 0.0:
                        CrossGhostDown[i] = point + (Range * 0.5)
                else:
                    if curr_norm > 0.0:
                        CrossUp[i] = point - (Range * 0.5)
                    elif curr_norm < 0.0:
                        CrossDown[i] = point + (Range * 0.5)
    return rates_total

def iMAGet(handle_iMA, buffer_num, start_pos, count, buffer):
    ResetLastError()
    if CopyBuffer(handle_iMA, buffer_num, start_pos, count, buffer) != count:
        PrintFormat('Failed to copy data from the iMA indicator, error code %d', GetLastError())
        return False
    return True

def doAlert(doWhat, time_last_bar, close):
    global _s_doAlert_previousAlert, _s_doAlert_previousTime
    message = ""
    if _s_doAlert_previousAlert != doWhat or _s_doAlert_previousTime != time_last_bar:
        _s_doAlert_previousAlert = doWhat
        _s_doAlert_previousTime = time_last_bar
        message = Symbol() + ' at ' + DoubleToString(close, Digits()) + ' ' + doWhat
        if alertsMessage:
            Alert(message)
        if alertsEmail:
            SendMail(Symbol() + ' 3MACross:' + ' M' + EnumToString(Period(), ''), message)
        if alertsSound:
            PlaySound('alert2.wav')

# ---- static local variables
_s_doAlert_previousAlert = 'nothing'
_s_doAlert_previousTime = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MACross3MACrossAlertWarnSig(_MQL5Indicator):
    name = 'MA Cross 3MACross Alert WarnSig'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMAPeriodFirst': 5,  # Period of the first Moving Average
        'InpMAShiftFirst': 0,  # Shift of the first Moving Average
        'InpMAMethodFirst': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # Method of the first Moving Average
        'InpMAPeriodSecond': 13,  # Period of the second Moving Average
        'InpMAShiftSecond': 0,  # Shift of the second Moving Average
        'InpMAMethodSecond': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # Method of the second Moving Average
        'InpMAPeriodThird': 34,  # Period of the third Moving Average
        'InpMAShiftThird': 0,  # Shift of the third Moving Average
        'InpMAMethodThird': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # Method of the third Moving Average
        'crossesOnCurrent': True,
        'alertsOn': True,
        'alertsMessage': True,
        'alertsSound': False,
        'alertsEmail': False,
    }

