"""candlestop_htf — converted from MQL5: MQL5 Indicators/CandleStop_HTF/candlestop_htf.mq5

CandleStop with the timeframe selection option available in input parameters
Copyright: Copyright © 2013, Nikolay Kositsin; Link: arria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2013, Nikolay Kositsin', 'link': 'arria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 1}, 'colors': {1: [16443110], 2: [3329330], 3: [13458026], 4: [9639167]}, 'widths': {2: 1, 3: 1, 4: 1}, 'styles': {2: 4, 3: 4, 4: 4}, 'labels': {1: 'Channel', 2: 'Support', 3: 'Middle', 4: 'Resistance'}, 'levels': [], 'description': ['CandleStop with the timeframe selection option available in input parameters'], 'name': 'candlestop_htf', 'source': 'MQL5 Indicators/CandleStop_HTF/candlestop_htf.mq5', 'folder': 'CandleStop_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Indicator chart period (timeframe)', 'sinput': False}, {'mql': 'UpTrailPeriods', 'py': 'UpTrailPeriods', 'param': 'UpTrailPeriods', 'type': 'uint', 'default': 5, 'label': 'High finding period', 'sinput': False}, {'mql': 'DnTrailPeriods', 'py': 'DnTrailPeriods', 'param': 'DnTrailPeriods', 'type': 'uint', 'default': 5, 'label': 'Low finding period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Indicator chart period (timeframe)
UpTrailPeriods = _input('UpTrailPeriods', 5)  # High finding period
DnTrailPeriods = _input('DnTrailPeriods', 5)  # Low finding period
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
UpIndBuffer = Arr(0, 0.0)
MdIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
UpChIndBuffer = Arr(0, 0.0)
DnChIndBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('CandleStop', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'CandleStop', UpTrailPeriods, DnTrailPeriods, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of the CandleStop indicator')
        return INIT_FAILED
    IndInit(0, UpChIndBuffer, INDICATOR_DATA)
    IndInit(1, DnChIndBuffer, INDICATOR_DATA)
    IndInit(2, UpIndBuffer, INDICATOR_DATA)
    IndInit(3, MdIndBuffer, INDICATOR_DATA)
    IndInit(4, DnIndBuffer, INDICATOR_DATA)
    PlotInit(0, 0.0, 0, Shift)
    PlotInit(1, 0.0, 0, Shift)
    PlotInit(2, 0.0, 0, Shift)
    PlotInit(3, 0.0, 0, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'CandleStop', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 1, UpChIndBuffer, 2, DnChIndBuffer, 1, UpIndBuffer, 0, MdIndBuffer, 2, DnIndBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def CountIndicator(Numb, Symb, TFrame, IndHandle, UpChBuffNumb, UpChIndBuf, DnChBuffNumb, DnChIndBuf, UpBuffNumb, UpIndBuf, MdBuffNumb, MdIndBuf, DnBuffNumb, DnIndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        UpChIndBuf[bar] = 0.0
        DnChIndBuf[bar] = 0.0
        UpIndBuf[bar] = 0.0
        MdIndBuf[bar] = 0.0
        DnIndBuf[bar] = 0.0
        if CopyTime(Symbol(), TFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            UpChArr = Arr(1, 0.0, dyn=False)
            DnChArr = Arr(1, 0.0, dyn=False)
            UpArr = Arr(1, 0.0, dyn=False)
            MdArr = Arr(1, 0.0, dyn=False)
            DnArr = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, UpChBuffNumb, _DT(iTime_[bar]), 1, UpChArr) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, DnChBuffNumb, _DT(iTime_[bar]), 1, DnChArr) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, UpBuffNumb, _DT(iTime_[bar]), 1, UpArr) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, MdBuffNumb, _DT(iTime_[bar]), 1, MdArr) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, DnBuffNumb, _DT(iTime_[bar]), 1, DnArr) <= 0:
                return (0 != 0)
            UpChIndBuf[bar] = UpChArr[0]
            DnChIndBuf[bar] = DnChArr[0]
            UpIndBuf[bar] = UpArr[0]
            MdIndBuf[bar] = MdArr[0]
            DnIndBuf[bar] = DnArr[0]
        else:
            UpChIndBuf[bar] = UpChIndBuf[bar + 1]
            DnChIndBuf[bar] = DnChIndBuf[bar + 1]
            UpIndBuf[bar] = UpIndBuf[bar + 1]
            MdIndBuf[bar] = MdIndBuf[bar + 1]
            DnIndBuf[bar] = DnIndBuf[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Print('Chart period for the ' + IndName + ' indicator cannot be less than the period of the current chart!')
        Print('You must change the indicator input parameters!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(1, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandlestopHtf(_MQL5Indicator):
    name = 'candlestop_htf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Indicator chart period (timeframe)
        'UpTrailPeriods': 5,  # High finding period
        'DnTrailPeriods': 5,  # Low finding period
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

