"""pivotpointuniversal — converted from MQL5: MQL5 Indicators/PivotPointUniversal/pivotpointuniversal.mq5

Classical pivot levels.
Copyright: VDV Soft; Link: vdv_2001@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'VDV Soft', 'link': 'vdv_2001@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}, 'colors': {1: [42495], 2: [8388736], 3: [8388736], 4: [16748574], 5: [16748574], 6: [25600], 7: [25600], 8: [25600], 9: [25600]}, 'widths': {1: 2, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1}, 'styles': {1: 2, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 'labels': {1: 'Pivot', 2: 'S1', 3: 'R1', 4: 'S2', 5: 'R2', 6: 'S3', 7: 'R3', 8: 'S4', 9: 'R4'}, 'levels': [], 'description': ['Classical pivot levels.'], 'name': 'pivotpointuniversal', 'source': 'MQL5 Indicators/PivotPointUniversal/pivotpointuniversal.mq5', 'folder': 'PivotPointUniversal', 'inputs': [{'mql': 'InpPivotType', 'py': 'InpPivotType', 'param': 'InpPivotType', 'type': 'int', 'default': 0, 'label': 'Pivot type', 'sinput': False}, {'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'int', 'default': 0, 'label': 'Period', 'sinput': False}, {'mql': 'InpTime', 'py': 'InpTime', 'param': 'InpTime', 'type': 'int', 'default': 0, 'label': 'Time', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum PivotType
PIVOT_CLASSIC = 0
PIVOT_FIBONACCI = 1
PIVOT_DEMARK = 2
PIVOT_CAMARILLA = 3
PIVOT_WOODIES = 4
_enum('PivotType', {0: 'PIVOT_CLASSIC', 1: 'PIVOT_FIBONACCI', 2: 'PIVOT_DEMARK', 3: 'PIVOT_CAMARILLA', 4: 'PIVOT_WOODIES'})

# enum inptime
TIME_TRADE_SERVER = 0
TIME_GMT = 1
_enum('inptime', {0: 'TIME_TRADE_SERVER', 1: 'TIME_GMT'})

# enum inpperiod
DAY = 0
WEEKLY = 1
MONTHLY = 2
_enum('inpperiod', {0: 'DAY', 1: 'WEEKLY', 2: 'MONTHLY'})

# ---- inputs and global variables
InpPivotType = _input('InpPivotType', PIVOT_CLASSIC)  # Pivot type
InpPeriod = _input('InpPeriod', DAY)  # Period
InpTime = _input('InpTime', TIME_TRADE_SERVER)  # Time
PBuffer = Arr(0, 0.0)
S1Buffer = Arr(0, 0.0)
R1Buffer = Arr(0, 0.0)
S2Buffer = Arr(0, 0.0)
R2Buffer = Arr(0, 0.0)
S3Buffer = Arr(0, 0.0)
R3Buffer = Arr(0, 0.0)
S4Buffer = Arr(0, 0.0)
R4Buffer = Arr(0, 0.0)
ShiftTime = 0  # Displacement of the buffer for construction of levels in the future

def OnInit():
    global ShiftTime
    period = ""
    shiftGMT = ' TRADE SERVER '
    _sw1 = InpPeriod
    if _sw1 == DAY:
        if PeriodSeconds(Period()) >= PeriodSeconds(PERIOD_H2):
            return -1
        period = '(DAY)'
        shiftGMT = (' GMT ' if (InpTime == TIME_GMT) else ' TRADE SERVER ')
        ShiftTime = _int(_idiv(TimeTradeServer() - TimeGMT(), PeriodSeconds(Period()))) + _idiv(PeriodSeconds(PERIOD_D1), PeriodSeconds(Period()))
    elif _sw1 == WEEKLY:
        if PeriodSeconds(Period()) >= PeriodSeconds(PERIOD_D1):
            return -1
        period = '(WEEKLY)'
        ShiftTime = _int(_idiv(TimeTradeServer() - TimeGMT(), PeriodSeconds(Period()))) + _idiv(PeriodSeconds(PERIOD_W1), PeriodSeconds(Period()))
    elif _sw1 == MONTHLY:
        if PeriodSeconds(Period()) >= PeriodSeconds(PERIOD_MN1):
            return -1
        period = '(MONTHLY)'
        ShiftTime = _int(_idiv(TimeTradeServer() - TimeGMT(), PeriodSeconds(Period()))) + _idiv(PeriodSeconds(PERIOD_MN1), PeriodSeconds(Period()))
    IndicatorSetString(INDICATOR_SHORTNAME, 'PivotPoint' + period + shiftGMT + 'time')
    SetIndexBuffer(0, PBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, S1Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, R1Buffer, INDICATOR_DATA)
    SetIndexBuffer(3, S2Buffer, INDICATOR_DATA)
    SetIndexBuffer(4, R2Buffer, INDICATOR_DATA)
    SetIndexBuffer(5, S3Buffer, INDICATOR_DATA)
    SetIndexBuffer(6, R3Buffer, INDICATOR_DATA)
    SetIndexBuffer(7, S4Buffer, INDICATOR_DATA)
    SetIndexBuffer(8, R4Buffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    for i in range(0, 9):
        PlotIndexSetInteger(i, PLOT_SHIFT, ShiftTime)
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 1
    time1 = MqlDateTime()
    time2 = MqlDateTime()
    if prev_calculated == 0:
        i = ShiftTime + 1
        ArrayInitialize(PBuffer, EMPTY_VALUE)
        ArrayInitialize(S1Buffer, EMPTY_VALUE)
        ArrayInitialize(R1Buffer, EMPTY_VALUE)
        ArrayInitialize(S2Buffer, EMPTY_VALUE)
        ArrayInitialize(R2Buffer, EMPTY_VALUE)
        ArrayInitialize(S3Buffer, EMPTY_VALUE)
        ArrayInitialize(R3Buffer, EMPTY_VALUE)
    else:
        i = prev_calculated - 1
    while i < rates_total:
        TimeToStruct(time[i - 1], time1)
        TimeToStruct(time[i], time2)
        _sw2 = InpPeriod
        if _sw2 == DAY:
            if time1.day != time2.day:
                time1.hour = 0
                time1.min = 0
                time1.sec = 0
                time2.hour = 0
                time2.min = 0
                time2.sec = 0
                DrawPivotLevel(StructToTime(time1), StructToTime(time2), i)
        elif _sw2 == WEEKLY:
            if time1.day_of_week != time2.day_of_week and time2.day_of_week == 1:
                time2.hour = 0
                time2.min = 0
                time2.sec = 0
                work = StructToTime(time2)
                DrawPivotLevel(work - PeriodSeconds(PERIOD_W1), work, i)
        elif _sw2 == MONTHLY:
            if time1.mon != time2.mon:
                time2.day = 1
                time1.day = time2.day
                time2.hour = 0
                time1.hour = time2.hour
                time2.min = 0
                time1.min = time2.min
                time2.sec = 0
                time1.sec = time2.sec
                DrawPivotLevel(StructToTime(time1), StructToTime(time2), i)
        i += 1
    return rates_total

def DrawPivotLevel(Previous, Current, Index):
    rates_total = 0
    shift = 0
    shift_end = 0
    range_ = 0.0
    pivot = 0.0
    support1 = 0.0
    support2 = 0.0
    support3 = 0.0
    support4 = 0.0
    resistance1 = 0.0
    resistance2 = 0.0
    resistance3 = 0.0
    resistance4 = 0.0
    iHigh_ = Arr(0, 0.0)
    iLow_ = Arr(0, 0.0)
    iClose_ = Arr(0, 0.0)
    iOpen_ = Arr(0, 0.0)
    HighDay = 0.0
    LowDay = 0.0
    CloseDay = 0.0
    OpenDay = 0.0
    shiftGMT = 0
    _sw3 = InpPeriod
    if _sw3 == DAY:
        shift_end = _idiv(PeriodSeconds(PERIOD_D1), PeriodSeconds(Period()))
        if InpTime == TIME_GMT:
            shiftGMT = TimeTradeServer() - TimeGMT()
    elif _sw3 == WEEKLY:
        shift_end = _idiv(PeriodSeconds(PERIOD_W1), PeriodSeconds(Period()))
    elif _sw3 == MONTHLY:
        shift_end = _idiv(PeriodSeconds(PERIOD_MN1), PeriodSeconds(Period()))
    _start = Previous + shiftGMT
    _end = Current + shiftGMT - 1
    rates_total = CopyHigh(None, Period(), _DT(_start), _DT(_end), iHigh_)
    if rates_total <= 0:
        return
    else:
        HighDay = iHigh_[ArrayMaximum(iHigh_, 0, rates_total)]
    rates_total = CopyLow(None, Period(), _DT(_start), _DT(_end), iLow_)
    if rates_total <= 0:
        return
    else:
        LowDay = iLow_[ArrayMinimum(iLow_, 0, rates_total)]
    rates_total = CopyClose(None, Period(), _DT(_end), 1, iClose_)
    if rates_total <= 0:
        return
    else:
        CloseDay = iClose_[0]
    rates_total = CopyOpen(None, Period(), _end + 1, 1, iOpen_)
    if rates_total <= 0:
        return
    else:
        OpenDay = iOpen_[0]
    _sw4 = InpPivotType
    if _sw4 == PIVOT_CLASSIC:
        pivot = (CloseDay + HighDay + LowDay) / 3
        support1 = (2 * pivot) - HighDay
        support2 = pivot - (HighDay - LowDay)
        support3 = (2 * pivot) - ((2 * HighDay) - LowDay)
        support4 = EMPTY_VALUE
        resistance1 = (2 * pivot) - LowDay
        resistance2 = pivot + (HighDay - LowDay)
        resistance3 = (2 * pivot) + (HighDay - (2 * LowDay))
        resistance4 = EMPTY_VALUE
    elif _sw4 == PIVOT_FIBONACCI:
        range_ = HighDay - LowDay
        pivot = (CloseDay + HighDay + LowDay) / 3
        support1 = pivot - (0.382 * range_)
        support2 = pivot - (0.618 * range_)
        support3 = pivot - range_
        support4 = EMPTY_VALUE
        resistance1 = pivot + (0.382 * range_)
        resistance2 = pivot + (0.618 * range_)
        resistance3 = pivot + range_
        resistance4 = EMPTY_VALUE
    elif _sw4 == PIVOT_DEMARK:
        if CloseDay < OpenDay:
            pivot = HighDay + (2 * LowDay) + CloseDay
        if CloseDay > OpenDay:
            pivot = (2 * HighDay) + LowDay + CloseDay
        if CloseDay == OpenDay:
            pivot = HighDay + LowDay + (2 * CloseDay)
        support1 = (pivot / 2) - HighDay
        resistance1 = (pivot / 2) - LowDay
        pivot = EMPTY_VALUE
        support2 = EMPTY_VALUE
        support3 = EMPTY_VALUE
        support4 = EMPTY_VALUE
        resistance2 = EMPTY_VALUE
        resistance3 = EMPTY_VALUE
        resistance4 = EMPTY_VALUE
    elif _sw4 == PIVOT_CAMARILLA:
        range_ = HighDay - LowDay
        pivot = EMPTY_VALUE
        support1 = CloseDay - ((range_ * 1.1) / 12)
        support2 = CloseDay - ((range_ * 1.1) / 6)
        support3 = CloseDay - ((range_ * 1.1) / 4)
        support4 = CloseDay - ((range_ * 1.1) / 2)
        resistance1 = ((range_ * 1.1) / 12) + CloseDay
        resistance2 = ((range_ * 1.1) / 6) + CloseDay
        resistance3 = ((range_ * 1.1) / 4) + CloseDay
        resistance4 = ((range_ * 1.1) / 2) + CloseDay
    elif _sw4 == PIVOT_WOODIES:
        range_ = HighDay - LowDay
        pivot = (HighDay + LowDay + (2 * CloseDay)) / 4
        support1 = (2 * pivot) - HighDay
        support2 = pivot - HighDay + LowDay
        support3 = EMPTY_VALUE
        support4 = EMPTY_VALUE
        resistance1 = (2 * pivot) - LowDay
        resistance2 = pivot + HighDay - LowDay
        resistance3 = EMPTY_VALUE
        resistance4 = EMPTY_VALUE
    shift = Index - ShiftTime + _int(_idiv(shiftGMT, PeriodSeconds(Period())))
    for i in range(0, shift_end + 1):
        PBuffer[shift + i] = pivot
        S1Buffer[shift + i] = support1
        S2Buffer[shift + i] = support2
        S3Buffer[shift + i] = support3
        S4Buffer[shift + i] = support4
        R1Buffer[shift + i] = resistance1
        R2Buffer[shift + i] = resistance2
        R3Buffer[shift + i] = resistance3
        R4Buffer[shift + i] = resistance4

def LineY(Index, StartY, EndY, StartX, EndX):
    LINH = _fdiv(StartY * (Index - EndX), StartX - EndX) + _fdiv(EndY * (Index - StartX), EndX - StartX)
    return LINH


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Pivotpointuniversal(_MQL5Indicator):
    name = 'pivotpointuniversal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPivotType': _Choice({0: 'PIVOT_CLASSIC', 1: 'PIVOT_FIBONACCI', 2: 'PIVOT_DEMARK', 3: 'PIVOT_CAMARILLA', 4: 'PIVOT_WOODIES'}, default=0),  # Pivot type
        'InpPeriod': _Choice({0: 'DAY', 1: 'WEEKLY', 2: 'MONTHLY'}, default=0),  # Period
        'InpTime': _Choice({0: 'TIME_TRADE_SERVER', 1: 'TIME_GMT'}, default=0),  # Time
    }

