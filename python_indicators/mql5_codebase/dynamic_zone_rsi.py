"""Dynamic_Zone_RSI — converted from MQL5: MQL5 Indicators/Dynamic_Zone_RSI/Dynamic_Zone_RSI.mq5

Dynamic Zone RSI oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 5, 6: 5}, 'colors': {1: [16711680], 2: [255], 3: [3329330], 4: [255], 5: [16711680], 6: [255]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 2, 6: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'RSI', 2: 'Top', 3: 'Middle', 4: 'Bottom', 5: 'Intersection up', 6: 'Intersection down'}, 'levels': [], 'description': ['Dynamic Zone RSI oscillator'], 'name': 'Dynamic_Zone_RSI', 'source': 'MQL5 Indicators/Dynamic_Zone_RSI/Dynamic_Zone_RSI.mq5', 'folder': 'Dynamic_Zone_RSI', 'inputs': [{'mql': 'InpPeriodRSI', 'py': 'InpPeriodRSI', 'param': 'InpPeriodRSI', 'type': 'uint', 'default': 5, 'label': 'RSI period', 'sinput': False}, {'mql': 'InpPeriodBB', 'py': 'InpPeriodBB', 'param': 'InpPeriodBB', 'type': 'uint', 'default': 30, 'label': 'Bands period', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 1.3185, 'label': 'Deviation', 'sinput': False}, {'mql': 'InpShowArrows', 'py': 'InpShowArrows', 'param': 'InpShowArrows', 'type': 'int', 'default': 1, 'label': 'Show intersection arrows', 'sinput': False}, {'mql': 'InpUseMiddle', 'py': 'InpUseMiddle', 'param': 'InpUseMiddle', 'type': 'int', 'default': 0, 'label': 'Allow midline intersections', 'sinput': False}, {'mql': 'InpUseAlerts', 'py': 'InpUseAlerts', 'param': 'InpUseAlerts', 'type': 'int', 'default': 0, 'label': 'Use alerts', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodRSI = _input('InpPeriodRSI', 5)  # RSI period
InpPeriodBB = _input('InpPeriodBB', 30)  # Bands period
InpDeviation = _input('InpDeviation', 1.3185)  # Deviation
InpShowArrows = _input('InpShowArrows', INPUT_YES)  # Show intersection arrows
InpUseMiddle = _input('InpUseMiddle', INPUT_NO)  # Allow midline intersections
InpUseAlerts = _input('InpUseAlerts', INPUT_NO)  # Use alerts
BufferRSI = Arr(0, 0.0)
BufferTop = Arr(0, 0.0)
BufferMiddle = Arr(0, 0.0)
BufferBottom = Arr(0, 0.0)
BufferArrUP = Arr(0, 0.0)
BufferArrDN = Arr(0, 0.0)
deviation = 0.0
period_rsi = 0
period_bb = 0
handle_rsi = 0

def OnInit():
    global deviation, handle_rsi, period_bb, period_rsi
    period_rsi = (1 if (InpPeriodRSI < 1) else InpPeriodRSI)
    period_bb = (1 if (InpPeriodBB < 1) else InpPeriodBB)
    deviation = InpDeviation
    SetIndexBuffer(0, BufferRSI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferTop, INDICATOR_DATA)
    SetIndexBuffer(2, BufferMiddle, INDICATOR_DATA)
    SetIndexBuffer(3, BufferBottom, INDICATOR_DATA)
    SetIndexBuffer(4, BufferArrUP, INDICATOR_DATA)
    SetIndexBuffer(5, BufferArrDN, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_ARROW, 158)
    PlotIndexSetInteger(5, PLOT_ARROW, 158)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Dynamic Zone RSI (' + _str(period_rsi) + ',' + _str(period_bb) + ',' + DoubleToString(deviation, 4) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferRSI, True)
    ArraySetAsSeries(BufferTop, True)
    ArraySetAsSeries(BufferMiddle, True)
    ArraySetAsSeries(BufferBottom, True)
    ArraySetAsSeries(BufferArrUP, True)
    ArraySetAsSeries(BufferArrDN, True)
    ResetLastError()
    handle_rsi = iRSI(None, PERIOD_CURRENT, period_rsi, PRICE_CLOSE)
    if handle_rsi == INVALID_HANDLE:
        Print('The iRSI (', _str(period_rsi), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_last_time
    ArraySetAsSeries(time, True)
    if rates_total < fmax(period_bb, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferRSI, EMPTY_VALUE)
        ArrayInitialize(BufferTop, EMPTY_VALUE)
        ArrayInitialize(BufferMiddle, EMPTY_VALUE)
        ArrayInitialize(BufferBottom, EMPTY_VALUE)
        ArrayInitialize(BufferArrUP, EMPTY_VALUE)
        ArrayInitialize(BufferArrDN, EMPTY_VALUE)
    count = (rates_total if (limit > 0) else 1)
    copied = 0
    copied = CopyBuffer(handle_rsi, 0, 0, count, BufferRSI)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferTop[i] = BandsOnArray(rates_total, i, period_bb, deviation, BufferRSI, UPPER_BAND)
        BufferMiddle[i] = BandsOnArray(rates_total, i, period_bb, deviation, BufferRSI, BASE_LINE)
        BufferBottom[i] = BandsOnArray(rates_total, i, period_bb, deviation, BufferRSI, LOWER_BAND)
        BufferArrDN[i] = EMPTY_VALUE
        BufferArrUP[i] = BufferArrDN[i]
        if InpShowArrows:
            if ((BufferRSI[i + 1] <= BufferTop[i + 1] and BufferRSI[i] > BufferTop[i]) or ((InpUseMiddle and BufferRSI[i + 1] <= BufferMiddle[i + 1]) and BufferRSI[i] > BufferMiddle[i])) or (BufferRSI[i + 1] <= BufferBottom[i + 1] and BufferRSI[i] > BufferBottom[i]):
                BufferArrUP[i] = BufferRSI[i]
            if ((BufferRSI[i + 1] >= BufferTop[i + 1] and BufferRSI[i] < BufferTop[i]) or ((InpUseMiddle and BufferRSI[i + 1] >= BufferMiddle[i + 1]) and BufferRSI[i] < BufferMiddle[i])) or (BufferRSI[i + 1] >= BufferBottom[i + 1] and BufferRSI[i] < BufferBottom[i]):
                BufferArrDN[i] = BufferRSI[i]
    if InpUseAlerts:
        if time[0] > _s_OnCalculate_last_time:
            if BufferRSI[0] > BufferTop[0] and BufferRSI[1] <= BufferTop[1]:
                Alert(Symbol() + ' ' + TimeframeToString(Period()) + ': RSI Above Top Band')
            if BufferRSI[0] < BufferBottom[0] and BufferRSI[1] >= BufferBottom[1]:
                Alert(Symbol() + ' ' + TimeframeToString(Period()) + ': RSI Below Bottom Band')
            _s_OnCalculate_last_time = TimeCurrent()
    return rates_total

def BandsOnArray(rates_total, index, period, deviation_bb, array, line, as_series=True):
    check_index = ((index <= (rates_total - period - 1)) if as_series else (index >= (period - 1)))
    if period < 1 or (not check_index):
        return 0.0
    dev = StdDevOnArray(rates_total, index, period, array)
    mid = 0.0
    for i in range(0, period):
        mid += array[index + i]
    mid = _fdiv(mid, period)
    top = mid + (dev * deviation_bb)
    btm = mid - (dev * deviation_bb)
    return (top if (line == UPPER_BAND) else btm if (line == LOWER_BAND) else mid)

def StdDevOnArray(rates_total, index, period, array, as_series=True):
    check_index = ((index <= (rates_total - period - 1)) if as_series else (index >= (period - 1)))
    if period < 1 or (not check_index):
        return 0.0
    avg = 0.0
    for i in range(0, period):
        avg += array[index + i]
    avg = _fdiv(avg, period)
    sd = 0.0
    for i in range(0, period):
        sd += (avg - array[index + i]) * (avg - array[index + i])
    return sqrt(_fdiv(sd, period))

def TimeframeToString(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7)

# ---- static local variables
_s_OnCalculate_last_time = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DynamicZoneRSI(_MQL5Indicator):
    name = 'Dynamic_Zone_RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodRSI': 5,  # RSI period
        'InpPeriodBB': 30,  # Bands period
        'InpDeviation': 1.3185,  # Deviation
        'InpShowArrows': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show intersection arrows
        'InpUseMiddle': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Allow midline intersections
        'InpUseAlerts': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Use alerts
    }

